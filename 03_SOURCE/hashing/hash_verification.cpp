#include "winll.hpp"
#include <array>
namespace winll {
bool verify_hashes() {
  constexpr std::array<std::string_view, 4> names = {
      "GetCurrentProcessId", "CreateMutexW", "CloseHandle", "GetCommandLineW"};
  constexpr std::array values = {hash_name(names[0]), hash_name(names[1]),
                                 hash_name(names[2]), hash_name(names[3])};
  for (std::size_t i = 0; i < names.size(); ++i) {
    if (hash_name(names[i]) != values[i])
      return false;
    for (std::size_t j = 0; j < i; ++j)
      if (values[i] == values[j])
        return false;
  }
  // A published FNV-1a collision demonstrates that matching hashes do not
  // identify a name.
  return hash_name("") == 2166136261u && hash_name("hello") == 0x4f9f2cabu &&
         hash_name("costarring") == hash_name("liquid");
}
} // namespace winll
