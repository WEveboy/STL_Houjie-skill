"""Install the complete stl-houjie folder after byte-level manifest checks."""
import argparse
import datetime
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

NAME = 'stl-houjie'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def source_directory():
    here = Path(__file__).resolve().parent
    for folder in (here / NAME, here.parent / 'skills' / NAME):
        if (folder / 'EDITION.json').is_file():
            return folder
    raise ValueError('cannot find the complete packaged skill')

def verify(folder):
    if folder.is_symlink():
        raise ValueError('skill root must not be a symbolic link')
    manifest = json.loads((folder / 'EDITION.json').read_text(encoding='utf-8'))
    actual = {p.relative_to(folder).as_posix() for p in folder.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    if actual != set(manifest['files']) | {'EDITION.json'}:
        raise ValueError('manifest file set mismatch')
    for name, expected in manifest['files'].items():
        p = folder / name
        if p.is_symlink() or not p.resolve().is_relative_to(folder.resolve()) or digest(p) != expected:
            raise ValueError('source integrity failed: ' + name)
    return manifest

def install(destination, replace=False, source=None):
    source = Path(source) if source else source_directory()
    edition = verify(source)
    root = Path(destination).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    target = root / NAME
    if target.is_symlink():
        raise ValueError('refusing a symlink installation target')
    if target.exists() and not replace:
        raise ValueError('already installed; intentional upgrades require --replace')
    if target.exists() and not target.is_dir():
        raise ValueError('installation target is not a directory')
    backup = None
    with tempfile.TemporaryDirectory(prefix='.stl-stage-', dir=root) as tmp:
        staged = Path(tmp) / NAME
        shutil.copytree(source, staged)
        verify(staged)
        if target.exists():
            backup = root / (NAME + '.backup-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
            if target.resolve().parent != root or backup.resolve().parent != root:
                raise ValueError('containment check failed')
            target.rename(backup)
        try:
            staged.rename(target)
        except BaseException:
            if backup is not None:
                backup.rename(target)
            raise
    verify(target)
    return {'status':'installed_and_verified','version':edition['version'],'target':str(target),'backup':str(backup) if backup else None}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--destination', type=Path, default=Path.home()/'.agents'/'skills')
    p.add_argument('--replace',action='store_true')
    a=p.parse_args()
    try:
        print(json.dumps(install(a.destination,a.replace),ensure_ascii=False,indent=2))
    except (ValueError,OSError) as e:
        p.exit(2,'error: '+str(e)+'\n')

if __name__=='__main__':
    main()
