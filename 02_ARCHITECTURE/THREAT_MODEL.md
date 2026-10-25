# Threat model

Trust boundaries: external PE/ciphertext files, HKCU registry data, remote HTTPS bytes, and operating-system snapshot/API results. Treat all artifact bytes as attacker-controlled even after TLS; AES-GCM authenticates them using a caller-supplied 32-byte key. With the public fixture key, authentication provides a reproducible test rather than adversarial provenance.

Defended properties: bounded reads, deterministic parsing failure, explicit origin allowlisting, rejection of malformed/authentication-invalid artifacts, strict inert schema, no execution path from bytes, RAII cleanup, visible API imports. OS TLS validation is retained; redirects cannot extend the allowlist.

Not defended: a compromised host, hostile same-user process or named object precreation, paging/crash dump disclosure, a user explicitly approving a malicious allowlist host, production key storage, inference of true parent identity, or exhaustive PE compatibility. Process inventory is observational and can race process exit. No privileged rights are requested. Review [security analysis](../07_DOCUMENTATION/SECURITY_ANALYSIS.md).

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
