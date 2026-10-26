# Remaining acceptance procedure

## HTTPS prerequisites

Use a controlled TLS endpoint with an already trusted certificate, or explicitly approve temporary certificate trust on a disposable Windows test runner. Never disable WinHTTP certificate validation. Existing `https_fixture_server.py` and `https_validation.py` provide the service and matrix. For certificate-negative cases, preserve each server certificate and its independently checked validity, hostname and issuer so a generic connection failure cannot be mistaken for a particular TLS result.

## Separate Windows sessions

Use an existing isolated Windows machine with two signed-in sessions. A different terminal window in the same session is insufficient. Do not create accounts or change session configuration as part of the test without authorization.

1. Record `query session` output and OS build in both sessions; confirm different session IDs.
2. In session A, start `build/windows/windows_ll.exe hold 30000`. Wait for its `acquired` diagnostic.
3. While that process is alive, run `build/windows/windows_ll.exe hash` in another terminal in session A. Require rejection with `already running in this session`.
4. While the same holder remains alive, run `build/windows/windows_ll.exe hash` in session B. Require success.
5. Wait for the holder to exit; require `hash` to succeed again in session A.
6. Preserve commands, timestamps, session IDs, stderr and exit codes. If the holder exits before step 4, repeat; no cross-session result can be claimed.

The application uses `Local\WindowsLL.WINLL001.ResearchHarness`, so the intended limit is per session. API basis: [kernel object namespaces](https://learn.microsoft.com/en-us/windows/win32/termserv/kernel-object-namespaces).

## PID reuse and ancestry

The application reports snapshot parent PID and labels it `reported_parent_pid`; it does not prove historical creation identity. The native stress runner compares the observed parent with the still-live launcher and inventories during process creation/exit. Its report records repeated child PIDs if they occur. Neither ordinary churn nor a live-parent match proves behavior under actual parent PID reuse. A controlled run must record original process creation/exit times and an actual reused PID before claiming that coverage. Do not manipulate the reported parent or spoof process identity to simulate a pass.

API basis: [process identifiers can be reused](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.process.id) and [process handles and identifiers](https://learn.microsoft.com/en-us/windows/win32/procthread/process-handles-and-identifiers).

## Assignment compliance

The original instructor rubric is required. The repository's internal requirements are not a substitute. Match each supplied rubric item to implementation, executable behavior, test evidence and explicit limitations before declaring assignment completion.
