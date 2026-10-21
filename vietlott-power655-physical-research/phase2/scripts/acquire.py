"""Bounded public-source acquisition; never log expiring media URLs.

Input clips are external to Git. Copy native video packets and preserve PTS.
Acquisition is not a statement that every mechanical event is visible.
"""
import argparse, datetime, hashlib, json, re, subprocess, sys, urllib.request, socket
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'scripts'))
from inspect_stream import metadata, stream_url
from media_bridge import Bridge

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('video_id'); ap.add_argument('--start',type=float,required=True)
    ap.add_argument('--duration',type=float,required=True); ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--audio-captions',action='store_true');ap.add_argument('--run-id',default='v2'); args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    prefix=f'{args.video_id}_{args.start:g}_{args.duration:g}_{args.run_id}'
    logpath=ROOT/'evidence'/f'acquire_{prefix}.json'; logpath.parent.mkdir(exist_ok=True)
    if logpath.exists(): raise SystemExit('Refuse overwriting acquisition log')
    # This host returns IPv6 first although its IPv6 transport stalls. Use IPv4,
    # with exactly the same public URL and no auth/cookies.
    original_getaddrinfo=socket.getaddrinfo
    socket.getaddrinfo=lambda host,port,family=0,type=0,proto=0,flags=0:original_getaddrinfo(host,port,socket.AF_INET,type,proto,flags)
    log={'video_id':args.video_id,'source_url':f'https://www.youtube.com/watch?v={args.video_id}',
         'requested_start':args.start,'requested_duration':args.duration,
         'accessed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'ffmpeg_version':subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],
         'code_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
         'code_sha256':sha(__file__),'transport_address_family':'IPv4','status':'started','video_file_sha256':None}
    try:
        info,clean=metadata(args.video_id); log['metadata']=clean; f=stream_url(info)
        log['selected_format']={k:f.get(k) for k in ['format_id','width','height','fps','vcodec','filesize','filesize_approx']}
        target=args.out/(prefix+'.mp4')
        if target.exists():raise ValueError('Refuse overwriting source clip')
        with Bridge(f['url']) as bridge:
            cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','warning','-rw_timeout','20000000',
                 '-ss',str(args.start),'-copyts','-i',bridge.url,'-to',str(args.start+args.duration),'-map','0:v:0',
                 '-an','-c:v','copy','-avoid_negative_ts','disabled','-y',str(target)]
            result=subprocess.run(cmd,capture_output=True,timeout=180)
            log['ffmpeg_returncode']=result.returncode
            log['stderr_sanitized']=re.sub(r'https?://\S+','[URL]',result.stderr.decode(errors='replace'))[-2000:]
            log['transport']={'bytes_sent':bridge.bytes_sent,'errors':bridge.errors}
        if result.returncode:raise RuntimeError('Video copy failed')
        log['video_file']=str(target); log['video_file_sha256']=sha(target)
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(target)]))
        log['probe']=probe
        pts=subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','csv=p=0',str(target)],text=True)
        values=[float(x.split(',')[0]) for x in pts.splitlines() if x and x.split(',')[0].replace('.','',1).isdigit()]
        log['decoded_frame_count']=len(values);log['pts_first']=values[0] if values else None;log['pts_last']=values[-1] if values else None
        log['pts_preserved']=bool(values and abs(values[0]-args.start)<5 and values[-1]>=args.start+args.duration-2)
        if not log['pts_preserved']:raise ValueError('PTS preservation/coverage check failed')
        if args.audio_captions:
            audio=[a for a in info['formats'] if a.get('vcodec')=='none' and a.get('acodec')!='none' and a.get('protocol')=='https' and not a.get('has_drm')]
            if audio:
                af=sorted(audio,key=lambda a:a.get('abr') or 0)[-1]; at=args.out/(prefix+'_audio.mka')
                with Bridge(af['url']) as b:
                    ar=subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-ss',str(args.start),'-copyts','-i',b.url,'-to',str(args.start+args.duration),'-vn','-c:a','copy',str(at)],capture_output=True,timeout=90)
                log['audio']={'format_id':af['format_id'],'returncode':ar.returncode,'file':str(at),'sha256':sha(at) if at.exists() else None,'listened_by_reviewer':False}
            options=info.get('automatic_captions',{}).get('vi-orig',[]) or info.get('automatic_captions',{}).get('vi',[])
            captions=[c for c in options if c.get('ext')=='json3']
            log['captions']={'manual_languages':list(info.get('subtitles',{})),'automatic_languages':list(info.get('automatic_captions',{})),'status':'unavailable'}
            if captions:
                try:
                    req=urllib.request.Request(captions[0]['url'],headers={'User-Agent':'Mozilla/5.0'})
                    with urllib.request.urlopen(req,timeout=25) as r: raw=r.read()
                    cap=args.out/(args.video_id+'_captions.json'); cap.write_bytes(raw)
                    log['captions'].update(status='retrieved_ASR_navigation_only',file=str(cap),sha256=sha(cap))
                except Exception as e:log['captions'].update(status='fetch_failed',error_type=type(e).__name__)
        log['status']='acquired'
    except Exception as e:
        log['status']='failed';log['error_type']=type(e).__name__;log['error']=re.sub(r'https?://\S+','[URL]',str(e))[:500]
    logpath.write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in log.items() if k not in ['metadata','probe']},ensure_ascii=True))
    return 0 if log['status']=='acquired' else 1
if __name__=='__main__':raise SystemExit(main())
