#!/usr/bin/env python3
"""Champion-X anti-crowd validation: train 2017-2023 / test 2024-2026.
Research only: does NOT predict draw numbers or assert exact-ticket popularity.
"""
import csv, hashlib, json, math, re, urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"anticrowd_validation_outputs"
OUT.mkdir(exist_ok=True)
URL_BALLS="https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power655.jsonl"
URL_PRIZES="https://raw.githubusercontent.com/leoodz/vn-vietlott/main/results/power6x55.json"

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Champion-X-research/1.0"}),timeout=75) as f:
        return f.read()
def value(x):
    if isinstance(x,dict):x=x.get("count")
    if x is None:return None
    s=str(x).strip().replace(",","").replace(".","")
    try:return int(s)
    except ValueError:return None

ballsraw=fetch(URL_BALLS)
prizeraw=fetch(URL_PRIZES)
balls=[json.loads(l) for l in ballsraw.decode().splitlines() if l.strip()]
prizes=json.loads(prizeraw)
assert isinstance(prizes,list)
lookup=defaultdict(list)
for item in balls:
    if len(item.get("result",[]))>=6:
        lookup[item["date"]].append(item)
rows=[];rejections=defaultdict(int)
for item in prizes:
    try:
        d=datetime.strptime(item["date"],"%d-%m-%Y").strftime("%Y-%m-%d")
        ns=sorted(int(n) for n in item["numbers"])
        if len(ns)!=6 or len(set(ns))!=6 or not all(1<=n<=55 for n in ns):raise ValueError("invalid balls")
        matches=[x for x in lookup[d] if sorted(x["result"][:6])==ns]
        if len(matches)!=1:raise ValueError("unmatched")
        tier=item["prizes"]
        n3=value(tier["giai_ba"]);n4=value(tier["giai_nhi"]);n5=value(tier["giai_nhat"])
        if n3 is None or n3<=0 or n4 is None or n5 is None or not (0<=n5<=n4<=n3):raise ValueError("invalid tiers")
        rows.append(dict(id=matches[0]["id"],date=d,year=int(d[:4]),low31=sum(n<=31 for n in ns),
                         high40=sum(n>=40 for n in ns),adj=sum(ns[i+1]==ns[i]+1 for i in range(5)),
                         number_sum=sum(ns),n3=n3,n4=n4,n5=n5))
    except (KeyError,TypeError,ValueError) as e:
        rejections[str(e)]+=1
rows.sort(key=lambda r:(r["date"],int(r["id"])))
seen=set();clean=[]
for r in rows:
    if r["id"] in seen:
        rejections["duplicate"]+=1;continue
    seen.add(r["id"]);clean.append(r)
rows=clean
p3=math.comb(6,3)*math.comb(49,3)/math.comb(55,6)
p4=math.comb(6,4)*math.comb(49,2)/math.comb(55,6)
p5=6*48/math.comb(55,6)
for r in rows:
    r["r4"]=(r["n4"]/r["n3"])/(p4/p3)
    r["r5"]=(r["n5"]/r["n3"])/(p5/p3)

train=[r for r in rows if r["year"]<=2023]
test=[r for r in rows if r["year"]>=2024]
assert len(train)>900 and len(test)>250, (len(train),len(test))
def average(a):return sum(a)/len(a)
mu=average([r["r4"] for r in train])
base_x=average([r["low31"] for r in train])
x=[r["low31"]-base_x for r in train]
y=[r["r4"]-mu for r in train]
slope=sum(a*b for a,b in zip(x,y))/sum(a*a for a in x)
# Training-only model, strictly fixed when scoring test.
def predict(r):return mu+slope*(r["low31"]-base_x)
def evalset(a):
    e0=[(r["r4"]-mu)**2 for r in a]
    e1=[(r["r4"]-predict(r))**2 for r in a]
    return {"n":len(a),"mean_actual":average([r["r4"] for r in a]),
            "mse_baseline":average(e0),"mse_low31_model":average(e1),
            "relative_mse_improvement":(average(e0)-average(e1))/average(e0),
            "by_group":{key:{
                "n":len(z),
                "actual_r4":average([r["r4"] for r in z]) if z else None,
                "model_r4":average([predict(r) for r in z]) if z else None}
                for key,z in {"low_0to2":[r for r in a if r["low31"]<=2],
                              "low_3":[r for r in a if r["low31"]==3],
                              "low_4to6":[r for r in a if r["low31"]>=4]}.items()}}
qtrain=evalset(train);qtest=evalset(test)
by_year={str(year):evalset([r for r in test if r["year"]==year]) for year in sorted(set(r["year"] for r in test))}
# Predictive association is with the pattern of already-drawn numbers and prize counts;
# drawing those exact numbers beforehand is still uniformly unlikely under fair lottery.
summary={"purpose":"out-of-time validation for lower-tier popularity, NOT ball prediction",
 "balls_sha256":hashlib.sha256(ballsraw).hexdigest(),
 "prizes_sha256":hashlib.sha256(prizeraw).hexdigest(),
 "input_draws":len(balls),"input_prize_rows":len(prizes),"matched":len(rows),
 "rejections":dict(rejections),"train_years":"2017-2023","test_years":"2024-2026",
 "training_params":{"mean_ratio4":mu,"mean_low31":base_x,"slope_per_extra_low31":slope},
 "train":qtrain,"test":qtest,"test_by_year":by_year,
 "null":"the probability of any exact 6/55 combination stays 1/C(55,6)"}
(OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
with (OUT/"predictions.csv").open("w",newline="") as f:
    w=csv.writer(f);w.writerow(["id","date","partition","low31","observed_normalized_4to3","predicted_normalized_4to3"])
    for r in rows:w.writerow([r["id"],r["date"],"train" if r["year"]<=2023 else "test",r["low31"],r["r4"],predict(r)])
print("RESULT_JSON="+json.dumps(summary,ensure_ascii=False))
