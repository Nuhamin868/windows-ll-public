# Implementation status — 2026-10-25

**PARTIALLY COMPLETE.** Current evidence supersedes the historical October 19 matrix. [Native Windows build and tests](https://github.com/Nuhamin868/windows-ll/actions/runs/40181027013) passed on October 25. Wine is reported separately. The original external rubric is unavailable.

| Requirement | Current evidence and remaining work |
|---|---|
| R01 PE parser | 5,059 portable checks including mutations passed; native Windows CLI inspection passed |
| R02 hashes | Native and Windows vectors/collision checks passed |
| R03 metadata/arguments | Native Windows JSON/Unicode/spaced arguments passed; historical ancestry/PID reuse acceptance pending |
| R04 mutex | Native duplicate rejection, release and reacquisition after forced termination passed; multiple sessions pending |
| R05 inventory | Native JSON, filter and architecture reporting passed; controlled access-denied cases pending |
| R06a local retrieval | Native valid/invalid inert artifact cases passed |
| R06b HTTPS | Implemented and cross-built; URL restrictions passed API units. Controlled fixture service and matrix runner added; live TLS matrix pending endpoint |
| R06c registry | Native valid/bad-tag/bad-schema, missing key/value, wrong type and >1 MiB rejection passed; concurrent mutation pending |
| R07 CNG AES-GCM/schema/wipe | Native Windows positive/negative API and CLI cases passed; portable Python reference checks passed |
| R08 defender research | Research only; synthetic correlations explicitly labeled |
| R09 development signing | osslsigncode signing, explicit trust verification, default trust rejection and tamper detection passed. External encrypted temporary key deleted. No public trust/timestamp/Windows Authenticode claim |
| R10 build/tests/package | Linux MinGW and fresh native Windows MinGW builds passed; source/unsigned/signed development artifacts and hashes provided |
| R11 source/evidence | RAII and source/test separation retained; current CI logs preserved |
| R12 documentation | Review, test plans, demonstration and TLS guide supplied |
| R13 curriculum | Existing defensive mapping/source inventory retained; operational course code not adopted |

Remaining: controlled trusted HTTPS and independently configured certificate-failure hosts; specialized denied access, PID reuse, concurrent registry changes and cross-session acceptance; verify original assignment rubric. Operational injection, payload execution, concealment and identity manipulation remain intentionally excluded.

## Acceptance continuation — 2026-10-26

Added a native-only runner for observed access-denied reporting, live launcher parent matching, process-churn inventory and concurrent registry mutation stress. Execution results are pending CI; neither forced PID reuse nor multiple-session acceptance is claimed. HTTPS endpoint/trust setup and external rubric remain requested inputs.
