#include "windows_support.hpp"
namespace winll {
MutexGuard::MutexGuard()
    : handle_(CreateMutexW(nullptr, FALSE,
                           L"Local\\WindowsLL.WINLL001.ResearchHarness")) {
  const auto error = GetLastError();
  if (!handle_.h)
    throw std::runtime_error("CreateMutexW failed: " + std::to_string(error));
  if (error == ERROR_ALREADY_EXISTS)
    throw std::runtime_error(
        "research harness already running in this session");
  // Lifetime of the open named object, rather than mutex ownership, gates this
  // session.
}
} // namespace winll
