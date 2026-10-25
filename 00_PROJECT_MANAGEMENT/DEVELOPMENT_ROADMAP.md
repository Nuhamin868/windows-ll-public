# Development roadmap

October 19: inspect environment; implement portable parser/hash/schema and Windows modules; build where tools permit; record evidence and limitations.

October 20–21: provision an isolated Windows 10 1709+/Windows 11 x64 test machine; execute PowerShell integration and Windows unit suites; review command-line quoting, access restrictions and architecture behavior under a standard user.

October 22–23: controlled HTTPS service tests (valid certificate, timeout, invalid TLS, redirect and oversize), registry failure paths and Unicode arguments; improve based on actual failures.

October 24: optional test signing with an external development key, signature/tamper validation; repeat clean cross-build, freeze evidence and review documentation.

October 25: complete acceptance review. If runtime or network gaps remain, submit explicitly as partial. No automatic deployment, public publication, or upstream messaging is part of this plan.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
