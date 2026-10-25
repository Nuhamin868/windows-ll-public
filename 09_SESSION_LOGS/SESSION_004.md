# Submission review — 2026-10-23

Inspected the user-supplied ZIP without executing its original executable. Extracted an isolated review copy under /home/noxira/Projects/windows-ll-submission-review/Windows LL; original ZIP preserved. Moved stale archived build caches outside the source tree, then rebuilt all Windows binaries using installed system tools. No dependencies were installed. Existing executable-bit changes caused by ZIP extraction were repaired.

Fresh native sanitizer, Python reference and synthetic tests passed. Wine portable checks passed (5,059); Windows API smoke suite passed (16). Static inspection was regenerated and the unsigned executable repackaged with its SHA-256 digest. Wine emits an advisory about missing wine32; x64 tests returned success. Windows validation and HTTPS acceptance must be recorded separately.

Added a presentation guide and GitHub-hosted Windows offline validation workflow. Preparing a private prerelease avoids publicly exposing coursework. Course source material is not republished; the existing fingerprint index is metadata. No offensive behavior was added. Original separate assignment rubric is unavailable; the archived requirements are the available acceptance reference.

Native Windows offline validation subsequently passed: https://github.com/Nuhamin868/windows-ll/actions/runs/39865808426 . Full workflow output and mutex log preserved under 08_EVIDENCE/windows-native. Fixed workflow transcript path to remain absolute when the invoked suite changes working directory; the full GitHub workflow log already preserves all test output. Source behavior and tested executables are unchanged.
