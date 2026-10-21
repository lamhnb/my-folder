"""Inspect public caption availability only; no media downloads or transcript archive."""
import json
from inspect_stream import metadata
def main():
    for vid in ['IUU05082QtE','diq_elyRXjo','LUEP3hWibQw','Eid9PPhMn_0','is8GgE2gQu8','GidYNrF55XY']:
        try:
            info,_=metadata(vid)
            print(json.dumps({'video_id':vid,'manual_languages':list(info.get('subtitles',{})),'automatic_languages':list(info.get('automatic_captions',{}))},ensure_ascii=True),flush=True)
        except Exception as e:print(json.dumps({'video_id':vid,'error_type':type(e).__name__}))
if __name__=='__main__':main()
