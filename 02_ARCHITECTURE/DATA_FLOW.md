# Data flow

```mermaid
flowchart TD
    CLI[Explicit CLI command] --> Mutex[Session named mutex guard]
    Mutex --> PE[Bounded file read / PE inspection]
    Mutex --> Proc[Read-only process snapshots]
    Mutex --> Hash[constexpr/runtime verification]
    Mutex --> Src[Local / HKCU / allowed HTTPS source]
    Src --> Cap[1 MiB cap and envelope validation]
    Cap --> GCM[CNG AES-GCM authentication]
    GCM --> Schema[Inert WLLD schema check]
    Schema --> Wipe[Wipe plaintext and key buffers]
    PE --> Report[JSON stdout report]
    Proc --> Report
    Wipe --> Event[Validation result only]
```

Ciphertext may be stored as a fixture. Plaintext exists only in application-owned non-executable memory. Authentication failure exits without calling the schema validator. A successful schema check records success without exporting its content.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
