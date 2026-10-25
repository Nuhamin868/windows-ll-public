# 2026-10-25 development release

Windows x64 C++20 inert research harness with complete source, fixtures and test runners. Includes unsigned `windows_ll.exe` and development-signed `windows_ll-dev-signed.exe`. The development signature is self-signed and has no default public trust or timestamp. SHA256SUMS covers both variants.

Portable sanitizer/reference checks, Wine API checks and the 31-case Wine integration runner passed. Previous native Windows offline validation passed; current expanded native CI is recorded separately. Development sign/verify/default-trust rejection/tamper detection passed. See [latest review](../SUBMISSION_REVIEW.md) for exact acceptance limits.

Controlled HTTPS fixture tooling is included, but live trusted HTTPS and extended native access/ancestry/session/race tests remain pending. This release is partially complete against those acceptance criteria. Public fixtures provide no production secrecy. No payload execution, injection, concealment or spoofing is implemented.
