"""Offline validation on Windows or Wine; never treats Wine as native Windows."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / '04_TESTING/test_data'
EXE = ROOT / 'build/windows/windows_ll.exe'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wine', action='store_true')
    args = parser.parse_args()
    if os.name != 'nt' and not args.wine:
        parser.error('Use --wine on Linux; native execution requires Windows')
    prefix = ['wine'] if args.wine else []
    env = dict(os.environ, WINEDEBUG='-all')
    cases = []

    def run(label, arguments, success=True, program=EXE, diagnostic=None):
        result = subprocess.run(prefix + [str(program)] + list(map(str, arguments)),
                                cwd=ROOT, env=env, capture_output=True,
                                encoding='utf-8', errors='replace', timeout=60)
        if (result.returncode == 0) != success:
            raise RuntimeError(f'{label}: exit {result.returncode}\n{result.stdout}\n{result.stderr}')
        if diagnostic and diagnostic not in result.stderr:
            raise RuntimeError(f'{label}: expected diagnostic {diagnostic!r}: {result.stderr}')
        cases.append({'case': label, 'exit': result.returncode})
        return result

    run('portable units', [DATA], program=ROOT / 'build/windows/winll_unit.exe')
    run('API units', [DATA], program=ROOT / 'build/windows/winll_windows_unit.exe')
    run('hash', ['hash'])
    result = run('metadata Unicode and spaces', ['metadata', 'space argument', 'λ'])
    rows = [json.loads(line) for line in result.stdout.splitlines()]
    assert rows[0]['pid'] > 0
    assert [row['value'] for row in rows[1:]][-2:] == ['space argument', 'λ']
    result = run('process JSON', ['processes', 'windows_ll'])
    rows = [json.loads(line) for line in result.stdout.splitlines()]
    assert rows and all('windows_ll' in row['name'] for row in rows)
    assert all(isinstance(row['query_error'], int) for row in rows)
    assert run('case sensitive filter', ['processes', 'WINDOWS_LL']).stdout.strip() == ''
    json.loads(run('own PE', ['pe', EXE]).stdout)
    run('valid artifact', ['artifact', DATA / 'artifact.bin', DATA / 'test-key.bin'])
    for name in ['bad-tag.bin', 'bad-schema.bin', 'truncated-artifact.bin']:
        run(name, ['artifact', DATA / name, DATA / 'test-key.bin'], False)
    run('wrong key', ['artifact', DATA / 'artifact.bin', DATA / 'wrong-key.bin'], False)
    run('malformed PE', ['pe', DATA / 'bad_mz.bin'], False)
    run('unknown command', ['unknown'], False)
    for value in ['-1', '30001', '2x']:
        run('invalid hold ' + value, ['hold', value], False)
    key = r'HKCU\Software\WindowsLL\TestArtifacts'
    # Never overwrite user data. The fixed key is required by the application.
    query = subprocess.run(prefix + ['reg', 'query', key], env=env, capture_output=True, timeout=60)
    if query.returncode == 0:
        raise RuntimeError('Test registry key exists; use an isolated account/prefix')
    if query.returncode != 1:
        raise RuntimeError('Cannot establish registry key absence')
    run('registry missing', ['registry', DATA / 'test-key.bin'], False)
    created = False
    try:
        run('create registry key', ['add', key, '/f'], program='reg')
        created = True
        run('registry missing value', ['registry', DATA / 'test-key.bin'], False)
        run('registry wrong type setup', ['add', key, '/v', 'Data', '/t', 'REG_SZ', '/d', 'inert', '/f'], program='reg')
        run('registry wrong type', ['registry', DATA / 'test-key.bin'], False)
        for name, valid in [('artifact.bin', True), ('bad-tag.bin', False), ('bad-schema.bin', False)]:
            run('registry setup ' + name, ['add', key, '/v', 'Data', '/t', 'REG_BINARY', '/d', (DATA / name).read_bytes().hex(), '/f'], program='reg')
            run('registry ' + name, ['registry', DATA / 'test-key.bin'], valid)
    finally:
        if created:
            run('registry cleanup', ['delete', key, '/f'], program='reg')
    with tempfile.TemporaryFile() as err:
        holder = subprocess.Popen(prefix + [str(EXE), 'hold', '30000'], cwd=ROOT,
                                  env=env, stdout=subprocess.DEVNULL, stderr=err)
        try:
            deadline = time.monotonic() + 15
            while True:
                err.seek(0)
                if b'acquired' in err.read():
                    break
                if holder.poll() is not None or time.monotonic() > deadline:
                    raise RuntimeError('Mutex holder failed readiness')
                time.sleep(0.1)
            run('cross process duplicate rejection', ['hash'], False,
                diagnostic='already running')
        finally:
            holder.terminate()
            holder.wait(timeout=15)
    run('mutex reacquisition after termination', ['hash'])
    report = {'platform': 'Wine compatibility (not native Windows)' if args.wine else 'native Windows',
              'cases': cases, 'result': 'PASS',
              'not_covered': ['live HTTPS', 'registry concurrent mutation', 'multiple Windows sessions',
                              'native Windows access denial and ancestry' ]}
    path = ROOT / '08_EVIDENCE/test_logs' / ('wine-integration.json' if args.wine else 'windows-integration.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'PASS {len(cases)} cases; {report["platform"]}; {path}')


if __name__ == '__main__':
    main()
