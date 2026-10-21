"""Build audit tables from persisted logs plus explicit manual review annotations.

Never invents event times. Unknown requested events remain NA. Annotation indices
refer to the contact-sheet sample sequence, whose PTS/hashes are read from logs.
"""
import datetime,json,platform,subprocess,sys
from pathlib import Path
import numpy as np
import cv2,scipy,matplotlib,yt_dlp,pypdf
from common import read_csv,write_csv,EVENTS,PADDLES,BALLS,digest
ROOT=Path(__file__).resolve().parents[1]
DRAW={
'IUU05082QtE':('01372','2026-07-16'), 'LUEP3hWibQw':('01373','2026-07-18'),
'Eid9PPhMn_0':('01374','2026-07-21'), 'is8GgE2gQu8':('01375','2026-07-23'),
'diq_elyRXjo':('01376','2026-07-25'),'oCXvnnydIbY':('01376','2026-07-25'),
'GidYNrF55XY':('00027','2017-09-30'),'tUoxKM647iE':('01374','2026-07-21')}
OFFICIAL={ 'IUU05082QtE':1060, 'LUEP3hWibQw':1040,'Eid9PPhMn_0':1050,'is8GgE2gQu8':1030,'diq_elyRXjo':990}
# Reviewed state observations, not inferred actuation times. Count NA when ambiguous.
ANNOTATIONS=[
('IUU05082QtE',1060,0,'loading_rack_handling_visible',None,'official_segment','medium'),
('IUU05082QtE',1060,6,'mixing_visible',None,'official_segment','high'),
('IUU05082QtE',1060,11,'display_channel_empty_visible',0,'official_segment','high'),
('IUU05082QtE',1060,12,'collector_ball_visible',1,'official_segment','high'),
('IUU05082QtE',1060,14,'collector_ball_visible',1,'official_segment','high'),
('IUU05082QtE',1060,19,'collector_balls_visible',3,'official_segment','high'),
('IUU05082QtE',1060,22,'collector_balls_visible',4,'official_segment','high'),
('IUU05082QtE',1060,24,'collector_balls_visible',5,'official_segment','high'),
('IUU05082QtE',1060,30,'seven_result_balls_visible',7,'official_segment','high'),
('LUEP3hWibQw',1040,2,'loading_rack_handling_visible',None,'official_segment','medium'),
('LUEP3hWibQw',1040,5,'green_control_button_hand_visible',None,'official_segment','high'),
('LUEP3hWibQw',1040,6,'mixing_visible_wide_view',None,'official_segment','medium'),
('LUEP3hWibQw',1040,9,'collector_ball_visible',1,'official_segment','high'),
('LUEP3hWibQw',1040,18,'seven_result_balls_visible',7,'official_segment','high'),
('Eid9PPhMn_0',1050,1,'loading_rack_handling_visible',None,'official_segment','high'),
('Eid9PPhMn_0',1050,7,'mixing_visible',None,'official_segment','high'),
('Eid9PPhMn_0',1050,12,'collector_ball_visible_overlay_not_yet_filled',1,'official_segment','high'),
('Eid9PPhMn_0',1050,30,'seven_result_balls_visible',7,'official_segment','high'),
('is8GgE2gQu8',1030,2,'loading_rack_handling_visible',None,'official_segment','high'),
('is8GgE2gQu8',1030,7,'green_control_button_hand_visible',None,'official_segment','high'),
('is8GgE2gQu8',1030,8,'mixing_visible',None,'official_segment','high'),
('is8GgE2gQu8',1030,15,'collector_ball_visible_overlay_not_yet_filled',1,'official_segment','high'),
('is8GgE2gQu8',1030,33,'seven_result_balls_visible',7,'official_segment','high'),
('diq_elyRXjo',990,3,'loading_rack_handling_visible',None,'official_segment','high'),
('diq_elyRXjo',990,7,'loading_motion_visible',None,'official_segment','high'),
('diq_elyRXjo',990,8,'mixing_visible',None,'official_segment','high'),
('diq_elyRXjo',990,13,'collector_ball_visible_overlay_not_yet_filled',1,'official_segment','high'),
('diq_elyRXjo',990,32,'seven_result_balls_visible',7,'official_segment','high'),
('IUU05082QtE',850,1,'rack_with_yellow_balls_visible',None,'operational_check_asr_indicated','high'),
('IUU05082QtE',850,2,'mixing_visible',None,'operational_check_asr_indicated','high'),
('IUU05082QtE',850,22,'seven_result_balls_visible',7,'operational_check_asr_indicated','high'),
('IUU05082QtE',877.3,20,'ball_downward_in_collector_box_visible',None,'operational_check_asr_indicated','medium'),
('IUU05082QtE',877.3,33,'ball_leaving_box_into_display_channel_visible',None,'operational_check_asr_indicated','high'),
('GidYNrF55XY',0,0,'slate_power655_draw00027_date20170930_visible',None,'opening_slate','high'),
('GidYNrF55XY',940,25,'collector_ball_visible',1,'historical_phase_unverified','high'),
('GidYNrF55XY',940,30,'seven_result_balls_visible',7,'historical_phase_unverified','medium')]

def load_clips():
    out=[]
    for f in sorted((ROOT/'evidence'/'clips').glob('*.json')):
        r=json.loads(f.read_text(encoding='utf-8'));r['_file']=f.relative_to(ROOT).as_posix();out.append(r)
    return out
def find_clip(clips,vid,start):
    candidates=[x for x in clips if x['video_id']==vid and abs(x['requested_start']-start)<1e-6 and x.get('frames_decoded',0)>0]
    return candidates[-1]
def main():
    clips=load_clips();frame_rows=[]
    for c in clips:
        if c.get('ffmpeg_exit_code')!=0:continue
        for i,s in enumerate(c['samples']):
            frame_rows.append({'source_id':c['video_id'],'format_id':c['source_format_id'],'source_pts_seconds':s['source_pts_seconds'],
                'clip_sample_index':i,'global_frame_index':None,'source_width':c['source_width'],'source_height':c['source_height'],
                'hash_kind':'preview_bgr_before_timestamp_overlay','sha256':s['preview_bgr_sha256'],'ledger':c['_file'],
                'source_url':f"https://www.youtube.com/watch?v={c['video_id']}&t={s['source_pts_seconds']:.6f}s"})
    app=read_csv(ROOT/'measurements'/'draw_01372_857_appearance.csv')
    for r in app:frame_rows.append({'source_id':r['source_id'],'format_id':'137','source_pts_seconds':float(r['timestamp_seconds']),
        'clip_sample_index':r['clip_frame_index'],'global_frame_index':None,'source_width':1920,'source_height':1080,
        'hash_kind':'native_crop_900x900_bgr_x510_y60','sha256':r['native_crop_bgr_sha256'],'ledger':'measurements/draw_01372_857_appearance.json',
        'source_url':f"https://www.youtube.com/watch?v={r['source_id']}&t={r['timestamp_seconds']}s"})
    write_csv(ROOT/'frames'/'frame_evidence_manifest.csv',list(frame_rows[0]),frame_rows)
    obs=[]
    for vid,start,i,kind,count,phase,conf in ANNOTATIONS:
        c=find_clip(clips,vid,start);s=c['samples'][i];draw=DRAW[vid][0]
        obs.append({'draw_id':draw,'source_id':vid,'event_type':'observed_'+kind,'timestamp_seconds':s['source_pts_seconds'],
            'frame_index':None,'confidence':conf,'evidence_frame':f"https://www.youtube.com/watch?v={vid}&t={s['source_pts_seconds']:.6f}s",
            'phase':phase,'collector_count_observed':count,'sha256_preview':s['preview_bgr_sha256'],'ledger':c['_file'],
            'notes':'reviewed=true; reviewer=Codex; state_snapshot_not_event_onset; no independent second review; global index unavailable'})
    write_csv(ROOT/'measurements'/'manual_observations.csv',list(obs[0]),obs)
    required=['power_segment_start','ball_loading_start','ball_loading_end','mixing_start','mixing_end','power_segment_end']
    required += [f'ball_{i}_{e}' for i in range(1,8) for e in ['capture_start','capture_end','selected']]
    for vid,(draw,date) in DRAW.items():
        if vid not in OFFICIAL and vid!='GidYNrF55XY':continue
        rows=[]
        for r in obs:
            if r['source_id']!=vid:continue
            row={k:r[k] for k in EVENTS}
            row['notes']+=f"; source_id={vid}; phase={r['phase']}; display_count={r['collector_count_observed']}"
            rows.append(row)
        for kind in required:rows.append({'draw_id':draw,'event_type':kind,'timestamp_seconds':None,'frame_index':None,'confidence':None,'evidence_frame':None,
            'notes':'not_measured; required_annotation_placeholder_not_observation; actual mechanical onset not validated frame-by-frame; see manual_observations.csv'})
        write_csv(ROOT/'measurements'/f'draw_{draw}_events.csv',EVENTS,rows)
        write_csv(ROOT/'measurements'/f'draw_{draw}_paddle_motion.csv',PADDLES,[])
        ballfile=ROOT/'measurements'/f'draw_{draw}_ball_tracking.csv'
        if not ballfile.exists():write_csv(ballfile,BALLS,[])
    sources=[];summary=[]
    for f in sorted((ROOT/'evidence'/'metadata').glob('*.json')):
        m=json.loads(f.read_text(encoding='utf-8'));vid=m['id'];draw,date=DRAW[vid]
        c=[c for c in clips if c['video_id']==vid and c.get('frames_decoded',0)>0];pt={s['source_pts_seconds'] for cl in c for s in cl['samples']}
        if vid=='IUU05082QtE':pt.update(float(r['timestamp_seconds']) for r in app)
        status='sampled_machine_footage' if vid in OFFICIAL or vid=='GidYNrF55XY' else ('sampled_graphics_only_excluded' if vid=='tUoxKM647iE' else 'sampled_machine_footage_duplicate_date_alignment_unverified')
        identity='visual_slate_verified' if vid in ('IUU05082QtE','GidYNrF55XY') else ('visual_final_summary_consistent_with_title_and_calendar' if vid in ('LUEP3hWibQw','is8GgE2gQu8') else 'title_calendar_consistent_not_full_visual_date_audit')
        source={'source_id':vid,'source_url':m['webpage_url'],'channel':m['channel'],'channel_id':m['channel_id'],'channel_official_verified':None,
            'title':m['title'],'upload_date':m['upload_date'],'release_date':m.get('release_date'),'draw_date_claimed':date,
            'draw_id_associated':draw,'draw_identity_status':identity,'duration_metadata_s':m['duration'],'max_width_metadata':m['width'],
            'max_height_metadata':m['height'],'fps_metadata':m['fps'],'video_sha256':None,'license_metadata':m['license'],
            'media_saved':False,'redistribution_permission':'not_established; media excluded by user choice','verification_status':status,
            'full_file_decoded':False,'all_capture_frames_manually_audited':False,'metadata_file':f.relative_to(ROOT).as_posix(),
            'notes':'Public YouTube rendition, not camera original. Official channel identity not proven by name. Date mapping source: Vietlott claim-deadline calendar; phase ASR is navigation only.'}
        if vid=='tUoxKM647iE':source['notes']+=' Title date 21 July, upload 22 July; inspected at 900/1200/1500/1800 s: graphics, not machine.'
        sources.append(source)
        official=find_clip(clips,vid,OFFICIAL[vid]) if vid in OFFICIAL else None
        frame_rate=150/(official['samples'][1]['source_pts_seconds']-official['samples'][0]['source_pts_seconds']) if official and official['sampling_every_native_frames']==150 else (300/(official['samples'][1]['source_pts_seconds']-official['samples'][0]['source_pts_seconds']) if official else None)
        summary.append({'draw_id_associated':draw,'source_id':vid,'draw_date_claimed':date,'native_pts_samples_unique':len(pt),
            'official_sampled_start_pts_s':official['samples'][0]['source_pts_seconds'] if official else None,
            'official_sampled_end_pts_s':official['samples'][-1]['source_pts_seconds'] if official else None,
            'sample_gap_seconds':(official['samples'][1]['source_pts_seconds']-official['samples'][0]['source_pts_seconds']) if official else None,
            'observed_rendition_sample_rate_hz':frame_rate,'fps_camera_original':None,'rpm_physical':None,'mixing_duration_seconds':None,
            'capture_period_seconds':None,'physical_direction':None,'paddle_phase_at_capture':None,'identity_validated_ball_tracks':0,
            'unlinked_color_candidates':109 if vid=='IUU05082QtE' else None,'appearance_phase':'operational_check_asr_indicated' if vid=='IUU05082QtE' else None,
            'uncertainty_note':'PTS locators verified; event onset, RPM, physical identity and systematic error unknown; no 95% CI justified',
            'completeness':'load_mix_and_7_display_sampled_not_all_capture_frames_audited' if official else 'partial_or_excluded'})
    write_csv(ROOT/'sources.csv',list(sources[0]),sources);write_csv(ROOT/'measurements_summary.csv',list(summary[0]),summary)
    hypotheses=[{'hypothesis':f'H{i}','status':'not_testable','independent_draws_with_required_validated_measurements':0,'statistic':None,'p_value':None,'ci95':None,'reason':r} for i,r in enumerate([
        'no calibrated physical paddle phase at validated capture times','native event onset series incomplete; coarse snapshot times are not event times',
        'detector/visibility not validated; no collector vs chamber eligible sample','no persistent ball ID or controlled initial state','no verified machine/ball-set IDs with repeated measurements'],1)]
    write_csv(ROOT/'measurements'/'hypothesis_results.csv',list(hypotheses[0]),hypotheses)
    write_csv(ROOT/'measurements'/'phase_assignments.csv',['source_id','first_pts','last_pts','phase','evidence','status'],[
        {'source_id':'IUU05082QtE','first_pts':857.022833,'last_pts':860.993467,'phase':'operational_check_indicated',
         'evidence':'ASR pretest landmarks 847.28 and 861.60; official draw follows after 1078; different visible result at 960 vs 1210',
         'status':'provisional_asr_plus_context; not manually listened or independently reviewed'}])
    (ROOT/'measurements'/'draw_01372_ball_tracking.method.json').write_text(json.dumps({
        'source_id':'IUU05082QtE','source_format_id':'137','source_pts_first':857.022833,'source_pts_last':860.993467,
        'phase':'operational_check_indicated_by_ASR_and_context; not official outcome data',
        'method':'unlinked HSV connected-component candidates; not persistent physical-ball tracks',
        'candidate_rows':109,'physical_identity_validated':False,'occlusion_known':False,'positions_imputed':False,
        'pixel_error_or_detection_accuracy':'unknown; no independently labelled validation set',
        'classification_ref':'measurements/phase_assignments.csv'},indent=2),encoding='utf-8')
    env={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),
        'packages':{'opencv-python-headless':cv2.__version__,'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__,'yt-dlp':yt_dlp.version.__version__,'pypdf':pypdf.__version__},
        'ffmpeg':subprocess.run(['ffmpeg','-version'],capture_output=True,text=True).stdout.splitlines()[0],
        'source_original_camera_fps_known':False,'media_included':False,'charts_visual_qa':'passed: three plots inspected; generated graphics only'}
    (ROOT/'evidence'/'environment.json').write_text(json.dumps(env,indent=2),encoding='utf-8')
    (ROOT/'evidence'/'coverage_counts.json').write_text(json.dumps({'metadata_urls':len(sources),'machine_footage_urls':7,'graphics_only_candidate_urls':1,
        'distinct_2026_dates_sampled_load_mix_7_display':5,'historical_dates_sampled':1,'full_files_decoded':0,
        'frame_ledger_rows_including_duplicate_samples_and_transforms':len(frame_rows),'manual_observations':len(obs),
        'physical_rpm_validated_draws':0,'all_captures_frame_audited_draws':0},indent=2),encoding='utf-8')
    print(json.dumps({'sources':len(sources),'frame_ledger_rows':len(frame_rows),'observations':len(obs)}))
if __name__=='__main__':main()
