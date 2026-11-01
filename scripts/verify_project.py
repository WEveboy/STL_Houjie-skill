"""Check published file contracts and relative links; not a semantic evaluator."""
import hashlib
import json
import re
from pathlib import Path
from install_codex import verify

ROOT=Path(__file__).resolve().parents[1]

def main():
    skill=ROOT/'skills/stl-houjie'
    manifest=verify(skill)
    errors=[]
    md_files=[p for p in ROOT.rglob('*.md') if not {'build','dist','.git','__pycache__','.cangjie','runs','snapshots'}.intersection(p.relative_to(ROOT).parts)]
    for p in md_files:
        text=p.read_text(encoding='utf-8')
        if re.search(r'C:[/\\]Users[/\\]HP|BEGIN (?:RSA |OPENSSH )?PRIVATE KEY|github_pat_[A-Za-z0-9_]+',text):
            errors.append(str(p.relative_to(ROOT))+': private path or credential')
        for target in re.findall(r'\]\(([^)\s]+)\)',text):
            target=target.split('#')[0]
            if target and not re.match(r'^[a-z]+:',target) and not (p.parent/target).exists():
                errors.append(str(p.relative_to(ROOT))+': broken link '+target)
    cards=list((skill/'references/capabilities').glob('*.md'))
    for card in cards:
        text=card.read_text(encoding='utf-8')
        for label in ['R','I','A1','A2','E','B']:
            if not re.search(r'^## '+label+r'(?:\s|\b)',text,re.M):
                errors.append(card.name+': missing '+label)
    if len(cards)==0:errors.append('no capability cards')
    for p in (ROOT/'platforms/deepseek/package.json',ROOT/'release-info.json'):
        if json.loads(p.read_text(encoding='utf-8'))['version']!='1.0.0':errors.append('version mismatch')
    if errors:raise ValueError('\n'.join(errors))
    print(json.dumps({'status':'passed','manifest_files':len(manifest['files']),'cards':len(cards),'markdown_links_checked':len(md_files)},ensure_ascii=False))

if __name__=='__main__':main()
