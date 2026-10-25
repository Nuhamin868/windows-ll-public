# Module design

The API boundary is `03_SOURCE/include/winll.hpp`. `Bytes` owns binary input. `PeReport` owns sections and import names, with no pointer into the source buffer. The parser reads integers bytewise, so it does not depend on struct packing, pointer alignment, or the host PE headers.

`windows_support.hpp` owns Win32 HANDLEs through a noncopyable wrapper. The named-mutex guard owns one handle for its entire command. WinHTTP handles and registry handles have API-specific destructors. CNG algorithm/key objects are destroyed in dependency order; key-object memory, supplied key material and plaintext use a SecureZeroMemory destructor. Exceptions propagate to `wmain`, which emits an error event and returns 1.

Reports are JSON or JSONL on stdout. Diagnostic retrieval/authentication events are JSONL on stderr and do not include plaintext or key material. The CLI parses exact positional command forms and rejects unexpected argument counts. No global state is required except Windows' named object namespace.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
