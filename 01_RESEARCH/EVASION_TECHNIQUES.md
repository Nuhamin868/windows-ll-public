# Evasion techniques: defensive research

These six subjects are **RESEARCH ONLY**. No operational injection, API hiding, parent selection or foreign command-line modification is implemented. The following detection ideas are analyst inferences, not validated detector performance. No technique was executed on a real endpoint.

## Remote function stomping

1. Mechanism: replace code in a function mapped by a different process, causing later execution to reach changed bytes.
2. Internals: image mappings, copy-on-write pages and executable page protections.
3. Prerequisites: sufficient cross-process modification rights and an execution opportunity.
4. Observables: access to another process, image-page changes and execution inconsistent with the backing file.
5. Risks: host corruption, crashes and unauthorized execution.
6. Telemetry: process-access events and endpoint memory-integrity evidence; ordinary process-start logs alone are insufficient.
7. Detection opportunity: correlate suspicious access with modified image pages and unusual call stacks.
8. Limits/mitigation: legitimate hotpatching/debugging can resemble changes; restrict rights and apply supported exploit protections.

## Remote thread hijacking

1. Mechanism: redirect an existing foreign thread rather than starting a new one.
2. Internals: thread context, scheduling state, instruction pointers and stack state.
3. Prerequisites: rights to manipulate that thread and compatible execution state.
4. Observables: abnormal thread-state transitions, context changes or execution destinations.
5. Risks: broken invariants, deadlocks and compromise of the target process.
6. Telemetry: endpoint thread/context and process-access instrumentation; absence of a new-thread event does not establish safety.
7. Detection opportunity: correlate an unexpected destination with preceding foreign access.
8. Limits/mitigation: debuggers are legitimate users; baseline tooling, reduce cross-process rights and investigate context.

## Early Bird APC injection

1. Mechanism: an APC queued before a thread starts can run before its ordinary routine.
2. Internals: per-thread APC queues and initial thread execution.
3. Prerequisites: access to influence the thread and a suitable queued callback destination.
4. Observables: suspicious startup timing and execution inconsistent with the expected image.
5. Risks: unauthorized early execution and process instability.
6. Telemetry: process-creation context, endpoint APC instrumentation and memory observations.
7. Detection opportunity: correlate unusual early execution with foreign access and suspicious memory.
8. Limits/mitigation: a generic CreateRemoteThread event need not exist; supported endpoint protections and least privilege reduce exposure.

## Parent-process spoofing

1. Mechanism: process creation can designate a parent differing from the initiating process.
2. Internals: extended process-creation attributes and parent-related metadata.
3. Prerequisites: documented rights to the designated parent and control over process creation.
4. Observables: relationships that disagree across provenance sources.
5. Risks: misleading ancestry-based attribution and inherited-security confusion.
6. Telemetry: process creation records plus endpoint creator-context evidence where available.
7. Detection opportunity: compare creator and reported parent with lifetime-aware identifiers.
8. Limits/mitigation: legitimate brokers use parent attributes; avoid parent-PID-only rules and constrain privileged handles.

## Command-line spoofing

1. Mechanism: mutable user-mode process parameters or differing collection times can produce inconsistent command-line views.
2. Internals: process parameters, startup arguments and independent telemetry snapshots.
3. Prerequisites: control of launch metadata or sufficient rights to alter mutable state.
4. Observables: discrepancies between creation-time command line, later queries and program activity.
5. Risks: misleading investigation and monitoring rules.
6. Telemetry: process-creation command-line capture and later behavioral evidence.
7. Detection opportunity: compare independent time-stamped observations, including image identity and files accessed.
8. Limits/mitigation: quoting, truncation and legitimate changes cause noise; preserve original events and never trust one string alone.

## API import concealment

1. Mechanism: runtime resolution can reduce names present in an ordinary static import table.
2. Internals: module/export metadata and function-address indirection.
3. Prerequisites: code capable of locating function addresses and making indirect calls.
4. Observables: sparse imports, resolver activity, indirect API calls or encoded name constants.
5. Risks: impaired static analysis, collision bugs and false confidence in hashes.
6. Telemetry: static PE reports, memory inspection and runtime behavior.
7. Detection opportunity: combine import features with execution observations; sparse imports alone are weak evidence.
8. Limits/mitigation: legitimate software resolves optional APIs; use multi-signal analysis. This harness keeps normal imports visible.

## Sources and interpretation

General cross-process risk and instrumentation context: [Microsoft cross-process injection research](https://www.microsoft.com/security/blog/2017/03/08/uncovering-cross-process-injection-with-windows-defender-atp/). APC semantics, including startup behavior: [QueueUserAPC](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-queueuserapc). Parent attributes: [UpdateProcThreadAttribute](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute). Memory-analysis context: [Microsoft fileless detection discussion](https://azure.microsoft.com/en-us/blog/detecting-fileless-attacks-with-azure-security-center/).

[Sysmon documentation](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon) describes event 1 (process creation), 8 (remote-thread creation), 10 (process access) and 7 (image load, when enabled). These events are not a complete trace of memory writes, context changes or APCs. Availability depends on configuration and sensor coverage. The correlation suggestions above are hypotheses for a defender to validate; no detection accuracy is claimed.

## Safe evidence exercise

`04_TESTING/test_data/synthetic_events.jsonl` explicitly marks every record synthetic. `analyze_synthetic.py` flags a contrived creator/parent mismatch and a memory-change marker after process access. Those markers are educational labels, not authentic Sysmon field mappings or measured attack events. This exercise tests reasoning over records without executing injection or spoofing. Preserve real logs separately if a future authorized defender lab supplies them.


[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
