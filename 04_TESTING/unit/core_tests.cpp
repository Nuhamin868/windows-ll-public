#include "winll.hpp"
#include <iostream>
#include <random>
#include <stdexcept>
using namespace winll;
void require(bool c, const char *msg) {
  if (!c)
    throw std::runtime_error(msg);
}
int main(int argc, char **argv) {
  try {
    if (argc != 2)
      throw std::runtime_error("fixture path required");
    std::filesystem::path root = argv[1];
    unsigned checks = 0;
    auto check = [&](bool b, const char *msg) {
      require(b, msg);
      ++checks;
    };
    check(verify_hashes(), "hash vectors/collision");
    for (const auto *name : {"pe32.bin", "pe64.bin"}) {
      auto b = read_file(root / name);
      auto p = inspect_pe(b);
      check(p.x64 == (std::string(name) == "pe64.bin"), "format");
      check(p.sections.size() == 1, "sections");
      check(p.imports.size() == 1, "DLL count");
      check(p.imports[0].dll == "KERNEL32.dll", "DLL");
      check(p.imports[0].functions ==
                std::vector<std::string>{"GetCurrentProcessId", "ordinal:7"},
            "name/ordinal imports");
      check(pe_json(p).find("GetCurrentProcessId") != std::string::npos,
            "JSON report");
      // OriginalFirstThunk fallback and a legitimately absent import directory.
      b[512] = b[513] = b[514] = b[515] = 0;
      check(inspect_pe(b).imports.size() == 1, "IAT fallback");
      auto d = p.x64 ? 112u : 96u;
      for (unsigned i = 0; i < 8; ++i)
        b[152 + d + 8 + i] = 0;
      check(inspect_pe(b).imports.empty(), "no imports");
    }
    for (const auto *name : {"bad_mz.bin", "bad_rva.bin", "bad_descriptor.bin",
                             "bad_ordinal.bin", "bad_directories.bin"}) {
      bool rejected = false;
      try {
        inspect_pe(read_file(root / name));
      } catch (const std::runtime_error &) {
        rejected = true;
      }
      check(rejected, name);
    }
    auto b = read_file(root / "pe64.bin");
    for (std::size_t n = 0; n < b.size(); ++n) {
      bool rejected = false;
      try {
        inspect_pe(std::span(b).first(n));
      } catch (const std::runtime_error &) {
        rejected = true;
      }
      check(rejected, "truncation accepted");
    }
    auto encoded = Bytes{'W', 'L', 'L', 'D', 1, 1, 0, 'A'};
    check(valid_schema(encoded), "schema valid");
    for (std::size_t n = 0; n < encoded.size(); ++n)
      check(!valid_schema(std::span(encoded).first(n)), "schema truncation");
    encoded[7] = 0;
    check(!valid_schema(encoded), "schema control character");
    encoded[7] = 'A';
    encoded.push_back('B');
    check(!valid_schema(encoded), "schema trailing byte");
    check(json_quote("\"\n\\") == "\"\\\"\\n\\\\\"" ||
              json_quote("\"\n\\") == "\"\\\"\\u000a\\\\\"",
          "JSON escaping");
    bool oversized = false;
    try {
      read_file(root / "pe64.bin", 16);
    } catch (const std::runtime_error &) {
      oversized = true;
    }
    check(oversized, "file limit");
    // Fixed-seed malformed corpus: safety check under ASan/UBSan, not a claim
    // of exhaustive fuzzing.
    std::mt19937 rng(1001);
    for (unsigned i = 0; i < 4000; ++i) {
      auto fuzz = b;
      for (unsigned j = 0; j < 8; ++j)
        fuzz[rng() % fuzz.size()] = static_cast<unsigned char>(rng());
      try {
        inspect_pe(fuzz);
      } catch (const std::runtime_error &) {
      }
      ++checks;
    }
    std::cout << "PASS " << checks << " checks (including 4000 mutations)\n";
    return 0;
  } catch (const std::exception &e) {
    std::cerr << "FAIL " << e.what() << '\n';
    return 1;
  }
}
