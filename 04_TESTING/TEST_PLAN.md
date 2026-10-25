# Test plan

## Portable tests

Run `bash 05_BUILD/scripts/test.sh`. CMake builds portable code with ASan/UBSan. CTest covers PE32/PE32+, section/import reports, names/ordinals, IAT fallback, absent imports, bad signatures/RVAs/descriptors/ordinals/directory counts, every shorter fixture length, inert schema, JSON escaping, file cap, hashes/collisions, and 4,000 fixed-seed mutations. Native executables contain no Windows API code. LeakSanitizer is disabled under tracing and is not claimed tested.

Python checks 13 fixture digests and independent reference AES-GCM behavior. Fixture regeneration requires Python `cryptography`: `python3 04_TESTING/test_data/generate_fixtures.py`. Public keys/nonces are test vectors only. Synthetic event checks require explicit labels and expect two educational correlations.

## Native Windows offline tests — passed October 25; specialized acceptance pending

Copy the full project to an isolated standard-user Windows 10 1709+/Windows 11 x64 machine. Run `04_TESTING/integration/windows_validation.ps1` from PowerShell. Capture all streams into `08_EVIDENCE/test_logs/windows-integration.log` using Tee-Object. Record OS build, PowerShell version, user context and final exit status.

The script runs Windows portable units, Windows API units (CNG valid/invalid artifacts, wrong keys, URL rejection, mutex lifecycle, Unicode conversion, metadata and inventory), CLI cases, temporary HKCU data and duplicate-instance integration. It refuses to overwrite an existing registry key. The suite passed in the October 25 native Windows CI run; raw evidence is in `08_EVIDENCE/windows-native-20261025/`. Repeat on the acceptance machine to establish its own results.

Manual checks: parse reports with ConvertFrom-Json; verify own PID/name, case-sensitive filter, Unicode and spaced arguments, and denied process-query errors. Compare observed parent with the launcher while recording process creation times. Exercise process exit during enumeration and separate sessions. Confirm duplicate rejection after holder readiness and successful reacquisition after closure/crash.

## Controlled HTTPS matrix — pending

Use a port-443 endpoint you control with a certificate already trusted by the isolated machine. Supply its exact DNS host explicitly. Do not disable certificate validation or modify trust roots to force success.

| Case | Expected result |
|---|---|
| HTTP 200 correct fixture/key | Authenticated schema success, no plaintext export |
| Wrong key or tag | Authentication failure before parsing |
| HTTP, wrong host, credentials, port 444 or fragment | Rejection without request |
| 301/302 to same/other host | No redirect followed |
| 404/500 | Error status |
| Expired/mismatched/untrusted certificate | TLS failure |
| Body >1 MiB, with/without Content-Length | Rejection during bounded read |
| Disconnect, timeout, slow drip | Error or elapsed read deadline |
| Empty/truncated/authenticated invalid schema | Envelope/auth/schema failure |

Preserve service-side request counts proving rejected sources/redirect targets were not fetched. Also test registry missing/wrong-type/oversize/changing values.

## Static inspection and signing

Use file, cross-objdump and native winll_inspect on the built executable. Require AMD64 PE32+, visible system imports and NX/ASLR flags. Compare identical clean-build hashes; make no cross-toolchain reproducibility claim.

Follow [development signing](../01_RESEARCH/CODE_SIGNING.md) when tooling exists. Preserve certificate subject/validity/fingerprint and verification output. Record default trust separately from explicit test-CA verification; a tampered disposable copy must fail integrity verification. Keys remain outside Git.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)

## Extended runners — 2026-10-25

Run `python3 04_TESTING/integration/runtime_validation.py` on Windows, or append `--wine` on Linux. It asserts parsed JSON, Unicode arguments, case-sensitive filters, positive/negative registry records and mutex reacquisition after termination. It refuses to overwrite an existing fixed test registry key and cleans up the key it creates. The PowerShell suite also tests oversized, missing and wrong-type registry values. The build-validation GitHub workflow builds current source and executes both native suites.

Controlled TLS service setup (use your own certificate and private key outside Git):

```bash
python3 04_TESTING/integration/https_fixture_server.py --cert /outside/repo/cert.pem --key /outside/repo/key.pem --bind CONTROLLED_BIND_ADDRESS --request-log /outside/repo/requests.jsonl
```

The service binds port 443 by default. Use a hostname resolving to that service and a certificate already trusted by the client. No trust-store changes or TLS bypasses are made. Start with a new request log; run only in your isolated lab. Keep its log accessible to the validation client, including over a mounted share if needed.

```bash
python3 04_TESTING/integration/https_validation.py --base-url https://YOUR_CONTROLLED_HOST --server-log /outside/repo/requests.jsonl
```

Append `--wine` for compatibility testing. Repeat `--rejected-tls-url https://CONTROLLED_CERT_FAILURE_HOST/valid` for independently configured expired, mismatched and untrusted certificate hosts. Preserve their certificate configuration with the evidence. The runner tests good/bad artifacts, wrong keys, empty/truncated records, redirect refusal, 404/500, size caps with/without Content-Length, receive timeout, slow-drip deadline, disconnect and URL restrictions. It checks server logs for forbidden redirect/rejected paths. A run with no certificate hosts does not cover certificate-failure categories. These tools are authored; no live HTTPS pass is claimed without executing against the controlled service.
