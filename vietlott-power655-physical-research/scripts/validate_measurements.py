"""Schema/integrity checks distinguish empty data from successful measurements."""
import argparse,csv,json,math
from pathlib import Path
from common import read_csv,EVENTS,PADDLES,BALLS
def validate(root):
    problems=[];counts={};measured=0
    schemas={'events':EVENTS,'paddle_motion':PADDLES,'ball_tracking':BALLS}
    for kind,fields in schemas.items():
        counts[kind]=0
        for p in sorted((root/'measurements').glob('*_'+kind+'.csv')):
            with p.open(encoding='utf-8-sig',newline='') as f:
                rd=csv.DictReader(f)
                if rd.fieldnames!=fields:problems.append(f'{p.name}: schema mismatch')
                for i,r in enumerate(rd,2):
                    counts[kind]+=1
                    for k in fields:
                        if r.get(k) in (None,''):problems.append(f'{p.name}:{i}: empty {k}; use NA')
                    if r.get('timestamp_seconds') not in ('NA',None,''):
                        try:
                            val=float(r['timestamp_seconds'])
                            if not math.isfinite(val) or val<0:raise ValueError()
                            measured+=1
                        except ValueError:problems.append(f'{p.name}:{i}: invalid timestamp')
                    if kind=='events' and r.get('timestamp_seconds')!='NA':
                        if 'reviewed=true' not in r.get('notes',''):problems.append(f'{p.name}:{i}: event lacks manual review')
                    ef=r.get('evidence_frame','NA')
                    if ef not in ('NA',None,'') and not ef.startswith('https://') and not (root/ef).is_file():problems.append(f'{p.name}:{i}: missing evidence')
    return {'schema_integrity':'passed' if not problems else 'failed','counts':counts,'timestamped_rows':measured,
            'experimental_completion':'no_measurements' if measured==0 else 'requires_scientific_review','problems':problems}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--out',type=Path);args=ap.parse_args();r=validate(args.root)
    if args.out:args.out.write_text(json.dumps(r,indent=2),encoding='utf-8')
    print(json.dumps(r));raise SystemExit(bool(r['problems']))
if __name__=='__main__':main()
