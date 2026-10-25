# Course alignment

The course is an input to the project's research questions and module priorities. It does not replace the WINLL-001 authorization or change the harness into an operational loader. All 2,350 source files are fingerprinted; all 205 lecture/prompt documents are text/heading/topic indexed. See [Maldev Academy knowledge base](../01_RESEARCH/MALDEV_ACADEMY_KNOWLEDGE_BASE.md) and [generated source manifest](../08_EVIDENCE/verification/maldev-academy-source-index.json).

| Course area | Harness treatment | Current evidence |
|---|---|---|
| Windows/PE fundamentals and parsing (8, 50) | Implement read-only PE32/PE32+ parser | Native malformed-input tests; Windows cross-build/static report |
| Detection and EDR context (10, 82) | Defensive telemetry and limitations research | Synthetic labeled events only |
| Process fundamentals and enumeration (11, 33) | Read-only metadata and inventory | Cross-compiled; native Windows runtime pending |
| Encryption and staging (16–19, 30–31) | Authenticated inert-data adapter only | Python crypto reference passes; Windows CNG/runtime pending |
| Signing/provenance (32) | Optional development signing with clear trust limits | Signing utility unavailable; workflow unverified |
| Compile-time hashing (51, 57) | Educational vectors/collision while keeping imports visible | Portable unit verification |
| Injection, thread/APC, mapping, stomping, spoofing (26–29, 35–49) | Detection research only | No operational implementation |
| Import concealment, hooks and syscalls (52–69, 83–89) | Research-only analysis; normal imports remain | Static import inspection and source review |
| Anti-analysis and AV bypass (20–25, 70–81) | Research-only risk/telemetry/mitigation notes | No evasion implementation |
| Low-level creation and DLL policy (90–91) | Defensive context only | No low-level process creation in harness |

Architecture decisions: course emphasis on multiple execution and evasion paths increased the need for explicit exclusion boundaries, visible APIs, independent telemetry, fixture labeling and research-only classification. Course claims are cross-checked against primary Windows documentation before implementation. Bundled executable examples remain outside the build graph.
