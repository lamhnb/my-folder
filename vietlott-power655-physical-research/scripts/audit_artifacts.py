"""Meaningful deliverable checks; a pass is data integrity, never scientific proof."""
import csv,json,math,re,subprocess,sys
from pathlib import Path
from common import read_csv
ROOT=Path(__file__).resolve().parents[1]
def main():
    failures=[]
    app=read_csv(ROOT/'measurements'/'draw_01372_857_appearance.csv')
    balls=read_csv(ROOT/'measurements'/'draw_01372_ball_tracking.csv')
    if len(app)!=120:failures.append('native appearance frame count !=120')
    if len(balls)!=109:failures.append('candidate detection count !=109')
    ts=[float(r['timestamp_seconds']) for r in app]
    if any(not .03336<y-x<.03338 for x,y in zip(ts,ts[1:])):failures.append('native PTS gap inconsistent')
    if len({r['track_id'] for r in balls})!=len(balls):failures.append('unlinked candidate IDs reused')
    if any(r['identity_confidence']!='NA' or r['occluded']!='NA' or r['frame_index']!='NA' for r in balls):failures.append('unknown identity/index/occlusion filled')
    if any(not (510<=float(r['center_x_px'])<=1410 and 60<=float(r['center_y_px'])<=960) for r in balls):failures.append('candidate outside crop')
    if any(not re.fullmatch('[0-9a-f]{64}',r['native_crop_bgr_sha256']) for r in app):failures.append('invalid frame hash')
    if any(p.stat().st_size and len(read_csv(p)) for p in (ROOT/'measurements').glob('*_paddle_motion.csv')):failures.append('physical paddle rows unexpectedly present')
    ev=[r for p in (ROOT/'measurements').glob('*_events.csv') for r in read_csv(p)]
    if sum(r['timestamp_seconds']=='NA' for r in ev)!=162:failures.append('required NA placeholders changed')
    if any(r['timestamp_seconds']!='NA' and ('phase=' not in r['notes'] or 'reviewed=true' not in r['notes']) for r in ev):failures.append('observed state lacks phase/review')
    for p in ROOT.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts:continue
        if p.suffix.lower() in ('.mp4','.mkv','.webm','.mp3','.wav','.m4a','.mov'):failures.append('media file present: '+p.name)
        if p.suffix.lower() in ('.json','.csv','.md','.txt'):
            txt=p.read_text(encoding='utf-8-sig')
            if re.search(r'https?://[^\s"<>]+(?:googlevideo\.com|i\.ytimg\.com)/[^\s"<>]*[?&](?:sig|sigh|ip|expire)=',txt):failures.append('signed media URL persisted: '+p.name)
    result=subprocess.run([sys.executable,str(ROOT/'scripts'/'test_pipeline.py')],capture_output=True,text=True)
    if result.returncode:failures.append('software tests failed')
    code={'integrity_status':'passed' if not failures else 'failed','failures':failures,'software_tests_exit_code':result.returncode,
        'software_tests_output':result.stderr,'appearance_native_frames':len(app),'unlinked_candidate_rows':len(balls),
        'physical_validated_paddle_rows':0,'unmeasured_required_event_rows':162,'source_frame_pixels_included':False,
        'scientific_completion':'partial; no certified RPM, per-ball tracks, full event annotation or bias test'}
    (ROOT/'evidence'/'artifact_audit.json').write_text(json.dumps(code,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in code.items() if k!='software_tests_output'}));raise SystemExit(bool(failures))
if __name__=='__main__':main()
