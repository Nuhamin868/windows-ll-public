# Import tables

Normal import descriptors identify a DLL and lookup/address tables; entries can identify a function by name or ordinal. A zero descriptor/table entry terminates the corresponding sequence. Consult the [Microsoft PE format](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format).

`inspect_pe` verifies terminators within limits, falls back to the address table when the original lookup table is absent, and reports ordinal names as `ordinal:N`. It does not resolve addresses. The harness's own normal imports remain visible to static inspection. Delay imports and full bound-only import reconstruction are outside this implementation.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
