#!/usr/bin/env python3
"""Research only: measure if predeclared aesthetic-pattern features add out-of-year
prediction of aggregate prize 4/3 concentration beyond birthday-range count.
This is NOT an estimator of the popularity of any exact six-number ticket.
"""
import json,math,hashlib,urllib.request
from collections import defaultdict,Counter
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"anticrowd_geometry_outputs"
OUT.mkdir(exist_ok=True)
DRAW_URL="https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power655.jsonl"
PRIZE_URL="https://raw.githubusercontent.com/leoodz/vn-vietlott/main/results/power6x55.json"
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Champion-X-Research/1.0"}),timeout=75) as r:return r.read()
def ct(v):
    if isinstance(v,dict):v=v.get("count")
    try:return int(str(v).replace(",","").replace(".",""))
    except (TypeError,ValueError):return None
def solve(A,b):
    n=len(b);z=[row[:]+[y] for row,y in zip(A,b)]
    for i in range(n):
        piv=max(range(i,n),key=lambda k:abs(z[k][i]))
        z[i],z[piv]=z[piv],z[i]
        if abs(z[i][i])<1e-10:raise ArithmeticError("singular")
        v=z[i][i]
        for j in range(i,n+1):z[i][j]/=v
        for k in range(n):
            if k==i:continue
            c=z[k][i]
            for j in range(i,n+1):z[k][j]-=c*z[i][j]
    return [r[-1] for r in z]
def features(ns):
    n=sorted(ns);gaps=[n[i+1]-n[i] for i in range(5)]
    mg=sum(gaps)/5
    return {"low31":sum(x<=31 for x in n),
      "adjacent":sum(z==1 for z in gaps),
      "gap_variance":sum((z-mg)**2 for z in gaps)/5,
      "number_sum":sum(n),
      "odd":sum(x%2 for x in n),
      "multiples5":sum(x%5==0 for x in n),
      "edge":sum(x<=6 or x>=50 for x in n)}
raw=fetch(DRAW_URL);rawp=fetch(PRIZE_URL)
draws=[json.loads(x) for x in raw.decode().splitlines() if x.strip()]
prizes=json.loads(rawp)
lookup=defaultdict(list)
for r in draws:lookup[r["date"]].append(r)
rows=[];invalid=Counter();seen=set()
for p in prizes:
    try:
        date=datetime.strptime(p["date"],"%d-%m-%Y").strftime("%Y-%m-%d")
        ns=sorted(int(x) for x in p["numbers"])
        poss=[r for r in lookup.get(date,[]) if sorted(r["result"][:6])==ns]
        if len(poss)!=1 or len(ns)!=6 or len(set(ns))!=6:raise ValueError("unmatched")
        id=poss[0]["id"]
        if id in seen:raise ValueError("duplicate")
        n3=ct(p["prizes"].get("giai_ba"));n4=ct(p["prizes"].get("giai_nhi"))
        if n3 is None or n3<=0 or n4 is None or not 0<=n4<=n3:raise ValueError("invalid tiers")
        row={"id":id,"date":date,"year":int(date[:4]),"n3":n3,"n4":n4,**features(ns)}
        rows.append(row);seen.add(id)
    except (KeyError,TypeError,ValueError,IndexError) as ex:invalid[str(ex)]+=1
p3=math.comb(6,3)*math.comb(49,3)/math.comb(55,6)
p4=math.comb(6,4)*math.comb(49,2)/math.comb(55,6)
for r in rows:r["target"]=(r["n4"]/r["n3"])/(p4/p3)
train=[r for r in rows if r["year"]<=2023]
test=[r for r in rows if r["year"]>=2024]
assert len(train)>900 and len(test)>350,(len(train),len(test))
def mean(x):return sum(x)/len(x)
base=mean([r["target"] for r in train])
low_features=["low31"]
geometry_features=["low31","adjacent","gap_variance","number_sum","odd","multiples5","edge"]
def train_model(keys):
    mus={k:mean([r[k] for r in train]) for k in keys}
    scales={k:max(1e-8,math.sqrt(mean([(r[k]-mus[k])**2 for r in train]))) for k in keys}
    def vector(r):return [1.0]+[(r[k]-mus[k])/scales[k] for k in keys]
    X=[vector(r) for r in train];y=[r["target"] for r in train];d=len(keys)+1
    H=[[sum(v[i]*v[j] for v in X) for j in range(d)] for i in range(d)]
    rhs=[sum(v[i]*yy for v,yy in zip(X,y)) for i in range(d)]
    # Fixed regularizer: 20 pseudo observations per standardized feature, no OOS tuning
    for j in range(1,d):H[j][j]+=20
    beta=solve(H,rhs)
    return lambda r:sum(a*b for a,b in zip(beta,vector(r))),{"variables":keys,"coefficients":beta,"center":mus,"scale":scales}
p_low,c_low=train_model(low_features)
p_geo,c_geo=train_model(geometry_features)
def metric(group):
    pred={"constant":lambda r:base,"low31":p_low,"geometry":p_geo}
    out={}
    for name,fn in pred.items():
        err=[(r["target"]-fn(r))**2 for r in group]
        mae=[abs(r["target"]-fn(r)) for r in group]
        out[name]={"mse":mean(err),"mae":mean(mae),"mean_prediction":mean([fn(r) for r in group])}
    out["size"]=len(group)
    out["geometry_skill_vs_constant"]=1-out["geometry"]["mse"]/out["constant"]["mse"]
    out["geometry_skill_vs_low31"]=1-out["geometry"]["mse"]/out["low31"]["mse"]
    out["low31_skill_vs_constant"]=1-out["low31"]["mse"]/out["constant"]["mse"]
    return out
result={"description":"Aggregate prize-tier ratio geometry test, not exact-six ticket probability",
 "source_sha256":{"draws":hashlib.sha256(raw).hexdigest(),"prizes":hashlib.sha256(rawp).hexdigest()},
 "counts":{"draws":len(draws),"prizes":len(prizes),"matched":len(rows),"training":len(train),"testing":len(test),"invalid":dict(invalid)},
 "training_years":"2017-2023","test_years":"2024-2026",
 "models":{"constant":base,"low31":c_low,"geometry":c_geo},
 "train":metric(train),"test":metric(test),
 "test_years":{str(year):metric([r for r in test if r["year"]==year]) for year in (2024,2025,2026)},
 "limitations":["Post-draw prize-tier ratios are not individual purchase logs.","A multivariate geometry score cannot be safely interpreted as exact-ticket duplicate-holder probability.","No impact on fair ball draw probabilities.","These years were already used to explore player choice; treat results as later-year model scoring, not virgin hypothesis confirmation."]}
(OUT/"results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print("RESULT_JSON="+json.dumps(result,ensure_ascii=False))
