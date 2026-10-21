"""Generate empirical statistics/charts from persisted engine runs, including failures."""
import csv
import json
from collections import Counter,defaultdict
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import binomtest
ROOT=Path(__file__).resolve().parents[1]


def dump(path,data):path.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')


def main_interval(r):
    t=[x['time'] for x in r['captures'][:6]]
    return float(np.mean(np.diff(t))) if len(t)==6 else None


def main():
    groups=defaultdict(dict)
    for path in sorted((ROOT/'results/runs').glob('*.json')):
        name=path.stem.rsplit('_seed',1)[0];r=json.loads(path.read_text());groups[name][r['seed']]=r
    if not groups:raise RuntimeError('No experiments executed')
    plan=json.loads((ROOT/'experiments/protocol.json').read_text())
    expected={(name,seed) for name,seed,updates in plan['jobs']}
    actual={(name,seed) for name,rows in groups.items() for seed in rows}
    if actual!=expected:
        raise RuntimeError(f'Ensemble incomplete or mismatched: {len(actual)}/{len(expected)} persisted jobs. Final statistics are not generated until the plan completes.')
    baseline_runs=[groups['baseline'][s] for s in sorted(groups['baseline'])]
    dump(ROOT/'results/monte_carlo.json',{'config':baseline_runs[0]['config'],'runs':baseline_runs,
         'scope':'same baseline Monte Carlo jobs as the complete sensitivity protocol; not an additional independent sample'})
    summaries=[];events=[]
    for name,rows in groups.items():
        rr=list(rows.values());valid=[r for r in rr if not r['failures']]
        counts=Counter(x for r in rr for x in r['failures'])
        timeout_phases=Counter(r['states'][-1]['phase'] for r in rr if 'incomplete_seven' in r['failures'])
        tt=[x['time'] for r in valid for x in r['captures']]
        intervals=[main_interval(r) for r in valid];intervals=[x for x in intervals if x is not None]
        ci=binomtest(len(valid),len(rr)).proportion_ci(.95)
        rotor_means=[float(np.mean([v[1] for v in r['rotor_samples_time_omega_torque_SI'] if v[0]>=r['config']['ramp_seconds']])) for r in rr]
        summaries.append({'configuration':name,'runs':len(rr),'complete_seven':sum(len(r['captures'])==7 for r in rr),
           'valid_runs':len(valid),'valid_fraction':len(valid)/len(rr),'valid_fraction_exact95_low':float(ci.low),'valid_fraction_exact95_high':float(ci.high),
           'failure_counts':dict(counts),'timeout_phase_counts':dict(timeout_phases),
           'complete_with_other_failure':sum(len(r['captures'])==7 and bool(r['failures']) for r in rr),
           'mean_main_interval_valid_s':float(np.mean(intervals)) if intervals else None,
           'mean_rms_speed_all_m_s':float(np.mean([r['rms_speed_mean_m_s'] for r in rr])),
           'max_penetration_all_m':max(r['max_penetration_m'] for r in rr),
           'requested_omega_rad_s':rr[0]['config']['rpm']*2*np.pi/60,
           'achieved_omega_post_ramp_mean_rad_s':float(np.mean(rotor_means)),
           'achieved_omega_post_ramp_between_seed_sd_rad_s':float(np.std(rotor_means)),
           'mean_seventh_time_valid_s':float(np.mean([r['captures'][6]['time'] for r in valid])) if valid else None})
        for r in rr:
            for e in r['captures']:events.append({'configuration':name,'seed':r['seed'],'valid_run':not r['failures'],
                 'index':e['index'],'role':e['role'],'label':e['label'],'physical_id':e['physical_id'],'time_s':e['time'],
                 **{f'{dim}_m':e['position'][i] for i,dim in enumerate('xyz')},
                 'speed_m_s':float(np.linalg.norm(e['velocity']))})
    with (ROOT/'results/capture_events.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(events[0]));w.writeheader();w.writerows(events)
    dump(ROOT/'results/summary.json',summaries)
    # Exact metamorphic checks, with same seed/config except metadata or insertion order.
    base=groups['baseline'][1000];shift=groups['label_shift'][1000];repeat=groups['repeat'][1000];rev=groups['insertion_reverse'][1000]
    eq=lambda a,b:a['physical_ids']==b['physical_ids'] and [e['time'] for e in a['captures']]==[e['time'] for e in b['captures']]
    label_ok=eq(base,shift) and all(b['label']==1+(a['label']-1+17)%55 for a,b in zip(base['captures'],shift['captures']))
    repeat_ok=eq(base,repeat) and base['final_positions']==repeat['final_positions']
    counts=Counter(e['label'] for r in groups['baseline'].values() for e in r['captures'][:6])
    special=Counter(e['label'] for r in groups['baseline'].values() for e in r['captures'][6:7])
    diagnostics={'exact_label_permutation_passed':label_ok,'same_seed_exact_repeat_passed':repeat_ok,
       'reverse_insertion_same_capture_path':eq(base,rev),'reverse_insertion_main_set_overlap':len(set(base['physical_ids'][:6])&set(rev['physical_ids'][:6])),
       'main_label_counts':{str(i):counts[i] for i in range(1,56)},'special_label_counts':{str(i):special[i] for i in range(1,56)},
       'main_label_capture_total_including_partial_runs':sum(counts.values()),
       'expected_main_count_per_label_conditional_on_capture_total':sum(counts.values())/55,
       'label_count_scope':'all attempted baseline runs, including partial captures in failed runs; timing histograms separately use valid runs only',
       'interpretation':'Different IDs after insertion reversal are numerical sensitivity, not fixed printed-number preference. Random label assignment is independent of packing and body creation.',
       'label_bias_inference':'not_powered; no real-machine bias claim',
       'physical_ensemble_valid':all(not r['failures'] for rr in groups.values() for r in rr.values())}
    # Empirical convergence of two macroscopic summaries, paired seeds. No exact-number criterion.
    convergence=[]
    for name in ['dt_half','dt_double','solver40','solver160','mirror_y']:
        pairs=[(groups['baseline'][s],r) for s,r in groups[name].items()]
        intervals=[(main_interval(a),main_interval(b)) for a,b in pairs]
        intervals=[(a,b) for a,b in intervals if a is not None and b is not None]
        ti=abs(np.mean([b for a,b in intervals])/np.mean([a for a,b in intervals])-1) if intervals else None
        sp=abs(np.mean([b['rms_speed_mean_m_s'] for a,b in pairs])/np.mean([a['rms_speed_mean_m_s'] for a,b in pairs])-1)
        valid=all(not a['failures'] and not b['failures'] for a,b in pairs)
        convergence.append({'configuration':name,'paired_seeds':len(pairs),'complete_main_interval_pairs':len(intervals),
          'mean_interval_relative_change':float(ti) if ti is not None else None,
          'mean_speed_relative_change':float(sp),'all_pairs_physical_valid':valid,
          'engineering_gate_passed':bool(valid and ti is not None and ti<.05 and sp<.15),
          'limitations':'Three paired seeds cannot prove distributional convergence; chaotic capture identity is not a convergence oracle.'})
    diagnostics['convergence']=convergence
    diagnostics['selection_probability_certified']=False
    dump(ROOT/'validation/ensemble_diagnostics.json',diagnostics)
    # Exploratory property diagnostic; reconstruct the exact documented RNG stream.
    # No printed labels or real winning numbers enter this calculation.
    property_diagnostics=[]
    for r in groups['ball_tolerances'].values():
        rng=np.random.default_rng(r['seed']+314159)
        radii=r['config']['ball_radius']+rng.uniform(-.5,.5,55)*r['config']['diameter_tolerance']
        masses=r['config']['ball_mass']+rng.uniform(-1,1,55)*r['config']['mass_tolerance']
        ii=r['physical_ids'][:6]
        property_diagnostics.append({'seed':r['seed'],'valid_run':not r['failures'],'main_count':len(ii),
          'mean_main_mass_minus_all55_kg':float(np.mean(masses[ii])-np.mean(masses)) if ii else None,
          'mean_main_diameter_minus_all55_m':float(np.mean(2*radii[ii])-np.mean(2*radii)) if ii else None})
    dump(ROOT/'results/physical_property_diagnostics.json',{'status':'exploratory_unpowered',
       'scope':'hypothetical properties, randomized anew for each seed; no evidence of actual Vietlott per-label properties',
       'runs':property_diagnostics,'inference':'No per-label bias or forecasting conclusion; only three loading ensembles.'})
    # All paired configurations use all attempted seeds; failures explicitly marked.
    fig,axs=plt.subplots(1,3,figsize=(15,6))
    names=[s['configuration'] for s in summaries];yy=np.arange(len(names))
    axs[0].barh(yy,[s['valid_fraction'] for s in summaries]);axs[0].set(yticks=yy,yticklabels=names,xlim=(0,1.05),xlabel='physically valid fraction (all attempts)')
    axs[1].barh(yy,[s['mean_rms_speed_all_m_s'] for s in summaries]);axs[1].set(yticks=[],xlabel='mean sampled RMS component speed / m s$^{-1}$')
    axs[2].barh(yy,[s['max_penetration_all_m']*1000 for s in summaries]);axs[2].axvline(2,color='red',ls='--');axs[2].set(yticks=[],xlabel='max penetration / mm (threshold 2)')
    fig.suptitle('Hypothetical mechanism: small paired sensitivity sweep, not Vietlott measurements');fig.tight_layout();fig.savefig(ROOT/'charts/sensitivity.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(11,5));xx=np.arange(len(summaries))
    ax.bar(xx-.18,[s['requested_omega_rad_s'] for s in summaries],width=.36,label='requested')
    ax.bar(xx+.18,[s['achieved_omega_post_ramp_mean_rad_s'] for s in summaries],width=.36,label='achieved, simulation',
           yerr=[s['achieved_omega_post_ramp_between_seed_sd_rad_s'] for s in summaries],capsize=2)
    ax.set(xticks=xx,xticklabels=names,ylabel='angular velocity / rad s$^{-1}$',title='Assumed motor: post-ramp tracking under load; not actual Vietlott RPM')
    ax.tick_params(axis='x',labelrotation=75,labelsize=8);ax.legend();fig.tight_layout();fig.savefig(ROOT/'charts/motor_tracking.png',dpi=150);plt.close(fig)
    fig,axs=plt.subplots(1,3,figsize=(14,4))
    baseline_valid_times=[e['time_s'] for e in events if e['configuration']=='baseline' and e['valid_run']]
    shared_time_bins=np.arange(0,max(baseline_valid_times)+2,1.)
    for role,col in [('main','tab:blue'),('special','tab:orange')]:
        vals=[e['time_s'] for e in events if e['configuration']=='baseline' and e['valid_run'] and e['role']==role]
        axs[0].hist(vals,bins=shared_time_bins,alpha=.6,label=role,color=col)
    axs[0].legend();axs[0].set(xlabel='entry time / s',ylabel='captures; correlated within run')
    vv=[e['speed_m_s'] for e in events if e['configuration']=='baseline' and e['valid_run']]
    axs[1].hist(vv,bins=15);axs[1].set(xlabel='speed at trough contact / m s$^{-1}$')
    axs[2].bar(range(1,56),[counts[i] for i in range(1,56)]);axs[2].set(xlabel='randomized printed label',ylabel='main captures (descriptive only)')
    fig.tight_layout();fig.savefig(ROOT/'charts/baseline_distributions.png',dpi=150);plt.close(fig)
    trajectory=ROOT/'results/baseline_seed1000.npz';perturbed=ROOT/'results/jitter_seed1000.npz'
    if trajectory.exists() and perturbed.exists():
        a=np.load(trajectory);b=np.load(perturbed);n=min(len(a['time']),len(b['time']))
        separation=np.sqrt(np.mean(np.sum((a['position'][:n]-b['position'][:n])**2,axis=2),axis=1))
        dump(ROOT/'results/chaos.json',{'initial_perturbation_m':1e-7,'seed':1000,
          'same_capture_sequence':base['physical_ids']==groups['jitter'][1000]['physical_ids'],
          'max_rms_same_ID_separation_m':float(separation.max()),'last_common_sample_separation_m':float(separation[-1]),
          'interpretation':'Finite-time divergence of one pair, not an estimated Lyapunov exponent.'})
        fig,axs=plt.subplots(1,3,figsize=(14,4));axs[0].semilogy(a['time'][:n],np.maximum(separation,1e-12));axs[0].set(xlabel='time / s',ylabel='RMS physical-ID separation / m')
        for j in range(5):axs[1].plot(a['time'],a['position'][:,j,2],alpha=.7)
        axs[1].set(xlabel='time / s',ylabel='z / m (first five physical IDs)')
        speed=np.linalg.norm(a['velocity'],axis=2);axs[2].plot(a['time'],speed.mean(axis=1));axs[2].fill_between(a['time'],np.quantile(speed,.1,axis=1),np.quantile(speed,.9,axis=1),alpha=.2);axs[2].set(xlabel='time / s',ylabel='speed mean and 10–90% / m s$^{-1}$')
        fig.tight_layout();fig.savefig(ROOT/'charts/trajectories_chaos.png',dpi=150);plt.close(fig)
    if trajectory.exists():
        a=np.load(trajectory);tt=a['time'];xyz=a['position'];vv=a['velocity']
        requests=[s for s in base['states'] if s['phase']=='ADMIT'];before=[];active_cloud=[]
        for j,e in enumerate(base['captures']):
            request=requests[j]['time'];k=max(0,np.searchsorted(tt,request-.1)-1);i=e['physical_id']
            captured_before=set(base['physical_ids'][:j]);active=[q for q in range(55) if q not in captured_before]
            active_cloud.extend(xyz[k,active].tolist())
            before.append({'capture_index':j+1,'role':e['role'],'physical_id':i,'request_time_s':request,'sample_time_s':float(tt[k]),
                 'x_m':float(xyz[k,i,0]),'y_m':float(xyz[k,i,1]),'z_m':float(xyz[k,i,2]),'speed_m_s':float(np.linalg.norm(vv[k,i]))})
        with (ROOT/'results/pre_admission_seed1000.csv').open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(before[0]));w.writeheader();w.writerows(before)
        cloud=np.asarray(active_cloud);selected=np.array([[r['x_m'],r['y_m'],r['z_m']] for r in before])
        fig,axs=plt.subplots(1,2,figsize=(10,4))
        for ax,i,j in [(axs[0],0,1),(axs[1],0,2)]:
            ax.scatter(cloud[:,i],cloud[:,j],s=9,alpha=.15,label='all active spheres at seven windows')
            ax.scatter(selected[:,i],selected[:,j],s=38,c='red',label='sphere subsequently captured')
            ax.set(xlabel='xyz'[i]+' / m',ylabel='xyz'[j]+' / m');ax.legend(fontsize=7)
        fig.suptitle('Before admission, one seed1000: correlated snapshots, not independent probability trials')
        fig.tight_layout();fig.savefig(ROOT/'charts/pre_admission_one_seed.png',dpi=150);plt.close(fig)
    # Pre-capture positions: confined by hypothetical pocket, not a hardware inference.
    pre=[q for r in groups['baseline'].values() for q in r['pre_capture']]
    fig,axs=plt.subplots(1,2,figsize=(9,4))
    axs[0].scatter([q['position'][0] for q in pre],[q['position'][1] for q in pre],s=12,alpha=.6);axs[0].set(xlabel='pocket x / m',ylabel='pocket y / m',title='Positions at isolation (all attempts)')
    axs[0].set_xticks([-.008,-.004,0,.004,.008]);axs[0].set_yticks([-.008,-.004,0,.004,.008])
    axs[1].hist([np.linalg.norm(q['velocity']) for q in pre],bins=15);axs[1].set(xlabel='speed at isolation / m s$^{-1}$',title='Hypothetical pocket support')
    fig.tight_layout();fig.savefig(ROOT/'charts/pre_capture.png',dpi=150);plt.close(fig)
    print(json.dumps({'configurations':len(groups),'runs':sum(len(r) for r in groups.values()),'diagnostics':diagnostics},indent=2))

if __name__=='__main__':main()
