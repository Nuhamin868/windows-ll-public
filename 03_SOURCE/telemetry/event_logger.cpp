#include "winll.hpp"
#include <iostream>
namespace winll {
void event(std::string_view name, std::string_view detail) {
  std::cerr << "{\"event\":" << json_quote(name)
            << ",\"detail\":" << json_quote(detail) << "}\n";
}
} // namespace winll
