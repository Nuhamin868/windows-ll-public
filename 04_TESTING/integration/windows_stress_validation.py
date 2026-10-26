"""Native Windows acceptance probes. Stress coverage does not force PID reuse."""
import collections
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
EXE = ROOT / 'build/windows/windows_ll.exe'
DATA = ROOT / '04_TESTING/test_data'


def main():
    if os.name != 'nt':
        raise SystemExit('Native Windows required; Wine is not accepted for this runner')
    import winreg

    def run(*args):
        return subprocess.run([str(EXE), *map(str, args)], cwd=ROOT,
                              capture_output=True, text=True, encoding='utf-8',
                              errors='replace', timeout=20)

    records = []
    result = run('processes')
    if result.returncode:
        raise RuntimeError(result.stderr)
    rows = [json.loads(line) for line in result.stdout.splitlines()]
    denied = [row for row in rows if row['query_error'] == 5]
    if any(row['architecture'] != 'unknown' for row in denied):
        raise RuntimeError('Access-denied process incorrectly reports a known architecture')
    records.append({'case': 'native process access denial',
                    'result': 'PASS' if denied else 'UNVERIFIED',
                    'observations': denied,
                    'limitation': 'A runner with no denied process cannot prove denial handling'})

    result = run('metadata')
    metadata = json.loads(result.stdout.splitlines()[0])
    if result.returncode or metadata['reported_parent_pid'] != os.getpid():
        raise RuntimeError('Observed parent did not match the live launcher')
    records.append({'case': 'live launcher parent observation', 'result': 'PASS',
                    'launcher_pid': os.getpid(), 'metadata': metadata,
                    'limitation': 'Does not establish historical ancestry or force PID reuse'})

    stop = threading.Event()
    errors = []
    children = []

    def churn():
        try:
            while not stop.is_set():
                child = subprocess.Popen([sys.executable, '-c', 'pass'],
                                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                children.append(child.pid)
                child.wait(timeout=10)
        except Exception as exc:
            errors.append(repr(exc))

    worker = threading.Thread(target=churn)
    worker.start()
    try:
        for _ in range(20):
            result = run('processes')
            if result.returncode:
                raise RuntimeError(result.stderr)
            observations = [json.loads(line) for line in result.stdout.splitlines()]
            if not observations or any(not isinstance(row['query_error'], int) for row in observations):
                raise RuntimeError('Malformed inventory during process churn')
    finally:
        stop.set()
        worker.join(timeout=15)
    if worker.is_alive() or errors or not children:
        raise RuntimeError(f'Process churn failed: {errors}')
    records.append({'case': 'process exit during enumeration stress', 'result': 'PASS',
                    'enumerations': 20, 'children_created': len(children),
                    'repeated_pids_observed': len(children) - len(set(children)),
                    'limitation': 'Stress run; a snapshot/query race or PID reuse is not guaranteed'})

    path = r'Software\WindowsLL\TestArtifacts'
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path):
            pass
    except FileNotFoundError:
        pass
    else:
        raise RuntimeError('Pre-existing registry test key; refusing to overwrite')
    valid = (DATA / 'artifact.bin').read_bytes()
    outcomes = collections.Counter()
    writes = collections.Counter()
    stop.clear()

    def mutate():
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE) as key:
                while not stop.is_set():
                    for label, kind, data in [('valid', winreg.REG_BINARY, valid),
                                              ('bad-tag', winreg.REG_BINARY, (DATA / 'bad-tag.bin').read_bytes()),
                                              ('oversize', winreg.REG_BINARY, b'A' * 1048577),
                                              ('wrong-type', winreg.REG_SZ, 'inert')]:
                        winreg.SetValueEx(key, 'Data', 0, kind, data)
                        writes[label] += 1
                        if stop.wait(0.002):
                            return
        except Exception as exc:
            errors.append(repr(exc))

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, path) as key:
        winreg.SetValueEx(key, 'Data', 0, winreg.REG_BINARY, valid)
    worker = threading.Thread(target=mutate)
    worker.start()
    try:
        for _ in range(60):
            result = run('registry', DATA / 'test-key.bin')
            if result.stdout.strip():
                raise RuntimeError('Registry run exported unexpected stdout')
            if result.returncode == 0:
                if 'artifact_validated' not in result.stderr:
                    raise RuntimeError('Success without authenticated validation')
                outcomes['authenticated success'] += 1
            elif result.returncode == 1 and any(msg in result.stderr for msg in (
                    'invalid registry artifact size/type', 'registry read changed or failed',
                    'authenticated decryption', 'invalid key/envelope', 'invalid inert schema')):
                outcomes['safe rejection'] += 1
            else:
                raise RuntimeError(f'Unexpected exit {result.returncode}: {result.stderr}')
    finally:
        stop.set()
        worker.join(timeout=15)
        if not worker.is_alive():
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, path)
    if worker.is_alive() or errors or not writes:
        raise RuntimeError(f'Registry writer failed: {errors}')
    records.append({'case': 'concurrent registry mutation stress', 'result': 'PASS',
                    'reads': 60, 'writes': dict(writes), 'outcomes': dict(outcomes),
                    'limitation': 'Concurrent stress, not deterministic scheduling between the two native reads'})
    overall = 'PASS' if denied else 'PARTIAL'
    report = {'platform': 'native Windows', 'os': platform.platform(), 'result': overall,
              'cases': records, 'remaining': ['forced PID reuse / historical ancestry',
                                            'multiple Windows sessions', 'controlled HTTPS matrix']}
    out = ROOT / '08_EVIDENCE/test_logs/windows-stress.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(f'{overall}: {len(records)} native Windows probes; {out}')


if __name__ == '__main__':
    main()
