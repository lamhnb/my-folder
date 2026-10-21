"""Validate delivered integrity separately from unidentifiable physical quantities."""
import csv,datetime,hashlib,json,subprocess,sys
from pathlib import Path
from build_results import ROOT,SOURCES,CORE
def rows(path):
    with Path(path).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def main():
    reportpath=ROOT/'validation_report.json'
    if reportpath.exists():raise SystemExit('Refuse overwriting validation; archive/new output needed')
    problems=[];tests=[]
    project=ROOT.parent
    suites=[('Phase1 regressions',[sys.executable,'-m','unittest','discover','-s','scripts','-p','test_pipeline.py','-v'],8),
            ('Phase2 motion synthetic',[sys.executable,'-m','unittest','discover','-s','phase2/scripts','-p','test_motion_diagnostics.py','-v'],8),
            ('Phase2 interval and unknown contracts',[sys.executable,'-m','unittest','discover','-s','phase2/scripts','-p','test_phase2_results.py','-v'],7),
            ('Legacy RPM synthetic and scalar reproduction',[sys.executable,'phase2/scripts/rpm_audit.py','--validate-only'],7)]
    for name,cmd,count in suites:
        r=subprocess.run(cmd,cwd=project,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
        tests.append({'name':name,'command':cmd,'returncode':r.returncode,'expected_test_count':count,'stdout':r.stdout,'stderr':r.stderr,'status':'passed' if r.returncode==0 else 'failed'})
        if r.returncode:problems.append(name+' failed')
    ev=rows(ROOT/'official_draw_events.csv');caps=rows(ROOT/'capture_event_audit.csv');sources=rows(ROOT/'phase2_sources.csv')
    if len(caps)!=35 or len(sources)!=5:problems.append('Study cardinality differs from5draws/35attempts')
    for e in ev:
        if any(v in (None,'') for v in e.values()):problems.append('Blank field; NA required: '+str(e))
        if e['timestamp_seconds']!='NA' or e['physical_accuracy_frames']!='NA':problems.append('Uncertified point/accuracy claim')
        lo,hi=e['lower_pts_seconds'],e['upper_pts_seconds']
        if lo!='NA' and hi!='NA' and float(lo)>float(hi):problems.append('Reversed interval')
        if e['event_type']=='permanent_isolation' and (lo!='NA' or hi!='NA'):problems.append('Uncertified isolation')
        for key,hkey in [('evidence_before','before_sha256'),('evidence_after','after_sha256')]:
            if e[key]!='NA' and (not (ROOT/e[key]).is_file() or sha(ROOT/e[key])!=e[hkey]):problems.append('Evidence hash mismatch: '+e[key])
    for draw in SOURCES:
        for i in range(1,8):
            actual=[e['event_type'] for e in ev if e['draw_id']==draw and e['capture_index']==str(i)]
            if any(actual.count(k)!=1 for k in CORE):problems.append(f'Missing/duplicate core event{draw}/{i}')
    ramp=[e for e in ev if e['event_type']=='trough_entry_visible_proxy']
    if len(ramp)!=35 or any(e['lower_pts_seconds']=='NA' or e['upper_pts_seconds']=='NA' for e in ramp):problems.append('Missing downstream proxy bounds')
    if any(float(e['upper_pts_seconds'])-float(e['lower_pts_seconds'])>.200201 for e in ramp):problems.append('Ramp localization target not met')
    checked_sources=[]
    for s in sources:
        path=Path(s['input_file_local_only']);actual=sha(path) if path.is_file() else None
        checked_sources.append({'source_id':s['source_id'],'sha256':actual,'expected_sha256':s['video_sha256'],'status':'passed' if actual==s['video_sha256'] else 'failed'})
        if actual!=s['video_sha256']:problems.append('Input hash mismatch: '+s['source_id'])
    paddles=rows(ROOT/'paddle_motion.csv')
    if len(paddles)!=5 or any(r[k]!='NA' for r in paddles for k in ['physical_angle_deg','physical_rpm','empirical_angle_error_deg']):problems.append('Physical paddle quantities improperly filled')
    gitdiff=subprocess.check_output(['git','diff','--name-only','b2b1938cf38cc976a302cd8fd6a29bd4dd3c3df5'],cwd=project,text=True).splitlines()
    outside=[p for p in gitdiff if not p.startswith('vietlott-power655-physical-research/phase2/')]
    if outside:problems.append('Tracked Phase1/protected files changed: '+str(outside))
    frame_manifest=rows(ROOT/'evidence'/'event_frame_manifest.csv')
    frame_pts={r['file']:float(r['source_pts_seconds']) for r in frame_manifest}
    for e in ev:
        for endpoint,bound in [('evidence_before','lower_pts_seconds'),('evidence_after','upper_pts_seconds')]:
            if e[endpoint]!='NA' and e[bound]!='NA' and abs(float(e[bound])-frame_pts[e[endpoint]])>1e-6:
                problems.append('Bound does not match native PTS locator: '+e['draw_id']+'/'+e['event_type'])
    result={'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'integrity_status':'passed' if not problems else 'failed',
            'study_status':'completed_with_explicit_observability_limits','decision':'NO-GO_calibratable_3D',
            'scientific_validation':'No physical angle/RPM/permanent-isolation timing or calibrated physical accuracy established. Software pass is not real-world calibration.',
            'counts':{'source_renditions':len(sources),'draw_clusters':5,'capture_attempts':len(caps),'event_and_context_rows':len(ev),'downstream_visibility_bounds':len(ramp),
                      'retained_event_endpoint_aliases':len(frame_manifest),'physical_RPM_measurements':0,'physical_angle_measurements':0,'certified_isolation_times':0,'software_tests_expected':30},
            'source_hash_checks':checked_sources,'software_tests':tests,'tracked_outside_phase2_changes':outside,
            'untracked_root_note':'Managed MEMORY_AGENT_STATE.md excluded from commit. Original video/audio inputs and redundant preview PNGs stay local.',
            'protocol_sha256':sha(ROOT/'locked_protocol.json'),'code_base_commit':'b2b1938cf38cc976a302cd8fd6a29bd4dd3c3df5',
            'code_state_note':'Phase2 scripts were additions in working tree at validation; exact per-script hashes and final Git commit identify implementation.',
            'script_sha256':{str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in sorted((ROOT/'scripts').glob('*.py'))},'problems':problems}
    reportpath.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'integrity_status':result['integrity_status'],'counts':result['counts'],'problems':problems}));return int(bool(problems))
if __name__=='__main__':raise SystemExit(main())
