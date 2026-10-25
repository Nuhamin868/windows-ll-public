#pragma once
#include "winll.hpp"
#include <stdexcept>
#include <windows.h>
namespace winll {
struct Handle {
  HANDLE h = nullptr;
  explicit Handle(HANDLE v = nullptr) : h(v) {}
  ~Handle() {
    if (h && h != INVALID_HANDLE_VALUE)
      CloseHandle(h);
  }
  Handle(const Handle &) = delete;
  Handle &operator=(const Handle &) = delete;
};
inline void wincheck(bool ok, const char *operation) {
  if (!ok)
    throw std::runtime_error(std::string(operation) + ": Windows error " +
                             std::to_string(GetLastError()));
}
inline std::string utf8(std::wstring_view v) {
  if (v.empty())
    return {};
  auto n = WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, v.data(),
                               static_cast<int>(v.size()), nullptr, 0, nullptr,
                               nullptr);
  wincheck(n > 0, "UTF-8 conversion");
  std::string s(n, '\0');
  wincheck(WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, v.data(),
                               static_cast<int>(v.size()), s.data(), n, nullptr,
                               nullptr) > 0,
           "UTF-8 conversion");
  return s;
}
class MutexGuard {
  Handle handle_;

public:
  MutexGuard();
};
} // namespace winll
