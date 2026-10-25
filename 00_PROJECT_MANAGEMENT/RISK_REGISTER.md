# Risk register

| Risk | Impact | Control / remaining work |
|---|---|---|
| Untrusted PE input | Bounds errors, CPU/memory exhaustion | Range checks, conservative caps, truncation/mutation corpus, ASan/UBSan; not a complete loader validator |
| Retrieved data confused with instructions | Unsafe execution | Only a fixed inert schema; no executable allocation, callback transfer, or process modification |
| Test key reused in production | Lost confidentiality/authenticity | Public test-key labels; no production-secret-management claim |
| Platform assumptions | Cross-build passes but Windows fails | Separate statuses and native Windows integration procedure |
| Parent PID or PID reuse | False identity conclusions | Snapshot observation only; correlate lifetime-aware external telemetry |
| Named object precreation | Local denial of service | Session scope; fail closed on collision; security boundary explicitly excluded |
| Logging command lines | Sensitive local metadata | Explicit command; stdout export is user controlled; avoid real secret arguments |
| Signing trust confusion | Incorrect trust claim | Development-only certificate; verification trust root supplied only for the command |
| TLS endpoint availability | Live path remains unverified | Offline reference fixtures; require controlled endpoint validation |
| Ephemeral toolchain | `/tmp` cleanup breaks reproduction | Normal dependency requirements documented; signature verification evidence retained |
| Strict PE acceptance | Valid exotic binaries rejected | Document ASCII section-name, overlap and normal-import limitations |
| Buffer wiping | Copies may remain in OS/compiler storage | RAII SecureZeroMemory for explicit key/plaintext buffers; no promise about paging/crash dumps |

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
