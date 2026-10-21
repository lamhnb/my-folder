"""Collect sanitized metadata, no media copies, no auth cookies, no signed URLs."""
import argparse, datetime, hashlib, io, json, urllib.request
from pathlib import Path
from inspect_stream import metadata

ROOT=Path(__file__).resolve().parents[1]
IDS=['IUU05082QtE','diq_elyRXjo','GidYNrF55XY','oCXvnnydIbY','is8GgE2gQu8','LUEP3hWibQw','tUoxKM647iE']
RULES='https://media.vietlott.vn/vi/04.2019/system/archivedate/the-le-mega--655.pdf'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rules',action='store_true');args=ap.parse_args()
    out=ROOT/'evidence'/'metadata';out.mkdir(parents=True,exist_ok=True)
    logs=[]
    for vid in IDS:
        try:
            _,clean=metadata(vid)
            clean['collected_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
            (out/f'{vid}.json').write_text(json.dumps(clean,ensure_ascii=False,indent=2),encoding='utf-8')
            logs.append({'video_id':vid,'status':'metadata_only','license':clean['license']})
        except Exception as e:
            logs.append({'video_id':vid,'status':'failed','error_type':type(e).__name__})
    if args.rules:
        from pypdf import PdfReader
        result={'url':RULES,'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
        try:
            req=urllib.request.Request(RULES,headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req,timeout=25) as r:
                raw=r.read();result['http_status']=r.status
            result['sha256_remote_pdf']=hashlib.sha256(raw).hexdigest()
            pdf=PdfReader(io.BytesIO(raw));result['page_count']=len(pdf.pages)
            # Full extracted text is printed for researcher inspection, not persisted or packaged.
            for i,p in enumerate(pdf.pages):
                print(json.dumps({'page':i+1,'text':p.extract_text()},ensure_ascii=True))
        except Exception as e:result.update(status='failed',error_type=type(e).__name__,error=str(e))
        (ROOT/'evidence'/'rules_retrieval.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        logs.append(result)
    (ROOT/'evidence'/'collection_log.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(logs,ensure_ascii=True))

if __name__=='__main__':main()
