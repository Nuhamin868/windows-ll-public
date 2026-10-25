#!/usr/bin/env bash
set -euo pipefail
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
source "$root/05_BUILD/scripts/tool_environment.sh"
mkdir -p "$root/08_EVIDENCE/test_logs"
cmake -S "$root" -B "$root/build/native" -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS='-fsanitize=address,undefined -fno-omit-frame-pointer'
cmake --build "$root/build/native"
ASAN_OPTIONS=detect_leaks=0 ctest --test-dir "$root/build/native" --output-on-failure 2>&1 | tee "$root/08_EVIDENCE/test_logs/native-unit.log"
python3 "$root/04_TESTING/integration/offline_fixture_test.py" 2>&1 | tee "$root/08_EVIDENCE/test_logs/offline-reference.log"
python3 "$root/04_TESTING/integration/analyze_synthetic.py" 2>&1 | tee "$root/08_EVIDENCE/test_logs/synthetic.log"
if command -v wine >/dev/null; then
 python3 "$root/04_TESTING/integration/runtime_validation.py" --wine 2>&1 | tee "$root/08_EVIDENCE/test_logs/wine-runtime.log"
else
 printf 'PENDING: Wine unavailable; run Windows PowerShell integration suite.\n'
fi
