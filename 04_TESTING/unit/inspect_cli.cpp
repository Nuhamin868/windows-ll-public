#include "winll.hpp"
#include <iostream>
int main(int argc, char **argv) {
  try {
    if (argc != 2)
      return 2;
    std::cout << winll::pe_json(winll::inspect_pe(
                     winll::read_file(argv[1], 64 * 1024 * 1024)))
              << '\n';
    return 0;
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
