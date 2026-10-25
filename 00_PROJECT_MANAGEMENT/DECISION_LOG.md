# Decision log

- D001: Preserve exact project name under the existing `~/Projects`; first inspect, then create. Use the writable workspace only for temporary authoring before authorized copy into project location.
- D002: No package manager installs. Obtain official repository tool archives into `/tmp`, verify detached signatures against the host pacman public keyring before extraction. Tools are temporary; record versions.
- D003: Separate portable parsing/hash/schema code from Windows-only API code. Native tests give parser safety evidence without pretending to validate Win32 behavior.
- D004: Use CNG AES-GCM rather than a handwritten cipher. Public deterministic fixture key/nonce are restricted to tests.
- D005: Require explicit CLI DNS host allowlisting and reject HTTP, alternate ports, credentials and redirects. Offline artifact fixtures permit progress without a network dependency.
- D006: Use an open named-mutex object's lifetime as the session instance guard; no ownership wait is needed. This is a convenience control, not an authentication boundary.
- D007: Keep API imports visible, including direct IsWow64Process2; require Windows 10 1709+ as a documented compatibility limit.
- D008: Record signing and Windows runtime as blocked/pending rather than fabricate successful results.
- D009: Use the supplied Maldev Academy corpus as defensive research context. Hash and index every exported file; extract text/headings/topics from lecture PDFs/HTML and prompts; keep course archives and standalone operational source out of the build graph.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
