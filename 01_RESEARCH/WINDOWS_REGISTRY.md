# Registry test artifact source

The application reads HKCU `Software\WindowsLL\TestArtifacts`, REG_BINARY `Data`. It never creates or changes this key. RegGetValueW first measures the value, enforces the 1 MiB cap, and then reads; type, size-change or API errors fail closed. Its HKEY is RAII-managed.

The supplied Windows test creates a disposable key only when it does not already exist, writes encrypted fixture bytes, validates through the CLI, and removes its key in a finally block. Run it in a disposable standard-user account. No persistence, autorun key, privileged hive or executable artifact is involved.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
