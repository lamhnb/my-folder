"""Serialize manually reviewed, bounded events; no image classification or fitting."""
import csv, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evidence'

CONFIG = {
 '01375': {'video':'is8GgE2gQu8', 'overview':[1030,1210],
   'mechanism':[None,[13,14],[13,14],[11,12],[12,13],[14,15],[21,22]],
   'collector':[[13,14],[21,22],[20,21],[21,22],[22,23],[21,22],[25,26]],
   'entry':[[3,7],[1,5],[3,7],[3,7],[6,10],[2,6],[2,6]],
   'overlay':[[38,39],[45,46],[52,53],[59,60],[66,67],[73,74],[80,81]],
   'nav_sheets':{1:[0,1],2:[0,1],3:[0,1],4:[0,1],5:[0,1],6:[0,1],7:[1,2]},
   'camera':'At 1070.002267 s the hub is near the pilot center but magnification is much larger and chamber rim extends outside frame; fixed annulus/ROI transfer refused.'},
 '01376': {'video':'diq_elyRXjo', 'overview':[990,1170],
   'mechanism':[None,[14,15],[16,17],[17,18],[18,19],[17,18],[18,19]],
   'collector':[[23,24],[21,22],[24,25],[24,25],[26,27],[23,24],[27,28]],
   'entry':[[2,6],[3,7],[3,7],[3,7],[0,4],[3,7],[3,7]],
   'overlay':[[34,35],[41,42],[47,48],[54,55],[61,62],[68,69],[75,76]],
   'nav_sheets':{1:[0,1],2:[0,1,2],3:[0,1,2],4:[0,1,2],5:[1,2],6:[1,2],7:[1,2]},
   'camera':'At 1029.028000 s the hub is roughly (1055,525), displaced from locked (932,525); scale/framing also differs. Fixed ROI transfer refused, without recentering or metric tuning.'}
}

def rows(folder):
 return list(csv.DictReader((E/folder/'frames.csv').open(encoding='utf-8')))

def ref(row):
 return {'file':row['file'],'source_pts_seconds':float(row['source_pts_seconds']),
         'sha256':row['sha256'],'width':int(row['width']),'height':int(row['height'])}

def event(kind, folder=None, pair=None, note='', status='bounded_visibility'):
 if pair is None:
  return {'event_type':kind,'lower_pts_seconds':None,'upper_pts_seconds':None,
          'event_timestamp_seconds':None,'status':'NA','before':None,'after':None,'note':note}
 rs=rows(folder); before,after=ref(rs[pair[0]]),ref(rs[pair[1]])
 return {'event_type':kind,'lower_pts_seconds':before['source_pts_seconds'],
         'upper_pts_seconds':after['source_pts_seconds'],'event_timestamp_seconds':None,
         'status':status,'before':before,'after':after,'note':note}

for draw,cfg in CONFIG.items():
 reviewed=[f'evidence/rep{draw}_overview/sheet_{i:03d}.jpg' for i in range(5)]
 captures=[]
 for i in range(7):
  tag=f'rep{draw}_c{i+1}'
  reviewed += [f'evidence/{tag}_nav/sheet_{s:03d}.jpg' for s in cfg['nav_sheets'][i+1]]
  reviewed += [f'evidence/{tag}_entry_native/sheet_000.jpg']
  events=[event('control_onset',note='Control downward actuation onset not established. First-attempt close-up already shows finger contact; later controls are off camera. Contact/light is not electrical command time.'),
   event('mechanism_first_visible_motion',tag+'_nav',cfg['mechanism'][i],
         note='Collector moving element changes from preceding stationary orientation; bracket from six-native-frame navigation, preview pixels. First attempt onset cut-occluded, hence NA.'),
   event('collector_ball_first_visible',tag+'_nav',cfg['collector'][i],
         note='Yellow surface first resolved below rim within housing after preceding empty housing sample; six-native-frame navigation visibility proxy, hidden entry plane unknown.'),
   event('permanent_isolation',note='Irreversible separation plane and closure topology not established from broadcast; pocket presence does not establish permanent isolation.'),
   event('trough_entry_visible_proxy',tag+'_entry_native',cfg['entry'][i],
         note='Leading physical ball edge passes collector mouth into downstream ramp/result channel. Every native frame reviewed in the local crop. Four-frame bracket retained for blur/refraction and edge-plane ambiguity; resolution is not empirical accuracy or selection time.'),
   event('overlay_number_first_clearly_readable',f'rep{draw}_overview',cfg['overlay'][i],
         note='Coarse bottom result-overlay bracket: preceding bottom graphic lacks new readable number, later sample has it. Venue background display is a separate graphic and may update sooner. Animation/first-readable transition not natively refined; timing quality target not met. Graphic event is separate from capture.',status='bounded_coarse_graphic'),
   event('spoken_announcement',note='Audio not reviewed directly; no ASR substitution.'),
   event('overlay_slot_filled',note='First slot-filled transition not separately refined; first-readable overview bracket cannot distinguish animation from slot placement.')]
  captures.append({'capture_index':i+1,'capture_role':'main' if i<6 else 'special','events':events})
 source=json.loads((E/f'source_{cfg["video"]}_ranges.json').read_text(encoding='utf-8'))
 extraction=json.loads((E/f'rep{draw}_overview/extraction.json').read_text(encoding='utf-8'))
 prefixes=[f'rep{draw}_overview',f'rep{draw}_geometry',f'rep{draw}_rotor']+[f'rep{draw}_c{i}_{suffix}' for i in range(1,8) for suffix in ['nav','entry_native']]
 manifests=[]
 for p in prefixes:
  manifests.append({'path':f'evidence/{p}/frames.csv','sha256':hashlib.sha256((E/p/'frames.csv').read_bytes()).hexdigest(),
                    'inspected_pts_seconds':[float(r['source_pts_seconds']) for r in rows(p)] if p.endswith('entry_native') or p.endswith('overview') else None,
                    'note':'PTS list is extraction coverage for nav; exact reviewed sheets and event endpoints identify actual visual review.'})
 reviewed += [f'evidence/rep{draw}_geometry/'+rows(f'rep{draw}_geometry')[0]['file'].split('/')[-1],
              f'evidence/rep{draw}_rotor/'+rows(f'rep{draw}_rotor')[0]['file'].split('/')[-1],
              'evidence/rotor_native_reference/pts_1098.030267.png']
 result={'schema_version':'1.0','draw_id':draw,'protocol':'phase2/locked_protocol.json',
  'review_kind':'manual_AI_visual_review_of_real_pinned_video','manual_AI_visual_review':True,
  'human_review':False,'blind_review':False,'reviewer_calibrated':False,
  'source':{'id':cfg['video'],'draw_id_context':draw,'input_file':extraction['input_file'],
   'input_sha256':extraction['input_sha256'],'source_pin':f'evidence/source_{cfg["video"]}_ranges.json',
   'source_dimensions':[1920,1080],'source_frame_rate':'30000/1001','native_encoded_interval_seconds':1001/30000,
   'camera_original_frame_rate':None,'shutter_exposure_seconds':None,'physical_clock_accuracy_seconds':None},
  'reviewed_contact_sheets_and_frames':reviewed,'extraction_manifests':manifests,
  'sampling':{'overview_every_native_frames':60,'navigation_every_native_frames':6,'entry_refinement_every_native_frames':1,
   'overview_requested_seconds':cfg['overview'],'overview_actual_first_pts':extraction['first_pts'],'overview_actual_last_pts':extraction['last_pts'],
   'time_basis':'native source rendition PTS, not frame/30'},
  'camera_gate':{'status':'fixed_ROI_transfer_refused','comparison':cfg['camera'],
   'pilot_reference':'evidence/rotor_native_reference/pts_1098.030267.png','replication_reference':rows(f'rep{draw}_rotor')[0]['file'],
   'motion_metrics_run':False,'physical_rpm':None,'physical_angle':None,
   'manual_event_crop_adjustment':{'xywh':[1450,0,470,750],'purpose':'View downstream collector mouth in close-up transport camera. Separate from locked motion ROI; crop logged in every extraction.json.','metric_tuning':False}},
  'captures':captures,'limitations':['All event point times remain NA; bounds describe physical visibility/graphic visibility, not latent selection time.',
   'Navigation images are 480x270 full-frame previews of native-PTS samples; native pixel refinement is limited to transport entry.',
   'No human or calibrated independent event review; no empirical temporal accuracy claim.',
   'No winning numbers used for parameter selection; visible result graphics only identify graphical transition state.',
   'Main six versus special transition separated; seven attempts are not seven independent draws.']}
 (E/f'replication_{draw}.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
 print(draw,[(c['capture_index'],c['events'][4]['lower_pts_seconds'],c['events'][4]['upper_pts_seconds']) for c in captures])
