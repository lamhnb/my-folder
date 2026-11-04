#!/usr/bin/env python3
"""Extract audit contact sheets from a lawfully obtained local full-draw video.
NO YouTube/SCTV scraping, DRM bypass, or inferred physical ball order.
Requires ffmpeg and ffprobe. Usage:
 python champion_x_extract_draw_evidence.py --input full_draw.mp4 --draw-id 01420 --date 2026-11-05 --every 2
"""
import argparse,csv,hashlib,json,shutil,subprocess
from pathlib import Path

def run(args):
    res=subprocess.run(args,text=True,capture_output=True,check=True)
    return res.stdout.strip()
def digest(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):h.update(block)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True,type=Path)
    ap.add_argument("--draw-id",required=True)
    ap.add_argument("--date",required=True)
    ap.add_argument("--every",type=float,default=2.0,help="Sample every N seconds (2 is for discovery only)")
    ap.add_argument("--output",type=Path,default=Path("physical_video_export"))
    args=ap.parse_args()
    if not args.input.is_file():ap.error("Video must exist locally and be lawfully obtained")
    for tool in ("ffmpeg","ffprobe"):
        if not shutil.which(tool):ap.error(f"Missing {tool}")
    if args.every<=0:ap.error("--every must be positive")
    folder=args.output/args.draw_id
    folder.mkdir(parents=True,exist_ok=True)
    metadata=json.loads(run(["ffprobe","-v","quiet","-show_format","-show_streams","-of","json",str(args.input)]))
    info={"draw_id":args.draw_id,"date":args.date,"filename":args.input.name,
      "sha256":digest(args.input),"duration_seconds":float(metadata.get("format",{}).get("duration",0)),
      "video_streams":[{k:s.get(k) for k in ("codec_name","width","height","avg_frame_rate")}
                       for s in metadata["streams"] if s.get("codec_type")=="video"],
      "extract_interval_seconds":args.every,"full_original_verified":False,
      "ball_order_verified":False,"machine_id":None,"ball_case_id":None}
    (folder/"video_metadata.json").write_text(json.dumps(info,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    fps=1/args.every
    # Numbered contact-sheet pages; image extraction is evidentiary, NOT OCR.
    run(["ffmpeg","-nostdin","-hide_banner","-loglevel","error","-y","-i",str(args.input),
      "-vf",f"fps={fps:.8f},scale=400:-2,tile=5x5:nb_frames=25:padding=4:margin=4",
      "-vsync","vfr",str(folder/"contact_%04d.jpg")])
    with (folder/"seven_ball_manual_annotation.csv").open("w",newline="",encoding="utf8") as f:
        w=csv.writer(f);w.writerow(["draw_id","date","ball_position","observed_ball_label","timestamp_sec",
          "verified_uncut_frame","source_frame_or_timecode","reviewer1","reviewer2","agreement","notes"])
        for position in range(1,8):w.writerow([args.draw_id,args.date,position,"","","","","","","",""])
    (folder/"README.md").write_text(
      "# Physical draw export — evidence, not a prediction\n\n"
      "Contact sheets sampled periodically help locate mechanical draw segments, "
      "but 2-second sampling may SKIP rapid ball exits. Review original video frame by frame "
      "around each event and record exact visible physical order and timecodes.\n\n"
      "Do not interpret sorted displayed results as chronological ball order. "
      "Two independent reviewers must verify six main balls as a set plus seventh special. "
      "Never guess illegible labels or infer machine/ball-case IDs.\n",encoding="utf8")
    print(json.dumps({"output":str(folder),"contact_sheets":len(list(folder.glob("contact_*.jpg"))),
       "duration_seconds":info["duration_seconds"],"sha256":info["sha256"],"ball_order_verified":False}))
if __name__=="__main__":main()
