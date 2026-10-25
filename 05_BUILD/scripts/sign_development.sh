#!/usr/bin/env bash
set -euo pipefail
# Keys remain outside the repository. Caller supplies password through an interactive prompt.
if [[ $# -lt 4 || $# -gt 5 ]]; then printf 'Usage: %s UNSIGNED_EXE SIGNED_EXE CERT_PEM KEY_PEM [PASSWORD_FILE]\n' "$0" >&2; exit 2; fi
[[ "$1" != "$2" ]] || { printf 'Separate output path required\n' >&2; exit 2; }
[[ ! -e "$2" ]] || { printf 'Refusing to overwrite signed output\n' >&2; exit 2; }
password_args=(-askpass)
if [[ $# == 5 ]]; then password_args=(-readpass "$5"); fi
osslsigncode sign "${password_args[@]}" -certs "$3" -key "$4" -h sha256 -n 'Windows LL development research build' -in "$1" -out "$2"
