"""Bounded public source discovery, metadata only; titles are unverified claims."""
import datetime,json
from pathlib import Path
import yt_dlp
from inspect_stream import Quiet
ROOT=Path(__file__).resolve().parents[1]
def main():
    out=[]
    for url in ['ytsearch6:Vietlott Power 6/55 21/07/2026','ytsearch4:Vietlott Power 6/55 14/07/2026','https://www.youtube.com/vietlott']:
        try:
            with yt_dlp.YoutubeDL({'quiet':True,'logger':Quiet(),'extract_flat':True,'playlistend':6,'socket_timeout':15,'retries':1}) as y:
                info=y.extract_info(url,download=False)
            entries=list(info.get('entries',[]))[:6]
            out.append({'query':url,'id':info.get('id'),'title':info.get('title'),'channel_id':info.get('channel_id'),
                'webpage_url':info.get('webpage_url'),'entries':[{k:e.get(k) for k in ['id','url','title','channel','channel_id','duration']} for e in entries]})
        except Exception as e:out.append({'query':url,'error_type':type(e).__name__})
    (ROOT/'evidence'/'discovery.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=True))
if __name__=='__main__':main()
