#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,struct
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
p=Path(__file__).resolve().parents[1]/'test_data'
manifest=json.loads((p/'manifest.json').read_text())
for name,sha in manifest.items():
 if hashlib.sha256((p/name).read_bytes()).hexdigest()!=sha: raise RuntimeError('fixture digest mismatch: '+name)
key=(p/'test-key.bin').read_bytes()
def decrypt(name,k=key):
 b=(p/name).read_bytes()
 if len(b)<33 or b[:4]!=b'WLL1': raise ValueError('envelope')
 return AESGCM(k).decrypt(b[4:16],b[32:]+b[16:32],b[:4])
def schema(b):
 return len(b)>=8 and b[:5]==b'WLLD\x01' and 1<=int.from_bytes(b[5:7],'little')<=256 and len(b)==7+int.from_bytes(b[5:7],'little') and all(32<=c<=126 for c in b[7:])
if not schema(decrypt('artifact.bin')):raise RuntimeError('schema')
for name,k in [('bad-tag.bin',key),('artifact.bin',b'\xff'*32)]:
 try:decrypt(name,k)
 except InvalidTag:pass
 else:raise RuntimeError('authentication unexpectedly accepted')
if schema(decrypt('bad-schema.bin')):raise RuntimeError('invalid schema accepted')
try:decrypt('truncated-artifact.bin')
except ValueError:pass
else:raise RuntimeError('truncated envelope accepted')
print('PASS 13 fixture SHA-256 digests; AES-GCM valid/tag-failure/wrong-key/schema/truncation reference checks (Python, not Windows CNG)')
