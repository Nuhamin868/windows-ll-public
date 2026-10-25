
#include "windows_support.hpp"
#include <functional>
#include <iostream>
using namespace winll;
int main(int argc, char **argv) {
  try {
    if (argc != 2)
      throw std::runtime_error("fixture path required");
    std::filesystem::path root = argv[1];
    unsigned n = 0;
    auto reject = [&](const std::function<void()> &f) {
      bool caught = false;
      try {
        f();
      } catch (const std::exception &) {
        caught = true;
      }
      if (!caught)
        throw std::runtime_error("negative case accepted");
      ++n;
    };
    const auto key = read_file(root / "test-key.bin", 32);
    validate_artifact(read_file(root / "artifact.bin"), key);
    ++n;
    for (const auto *name :
         {"bad-tag.bin", "bad-schema.bin", "truncated-artifact.bin"})
      reject([&] { validate_artifact(read_file(root / name), key); });
    reject([&] {
      validate_artifact(read_file(root / "artifact.bin"),
                        read_file(root / "wrong-key.bin", 32));
    });
    reject([&] {
      validate_artifact(read_file(root / "artifact.bin"), Bytes(31));
    });
    for (const auto *url :
         {L"http://example.invalid/a", L"https://other.invalid/a",
          L"https://example.invalid:444/a",
          L"https://user:pass@example.invalid/a",
          L"https://example.invalid/a#fragment"})
      reject([&] { retrieve_https(url, L"example.invalid"); });
    reject([&] { retrieve_https(L"https://example.invalid/a", L""); });
    {
      MutexGuard first;
      reject([] { MutexGuard second; });
    }
    {
      MutexGuard again;
      ++n;
    }
    if (utf8(L"\u03bb") != "\xce\xbb")
      throw std::runtime_error("Unicode conversion");
    ++n;
    process_metadata();
    process_inventory(L"winll_windows_unit");
    ++n;
    std::cout << "PASS " << n << " Windows API unit/smoke cases\n";
    return 0;
  } catch (const std::exception &e) {
    std::cerr << "FAIL " << e.what() << '\n';
    return 1;
  }
}
