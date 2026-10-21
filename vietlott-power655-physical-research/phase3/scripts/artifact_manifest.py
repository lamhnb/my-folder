"""Hash publishable Phase 3 artifacts (gitignore respected); exclude manifest itself."""
import csv
import subprocess
from pathlib import Path
from extract_pilot import sha
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
PREFIX='vietlott-power655-physical-research/phase3/'

def main():
    paths=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z','--',PREFIX],cwd=REPO).decode().split('\0')
    rows=[]
    for name in sorted(set(filter(None,paths))):
        path=REPO/name
        if path.name=='artifact_manifest.csv':continue
        rows.append(dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path),bytes=path.stat().st_size))
    with (ROOT/'artifact_manifest.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['path','sha256','bytes']);w.writeheader();w.writerows(rows)
    print(f'{len(rows)} artifacts; {sum(r["bytes"] for r in rows)} bytes')
if __name__=='__main__':main()
