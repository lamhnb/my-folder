"""PyBullet dynamics; no coordinate-based winning-number picker.

One physical ID remains attached to each sphere for its complete lifetime.
Capture: open upper gate -> contact-supported single pocket -> upper gate
closes only with a clear swept volume -> hold -> lower gate opens -> ball
contacts physical trough. No teleport, removal, disabling ball collisions,
or force depending on printed number. Jam/extra ball is an explicit failure.
"""
import hashlib
import json
import math
import platform
import time
from pathlib import Path
import numpy as np
import pybullet as p
from .geometry import shell, arm_parts, initial_positions

ROOT=Path(__file__).resolve().parents[1]


def load_config(path=None, **updates):
    c=json.loads((ROOT/'configs/baseline.json').read_text())
    if path: c.update(json.loads(Path(path).read_text()))
    c.update(updates)
    if not 0<c['mouth_radius']<c['radius']: raise ValueError('Invalid outlet')
    if c['dt']<=0 or c['max_seconds']<=0 or c['solver_iterations']<1: raise ValueError('Invalid numerical controls')
    if c['ball_radius']<=0 or c['ball_mass']<=0: raise ValueError('Invalid ball')
    if c['label_shift']!=int(c['label_shift']): raise ValueError('Labels must be integers')
    return c


class Twin:
    def __init__(self,c,seed=0):
        self.c=c; self.seed=seed; self.client=p.connect(p.DIRECT)
        p.setGravity(0,0,-c['gravity']);p.setTimeStep(c['dt'])
        p.setPhysicsEngineParameter(numSolverIterations=c['solver_iterations'],
                                    deterministicOverlappingPairs=1,contactBreakingThreshold=.001,
                                    restitutionVelocityThreshold=0.01)
        self.t=0.; self.events=[]; self.states=[];self.captured=[];self.phase='MIX'
        self.phase_since=0.;self.next_request=c['mix_seconds'];self.held=None
        self.gate_open=0.;self.floor_open=0.;self.failures=[];self.max_penetration=0.
        self.max_ball_overlap=0.;self.max_penetration_pair=None;self.trace=[]
        self.jam_time=0.;self.speed_samples=[];self.pre_capture=[];self.uncollected_exit_ids=set();self.rotor_samples=[]
        self.z=-math.sqrt(c['radius']**2-c['mouth_radius']**2)
        self.floor_z=self.z-c['pocket_height']
        vertices,faces=shell(c)
        sh=p.createCollisionShape(p.GEOM_MESH,vertices=vertices,indices=np.array(faces).ravel().tolist(),flags=p.GEOM_FORCE_CONCAVE_TRIMESH)
        self.chamber=p.createMultiBody(0,sh)
        self.static=[self.chamber]
        # Tube walls made of tangent boxes. Contacts remain ordinary rigid-body contacts.
        a=c['mouth_radius'];height=c['pocket_height']+.075
        for j in range(24):
            ang=2*math.pi*j/24
            self.box([.004,a*math.tan(math.pi/24)+.002,height/2],
                     [(a+.004)*math.cos(ang),(a+.004)*math.sin(ang),self.z-height/2+.002],
                     p.getQuaternionFromEuler([0,0,ang]))
        # Convex bevel at leading edge lifts an upper queued ball during closing.
        # The occupied pocket below must be clear of the swept lower face.
        w=a+.008;d=c['gate_thickness']/2
        vv=[[x,y,z] for x,z in [(-w,-d),(-w,0),(w,.012),(w,-d)] for y in [-w,w]]
        gs=p.createCollisionShape(p.GEOM_MESH,vertices=vv)
        self.upper=p.createMultiBody(0,gs,basePosition=[0,0,self.z]);self.static.append(self.upper)
        self.lower=self.box([a+.008,a+.008,c['gate_thickness']/2],[0,0,self.floor_z])
        # Continuous sloping trough with side rails, bottom stop and separate special stop.
        self.slope=.16; self.ramp_top=self.floor_z-.13
        self.ramp=self.box([.44,.046,.008],[.36,0,self.ramp_top-.36*self.slope],
                           p.getQuaternionFromEuler([0,math.atan(self.slope),0]))
        for y in [-.05,.05]:
            self.box([.44,.006,.06],[.36,y,self.ramp_top-.36*self.slope+.045],
                     p.getQuaternionFromEuler([0,math.atan(self.slope),0]))
        self.box([.008,.052,.065],[.79,0,self.ramp_top-.79*self.slope+.05])
        self.box([.008,.052,.065],[-.075,0,self.ramp_top+.012+.05])
        self.special_stop=self.box([.005,.045,.05],[.16,.20,self.ramp_top])
        # Motor drives a finite-inertia revolute link. No per-step arm teleportation.
        parts=arm_parts(c)
        shape=p.createCollisionShapeArray(shapeTypes=[p.GEOM_BOX]*len(parts),
                 halfExtents=[v[0] for v in parts],collisionFramePositions=[v[1] for v in parts],
                 collisionFrameOrientations=[p.getQuaternionFromEuler([0,v[2],0]) for v in parts])
        self.rotor=p.createMultiBody(baseMass=0,baseCollisionShapeIndex=-1,
                 linkMasses=[.8],linkCollisionShapeIndices=[shape],linkVisualShapeIndices=[-1],
                 linkPositions=[[0,0,0]],linkOrientations=[[0,0,0,1]],linkInertialFramePositions=[[0,0,0]],
                 linkInertialFrameOrientations=[[0,0,0,1]],linkParentIndices=[0],
                 linkJointTypes=[p.JOINT_REVOLUTE],linkJointAxis=[[0,1,0]])
        p.changeDynamics(self.rotor,0,lateralFriction=c['friction'],restitution=c['restitution'])
        rng=np.random.default_rng(seed+314159)
        self.radii=c['ball_radius']+rng.uniform(-.5,.5,55)*c['diameter_tolerance']
        self.masses=c['ball_mass']+rng.uniform(-1,1,55)*c['mass_tolerance']
        if np.any(self.masses<=0) or np.any(self.radii<=0): raise ValueError('Invalid tolerances')
        self.balls=[None]*55
        positions=initial_positions(c,seed)
        order=list(range(55)); order=order[::-1] if c['reverse_insertion'] else order
        for i in order:
            shape=p.createCollisionShape(p.GEOM_SPHERE,radius=float(self.radii[i]))
            self.balls[i]=p.createMultiBody(float(self.masses[i]),shape,basePosition=positions[i])
            p.changeDynamics(self.balls[i],-1,lateralFriction=c['friction'],restitution=c['restitution'],
               rollingFriction=c['rolling_friction'],spinningFriction=c['spinning_friction'],
               linearDamping=c['linear_damping'],angularDamping=c['angular_damping'],
               ccdSweptSphereRadius=float(self.radii[i])*.8,contactProcessingThreshold=0)
        self.index={body:i for i,body in enumerate(self.balls)}
        # Unknown real loading order: randomize labels with an independent stream.
        # Sequential rejection packing must never attach a permanent printed number
        # to the first/last accepted location or engine body creation order.
        label_rng=np.random.default_rng(np.random.SeedSequence([seed,9021047]))
        self.labels=[1+(int(i)+c['label_shift'])%55 for i in label_rng.permutation(55)]
        for body in self.static:
            p.changeDynamics(body,-1,lateralFriction=c['friction'],restitution=c['restitution'])
        self.set_phase('MIX')

    def box(self,half,pos,orn=(0,0,0,1)):
        shape=p.createCollisionShape(p.GEOM_BOX,halfExtents=half)
        body=p.createMultiBody(0,shape,basePosition=pos,baseOrientation=orn)
        self.static.append(body)
        return body

    def set_phase(self,phase):
        self.phase=phase;self.phase_since=self.t
        self.states.append({'time':self.t,'phase':phase,'captured':len(self.captured)})

    def positions(self):
        return np.array([p.getBasePositionAndOrientation(b)[0] for b in self.balls])

    def controller(self,pos):
        c=self.c;dt=c['dt'];a=c['mouth_radius'];rmax=float(max(self.radii))
        if self.phase=='MIX' and self.t>=self.next_request:
            if len(self.captured)==6:
                # Special stays in a separate physical upstream keeper.
                p.resetBasePositionAndOrientation(self.special_stop,[.16,0,self.ramp_top-.16*self.slope+.045],[0,0,0,1])
            self.set_phase('ADMIT')
        if self.phase=='ADMIT':
            self.gate_open=min(.11,self.gate_open+c['gate_speed']*dt)
            candidates=[i for i,v in enumerate(pos) if i not in self.captured and
                        v[2]+self.radii[i]<self.z-c['gate_thickness']/2-.001 and
                        v[2]>self.floor_z and np.linalg.norm(v[:2])<a]
            supported=[i for i in candidates if p.getContactPoints(self.balls[i],self.lower)]
            # Clear swept slab required before closure. Never rank candidates by label/distance.
            obstruction=any(v[2]<self.z+.005 and abs(v[2]-self.z)<self.radii[i]+c['gate_thickness']+.001 and
                            abs(v[0])<a+self.radii[i]+.11 and abs(v[1])<a+self.radii[i]
                            for i,v in enumerate(pos) if i not in supported)
            if len(supported)==1 and not obstruction:
                self.held=supported[0];self.set_phase('ISOLATE')
            if self.t-self.phase_since>12: self.jam_time+=dt
        elif self.phase=='ISOLATE':
            self.gate_open=max(0,self.gate_open-c['gate_speed']*dt)
            if self.gate_open==0:
                self.pre_capture.append({'time':self.t,'physical_id':self.held,'position':pos[self.held].tolist(),
                    'velocity':list(p.getBaseVelocity(self.balls[self.held])[0]),'remaining_before':55-len(self.captured)})
                self.set_phase('HOLD')
        elif self.phase=='HOLD' and self.t-self.phase_since>=c['hold_seconds']:
            self.set_phase('RELEASE')
        elif self.phase=='RELEASE':
            self.floor_open=min(.11,self.floor_open+c['gate_speed']*dt)
            i=self.held
            if pos[i,2]<self.floor_z-.045 and p.getContactPoints(self.balls[i],self.ramp):
                if i in self.captured: self.failures.append('double_capture')
                self.captured.append(i)
                self.events.append({'index':len(self.captured),'role':'special' if len(self.captured)==7 else 'main',
                   'physical_id':i,'label':self.labels[i],'time':self.t,'remaining':55-len(self.captured),
                   'position':pos[i].tolist(),'velocity':list(p.getBaseVelocity(self.balls[i])[0])})
                self.set_phase('RESET')
        elif self.phase=='RESET':
            if self.held is not None and pos[self.held,2]+self.radii[self.held]>self.floor_z-.012: return
            self.floor_open=max(0,self.floor_open-c['gate_speed']*dt)
            if self.floor_open==0:
                self.held=None;self.next_request=max(self.next_request+c['capture_period'],self.t+.1)
                self.set_phase('DONE' if len(self.captured)==7 else 'MIX')
        p.resetBasePositionAndOrientation(self.upper,[self.gate_open,0,self.z],[0,0,0,1])
        p.resetBaseVelocity(self.upper,[c['gate_speed'] if self.phase=='ADMIT' and self.gate_open<.11 else
                                       -c['gate_speed'] if self.phase=='ISOLATE' and self.gate_open>0 else 0,0,0])
        p.resetBasePositionAndOrientation(self.lower,[self.floor_open,0,self.floor_z],[0,0,0,1])
        p.resetBaseVelocity(self.lower,[c['gate_speed'] if self.phase=='RELEASE' and self.floor_open<.11 else
                                       -c['gate_speed'] if self.phase=='RESET' and self.floor_open>0 else 0,0,0])

    def step(self):
        c=self.c
        omega=c['rpm']*2*math.pi/60*min(1,self.t/max(c['ramp_seconds'],c['dt']))
        omega*=1+c['rpm_modulation']*math.sin(2*math.pi*.4*self.t)
        p.setJointMotorControl2(self.rotor,0,p.VELOCITY_CONTROL,targetVelocity=omega,force=c['motor_torque'])
        self.controller(self.positions())
        p.stepSimulation();self.t+=c['dt']
        contacts=p.getContactPoints()
        for cp in contacts:
            if cp[1] not in self.index and cp[2] not in self.index: continue
            dep=max(0,-cp[8])
            if dep>self.max_penetration:
                self.max_penetration=dep;self.max_penetration_pair=[cp[1],cp[2],self.t]
            if cp[1] in self.index and cp[2] in self.index:self.max_ball_overlap=max(self.max_ball_overlap,dep)
        if p.getNumBodies()!=len(self.static)+56: raise AssertionError('Body conservation failed')
        if int(round(self.t/c['dt']))%max(1,round(c['sample_seconds']/c['dt']))==0:
            xyz=self.positions();vel=np.array([p.getBaseVelocity(b)[0] for b in self.balls])
            joint=p.getJointState(self.rotor,0)
            self.trace.append((self.t,xyz,vel,[joint[0],self.gate_open,self.floor_open]))
            self.rotor_samples.append((self.t,joint[1],joint[3]))
            self.speed_samples.append(float(np.sqrt(np.mean(vel**2))))
            # Escape check separates chamber, neck, and result trough volumes.
            for i,v in enumerate(xyz):
                if v[2]<self.floor_z-self.radii[i]-.01 and i not in self.captured and i!=self.held:
                    self.uncollected_exit_ids.add(i)
                valid=(np.linalg.norm(v/[1,c['depth_scale'],1])<c['radius']+self.radii[i]+.004 or
                       (np.linalg.norm(v[:2])<c['mouth_radius']+.025 and self.ramp_top-.04<v[2]<self.z+.04) or
                       (-.1<v[0]<.83 and abs(v[1])<.09 and self.ramp_top-.22<v[2]<self.floor_z))
                if not valid and 'escaped_body' not in self.failures:self.failures.append('escaped_body')

    def run(self):
        start=time.perf_counter();settled_until=None
        while self.t<self.c['max_seconds']:
            self.step()
            if round(self.t/self.c['dt'])%round(10/self.c['dt'])==0:
                print(f'seed={self.seed} t={self.t:.1f}s phase={self.phase} captures={len(self.captured)} penetration={self.max_penetration:.6f}',flush=True)
            if self.phase=='DONE':
                if settled_until is None:settled_until=self.t+2.
                if self.t>=settled_until: break
        if len(self.captured)<7:self.failures.append('incomplete_seven')
        if self.max_penetration>self.c['penetration_limit']:self.failures.append('penetration_limit')
        if len(set(self.captured))!=len(self.captured):self.failures.append('nonunique_capture')
        if self.uncollected_exit_ids:self.failures.append('unauthorized_exit')
        final_positions=self.positions()
        remaining_in_chamber=int(sum(i not in self.captured and v[2]>self.z-.03 for i,v in enumerate(final_positions)))
        return {'seed':self.seed,'config':self.c,'config_sha256':hashlib.sha256(json.dumps(self.c,sort_keys=True).encode()).hexdigest(),
                'implementation_sha256':{name:hashlib.sha256((ROOT/'simulator'/name).read_bytes()).hexdigest() for name in ['core.py','geometry.py']},
                'engine_api':p.getAPIVersion(),'python':platform.python_version(),'platform':platform.platform(),
                'seconds':self.t,'wall_seconds':time.perf_counter()-start,'captures':self.events,'states':self.states,
                'physical_ids':self.captured,'remaining':55-len(self.captured),'body_count':p.getNumBodies(),
                'max_penetration_m':self.max_penetration,'max_ball_overlap_m':self.max_ball_overlap,
                'max_penetration_pair':self.max_penetration_pair,'jam_seconds':self.jam_time,
                'rms_speed_mean_m_s':float(np.mean(self.speed_samples)) if self.speed_samples else None,
                'failures':sorted(set(self.failures)),
                'pre_capture':self.pre_capture,'rotor_samples_time_omega_torque_SI':self.rotor_samples,
                'uncollected_exit_ids':sorted(self.uncollected_exit_ids),
                'remaining_in_chamber':remaining_in_chamber,'final_positions':final_positions.tolist(),
                'scope':'hypothetical_model_only'}

    def save_trace(self,path):
        np.savez_compressed(path,time=np.array([x[0] for x in self.trace]),
                            position=np.array([x[1] for x in self.trace]),velocity=np.array([x[2] for x in self.trace]),
                            mechanism=np.array([x[3] for x in self.trace]),
                            labels=self.labels,radii=self.radii)

    def close(self):
        if p.isConnected(self.client):p.disconnect(self.client)


def simulate(c,seed,trace=None):
    twin=Twin(c,seed)
    try:
        report=twin.run()
        if trace:twin.save_trace(trace)
        return report
    finally:twin.close()
