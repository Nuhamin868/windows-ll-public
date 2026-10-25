#!/usr/bin/env bash
set -u
printf 'Windows LL environment: '; date -Is
uname -a
missing=0
for tool in cmake ninja x86_64-w64-mingw32-g++ python3 git; do
 if command -v "$tool"; then :; else printf 'MISSING REQUIRED: %s\n' "$tool"; missing=1; fi
done
for tool in wine osslsigncode openssl; do command -v "$tool" || printf 'OPTIONAL UNAVAILABLE: %s\n' "$tool"; done
exit "$missing"
