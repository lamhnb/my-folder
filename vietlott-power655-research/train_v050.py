#!/usr/bin/env python3
"""Power 6/55 v0.5.0: strict-past signal gate and fixed-size probability model.
Research only. Under fair draws, uniform distribution is optimal.
"""
import argparse, json, math
from pathlib import Path

N=55
K=6
P=K/N
BASE=P*(1-P)

def read_data(path):
    rows=[json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
    ids=set();last=""
    for r in rows:
        d=r["result"][:6]
        if len(d)!=6 or len(set(d))!=6 or any(type(x)!=int or not 1<=x<=55 for x in d):
            raise ValueError("Invalid draw")
        if r["id"] in ids or r["date"]<last:raise ValueError("Duplicate or unsorted draw")
        ids.add(r["id"]);last=r["date"]
    return rows

def posterior_weights(rows,t,window=365,prior=250):
    subset=rows[max(0,t-window):t]
    counts=[0]*55
    for r in subset:
        for x in r["result"][:6]:counts[x-1]+=1
    q=[(x+prior*P)/(len(subset)+prior) for x in counts]
    # Positive odds define a conditional Bernoulli distribution with exactly K draws.
    return [v/(1-v) for v in q]

def fixed_size_marginals(weights):
    # Prefix and suffix elementary symmetric polynomials, order <=K.
    prefix=[[0.]*(K+1) for _ in range(N+1)]
    suffix=[[0.]*(K+1) for _ in range(N+1)]
    prefix[0][0]=suffix[N][0]=1.
    for i,w in enumerate(weights):
        prefix[i+1][0]=1.
        for k in range(1,K+1):
            prefix[i+1][k]=prefix[i][k]+w*prefix[i][k-1]
    for i in range(N-1,-1,-1):
        suffix[i][0]=1.
        for k in range(1,K+1):
            suffix[i][k]=suffix[i+1][k]+weights[i]*suffix[i+1][k-1]
    z=prefix[N][K]
    marg=[]
    for i,w in enumerate(weights):
        e=0.
        for a in range(K):
            e+=prefix[i][a]*suffix[i+1][K-1-a]
        marg.append(w*e/z)
    if abs(sum(marg)-K)>1e-8:raise ArithmeticError("Marginals must sum to six")
    return marg

def brier(q,draw):
    actual=set(draw["result"][:6])
    return sum((v-int(i+1 in actual))**2 for i,v in enumerate(q))/N

def gate(rows,t,window=112,threshold=.00005):
    # No information from t or later. Prequential validation on earlier window.
    start=max(365,t-window)
    if start>=t:return False
    gain=0.
    for k in range(start,t):
        q=fixed_size_marginals(posterior_weights(rows,k))
        gain+=BASE-brier(q,rows[k])
    return gain/(t-start)>threshold

def replay(rows,start,end):
    records=[]
    for t in range(start,end):
        enabled=gate(rows,t)
        q=fixed_size_marginals(posterior_weights(rows,t)) if enabled else [P]*N
        # Predict first; only now inspect result[t].
        records.append({"id":rows[t]["id"],"date":rows[t]["date"],
                        "gate_enabled":enabled,"brier":brier(q,rows[t]),
                        "baseline_brier":BASE})
    return {"draws":len(records),"gate_enabled":sum(r["gate_enabled"] for r in records),
            "mean_brier":sum(r["brier"] for r in records)/len(records),
            "uniform_brier":BASE,"records":records}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",required=True)
    ap.add_argument("--output",default="results_v050.json")
    args=ap.parse_args()
    rows=read_data(args.data)
    if len(rows)<1408:raise ValueError("Expected >=1408 historical draws")
    # Fixed historic boundaries: do not select parameters using the final holdout.
    report={"version":"0.5.0","train":replay(rows,1000,1250),
            "validation":replay(rows,1250,1394),
            "holdout":replay(rows,1394,1408)}
    enabled=gate(rows,len(rows))
    probs=fixed_size_marginals(posterior_weights(rows,len(rows))) if enabled else [P]*N
    report["next_forecast"]={"gate_enabled":enabled,"probabilities":probs}
    Path(args.output).write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({k:{m:v[m] for m in ("draws","gate_enabled","mean_brier","uniform_brier")}
                      for k,v in report.items() if k in ("train","validation","holdout")},indent=2))
if __name__=="__main__":main()
