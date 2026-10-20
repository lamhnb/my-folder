#!/usr/bin/env python3
"""B7-200 v0.2.0: 200-ticket sequential greedy coverage research generator.
Consistent rank indices (0..35), per-draw deterministic seed, 70 trials for EACH
of 194 added tickets. Six B1 seed tickets remain unchanged.
No claim of forecasting advantage; backtest independently before promotion.
"""
import argparse, json, random
from pathlib import Path
from itertools import combinations

VERSION="B7-200-v0.2.0"
WINDOW=156
SEED=712345
CANDIDATES=200
TRIALS=70

def generate(rank, draw_id, count=CANDIDATES):
    if len(rank)<36: raise ValueError("Ranking must have >=36 unique numbers")
    rng=random.Random(SEED ^ int(draw_id))
    # Every internal ticket uses only rank indices, including the six B1 seeds.
    tickets=[tuple(range(j,36,6)) for j in range(6)]
    seen=set(tickets)
    covered={2:set(),3:set(),4:set(),5:set()}
    def add(ticket):
        for k in covered:
            covered[k].update(combinations(ticket,k))
    for ticket in tickets: add(ticket)
    while len(tickets)<count:
        winner=None;best=-1
        for _ in range(TRIALS):
            trial=tuple(sorted(rng.sample(range(36),6)))
            if trial in seen: continue
            # Marginal coverage measured against ALL tickets already accepted.
            gain=(10*sum(q not in covered[4] for q in combinations(trial,4))
                  +3*sum(q not in covered[3] for q in combinations(trial,3))
                  +sum(q not in covered[2] for q in combinations(trial,2))
                  +sum(q not in covered[5] for q in combinations(trial,5)))
            if gain>best:
                best=gain;winner=trial
        if winner is None: raise RuntimeError("Unable to find distinct candidate")
        tickets.append(winner);seen.add(winner);add(winner)
    assert len(tickets)==count and len(seen)==count
    numbers=[sorted(rank[i] for i in ticket) for ticket in tickets]
    assert len({tuple(t) for t in numbers})==count
    return numbers, {str(k):len(v) for k,v in covered.items()}

def replay(rows,start="2022-10-15",end="2026-10-20"):
    rows=sorted(rows,key=lambda r:(r["date"],int(r["id"])))
    first=next(i for i,r in enumerate(rows) if r["date"]>=start)
    if first<WINDOW:raise ValueError("Insufficient history")
    counts=[0]*56
    for row in rows[first-WINDOW:first]:
        for n in row["result"][:6]: counts[n]+=1
    log=[]
    for i in range(first,len(rows)):
        row=rows[i]
        if row["date"]>end:break
        rank=sorted(range(1,56),key=lambda n:(-counts[n],n))
        tickets,coverage=generate(rank,row["id"])
        actual=set(row["result"][:6])
        hits=[len(actual.intersection(ticket)) for ticket in tickets]
        log.append({"id":row["id"],"date":row["date"],
                    "best6":max(hits[:6]),"best100":max(hits[:100]),
                    "best200":max(hits),"hits":hits,"coverage":coverage,
                    "tickets":tickets})
        for n in row["result"][:6]:counts[n]+=1
        for n in rows[i-WINDOW]["result"][:6]:counts[n]-=1
    return {"version":VERSION,"window":WINDOW,"trials_per_ticket":TRIALS,
            "draws":len(log),"ge5_100":sum(x["best100"]>=5 for x in log),
            "ge5_200":sum(x["best200"]>=5 for x in log),
            "ge4_100":sum(x["best100"]>=4 for x in log),
            "ge4_200":sum(x["best200"]>=4 for x in log),"records":log}
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",required=True)
    ap.add_argument("--output",default="b7_200_replay.json")
    a=ap.parse_args()
    rows=[json.loads(s) for s in Path(a.data).read_text(encoding="utf-8").splitlines() if s.strip()]
    result=replay(rows)
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print({k:v for k,v in result.items() if k!="records"})
