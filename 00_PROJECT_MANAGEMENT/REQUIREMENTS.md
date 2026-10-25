# Requirements and traceability

Each ID maps to a module section in the [module reference](../07_DOCUMENTATION/MODULE_REFERENCE.md), which records objectives, design, APIs, tests, results, and limitations.

| ID | Assignment requirement | Evidence / disposition |
|---|---|---|
| R01 | Validate PE32/PE32+, sections, imports, malformed input; structured report | `pe_inspector.cpp`, portable unit suite, static own-binary report |
| R02 | constexpr/runtime names, vectors, collisions; visible imports | `hash_verification.cpp`, known FNV-1a collision and static import report |
| R03 | PID, observed parent, own command line and parsed arguments | `process_metadata.cpp`, `application.cpp`; native Windows offline tests passed; specialized acceptance pending |
| R04 | Named mutex, duplicate control, resource/error handling | `mutex_guard.cpp`, native Windows duplicate/reacquisition tests passed; cross-session acceptance pending |
| R05 | Inventory, PID/name/architecture, filter/export/access errors | `process_inventory.cpp`; stdout JSONL export; native Windows offline tests passed; specialized acceptance pending |
| R06 | HTTPS exact host allowlist, HKCU binary, local file, caps/logging | `artifact_client.cpp`, `logger.cpp`; native registry tests passed; controlled HTTPS pending |
| R07 | CNG AES-256-GCM authentication, inert schema, memory-only validation/wipe | `artifact_validator.cpp`, `schema.cpp`; reference and native Windows CNG tests passed |
| R08 | Six techniques, mechanisms/prerequisites/observables/telemetry/mitigations | Research only, linked primary references and labeled synthetic traces |
| R09 | Optional test Authenticode signing, key exclusion, trust distinction | Development signing/trust/tamper checks passed with osslsigncode; no public trust claim |
| R10 | CMake/MinGW, tests, static inspection, release package | Build guide, scripts, evidence, SHA256SUMS |
| R11 | Version control, RAII, source/test separation, records | Git repository, source headers, evidence and session log |
| R12 | Obsidian knowledge base, all major documents linked | README and relative links; documentation checker |
| R13 | Use supplied Maldev Academy documents as knowledge and align the harness | Defensive course map, full source fingerprint index and per-module implementation mapping; code archives are not imported |

The authoritative per-requirement status is the [implementation matrix](IMPLEMENTATION_STATUS.md).

`VERIFIED` names the scope of verification; it never implies Windows runtime where only native tests ran. R13 is verified as corpus inventory and defensive alignment, not as adoption of operational course code.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
