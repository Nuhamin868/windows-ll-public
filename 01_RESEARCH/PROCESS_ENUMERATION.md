# Read-only process enumeration

The implementation snapshots processes with Toolhelp and queries architecture through a PROCESS_QUERY_LIMITED_INFORMATION handle. Access failure emits `unknown` with a numeric error. The filter is a case-sensitive substring of the process name; stdout JSONL is the export format.

Direct [IsWow64Process2](https://learn.microsoft.com/en-us/windows/win32/api/wow64apiset/nf-wow64apiset-iswow64process2) imposes a Windows 10 1709 minimum. A process can exit after its snapshot entry was read. No memory-write, thread-context or synchronization access is requested for enumerated processes. Windows runtime cases cover own-process matching and standard-user denied queries; they remain pending until actually executed.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
