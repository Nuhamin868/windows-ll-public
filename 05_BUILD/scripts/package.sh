#!/usr/bin/env bash
set -euo pipefail
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
# Never package a previous executable after a failed build or test.
bash "$root/05_BUILD/scripts/build.sh"
bash "$root/05_BUILD/scripts/test.sh"
[[ -f "$root/build/windows/windows_ll.exe" ]]
mkdir -p "$root/06_RELEASE/binaries"
cp -- "$root/build/windows/windows_ll.exe" "$root/06_RELEASE/binaries/windows_ll.exe"
(cd "$root/06_RELEASE"; sha256sum binaries/*.exe > SHA256SUMS)
printf 'Unsigned development package created; runtime validation status is in RELEASE_NOTES.md\n'
