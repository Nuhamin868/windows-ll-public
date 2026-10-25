# Authenticated memory-only artifact validation

The CNG adapter uses [BCryptDecrypt](https://learn.microsoft.com/en-us/windows/win32/api/bcrypt/nf-bcrypt-bcryptdecrypt) in GCM mode with authenticated cipher-mode information. The fixed header is AAD. Authentication failure stops processing before plaintext schema inspection. AES-256-GCM is an established API primitive; the project implements no cipher.

Our envelope, inert schema, exact sizes and zeroing strategy are specified in [implementation details](../07_DOCUMENTATION/IMPLEMENTATION_DETAILS.md). Python cryptography generates and independently validates deterministic fixtures; that establishes reference interoperability only until CNG runs on Windows. The buffer is ordinary data memory, never changed to executable permissions or used as instructions. Clearing explicit buffers does not guarantee erasure of OS paging or crash-dump copies.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
