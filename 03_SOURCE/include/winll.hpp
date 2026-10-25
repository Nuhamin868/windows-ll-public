#pragma once
#include <cstdint>
#include <filesystem>
#include <span>
#include <string>
#include <string_view>
#include <vector>
namespace winll {
using Bytes = std::vector<unsigned char>;
constexpr std::uint32_t hash_name(std::string_view s) {
  std::uint32_t h = 2166136261u;
  for (unsigned char c : s) {
    h ^= c;
    h *= 16777619u;
  }
  return h;
}
static_assert(hash_name("hello") == 0x4f9f2cabu);
struct Import {
  std::string dll;
  std::vector<std::string> functions;
};
struct Section {
  std::string name;
  std::uint32_t rva, virtual_size, raw, size;
};
struct PeReport {
  bool x64;
  std::uint16_t machine;
  std::vector<Section> sections;
  std::vector<Import> imports;
};
Bytes read_file(const std::filesystem::path &, std::size_t limit = 1024 * 1024);
PeReport inspect_pe(std::span<const unsigned char>);
std::string pe_json(const PeReport &);
std::string json_quote(std::string_view);
bool verify_hashes();
bool valid_schema(std::span<const unsigned char>);
void event(std::string_view name, std::string_view detail);
#ifdef _WIN32
Bytes retrieve_registry();
Bytes retrieve_https(const std::wstring &url, const std::wstring &allowed_host);
void validate_artifact(const Bytes &, Bytes key);
void process_metadata();
void process_inventory(const std::wstring &filter);
int application(int, wchar_t **);
#endif
} // namespace winll
