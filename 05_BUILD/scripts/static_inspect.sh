#!/usr/bin/env bash
set -euo pipefail
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$root/05_BUILD/scripts/tool_environment.sh"
mkdir -p "$root/08_EVIDENCE/verification"
file "$root/build/windows/windows_ll.exe" > "$root/08_EVIDENCE/verification/file.txt"
x86_64-w64-mingw32-objdump -p "$root/build/windows/windows_ll.exe" > "$root/08_EVIDENCE/verification/objdump.txt"
ASAN_OPTIONS=detect_leaks=0 "$root/build/native/winll_inspect" "$root/build/windows/windows_ll.exe" > "$root/08_EVIDENCE/verification/imports.json"
