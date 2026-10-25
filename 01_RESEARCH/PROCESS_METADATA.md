# Process metadata analysis

The `metadata` command reports GetCurrentProcessId, Toolhelp's reported parent PID, GetCommandLineW, and the C runtime's parsed wide-character arguments. Snapshot values can race process exit or PID reuse. Parent fields should not be equated with a trustworthy creator history.

Windows permits process-creation attributes, including a selected parent, under documented access constraints. This harness neither selects a parent nor mutates another process's command-line data. See [Microsoft's attribute documentation](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute) and the research-only [detection analysis](EVASION_TECHNIQUES.md).

Validation: preserve metadata JSON, launcher information and OS version from a standard-user Windows run. Compare the observed parent with that launcher while recording process creation times externally. No real Windows ancestry output is fabricated here.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
