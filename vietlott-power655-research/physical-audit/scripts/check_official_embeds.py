"""Trace video URLs through the operator website; inspect accessible metadata.
No inference from a channel's display name. No cookies or access bypass.
"""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime,timezone
import json,re,hashlib,subprocess
OUT=Path(__file__).resolve().parents[1]
LOCAL=Path('C:/vietlott-research-output/physical-audit-20261022')
class Text(HTMLParser):
 def __init__(self):super().__init__();self.bits=[]
 def handle_data(self,s):self.bits.append(s)
def main():
 h=(LOCAL/'documents/OFFICIAL_VIDEO_PAGE.html').read_text(encoding='utf-8')
 embeds=[]
 for m in re.finditer(r'youtube.com/embed/([a-zA-Z0-9_-]{11})',h):
  s=Text();s.feed(h[m.end():m.end()+1000]);text=' '.join(' '.join(s.bits).split())
  embeds.append(dict(video_id=m.group(1),source_url='https://www.youtube.com/watch?v='+m.group(1),operator_page='https://vietlott.vn/vi/trung-thuong/video-quay-so-mo-thuong',following_text=text[:350]))
 # Index 7 is the first POWER item in the inspected operator page snapshot.
 selected=embeds[7]
 assert 'Power 6/55' in selected['following_text']
 cmd=['C:/vietlott-power655-env/Scripts/python.exe','-m','yt_dlp','--skip-download','--dump-single-json','--socket-timeout','10','--retries','0','--extractor-retries','0',selected['source_url']]
 try:
  r=subprocess.run(cmd,capture_output=True,timeout=90)
  metadata=json.loads(r.stdout) if r.returncode==0 else None
  result=dict(returncode=r.returncode,stderr=r.stderr.decode('utf-8','replace')[-1800:],video_id=selected['video_id'],metadata={k:metadata.get(k) for k in ['id','title','channel','channel_id','duration','upload_date']} if metadata else None)
  if metadata:(LOCAL/'official_embed_full_metadata.json').write_text(json.dumps(metadata),encoding='utf-8')
 except subprocess.TimeoutExpired:result=dict(video_id=selected['video_id'],status='TIMED_OUT_90_SECONDS',metadata=None)
 data=dict(retrieved_utc=datetime.now(timezone.utc).isoformat(),operator_page_sha256=hashlib.sha256(h.encode()).hexdigest(),embeds=embeds,selected_check=result,official_footer_channel_check='yt-dlp returned account terminated due to trademark claim; tool statement only, ownership/claim not independently investigated',limitations='Operator links authenticate link placement, not camera master or asset identity; no new video pixels claimed from metadata')
 (OUT/'extracted/official_embeds.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=True))
if __name__=='__main__':main()
