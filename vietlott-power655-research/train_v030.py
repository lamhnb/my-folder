#!/usr/bin/env python3
"""v0.3.0 experimental challenger: true 55-number replacement and pair/triple shrinkage.
Requires draw-level JSONL; see README. No guaranteed predictive advantage.
"""
import argparse,json,random,math
from pathlib import Path
P=6/55
def load(path):
    rows=[json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]
    prev="";ids=set()
    for r in rows:
        d=r["result"][:6]
        if len(d)!=6 or len(set(d))!=6 or any(type(x)!=int or not 1<=x<=55 for x in d):raise ValueError("Invalid draw")
        if r["date"]<prev or r["id"] in ids:raise ValueError("Unsorted or duplicate")
        prev=r["date"];ids.add(r["id"])
    return rows
def scores(rows,t,window):
    ds=rows[max(0,t-window):t] if window else rows[:t]
    counts=[0]*56
    pair=[[0]*56 for _ in range(56)]
    tri={}
    for r in ds:
        d=sorted(r["result"][:6])
        for x in d:counts[x]+=1
        for i,x in enumerate(d):
            for j in range(i+1,6):
                y=d[j];pair[x][y]+=1;pair[y][x]+=1
                for z in d[j+1:]:
                    k=(x,y,z);tri[k]=tri.get(k,0)+1
    n=len(ds)
    prob=[0]+[(counts[i]+20*P)/(n+20) for i in range(1,56)]
    return prob,pair,tri,n
def optimize(rows,t,window=60,alpha=.0005,beta=.0001,overlap=.01,seed=0):
    prob,pair,tri,n=scores(rows,t,window)
    rng=random.Random(seed+t)
    rank=sorted(range(1,56),key=lambda x:(-prob[x],x))
    # Start from 36 distinct numbers, then allow replacement from all 55.
    tickets=[rank[j::6][:6] for j in range(6)]
    def obj(T):
        individual=sum(prob[x] for a in T for x in a)
        pairs=sum(math.log1p(pair[x][y]) for a in T for i,x in enumerate(a) for y in a[i+1:])
        triples=sum(math.log1p(tri.get(tuple(sorted((x,y,z))),0)) for a in T for i,x in enumerate(a) for j,y in enumerate(a) if j>i for z in a[j+1:])
        penalty=sum(len(set(T[i])&set(T[j]))**2 for i in range(6) for j in range(i+1,6))
        return individual+alpha*pairs+beta*triples-overlap*penalty
    best=obj(tickets)
    # Deterministic coordinate ascent; all moves preserve valid six-number tickets.
    for _ in range(2):
        improved=False
        for i in range(6):
            for j in range(6):
                old=tickets[i][j]
                for x in rank:
                    if x==old or x in tickets[i]:continue
                    tickets[i][j]=x
                    val=obj(tickets)
                    if val>best+1e-12:best=val;old=x;improved=True
                    else:tickets[i][j]=old
        if not improved:break
    return [sorted(a) for a in tickets]
def eval_tickets(tickets,row):
    actual=set(row["result"][:6])
    hits=[len(set(a)&actual) for a in tickets]
    return {"best":max(hits),"ge3":int(max(hits)>=3),"ge4":int(max(hits)>=4),"hits":hits}
def run(rows,train=112,holdout=28):
    boundary=len(rows)-holdout
    if boundary-train<365:raise ValueError("Need longer history")
    params=[(60,.0005,.0001,.01),(120,.0005,.0001,.01),(365,.0005,.0001,.01),
            (60,.001,.0002,.005)]
    trained=[]
    for p in params:
        outs=[eval_tickets(optimize(rows,t,*p,seed=19),rows[t]) for t in range(boundary-train,boundary)]
        trained.append({"params":p,"ge3":sum(x["ge3"] for x in outs),"ge4":sum(x["ge4"] for x in outs)})
    selected=max(trained,key=lambda x:(x["ge3"],x["ge4"]))["params"]
    rng=random.Random(20261008)
    replay=[]
    for t in range(boundary,len(rows)):
        # Generate all predictions before revealing this draw.
        challenger=optimize(rows,t,*selected,seed=19)
        nums=rng.sample(range(1,56),36)
        random_t=[nums[j*6:(j+1)*6] for j in range(6)]
        c=eval_tickets(challenger,rows[t]);r=eval_tickets(random_t,rows[t])
        replay.append({"id":rows[t]["id"],"date":rows[t]["date"],"tickets":challenger,
                       "challenger":c,"random":r})
    return {"version":"0.3.0","train":train,"holdout":holdout,"training":trained,
            "selected":selected,"replay":replay,
            "challenger_ge3":sum(x["challenger"]["ge3"] for x in replay),
            "challenger_ge4":sum(x["challenger"]["ge4"] for x in replay),
            "random_ge3":sum(x["random"]["ge3"] for x in replay),
            "next_tickets":optimize(rows,len(rows),*selected,seed=19)}
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",required=True);ap.add_argument("--train-window",type=int,default=112)
    ap.add_argument("--holdout",type=int,default=28);ap.add_argument("--output",default="results_v030.json")
    a=ap.parse_args();out=run(load(a.data),a.train_window,a.holdout)
    Path(a.output).write_text(json.dumps(out,indent=2),encoding="utf-8")
    print(json.dumps({k:out[k] for k in ("version","selected","challenger_ge3","challenger_ge4","random_ge3")}))
