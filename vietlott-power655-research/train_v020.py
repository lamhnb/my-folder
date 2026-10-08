#!/usr/bin/env python3
"""Power 6/55 v0.2.0: strict-past online mixture and constrained portfolio."""
import argparse, json, math, random
from pathlib import Path
P=6/55
WINDOWS=(0,30,60,120,365)
def load(path):
    rows=[json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
    ids=set(); date=""
    for r in rows:
        a=r["result"][:6]
        if len(a)!=6 or len(set(a))!=6 or any(type(n)!=int or not 1<=n<=55 for n in a): raise ValueError("Invalid draw")
        if r["date"]<date or r["id"] in ids: raise ValueError("Unsorted/duplicate draw")
        ids.add(r["id"]);date=r["date"]
    return rows
def features(rows,t):
    data=rows[:t]
    outputs=[]
    for w in WINDOWS:
        ds=data[-w:] if w else data
        c=[0]*56
        for r in ds:
            for n in r["result"][:6]:c[n]+=1
        outputs.append([(c[n]+20*P)/(len(ds)+20) for n in range(1,56)])
    return outputs
def pair_counts(rows,t,window=120):
    c=[[0]*56 for _ in range(56)]
    for r in rows[max(0,t-window):t]:
        a=r["result"][:6]
        for i,x in enumerate(a):
            for y in a[i+1:]:c[x][y]+=1;c[y][x]+=1
    return c
def probabilities(fs,weights):
    return [sum(weights[k]*fs[k][i] for k in range(len(fs))) for i in range(55)]
def make_portfolio(probs,pairs,penalty,seed):
    rng=random.Random(seed)
    ranking=sorted(range(1,56),key=lambda n:(-probs[n-1],n))
    # Candidate pool: top 42 numbers; always six valid, distinct tickets.
    pool=ranking[:42]
    best=None
    for restart in range(3):
        if restart==0:
            t=[sorted(pool[j::6][:6]) for j in range(6)]
        else:
            shuffled=pool[:36];rng.shuffle(shuffled)
            t=[sorted(shuffled[j*6:(j+1)*6]) for j in range(6)]
        def objective(tickets):
            quality=sum(sum(probs[n-1] for n in a) for a in tickets)
            association=sum(sum(pairs[x][y] for i,x in enumerate(a) for y in a[i+1:]) for a in tickets)
            overlap=sum(len(set(tickets[i])&set(tickets[j]))**2 for i in range(6) for j in range(i+1,6))
            return quality+.0008*association-penalty*overlap
        score=objective(t)
        for _ in range(2):
            improved=False
            for i in range(6):
                for j in range(i+1,6):
                    for a in range(6):
                        for b in range(6):
                            t[i][a],t[j][b]=t[j][b],t[i][a]
                            s=objective(t)
                            if s>score+1e-12:score=s;improved=True
                            else:t[i][a],t[j][b]=t[j][b],t[i][a]
            if not improved:break
        if best is None or score>best[0]:best=(score,[sorted(a) for a in t])
    tickets=best[1]
    assert len(tickets)==6 and all(len(a)==6 and len(set(a))==6 for a in tickets)
    return tickets
def evaluate(tickets,actual):
    target=set(actual["result"][:6])
    hits=[len(set(a)&target) for a in tickets]
    return {"hits":hits,"best":max(hits),"ge3":int(max(hits)>=3),"ge4":int(max(hits)>=4)}
def run(rows,train=112,holdout=28,eta=5,seed=17):
    boundary=len(rows)-holdout
    if boundary<train+365:raise ValueError("Insufficient history")
    # Select penalty using only the earlier training window, not holdout.
    penalties=(0,.001,.005,.02)
    candidates=[]
    for pen in penalties:
        success=0;ge4=0;best=0
        for t in range(boundary-train,boundary):
            fs=features(rows,t);pr=probabilities(fs,[.2]*5)
            a=evaluate(make_portfolio(pr,pair_counts(rows,t),pen,seed+t),rows[t])
            success+=a["ge3"];ge4+=a["ge4"];best+=a["best"]
        candidates.append({"penalty":pen,"ge3":success,"ge4":ge4,"best_sum":best})
    selected=max(candidates,key=lambda x:(x["ge3"],x["ge4"],x["best_sum"]))["penalty"]
    weights=[.2]*5;records=[]
    rng=random.Random(seed)
    for t in range(boundary,len(rows)):
        fs=features(rows,t)
        pred=probabilities(fs,weights)
        tickets=make_portfolio(pred,pair_counts(rows,t),selected,seed+t)
        random_nums=rng.sample(range(1,56),36)
        random_tickets=[random_nums[i*6:(i+1)*6] for i in range(6)]
        # Reveal actual only after all predictions are constructed.
        result=evaluate(tickets,rows[t]);baseline=evaluate(random_tickets,rows[t])
        losses=[sum((f[n-1]-(n in rows[t]["result"][:6]))**2 for n in range(1,56))/55 for f in fs]
        before=weights[:]
        weights=[w*math.exp(-eta*loss) for w,loss in zip(weights,losses)]
        total=sum(weights);weights=[w/total for w in weights]
        records.append({"id":rows[t]["id"],"date":rows[t]["date"],"tickets":tickets,
                        "result":result,"random":baseline,"weights_before":before,"weights_after":weights})
    final=make_portfolio(probabilities(features(rows,len(rows)),weights),
                         pair_counts(rows,len(rows)),selected,seed+len(rows))
    return {"version":"0.2.0","train":train,"holdout":holdout,"selected_penalty":selected,
            "training_candidates":candidates,"replay":records,"final_weights":weights,
            "next_tickets":final,
            "holdout_ge3":sum(r["result"]["ge3"] for r in records),
            "random_ge3":sum(r["random"]["ge3"] for r in records)}
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",required=True);ap.add_argument("--train-window",type=int,default=112)
    ap.add_argument("--holdout",type=int,default=28);ap.add_argument("--output",default="results_v020.json")
    args=ap.parse_args()
    report=run(load(args.data),args.train_window,args.holdout)
    Path(args.output).write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps({k:report[k] for k in ("version","selected_penalty","holdout_ge3","random_ge3","next_tickets")}))
