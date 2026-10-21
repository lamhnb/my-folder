"""Pin public non-DRM rendition bytes locally; media files remain outside Git."""
import argparse,datetime,hashlib,json,socket,subprocess,sys,time,urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'scripts'))
from inspect_stream import metadata,stream_url

def main():
    ap=argparse.ArgumentParser();ap.add_argument('video_id');ap.add_argument('--out',type=Path,required=True);ap.add_argument('--audio-captions',action='store_true');ap.add_argument('--ranges',action='store_true');a=ap.parse_args()
    old=socket.getaddrinfo;socket.getaddrinfo=lambda host,port,family=0,type=0,proto=0,flags=0:old(host,port,socket.AF_INET,type,proto,flags)
    suffix='_ranges' if a.ranges else ''
    logpath=ROOT/'evidence'/f'source_{a.video_id}{suffix}.json';logpath.parent.mkdir(exist_ok=True)
    if logpath.exists():raise SystemExit('Refuse overwrite')
    log={'video_id':a.video_id,'url':f'https://www.youtube.com/watch?v={a.video_id}','accessed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'network':'IPv4','status':'started','full_video_decoded':False}
    def fetch(fmt,target):
        if target.exists():raise ValueError('Refuse overwriting source')
        h=hashlib.sha256();n=0;started=time.monotonic()
        if a.ranges and fmt.get('filesize'):
            size=int(fmt['filesize']);chunk=4*1024*1024
            if size>1_000_000_000:raise ValueError('Source size bound exceeded')
            def get_range(start):
                end=min(start+chunk,size)-1
                req=urllib.request.Request(fmt['url'],headers={'User-Agent':'Mozilla/5.0','Range':f'bytes={start}-{end}'})
                with urllib.request.urlopen(req,timeout=25) as r:
                    raw=r.read(chunk+1)
                    if r.status!=206 or len(raw)!=end-start+1:raise ValueError('Incomplete or ignored byte range')
                    return raw
            with ThreadPoolExecutor(max_workers=8) as pool,target.open('wb') as out:
                # Limit outstanding work to a bounded 32 MB window.
                starts=list(range(0,size,chunk))
                for begin in range(0,len(starts),8):
                    for raw in pool.map(get_range,starts[begin:begin+8]):out.write(raw);h.update(raw);n+=len(raw)
                    if time.monotonic()-started>240:raise ValueError('Range acquisition time bound exceeded')
            return {'file':str(target),'format_id':fmt['format_id'],'sha256':h.hexdigest(),'bytes':n,'elapsed_seconds':time.monotonic()-started,'transport':'8 concurrent standard byte ranges of 4MiB','complete_content_length_verified':n==size}
        req=urllib.request.Request(fmt['url'],headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=20) as r,target.open('wb') as out:
            while block:=r.read(1024*1024):
                n+=len(block)
                if n>1_000_000_000 or time.monotonic()-started>150:raise ValueError('Acquisition bound exceeded')
                out.write(block);h.update(block)
        return {'file':str(target),'format_id':fmt['format_id'],'sha256':h.hexdigest(),'bytes':n,'elapsed_seconds':time.monotonic()-started}
    try:
        info,clean=metadata(a.video_id);log['metadata']=clean;a.out.mkdir(parents=True,exist_ok=True)
        fmt=stream_url(info);log['video']=fetch(fmt,a.out/(a.video_id+'_f'+fmt['format_id']+suffix+'.mp4'));print('video bytes pinned',flush=True)
        log['video']['probe']=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',log['video']['file']]))
        if a.audio_captions:
            fs=[f for f in info['formats'] if f.get('vcodec')=='none' and f.get('acodec') not in ('none',None) and f.get('protocol')=='https' and not f.get('has_drm')]
            if fs:
                af=sorted(fs,key=lambda f:f.get('abr') or 0)[-1];log['audio']=fetch(af,a.out/(a.video_id+'_f'+af['format_id']+suffix+'.'+af.get('ext','m4a')));log['audio']['listened_by_reviewer']=False
            opts=info.get('automatic_captions',{}).get('vi-orig',[]) or info.get('automatic_captions',{}).get('vi',[])
            log['captions']={'status':'not_available','manual_languages':list(info.get('subtitles',{})),'auto_languages':list(info.get('automatic_captions',{}))}
            fs=[f for f in opts if f.get('ext')=='json3']
            if fs:
                try:
                    req=urllib.request.Request(fs[0]['url'],headers={'User-Agent':'Mozilla/5.0'})
                    with urllib.request.urlopen(req,timeout=20) as r:raw=r.read()
                    target=a.out/(a.video_id+'_captions.json');target.write_bytes(raw)
                    log['captions'].update(status='retrieved_ASR_navigation_only',file=str(target),sha256=hashlib.sha256(raw).hexdigest())
                except Exception as e:log['captions'].update(status='failed',error_type=type(e).__name__)
        log['status']='acquired'
    except Exception as e:log['status']='failed';log['error_type']=type(e).__name__
    log['ffmpeg_version']=subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0]
    log['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    log['code_base_commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    logpath.write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in log.items() if k!='metadata'},ensure_ascii=True))
    return int(log['status']!='acquired')
if __name__=='__main__':raise SystemExit(main())
