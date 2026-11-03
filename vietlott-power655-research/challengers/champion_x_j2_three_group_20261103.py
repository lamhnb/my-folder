#!/usr/bin/env python3
"""Champion-X: grouped sixth-number preference; never predicts lottery balls.
Frozen train 2017-23, later test 2024-26.
Uses Jackpot2/(Jackpot2+First) conditional on five main matches.
"""
import json, hashlib, math, urllib.request, random
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"j2_sixth_group_outputs"
OUT.mkdir(exist_ok=True)
DRAW="https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power655.jsonl"
PRIZE="https://raw.githubusercontent.com/leoodz/vn-vietlott/main/results/power6x55.json"
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Champion-X-Research/1.0"}),timeout=90) as f:return f.read()
def num(v):
    if isinstance(v,dict):v=v.get("count")
    try:return int(str(v).replace(",","").replace(".",""))
    except (ValueError,TypeError):return None
def group(n):
    return 0 if n<=12 else (1 if n<=31 else 2)
def clip(x):return max(1e-9,min(1-1e-9,x))
def loss(data,fn):
    n=sum(r["exposure"] for r in data)
    if n==0:return None
    ll=sum(-r["j2"]*math.log(clip(fn(r)))-r["first"]*math.log(1-clip(fn(r))) for r in data)/n
    brier=sum(r["j2"]*(1-fn(r))**2+r["first"]*fn(r)**2 for r in data)/n
    return {"exposures":n,"draws":len(data),"jackpot2":sum(r["j2"] for r in data),"logloss":ll,"brier":brier}
raw=fetch(DRAW); raw2=fetch(PRIZE)
balls=[json.loads(s) for s in raw.decode().splitlines() if s.strip()]
prizes=json.loads(raw2)
lookup=defaultdict(list)
for r in balls:lookup[r["date"]].append(r)
rows=[];bad=Counter();seen=set()
for item in prizes:
    try:
        date=datetime.strptime(item["date"],"%d-%m-%Y").strftime("%Y-%m-%d")
        main=sorted(map(int,item["numbers"]))
        m=[r for r in lookup.get(date,[]) if sorted(r["result"][:6])==main]
        if len(m)!=1:raise ValueError("no unique match")
        rid=m[0]["id"]
        if rid in seen:raise ValueError("duplicate ID")
        if len(main)!=6 or len(set(main))!=6:raise ValueError("bad main")
        bonus=int(m[0]["result"][6])
        if bonus in main or not 1<=bonus<=55:raise ValueError("bad bonus")
        p=item["prizes"]
        j2=num(p.get("jackpot2"));first=num(p.get("giai_nhat"))
        if None in (j2,first) or min(j2,first)<0 or j2+first<=0:raise ValueError("invalid counts")
        remaining=[n for n in range(1,56) if n not in main]
        opp=[sum(group(n)==g for n in remaining) for g in range(3)]
        assert sum(opp)==49 and opp[group(bonus)]>=1
        rows.append(dict(id=rid,year=int(date[:4]),date=date,main=main,bonus=bonus,
            bonus_group=group(bonus),low_main=sum(n<=31 for n in main),
            opportunities=opp,j2=j2,first=first,exposure=j2+first))
        seen.add(rid)
    except (ValueError,KeyError,TypeError,IndexError) as e:bad[str(e)]+=1
rows.sort(key=lambda x:(x["date"],int(x["id"])))
train=[r for r in rows if r["year"]<=2023];test=[r for r in rows if r["year"]>=2024]
assert len(train)>900 and len(test)>350
def grouped(data):
    ans={}
    for g in range(3):
        ds=[r for r in data if r["bonus_group"]==g]
        j=sum(r["j2"] for r in ds);f=sum(r["first"] for r in ds);n=j+f
        expected=n/49
        ans[["01-12","13-31","32-55"][g]]={
           "draws":len(ds),"jackpot2":j,"first":f,"five_main_exposures":n,
           "observed_probability":j/n if n else None,"uniform_probability":1/49,
           "rate_over_uniform":j/expected if expected else None,
           "mean_opportunities_when_bonus_in_group":sum(r["opportunities"][g] for r in ds)/len(ds) if ds else None}
    return ans

# Fixed training model: group probabilities with mild pseudo-counts centered on uniform.
p0=1/49
trainmean=(sum(r["j2"] for r in train)+.5)/(sum(r["exposure"] for r in train)+1)
shrink=400 # fixed without looking at the test period
pgroup={}
for g in range(3):
    ds=[r for r in train if r["bonus_group"]==g]
    j=sum(r["j2"] for r in ds);n=sum(r["exposure"] for r in ds)
    pgroup[g]=(j+shrink*p0)/(n+shrink)
def evaluate(data):
    uniform=loss(data,lambda r:p0)
    constant=loss(data,lambda r:trainmean)
    category=loss(data,lambda r:pgroup[r["bonus_group"]])
    for key,value in (("constant",constant),("group",category)):
        value["logloss_delta_vs_uniform"]=uniform["logloss"]-value["logloss"]
        value["brier_delta_vs_uniform"]=uniform["brier"]-value["brier"]
    return {"uniform":uniform,"constant":constant,"group":category,
        "rates":grouped(data)}
results={"description":"Inverse ticket distribution: Jackpot2 vs Prize1 with three sixth-number groups",
    "source_sha256":{"balls":hashlib.sha256(raw).hexdigest(),"prizes":hashlib.sha256(raw2).hexdigest()},
    "input":{"ball_rows":len(balls),"prize_rows":len(prizes),"matched":len(rows),"excluded":dict(bad)},
    "reference":{"uniform_p_j2_given_five_mains":p0,
      "group_borders":[[1,12],[13,31],[32,55]],"sixth_number_opportunities_per_draw":49},
    "training_period":"2017-2023","testing_period":"2024-2026",
    "fixed_training_group_probs":{str(k):v for k,v in pgroup.items()},
    "train":evaluate(train),"test":evaluate(test),
    "test_years":{str(y):evaluate([r for r in test if r["year"]==y]) for y in [2024,2025,2026]},
    "limits":"These are five-match ticket category counts and are not exact 6-number ticket frequencies; the low-number hypothesis was previously explored on these years. No new Jackpot-hit prediction; train/test does not make post-hoc hypothesis discovery a virgin OOS study."}
(OUT/"group_heldout.json").write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n")
print("RESULT_JSON="+json.dumps(results,ensure_ascii=False))
