from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re
OUT=Path(__file__).resolve().parents[1]
LOCAL=Path('C:/vietlott-research-output/physical-audit-20261022/documents')
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('href','src') and v:self.links.append(v)
def main():
 p=LOCAL/'VIETLOTT.html';h=p.read_text(encoding='utf-8',errors='replace');s=Links();s.feed(h)
 relevant=sorted(set(x for x in s.links if any(k in x.lower() for k in ['cong-bo','dau-thau','thiet-bi','quay-so','youtube','the-le','quy-trinh'])))
 data=dict(source_url='https://vietlott.vn/',source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),title=re.findall('<title>(.*?)</title>',h,re.S),links=relevant,video_ids=sorted(set(re.findall(r'(?:youtu.be/|youtube.com/(?:embed/|watch\?v=))([a-zA-Z0-9_-]{11})',h))))
 (OUT/'extracted/official_site_links.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
 print(json.dumps(data,ensure_ascii=True))
if __name__=='__main__':main()
