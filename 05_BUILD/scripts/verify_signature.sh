#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 || $# -gt 2 ]]; then printf 'Usage: %s EXE [TEST_CA_PEM]\n' "$0" >&2; exit 2; fi
command -v osslsigncode >/dev/null
if [[ $# == 2 ]]; then osslsigncode verify -CAfile "$2" -in "$1"; else osslsigncode verify -in "$1"; fi
