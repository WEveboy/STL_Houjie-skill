"""Compile the publication Bundle with a separately installed Cangjie 2.5.0."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cangjie',required=True,type=Path)
    args=parser.parse_args()
    cli=args.cangjie/'scripts/cangjie.py'
    if not cli.is_file():raise ValueError('pass the installed Cangjie root containing scripts/cangjie.py')
    env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
    subprocess.run([sys.executable,str(cli),'compile','--bundle',str(ROOT/'source'),
                    '--out',str(ROOT/'build/recompiled-skill'),'--output','single'],env=env,check=True)
    print('Compiled into build/recompiled-skill. Compare and validate before replacing the frozen installation source.')

if __name__=='__main__':main()
