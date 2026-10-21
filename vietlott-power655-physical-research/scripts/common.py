"""Explicit schemas and PTS-based timing. NA never implies zero."""
import csv,hashlib,json,subprocess
from pathlib import Path
EVENTS=['draw_id','event_type','timestamp_seconds','frame_index','confidence','evidence_frame','notes']
PADDLES=['draw_id','timestamp_seconds','frame_index','paddle_id','angle_deg','angular_velocity_deg_s','rpm','tracking_confidence']
BALLS=['draw_id','timestamp_seconds','frame_index','track_id','center_x_px','center_y_px','radius_px','identity_confidence','occluded']
def write_csv(path,fields,rows):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in rows:w.writerow({k:'NA' if r.get(k) is None else r[k] for k in fields})
def read_csv(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def probe(path):
    p=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,check=True)
    return json.loads(p.stdout)
def frame_pts(path):
    p=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(path)],capture_output=True,check=True)
    return [float(f['best_effort_timestamp_time']) for f in json.loads(p.stdout)['frames']]
