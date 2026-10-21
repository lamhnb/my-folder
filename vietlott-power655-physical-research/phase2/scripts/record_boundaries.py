"""Record reviewed pilot context without fabricating hidden onset timestamps."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def sample(folder,target):
    with (ROOT/'evidence'/folder/'frames.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
    r=min(rows,key=lambda r:abs(float(r['source_pts_seconds'])-target))
    if abs(float(r['source_pts_seconds'])-target)>.035:raise ValueError('Requested context frame not in manifest')
    return {'file':r['file'],'source_pts_seconds':float(r['source_pts_seconds'])}

def main():
    out=ROOT/'evidence'/'pilot_boundary_review.json'
    if out.exists():raise SystemExit('Refuse overwrite')
    def e(name,lo,hi,status,before,after,note,kind='unknown'):
        return {'event_type':name,'event_timestamp_seconds':None,'lower_pts_seconds':lo,'upper_pts_seconds':hi,'status':status,'before':before,'after':after,'note':note,'data_class':kind}
    events=[
      e('pretest_end',None,None,'NA_exact_boundary_not_established',sample('pilot_overview',1018.050367),sample('pilot_overview',1020.052367),
        'ASR navigation at1013.36–1019.96 concerns equipment-check conclusion; speaker/phase change observed. Audio fetched but not directly listened. Neither speech ASR nor stage graphic certifies last physical check action.'),
      e('official_ball_set_selection',None,None,'NA_no_verified_set_selection_or_ID',None,sample('setup_overview',1045.0442),
        'Visible manual ball/rack rearrangement does not identify selection among sets or ball-set serial. No exact set-choice event is established.'),
      e('official_rack_loading_start',None,1045.044,'left_censored_preparation_already_underway',None,sample('setup_overview',1045.044),
        'First close-up already shows a gloved operator at rack. Start of manual preparation and first ball insertion are not continuously resolved. Upper bound concerns activity already underway, not identity/certification of55balls.'),
      e('rack_preparation_observed_span',1045.044,1061.8608,'observation_coverage_not_duration',sample('setup_overview',1045.044),sample('setup_overview',1061.8608),
        'Manual rack rearrangement/loading motions are visible during this span. Coverage endpoints are snapshots, not certified start/end of complete official-set loading.','observation_context'),
      e('official_rack_loading_end',None,None,'NA_last_ball_and_full_set_not_verified',sample('setup_overview',1061.6606),sample('setup_overview',1062.061),
        'Operator lowers hand and camera returns wide. Completeness/identity of55balls and final physical insertion frame are not certified.'),
      e('official_mixing_onset',None,1088.120367,'left_censored_running_seen_after_cut',sample('mixing_before_native',1085.117367),sample('mixing_after_native',1088.120367),
        'Control shot and changed camera framing obscure onset. Native1088.087000/1088.120367 show moving blade/ball departure. The wide before frame is context, not proof motor remained off until its PTS. Do not subtract this upper bound to report exact mixing duration.'),
      e('official_ball_release_from_rack_onset',None,1088.087,'left_censored_release_already_underway',sample('mixing_before_native',1085.084),sample('mixing_after_native',1088.087),
        'First close-up after control shot already shows rack balls dropping/partly departed. No exact first-release frame is asserted.'),
      e('rotor_stop_onset',None,1206.238367,'left_censored_stationary_state_after_cut',sample('pilot_overview',1198.230367),sample('pilot_overview',1206.238367),
        'Rail shot hides rotor. Following repeated stage samples1200.232367–1206.238367 show same clear blade orientation and settled balls. This bounds an observed stopped state only; stop command and deceleration are not measured.'),
      e('official_draw_end',None,None,'NA_semantic_end_not_physically_timed',sample('pilot_overview',1232.264367),sample('pilot_overview',1234.266367),
        'Power result summary transitions toward another product in stage graphics. Final spoken declaration/audio timing and official procedural end are not independently verified. Last result display is not a motor/gate event.'),
    ]
    out.write_text(json.dumps({'draw_id':'01372','manual_AI_visual_review':True,'human_review':False,'audio_status':'retrieved_not_directly_listened','ASR':'navigation_only_not_physical_oracle','events':events},indent=2),encoding='utf-8')
    print(json.dumps({'recorded_boundary_or_context_rows':len(events),'certified_exact_boundary_times':0}))
if __name__=='__main__':main()
