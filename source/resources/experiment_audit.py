"""Archive and recompute local teaching experiments. Hashes are not signatures."""
import datetime
import hashlib
import json
import os
import platform
import shutil
import sys
import tempfile
from pathlib import Path

VERSION='1.0.0'
FILES=('input.json','result.json','events.json')
def encoded(value):return (json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n').encode('utf-8')
def sha(data):return hashlib.sha256(data).hexdigest()
def code_fingerprint():
    root=Path(__file__).resolve().parent
    return {n:sha((root/n).read_bytes()) for n in ['stl_lab.py','stl_extensions.py','experiment_audit.py']}

def create(input_file,out,load,run):
    out=Path(out).expanduser().absolute()
    if out.exists() or out.is_symlink():raise ValueError('experiment output already exists; use a new directory')
    data=load(input_file);result=run(data) # Validate before creating output.
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.parent.resolve()/out.name != out.resolve():raise ValueError('unsafe experiment destination')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    payloads={'input.json':encoded(data),'result.json':encoded(result),
              'events.json':encoded([{'sequence':0,'stage':'input_validated','utc':now},
                                    {'sequence':1,'stage':'computed','utc':now},
                                    {'sequence':2,'stage':'archived','utc':now}])}
    manifest={'schema_version':1,'tool_version':VERSION,'operation':data['op'],
              'python':platform.python_version(),'platform':sys.platform,
              'files':{n:sha(b) for n,b in payloads.items()},'code':code_fingerprint(),
              'hash_scope':'content consistency only; no authentication or independent algorithm proof'}
    with tempfile.TemporaryDirectory(prefix='.stl-experiment-',dir=out.parent) as temp:
        staged=Path(temp)/'archive';staged.mkdir()
        for name,content in payloads.items():(staged/name).write_bytes(content)
        (staged/'manifest.json').write_bytes(encoded(manifest))
        # rename is no-clobber on Windows; explicit recheck protects ordinary reruns.
        if out.exists():raise ValueError('output appeared during preparation')
        staged.rename(out)
    return {'status':'archived','directory':str(out),'operation':data['op'],'files':list(payloads)+['manifest.json']}

def audit(directory,recompute,load,run):
    root=Path(directory).resolve()
    if not root.is_dir():raise ValueError('experiment directory not found')
    failures=[]
    for name in FILES+('manifest.json',):
        p=root/name
        if p.is_symlink() or not p.is_file():raise ValueError('missing or symbolic experiment file: '+name)
    manifest=load(root/'manifest.json')
    if type(manifest) is not dict or manifest.get('schema_version')!=1:raise ValueError('invalid manifest schema')
    required={'schema_version','tool_version','operation','python','platform','files','code','hash_scope'}
    if set(manifest)!=required or type(manifest['files']) is not dict or set(manifest['files'])!=set(FILES):raise ValueError('manifest contract mismatch')
    for name in FILES:
        if sha((root/name).read_bytes())!=manifest['files'][name]:failures.append('hash:'+name)
    if manifest['tool_version']!=VERSION:failures.append('tool-version')
    if manifest['code']!=code_fingerprint():failures.append('code-fingerprint')
    data=load(root/'input.json');stored=load(root/'result.json',max_bytes=2*1024*1024);events=load(root/'events.json')
    if type(data) is not dict or type(stored) is not dict:raise ValueError('input and result must be JSON objects')
    if data.get('op')!=manifest['operation']:failures.append('operation')
    expected_stages=['input_validated','computed','archived']
    if type(events) is not list or len(events)!=3:failures.append('events-shape')
    else:
        previous=None
        for i,event in enumerate(events):
            if type(event) is not dict or set(event)!={'sequence','stage','utc'} or type(event.get('sequence')) is not int or event.get('sequence')!=i or event.get('stage')!=expected_stages[i]:
                failures.append('events-sequence');continue
            try:
                stamp=datetime.datetime.fromisoformat(event['utc'])
                if stamp.tzinfo is None or (previous is not None and stamp<previous):raise ValueError('invalid event time')
                previous=stamp
            except (ValueError,TypeError):failures.append('events-time')
    recomputed=None
    if recompute:
        actual=run(data)
        # Compare the serialized JSON model, including dictionary key normalization.
        recomputed=encoded(json.loads(encoded(actual)))==encoded(stored)
        if not recomputed:failures.append('recomputed-result')
    return {'status':'ok' if not failures else 'audit_failed','checks':{'hashes':not any(x.startswith('hash:') for x in failures),'recomputed':recomputed},'failures':failures,
            'scope':'reuses installed teaching algorithms; coordinated manifest edits are not authenticated'}
