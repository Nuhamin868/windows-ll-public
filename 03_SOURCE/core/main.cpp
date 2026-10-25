#include "winll.hpp"
#include <exception>
int wmain(int argc, wchar_t **argv) {
  try {
    return winll::application(argc, argv);
  } catch (const std::exception &e) {
    winll::event("error", e.what());
    return 1;
  }
}
