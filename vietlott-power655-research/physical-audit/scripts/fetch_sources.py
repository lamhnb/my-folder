"""Bounded primary-source HTTP recheck; no access-control bypass.
Keep source bytes locally; publish status, URL, digest and limited factual notes.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,urllib.request,urllib.error
OUT=Path(__file__).resolve().parents[1]
LOCAL=Path('C:/vietlott-research-output/physical-audit-20261022/documents')
URLS={
 'RULE2017':'https://media.vietlott.vn/vi/04.2019/system/archivedate/the-le-mega--655.pdf',
 'MAGNUM':'https://www.smartplay.com/lottery-products/lottery-draw-machines/magnum',
 'HALOGEN':'https://www.smartplay.com/lottery-products/lottery-draw-machines/halogen',
 'BALLCAT':'https://www.smartplay.com/lottery-products/lottery-drawing-balls',
 'VALIDATION_TOOLS':'https://www.smartplay.com/lottery-products/drawing-ball-validation-tools',
 'GOVLOT':'https://www.smartplay.com/lottery-solutions/government-lotteries',
 'VIETLOTT':'https://vietlott.vn/',
 'PROCUREMENT':'https://muasamcong.mof.gov.vn/',
 'OFFICIAL_CALENDAR':'https://vietlott.vn/vi/trung-thuong/linh-thuong/thoi-gian-linh-thuong-655',
 'OFFICIAL_VIDEO_PAGE':'https://vietlott.vn/vi/trung-thuong/video-quay-so-mo-thuong',
 'OFFICIAL_PROCESS_PAGE':'https://vietlott.vn/vi/trung-thuong/quay-so-mo-thuong/quy-trinh-qsmt',
 'OFFICIAL_VENUE_PAGE':'https://vietlott.vn/vi/trung-thuong/quay-so-mo-thuong/dia-diem-quay-so-mo-thuong',
 'CURRENT_LINKED_POWER_RULE':'https://media.vietlott.vn//main.vi/08.2022/cms/power655.pdf',
}
def main():
 LOCAL.mkdir(exist_ok=True)
 ledger=OUT/'extracted/http_recheck.json'
 rows=json.loads(ledger.read_text(encoding='utf-8')) if ledger.exists() else []
 for id,url in URLS.items():
  if any(x['evidence_id']==id for x in rows):continue
  row=dict(evidence_id=id,url=url,accessed_utc=datetime.now(timezone.utc).isoformat(),http_status=None,sha256='',local_file='',error='')
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Power655ResearchAudit/1.0'})
   with urllib.request.urlopen(req,timeout=25) as r:
    body=r.read();row.update(http_status=r.status,resolved_url=r.url,content_type=r.headers.get('Content-Type',''))
   p=LOCAL/(id+('.pdf' if body.startswith(b'%PDF') else '.html'));p.write_bytes(body)
   row.update(sha256=hashlib.sha256(body).hexdigest(),local_file=str(p),bytes=len(body))
  except urllib.error.HTTPError as e:row.update(http_status=e.code,error=str(e))
  except Exception as e:row['error']=type(e).__name__+': '+str(e)
  rows.append(row);print(id,row['http_status'],flush=True)
 ledger.write_text(json.dumps(rows,indent=2),encoding='utf-8')
if __name__=='__main__':main()
