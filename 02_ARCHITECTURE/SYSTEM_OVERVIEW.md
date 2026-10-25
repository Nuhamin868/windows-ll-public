# System overview

One console executable exposes explicit commands. The portable `winll_core` library implements file reads, JSON escaping, PE parsing, hashes and schema validation. Windows adapters implement process snapshots, mutex handles, WinHTTP, registry access and CNG decryption. Each command completes or returns exit code 1 with a structured diagnostic. Help returns 0.

Only process query handles are used. Binary input is read as data. No module loads external code or changes process identities. Direct imports remain inspectable. A native test executable links only portable code; it cannot stand in for Windows integration validation.

The [course alignment](COURSE_ALIGNMENT.md) maps the supplied curriculum to the safe implementation and research-only boundary.

See [data flow](DATA_FLOW.md), [module design](MODULE_DESIGN.md), [threat model](THREAT_MODEL.md), and [module reference](../07_DOCUMENTATION/MODULE_REFERENCE.md).

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
