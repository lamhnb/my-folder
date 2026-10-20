#!/usr/bin/env python3
"""B7-100 ORIGINAL RESEARCH SNAPSHOT v0.1.0.
Reproduces the original 70-trial greedy candidate generator's mixed-coordinate behavior.
Historical research only; DO NOT treat reported 5/6 hits as independently validated.
PRNG is continuous across draws, so replay must start from the same date and order.
"""
import argparse,json
from pathlib import Path
SEED=712345
class LCG:
    def __init__(self,seed=SEED):self.state=seed
    def random(self):
        self.state=(1664525*self.state+1013904223)&0xffffffff
        return self.state/4294967296
def combinations(a,k):
    out=[]
    def walk(s,p):
        if len(p)==k:
            out.append("-".join(map(str,p)));return
        for i in range(s,len(a)-(k-len(p))+1):walk(i+1,p+[a[i]])
    walk(0,[])
    return out
def generate_original(rank,rng,limit=100,trials=70):
    base=rank[:36]
    tickets=[base[j::6] for j in range(6)]
    seen=set();pairs=set();triples=set();quads=set()
    def register(a):
        a=sorted(a);seen.add("-".join(map(str,a)))
        for x in combinations(a,2):pairs.add(x)
        for x in combinations(a,3):triples.add(x)
        for x in combinations(a,4):quads.add(x)
    for a in tickets:register(a)
    while len(tickets)<limit:
        best=None;best_score=-1
        for _ in range(trials):
            pool=list(range(36))
            for j in range(6):
                k=j+int(rng.random()*(36-j))
                pool[j],pool[k]=pool[k],pool[j]
            a=sorted(pool[:6])
            if "-".join(map(str,a)) in seen:continue
            score=(10*sum(x not in quads for x in combinations(a,4))
                  +3*sum(x not in triples for x in combinations(a,3))
                  +sum(x not in pairs for x in combinations(a,2)))
            if score>best_score:best_score=score;best=a
        if best is None:raise RuntimeError("Candidate generation exhausted")
        # Original mixed-coordinate behavior: indices are registered against number-valued seed tickets.
        tickets.append(best)
        register(best)
    # Original return mapping: all candidate arrays mapped as ranking positions.
    # First six original seed tickets were number-valued, so preserve them explicitly.
    return [sorted(a) for a in tickets[:6]]+[sorted(base[i] for i in a) for a in tickets[6:]]
def replay(rows,start="2022-10-15",end="2026-10-20"):
    rows=sorted(rows,key=lambda r:(r["date"],str(r["id"])))
    begin=next(i for i,r in enumerate(rows) if r["date"]>=start)
    if begin<156:raise ValueError("Need 156 preceding draws")
    rng=LCG();counts=[0]*56
    for r in rows[begin-156:begin]:
        for n in r["result"][:6]:counts[n]+=1
    log=[]
    for i in range(begin,len(rows)):
        row=rows[i]
        if row["date"]>end:break
        rank=sorted(range(1,56),key=lambda n:(-counts[n],n))
        tickets=generate_original(rank,rng)
        actual=set(row["result"][:6])
        hits=[len(actual.intersection(a)) for a in tickets]
        log.append({"id":row["id"],"date":row["date"],"best":max(hits),"hits":hits,"tickets":tickets})
        for n in row["result"][:6]:counts[n]+=1
        for n in rows[i-156]["result"][:6]:counts[n]-=1
    return {"version":"B7-100-original-snapshot-v0.1.0","draws":len(log),
            "ge3":sum(x["best"]>=3 for x in log),"ge4":sum(x["best"]>=4 for x in log),
            "ge5":sum(x["best"]>=5 for x in log),"records":log}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--data",required=True);p.add_argument("--output",default="b7_original_results.json")
    a=p.parse_args();rows=[json.loads(line) for line in Path(a.data).read_text(encoding="utf-8").splitlines() if line.strip()]
    result=replay(rows)
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print({k:result[k] for k in ("version","draws","ge3","ge4","ge5")})
