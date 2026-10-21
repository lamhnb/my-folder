"""Retrieve independent published unordered sets; HTTP failures never mean verification."""
import argparse
import concurrent.futures
import hashlib
import html
import json
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'evidence'/'result_sources'
EXPECTED_DATES={'01372':'16-07-2026','01373':'18-07-2026','01374':'21-07-2026','01375':'23-07-2026','01376':'25-07-2026'}

def parse_result(text,draw):
    match=re.search(r'Kỳ vé:.*?#'+re.escape(draw)+r'.*?(?=</ul>)',text,re.S)
    if not match:return [],''
    snippet=match.group(0)
    nums=re.findall(r'<div[^>]*class="[^"]*\bbool\b[^"]*"[^>]*>\s*(\d{1,2})\s*</div>',snippet)
    extract=' '.join(html.unescape(re.sub('<[^>]+>',' ',snippet)).split())
    return [int(n) for n in nums],extract

def fetch(item):
    draw,date=item
    out={'draw_id':draw,'retrieved_utc':datetime.now(timezone.utc).isoformat()}
    for kind,url in (
        ('official',f'https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/655?drawId={draw}'),
        ('secondary',f'https://www.minhngoc.net.vn/ket-qua-xo-so/dien-toan-vietlott/power-6x55/{date}.html')):
        record={'url':url,'request_purpose':'official_result_lookup_attempt' if kind=='official' else 'independent_published_unordered_result'}
        try:
            with urllib.request.urlopen(url,timeout=30) as response:
                raw=response.read();record['http_status']=response.status
            record['response_sha256']=hashlib.sha256(raw).hexdigest()
            text=raw.decode('utf-8',errors='replace')
            # Keep minimal published result extract plus whole response hash; omit site boilerplate.
            match=re.search(r'Kỳ vé:.*?#'+draw+r'.*?(?=</ul>)',text,re.S)
            if kind=='secondary' and match:
                snippet=match.group(0)
                nums,extract=parse_result(text,draw)
                record['published_numbers']=nums
                record['result_extract']=extract
                record['parser_status']='parsed_seven' if len(nums)==7 else 'needs_manual_inspection'
            else:
                record['parser_status']='not_verified'
            # Original HTTP response is local audit input; only bounded facts go in Git.
            local=Path('C:/vietlott-research-output/phase3-http');local.mkdir(exist_ok=True)
            (local/f'{draw}_{kind}.html').write_bytes(raw)
        except (urllib.error.URLError,TimeoutError) as exc:
            record['http_status']=getattr(exc,'code',None)
            record['error']=str(exc)
            record['parser_status']='unavailable'
        out[kind]=record
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--reparse-local',action='store_true');a=p.parse_args()
    if a.reparse_local:
        for draw in EXPECTED_DATES:
            path=EVIDENCE/f'draw{draw}.json';record=json.loads(path.read_text(encoding='utf-8'))
            raw=(Path('C:/vietlott-research-output/phase3-http')/f'{draw}_secondary.html').read_bytes()
            if hashlib.sha256(raw).hexdigest()!=record['secondary']['response_sha256']:raise RuntimeError('Cached HTTP hash mismatch')
            nums,extract=parse_result(raw.decode('utf-8'),draw)
            record['secondary']['parser_history']=['initial_li_text_only_parser_returned_zero_labels']
            record['secondary'].update(published_numbers=nums,result_extract=extract,parser_status='parsed_seven' if len(nums)==7 else 'needs_manual_inspection')
            path.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
            print(draw,nums)
        return
    EVIDENCE.mkdir(parents=True,exist_ok=False)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for record in pool.map(fetch,EXPECTED_DATES.items()):
            (EVIDENCE/f"draw{record['draw_id']}.json").write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
            print(record['draw_id'],record['official']['http_status'],record['secondary'].get('published_numbers'),record['secondary']['parser_status'])
if __name__=='__main__':main()
