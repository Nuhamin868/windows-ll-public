"""Exercise a controlled https_fixture_server with normal certificate validation."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import time
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True, help='https://controlled-host, port 443')
    parser.add_argument('--wine', action='store_true')
    parser.add_argument('--rejected-tls-url', action='append', default=[],
                        help='Controlled expired/mismatched/untrusted HTTPS URL; repeat for each')
    parser.add_argument('--server-log', type=Path, required=True,
                        help='Request log from the fixture server, accessible locally')
    args = parser.parse_args()
    url = urlsplit(args.base_url)
    if url.scheme != 'https' or not url.hostname or url.port not in (None, 443) or url.path not in ('', '/') or url.query or url.fragment or url.username or url.password:
        parser.error('base-url must be https://controlled-host on port 443')
    if os.name != 'nt' and not args.wine:
        parser.error('Use --wine on Linux')
    prefix = ['wine'] if args.wine else []
    data = ROOT / '04_TESTING/test_data'
    records = []
    # Read the log before testing; redirect-target must not occur during this run.
    before = args.server_log.read_text().splitlines()

    def case(name, target, host, key, success, diagnostic):
        started = time.monotonic()
        result = subprocess.run(prefix + [str(ROOT / 'build/windows/windows_ll.exe'),
                                'https', target, host, str(data / key)], cwd=ROOT,
                                env=dict(os.environ, WINEDEBUG='-all'), capture_output=True,
                                encoding='utf-8', errors='replace', timeout=50)
        elapsed = time.monotonic() - started
        if (result.returncode == 0) != success or diagnostic not in result.stderr:
            raise RuntimeError(f'{name}: exit={result.returncode}; {result.stderr}')
        if result.stdout.strip():
            raise RuntimeError(f'{name}: unexpected stdout')
        records.append({'case': name, 'exit': result.returncode, 'seconds': round(elapsed, 3)})

    base = args.base_url.rstrip('/')
    host = url.hostname
    for route, ok, message in [('/valid', True, 'artifact_validated'),
                               ('/bad-tag', False, 'authenticated decryption'),
                               ('/bad-schema', False, 'invalid inert schema'),
                               ('/empty', False, 'invalid key/envelope'),
                               ('/truncated', False, 'invalid key/envelope'),
                               ('/redirect', False, 'HTTPS status 302'),
                               ('/redirect301', False, 'HTTPS status 301'),
                               ('/redirect-other', False, 'HTTPS status 302'),
                               ('/404', False, 'HTTPS status 404'),
                               ('/500', False, 'HTTPS status 500'),
                               ('/oversize', False, 'size cap'),
                               ('/oversize-no-length', False, 'size cap'),
                               ('/timeout', False, 'HTTPS receive'),
                               ('/slow-drip', False, 'deadline exceeded')]:
        case(route, base + route, host, 'test-key.bin', ok, message)
    case('wrong key', base + '/valid', host, 'wrong-key.bin', False, 'authenticated decryption')
    # A disconnected response must fail, whether WinHTTP detects truncation or the envelope check does.
    case('disconnect', base + '/disconnect', host, 'test-key.bin', False, 'error')
    for target, allow in [('http://' + host + '/rejected-http', host),
                          (base + '/rejected-host', 'example.invalid'),
                          ('https://' + host + ':444/rejected-port', host),
                          ('https://user:pass@' + host + '/rejected-credentials', host),
                          (base + '/rejected-fragment#x', host)]:
        case('URL rejected', target, allow, 'test-key.bin', False, 'error')
    for target in args.rejected_tls_url:
        tls = urlsplit(target)
        if tls.scheme != 'https' or not tls.hostname or tls.port not in (None, 443):
            parser.error('rejected TLS URLs must use HTTPS port 443')
        case('TLS rejection', target, tls.hostname, 'test-key.bin', False, 'HTTPS send')
    lines = args.server_log.read_text().splitlines()
    if lines[:len(before)] != before:
        raise RuntimeError('Server log was replaced during run')
    paths = [json.loads(line)['path'] for line in lines[len(before):]]
    if '/valid' not in paths or any(p.startswith('/rejected-') or p == '/redirect-target' for p in paths):
        raise RuntimeError('Server request evidence failed')
    report = {'result': 'PASS', 'platform': 'Wine' if args.wine else 'native Windows',
              'cases': records, 'server_paths': paths,
              'certificate_cases_supplied': len(args.rejected_tls_url),
              'limitations': 'Certificate categories require separately configured controlled hosts.'}
    out = ROOT / '08_EVIDENCE/test_logs/https-integration.json'
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(f'PASS {len(records)} controlled HTTPS cases; {out}')


if __name__ == '__main__':
    main()
