#include "winll.hpp"
namespace winll {
bool valid_schema(std::span<const unsigned char> b) {
  // WLLD, version 1, little-endian uint16 text length, printable ASCII
  // (1..256).
  if (b.size() < 7 || b[0] != 'W' || b[1] != 'L' || b[2] != 'L' ||
      b[3] != 'D' || b[4] != 1)
    return false;
  auto n = static_cast<unsigned>(b[5]) + (static_cast<unsigned>(b[6]) << 8);
  if (n == 0 || n > 256 || b.size() != 7 + n)
    return false;
  for (std::size_t i = 7; i < b.size(); ++i)
    if (b[i] < 32 || b[i] > 126)
      return false;
  return true;
}
} // namespace winll
