# Technical report

Windows LL implements an inert C++20 Windows internals harness. It inspects PE imports, verifies hashes, observes process metadata, lists processes, guards instances, retrieves bounded ciphertext and authenticates inert structured data. Injection/evasion subjects remain research only; normal API imports stay visible.

Safety boundaries are checked byte spans and caps, explicit HTTPS origin selection, authentication before schema inspection, a narrow data schema, RAII cleanup and sensitive buffer wiping. No process memory is modified and retrieved bytes cannot enter executable memory.

The portable 5,059-check suite passed under ASan/UBSan with leak detection disabled; fixture reference AES-GCM and synthetic analysis passed. These establish portable behavior only. Current cross-build/static evidence is in [test results](../04_TESTING/TEST_RESULTS.md). Target-platform execution, live controlled HTTPS and signing must retain pending/blocked status until actually measured.

[Module reference](MODULE_REFERENCE.md) records objectives, source/APIs, dependencies, build/tests and limitations. [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md) distinguishes verified scope from implemented code and research. This research harness is not completion of an operational injection assignment. See [security analysis](SECURITY_ANALYSIS.md), [limitations](LIMITATIONS.md), and [submission checklist](FINAL_SUBMISSION.md).

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
