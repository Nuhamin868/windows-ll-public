> Latest status: [2026-10-25 submission review](SUBMISSION_REVIEW.md). Expanded native Windows integration and development signing passed; controlled HTTPS and specialized acceptance remain pending. Older entries below are historical.

# Windows LL

WINLL-001 · Windows internals research harness · C++20 · Windows x64 · deadline 2026-10-25.

Inspect PE imports, verify compile-time hashes, observe process metadata, enumerate processes, enforce a single session instance, and authenticate inert encrypted artifacts. The harness never loads or executes artifact contents. Native Windows offline suites passed. Consult the [status matrix](00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md) for measured results.

## Build and test

Required host tools: CMake 3.20+, Ninja, MinGW-w64 GCC, Python 3 with `cryptography`, Git. Optional: Wine and osslsigncode. Dependency installation requires separate approval; scripts never install tools.

```bash
cd "$HOME/Projects/Windows LL"
bash 05_BUILD/scripts/check_environment.sh
bash 05_BUILD/scripts/build.sh
bash 05_BUILD/scripts/test.sh
bash 05_BUILD/scripts/package.sh
```

Native tests compile only the platform-independent parser/hash/schema code, under ASan/UBSan. LeakSanitizer is disabled in the script because the agent tracing environment prevents it from running. Windows components compile exclusively into PE executables. `build/windows/windows_ll.exe` is the CLI; `build/windows/winll_unit.exe` contains portable unit tests compiled for Windows.

The session uses temporary, signature-verified tools under `/tmp/winll-tools/root` because system CMake/MinGW are missing. To use them while present:

```bash
export PATH="/tmp/winll-tools/root/usr/bin:$PATH"
export LD_LIBRARY_PATH="/tmp/winll-tools/root/usr/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

Build/test scripts automatically discover these temporary tools when system dependencies are missing. Set `WINLL_TOOLS_ROOT` to use another extracted toolchain root. Packaging reruns the build and tests and stops on failure.

The temporary tools are not a persistent installation. See the [environment report](08_EVIDENCE/verification/ENVIRONMENT_REPORT.md) and [build guide](05_BUILD/BUILD_GUIDE.md).

## Windows usage

Run from the project root in PowerShell on Windows 10 **1709 or newer**, or Windows 11 x64:

```powershell
.\build\windows\windows_ll.exe hash
.\build\windows\windows_ll.exe metadata
.\build\windows\windows_ll.exe processes explorer > processes.jsonl
.\build\windows\windows_ll.exe pe .\build\windows\windows_ll.exe > imports.json
.\build\windows\windows_ll.exe artifact .\04_TESTING\test_data\artifact.bin .\04_TESTING\test_data\test-key.bin
.\04_TESTING\integration\windows_validation.ps1
```

`processes [filter]` matches a case-sensitive substring. Unknown/denied architecture queries include the Windows error code. `metadata` reports observed parent PID and this application's command line; this is not proof of original process creation identity. JSON reports go to stdout and diagnostic events to stderr; shell redirection explicitly exports only the chosen report.

`registry KEYFILE` reads only HKCU `Software\\WindowsLL\\TestArtifacts`, REG_BINARY value `Data`. `https URL ALLOWED_HOST KEYFILE` requires HTTPS port 443 and an exact, explicitly supplied DNS host; TLS validation stays enabled, redirects and URL credentials are rejected. No host is trusted implicitly. Only use an endpoint you administer. No successful live HTTPS test is claimed.

The fixture key and nonce are public test vectors. Fixtures contain a versioned ASCII data record, not PE code. Decrypted bytes are authenticated before schema inspection, wiped from application buffers, and never exported. Envelope format and limits: [implementation details](07_DOCUMENTATION/IMPLEMENTATION_DETAILS.md).

## Knowledge base

The [course-informed knowledge base](01_RESEARCH/MALDEV_ACADEMY_KNOWLEDGE_BASE.md) maps the user-supplied Maldev Academy curriculum to this defensive harness. Its source index fingerprints all 2,350 export files and indexes lecture/prompt text without importing bundled code. See the [architecture alignment](02_ARCHITECTURE/COURSE_ALIGNMENT.md).

- [Requirements](00_PROJECT_MANAGEMENT/REQUIREMENTS.md), [tasks](00_PROJECT_MANAGEMENT/MASTER_TASK_LIST.md), [roadmap](00_PROJECT_MANAGEMENT/DEVELOPMENT_ROADMAP.md)
- [Architecture](02_ARCHITECTURE/SYSTEM_OVERVIEW.md), [threat model](02_ARCHITECTURE/THREAT_MODEL.md)
- [Module reference](07_DOCUMENTATION/MODULE_REFERENCE.md), [technical report](07_DOCUMENTATION/TECHNICAL_REPORT.md)
- [Test results](04_TESTING/TEST_RESULTS.md), [validation report](04_TESTING/VALIDATION_REPORT.md)
- [Research](01_RESEARCH/EVASION_TECHNIQUES.md), [references](01_RESEARCH/MALDEV_REFERENCES.md)
- [Release notes](06_RELEASE/RELEASE_NOTES.md), [limitations](07_DOCUMENTATION/LIMITATIONS.md), [submission checklist](07_DOCUMENTATION/FINAL_SUBMISSION.md)
- [Session record](09_SESSION_LOGS/SESSION_001.md)

Open this folder as an Obsidian vault. Markdown links are relative; no plugin is required.

## Submission review — 2026-10-23

Fresh MinGW x64 build and native ASan/UBSan suite passed. Wine passed 5,059 portable checks and 16 Windows API smoke cases (including CNG positive/negative cases, mutex, Unicode and process queries); see `08_EVIDENCE/test_logs/wine-api.log`. Wine is compatibility-layer evidence, not native Windows acceptance. A private GitHub prerelease includes complete source, the unsigned executable, and an offline validation bundle. The Windows validation workflow records actual native results separately.

System CMake, Ninja, MinGW, Wine, and osslsigncode are now available; the earlier missing-tool notes describe the original environment. No dependencies were installed during this review. Signing remains optional and untested, and the executable is unsigned. Controlled HTTPS validation and the extended Windows cases remain pending. See [demonstration guide](07_DOCUMENTATION/DEMONSTRATION.md).
