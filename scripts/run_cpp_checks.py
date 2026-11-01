"""Compile and run original C++17 checks with the current host compiler."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def locate_source(root):
    choices = [root / 'skills/stl-houjie/resources/contract_checks.cpp',
               root / 'skills/stl-houjie-source/resources/contract_checks.cpp',
               root / 'books/stl-houjie/.cangjie/capabilities/resources/contract_checks.cpp']
    choices.extend(root.glob('skills/*/resources/contract_checks.cpp'))
    return next((x for x in choices if x.is_file()), None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path)
    parser.add_argument('--build-dir', type=Path)
    parser.add_argument('--compiler')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    source = args.source or locate_source(root)
    if source is None:
        # In the authoring workspace this runner lives two directories below its source root.
        source = locate_source(root.parents[1]) if len(root.parents) > 1 else None
    if source is None or not source.is_file():
        print(json.dumps({'status': 'error', 'message': 'contract_checks.cpp not found; use --source'}))
        return 2
    compiler = shutil.which(args.compiler) if args.compiler else next(
        (shutil.which(x) for x in ['g++', 'clang++', 'cl'] if shutil.which(x)), None)
    if not compiler:
        print(json.dumps({'status': 'unavailable', 'message': 'No supported C++ compiler found'}))
        return 2
    build = (args.build_dir or root / 'build/cpp-checks').resolve()
    build.mkdir(parents=True, exist_ok=True)
    exe = build / ('contract_checks.exe' if os.name == 'nt' else 'contract_checks')
    msvc = Path(compiler).stem.lower() == 'cl'
    command = ([compiler, '/nologo', '/std:c++17', '/EHsc', '/W4', '/UNDEBUG', str(source.resolve()),
                '/Fe:' + str(exe), '/Fo:' + str(build / 'contract_checks.obj')]
               if msvc else [compiler, '-std=c++17', '-Wall', '-Wextra', '-pedantic', '-O0',
                             '-UNDEBUG', str(source.resolve()), '-o', str(exe)])
    version_run = subprocess.run([compiler] if msvc else [compiler, '--version'],
                                 capture_output=True, text=True, errors='replace', timeout=30)
    version = (version_run.stdout + version_run.stderr).strip().splitlines()[0]
    compiled = subprocess.run(command, cwd=build, capture_output=True, text=True,
                              errors='replace', timeout=120)
    record = {'compiler': Path(compiler).name, 'compiler_version': version,
              'standard': 'C++17', 'compile_exit_code': compiled.returncode,
              'compile_output': compiled.stdout + compiled.stderr,
              'scope': 'host standard-library experiments; does not verify all historical SGI code'}
    if compiled.returncode:
        record['status'] = 'compile_failed'
    else:
        run = subprocess.run([str(exe)], cwd=build, capture_output=True, text=True,
                             errors='replace', timeout=30)
        record.update({'run_exit_code': run.returncode, 'stderr': run.stderr})
        try:
            record['result'] = json.loads(run.stdout)
            assert record['result']['status'] == 'ok' and record['result']['passed']
            record['status'] = 'ok' if run.returncode == 0 else 'run_failed'
        except (ValueError, KeyError, AssertionError):
            record.update({'status': 'invalid_output', 'stdout': run.stdout})
    (build / 'result.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(record, ensure_ascii=False))
    return 0 if record['status'] == 'ok' else 1


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'status': 'error', 'message': str(exc)}))
        raise SystemExit(1)
