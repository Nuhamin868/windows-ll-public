# Master task list

## Completed

- [x] Inspect OS, tools, existing Projects directory and project absence; preserve initial report.
- [x] Create project hierarchy, CMake cross-toolchain, coding rules and Git exclusions.
- [x] Implement bounded PE inspection and constexpr hash verification with deterministic tests.
- [x] Implement metadata, session mutex, process inventory and filtered JSONL export.
- [x] Implement capped local/HKCU/explicit-allowlist HTTPS retrieval and structured diagnostics.
- [x] Implement CNG AES-GCM authentication, strict inert schema and explicit buffer wiping.
- [x] Generate harmless PE and encrypted fixtures, wrong-key/tag/schema/truncation cases.
- [x] Author Windows API unit and PowerShell integration suites; cross-compile targets.
- [x] Run portable sanitizer/reference/synthetic tests; capture evidence.
- [x] Document six research-only subjects, architecture, module references and limitations.
- [x] Build Windows x64 binaries, inspect PE imports and prepare unsigned development package.
- [x] Document optional signing and missing tool; maintain status and session records.

- [x] Index all 2,350 supplied course-export files and align lecture modules to the defensive architecture.

## Remaining verification

- [x] Run original and expanded native Windows portable/API/CLI/registry/mutex suites (October 25 CI passed).
- [ ] Review process JSONL, ancestry/PID reuse, denied access, Unicode and multiple sessions.
- [ ] Run controlled HTTPS positive, authentication, certificate, redirects, status, cap, timeout and disconnect cases.
- [x] Test registry missing/oversize/wrong-type values on Windows.
- [ ] Test concurrent registry changes under controlled conditions.
- [ ] Fix observed Windows failures and repeat affected checks.
- [x] Test development sign/verify/default trust/tamper detection; delete temporary encrypted external key.
- [ ] Update validation/release/status records and final acceptance checklist from actual results.

Operational injection/spoofing implementations are intentionally excluded and are not remaining tasks.

[Home](../README.md) · [Status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)

Session 002: repaired automatic temporary-tool discovery and made packaging require a successful build and available tests; see [session record](../09_SESSION_LOGS/SESSION_002.md). Target-platform validation remains pending.

## Submission review — 2026-10-23

Fresh MinGW x64 build and native ASan/UBSan suite passed. Wine passed 5,059 portable checks and 16 Windows API smoke cases (including CNG positive/negative cases, mutex, Unicode and process queries); see `08_EVIDENCE/test_logs/wine-api.log`. Wine is compatibility-layer evidence, not native Windows acceptance. A private GitHub prerelease includes complete source, the unsigned executable, and an offline validation bundle. The Windows validation workflow records actual native results separately.

System CMake, Ninja, MinGW, Wine, and osslsigncode are now available; the earlier missing-tool notes describe the original environment. No dependencies were installed during this review. Signing remains optional and untested, and the executable is unsigned. Controlled HTTPS validation and the extended Windows cases remain pending. Status remains PARTIALLY COMPLETE until those requirements have real evidence. See [demonstration guide](../07_DOCUMENTATION/DEMONSTRATION.md).

2026-10-25: added the 31-case Wine integration runner, controlled HTTPS fixture service/runner, fresh-source native CI, extended registry tests and verified development signing. See [latest review](../SUBMISSION_REVIEW.md). Live TLS and extended native acceptance remain pending.

2026-10-26: authored native-only access-denied, parent-observation, process-churn and concurrent-registry stress probes; native CI execution pending. PID reuse, multiple sessions, TLS setup and external rubric remain open.
