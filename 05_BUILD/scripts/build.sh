#!/usr/bin/env bash
set -euo pipefail
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$root/05_BUILD/scripts/tool_environment.sh"
mkdir -p "$root/08_EVIDENCE/build_logs"
cmake -S "$root" -B "$root/build/windows" -G Ninja -DCMAKE_TOOLCHAIN_FILE="$root/05_BUILD/toolchains/mingw64.cmake" -DCMAKE_BUILD_TYPE=Release 2>&1 | tee "$root/08_EVIDENCE/build_logs/configure.log"
cmake --build "$root/build/windows" 2>&1 | tee "$root/08_EVIDENCE/build_logs/build.log"
