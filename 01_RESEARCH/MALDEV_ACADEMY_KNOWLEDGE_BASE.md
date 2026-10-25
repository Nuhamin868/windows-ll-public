# Maldev Academy course knowledge base and system alignment

This note records how the user-provided Maldev Academy export informed Windows LL. It is a defensive, research-oriented reading map; it does not adopt the course's operational loader/evasion objective. This project remains the safe research harness defined in its [charter](../00_PROJECT_MANAGEMENT/PROJECT_CHARTER.md), with the boundaries in its [threat model](../02_ARCHITECTURE/THREAT_MODEL.md).

## Corpus processing record

The supplied directory was `/home/hammerspacecraft/Downloads/Telegram Desktop/Maldev-Academy-Malware-Development`. Its extracted course folder is recorded in [`maldev-academy-source-index.json`](../08_EVIDENCE/verification/maldev-academy-source-index.json).

The index inventories all **2,350 files** by relative path, byte length, SHA-256 and file type. The textual learning material consists of **92 PDF files (788 total pages), 92 HTML pages and 21 text challenge prompts**. All PDF pages were passed through Poppler text extraction; HTML text/headings were extracted using Python's standard parser while excluding code/pre blocks, scripts, styles, navigation and SVG. The resulting index records headings and text-extraction counts rather than copying course prose. Challenge prompts are indexed but not answered.

The export also contains **187 ZIP archives, 25 standalone source/project files, and 1,933 supporting media/web files**. Archives and code are fingerprinted only. No archive was extracted, no sample was built/run, and no course source file was copied into the harness. The originals were left untouched. The full export is indexed, while generated knowledge notes summarize the course through defensive research and per-module alignment. The index is a searchable catalog and provenance record, not a model fine-tune or a copy of the source material. Re-run the source indexer after setting up the same source directory:

```bash
python3 04_TESTING/integration/index_course_sources.py \
  --output 08_EVIDENCE/verification/maldev-academy-source-index.json
```

If the course export is moved, pass its parent directory with `--source`. For every lecture document, the index also records extracted HTML headings or PDF heading candidates, topical signals and extracted text length. It stores no lecture prose or code. It contains hashes for every original file, which lets a reviewer confirm precisely which corpus revision informed this map.

## Course-informed design choices

- **Treat PE metadata as untrusted input.** PE and import-table material informed a bounded, read-only parser with explicit range checks and deterministic malformed-input tests. It never maps or runs an image.
- **Separate hashing education from import hiding.** The harness demonstrates compile-time/runtime hash agreement and collision risk, while retaining normal, inspectable Windows imports.
- **Make process observations auditable.** Process enumeration and own-process metadata are read-only. Parent PID is labeled as an observed value, not proof of a creator relationship.
- **Constrain staging and encryption to inert data.** Local, HKCU, and allowlisted HTTPS retrieval end at authenticated schema validation. Retrieved bytes cannot be transferred to executable memory or interpreted as instructions. Legacy obfuscation/encryption examples are not used.
- **Treat signing as provenance evidence.** The optional development workflow distinguishes signature integrity from publisher trust and does not describe a self-signed certificate as publicly trusted.
- **Turn detection/EDR lessons into analyst questions.** The project catalogs relevant behavior, telemetry limits, false positives and mitigations. It does not try to evade static or behavioral detection.

These choices are reflected in the [system overview](../02_ARCHITECTURE/SYSTEM_OVERVIEW.md), [data flow](../02_ARCHITECTURE/DATA_FLOW.md), [security analysis](../07_DOCUMENTATION/SECURITY_ANALYSIS.md), and [implementation matrix](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md).

## Module-by-module reading map

The module titles below come from the exported HTML lecture filenames. PDF copies and supplementary readings are independently inventoried in the JSON manifest; filenames are not assumed to pair one-to-one. “Research only” means it informs analyst context, not an implemented feature.

| Module | Course topic | How it informs this project |
|---:|---|---|
| 1 | Module 1: Welcome Module | Background reference only; undocumented structure use is not introduced. |
| 2 | Module 2: Introduction To Malware Development | Background reference only; undocumented structure use is not introduced. |
| 3 | Module 3: Required Tools | Background reference only; undocumented structure use is not introduced. |
| 4 | Module 4: Coding Basics | Background reference only; undocumented structure use is not introduced. |
| 5 | Module 5: Windows Architecture | Background reference only; undocumented structure use is not introduced. |
| 6 | Module 6: Windows Memory Management | Background reference only; undocumented structure use is not introduced. |
| 7 | Module 7: Introduction To The Windows API | Background reference only; undocumented structure use is not introduced. |
| 8 | Module 8: Portable Executable Format | Directly informs the bounded read-only PE inspector. |
| 9 | Module 9: Dynamic-Link Library | Background reference only; undocumented structure use is not introduced. |
| 10 | Module 10: Detection Mechanisms | Informs defender-facing detection context only; no sensor bypass or detection-evasion code. |
| 11 | Module 11: Windows Processes | Informs own-process metadata and read-only process inventory. |
| 12 | Module 12: Undocumented Structures | Background reference only; undocumented structure use is not introduced. |
| 13 | Module 13: Payload Placement - .data & .rdata Sections | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 14 | Module 14: Payload Placement - .text Section | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 15 | Module 15: Payload Placement - .rsrc Section | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 16 | Module 16: Introduction To Payload Encryption | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 17 | Module 17: Payload Encryption - XOR | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 18 | Module 18: Payload Encryption - RC4 | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 19 | Module 19: Payload Encryption - AES Encryption | Informs use of Windows CNG for authenticated inert test records; legacy payload crypto is excluded. |
| 20 | Module 20: Evading Microsoft Defender Static Analysis | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 21 | Module 21: Payload Obfuscation - IPv4_IPv6Fuscation | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 22 | Module 22: Payload Obfuscation - MACFucscation | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 23 | Module 23: Payload Obfuscation - UUIDFuscation | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 24 | Module 24: Maldev Academy Tool - HellShell | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 25 | Module 25: Maldev Academy Tool - MiniShell | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 26 | Module 26: Local Payload Execution - DLL | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 27 | Module 27: Local Payload Execution - Shellcode | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 28 | Module 28: Process Injection - DLL Injection | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 29 | Module 29: Process Injection - Shellcode Injection | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 30 | Module 30: Payload Staging - Web Server | Informs inert artifact retrieval only; no payload staging or execution. |
| 31 | Module 31: Payload Staging - Windows Registry | Informs inert artifact retrieval only; no payload staging or execution. |
| 32 | Module 32: Malware Binary Signing | Informs optional development signing and explicit trust limitations. |
| 33 | Module 33: Process Enumeration - EnumProcesses | Informs accessible, read-only process enumeration. |
| 34 | Module 34: Process Enumeration - NtQuerySystemInformation | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 35 | Module 35: Thread Hijacking - Local Thread Creation | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 36 | Module 36: Thread Hijacking - Remote Thread Creation | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 37 | Module 37: Thread Hijacking - Local Thread Enumeration | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 38 | Module 38: Thread Hijacking - Remote Thread Enumeration | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 39 | Module 39: APC Injection | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 40 | Module 40: Early Bird APC Injection | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 41 | Module 41: Callback Code Execution | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 42 | Module 42: Local Mapping Injection | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 43 | Module 43: Remote Mapping Injection | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 44 | Module 44: Local Function Stomping Injection | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 45 | Module 45: Remote Function Stomping Injection | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 46 | Module 46: Payload Execution Control | Course execution control is excluded; the harness mutex only prevents duplicate app instances. |
| 47 | Module 47: Spoofing PPID | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 48 | Module 48: Process Argument Spoofing (1) | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 49 | Module 49: Process Argument Spoofing (2) | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 50 | Module 50: Parsing PE Headers | Directly informs the bounded read-only PE inspector. |
| 51 | Module 51: String Hashing | Informs a visible, noncryptographic hash demonstration; no concealment/resolution. |
| 52 | Module 52: IAT Hiding & Obfuscation - Introduction | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 53 | Module 53: IAT Hiding & Obfuscation - Custom GetProcAddress | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 54 | Module 54: IAT Hiding & Obfuscation - Custom GetModuleHandle | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 55 | Module 55: IAT Hiding & Obfuscation - API Hashing | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 56 | Module 56: IAT Hiding & Obfuscation - Custom Pseudo Handles | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 57 | Module 57: IAT Hiding & Obfuscation - Compile Time API Hashing | Contrast reference: compile-time hashing is tested while imports remain visible. |
| 58 | Module 58: API Hooking - Introduction | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 59 | Module 59: API Hooking - Detours Library | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 60 | Module 60: API Hooking - Minhook Library | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 61 | Module 61: API Hooking - Custom Code | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 62 | Module 62: API Hooking - Using Windows APIs | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 63 | Module 63: Syscalls - Introduction | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 64 | Module 64: Syscalls - Userland Hooking | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 65 | Module 65: Syscalls - SysWhispers | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 66 | Module 66: Syscalls - Hell's Gate | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 67 | Module 67: Syscalls - Reimplementing Classic Injection | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 68 | Module 68: Syscalls - Reimplementing Mapping Injection | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 69 | Module 69: Syscalls - Reimplementing APC Injection | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 70 | Module 70: Anti-Analysis - Introduction | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 71 | Module 71: Anti-Debugging - Multiple Techniques | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 72 | Module 72: Anti-Debugging - Self-Deletion | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 73 | Module 73: Anti-Virtual Environments - Multiple Techniques | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 74 | Module 74: Anti-Virtual Environments - Multiple Delay Execution Techniques | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 75 | Module 75: Anti-Virtual Environments - API Hammering | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 76 | Module 76: Binary Entropy Reduction | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 77 | Module 77: Brute Force Decryption | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 78 | Module 78: MalDev Academy Tool - KeyGuard | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 79 | Module 79: CRT Library Removal & Malware Compiling | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 80 | Module 80: IAT Camouflage | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 81 | Module 81: Bypassing AVs | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 82 | Module 82: Introduction To EDRs | Informs defender-facing detection context only; no sensor bypass or detection-evasion code. |
| 83 | Module 83: NTDLL Unhooking - Introduction | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 84 | Module 84: NTDLL Unhooking - From Disk | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 85 | Module 85: NTDLL Unhooking - From KnownDlls Directory | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 86 | Module 86: NTDLL Unhooking - From a Suspended Process | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 87 | Module 87: NTDLL Unhooking - From a Web Server | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 88 | Module 88: Updating Hell's Gate | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 89 | Module 89: Indirect Syscalls - HellsHall | Research-only subject; no operational evasion, injection, execution, spoofing, concealment or unhooking implementation. |
| 90 | Module 90: Block DLL Policy | Defensive policy concept only; not used to disable, block or bypass security products. |
| 91 | Module 91: Diving Into NtCreateUserProcess | Process creation internals are a reference topic; no low-level/deceptive process creation is implemented. |
| TOC | Course contents index | Lists the course sequence; used to check coverage. |

## Topic coverage and boundaries

**Foundations and file formats (1–12, 50).** Windows architecture, memory, APIs, processes, DLLs, detection, and PE concepts ground the parser and documentation. Undocumented structures remain background only. The implementation follows documented file-format references and declines to reproduce course-specific loader examples.

**Section placement, cryptography, and static evasion (13–25, 76–80).** The project does not hide instructions in PE sections, transform shellcode into textual encodings, reduce entropy to defeat scanners, brute-force an embedded key, or implement payload-packing tools. The safe overlap is narrow: read-only PE inspection and an authenticated, public test fixture whose plaintext is constrained to inert printable data. Hashes are demonstrative and imports remain visible.

**Execution, injection, and process identity (26–29, 35–49).** Local/remote payload execution, DLL and shellcode injection, thread hijacking, APCs, mapping, function stomping, callback execution and parent/argument spoofing are documented only as defensive research. There are no remote process write/thread/context APIs in application code. The named mutex is only duplicate-instance control; it is not course-style payload execution control.

**Retrieval, registry and signing (30–32).** The harness has constrained read-only source adapters and a development signing procedure. The source adapter accepts encrypted inert data only; it is not a staged payload downloader. The certificate workflow is not an evasion or trust-acquisition feature.

**Enumeration, hashing, imports, hooks and syscalls (33–34, 51–69).** Enumeration maps to documented read-only snapshots. The undocumented `NtQuerySystemInformation` lesson is not adopted. The hash lesson is shown with a known collision, while IAT concealment, custom resolvers, hook manipulation and direct/indirect syscall techniques are research-only and absent from source.

**Anti-analysis and endpoint defense (70–91).** Anti-debugging, anti-VM checks, delay tactics, API hammering, AV bypass, unhooking and related loader construction are not implemented. EDR/detection topics inform behavior-based investigation questions. DLL policy and low-level process creation are references for defensive review, not controls used to disable monitoring or disguise process creation.

## Reading priorities for continuing defensive work

1. Compare parser output with trusted file provenance, Authenticode verification and section/permission anomalies; parser success does not establish that an image is benign.
2. Correlate process creation, observed parent, command line, image load and access events across independent sensors and time. A single PID/parent field is weak evidence.
3. Review unexpected cross-process access together with thread starts/changes and memory protections. Missing one event type does not rule out suspicious activity.
4. Treat unusual entropy, sparse imports, encrypted resources, delay behavior and hook inconsistencies as context-dependent signals, never standalone verdicts. Legitimate packers, updaters, profilers, accessibility tools and security agents can produce similar observations.
5. Preserve original telemetry, sensor configuration and collection gaps. The project's synthetic event traces are educational fixtures, not samples from the course or real endpoint logs.

## Reference and verification limits

The course is a user-supplied secondary learning source, not the authoritative definition of Windows APIs or the PE format. Microsoft API documentation and the PE/COFF specification remain authoritative for implementation details. The course inventory establishes provenance and topic coverage; it does not verify course claims or independently validate detection effectiveness. No claims are made that the operational examples in the export were executed or reproduced.

For project implementation/test status, see the [module reference](../07_DOCUMENTATION/MODULE_REFERENCE.md), [test results](../04_TESTING/TEST_RESULTS.md) and [session log](../09_SESSION_LOGS/SESSION_003.md).
