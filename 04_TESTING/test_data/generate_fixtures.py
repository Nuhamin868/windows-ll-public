#!/usr/bin/env python3
"""Creates inert data and non-loadable PE parser fixtures, never payload code."""
from pathlib import Path
import struct, hashlib, json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
root=Path(__file__).resolve().parent

def pe(x64=True):
 b=bytearray(1024)
 def u(o,v,n=4): b[o:o+n]=v.to_bytes(n,'little')
 b[:2]=b'MZ';u(60,128);b[128:132]=b'PE\0\0';u(132,0x8664 if x64 else 0x14c,2);u(134,1,2)
 opts=240 if x64 else 224;u(148,opts,2);u(150,0x22,2);o=152
 u(o,0x20b if x64 else 0x10b,2);u(o+32,4096);u(o+36,512);u(o+56,8192);u(o+60,512)
 d=112 if x64 else 96;u(o+d-4,16);u(o+d+8,4096);u(o+d+12,40)
 s=o+opts;b[s:s+8]=b'.idata\0\0';u(s+8,512);u(s+12,4096);u(s+16,512);u(s+20,512)
 u(512,0x1040);u(524,0x1080);u(528,0x1040)
 step=8 if x64 else 4;u(576,0x10a0,step);u(576+step,(1<<(63 if x64 else 31))|7,step)
 b[640:653]=b'KERNEL32.dll\0';b[674:694]=b'GetCurrentProcessId\0'
 return b
fixtures={'pe64.bin':pe(),'pe32.bin':pe(False),'bad_mz.bin':b'not a PE'}
b=pe();b[152+120:152+124]=(0xfffffff0).to_bytes(4,'little');fixtures['bad_rva.bin']=b
b=pe();b[532:552]=b'\x01'*20;fixtures['bad_descriptor.bin']=b
b=pe();b[576:584]=(0x8000000000010001).to_bytes(8,'little');fixtures['bad_ordinal.bin']=b
b=pe();b[152+108:152+112]=(17).to_bytes(4,'little');fixtures['bad_directories.bin']=b
key=bytes(range(32));nonce=bytes(range(12));plain=b'WLLD\x01'+struct.pack('<H',19)+b'inert research data'
def envelope(data):
 encrypted=AESGCM(key).encrypt(nonce,data,b'WLL1')
 return b'WLL1'+nonce+encrypted[-16:]+encrypted[:-16]
fixtures['test-key.bin']=key;fixtures['artifact.bin']=envelope(plain)
b=bytearray(fixtures['artifact.bin']);b[16]^=1;fixtures['bad-tag.bin']=b
fixtures['bad-schema.bin']=envelope(b'MZ inert invalid schema')
fixtures['truncated-artifact.bin']=fixtures['artifact.bin'][:20]
fixtures['wrong-key.bin']=b'\xff'*32
for name,b in fixtures.items(): (root/name).write_bytes(b)
(root/'manifest.json').write_text(json.dumps({name:hashlib.sha256(b).hexdigest() for name,b in sorted(fixtures.items())},indent=2)+'\n')
print(f'Generated {len(fixtures)} inert fixtures. Fixed key/nonce are public test vectors only.')
