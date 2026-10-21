"""Strict allowlist archive: no video, audio, source stills, env or credentials."""
import argparse,csv,hashlib,json,zipfile
from pathlib import Path
from common import write_csv,digest
ROOT=Path(__file__).resolve().parents[1]
ALLOWED={'.md','.csv','.json','.py','.txt'}
CHARTS={'appearance_phase.png','appearance_spectrum.png','candidate_detection_density.png'}
def files():
    out=[]
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts or p.name=='file_manifest.csv':continue
        rel=p.relative_to(ROOT)
        if p.name in ('.gitignore','.gitattributes') or p.suffix in ALLOWED or (len(rel.parts)==2 and rel.parts[0]=='charts' and p.name in CHARTS):out.append(p)
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    if args.out.exists():raise SystemExit('Refusing to overwrite existing handoff archive')
    audit=json.loads((ROOT/'evidence'/'artifact_audit.json').read_text())
    if audit['integrity_status']!='passed':raise SystemExit('Artifact integrity failed')
    selected=files()
    write_csv(ROOT/'file_manifest.csv',['path','bytes','sha256'],[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in selected])
    selected.append(ROOT/'file_manifest.csv');args.out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in selected:z.write(p,ROOT.name+'/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(args.out) as z:
        if z.testzip():raise RuntimeError('ZIP CRC failure')
        for p in selected:
            b=z.read(ROOT.name+'/'+p.relative_to(ROOT).as_posix())
            if hashlib.sha256(b).hexdigest()!=digest(p):raise RuntimeError('ZIP file hash mismatch')
    sha=digest(args.out);args.out.with_suffix('.zip.sha256.txt').write_text(sha+'  '+args.out.name+'\n',encoding='utf-8')
    print(json.dumps({'zip':str(args.out),'sha256':sha,'files':len(selected),'bytes':args.out.stat().st_size,'crc_and_hash_verification':'passed','media_files':0}))
if __name__=='__main__':main()
