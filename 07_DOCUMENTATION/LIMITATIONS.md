# Limitations

- No Windows VM or Wine was available at initial inspection. Windows API runtime behavior, concurrency, registry and CNG negative paths require the supplied native Windows suite.
- Controlled HTTPS success, invalid certificate, redirects, timeout, overflow, and disconnect behavior need a trusted test service. Do not substitute a random public artifact endpoint.
- Direct IsWow64Process2 requires Windows 10 1709 or newer. Older Windows 10 releases are not supported by this build.
- Mutex limits one instance per local session; it does not coordinate all sessions or prevent intentional precreation denial of service.
- Parent PID is a Toolhelp snapshot observation. No guarantee of creator identity or full historical ancestry; correlate external process lifetime logs.
- Inventory is case-sensitive substring filtering, point-in-time, and does not elevate privileges. Processes may disappear between enumeration and querying.
- PE inspection supports normal import directories, not delay imports, loader emulation, exhaustive bound import decoding, exports, signatures or all exotic PE layouts. Section names are restricted to printable ASCII.
- Public test keys provide no real secrecy. There is no secret vault, production enrollment, key rotation, replay protection, or general-purpose artifact format.
- Native ASan/UBSan tests exclude Win32 adapters; leak detection was disabled because it fails under agent tracing.
- The development signing workflow is not verified until osslsigncode is available. No signed build is claimed without a verification log.
- Local tools under `/tmp` are ephemeral. Reinstalling system dependencies is a separate user-approved operation.
- Offensive injection/spoofing is intentionally research only. This deliverable is not completion of an operational injection assignment.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
