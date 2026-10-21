"""Independent analytical rigid-body experiments; no lottery outcomes used."""
import math
import numpy as np
import pybullet as p


def world(dt,iterations=80,gravity=0):
    cid=p.connect(p.DIRECT);p.setGravity(0,0,-gravity);p.setTimeStep(dt)
    p.setPhysicsEngineParameter(numSolverIterations=iterations,restitutionVelocityThreshold=0,
                               contactERP=0,contactSlop=0)
    return cid


def sphere(pos,vel=(0,0,0),r=.025,m=.01234,e=1,mu=0,rolling=0):
    b=p.createMultiBody(m,p.createCollisionShape(p.GEOM_SPHERE,radius=r),basePosition=pos)
    p.changeDynamics(b,-1,restitution=e,lateralFriction=mu,rollingFriction=rolling,
                     spinningFriction=0,linearDamping=0,angularDamping=0)
    p.resetBaseVelocity(b,vel);return b


def isolated(dt=.0005,iterations=80,restitution=1):
    world(dt,iterations)
    try:
        bodies=[sphere([-.08,0,0],[.4,0,0],e=restitution),sphere([.08,0,0],[-.2,0,0],e=restitution)]
        mass=.01234
        def measures():
            v=np.array([p.getBaseVelocity(b)[0] for b in bodies])
            return mass*v.sum(axis=0),.5*mass*np.sum(v*v)
        p0,e0=measures();maxdep=0
        for _ in range(round(.6/dt)):
            p.stepSimulation()
            for cp in p.getContactPoints():maxdep=max(maxdep,-cp[8])
        p1,e1=measures()
        vv=[p.getBaseVelocity(b)[0][0] for b in bodies]
        return {'dt':dt,'iterations':iterations,'per_body_restitution':restitution,
                'measured_relative_restitution':(vv[1]-vv[0])/.6,
                'expected_combined_restitution':restitution**2,'momentum_error_kg_m_s':float(np.linalg.norm(p1-p0)),
                'energy_relative_error':float(abs(e1-e0)/e0),'penetration_m':maxdep,
                'outgoing_x':[p.getBaseVelocity(b)[0][0] for b in bodies]}
    finally:p.disconnect()


def dissipative(mu=.4,rolling=.001,dt=.0005):
    world(dt,gravity=9.80665)
    try:
        ground=p.createMultiBody(0,p.createCollisionShape(p.GEOM_PLANE))
        p.changeDynamics(ground,-1,lateralFriction=mu,restitution=0,rollingFriction=rolling)
        b=sphere([0,0,.02501],[.6,0,0],e=0,mu=mu,rolling=rolling)
        energies=[];maxdep=0
        for j in range(round(2/dt)):
            v,w=p.getBaseVelocity(b);z=p.getBasePositionAndOrientation(b)[0][2]
            energies.append(.5*.01234*np.dot(v,v)+.5*(.4*.01234*.025**2)*np.dot(w,w)+.01234*9.80665*(z-.025))
            p.stepSimulation()
            for cp in p.getContactPoints(b,ground):maxdep=max(maxdep,-cp[8])
        return {'initial_energy_J':float(energies[0]),'final_energy_J':float(energies[-1]),
                'ratio':float(energies[-1]/energies[0]),'max_energy_J':float(max(energies)),
                'max_penetration_m':maxdep,'final_height_m':p.getBasePositionAndOrientation(b)[0][2]}
    finally:p.disconnect()


def free_fall(dt):
    world(dt,gravity=9.80665)
    try:
        b=sphere([0,0,1]);t=.4
        for _ in range(round(t/dt)):p.stepSimulation()
        z=p.getBasePositionAndOrientation(b)[0][2]
        return {'dt':dt,'absolute_z_error_m':abs(z-(1-.5*9.80665*t*t))}
    finally:p.disconnect()


def run_numerical():
    isolated_rows=[isolated(dt,it) for dt in [.001,.0005,.00025] for it in [40,80,160]]
    falls=[free_fall(dt) for dt in [.002,.001,.0005]]
    friction=dissipative();frictionless=dissipative(0,0)
    inelastic=isolated(restitution=.55)
    checks={
      'isolated_momentum':max(x['momentum_error_kg_m_s'] for x in isolated_rows)<1e-9,
      'isolated_elastic_energy':max(x['energy_relative_error'] for x in isolated_rows)<.05,
      'isolated_overlap':max(x['penetration_m'] for x in isolated_rows)<.001,
      'free_fall_first_order_convergence':falls[-1]['absolute_z_error_m']<.6*falls[-2]['absolute_z_error_m']<.36*falls[0]['absolute_z_error_m'],
      'friction_dissipates':-.01<=friction['ratio']<.2 and friction['max_energy_J']<=1.02*friction['initial_energy_J'],
      'friction_plane_no_fallthrough':friction['max_penetration_m']<.0001 and friction['final_height_m']>.0249,
      'frictionless_energy':abs(frictionless['ratio']-1)<.02,
      'inelastic_combination':abs(inelastic['measured_relative_restitution']-inelastic['expected_combined_restitution'])<.02,
      'isolated_solver_sensitivity':max(max(x['energy_relative_error'] for x in isolated_rows if x['dt']==dt)-min(x['energy_relative_error'] for x in isolated_rows if x['dt']==dt) for dt in [.001,.0005,.00025])<.01
    }
    return {'scope':'analytical_isolated_experiments_only','thresholds':{'momentum':1e-9,'energy_relative':.05,'isolated_penetration_m':.001},
            'checks':checks,'passed':all(checks.values()),'isolated':isolated_rows,
            'free_fall':falls,'friction':friction,'frictionless':frictionless,'inelastic':inelastic}
