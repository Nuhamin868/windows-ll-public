# Build guide

Required: CMake 3.20+, Ninja, MinGW-w64 GCC/binutils/headers/CRT/winpthreads, native GCC for portable tests, Python 3 with cryptography, Git. Optional: Wine/Windows x64, OpenSSL/osslsigncode. `check_environment.sh` only inspects; it does not install.

```bash
cd "$HOME/Projects/Windows LL"
bash 05_BUILD/scripts/build.sh
bash 05_BUILD/scripts/test.sh
ASAN_OPTIONS=detect_leaks=0 build/native/winll_inspect build/windows/windows_ll.exe > 08_EVIDENCE/verification/imports.json
x86_64-w64-mingw32-objdump -p build/windows/windows_ll.exe > 08_EVIDENCE/verification/objdump.txt
bash 05_BUILD/scripts/package.sh
```

The CMake toolchain selects Windows AMD64 and cross-GCC. Windows API sources are excluded from native builds. Static C++ runtime linking avoids MinGW runtime DLL distribution; ordinary system DLL imports remain visible. Linker options suppress insertion of current PE timestamps and request NX/ASLR/high-entropy support. Reproducibility requires the same configuration/toolchain; record actual hash comparisons.

System CMake/MinGW were absent. Repository URLs came from pacman -Sp. Archives and signatures were fetched over HTTPS, verified against the host pacman public keyring with gpgv, and extracted under `/tmp/winll-tools/root`. No package installation occurred. Set PATH and LD_LIBRARY_PATH as shown in the README. These temporary files may disappear; permanent provisioning requires separate approval. Exact versions and any relocation settings are in the environment report.

Linux cannot directly execute PE binaries. test.sh optionally runs Windows portable units through Wine, while the PowerShell suite supplies native Windows API coverage. Native reference crypto tests do not validate CNG. Packaging copies the unsigned executable and records SHA-256 without changing its validation status. Consult [test plan](../04_TESTING/TEST_PLAN.md) and [signing](../01_RESEARCH/CODE_SIGNING.md).

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)

Scripts automatically discover the session toolchain under `/tmp/winll-tools/root` when system tools are missing; `WINLL_TOOLS_ROOT` overrides that root. Packaging now builds and runs the available tests before copying, so failed commands cannot silently package an older executable. Temporary tools still disappear if `/tmp` is cleaned.
