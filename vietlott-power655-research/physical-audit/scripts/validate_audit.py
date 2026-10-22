"""Validate the audit evidence package; never writes to prior research.
Portable schema/claim checks always run. Local media checks run when available.
"""
from pathlib import Path
from datetime import datetime,timezone
import csv,hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parents[1];EX=OUT/'extracted'
BASE='01a56ea5f1f453960bf662ac64b0c129b1aa2006'
PREFIX='vietlott-power655-research/physical-audit/'
P=ROOT/'vietlott-power655-physical-research';DT=P/'digital-twin'
checks={};errors=[];skipped=[]
def check(name,condition,detail=''):
 checks[name]=bool(condition)
 if not condition:errors.append(dict(check=name,detail=detail))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:
  r=csv.DictReader(f);rows=list(r)
  check('csv_rectangular:'+p.relative_to(OUT).as_posix(),None not in (r.fieldnames or []) and all(None not in x and all(v is not None for v in x.values()) for x in rows))
  return rows,r.fieldnames
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8','replace').strip()
def main():
 required=['AUDIT_REPORT.md','ARTIFACT_INVENTORY.csv','PHYSICAL_DATA_STATUS.csv','MACHINE_BALLSET_HISTORY.csv','EVIDENCE_REGISTER.csv','SIMULATOR_PARAMETER_GAPS.md','RECOVERY_PLAN.md']
 check('all_requested_deliverables_present',all((OUT/f).is_file() and (OUT/f).stat().st_size>0 for f in required))
 tables={}
 for p in OUT.rglob('*.csv'):
  tables[p.relative_to(OUT).as_posix()]=read(p)
 schemas={
 'ARTIFACT_INVENTORY.csv':{'artifact','location','commit_sha','purpose','status'},
 'PHYSICAL_DATA_STATUS.csv':{'parameter','value_SI','unit_SI','status','basis','applicability','actual_2026_asset_status','evidence_ids','simulator_original_classification'},
 'MACHINE_BALLSET_HISTORY.csv':{'draw_id','date','machine_id','ball_set_id','operator_documented_model','model_applicability','observed_case_code','evidence_ids','confidence'},
 'EVIDENCE_REGISTER.csv':{'evidence_id','source_url','locator','sha256','extraction_method','claim','applicability','status','confidence','limitations'},
 }
 for name,cols in schemas.items():check('required_schema:'+name,cols.issubset(tables[name][1]))
 E=tables['EVIDENCE_REGISTER.csv'][0];ids={r['evidence_id'] for r in E}
 check('unique_evidence_ids',len(ids)==len(E))
 statuses={'VERIFIED','PARTIAL','ESTIMATED','NOT_PUBLIC','NOT_FOUND','NOT_EXECUTED','NOT_AUDITABLE'}
 phys=tables['PHYSICAL_DATA_STATUS.csv'][0];hist=tables['MACHINE_BALLSET_HISTORY.csv'][0];vis=tables['extracted/visual_review.csv'][0];balls=tables['extracted/individual_ball_specs.csv'][0]
 check('status_vocabulary',all(r['status'] in statuses for r in E+phys+vis+balls))
 check('no_unsupported_NOT_PUBLIC_classification',all(r['status']!='NOT_PUBLIC' for r in E+phys+vis+balls))
 bad=[]
 for name,(rows,_) in tables.items():
  for i,r in enumerate(rows):
   if 'evidence_ids' in r:
    bad.extend((name,i,x) for x in r['evidence_ids'].split(';') if x and x not in ids)
 check('all_evidence_references_resolve',not bad,str(bad[:8]))
 check('history_six_traceable_dates_only',[(r['draw_id'],r['date']) for r in hist]==[('00027','2017-09-30'),('01372','2026-07-16'),('01373','2026-07-18'),('01374','2026-07-21'),('01375','2026-07-23'),('01376','2026-07-25')])
 check('no_case_code_or_model_promoted_to_asset_id',all(r['machine_id']=='UNKNOWN' and r['ball_set_id']=='UNKNOWN' for r in hist))
 expected_codes={'01372':'UNKNOWN','01373':'VC2','01374':'VC4','01375':'VC2','01376':'VC2'}
 check('case_observations_explicitly_partial',len(vis)==5 and all(r['status']=='PARTIAL' and r['case_code']==expected_codes[r['draw_id']] and r['persistent_ballset_id']=='UNKNOWN' and r['independent_second_review']=='NOT_EXECUTED' for r in vis))
 check('case_history_matches_review',all(r['observed_case_code']==expected_codes[r['draw_id']] for r in hist if r['draw_id']!='00027'))
 check('55_number_labels_not_physical_ids',len(balls)==55 and {r['printed_number'] for r in balls}=={f'{i:02d}' for i in range(1,56)} and all(r['ball_set_id']=='UNKNOWN' and r['physical_unit_id']=='UNKNOWN' for r in balls))
 actualcols=[k for k in balls[0] if k.startswith('actual_')]
 check('no_nominal_values_in_actual_ball_measurements',all(all(r[k]=='UNKNOWN' for k in actualcols) and r['measurement_date']=='UNKNOWN' and r['status']=='NOT_FOUND' for r in balls))
 check('no_invented_maintenance_events',not tables['extracted/maintenance_events.csv'][0])
 original=list(csv.DictReader((DT/'parameter_registry.csv').open(encoding='utf-8')))
 dependency=tables['extracted/parameter_dependency_map.csv'][0]
 check('all_99_parameters_mapped',len(dependency)==99 and {r['parameter'] for r in dependency}=={r['parameter'] for r in original})
 check('physical_status_143_unique_entries',len(phys)==143 and len({r['parameter'] for r in phys})==143)
 check('synthetic_defaults_not_real_measurements',all(r['value_SI']=='UNKNOWN' and r['status']=='NOT_FOUND' for r in phys if r['basis']=='synthetic_default'))
 current=tables['extracted/current_rule_facts.csv'][0];facts={r['parameter']:r for r in current}
 check('new_model_from_operator_document_not_resemblance',facts['power_documented_machine_model']['value_SI']=='MAGNUM II' and facts['power_documented_manufacturer']['value_SI']=='SMART PLAY' and all(facts[k]['pdf_page_1based']=='7' for k in ['power_documented_machine_model','power_documented_manufacturer']))
 vals={'mixing_chamber_diameter':'.61','machine_height':'1.78','machine_base_length':'.86','machine_base_width':'.84','machine_mass':'159','ball_mass_nominal':'.01234','ball_mass_tolerance':'.000617','ball_diameter_nominal':'.0505','ball_diameter_tolerance':'.001'}
 check('SI_transcriptions_match_reviewed_facts',all(abs(float(facts[k]['value_SI'])-float(v))<1e-12 for k,v in vals.items()))
 check('filename_year_not_issuance_date',facts['document_base_date']['value_SI']=='2023-03-03' and facts['document_amendment_effective_date']['value_SI']=='2025-01-22')
 pages=tables['extracted/rule_page_manifest.csv'][0]
 check('all_16_scan_pages_reviewed',len(pages)==16 and [int(r['pdf_page_1based']) for r in pages]==list(range(1,17)) and all(r['visual_review']=='INSPECTED' for r in pages))
 http=json.loads((EX/'http_recheck.json').read_text());h={r['evidence_id']:r for r in http}
 newsha='9819e0a0d18696d98438e37b4c4ab5caf8b285b7e0edf6c8acfba7a712be4b8e';oldsha='a0060ec29bbd39d9bbad3ef157a3214fba270b5290ea665e9ade098563cec589'
 check('official_PDF_source_digests_pinned',h['CURRENT_LINKED_POWER_RULE']['sha256']==newsha and h['RULE2017']['sha256']==oldsha and next(r for r in E if r['evidence_id']=='R10')['sha256']==newsha)
 sources=list(csv.DictReader((P/'phase2/phase2_sources.csv').open(encoding='utf-8')));sm={r['draw_id']:r for r in sources}
 manifests=tables['extracted/identity_frame_manifest.csv'][0]+tables['extracted/case_frame_manifest.csv'][0]
 check('315_native_frames_bound_to_five_pinned_sources',len(manifests)==315 and all(r['source_sha256']==sm[r['draw_id']]['video_sha256'] and r['source_url']==sm[r['draw_id']]['source_url'] and (r['width'],r['height'])==('1920','1080') for r in manifests))
 indexed={(r['draw_id'],float(r['source_pts_seconds'])):r for r in manifests}
 check('case_transcriptions_bound_to_native_frame_pairs',all(indexed[(r['draw_id'],float(r['label_pts_1']))]['frame_sha256']==r['label_frame_sha256_1'] and indexed[(r['draw_id'],float(r['label_pts_2']))]['frame_sha256']==r['label_frame_sha256_2'] and indexed[(r['draw_id'],float(r['open_case_pts']))]['frame_sha256']==r['open_frame_sha256'] for r in vis))
 # Portable audit works without copyrighted local inputs; local checks never fabricate a pass.
 all_local=all(Path(r['local_frame_path']).is_file() for r in manifests)
 if all_local:check('local_native_frame_file_hashes',all(sha(Path(r['local_frame_path']))==r['frame_sha256'] for r in manifests))
 else:skipped.append('Local native pixels not available; manifests validated, pixel bytes not rehashed')
 if all(Path(r['input_file_local_only']).is_file() for r in sources):check('local_five_full_MP4_hashes',all(sha(Path(r['input_file_local_only']))==r['video_sha256'] for r in sources))
 else:skipped.append('Local source MP4s unavailable; no full-video rehash claimed')
 docs=Path('C:/vietlott-research-output/physical-audit-20261022/documents')
 if (docs/'CURRENT_LINKED_POWER_RULE.pdf').exists():
  from pypdf import PdfReader
  p=docs/'CURRENT_LINKED_POWER_RULE.pdf';pdf=PdfReader(p)
  check('local_current_PDF_rehash_and_scan_character',sha(p)==newsha and len(pdf.pages)==16 and all(not p.extract_text().strip() for p in pdf.pages))
  html=(docs/'OFFICIAL_PROCESS_PAGE.html').read_text(encoding='utf-8')
  check('direct_official_link_chain',h['CURRENT_LINKED_POWER_RULE']['url'] in html and sha(docs/'OFFICIAL_PROCESS_PAGE.html')==h['OFFICIAL_PROCESS_PAGE']['sha256'])
  check('local_all_rendered_page_hashes',all(sha(Path(r['local_png']))==r['sha256'] for r in pages))
 else:skipped.append('Local source PDF/rendered pages unavailable; URL/source hashes remain pinned')
 frozen=tables['extracted/audit_input_hashes.csv'][0]
 check('prior_research_input_hashes_unchanged',all(sha(ROOT/r['path'])==r['sha256'] for r in frozen))
 saved=json.loads((EX/'saved_simulation_review.json').read_text())
 check('saved_run_totals_reconcile',saved['runs']==saved['stored_summary_total_runs']==78 and saved['valid_runs']==saved['stored_summary_valid_runs']==66 and saved['incomplete_runs']==9 and saved['complete_with_failures']==3 and saved['baseline_valid']==18 and saved['baseline_runs']==20 and saved['all_implementation_hashes_match'])
 check('stored_numerical_checks_not_claimed_new_runs',saved['stored_numerical_checks']==9 and saved['stored_system_checks']==14 and saved['stored_numerical_all_pass'] and saved['stored_system_all_pass'] and saved['independent_physical_validation'] is False)
 inv=json.loads((EX/'inventory_summary.json').read_text())
 check('unreachable_false_alarm_cross_checked',inv['fsck_reported_unreachable_commits']==inv['reported_unreachable_also_reachable']==138 and inv['genuinely_unreachable_lottery_commits']==0)
 check('inventory_count_matches_CSV',len(tables['ARTIFACT_INVENTORY.csv'][0])==inv['inventory_rows'])
 changes=git('diff','--name-only',BASE).splitlines()
 check('all_tracked_changes_confined_to_audit',all(p.startswith(PREFIX) for p in changes),str(changes[:10]))
 check('requested_audit_branch',git('rev-parse','--abbrev-ref','HEAD')=='audit/power655-physical-data-recovery')
 frozenrefs=tables['extracted/refs.csv'][0]
 check('protected_remote_heads_unchanged',all(git('rev-parse',r['ref'])==r['commit_sha'] for r in frozenrefs if r['ref'].startswith('refs/remotes/origin/') and r['ref']!='refs/remotes/origin/HEAD'))
 bad_media=[p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file() and p.suffix.lower() in ['.mp4','.m4a','.png','.jpg','.jpeg','.pdf','.gif']]
 check('no_new_copyrighted_source_pixels_or_video_in_audit',not bad_media,str(bad_media))
 md='\n'.join(p.read_text(encoding='utf-8') for p in OUT.glob('*.md'))
 check('no_invisible_or_tool_reference_tokens',not any(x in md for x in ['\u200b','\ufeff','turn19view0','::chatgpt-content-reference']))
 report=dict(generated_utc=datetime.now(timezone.utc).isoformat(),passed=all(checks.values()),checks=checks,passed_checks=sum(checks.values()),total_checks=len(checks),failures=errors,skipped_local_checks=skipped,base_commit=BASE,current_head=git('rev-parse','HEAD'),scope='Audit schemas/provenance/integrity and frozen result consistency; manual scan/case readings remain single-auditor observations; no independent actual-physics or forecast validation',scientific_datasets_complete=False,new_simulator_runs=0)
 (EX/'validation_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps({k:report[k] for k in ['passed','passed_checks','total_checks','failures','skipped_local_checks','new_simulator_runs']},indent=2))
 return 0 if report['passed'] else 1
if __name__=='__main__':sys.exit(main())
