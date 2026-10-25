#!/usr/bin/env bash
# Source this helper; keep environment changes within the calling script.
winll_tools_root="${WINLL_TOOLS_ROOT:-/tmp/winll-tools/root}"
if ! command -v cmake >/dev/null || ! command -v x86_64-w64-mingw32-g++ >/dev/null; then
    if [[ -x "$winll_tools_root/usr/bin/cmake" && -x "$winll_tools_root/usr/bin/x86_64-w64-mingw32-g++" ]]; then
        export PATH="$winll_tools_root/usr/bin:$PATH"
        export LD_LIBRARY_PATH="$winll_tools_root/usr/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
    fi
fi
for winll_tool in cmake ctest ninja x86_64-w64-mingw32-g++; do
    if ! command -v "$winll_tool" >/dev/null; then
        printf 'Missing dependency: %s. Install the documented tools or set WINLL_TOOLS_ROOT to an extracted toolchain root. No packages were installed.\n' "$winll_tool" >&2
        return 1
    fi
done
