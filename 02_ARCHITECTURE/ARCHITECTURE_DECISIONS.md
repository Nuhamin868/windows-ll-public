# Architecture decisions

ADR-01: A single CMake project produces separate native portable tests and Windows executable targets. This preserves host tooling convenience and target-platform clarity.

ADR-02: Standard-library PE decoding is bounded and independent of Windows headers. Conservative rejection is preferable to guessing an ambiguous raw/RVA mapping. Delay imports, bound-only imports, loader emulation and certificate-chain parsing are outside scope.

ADR-03: SHA-256 fixture manifests detect accidental changes; AES-GCM handles artifact authentication. Noncryptographic FNV-1a demonstrates constexpr arithmetic only.

ADR-04: No persistent registry writes or network endpoint are performed by the CLI. Registry setup lives only in the explicit Windows test procedure and refuses to overwrite an existing key.

ADR-05: Research-only offensive techniques stay in Markdown and synthetic JSONL data. They have no callable implementation in the binary.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
