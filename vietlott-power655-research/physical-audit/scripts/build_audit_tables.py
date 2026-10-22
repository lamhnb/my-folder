"""Build audit tables from frozen Git files and explicit reviewed observations.
No simulator execution, automatic identifier guessing or winning-number fitting.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv,hashlib,json,subprocess,collections,re
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parents[1];EX=OUT/'extracted'
P=ROOT/'vietlott-power655-physical-research';DT=P/'digital-twin'
BASE='01a56ea5f1f453960bf662ac64b0c129b1aa2006'
RULE='https://media.vietlott.vn/vi/04.2019/system/archivedate/the-le-mega--655.pdf'
NOW=datetime.now(timezone.utc).isoformat()
def readcsv(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
def dump(name,rows,fields=None):
 with (OUT/name).open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields or list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8','replace').strip()
def gh(commit,path):return f'https://github.com/lamhnb/my-folder/blob/{commit}/{path}'
E=[]
def ev(id,typ,url,loc,claim,scope,status='VERIFIED',confidence='high_for_stated_scope',digest='',method='direct file inspection',limitations=''):
 E.append(dict(evidence_id=id,source_type=typ,source_url=url,locator=loc,sha256=digest,accessed_utc=NOW,extraction_method=method,claim=claim,applicability=scope,status=status,confidence=confidence,limitations=limitations))
local_sources=[
 ('G01','extracted/refs.csv','Fetched ref/commit inventory and remote branch coverage'),
 ('G02','../../vietlott-power655-physical-research/FINAL_HANDOFF.md','Phase 1 delivered reconnaissance; explicitly incomplete physical measurements'),
 ('G03','../../vietlott-power655-physical-research/equipment_research.md','Historical equipment nominals and unresolved identities were already committed'),
 ('G04','../../vietlott-power655-physical-research/phase2/PHASE2_FINAL_HANDOFF.md','35 downstream proxies on five draws; NO-GO for calibrated dynamics'),
 ('G05','../../vietlott-power655-physical-research/phase3/PHASE3_HANDOFF.md','35 provisional labels; zero independently verified cohort; expansion not attempted'),
 ('G06','../../vietlott-power655-physical-research/phase4/PHASE4_EXECUTION_PLAN.md','22-line Phase 4 plan; specified output handoff absent from all fetched refs'),
 ('G07','../../vietlott-power655-physical-research/digital-twin/FINAL_DIGITAL_TWIN_HANDOFF.md','Runnable hypothetical simulator, numerical results and scientific limitations'),
 ('G08','../../vietlott-power655-physical-research/digital-twin/configs/baseline.json','Synthetic baseline controls'),
 ('G09','../../vietlott-power655-physical-research/digital-twin/simulator/core.py','Shared contact coefficients and seeded uniform ball-property perturbations; no per-number measured property import'),
 ('G10','../../vietlott-power655-physical-research/digital-twin/parameter_registry.csv','99 entries with explicit evidence classifications'),
 ('G11','../../vietlott-power655-physical-research/digital-twin/results/summary.json','Frozen 78-run aggregate; no new runs in this audit'),
 ('G12','../../vietlott-power655-physical-research/digital-twin/calibration/identifiability.json','Downstream cadence only; retrospective reserve and rank-deficient reduced observation equation'),
 ('G15','../../vietlott-power655-physical-research/phase2/phase2_sources.csv','Five source file SHA256/PTS/rendition pins; camera masters not authenticated'),
 ('G16','extracted/zip_members.csv','Three local ZIP archives; 362 members checked with CRC and hashes'),
]
for id,rel,claim in local_sources:
 p=(OUT/rel).resolve()
 if not p.exists():raise ValueError(p)
 relroot=p.relative_to(ROOT).as_posix()
 ev(id,'git_file' if not rel.startswith('extracted') else 'audit_extraction',gh(BASE,relroot) if not rel.startswith('extracted') else rel,rel,claim,'Prior research unless explicitly audit extraction',digest=sha(p))
for id,ref,path,claim in [
 ('G13','origin/research/power655-b1-physical-a','vietlott-power655-physical-research/digital-twin/experiments/b1_physical_a/PROTOCOL.md','Protocol only; rank-to-slot assignment explicitly assumed; no actual machine/ball measurements'),
 ('G14','origin/research/power655-b1-adaptive-momentum30','vietlott-power655-research/adaptive-momentum30/README.md','Frequency-momentum backtest report; no physical identification data')]:
 body=subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT)
 c=git('rev-parse',ref);(EX/(id+'_context.md')).write_bytes(body)
 ev(id,'other_branch_git_file',gh(c,path),path,claim,'Context only; preserved without checkout or modification',digest=hashlib.sha256(body).hexdigest(),method='git show at pinned remote commit')

http=json.loads((EX/'http_recheck.json').read_text(encoding='utf-8'))
httpmap={x['evidence_id']:x for x in http}
for id,key,claim,scope,loc,lim in [
 ('R01','RULE2017','2017 Power rule: geometry class, nominal ball specifications, selection/check/maintenance/recordkeeping requirements','Historical normative specification; no demonstrated 2026 version or asset linkage','Decision 478 dated 2017-05-26; pp.4-8; Articles 7-8','Requirement is not an executed inspection, measured ball value or maintenance event'),
 ('R02','MAGNUM','Manufacturer lists Vietnam Vietlott among Magnum users','Vendor/operator relationship only','Magnum product page deployment list','No Power product/draw/serial linkage; catalog values excluded from actual parameters'),
 ('R03','HALOGEN','Catalog comparison for a different candidate model','Manufacturer catalog only','Halogen product page','Visual resemblance excluded as identification'),
 ('R04','GOVLOT','Manufacturer describes Vietlott Mega 6/45 installation','Different game','Vietnam deployment section','Cannot infer Power equipment or ball provenance'),
 ('R05','BALLCAT','Closed-cell foam 40/50 mm matched sets and custom printing offered','Generic Smartplay ball catalog','Foam Lottery Balls / custom printing','Not measurements or verified supplier of actual Power balls; animated 0 counters ignored'),
 ('R06','VALIDATION_TOOLS','Vendor offers ball-weight reports and dimensional validation tools','Generic product capability','DBVS / Go-NoGo / Setra sections','No evidence Vietlott uses DBVS/RFID or this accuracy; marketing fairness claims not adopted'),
 ('R07','VIETLOTT','Current official website links YouTube channel UCucGZm2OZJxf3LpIpKGAQhA','Official footer as retrieved in audit','Footer YouTube href','Different from old source metadata channel IDs; does not prove old channels unofficial or authenticate old renditions'),
 ('R08','OFFICIAL_CALENDAR','Official calendar used for draw/date reconciliation','Only rows actually located by extraction','Power 655 claim-deadline calendar','Not machine or ball-set data'),
 ('R09','PROCUREMENT','Procurement portal opened through web tool; direct HTTP retrieval failed','Bounded public search only','Search UI / redirected mof.gov.vn','No authenticated tender attachment search or exhaustive procurement-history review completed'),
 ('R10','CURRENT_LINKED_POWER_RULE','Power operator rule explicitly names SMART PLAY MAGNUM II and numeric machine/ball specifications; 2023 base plus 2025 venue amendment','Product-level operator-documented nominal configuration; no per-draw serial or actual ball metrology','PDF pp.1-11 base Decision 125 dated 2023-03-03; pp.13,15 venue amendment effective 2025-01-22; Article 8 pp.7-9','16-page scanned PDF; all pages visually read after Poppler rendering. URL directory year 2022 is not enactment date. No claim of exhaustive amendment discovery or actual unit match'),
 ('R11','OFFICIAL_PROCESS_PAGE','Official process page links the newly recovered 16-page Power PDF','Source discovery and operator provenance','href for Power 6/55 to //main.vi/08.2022/cms/power655.pdf','This link/document was not found in the old source lists or Git string history'),
 ('R12','OFFICIAL_VIDEO_PAGE','14 operator-embedded YouTube links recovered; selected Power metadata attempt timed out','Operator link placement only','extracted/official_embeds.json','No new official-linked video pixels obtained; old five renditions remain ownership-unverified'),
]:
 h=httpmap[key]
 ev(id,'operator_document' if id in ['R01','R07','R08','R10','R11','R12'] else 'manufacturer_catalog' if id in ['R02','R03','R04','R05','R06'] else 'procurement_portal',h['url'],loc,claim,scope,status='VERIFIED' if h['http_status']==200 or id=='R09' else 'NOT_AUDITABLE',digest=h.get('sha256',''),method='urllib HTTP fetch; source bytes local; PDF pypdf text extraction' if id=='R01' else 'direct HTTP; Poppler 120 DPI native scan visual transcription' if id=='R10' else 'direct HTTP plus web/source inspection',limitations=lim)
sources=readcsv(P/'phase2/phase2_sources.csv')
for s in sources:
 ev('V'+s['draw_id'],'broadcast_rendition',s['source_url'],'Native PTS; format 137; source ledger G15','Public rendition SHA256 matched again in this audit','Associated draw/date; not camera master or authenticated official channel',digest=s['video_sha256'],method='fresh full file hash and native ffmpeg frame extraction',limitations='Identifies source bytes, not machine serial; channel ownership unverified for these five sources')
ev('V00027','broadcast_rendition','https://www.youtube.com/watch?v=GidYNrF55XY','PTS 0 slate per frozen Phase 1','2017-09-30 / 00027 slate recorded by prior Phase 1','Historical observation reused, not redecoded in this audit',confidence='medium_prior_pixel_record',method='G02 and sources.csv; source video not available locally',limitations='No full-source SHA; no new identity review')
for key,title,anchor in [('T1','Phase 1 original visible task','Sections 5,8,9'),('T2','Phase 2 user attachment','Phase 2A/2D/2F'),('T3','Phase 3 user attachment','Task B and H4'),('TDT','Digital Twin master task','Task A / B / E / I')]:
 ev(key,'visible_user_task','extracted/task_requirements.md',anchor,title,'Requirement evidence only; current audit instructions take precedence',method='Visible task read via app and user attachment; no hidden context retained',limitations='Exact requested scope distinguished from later stricter per-draw audit schema')

details=readcsv(EX/'case_frame_manifest.csv');overview=readcsv(EX/'identity_frame_manifest.csv')
def frame(draw,t):
 return next(x for x in details+overview if x['draw_id']==draw and abs(float(x['source_pts_seconds'])-t)<0.000001)
caseinfo=[
 ('01372','UNKNOWN',689.021667,690.022667,694.026667,'yellow','Label partly out of frame; no suffix guessed'),
 ('01373','VC2',692.024667,693.025667,697.029667,'yellow','Readable case inscription; no certified case-to-ball inventory'),
 ('01374','VC4',689.021667,690.022667,697.029667,'green','Readable case inscription; no certified case-to-ball inventory'),
 ('01375','VC2',680.012667,681.013667,683.015667,'yellow','Readable case inscription; no certified case-to-ball inventory'),
 ('01376','VC2',640.006033,641.007033,647.013033,'yellow','Readable case inscription; no certified case-to-ball inventory'),
]
visual=[];history=[]
history.append(dict(draw_id='00027',date='2017-09-30',machine_id='UNKNOWN',ball_set_id='UNKNOWN',operator_documented_model='UNKNOWN',model_applicability='2023 model document not applied retrospectively to 2017',observed_case_code='UNKNOWN',observed_ball_color='UNKNOWN',case_to_draw_link_status='NOT_FOUND',evidence_ids='V00027;G02',confidence='medium_for_date_only;none_for_asset_ID',notes='Historical slate from prior extraction; no fresh full-video review'))
for draw,code,t1,t2,ot,color,note in caseinfo:
 a,b,o=frame(draw,t1),frame(draw,t2),frame(draw,ot)
 id='F'+draw
 ev(id,'native_video_frame_pair',a['source_url'],f'case label PTS {t1:.6f},{t2:.6f}; open case PTS {ot:.6f}',f'POWER case observed; literal case code {code}; open-case ball appearance {color}','Preparation in associated broadcast; persistent official ball-set identity unknown',status='PARTIAL',confidence='medium_single_auditor_visual_transcription',digest=a['frame_sha256']+';'+b['frame_sha256'],method='Native full frames; contact sheet navigation; optional lossless crop and 180-degree display rotation',limitations=note+'; no independent second label reviewer; no physical properties inferred from color')
 visual.append(dict(draw_id=draw,case_code=code,label_pts_1=t1,label_pts_2=t2,open_case_pts=ot,label_frame_sha256_1=a['frame_sha256'],label_frame_sha256_2=b['frame_sha256'],open_frame_sha256=o['frame_sha256'],ball_color=color,status='PARTIAL',reviewer='codex_auditor_20261022',independent_second_review='NOT_EXECUTED',stage='preparation_case_unsealing_before_trial_and_official_segment',persistent_ballset_id='UNKNOWN',notes=note))
 src=next(s for s in sources if s['draw_id']==draw)
 history.append(dict(draw_id=draw,date=src['draw_date_associated'],machine_id='UNKNOWN',ball_set_id='UNKNOWN',operator_documented_model='MAGNUM II',model_applicability='Product-level rule 2023; actual per-draw unit/model allocation unverified',observed_case_code=code,observed_ball_color=color,case_to_draw_link_status='PARTIAL',evidence_ids=id+';V'+draw+';G15;R10',confidence='medium_case_reading;none_for_persistent_asset_ID',notes='Case is shown in preparation for broadcast; cut coverage and case-code semantics do not certify individual ball continuity or official serial'))
dump('MACHINE_BALLSET_HISTORY.csv',history)
dump('extracted/visual_review.csv',visual)
ev('FMULTI','native_video_frame','https://www.youtube.com/watch?v=Eid9PPhMn_0','PTS 860.292767; overview manifest','Two separate circular mixer units visible; foreground populated and rear apparently empty','This sampled broadcast image only',digest=frame('01374',860.292767)['frame_sha256'],method='Native visual inspection',limitations='No serial/nameplate read; not proof both used for same Power draw or count of entire fleet')
ev('SSEARCH','bounded_research_log','extracted/search_log.csv','Queries and primary-source outcomes','Recovered product-level model/specifications, but no serial-linked records, actual per-ball measurements or maintenance events','Available public indexed pages and fetched sources only',status='PARTIAL',confidence='high_for_logged_outcome_only',method='web search plus direct source inspection',limitations='Not exhaustive; no operator or supplier contacted; NOT_PUBLIC not established')
dump('EVIDENCE_REGISTER.csv',E)

numeric={'mesh_lat','mesh_lon','dt','solver_iterations','sample_seconds','penetration_limit','max_seconds','reverse_insertion','label_shift','mirror_y','initial_jitter','arm_segments','tube_panels','gate_pause_depth'}
reg=readcsv(DT/'parameter_registry.csv');cfg=json.loads((DT/'configs/baseline.json').read_text())
status=[];gaps=[]
def dependency(k):
 if k in numeric:return 'numerical_or_experiment_control','engine convergence/implementation; not a measured machine property','G08;G09;G10'
 if 'ball' in k or k in ['diameter_tolerance','mass_tolerance','center_of_mass_offsets','simulated_center_of_mass_offset','uniform_sphere_nominal_density']:
  return 'ball_set_and_individual_properties','collision clearance, inertia, persistent number-linked differences; needs per-ball serial and metrology','R01;R05;G09;G10'
 if any(x in k for x in ['friction','restitution','damping','stiffness']):return 'contact_law','collision losses, mixing, jamming; dedicated material tests needed','G09;G10;R05'
 if any(x in k for x in ['gate','mouth','pocket','hold','capture','trough','stop','tube','isolation','latency']):return 'collector_and_control','admission, isolation, release and time-to-ramp; needs measured gate geometry and trigger logs','G04;G09;G10'
 if any(x in k for x in ['RPM','rpm','rotor','rotation','axis','arm','paddle','ramp','mix','deceleration']):return 'mixer_geometry_and_drive','mixing state and load response; needs dimensioned model and measured motor trajectory','G04;G08;G09;G10'
 if any(x in k for x in ['initial','loading']):return 'initial_state_and_loading','number-to-position map and velocities; full loading path and repeatable loading records needed','R01;G09;G10'
 if any(x in k for x in ['temperature','humidity','vibration','electrostatic','gravity']):return 'environment','influence not quantified for this machine; local measurements needed before adding forces','G10'
 if any(x in k for x in ['frame','proxy','interval','camera','refraction']):return 'video_measurement','image observables do not uniquely identify hidden SI parameters','G04;G12'
 return 'machine_identity_and_geometry','asset lineage, scale and chamber/shaft geometry; serial-linked records needed','G03;G07;G10;R02'
for r in reg:
 k=r['parameter'];cl=r['classification'];group,impact,eids=dependency(k)
 if k in numeric:
  v=r['value_SI'];st='VERIFIED';basis='implementation_control';scope='Frozen implementation only; no corresponding measured hardware value';real='NOT_FOUND'
 elif cl=='documented':
  v=r['value_SI'];st='VERIFIED';basis='historical_documented_nominal';scope='2017 rule only; applicability to actual 2026 asset unverified';real='NOT_FOUND';eids+=';R01'
 elif cl=='measured':
  v=r['value_SI'];st='VERIFIED';basis='rendition_observation';scope=r['applicability'];real='NOT_FOUND'
 elif cl=='estimated':
  v=r['value_SI'];st='ESTIMATED';basis='derived_observable_or_nominal_equivalent';scope=r['applicability'];real='NOT_FOUND'
 else:
  v='UNKNOWN';st='NOT_FOUND';basis='synthetic_default' if cl=='assumed' else 'unknown_actual_parameter';scope='Actual Power hardware/property unavailable in audited evidence';real='NOT_FOUND'
 if k=='manufacturer_model':
  v='SMART PLAY / MAGNUM II';st='VERIFIED';basis='operator_documented_product_model';scope='2023 Power rule linked on official site in audit; not per-draw asset identity';eids+=';R10'
 if k in ['radius','actual_loading_order']:eids+=';R10'
 if cl=='documented':eids+=';R10'
 status.append(dict(parameter=k,value_SI=v,unit_SI=r['unit_SI'],uncertainty_or_range_SI=r['uncertainty_or_range_SI'],status=st,basis=basis,applicability=scope,actual_2026_asset_status=real,simulator_value_SI=r['value_SI'],simulator_original_classification=cl,simulator_config_value=str(cfg.get(k,'NOT_A_CONFIG_KEY')),evidence_ids=eids,notes=r['notes']+'; synthetic ranges are not measured tolerances or confidence intervals' if cl=='assumed' else r['notes']))
 recovered='R10 names model; serial/unit allocation still unknown' if k=='manufacturer_model' else 'R10 documents 0.61 m mixing chamber diameter; collision inner radius remains ambiguous' if k=='radius' else 'R10 confirms nominal size/mass/tolerances/counts' if k in ['ball_radius','ball_mass','documented_diameter','documented_diameter_tolerance','documented_mass_tolerance','ball_count','paddle_count'] else 'R10 supplies normative loading label sequence only' if k=='actual_loading_order' else 'No calibrated per-draw physical value recovered'
 gaps.append(dict(parameter=k,group=group,classification=cl,current_value=r['value_SI'],units=r['unit_SI'],missing_dependency=impact,recovered_information=recovered,evidence_ids=eids))
extra=[
 ('historical_ball_material','solid foam plastic','1','material category only','VERIFIED','R01','2017 Article 8.2a; actual manufacturer/polymer unknown'),
 ('historical_ball_marking_repetitions','12','1','normative count','VERIFIED','R01','Underlined numeral printed twelve times; ink thickness/mass/roughness unknown'),
 ('historical_machine_count_used','1','1','normative count','VERIFIED','R01','2017 rule; not a per-draw serial assignment'),
 ('historical_backup_machine_count','2','1','normative count','VERIFIED','R01','2017 requirement; actual fleet inventory unknown'),
 ('historical_backup_ball_cases_minimum','1','1','minimum additional case','VERIFIED','R01','2017 requirement; number of operational sets unknown'),
 ('historical_maintenance_interval','3 calendar months','1','calendar interval; not constant SI seconds','VERIFIED','R01','Requirement to maintain and keep witnessed log; actual dates unknown'),
 ('historical_loading_label_order','01 through 55','1','normative sequence only','VERIFIED','R01','Article 7.1g; not actual positions, velocities, timing or a 2026 observed full load'),
 ('actual_ball_sphericity','UNKNOWN','m','unknown','NOT_FOUND','R01;R05;SSEARCH','Nominal round shape is not measured sphericity'),
 ('actual_marking_mass_surface_effect','UNKNOWN','kg;1','unknown','NOT_FOUND','R01;R05;SSEARCH','No ink/mass/roughness/contact measurements'),
 ('actual_ball_inspection_records','UNKNOWN','1','unknown','NOT_FOUND','R01;SSEARCH','2017 requires pre-draw weight/size checks, but actual readings/certificates not recovered'),
 ('actual_ball_manufacturer_batch','UNKNOWN','1','unknown','NOT_FOUND','R05;SSEARCH','Generic vendor catalog is not traceability of Vietlott balls'),
 ('actual_ball_serial_continuity','UNKNOWN','1','unknown','NOT_FOUND','F01373;F01374;F01375;F01376','Case inscription repeats do not prove individual ball reuse'),
]
for k,v,u,unc,st,ids,n in extra:
 status.append(dict(parameter=k,value_SI=v,unit_SI=u,uncertainty_or_range_SI=unc,status=st,basis='historical_rule' if st=='VERIFIED' else 'unknown_actual_parameter',applicability='Historical rule only' if st=='VERIFIED' else 'Actual numbered Vietlott balls',actual_2026_asset_status='NOT_FOUND',simulator_value_SI='NOT_IMPLEMENTED_OR_NOT_IMPORTED',simulator_original_classification='not_in_original_registry',simulator_config_value='NOT_A_CONFIG_KEY',evidence_ids=ids,notes=n))
current_facts=readcsv(EX/'current_rule_facts.csv')
for r in current_facts:
 status.append(dict(parameter='operator_rule_2023.'+r['parameter'],value_SI=r['value_SI'],unit_SI=r['unit_SI'],uncertainty_or_range_SI='not quantified by source unless a tolerance field is given',status=r['status'],basis='operator_documented_nominal_or_procedure',applicability='2023 base rule and 2025 venue amendment, as linked by official site during audit',actual_2026_asset_status='NOT_FOUND',simulator_value_SI='NOT_IMPORTED_IN_THIS_AUDIT',simulator_original_classification='not_in_original_registry',simulator_config_value='NOT_A_CONFIG_KEY',evidence_ids='R10;R11',notes=r['notes']))
dump('PHYSICAL_DATA_STATUS.csv',status)
dump('extracted/parameter_dependency_map.csv',gaps)
balls=[]
for n in range(1,56):
 balls.append(dict(printed_number=f'{n:02d}',ball_set_id='UNKNOWN',physical_unit_id='UNKNOWN',actual_mass_kg='UNKNOWN',actual_diameter_m='UNKNOWN',actual_material='UNKNOWN',actual_sphericity_m='UNKNOWN',actual_restitution='UNKNOWN',actual_static_friction='UNKNOWN',actual_kinetic_friction='UNKNOWN',actual_surface_roughness_m='UNKNOWN',actual_center_of_mass_offset_m='UNKNOWN',measurement_date='UNKNOWN',inspection_certificate='UNKNOWN',status='NOT_FOUND',historical_nominal_mass_kg='0.01234',historical_mass_tolerance_kg='0.000617',historical_nominal_diameter_m='0.0505',historical_diameter_tolerance_m='0.001',evidence_ids='R01;R10;SSEARCH',notes='Number is a label, not a persistent physical unit. Nominals confirmed in 2023 rule; not measurements or assignments to the actual ball.'))
dump('extracted/individual_ball_specs.csv',balls)
dump('extracted/maintenance_events.csv',[],['event_date','draw_id','machine_id','ball_set_id','event_type','measured_value','evidence_ids','status'])

inputs=[]
for p in [P/'FINAL_HANDOFF.md',P/'equipment_research.md',P/'unknown_parameters.md',P/'sources.csv',P/'phase2/PHASE2_FINAL_HANDOFF.md',P/'phase2/phase2_sources.csv',P/'phase2/capture_event_audit.csv',P/'phase2/official_draw_events.csv',P/'phase3/PHASE3_HANDOFF.md',P/'phase3/draw_order_verified.csv',P/'phase3/PHASE3_RESEARCH_PROTOCOL.md',P/'phase4/PHASE4_EXECUTION_PLAN.md',DT/'FINAL_DIGITAL_TWIN_HANDOFF.md',DT/'parameter_registry.csv',DT/'configs/baseline.json',DT/'simulator/core.py',DT/'simulator/geometry.py',DT/'results/summary.json',DT/'calibration/identifiability.json']:
 inputs.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),bytes=p.stat().st_size,commit_sha=BASE))
dump('extracted/audit_input_hashes.csv',inputs)
(EX/'table_summary.json').write_text(json.dumps(dict(generated_utc=NOW,base_commit=BASE,evidence_rows=len(E),physical_status_rows=len(status),parameter_dependency_rows=len(gaps),history_rows=len(history),persistent_machine_ids_verified=0,persistent_ballset_ids_verified=0,case_code_readings=sum(x['case_code']!='UNKNOWN' for x in visual),individual_ball_measurement_rows=0,maintenance_events=0,original_registry_classifications=dict(collections.Counter(r['classification'] for r in reg))),indent=2),encoding='utf-8')
print((EX/'table_summary.json').read_text())
if __name__=='__main__':pass
