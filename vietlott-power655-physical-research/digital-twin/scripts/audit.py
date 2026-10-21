"""Artifact/integrity audit; scientific failure flags remain data, not hidden."""
import csv
import hashlib
import json
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checks={};errors=[]
    branch=subprocess.check_output(['git','rev-parse','--abbrev-ref','HEAD'],cwd=REPO,text=True).strip()
    checks['requested_branch']=branch=='research/power655-physical-digital-twin'
    base='f329cab62a64c081d635eac8033a7029f7b4d51a'
    changed=subprocess.check_output(['git','diff','--name-only',base,'--'],cwd=REPO,text=True).splitlines()
    checks['protected_tracked_files_unchanged']=all(x.startswith('vietlott-power655-physical-research/digital-twin/') for x in changed)
    plan=json.loads((ROOT/'experiments/protocol.json').read_text())
    expected={f'{name}_seed{seed}.json' for name,seed,updates in plan['jobs']}
    paths=list((ROOT/'results/runs').glob('*.json'))
    checks['all_planned_runs_persisted']={p.name for p in paths}==expected
    hashes={name:sha(ROOT/'simulator'/name) for name in ['core.py','geometry.py']}
    for path in paths:
        r=json.loads(path.read_text());ee=r['captures']
        assertions=[len(r['final_positions'])==55,r['body_count']==89,
           len({e['physical_id'] for e in ee})==len(ee),len({e['label'] for e in ee})==len(ee),
           r['remaining']==55-len(ee),len(ee)<=7,
           all(e['role']==('special' if i==6 else 'main') and e['remaining']==54-i for i,e in enumerate(ee)),
           all(0<=e['physical_id']<55 and 1<=e['label']<=55 for e in ee),
           len(ee)!=7 or (r['remaining_in_chamber']==48 and len(r['pre_capture'])==7 and r['pre_capture'][6]['remaining_before']==49),
           r['implementation_sha256']==hashes,
           r['config_sha256']==hashlib.sha256(json.dumps(r['config'],sort_keys=True).encode()).hexdigest(),
           path.stem.endswith('_seed'+str(r['seed']))]
        if not all(assertions):errors.append(path.name)
    checks['run_integrity_and_current_implementation']=not errors
    torque_paths=list((ROOT/'results/torque_diagnostic').glob('seed*.json'))
    checks['three_posthoc_torque_runs_separate_and_pinned']=(len(torque_paths)==3 and all(
        json.loads(p.read_text())['implementation_sha256']==hashes and
        json.loads(p.read_text())['config']['motor_torque']==30. for p in torque_paths))
    sources=json.loads((ROOT/'results/source_hash_verification.json').read_text())
    checks['five_original_videos_hash_verified']=len(sources)==5 and all(x['expected']==x['actual'] for x in sources)
    frames=json.loads((ROOT/'geometry/landmark_provenance.json').read_text())
    checks['landmark_frames_match_prior_ledgers']=len(frames)==5 and all(x['matches_prior_frame_ledger'] for x in frames)
    mesh=json.loads((ROOT/'geometry/mesh_quality.json').read_text())
    checks['clean_cad_manifold_and_hash']=(mesh['all_clean_edges_have_two_incident_faces'] and
       mesh['clean_euler_characteristic']==2 and mesh['clean_obj_sha256']==sha(ROOT/'geometry/chamber_clean.obj'))
    old=json.loads((ROOT/'results/development_gate_v1/baseline_seed1004.json').read_text())
    archive=ROOT/'results/development_gate_v1/replay/simulator'
    checks['failed_gate_version_source_hash_preserved']=all(sha(archive/name)==old['implementation_sha256'][name] for name in ['core.py','geometry.py'])
    ignored_dirs={'__pycache__','.pytest_cache','local-evidence','.venv'}
    checks['no_new_source_video']=not any(p.suffix.lower() in ['.mp4','.m4a','.webm','.mov'] for p in ROOT.rglob('*')
       if p.is_file() and not any(x in p.parts for x in ignored_dirs))
    checks['baseline_numerical_and_system_passed']=all(json.loads((ROOT/f'validation/{name}.json').read_text())['passed'] for name in ['numerical','system'])
    diagnostics=json.loads((ROOT/'validation/ensemble_diagnostics.json').read_text())
    checks['exact_label_permutation']=diagnostics['exact_label_permutation_passed']
    checks['same_binary_exact_repeat']=diagnostics['same_seed_exact_repeat_passed']
    checks['handoff_exists']=(ROOT/'FINAL_DIGITAL_TWIN_HANDOFF.md').exists()
    required=['README.md','FINAL_DIGITAL_TWIN_HANDOFF.md','parameter_registry.csv','requirements.txt',
              'geometry/chamber.obj','renders/seed0.gif','results/trajectory_seed0.csv','charts/sensitivity.png']
    checks['required_deliverables']=all((ROOT/name).is_file() for name in required)
    registry=list(csv.DictReader((ROOT/'parameter_registry.csv').open(encoding='utf-8')))
    keys={r['parameter'] for r in registry}
    all_controls=set(json.loads((ROOT/'configs/baseline.json').read_text()))
    for updates in plan['configurations'].values():all_controls.update(updates)
    checks['all_runtime_controls_registered']=all_controls.issubset(keys)
    checks['parameter_provenance_schema']=all(r['classification'] in ['measured','documented','estimated','assumed','unknown'] and
       r['source'] and r['applicability'] and r['uncertainty_or_range_SI'] for r in registry)
    report={'passed':all(checks.values()),'checks':checks,'run_integrity_errors':errors,'runs':len(paths),
      'branch':branch,'base':base,'scientific_prediction_validated':False,
      'note':'Artifact pass is separate from per-configuration physical failures and incomplete real-world calibration.'}
    (ROOT/'validation/audit.json').write_text(json.dumps(report,indent=2))
    excluded={'results/file_manifest.csv','validation/audit.json'}
    rows=[]
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file():continue
        rel=path.relative_to(ROOT).as_posix()
        if rel in excluded or any(x in path.parts for x in ignored_dirs):continue
        rows.append({'path':rel,'bytes':path.stat().st_size,'sha256':sha(path)})
    with (ROOT/'results/file_manifest.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['path','bytes','sha256']);w.writeheader();w.writerows(rows)
    print(json.dumps(report,indent=2))
    if not report['passed']:raise SystemExit(2)

if __name__=='__main__':main()
