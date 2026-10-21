"""Draw-level conditional nulls. Primary eligibility is separate from code validity."""
import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import beta

ROOT=Path(__file__).resolve().parents[1]
HYPOTHESES=['H1','H2','H3','H4','SPECIAL']

def read_csv(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def write_csv(path,rows):
    with Path(path).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def validate_draw(rows):
    if len(rows)!=7 or sorted(int(r['capture_index']) for r in rows)!=list(range(1,8)):
        raise ValueError('Require exactly one row for each capture 1..7')
    ordered=sorted(rows,key=lambda r:int(r['capture_index']))
    if len({r['draw_id'] for r in rows})!=1 or len({r['source_id'] for r in rows})!=1:
        raise ValueError('Draw/source conflict')
    if len({r['draw_date'] for r in rows})!=1 or len({r['source_sha256'] for r in rows})!=1:
        raise ValueError('Date/source hash conflict')
    if [r['ball_type'] for r in ordered]!=['main']*6+['special']:
        raise ValueError('Special is not exchangeable with six main')
    numbers=[int(r['ball_number']) for r in ordered]
    if len(set(numbers))!=7 or not all(1<=n<=55 for n in numbers):
        raise ValueError('Distinct numbers in 1..55 required')
    times=[float(r['readable_pts_start']) for r in ordered]
    if any(not math.isfinite(t) for t in times) or times!=sorted(set(times)):
        raise ValueError('Source PTS must increase by capture')
    if any(not math.isfinite(float(r['readable_pts_end'])) or float(r['readable_pts_end'])<float(r['readable_pts_start']) for r in ordered):
        raise ValueError('Reversed readable sample bounds')
    return ordered,numbers

def eligible_draws(rows,quality):
    groups=defaultdict(list)
    for r in rows:groups[r['draw_id']].append(r)
    accepted=[];reasons={}
    for draw,group in groups.items():
        try:ordered,nums=validate_draw(group)
        except (ValueError,KeyError) as exc:reasons[draw]=str(exc);continue
        if not all(r['verification_status']=='verified_two_reviews' for r in ordered):
            reasons[draw]='independent_second_review_missing';continue
        if any(r['primary_review'] in ('','NA') or r['secondary_review'] in ('','NA','not_performed') or
               r['secondary_review']==r['primary_review'] for r in ordered):
            reasons[draw]='distinct_independent_reviewers_required';continue
        if quality.get(draw,{}).get('official_result_status')!='verified':
            reasons[draw]='independent_official_result_missing';continue
        accepted.append((draw,ordered[0]['draw_date'],nums))
    accepted.sort(key=lambda x:(x[1],x[0]))
    return accepted,reasons

def position_expected(main):
    counts=np.bincount(np.asarray(main).ravel()-1,minlength=55)
    return np.repeat(counts[:,None]/6,6,axis=1)

def position_stat(main,expected):
    main=np.asarray(main,dtype=int)
    counts=np.zeros((55,6))
    np.add.at(counts,(main.ravel()-1,np.tile(np.arange(6),len(main))),1)
    mask=expected>0
    return float(np.sum(((counts-expected)[mask]**2)/expected[mask]))

def transition_expected(main):
    expected=np.zeros((55,55))
    for row in np.asarray(main,dtype=int):
        ix=row-1
        expected[np.ix_(ix,ix)]+=1/6
    np.fill_diagonal(expected,0)
    return expected

def transition_stat(main,expected):
    main=np.asarray(main,dtype=int)
    counts=np.zeros((55,55))
    np.add.at(counts,(main[:,:-1].ravel()-1,main[:,1:].ravel()-1),1)
    mask=expected>0
    return float(np.sum(((counts-expected)[mask]**2)/expected[mask]))

def temporal_alignment(main):
    a,b=np.array_split(main,2)
    def residual(x):
        e=position_expected(x); c=np.zeros((55,6))
        np.add.at(c,(x.ravel()-1,np.tile(np.arange(6),len(x))),1)
        return (c-e).ravel()
    ra,rb=residual(a),residual(b);den=np.linalg.norm(ra)*np.linalg.norm(rb)
    return float(np.dot(ra,rb)/den) if den else 0.

def remaining(main):
    return np.asarray([sorted(set(range(1,56))-set(map(int,row))) for row in main],dtype=int)

def special_stat(special,remaining49):
    return float(abs(np.sum(np.asarray(special)-remaining49.mean(axis=1))))

def holm(pvalues):
    """Fixed family includes nonexecuted hypotheses as p=1 only internally."""
    order=sorted(pvalues,key=pvalues.get);m=len(order);out={};running=0.
    for rank,key in enumerate(order):
        running=max(running,(m-rank)*pvalues[key]);out[key]=min(1.,running)
    return out

def mc_result(observed,null):
    null=np.asarray(null);k=int(np.count_nonzero(null>=observed-1e-10));b=len(null)
    lo=0. if k==0 else float(beta.ppf(.025,k,b-k+1))
    hi=1. if k==b else float(beta.ppf(.975,k+1,b-k))
    sd=float(null.std(ddof=1));delta=float(observed-null.mean())
    return dict(statistic=float(observed),null_mean=float(null.mean()),null_sd=sd,
                effect_null_centered=delta,effect_null_standardized=delta/sd if sd>1e-12 else 'NA',
                exceedances=k,permutations=b,p_value=(k+1)/(b+1),mc_exceedance_ci_low=lo,mc_exceedance_ci_high=hi)

def monte_carlo(main,special,b=19999,seed=20261021,include_temporal=False):
    main=np.asarray(main,dtype=int)
    if main.ndim!=2 or main.shape[1]!=6 or len(main)==0:raise ValueError('nonempty n x 6 required')
    if b<1:raise ValueError('positive Monte Carlo count required')
    for row in main:
        if len(set(row))!=6 or min(row)<1 or max(row)>55:raise ValueError('invalid main set')
    rem=remaining(main)
    if len(special)!=len(main) or any(int(s) not in r for s,r in zip(special,rem)):
        raise ValueError('special must belong to remaining 49')
    e1,e2=position_expected(main),transition_expected(main)
    observed={'H1':position_stat(main,e1),'H2':transition_stat(main,e2),'SPECIAL':special_stat(special,rem)}
    if include_temporal:observed['H3']=temporal_alignment(main)
    null={k:[] for k in observed};rng=np.random.default_rng(seed)
    for _ in range(b):
        perm=rng.permuted(main,axis=1)
        null['H1'].append(position_stat(perm,e1));null['H2'].append(transition_stat(perm,e2))
        sampled=rem[np.arange(len(rem)),rng.integers(0,49,len(rem))]
        null['SPECIAL'].append(special_stat(sampled,rem))
        if include_temporal:null['H3'].append(temporal_alignment(perm))
    results={k:mc_result(v,null[k]) for k,v in observed.items()}
    corrected=holm({k:results[k]['p_value'] if k in results else 1. for k in HYPOTHESES})
    for k,r in results.items():r['holm_fwer_p']=corrected[k]
    return results

def descriptive_gap(main,seed=20261022):
    per_draw=np.abs(np.diff(np.asarray(main),axis=1)).mean(axis=1)
    out={'mean_absolute_adjacent_gap':float(per_draw.mean()),'ci_low':'NA','ci_high':'NA'}
    if len(main)>=20:
        rng=np.random.default_rng(seed)
        means=per_draw[rng.integers(0,len(main),size=(2000,len(main)))].mean(axis=1)
        out['ci_low'],out['ci_high']=map(float,np.quantile(means,[.025,.975]))
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--pilot-sensitivity',action='store_true');a=p.parse_args()
    rows=read_csv(ROOT/'draw_order_verified.csv');quality={r['draw_id']:r for r in read_csv(ROOT/'quality_audit.csv')}
    accepted,reasons=eligible_draws(rows,quality)
    result=[]
    for hypothesis in HYPOTHESES:
        result.append(dict(hypothesis=hypothesis,analysis_population='primary_verified_only',
            status='not_testable',n_eligible_draws=len(accepted),n_analyzed_draws=0,statistic='NA',effect_size='NA',
            uncertainty='NA',permutations=0,p_value='NA',holm_fwer_p='NA',
            reason='No independently reviewed and officially reconciled draws; expansion/holdout gates not passed' if not accepted else 'Primary historical cohort not yet frozen'))
    # Fail closed. Future primary execution needs a sealed cohort/holdout manifest, not a sample-count override.
    write_csv(ROOT/'order_bias_tests.csv',result)
    (ROOT/'evidence'/'eligibility.json').write_text(json.dumps(dict(accepted=[x[0] for x in accepted],exclusions=reasons,primary_executed=False),indent=2))
    if a.pilot_sensitivity:
        groups=defaultdict(list)
        for r in rows:groups[r['draw_id']].append(r)
        pilot=[validate_draw(groups[draw])[1] for draw in sorted(groups)]
        array=np.asarray(pilot);results=monte_carlo(array[:,:6],array[:,6])
        out=[]
        for hypothesis,r in results.items():
            out.append(dict(hypothesis=hypothesis,analysis_population='provisional_single_reviewer_pilot_only',
                status='exploratory_sensitivity_not_primary',n_draws=len(pilot),seed=20261021,**r,
                effect_ci='NA_n_lt_20',limitation='No independent second review or official numerical reconciliation; no holdout; not predictive evidence'))
        write_csv(ROOT/'pilot_sensitivity.csv',out)
        (ROOT/'evidence'/'pilot_descriptive.json').write_text(json.dumps(descriptive_gap(array[:,:6]),indent=2))
    print(json.dumps(dict(n_eligible=len(accepted),primary_executed=False,pilot_sensitivity=a.pilot_sensitivity)))

if __name__=='__main__':main()
