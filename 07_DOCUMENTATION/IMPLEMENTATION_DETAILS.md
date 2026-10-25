# Implementation details

## Artifact envelope

| Offset | Length | Meaning |
|---|---|---|
| 0 | 4 | ASCII `WLL1`, authenticated as AAD |
| 4 | 12 | GCM nonce |
| 16 | 16 | GCM authentication tag |
| 32 | remainder | AES-256-GCM ciphertext |

Input cap: 1 MiB. Key file: exactly 32 raw bytes, not hex. CNG receives the original 4-byte header as authenticated additional data, a 12-byte nonce and a 16-byte tag. Failure is propagated before schema validation. Key/plaintext/key-object buffers are wiped on success and exceptions. The fixed fixture key and nonce must never be reused for different production messages; authenticated-invalid-schema test data deliberately uses the same public test vector for deterministic testing only.

## Plaintext schema

ASCII `WLLD` (4), version `01` (1), little-endian uint16 length (2), and 1–256 printable ASCII text bytes. No trailing data. There are no executable opcodes, module names, paths, callbacks, or commands in the schema. No decrypted value is printed or written to disk. This is a restricted inert record schema, not a general JSON interpreter.

## PE parser limits

Maximum CLI input 64 MiB; 1–96 sections, at most 1,024 DLL descriptors, 65,536 thunk entries per DLL, strings bounded at 4,096 bytes. Bytewise reads use checked spans. Virtual addresses use 64-bit intermediate arithmetic, raw reads must lie within one file-backed range, and overlaps are rejected. PE32/PE32+ and ordinal imports are supported. Zero OriginalFirstThunk falls back to the import address table. Virtual zero-fill cannot back an on-disk import. Optional-header directory count must fit its declared size.

The parser reports format, machine, section name/RVA/raw size/offset, DLLs and functions. It does not map an executable, resolve functions, run entry points, or validate every Windows loader rule. ASCII section names are required by this conservative inspection profile; unusual valid PE names may be rejected.

## Retrieval

Local reads stream with a cap rather than trusting a pre-read file size. Registry is a fixed HKCU REG_BINARY query; a changing value or read failure is rejected. WinHTTP accepts only exact explicitly approved host names, HTTPS port 443, HTTP 200 and no redirects. Credentials/fragments are rejected. Proxy use is disabled. Per-operation timeouts are five seconds; streamed response reads also use a 30-second elapsed deadline checked between reads. DNS/connection/headers have their own API timeouts; this is not a hard whole-command wall-clock SLA.

## CLI and telemetry

`wmain` preserves Windows Unicode argument parsing; no shell command is constructed. JSON string escaping preserves UTF-8 text. Metadata explicitly exposes the user's own command line, so do not place secrets on it. Process export uses stdout redirection. Errors go to stderr with return code 1. Logs do not claim to be Windows Event Log or ETW integration; they are application JSONL.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
