# Compile-time API hash verification

`hash_verification.cpp` demonstrates 32-bit FNV-1a, starting at 2166136261 and multiplying by 16777619 after XORing each byte. Arithmetic wraps in unsigned uint32. `hello` has expected hash `4f9f2cab`; empty text preserves the basis. Four harmless API names have constexpr values compared with runtime evaluation.

`costarring` and `liquid` deliberately produce the same hash. A finite hash cannot uniquely identify arbitrary strings; even collision-free fixture names provide no general guarantee. This hash provides neither secrecy nor cryptographic integrity. It is not used to resolve functions. The implementation's API calls use ordinary imports. The collision and deterministic vectors are checked by the portable unit suite.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)
