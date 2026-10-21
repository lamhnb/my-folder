"""Find ASR caption landmarks as navigation aids; never physical event evidence.

No transcript stored, only category/time/status. ASR may be wrong or misaligned.
"""
import argparse,datetime,json,unicodedata,urllib.request
from pathlib import Path
from inspect_stream import metadata
ROOT=Path(__file__).resolve().parents[1]
def plain(s):return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn').replace('đ','d')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('ids',nargs='+');args=ap.parse_args();out=[]
    for vid in args.ids:
        info,_=metadata(vid);options=info.get('automatic_captions',{}).get('vi-orig',[])
        formats=[f for f in options if f.get('ext')=='json3']
        if not formats:out.append({'video_id':vid,'status':'no_original_vi_json3'});continue
        try:
            req=urllib.request.Request(formats[0]['url'],headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=20) as r:data=json.load(r)
            landmarks=[];printed=0
            for e in data.get('events',[]):
                t=e.get('tStartMs',0)/1000;txt=''.join(s.get('utf8','') for s in e.get('segs',[]));norm=plain(txt)
                cats=[k for k,term in [('official','chinh thuc'),('pretest','kiem tra'),('mix','tron bong'),('load','nap bong'),('power','power')] if term in norm]
                if 'quay thử' in txt.lower():cats.append('trial_keyword')
                if cats:
                    landmarks.append({'source_caption_seconds':t,'categories':cats,'evidence_level':'automatic_caption_navigation_only'})
                    # Keep no transcript excerpts in output/artifacts.
            out.append({'video_id':vid,'status':'navigation_only_not_verified_speech','landmarks':landmarks})
        except Exception as e:out.append({'video_id':vid,'status':'caption_fetch_failed','error_type':type(e).__name__})
    (ROOT/'evidence'/'caption_landmarks.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps({'statuses':[(x['video_id'],x['status']) for x in out]}))
if __name__=='__main__':main()
