"""Write explicit feasibility/hypothesis summaries, with no fabricated estimates."""
import csv,json
from pathlib import Path
from build_results import ROOT,write_csv
def main():
    hypotheses=[
      {'hypothesis':'H1','status':'not_testable','independent_draws_with_required_physical_inputs':0,'observation':'No verified physical angle at confirmed isolation/selection time.','estimate':None,'p_value':None,'confidence_interval':None,'unknown':'Unique marker; calibration; alias branch; true capture/isolating plane.','evidence':'evidence/pilot_motion/interpretation.md; evidence/native_refinement.json'},
      {'hypothesis':'H2','status':'partially_observable_descriptive_only','independent_draws_with_required_physical_inputs':0,'observation':'35 downstream transport visibility brackets across5draws;25main-to-main and5main-to-special intervals.','estimate':'See evidence/cadence_summary.json: five draw-level means of visible downstream intervals; no physical capture timer identified.','p_value':None,'confidence_interval':None,'unknown':'Mixing onset/duration, hidden selection/isolation times, control latency, same machine/ball-set identity.','evidence':'evidence/visible_cadence_intervals.csv; evidence/visible_cadence_by_draw.csv; evidence/pilot_boundary_review.json'},
      {'hypothesis':'H3','status':'not_testable','independent_draws_with_required_physical_inputs':0,'observation':'Moving balls/masks and colour differences visible; no validated sampling density or visibility correction.','estimate':None,'p_value':None,'confidence_interval':None,'unknown':'Detector precision/recall, per-depth visibility, collector-area calibration and independent labels.','evidence':'evidence/pilot_motion/interpretation.md; evidence/replication_01374.json'},
      {'hypothesis':'H4','status':'not_testable','independent_draws_with_required_physical_inputs':0,'observation':'No validated identity chain from loading through mixing/collisions to selection.','estimate':None,'p_value':None,'confidence_interval':None,'unknown':'BallIDs, initial3Dstates and controlled interventions.','evidence':'unresolved_parameters.md'},
      {'hypothesis':'H5','status':'not_testable','independent_draws_with_required_physical_inputs':0,'observation':'Apparent colour/camera conditions differ across broadcasts.','estimate':None,'p_value':None,'confidence_interval':None,'unknown':'Serials, verified ball-set/material data, comparable camera calibration, replicated groups.','evidence':'evidence/replication_01374.json; unresolved_parameters.md'},
    ]
    write_csv(ROOT/'phase2_hypothesis_results.csv',list(hypotheses[0]),hypotheses)
    rows=[
      ('source_PTS','observation','yes','30000/1001 encoded rendition timing','microsecond text precision is not event accuracy','ffprobe/showinfo and extraction.json'),
      ('physical_absolute_paddle_angle','unknown','no',None,'unique material marker and camera calibration absent','evidence/pilot_motion/interpretation.md'),
      ('threefold_symmetry_shared_axis','assumption','not_verified',None,'apparent three blades do not certify shared axis/speed;h3 remains an image hypothesis','locked_protocol.json'),
      ('physical_RPM','unknown','no',None,'legacy candidates and new same-pixel image frequencies cannot resolve marker/alias/calibration','evidence/legacy_rpm_audit.md'),
      ('image_pattern_frequency','estimate','pilot_only','3.596368Hz unmasked h3 spectrum','bin0.199798Hz is notCI; shared signal autocorrelation compatible within bin','evidence/pilot_motion/diagnostics.json'),
      ('collector_external_motion','observation','partial','pilot5initial-onset brackets;2cut-censored','orientation of exposed element only; not complete gate_open state','evidence/native_refinement.json'),
      ('collector_ball_visibility','observation','partial','pilot6appearance brackets;firstalreadyvisible','hidden true entry plane and earlier occluded occupancy unknown','evidence/native_refinement.json'),
      ('permanent_ball_isolation_time','unknown','no',None,'internal separation/closure topology and irreversibility unknown','evidence/native_refinement.json'),
      ('downstream_transport_proxy','observation','yes','35bounds;pilot1–2encoded intervals;replication1–4intervals','localization width is not empirical physical accuracy;different manual view crops disclosed','official_draw_events.csv'),
      ('bottom_result_graphic','observation','yes_but_quality_varies','pilot0.1001–0.2002s;replication2.002s coarsebounds','graphic latencies differ from selection;replication graphics fail0.2002s target','official_draw_events.csv'),
      ('button_electrical_command','unknown','no',None,'finger contact/light not electrical actuation or latency','capture_event_audit.csv'),
      ('official_mixing_duration','unknown','no',None,'start hidden by cut; ASR not physical oracle','evidence/pilot_boundary_review.json'),
      ('visible_cadence','estimate','descriptive_only','five draw-level summaries','draw is independent unit;special separate;no timer/null inference','evidence/cadence_summary.json'),
      ('individual_ball_identity_through_collisions','unknown','no',None,'no calibrated ID associations through occlusion/depth','unresolved_parameters.md'),
      ('camera_original_FPS_shutter','unknown','no',None,'24/149near-duplicate candidate pairs in pilot;encodedFPS not independent-frame rate','evidence/pilot_motion/source_frame_quality.json'),
      ('machine_geometry_material_parameters','unknown','no',None,'dimensions,serials,mass/friction/restitution not recoverable uniquely from these views','unresolved_parameters.md'),
      ('calibratable_3D_simulation','decision','NO-GO',None,'missing identifiable physical parameters and state;qualitative illustration remains possible','simulation_readiness.md'),
    ]
    fields=['quantity','epistemic_class','observable','value_or_scope','limitation','evidence']
    write_csv(ROOT/'observability_matrix.csv',fields,[dict(zip(fields,r)) for r in rows])
    failures=[
      ('web_youtube_open','failed','Onlinefetchthrottled;no pixels','evidence/transport_failures.json'),
      ('default_address_family','terminated','No clip after>180s;IPv4 diagnosticHTTP succeeded','evidence/transport_failures.json'),
      ('copyts_relative_duration','failed','Exit0but0decodedframes;PTScoverage rejected;input262bytesnotvideo','evidence/acquire_IUU05082QtE_980_265.json'),
      ('bounded_bridge_copy','terminated_failed','Partial67MBMP4moovmissing;nevermeasurementinput','evidence/acquire_IUU05082QtE_980_265_v2.json'),
      ('sequential_download','failed','Bound exceeded;partialfile never source input','evidence/source_IUU05082QtE.json'),
      ('standard_ranges_download','succeeded','Fivecompletecontent-length inputs hashpinned;failedattempts retained','phase2_sources.csv'),
      ('preview_first_capture','corrected','Lowresolution missedballalreadyheld;nativeevidence supersedes onset estimate','evidence/native_refinement.json'),
      ('preview_sixth_mechanism','corrected','Firstcloseupalreadyopen;secondarymotion not initialonset','evidence/native_refinement.json'),
      ('legacy_stable_camera_assumption','refuted','Same120nativecrop hashesverified;framing/scalechangeobserved','evidence/legacy_camera_review.json'),
      ('masked_motion_spectrum','refused','Frame51missingangularsector;no interpolation','evidence/pilot_motion/diagnostics.json'),
      ('motion_transfer_four_draws','refused','Changedzoom/center;greenballs01374affectyellowmask;no silentretuning','evidence/replication_01374.json'),
      ('derived_builder_before_dependencies','failed_corrected','Missingreplicationreview rejected;added fullpreflightbeforeoutputmutation','scripts/test_phase2_results.py'),
      ('pip_freeze_runtime','unavailable','Environmenthasnopip;installedversionspinnedviaimportlib.metadata','evidence/runtime_versions.json'),
      ('independent_human_audio_review','not_done','No calibrated humanreviewor directaudiolistening;do not infer accuracy','DATA_DICTIONARY.md'),
    ]
    fields=['attempt','outcome','reason_or_resolution','evidence']
    write_csv(ROOT/'evidence'/'failed_attempts.csv',fields,[dict(zip(fields,r)) for r in failures])
    print(json.dumps({'hypotheses':len(hypotheses),'observability_rows':len(rows),'attempts_and_limitations':len(failures)}))
if __name__=='__main__':main()
