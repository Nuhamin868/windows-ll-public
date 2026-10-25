# Development Authenticode signing

Signing binds a publisher certificate and integrity claim to a PE image. Public trust depends on a recognized trust chain; a development self-signed certificate has no default public trust. See [Microsoft's trust models](https://learn.microsoft.com/en-us/azure/artifact-signing/concept-trust-models).

Optional Linux procedure after osslsigncode is separately provisioned:

```bash
umask 077
mkdir -p "$HOME/.local/share/windows-ll-signing"
openssl req -x509 -newkey rsa:3072 -sha256 -days 30 \
  -keyout "$HOME/.local/share/windows-ll-signing/dev-key.pem" \
  -out "$HOME/.local/share/windows-ll-signing/dev-cert.pem" \
  -subj '/CN=Windows LL Development Only' \
  -addext 'keyUsage=critical,digitalSignature' \
  -addext 'extendedKeyUsage=codeSigning'
bash 05_BUILD/scripts/sign_development.sh \
  build/windows/windows_ll.exe 06_RELEASE/binaries/windows_ll-dev-signed.exe \
  "$HOME/.local/share/windows-ll-signing/dev-cert.pem" \
  "$HOME/.local/share/windows-ll-signing/dev-key.pem"
bash 05_BUILD/scripts/verify_signature.sh \
  06_RELEASE/binaries/windows_ll-dev-signed.exe \
  "$HOME/.local/share/windows-ll-signing/dev-cert.pem" \
  > 08_EVIDENCE/verification/development-signature.log 2>&1
```

OpenSSL prompts for a key passphrase. The signer should prompt as supported by the installed osslsigncode; do not put passphrases in Git or command-line arguments. Certificate files and keys remain outside the repository. Supplying CAfile to one verification command does not install a Windows trust root. Do not alter the machine's trusted roots for this exercise.

Inspect with `Get-AuthenticodeSignature` on Windows and record the result; an untrusted self-signed chain is expected unless a separate explicit test trust arrangement exists. Preserve unsigned and signed hashes independently. A tampered copy must fail signature integrity verification. No timestamp service, public identity validation or SmartScreen reputation is claimed. Development sign/verify/default-trust rejection/tamper checks passed on 2026-10-25 using osslsigncode. See `08_EVIDENCE/verification/development-signature.log`. Windows Authenticode and public trust are not claimed.

[Project home](../README.md) · [Implementation status](../00_PROJECT_MANAGEMENT/IMPLEMENTATION_STATUS.md)

Automated disposable-key check: `python3 05_BUILD/scripts/check_development_signing.py`. It creates encrypted temporary private material outside Git, verifies the signed executable, checks tampering, and deletes the private key. It refuses to overwrite an existing signed output.
