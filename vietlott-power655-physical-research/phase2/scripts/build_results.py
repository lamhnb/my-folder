"""Build Phase2 derived tables from immutable visual reviews; never fill events.

Derived tables may be refreshed explicitly; raw reviews/source observations are
never modified. NA point timestamps are intentional for interval-censored events.
"""
import argparse,csv,datetime,hashlib,json,math,shutil,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCES={'01372':'IUU05082QtE','01373':'LUEP3hWibQw','01374':'Eid9PPhMn_0','01375':'is8GgE2gQu8','01376':'diq_elyRXjo'}
DATES={'01372':'2026-07-16','01373':'2026-07-18','01374':'2026-07-21','01375':'2026-07-23','01376':'2026-07-25'}
CORE=['control_onset','mechanism_first_visible_motion','collector_ball_first_visible','permanent_isolation','trough_entry_visible_proxy','overlay_number_first_clearly_readable']
ALIASES={'control_command_onset':'control_onset','ball_first_visible_in_upper_collector':'collector_ball_first_visible',
 'first_visible_ball_in_collector':'collector_ball_first_visible','permanent_ball_isolation':'permanent_isolation',
 'leading_edge_exit_onto_downstream_ramp_proxy':'trough_entry_visible_proxy'}

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def write_csv(path,fields,rows,refresh=False):
    if path.exists() and not refresh:raise ValueError(f'Refuse overwrite: {path}')
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for row in rows:w.writerow({k:'NA' if row.get(k) is None else row[k] for k in fields})

def interval_difference(later,earlier):
    """All possible later-earlier differences; no midpoint precision invented."""
    a,b=later;c,d=earlier
    if any(not math.isfinite(x) for x in (a,b,c,d)) or a>b or c>d:raise ValueError('Invalid interval')
    return a-d,b-c

def normalize_event(e):
    name=e.get('event_type',e.get('event'))
    name=ALIASES.get(name,name)
    if name is None:raise ValueError('Event type missing')
    lo=e.get('lower_pts_seconds');hi=e.get('upper_pts_seconds')
    if lo is not None and hi is not None and lo>hi:raise ValueError('Reversed event bounds')
    if e.get('event_timestamp_seconds') is not None:raise ValueError('Point event forbidden in interval-only review')
    # Neither graphics nor a separate-position proxy may become isolation time.
    if name=='permanent_isolation' and (lo is not None or hi is not None):raise ValueError('No certified irreversible gate plane in this study')
    return dict(e,event_type=name,lower_pts_seconds=lo,upper_pts_seconds=hi)

def captures_from_review(data):
    captures=data.get('captures',[])
    if len(captures)==7 and all('events' in c for c in captures):return captures
    raise ValueError('Expected seven capture objects with events[]')

def build(refresh=False):
    required=[ROOT/'evidence'/f'source_{v}_ranges.json' for v in SOURCES.values()]
    required += [ROOT/'evidence'/('native_refinement.json' if d=='01372' else f'replication_{d}.json') for d in SOURCES]
    required += [ROOT/'evidence'/'pilot_boundary_review.json',ROOT/'evidence'/'pilot_independent_review.json']
    missing=[str(p) for p in required if not p.is_file()]
    if missing:raise ValueError('Required review/pin missing before build: '+', '.join(missing))
    source_rows=[];events=[];capture_rows=[];manifest=[];framefolder=ROOT/'evidence'/'event_frames';framefolder.mkdir(exist_ok=True)
    def evidence_copy(obj,draw,cap,name,side):
        if not obj or not obj.get('file'):return None,None
        source=ROOT/obj['file']
        if ROOT.resolve() not in source.resolve().parents:raise ValueError('Frame reference outside Phase2')
        if not source.is_file():raise ValueError(f'Missing reviewed frame: {source}')
        target=framefolder/f'draw{draw}_capture{cap:02d}_{name}_{side}{source.suffix}'
        if target.exists():
            if digest(target)!=digest(source):
                # Keep superseded evidence bytes; current derived table points to
                # an explicit content-versioned alias after a documented review correction.
                target=target.with_name(target.stem+'_'+digest(source)[:12]+target.suffix)
                if target.exists() and digest(target)!=digest(source):raise ValueError('Alias content conflict')
        if not target.exists():shutil.copyfile(source,target)
        origin=source.parent/'extraction.json';ex=read(origin) if origin.exists() else {}
        manifest.append({'file':str(target.relative_to(ROOT)).replace('\\','/'),'source_review_file':obj['file'],'sha256':digest(target),
                         'source_pts_seconds':obj.get('source_pts_seconds'),'native_pixels':ex.get('native_pixels'),
                         'crop_source_xywh':json.dumps(ex.get('arguments',{}).get('crop')),'output_dimensions':json.dumps(ex.get('output_dimensions'))})
        return str(target.relative_to(ROOT)).replace('\\','/'),digest(target)
    for draw,vid in SOURCES.items():
        pin=read(ROOT/'evidence'/f'source_{vid}_ranges.json');video=pin['video'];stream=video['probe']['streams'][0]
        source_rows.append({'draw_id':draw,'draw_date_associated':DATES[draw],'source_url':pin['url'],'source_id':vid,'format_id':video['format_id'],
            'rendition_width':stream['width'],'rendition_height':stream['height'],'rendition_fps':stream['avg_frame_rate'],'time_base':stream['time_base'],
            'video_sha256':video['sha256'],'input_bytes':video['bytes'],'input_file_local_only':video['file'],'accessed_utc':pin['accessed_utc'],
            'ffmpeg_version':pin['ffmpeg_version'],'acquisition_script_sha256':pin['script_sha256'],'code_base_commit':pin['code_base_commit'],
            'audio_sha256':pin.get('audio',{}).get('sha256'),'captions_sha256':pin.get('captions',{}).get('sha256'),
            'audio_review_status':'retrieved_not_listened' if 'audio' in pin else 'not_retrieved_phase2_replication',
            'full_video_downloaded':True,'full_video_decoded':False,'source_master_authenticated':False,'notes':'Public rendition, not camera master. See source pin JSON; recording date/serial not certified by upload metadata.'})
        path=ROOT/'evidence'/('native_refinement.json' if draw=='01372' else f'replication_{draw}.json')
        review=read(path);caps=captures_from_review(review)
        if draw=='01372':
            coarse=read(ROOT/'evidence'/'pilot_independent_review.json')
            for c,old in zip(caps,coarse['captures']):
                c['events'] += [e for e in old['events'] if 'overlay_' in e['event_type'] or e['event_type']=='spoken_announcement']
            # Supersede the right-censored special graphic with newly inspected 3-frame samples.
            def sf(t):return {'file':f'evidence/special_overlay_end/pts_{t:.6f}.png','source_pts_seconds':t}
            for e in caps[6]['events']:
                if e['event_type']=='overlay_number_first_clearly_readable':
                    e.update(lower_pts_seconds=1197.029167,upper_pts_seconds=1197.129267,before=sf(1197.029167),after=sf(1197.129267),status='observed_image_state_transition',note='Extended review: first legible special graphic during animation. Not capture time.')
                elif e['event_type']=='overlay_result_slot_first_filled':
                    e.update(lower_pts_seconds=1197.129267,upper_pts_seconds=1197.229367,before=sf(1197.129267),after=sf(1197.229367),status='observed_image_state_transition',note='Extended review: special graphic reaches slot. Separate from first legibility.')
        for c in caps:
            cap=int(c['capture_index']);seen={};wide={'draw_id':draw,'source_id':vid,'capture_index':cap,'capture_type':'special' if cap==7 else 'main'}
            for item in c['events']:
                e=normalize_event(item);name=e['event_type']
                if name in seen:raise ValueError(f'Duplicate capture event {draw}/{cap}/{name}')
                seen[name]=e
            for name in CORE:
                if name not in seen:seen[name]={'event_type':name,'lower_pts_seconds':None,'upper_pts_seconds':None,'status':'NA_not_established_in_review','note':'No qualified observation in the reviewed material; not a measured zero.'}
            for name,e in seen.items():
                lo,hi=e.get('lower_pts_seconds'),e.get('upper_pts_seconds');width=hi-lo if lo is not None and hi is not None else None
                before,bsha=evidence_copy(e.get('before'),draw,cap,name,'before');after,asha=evidence_copy(e.get('after'),draw,cap,name,'after')
                graphic=name.startswith('overlay_') or name=='spoken_announcement'
                events.append({'draw_id':draw,'source_id':vid,'capture_index':cap,'capture_type':'special' if cap==7 else 'main','event_type':name,
                    'data_class':'observation_graphic' if graphic else 'observation_visibility_only','timestamp_seconds':None,'lower_pts_seconds':lo,'upper_pts_seconds':hi,
                    'bracket_width_seconds':width,'encoded_frame_intervals':round(width*30000/1001,3) if width is not None else None,
                    'physical_accuracy_frames':None,'status':e.get('status'),'evidence_before':before,'evidence_after':after,'before_sha256':bsha,'after_sha256':asha,
                    'review_kind':'AI_visual_native_crop_plus_preview' if draw=='01372' else 'AI_visual_replication_review','human_review':False,
                    'definition_ref':'locked_protocol.json','raw_review_ref':str(path.relative_to(ROOT)).replace('\\','/'),'notes':e.get('note',e.get('notes','NA'))})
                if name in CORE:
                    for suffix,val in [('lower_pts',lo),('upper_pts',hi),('status',e.get('status'))]:wide[name+'_'+suffix]=val
            capture_rows.append(wide)
        if draw=='01372':
            for item in read(ROOT/'evidence'/'pilot_boundary_review.json')['events']:
                e=normalize_event(item);name=e['event_type'];lo,hi=e.get('lower_pts_seconds'),e.get('upper_pts_seconds')
                before,bsha=evidence_copy(e.get('before'),draw,0,name,'before');after,asha=evidence_copy(e.get('after'),draw,0,name,'after')
                events.append({'draw_id':draw,'source_id':vid,'capture_index':None,'capture_type':'boundary_or_context','event_type':name,'data_class':e['data_class'],
                    'timestamp_seconds':None,'lower_pts_seconds':lo,'upper_pts_seconds':hi,'bracket_width_seconds':None,'encoded_frame_intervals':None,'physical_accuracy_frames':None,
                    'status':e['status'],'evidence_before':before,'evidence_after':after,'before_sha256':bsha,'after_sha256':asha,'review_kind':'AI_visual_context_with_ASR_navigation_only',
                    'human_review':False,'definition_ref':'evidence/pilot_boundary_review.json','raw_review_ref':'evidence/pilot_boundary_review.json','notes':e['note']})
    fields=list(events[0]);write_csv(ROOT/'official_draw_events.csv',fields,events,refresh)
    write_csv(ROOT/'capture_event_audit.csv',list(capture_rows[0]),capture_rows,refresh)
    write_csv(ROOT/'phase2_sources.csv',list(source_rows[0]),source_rows,refresh)
    write_csv(ROOT/'evidence'/'event_frame_manifest.csv',list(manifest[0]),manifest,refresh)
    # A feasibility row is not a physical angle/RPM measurement.
    paddle=[{'draw_id':d,'source_id':v,'paddle_id':None,'physical_angle_deg':None,'physical_rpm':None,'physical_direction':None,'empirical_angle_error_deg':None,
             'status':'not_identifiable','reason':'No verified unique material marker, camera calibration or independent alias bound; see pilot_motion and replication camera quality gates.'} for d,v in SOURCES.items()]
    write_csv(ROOT/'paddle_motion.csv',list(paddle[0]),paddle,refresh)
    cadence=[];bydraw=[]
    for draw in SOURCES:
        g={int(e['capture_index']):e for e in events if e['draw_id']==draw and e['event_type']=='trough_entry_visible_proxy'}
        means=[]
        for i in range(2,8):
            a,b=g.get(i),g.get(i-1)
            if not a or not b or any(x is None for x in (a['lower_pts_seconds'],a['upper_pts_seconds'],b['lower_pts_seconds'],b['upper_pts_seconds'])):continue
            lo,hi=interval_difference((a['lower_pts_seconds'],a['upper_pts_seconds']),(b['lower_pts_seconds'],b['upper_pts_seconds']))
            cadence.append({'draw_id':draw,'interval_index':i-1,'from_capture':i-1,'to_capture':i,'interval_type':'main_to_special' if i==7 else 'main_to_main',
                            'duration_lower_seconds':lo,'duration_upper_seconds':hi,'midpoint_descriptive_seconds':(lo+hi)/2,'point_accuracy_seconds':None,
                            'data_class':'estimate_from_visibility_intervals','independent_unit':'draw','selection_timer_inferred':False})
            if i<=6:means.append((lo+hi)/2)
        if means:bydraw.append({'draw_id':draw,'main_intervals_available':len(means),'mean_main_visible_interval_midpoint_seconds':statistics.mean(means),
                               'min_main_visible_interval_midpoint_seconds':min(means),'max_main_visible_interval_midpoint_seconds':max(means)})
    write_csv(ROOT/'evidence'/'visible_cadence_intervals.csv',list(cadence[0]),cadence,refresh)
    write_csv(ROOT/'evidence'/'visible_cadence_by_draw.csv',list(bydraw[0]),bydraw,refresh)
    summary={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'independent_draws_with_descriptive_cadence':len(bydraw),'by_draw':bydraw,
             'mean_of_draw_means_seconds':statistics.mean(r['mean_main_visible_interval_midpoint_seconds'] for r in bydraw),
             'sample_sd_of_draw_means_seconds':statistics.stdev(r['mean_main_visible_interval_midpoint_seconds'] for r in bydraw) if len(bydraw)>1 else None,
             'p_value':None,'confidence_interval':None,'interval_bounds_are':'observation-localization bounds, not confidence intervals or physical accuracy',
             'H2_status':'visible_downstream_cadence_descriptive_only; physical mixing/capture timer not identified','locked_protocol_sha256':digest(ROOT/'locked_protocol.json')}
    (ROOT/'evidence'/'cadence_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    delays=[]
    for cap in range(1,8):
        g={e['event_type']:e for e in events if e['draw_id']=='01372' and e['capture_index']==cap}
        graphic=g['overlay_number_first_clearly_readable'];ramp=g['trough_entry_visible_proxy']
        lo,hi=interval_difference((graphic['lower_pts_seconds'],graphic['upper_pts_seconds']),(ramp['lower_pts_seconds'],ramp['upper_pts_seconds']))
        delays.append({'draw_id':'01372','capture_index':cap,'delay_lower_seconds':lo,'delay_upper_seconds':hi,'reference':'graphic legibility minus downstream ramp visibility; not physical selection latency','confidence_interval':None})
    write_csv(ROOT/'evidence'/'pilot_overlay_delays.csv',list(delays[0]),delays,refresh)
    return {'sources':len(source_rows),'capture_attempts':len(capture_rows),'event_rows':len(events),'retained_event_frame_aliases':len(manifest),'cadence_intervals':len(cadence)}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--refresh-derived',action='store_true');a=ap.parse_args();print(json.dumps(build(a.refresh_derived)))
