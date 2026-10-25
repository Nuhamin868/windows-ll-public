# PE format

The implementation follows Microsoft's [PE specification](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format). An RVA is relative to an image base and is not generally a file offset. PE32 and PE32+ use different optional-header layouts and thunk widths.

Our reader validates the declared header/section ranges before resolving an RVA, rejects virtual-only data as an import source, and constructs owned reports. It rejects overlapping sections and invalid directory counts. It deliberately does not load images. [Implementation details](../07_DOCUMENTATION/IMPLEMENTATION_DETAILS.md) describe its conservative profile; `pe32.bin` and `pe64.bin` are non-loadable parser fixtures with no instructions or entry point.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
