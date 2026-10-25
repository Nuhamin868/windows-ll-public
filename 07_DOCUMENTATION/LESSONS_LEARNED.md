# Lessons learned

A platform-independent parser can be exercised thoroughly while a cross-compiler is unavailable; that progress must not be described as Windows API validation. Deterministic malicious-looking header mutations test data parsing without creating payloads. A known hash collision makes the limits of a noncryptographic hash concrete.

Signature verification must use the actual binary pacman keyring or import the armored key bundle correctly. Passing an armored file directly to gpgv failed, so the existing `/etc/pacman.d/gnupg/pubring.gpg` was used. Downloads should have one writer per destination; retry work was adjusted accordingly. Slow mirrors can be range-downloaded, but the whole archive must still pass signature verification before execution.

LeakSanitizer fails under tracing in this environment; recording the failure and running ASan/UBSan with leak detection disabled is more accurate than silently calling all sanitizers successful. Public fixtures permit repeatable crypto interoperability tests, but only a native CNG run verifies the Windows adapter.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
