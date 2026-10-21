"""Audit inputs without editing earlier phases; generate parameter/source ledgers."""
import csv
import hashlib
import json
import math
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def writecsv(path,rows):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def main():
    inventory=[]
    for path in sorted(ROOT.parent.rglob('*')):
        if not path.is_file() or ROOT in path.parents or path.suffix not in ['.md','.py','.csv','.json']:continue
        b=path.read_bytes();text=b.decode('utf-8-sig',errors='replace')
        inventory.append({'path':str(path.relative_to(ROOT.parent)).replace('\\','/'),
          'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'lines':len(text.splitlines()),
          'python_symbols':';'.join(re.findall(r'^(?:def|class) ([\w_]+)',text,re.M)),
          'inspection':'loaded_for_inventory; substantive findings traced in source_review.md'})
    writecsv(ROOT/'results/input_inventory.csv',inventory)
    c=json.loads((ROOT/'configs/baseline.json').read_text())
    registry=[]
    units={k:'1' for k in c}
    for k in ['radius','wall_thickness','ball_radius','diameter_tolerance','arm_length','arm_width','arm_depth','arm_curve',
              'mouth_radius','pocket_height','gate_thickness','gate_pause_depth','penetration_limit','initial_jitter']:units[k]='m'
    for k in ['ball_mass','mass_tolerance']:units[k]='kg'
    for k in ['dt','ramp_seconds','hold_seconds','mix_seconds','capture_period','max_seconds','sample_seconds']:units[k]='s'
    units.update(gravity='m s^-2',motor_torque='N m',gate_speed='m s^-1',rpm='rad s^-1')
    ranges={'radius':'.25:.45','depth_scale':'.6:1.2','wall_thickness':'.004:.020','ball_radius':'.02475:.02575',
       'ball_mass':'.011723:.012957','friction':'.05:.5','restitution':'.2:.8','rolling_friction':'0:.004',
       'spinning_friction':'0:.004','rpm':f'{15*2*math.pi/60}:{45*2*math.pi/60}',
       'mouth_radius':'.029:.037','pocket_height':'.055:.070','arm_length':'.24:.29','arm_depth':'.04:.10',
       'arm_curve':'0:.04','gate_speed':'.10:.4','mix_seconds':'3:30','capture_period':'3:15',
       'dt':'.00025:.001','solver_iterations':'40:160'}
    ranges['motor_torque']='3:30; post-hoc actuator stress range, not a measured hardware interval'
    documented={'ball_radius','ball_mass'}
    for key,value in c.items():
        registry.append({'parameter':key,'value_SI':value if key!='rpm' else value*2*math.pi/60,
           'unit_SI':units[key],'uncertainty_or_range_SI':ranges.get(key,'not experimentally quantified'),
           'classification':'documented' if key in documented else 'assumed',
           'source':'E01 Article 8.2 pages 7-8 via prior pinned extraction' if key in documented else 'configs/baseline.json; research hypothesis or numerical control',
           'applicability':'2017 nominal rule; not measured 2026 set' if key in documented else 'hypothetical simulator only',
           'current_machine_status':'unknown','notes':'radius = documented diameter / 2' if key=='ball_radius' else 'requested motor command in rev/min, not achieved speed; registry converts to rad/s' if key=='rpm' else ''})
    unknown_units={'each_ball_mass':'kg','each_ball_diameter':'m','ball_material_density':'kg m^-3',
       'center_of_mass_offsets':'m','contact_stiffness':'N m^-1','actual_RPM_time_series':'rad s^-1',
       'actual_mix_duration':'s','deceleration':'rad s^-2','loading_port_geometry':'m',
       'initial_55_positions_velocities':'m; m s^-1','initial_55_positions':'m','initial_55_velocities':'m s^-1',
       'control_latency':'s','permanent_isolation_time':'s','temperature':'K','vibration':'m s^-2','electrostatic_charge':'C'}
    for key in ['manufacturer_model','serial','revision','machine_replacement_history','maintenance_log',
       'ball_set_id','ball_replacement_history','each_ball_mass','each_ball_diameter','ball_material_density',
       'center_of_mass_offsets','static_friction','kinetic_friction_velocity_law','contact_stiffness',
       'actual_RPM_time_series','rotation_direction','axis_topology','actual_mix_duration','deceleration',
       'actual_gate_topology','loading_port_geometry','actual_loading_order','initial_55_positions_velocities','initial_55_positions','initial_55_velocities',
       'control_latency','permanent_isolation_time','wall_refraction','camera_intrinsics_extrinsics',
       'temperature','humidity','vibration','electrostatic_charge']:
        registry.append(dict(parameter=key,value_SI='NA',unit_SI=unknown_units.get(key,'1'),uncertainty_or_range_SI='unknown',
           classification='unknown',source='../phase2/unresolved_parameters.md',applicability='Power 6/55 broadcasts 2026',
           current_machine_status='unknown',notes='Not inferred from a similar Smartplay model'))
    for key,val,unit,source in [('ball_count',55,'1','E01 Article 8.2'),('paddle_count',3,'1','E01 Article 5.2 / 8.1'),
       ('documented_diameter',.0505,'m','E01 Article 8.2c'),('documented_diameter_tolerance',.001,'m','E01 Article 8.2c'),
       ('documented_mass_tolerance',.000617,'kg','E01 Article 8.2c')]:
        registry.append(dict(parameter=key,value_SI=val,unit_SI=unit,uncertainty_or_range_SI='rule nominal/tolerance, not empirical CI',
             classification='documented',source=source,applicability='2017 rule; equipment linkage to 2026 unknown',current_machine_status='unknown',notes=''))
    for key,val,unit in [('rotor_mass',.8,'kg'),('arm_root_radius',.035,'m'),('arm_segments',5,'1'),
       ('gate_travel',.11,'m'),('gate_bevel_height',.012,'m'),('tube_extra_height',.075,'m'),
       ('tube_panels',24,'1'),('trough_slope_angle',math.atan(.16),'rad'),('trough_length',.88,'m'),
       ('trough_inner_width',.092,'m'),('trough_drop_below_pocket',.13,'m'),
       ('main_end_stop_x',.79,'m'),('special_stop_x',.16,'m')]:
        registry.append(dict(parameter=key,value_SI=val,unit_SI=unit,uncertainty_or_range_SI='engineering construction constant; not experimentally quantified or exhaustively swept',
             classification='assumed',source='simulator/core.py or simulator/geometry.py',applicability='hypothetical model only',
             current_machine_status='unknown',notes='Implementation construction constant, not measured machine dimension'))
    for key,val,unit,kind,uncertainty in [('encoded_frame_interval',1001/30000,'s','measured','encoded rendition spacing; not camera-original exposure'),
       ('training_downstream_mean_interval',13.1247783,'s','estimated','two draw means; not a calibrated controller period or CI'),
       ('downstream_proxy_bracket_max_width',.133467,'s','measured','localization bound; not physical isolation-time accuracy')]:
        registry.append(dict(parameter=key,value_SI=val,unit_SI=unit,uncertainty_or_range_SI=uncertainty,
             classification=kind,source='../phase2/capture_event_audit.csv; calibration/intervals.csv',
             applicability='five 2026 broadcast renditions; downstream image proxy only',
             current_machine_status='physical interpretation limited',notes='Observable summary, not a recovered mechanical parameter'))
    registry.append(dict(parameter='mirror_y',value_SI=False,unit_SI='1',uncertainty_or_range_SI='boolean test transform',
             classification='assumed',source='experiments/protocol.json',applicability='hypothetical mirrored loading only',
             current_machine_status='unknown',notes='Optional experiment control; baseline false'))
    registry.append(dict(parameter='simulated_center_of_mass_offset',value_SI='[0,0,0]',unit_SI='m',
             uncertainty_or_range_SI='zero by model assumption; actual offsets unknown and not swept',classification='assumed',
             source='PyBullet centered uniform sphere construction in simulator/core.py',applicability='hypothetical rigid spheres only',
             current_machine_status='unknown',notes='Actual CoM deviations and anisotropy are not modeled'))
    registry.append(dict(parameter='uniform_sphere_nominal_density',value_SI=c['ball_mass']/(4*math.pi*c['ball_radius']**3/3),unit_SI='kg m^-3',
             uncertainty_or_range_SI='derived from historical nominal size/mass under uniform solid sphere assumption; not measured',classification='estimated',
             source='E01 historical nominals plus sphere volume formula',applicability='nominal equivalent density only',
             current_machine_status='unknown',notes='Not a measured foam material density or 2026 ball density'))
    writecsv(ROOT/'parameter_registry.csv',registry)

if __name__=='__main__':main()
