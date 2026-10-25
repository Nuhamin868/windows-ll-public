# Demonstration and explanation guide

This project demonstrates a read-only Windows internals harness. It does not execute retrieved content. The assignment's original external rubric was not included separately; REQUIREMENTS.md records the requirements available in this archive.

## Prepare

Use a standard-user Windows 10 1709+ or Windows 11 x64 account. Extract the validation release ZIP. Keep the fixtures beside the executables. Review FINAL_SUBMISSION.md and the latest validation report before claiming completion. Run `04_TESTING/integration/windows_validation.ps1` in PowerShell to exercise the offline suite.

## Present

1. Run `build/windows/windows_ll.exe hash`. Explain constexpr versus runtime FNV-1a and why the tested collision means hashes are not unique identities.
2. Run `build/windows/windows_ll.exe pe build/windows/windows_ll.exe`. Explain file offsets versus RVAs, PE32+ imports, bounds checks, and why parsing a file never executes it.
3. Run `build/windows/windows_ll.exe metadata "space argument" λ`. Explain the observed parent PID and Unicode arguments; a snapshot cannot prove historical ancestry.
4. Run `build/windows/windows_ll.exe processes windows_ll`. Explain the name filter, architecture queries, limited permissions, and races with process exit.
5. Run `build/windows/windows_ll.exe artifact 04_TESTING/test_data/artifact.bin 04_TESTING/test_data/test-key.bin`. Explain AES-256-GCM authentication, the constrained inert schema, and wiping. Repeat with bad-tag.bin to demonstrate rejection. The fixture key is public test data.
6. Run `build/windows/windows_ll.exe hold 10000` and invoke `hash` in a second terminal. Explain duplicate-instance rejection and handle cleanup, then show a successful run after the holder ends.
7. Show the PowerShell integration log for the HKCU test fixture and automatic cleanup. Show the requirement matrix, test evidence and remaining HTTPS validation.

## Explain the source

Start at `03_SOURCE/core/main.cpp` and `application.cpp` for dispatch and error reporting. The portable PE/hash/schema library is separate from Windows process, retrieval, mutex and CNG adapters. RAII closes handles; parser bounds reject malformed files. Reports go to stdout, diagnostic JSON events to stderr. Explain one positive and one negative test for each demonstrated component using MODULE_REFERENCE.md and IMPLEMENTATION_DETAILS.md.

## Remaining acceptance work

Native offline validation does not establish controlled HTTPS behavior, access-denied scenarios, PID reuse, cross-session behavior or every registry failure. Complete TEST_PLAN.md against a controlled trusted TLS service and retain genuine evidence. The release is unsigned; optional signing is not a prerequisite for demonstrating this unsigned research build. Do not describe this as an operational malware implementation or claim an external rubric has been fully satisfied.
