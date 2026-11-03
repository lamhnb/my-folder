#!/usr/bin/env python3
"""Power 6/55: infer sixth-ball number preference from Jackpot2 / Prize1.
Draw-level grouped binomial with exact 1:48 expected jackpot2/prize1 under uniform tickets.
Research-only; winning draw is independent of ticket popularity under the null.
"""
import hashlib,json,math,random,urllib.request
from collections import Counter,defaultdict
from datetime import datetime
from pathlib import Path
BASE=Path(__file__).resolve().parent
OUT=BASE/"j2_sixth_number_outputs";OUT.mkdir(exist_ok=True)
DRAW_URL="https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power655.jsonl"
PRIZE_URL="https://raw.githubusercontent.com/leoodz/vn-vietlott/main/results/power6x55.json"
def fetch(u):
    req=urllib.request.Request(u,headers={"User-Agent":"Champion-X-research/1.0"})
    with urllib.request.urlopen(req,timeout=75) as f:return f.read()
def ct(v):
    if isinstance(v,dict):v=v.get("count")
    try:return int(str(v).strip().replace(",","").replace(".",""))
    except (ValueError,TypeError):return None
drawdata=fetch(DRAW_URL);prizedata=fetch(PRIZE_URL)
draws=[json.loads(v) for v in drawdata.decode().splitlines() if v.strip()]
payouts=json.loads(prizedata)
lookup=defaultdict(list)
for r in draws:lookup[r["date"]].append(r)
rows=[];reasons=Counter();seen=set()
for r in payouts:
    try:
        dt=datetime.strptime(r["date"],"%d-%m-%Y").strftime("%Y-%m-%d")
        wins=sorted(int(x) for x in r["numbers"])
        found=[z for z in lookup.get(dt,[]) if sorted(z["result"][:6])==wins]
        if len(found)!=1:raise ValueError("unmatched date and balls")
        id=found[0]["id"]
        if id in seen:raise ValueError("duplicate draw")
        b=int(found[0]["result"][6])
        if not 1<=b<=55 or b in wins:raise ValueError("invalid bonus")
        p=r["prizes"]
        j2=ct(p.get("jackpot2"));first=ct(p.get("giai_nhat"))
        second=ct(p.get("giai_nhi"));third=ct(p.get("giai_ba"))
        if None in (j2,first,second,third) or any(x<0 for x in (j2,first,second,third)) or third<=0:raise ValueError("missing tiers")
        if j2+first==0:raise ValueError("no 5-main prize exposure")
        if first>second or second>third:raise ValueError("impossible prize ordering")
        rows.append({"id":id,"date":dt,"year":int(dt[:4]),"bonus":b,"low_bonus":int(b<=31),"day_bonus":int(b<=12),
            "low_main":sum(x<=31 for x in wins),"j2":j2,"first":first,
            "n5":j2+first,"third":third})
        seen.add(id)
    except (KeyError,ValueError,TypeError,IndexError) as e:reasons[str(e)]+=1
rows.sort(key=lambda r:(r["date"],int(r["id"])))
assert len(rows)>1100,(len(rows),reasons)
P0=1/49

def stats(z):
    J=sum(r["j2"] for r in z);F=sum(r["first"] for r in z);N=J+F
    p=J/N if N else None
    expected=N*P0
    se=math.sqrt(N*P0*(1-P0))
    return {"draws":len(z),"j2":J,"first":F,"n5":N,
       "observed_p":p,"null_p":P0,"observed_j2_to_first":J/F if F else None,
       "observed_to_uniform_j2_ratio":J/expected if expected else None,
       "expected_j2":expected,"z_to_uniform":(J-expected)/se if se else None}

def by_group(z,key):
    return {str(k):stats([r for r in z if r[key]==k]) for k in sorted({r[key] for r in z})}
def logit(p):return math.log(p/(1-p))
def sigmoid(x):
    if x>=0:return 1/(1+math.exp(-x))
    a=math.exp(x);return a/(1+a)
def fit_group(z):
    # Fit 2 grouped rates with continuity smoothing 1/2 event per group to avoid zero.
    estimates={}
    for k in [0,1]:
        g=[r for r in z if r["low_bonus"]==k]
        J=sum(r["j2"] for r in g);N=sum(r["n5"] for r in g)
        estimates[k]=(J+0.5)/(N+1)
    return estimates
def loss(z,pred):
    # Each count is aggregated logloss/Brier across all 5-match ticket exposures, no trial expansion.
    N=sum(r["n5"] for r in z)
    logloss=-sum(r["j2"]*math.log(pred(r)) +r["first"]*math.log1p(-pred(r)) for r in z)/N
    brier=sum(r["j2"]*(1-pred(r))**2+r["first"]*pred(r)**2 for r in z)/N
    return {"n_exposures":N,"j2":sum(r["j2"] for r in z),"logloss":logloss,"brier":brier}
train=[r for r in rows if r["year"]<=2023];test=[r for r in rows if r["year"]>=2024]
assert len(train)>800 and len(test)>250,(len(train),len(test))
trained=fit_group(train)
train_rate=(sum(r["j2"] for r in train)+0.5)/(sum(r["n5"] for r in train)+1)
def metrics(z):
    uniform=loss(z,lambda r:P0)
    constant=loss(z,lambda r:train_rate)
    bonus_group=loss(z,lambda r:trained[r["low_bonus"]])
    for x in [constant,bonus_group]:
        x["logloss_improvement_vs_uniform"]=uniform["logloss"]-x["logloss"]
        x["logloss_improvement_vs_train_rate"]=constant["logloss"]-x["logloss"]
        x["brier_improvement_vs_uniform"]=uniform["brier"]-x["brier"]
    return {"uniform":uniform,"trained_constant":constant,"trained_low_bonus":bonus_group}
summary={
"method":"Power Jackpot2 versus Prize1 conditional on exactly 5 main matches: uniform P(J2|5 matches)=1/49, J2:First=1:48",
"inputs":{"draw_sha256":hashlib.sha256(drawdata).hexdigest(),"prize_sha256":hashlib.sha256(prizedata).hexdigest(),"ball_rows":len(draws),"prize_rows":len(payouts),"matched_valid":len(rows),"rejects":dict(reasons)},
"all":stats(rows),"train":{"stats":stats(train),"by_low_bonus":by_group(train,"low_bonus"),"by_day_bonus":by_group(train,"day_bonus")},
"test":{"stats":stats(test),"by_low_bonus":by_group(test,"low_bonus"),"by_day_bonus":by_group(test,"day_bonus")},
"learned_p_from_train":trained,"train_rate":train_rate,"train_metrics":metrics(train),"test_metrics":metrics(test),
"by_test_year":{str(y):{"stats":stats([r for r in test if r["year"]==y]),"by_low_bonus":by_group([r for r in test if r["year"]==y],"low_bonus")}
                for y in [2024,2025,2026]},
"critical_limitation":"J2 and first are count data about 5-match ticket classes; the jackpot2 ratio tests average bonus preference conditional on a winning 5-subset, NOT the exact popularity of any given six-number combination; data reuse and shared tickets invalidate naive iid significance; no ball prediction."
}
(OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
print("RESULT_JSON="+json.dumps(summary,ensure_ascii=False))
