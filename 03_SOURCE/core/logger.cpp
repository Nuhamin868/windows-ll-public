#include "winll.hpp"
#include <fstream>
#include <stdexcept>
namespace winll {
Bytes read_file(const std::filesystem::path &path, std::size_t limit) {
  std::ifstream f(path, std::ios::binary);
  if (!f)
    throw std::runtime_error("cannot open file");
  Bytes b;
  char chunk[4096];
  while (f) {
    f.read(chunk, sizeof chunk);
    auto n = static_cast<std::size_t>(f.gcount());
    if (n > limit - b.size())
      throw std::runtime_error("file exceeds size limit");
    b.insert(b.end(), chunk, chunk + n);
  }
  if (!f.eof())
    throw std::runtime_error("file read failed");
  return b;
}
std::string json_quote(std::string_view s) {
  constexpr char hex[] = "0123456789abcdef";
  std::string o = "\"";
  for (unsigned char c : s) {
    if (c == '"' || c == '\\') {
      o += '\\';
      o += static_cast<char>(c);
    } else if (c < 32) {
      o += "\\u00";
      o += hex[c >> 4];
      o += hex[c & 15];
    } else
      o += static_cast<char>(c);
  }
  return o + '"';
}
} // namespace winll
