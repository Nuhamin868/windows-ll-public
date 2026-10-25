"""Sign a disposable development build and check explicit trust and tampering."""
import datetime
import os
from pathlib import Path
import secrets
import subprocess
import tempfile
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '06_RELEASE/binaries/windows_ll-dev-signed.exe'
LOG = ROOT / '08_EVIDENCE/verification/development-signature.log'
if OUT.exists():
    raise SystemExit('Signed output already exists; preserve it or move it before rerunning')
OUT.parent.mkdir(parents=True, exist_ok=True)
LOG.parent.mkdir(parents=True, exist_ok=True)
# Private material is encrypted, outside the repository, and deleted on exit.
with tempfile.TemporaryDirectory(prefix='winll-signing-') as temporary:
    secret = Path(temporary)
    os.chmod(secret, 0o700)
    password = secrets.token_urlsafe(48).encode()
    key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Windows LL Development Only')])
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
            .serial_number(x509.random_serial_number()).not_valid_before(now - datetime.timedelta(minutes=5))
            .not_valid_after(now + datetime.timedelta(days=30))
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .add_extension(x509.KeyUsage(digital_signature=True, content_commitment=False, key_encipherment=False,
                           data_encipherment=False, key_agreement=False, key_cert_sign=False, crl_sign=False,
                           encipher_only=None, decipher_only=None), critical=True)
            .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.CODE_SIGNING]), critical=False)
            .sign(key, hashes.SHA256()))
    keyfile, certfile, passfile = [secret / name for name in ('key.pem', 'cert.pem', 'password')]
    keyfile.write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                         serialization.BestAvailableEncryption(password)))
    certfile.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    passfile.write_bytes(password + b'\n')
    for file in (keyfile, certfile, passfile):
        os.chmod(file, 0o600)
    with LOG.open('w') as log:
        def execute(label, command, success):
            result = subprocess.run(list(map(str, command)), cwd=ROOT, capture_output=True, text=True)
            log.write(f'CASE {label}\n{result.stdout}{result.stderr}\nexit={result.returncode}\n')
            log.flush()
            if (result.returncode == 0) != success:
                raise RuntimeError(f'{label} unexpected exit {result.returncode}; see {LOG}')
        execute('development signing', ['bash', ROOT / '05_BUILD/scripts/sign_development.sh',
                ROOT / 'build/windows/windows_ll.exe', OUT, certfile, keyfile, passfile], True)
        execute('explicit development certificate trust', ['osslsigncode', 'verify', '-CAfile', certfile, '-in', OUT], True)
        execute('default trust rejection', ['osslsigncode', 'verify', '-in', OUT], False)
        tampered = secret / 'tampered.exe'
        image = bytearray(OUT.read_bytes())
        # Alter a section byte, outside PE header fields excluded from Authenticode.
        pe = int.from_bytes(image[0x3c:0x40], 'little')
        optional_size = int.from_bytes(image[pe + 20:pe + 22], 'little')
        section = pe + 24 + optional_size
        offset = int.from_bytes(image[section + 20:section + 24], 'little')
        image[offset] ^= 1
        tampered.write_bytes(image)
        execute('tamper detection', ['osslsigncode', 'verify', '-CAfile', certfile, '-in', tampered], False)
        log.write('PASS development sign, explicit trust, default trust rejection, tamper detection\n'
                  'No public trust, timestamp, or Windows Authenticode claim. Temporary private key deleted.\n')
print(f'PASS development signing checks; {LOG}')
