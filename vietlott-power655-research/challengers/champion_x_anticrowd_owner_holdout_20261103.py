#!/usr/bin/env python3
"""Research-only anti-crowd Jackpot ownership validation.
Train <=2023, evaluate >=2024; no Frozen predictor or future draw features.
The label (other person held winning combo) is post-draw; ball probabilities stay uniform.
"""
import hashlib, json, math, re, urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

OUT=Path(__file__).resolve().parent/"anticrowd_owner_outputs";OUT.mkdir(exist_ok=True)
DRAW_URL="https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power655.jsonl"
PRIZE_URL="https://raw.githubusercontent.com/leoodz/vn-vietlott/main/results/power6x55.json"

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"champion-x-anticrowd/1.0"}),timeout=75) as r:return r.read()
def cnt(v):
    if isinstance(v,dict):v=v.get("count")
    try:return int(str(v).replace(",","").replace(".",""))
    except (ValueError,TypeError):return None
def money(v):
    if isinstance(v,dict):v=v.get("amount")
    s=str(v or "")
    m=re.search(r"(?<![0-9])(?:[0-9]{1,3}[.,]){3,5}[0-9]{3}(?![0-9])",s)
    if m:return int(re.sub(r"[^0-9]","",m.group()))
    if re.fullmatch(r"[0-9]{9,13}",s.strip()):return int(s.strip())
    return None
def sigmoid(z):
    if z>0:return 1/(1+math.exp(-z))
    x=math.exp(z);return x/(1+x)
def solve(a,b):
    A=[list(row)+[v] for row,v in zip(a,b)]
    n=len(b)
    for i in range(n):
        p=max(range(i,n),key=lambda j:abs(A[j][i]));A[i],A[p]=A[p],A[i]
        if abs(A[i][i])<1e-12:raise ArithmeticError("singular")
        d=A[i][i]
        for j in range(i,n+1):A[i][j]/=d
        for k in range(n):
            if k==i:continue
            f=A[k][i]
            for j in range(i,n+1):A[k][j]-=f*A[i][j]
    return [A[i][n] for i in range(n)]
def fit(xs,ys,lam=6.0):
    d=len(xs[0]);beta=[math.log(sum(ys)/(len(ys)-sum(ys)))]+[0]*(d-1)
    for _ in range(55):
        grad=[0.0]*d;hess=[[0.0]*d for _ in range(d)]
        for x,y in zip(xs,ys):
            p=sigmoid(sum(a*b for a,b in zip(beta,x)))
            w=max(1e-10,p*(1-p))
            for i in range(d):
                grad[i]+=(p-y)*x[i]
                for j in range(d):hess[i][j]+=w*x[i]*x[j]
        for j in range(1,d):grad[j]+=lam*beta[j];hess[j][j]+=lam
        shift=solve(hess,grad);beta=[b-u for b,u in zip(beta,shift)]
        if max(abs(u) for u in shift)<1e-9:break
    return beta
def score(y,prob):
    n=len(y);eps=1e-12
    ll=-sum(v*math.log(max(eps,min(1-eps,p)))+(1-v)*math.log(max(eps,min(1-eps,1-p))) for v,p in zip(y,prob))/n
    br=sum((v-p)**2 for v,p in zip(y,prob))/n
    pos=[p for v,p in zip(y,prob) if v];neg=[p for v,p in zip(y,prob) if not v]
    auc=(sum(1 if a>b else (.5 if a==b else 0) for a in pos for b in neg)/(len(pos)*len(neg))) if pos and neg else None
    return {"n":n,"owners":sum(y),"mean_probability":sum(prob)/n,"logloss":ll,"brier":br,"auc":auc}

raw=fetch(DRAW_URL);raw_prizes=fetch(PRIZE_URL)
ball_rows=[json.loads(v) for v in raw.decode().splitlines() if v.strip()]
prize_rows=json.loads(raw_prizes)
look=defaultdict(list)
for r in ball_rows:look[r["date"]].append(r)
matched=[];reject=defaultdict(int)
for q in prize_rows:
    try:
        date=datetime.strptime(q["date"],"%d-%m-%Y").strftime("%Y-%m-%d")
        ns=sorted(int(k) for k in q["numbers"])
        if len(ns)!=6 or len(set(ns))!=6 or not all(1<=z<=55 for z in ns):raise ValueError("invalid balls")
        found=[r for r in look.get(date,[]) if sorted(r["result"][:6])==ns]
        if len(found)!=1:raise ValueError("bad identity")
        p=q["prizes"];owner=cnt(p.get("jackpot1"));n3=cnt(p.get("giai_ba"));n4=cnt(p.get("giai_nhi"));pot=money(p.get("jackpot1"))
        if owner is None or n3 is None or n3<=0 or n4 is None or pot is None or pot<1e9 or pot>1e12:raise ValueError("invalid payout")
        if not 0<=n4<=n3:raise ValueError("invalid tier relation")
        matched.append({"id":int(found[0]["id"]),"date":date,"year":int(date[:4]),"numbers":ns,
           "owner":int(owner>0),"owner_count":owner,"pot":pot,
           "low31":sum(z<=31 for z in ns),"adjacent":sum(ns[i+1]==ns[i]+1 for i in range(5)),
           "sum":sum(ns)})
    except (KeyError,ValueError,TypeError,IndexError) as e:reject[str(e)]+=1
matched.sort(key=lambda x:x["id"])
byid={x["id"]:x for x in matched}
rows=[]
for r in matched:
    prev=byid.get(r["id"]-1)
    if prev is None or prev["date"]>=r["date"]:continue
    r={**r,"prepot":30_000_000_000 if prev["owner"] else prev["pot"]}
    rows.append(r)
train=[r for r in rows if r["year"]<=2023];test=[r for r in rows if r["year"]>=2024]
assert len(train)>900 and len(test)>350,(len(train),len(test))
mean=lambda a:sum(a)/len(a)
potavg=mean([math.log(r["prepot"]/3e10) for r in train]);potsd=(mean([(math.log(r["prepot"]/3e10)-potavg)**2 for r in train]))**.5
loavg=mean([r["low31"] for r in train]);losd=(mean([(r["low31"]-loavg)**2 for r in train]))**.5
adjavg=mean([r["adjacent"] for r in train]);adjsd=(mean([(r["adjacent"]-adjavg)**2 for r in train]))**.5
def vec(r,which):
    pot=(math.log(r["prepot"]/3e10)-potavg)/potsd
    lo=(r["low31"]-loavg)/losd
    adj=(r["adjacent"]-adjavg)/adjsd
    if which=="pot":return [1,pot]
    if which=="pot_low":return [1,pot,lo]
    if which=="pot_low_adj":return [1,pot,lo,adj]
    if which=="low":return [1,lo]
    raise ValueError(which)
base=mean([r["owner"] for r in train])
models={m:fit([vec(r,m) for r in train],[r["owner"] for r in train])
   for m in ("pot","low","pot_low","pot_low_adj")}
def testset(sample):
    ys=[r["owner"] for r in sample];ans={"constant":score(ys,[base]*len(ys))}
    for m,b in models.items():
        ans[m]=score(ys,[sigmoid(sum(x*y for x,y in zip(vec(r,m),b))) for r in sample])
    for model in ans:
        ans[model]["brier_skill_vs_constant"]=1-ans[model]["brier"]/ans["constant"]["brier"]
        ans[model]["logloss_improvement_vs_constant"]=ans["constant"]["logloss"]-ans[model]["logloss"]
    return ans
results={"description":"Jackpot ownership proxy validation, not ball forecast",
 "snapshots":{"draw_sha256":hashlib.sha256(raw).hexdigest(),"prize_sha256":hashlib.sha256(raw_prizes).hexdigest()},
 "counts":{"draws":len(ball_rows),"prize_rows":len(prize_rows),"matched":len(matched),
           "with_lag_pot":len(rows),"train":len(train),"test":len(test),"rejected":dict(reject)},
 "train_years":"2017-2023","test_years":"2024-2026","base_train_owner_rate":base,
 "normalization_train":{"logpot_mean":potavg,"logpot_sd":potsd,"low31_mean":loavg,"low31_sd":losd},
 "model_coefficients":models,"train_metrics":testset(train),"test_metrics":testset(test),
 "test_by_year":{str(y):testset([r for r in test if r["year"]==y]) for y in (2024,2025,2026)},
 "interpretation":"A signal in exact-six owner presence is not a signal about which balls will be drawn; small positive sample, third-party ledger, and reused historical periods."}
(OUT/"owner_holdout.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n")
print("RESULT_JSON="+json.dumps(results,ensure_ascii=False))
