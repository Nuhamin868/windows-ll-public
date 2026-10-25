> Latest status: [2026-10-25 submission review](../SUBMISSION_REVIEW.md). Expanded native Windows integration and development signing passed; controlled HTTPS and specialized acceptance remain pending. Older entries below are historical.

# Test results

Results recorded from actual host runs; raw evidence takes precedence over narrative. The full 2,350-file course-export index completed with 92 PDF/788 pages, 92 HTML and 21 text documents processed and zero parse errors; see `08_EVIDENCE/verification/maldev-academy-source-index.json`. This is corpus indexing evidence, not Windows runtime validation.

| Check | Actual result | Evidence |
|---|---|---|
| MinGW Windows x64 Release configure/build | PASS; CLI and three test/inspection executables produced | `08_EVIDENCE/build_logs/configure.log`, `build.log` |
| Portable native ASan/UBSan CTest | PASS, 1/1 test; 5,059 internal checks including 4,000 deterministic mutations | `08_EVIDENCE/test_logs/native-unit.log`, `native-detail.log` |
| LeakSanitizer | NOT VERIFIED; failed under tracing, then disabled | Environment report; native script explicitly sets detect_leaks=0 |
| Offline reference artifact | PASS, 13 SHA-256 fixture digests; valid AES-GCM, bad tag, wrong key, invalid schema, truncation | `08_EVIDENCE/test_logs/offline-reference.log` |
| Synthetic telemetry analysis | PASS, 2 educational correlations; every record synthetic | `08_EVIDENCE/test_logs/synthetic.log` |
| Static PE and import inspection | PASS, AMD64 PE32+, visible system APIs, NX/ASLR/high entropy | `08_EVIDENCE/verification/file.txt`, `objdump.txt`, `imports.json`, `static-checks.txt` |
| Two independent Release builds | PASS; identical bytes and SHA-256 using the same toolchain | `08_EVIDENCE/verification/static-checks.txt` |
| Script syntax / document links | See actual checker log; not runtime validation | `08_EVIDENCE/verification/documentation-checks.txt` |
| Windows units / native API / PowerShell integration | PASS in October 25 native CI; specialized acceptance pending | `08_EVIDENCE/windows-native-20261025/` |
| Controlled HTTPS matrix | PENDING; no controlled trusted endpoint supplied | TEST_PLAN.md |
| Development Authenticode | PASS explicit trust, default trust rejection and tamper detection under osslsigncode; no public trust claim | Code-signing workflow and release notes |

Python reference decryption is not proof of BCryptDecrypt runtime behavior. Native Windows suites established offline mutex, process, registry and CNG behavior. Controlled live WinHTTP and specialized acceptance remain pending. No genuine endpoint attack traces or screenshots were collected.

[Home](../README.md) · [Status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)

Session 002: repaired automatic temporary-tool discovery and made packaging require a successful build and available tests; see [session record](../09_SESSION_LOGS/SESSION_002.md). Target-platform validation remains pending.

## Submission review — 2026-10-23

Fresh MinGW x64 build and native ASan/UBSan suite passed. Wine passed 5,059 portable checks and 16 Windows API smoke cases (including CNG positive/negative cases, mutex, Unicode and process queries); see `08_EVIDENCE/test_logs/wine-api.log`. Wine is compatibility-layer evidence, not native Windows acceptance. A private GitHub prerelease includes complete source, the unsigned executable, and an offline validation bundle. The Windows validation workflow records actual native results separately.

System CMake, Ninja, MinGW, Wine, and osslsigncode are now available; the earlier missing-tool notes describe the original environment. No dependencies were installed during this review. Signing remains optional and untested, and the executable is unsigned. Controlled HTTPS validation and the extended Windows cases remain pending. Status remains PARTIALLY COMPLETE until those requirements have real evidence. See [demonstration guide](../07_DOCUMENTATION/DEMONSTRATION.md).

## Extended native validation — 2026-10-25

[Current-source Windows CI](https://github.com/Nuhamin868/windows-ll/actions/runs/40181027013) passed the fresh MinGW build, 31 integration/setup/cleanup cases, 5,059 portable checks, 16 API cases and the PowerShell suite including registry oversize/type/missing-value tests. Raw logs: `08_EVIDENCE/windows-native-20261025/`. Development signing/tamper checks also passed under osslsigncode. Live HTTPS and specialized acceptance remain pending.
