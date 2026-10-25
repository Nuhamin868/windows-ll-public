# Module reference

Each module records objectives, implementation and the verification boundary. Build evidence is centralized in [test results](../04_TESTING/TEST_RESULTS.md). A cross-build is never a runtime result.

## Module 01 — PE parser

- Objective: Inspect PE32/PE32+ headers, sections and normal imports.
- Design / implementation: Bounded bytewise reader, conservative RVA/overlap checks, name/ordinal imports and JSON.
- Source references: `03_SOURCE/pe/pe_inspector.cpp`.
- APIs / dependencies: None; portable standard library.
- Build result: see [build evidence](../04_TESTING/TEST_RESULTS.md); Windows code builds exclusively with MinGW.
- Test procedure: Portable fixtures, truncations, malformed ranges/directories/descriptors/ordinals and deterministic mutations.
- Test result / completion: **VERIFIED: native portable core; Windows CLI pending.**
- Known limitations: No loader emulation, delay imports, exhaustive bound-only import recovery or non-ASCII section names.

## Module 02 — Compile-time hashes

- Objective: Compare deterministic constexpr/runtime values and collisions with normal imports.
- Design / implementation: FNV-1a uint32, harmless API names, hello/empty vectors, costarring/liquid collision.
- Source references: `03_SOURCE/hashing/hash_verification.cpp; include/winll.hpp`.
- APIs / dependencies: C++20 constexpr; no API resolution.
- Build result: see [build evidence](../04_TESTING/TEST_RESULTS.md); Windows code builds exclusively with MinGW.
- Test procedure: Portable hash vectors, fixture collisions and known collision.
- Test result / completion: **VERIFIED: native portable core; Windows CLI pending.**
- Known limitations: Not cryptographic or unique.

## Module 03 — Process metadata

- Objective: Report current PID, observed parent PID, own command line and parsed arguments.
- Design / implementation: Toolhelp snapshot and wide runtime arguments, UTF-8 JSON.
- Source references: `03_SOURCE/process/process_metadata.cpp; core/application.cpp`.
- APIs / dependencies: GetCurrentProcessId, CreateToolhelp32Snapshot, Process32FirstW/NextW, GetCommandLineW, WideCharToMultiByte.
- Build result: see [build evidence](../04_TESTING/TEST_RESULTS.md); Windows code builds exclusively with MinGW.
- Test procedure: Windows API smoke case and CLI spaced/Unicode argument integration.
- Test result / completion: **IMPLEMENTED; Windows runtime pending.**
- Known limitations: Snapshot race and PID reuse; parent is not authenticated creator identity.

## Module 04 — Mutex

- Objective: Prevent duplicate harness commands within a session.
- Design / implementation: RAII named-object handle; immediate ERROR_ALREADY_EXISTS detection.
- Source references: `03_SOURCE/execution_control/mutex_guard.cpp; include/windows_support.hpp`.
- APIs / dependencies: CreateMutexW, GetLastError, CloseHandle.
- Build result: see [build evidence](../04_TESTING/TEST_RESULTS.md); Windows code builds exclusively with MinGW.
- Test procedure: Windows nested guard/reacquisition unit tests and PowerShell cross-process concurrency test.
- Test result / completion: **IMPLEMENTED; Windows runtime pending.**
- Known limitations: Session-only scope; intentional precreation can deny service.

## Module 05 — Process inventory

- Objective: List PID/name/architecture, filter and export accessible processes.
- Design / implementation: Snapshot, limited-query handles, direct architecture API, case-sensitive substring, JSONL stdout.
- Source references: `03_SOURCE/process/process_inventory.cpp`.
- APIs / dependencies: Toolhelp, OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION), IsWow64Process2, CloseHandle.
- Build result: see [build evidence](../04_TESTING/TEST_RESULTS.md); Windows code builds exclusively with MinGW.
- Test procedure: Windows self-inventory smoke test, integration filter, manual denied-query and JSON export checks.
- Test result / completion: **IMPLEMENTED; Windows runtime pending.**
- Known limitations: Windows 10 1709+; query denial and process exit can produce unknown architecture.

## Module 06 — Retrieval

- Objective: Read capped encrypted inert bytes from file, fixed HKCU test key or explicitly approved HTTPS host.
- Design / implementation: Streaming cap, REG_BINARY size/type checks, exact host/port validation, no redirects, TLS defaults, errors/logs.
- Source references: `03_SOURCE/retrieval/artifact_client.cpp; core/logger.cpp`.
- APIs / dependencies: RegOpenKeyExW, RegGetValueW, RegCloseKey; WinHTTP request/URL/query/read/timeout/handle APIs.
- Build result: see [build evidence](../04_TESTING/TEST_RESULTS.md); Windows code builds exclusively with MinGW.
- Test procedure: Native file cap; Windows URL rejection unit tests; local/registry integration and controlled HTTPS matrix.
- Test result / completion: **IMPLEMENTED; portable bounded file read VERIFIED; Windows paths pending.**
- Known limitations: Network/registry adapters untested; no proxy, replay defense or production source enrollment.

## Module 07 — Decryption

- Objective: Authenticate benign data in memory, validate inert schema, wipe buffers.
- Design / implementation: CNG AES-256-GCM, 4-byte AAD, 12-byte nonce, 16-byte tag; schema only after authentication; RAII wipes.
- Source references: `03_SOURCE/crypto/artifact_validator.cpp; crypto/schema.cpp`.
- APIs / dependencies: BCrypt provider/key/property/decrypt/destruction APIs, SecureZeroMemory.
- Build result: see [build evidence](../04_TESTING/TEST_RESULTS.md); Windows code builds exclusively with MinGW.
- Test procedure: Native schema tests; Python reference valid/tag/wrong-key/schema/truncation cases; Windows CNG suite.
- Test result / completion: **IMPLEMENTED; schema and reference fixtures VERIFIED; CNG runtime pending.**
- Known limitations: Public fixture key; no production key vault, replay defense or paging guarantees.

## Module 08 — Evasion research

- Objective: Analyze six techniques safely.
- Design / implementation: Eight aspects per technique, primary references and labeled synthetic correlations.
- Source references: `01_RESEARCH/EVASION_TECHNIQUES.md; 04_TESTING/integration/analyze_synthetic.py`.
- APIs / dependencies: No operational Windows implementation.
- Build result: see [build evidence](../04_TESTING/TEST_RESULTS.md); Windows code builds exclusively with MinGW.
- Test procedure: Two expected synthetic correlations and synthetic-label checks.
- Test result / completion: **RESEARCH ONLY; synthetic analysis VERIFIED.**
- Known limitations: No real attack traces or measured detector efficacy.

## Module 09 — Signing

- Objective: Optional test Authenticode signing with external keys.
- Design / implementation: Separate unsigned/signed copy, certificate instructions, explicit test-CA verification and Git exclusions.
- Source references: `05_BUILD/scripts/sign_development.sh; verify_signature.sh`.
- APIs / dependencies: OpenSSL, osslsigncode; Windows Get-AuthenticodeSignature procedure.
- Build result: see [build evidence](../04_TESTING/TEST_RESULTS.md); Windows code builds exclusively with MinGW.
- Test procedure: Sign, verify using test CA, record certificate details, reject tampered copy.
- Test result / completion: **BLOCKED: signing tool unavailable; workflow untested.**
- Known limitations: A self-signed certificate has no default public trust. Tool missing.



[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
