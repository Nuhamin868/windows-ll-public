#include "windows_support.hpp"
#include <iostream>
#include <tlhelp32.h>
namespace winll {
void process_metadata() {
  const DWORD pid = GetCurrentProcessId();
  Handle snapshot(CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0));
  wincheck(snapshot.h != INVALID_HANDLE_VALUE, "process snapshot");
  PROCESSENTRY32W e{};
  e.dwSize = sizeof e;
  wincheck(Process32FirstW(snapshot.h, &e), "Process32FirstW");
  DWORD parent = 0;
  bool found = false;
  do {
    if (e.th32ProcessID == pid) {
      parent = e.th32ParentProcessID;
      found = true;
      break;
    }
  } while (Process32NextW(snapshot.h, &e));
  if (!found)
    throw std::runtime_error("current process missing from snapshot");
  std::cout << "{\"event\":\"metadata\",\"pid\":" << pid
            << ",\"reported_parent_pid\":" << parent
            << ",\"command_line\":" << json_quote(utf8(GetCommandLineW()))
            << "}\n";
}
} // namespace winll
