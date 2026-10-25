#include "winll.hpp"
#include <algorithm>
#include <limits>
#include <sstream>
#include <stdexcept>
namespace winll {
namespace {
struct Reader {
  std::span<const unsigned char> b;
  void bounds(std::size_t p, std::size_t n) const {
    if (p > b.size() || n > b.size() - p)
      throw std::runtime_error("PE: truncated range");
  }
  std::uint64_t u(std::size_t p, unsigned n) const {
    bounds(p, n);
    std::uint64_t v = 0;
    for (unsigned i = 0; i < n; ++i)
      v |= std::uint64_t(b[p + i]) << (8 * i);
    return v;
  }
};
} // namespace
PeReport inspect_pe(std::span<const unsigned char> b) {
  Reader r{b};
  if (r.u(0, 2) != 0x5a4d)
    throw std::runtime_error("PE: missing MZ");
  auto nt = static_cast<std::size_t>(r.u(0x3c, 4));
  r.bounds(nt, 24);
  if (nt < 64 || r.u(nt, 4) != 0x4550)
    throw std::runtime_error("PE: invalid NT signature");
  auto count = r.u(nt + 6, 2), optsize = r.u(nt + 20, 2);
  auto opt = nt + 24;
  r.bounds(opt, optsize);
  auto magic = r.u(opt, 2);
  bool x64 = magic == 0x20b;
  if (magic != 0x10b && !x64)
    throw std::runtime_error("PE: unsupported optional header");
  std::size_t dir = x64 ? 112 : 96;
  if (optsize < dir || count == 0 || count > 96)
    throw std::runtime_error("PE: invalid header or section count");
  auto dirs = r.u(opt + dir - 4, 4);
  if (dirs > (optsize - dir) / 8)
    throw std::runtime_error("PE: data directory exceeds optional header");
  auto headers = r.u(opt + 60, 4), image = r.u(opt + 56, 4);
  auto st = opt + optsize;
  r.bounds(st, static_cast<std::size_t>(count) * 40);
  if (headers < st + count * 40 || headers > b.size() || image < headers)
    throw std::runtime_error("PE: invalid image/header size");
  PeReport out{x64, static_cast<std::uint16_t>(r.u(nt + 4, 2)), {}, {}};
  for (std::size_t i = 0; i < count; ++i) {
    auto s = st + i * 40;
    std::string name;
    for (unsigned j = 0; j < 8 && b[s + j]; ++j) {
      if (b[s + j] < 32 || b[s + j] > 126)
        throw std::runtime_error("PE: non-ASCII section name unsupported");
      name += static_cast<char>(b[s + j]);
    }
    Section sec{name, static_cast<std::uint32_t>(r.u(s + 12, 4)),
                static_cast<std::uint32_t>(r.u(s + 8, 4)),
                static_cast<std::uint32_t>(r.u(s + 20, 4)),
                static_cast<std::uint32_t>(r.u(s + 16, 4))};
    if (sec.size)
      r.bounds(sec.raw, sec.size);
    auto extent = std::max(sec.virtual_size, sec.size);
    if (sec.rva < headers || sec.rva > image || extent > image - sec.rva ||
        (sec.size && sec.raw < headers))
      throw std::runtime_error("PE: invalid section range");
    for (const auto &prev : out.sections) {
      if (std::uint64_t(sec.rva) < std::uint64_t(prev.rva) +
                                       std::max(prev.virtual_size, prev.size) &&
          std::uint64_t(prev.rva) < std::uint64_t(sec.rva) + extent)
        throw std::runtime_error("PE: overlapping RVA ranges");
      if (sec.size && prev.size &&
          std::uint64_t(sec.raw) < std::uint64_t(prev.raw) + prev.size &&
          std::uint64_t(prev.raw) < std::uint64_t(sec.raw) + sec.size)
        throw std::runtime_error("PE: overlapping raw ranges");
    }
    out.sections.push_back(sec);
  }
  auto offset = [&](std::uint64_t v, std::size_t n) -> std::size_t {
    if (v > UINT32_MAX || n > UINT32_MAX - v)
      throw std::runtime_error("PE: RVA overflow");
    if (v < headers && n <= headers - v) {
      r.bounds(static_cast<std::size_t>(v), n);
      return static_cast<std::size_t>(v);
    }
    for (const auto &s : out.sections)
      if (v >= s.rva && v - s.rva < s.size && n <= s.size - (v - s.rva))
        return s.raw + static_cast<std::size_t>(v - s.rva);
    throw std::runtime_error("PE: RVA is not file backed");
  };
  auto str = [&](std::uint64_t v) {
    std::string s;
    for (unsigned i = 0; i < 4096; ++i) {
      auto c = b[offset(v + i, 1)];
      if (!c)
        return s;
      if (c < 32 || c > 126)
        throw std::runtime_error("PE: invalid import string");
      s += static_cast<char>(c);
    }
    throw std::runtime_error("PE: unterminated string");
  };
  if (dirs < 2)
    return out;
  auto irva = r.u(opt + dir + 8, 4), isz = r.u(opt + dir + 12, 4);
  if (!irva && !isz)
    return out;
  if (!irva || isz < 20 || isz > 1024 * 1024)
    throw std::runtime_error("PE: invalid import directory");
  offset(irva, static_cast<std::size_t>(isz));
  bool end = false;
  for (std::uint64_t k = 0; k + 20 <= isz; k += 20) {
    auto d = offset(irva + k, 20);
    bool zero = true;
    for (unsigned j = 0; j < 20; ++j)
      zero &= b[d + j] == 0;
    if (zero) {
      end = true;
      break;
    }
    if (out.imports.size() >= 1024)
      throw std::runtime_error("PE: too many imports");
    auto lookup = r.u(d, 4);
    if (!lookup)
      lookup = r.u(d + 16, 4);
    if (!lookup)
      throw std::runtime_error("PE: missing thunk");
    Import imp{str(r.u(d + 12, 4)), {}};
    if (imp.dll.empty())
      throw std::runtime_error("PE: empty DLL name");
    bool term = false;
    for (std::uint64_t j = 0; j < 65536; ++j) {
      auto v =
          r.u(offset(lookup + j * (x64 ? 8 : 4), x64 ? 8 : 4), x64 ? 8 : 4);
      if (!v) {
        term = true;
        break;
      }
      const auto flag = x64 ? (1ull << 63) : (1ull << 31);
      if (v & flag) {
        if (v & ~(flag | 0xffffull))
          throw std::runtime_error("PE: invalid ordinal thunk");
        imp.functions.push_back("ordinal:" + std::to_string(v & 0xffff));
      } else {
        if (v > UINT32_MAX)
          throw std::runtime_error("PE: invalid name RVA");
        offset(v, 2);
        auto name = str(v + 2);
        if (name.empty())
          throw std::runtime_error("PE: empty function name");
        imp.functions.push_back(name);
      }
    }
    if (!term)
      throw std::runtime_error("PE: unterminated thunk table");
    out.imports.push_back(std::move(imp));
  }
  if (!end)
    throw std::runtime_error("PE: unterminated import descriptors");
  return out;
}
std::string pe_json(const PeReport &p) {
  std::ostringstream o;
  o << "{\"format\":\"" << (p.x64 ? "PE32+" : "PE32")
    << "\",\"machine\":" << p.machine << ",\"sections\":[";
  bool first = true;
  for (const auto &s : p.sections) {
    if (!first)
      o << ',';
    first = false;
    o << "{\"name\":" << json_quote(s.name) << ",\"rva\":" << s.rva
      << ",\"raw_offset\":" << s.raw << ",\"raw_size\":" << s.size << '}';
  }
  o << "],\"imports\":[";
  first = true;
  for (const auto &i : p.imports) {
    if (!first)
      o << ',';
    first = false;
    o << "{\"dll\":" << json_quote(i.dll) << ",\"functions\":[";
    bool f = true;
    for (const auto &n : i.functions) {
      if (!f)
        o << ',';
      f = false;
      o << json_quote(n);
    }
    o << "]}";
  }
  o << "]}";
  return o.str();
}
} // namespace winll
