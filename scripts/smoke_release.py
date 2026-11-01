"""Extract the real Codex archive and run its packaged tool after install."""
import argparse
import json
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path);args=parser.parse_args()
    if args.out:
        args.out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='stl-smoke-') as tmp:
        work=Path(tmp)
        with zipfile.ZipFile(ROOT/'dist/stl-houjie-Codex-1.0.0.zip') as z:
            if z.testzip() is not None:raise ValueError('archive CRC failed')
            if any(not (work/'codex'/name).resolve().is_relative_to((work/'codex').resolve()) for name in z.namelist()):
                raise ValueError('unsafe archive path')
            z.extractall(work/'codex')
        result=subprocess.run([sys.executable,str(work/'codex/install_codex.py'),'--destination',str(work/'installed')],check=True,capture_output=True,text=True,encoding='utf-8')
        lab=work/'installed/stl-houjie/resources/stl_lab.py'
        run=subprocess.run([sys.executable,str(lab),'demo'],check=True,capture_output=True,text=True,encoding='utf-8')
        operations=subprocess.run([sys.executable,str(lab),'operations'],check=True,capture_output=True,text=True,encoding='utf-8')
        if len(json.loads(operations.stdout)['operations'])!=11:raise ValueError('extension modules missing')
        input_file=work/'tree.json';input_file.write_text('{"op":"tree-check","root":null,"nodes":[]}',encoding='utf-8')
        subprocess.run([sys.executable,str(lab),'experiment',str(input_file),'--out',str(work/'experiment')],check=True,capture_output=True)
        workflow=subprocess.run([sys.executable,str(lab),'audit',str(work/'experiment'),'--recompute'],check=True,capture_output=True,text=True,encoding='utf-8')
        with tarfile.open(ROOT/'dist/dsh-stl-houjie-1.0.0.tgz') as t:
            if not t.getmember('package/skills/stl-houjie/SKILL.md').isfile():raise ValueError('DSH entry missing')
        report={'status':'passed','installation':json.loads(result.stdout),'tool_output':json.loads(run.stdout),'operations':json.loads(operations.stdout),'archive_recompute':json.loads(workflow.stdout),'dsh_archive':'entry present; actual Harness session not executed'}
        report['installation'].pop('target',None);report['installation'].pop('backup',None)
        if args.out:(args.out/'archive-smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
