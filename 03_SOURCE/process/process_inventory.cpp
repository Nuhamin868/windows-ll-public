#include "windows_support.hpp"
#include <iostream>
#include <tlhelp32.h>
namespace winll {
void process_inventory(const std::wstring &filter) {
  Handle snap(CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0));
  wincheck(snap.h != INVALID_HANDLE_VALUE, "process snapshot");
  PROCESSENTRY32W e{};
  e.dwSize = sizeof e;
  wincheck(Process32FirstW(snap.h, &e), "Process32FirstW");
  do {
    if (std::wstring(e.szExeFile).find(filter) == std::wstring::npos)
      continue;
    Handle process(
        OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, e.th32ProcessID));
    USHORT pm = 0, nm = 0;
    std::string arch = "unknown";
    DWORD error = 0;
    if (process.h) {
      if (IsWow64Process2(process.h, &pm, &nm)) {
        auto m = pm ? pm : nm;
        arch = m == IMAGE_FILE_MACHINE_AMD64   ? "x64"
               : m == IMAGE_FILE_MACHINE_I386  ? "x86"
               : m == IMAGE_FILE_MACHINE_ARM64 ? "arm64"
                                               : "other";
      } else
        error = GetLastError();
    } else
      error = GetLastError();
    std::cout << "{\"event\":\"process\",\"pid\":" << e.th32ProcessID
              << ",\"name\":" << json_quote(utf8(e.szExeFile))
              << ",\"architecture\":" << json_quote(arch)
              << ",\"query_error\":" << error << "}\n";
  } while (Process32NextW(snap.h, &e));
  if (GetLastError() != ERROR_NO_MORE_FILES)
    wincheck(false, "Process32NextW");
}
} // namespace winll
