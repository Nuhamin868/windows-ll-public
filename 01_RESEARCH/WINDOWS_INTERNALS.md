# Windows internals research

Windows processes own address spaces, threads and kernel object handles. This harness only snapshots process records and queries limited process information. Its C++ destructors close handles on normal returns and exceptions. It does not inspect another process's private memory.

The research boundary is explicit: PE bytes are parsed on disk, registry bytes remain inert, and authenticated plaintext is a bounded ASCII record. A process name, PID or reported parent is an observation rather than a verified identity. See [process metadata](PROCESS_METADATA.md), [architecture](../02_ARCHITECTURE/SYSTEM_OVERVIEW.md), and [primary references](MALDEV_REFERENCES.md).

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
