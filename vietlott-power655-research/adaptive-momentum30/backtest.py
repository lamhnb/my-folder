#!/usr/bin/env python3
"""B1 Adaptive Replacement: strict-past rolling frequency challenger.
Usage: python backtest.py data/power655.jsonl
Input JSONL records: {"id":..., "date":..., "result":[six mains, special]}.
"""
import json, sys
from collections import Counter
from pathlib import Path

WINDOW_LONG=156
WINDOW_SHORT=30
START_ID=789
END_ID=1413

def rank_numbers(history):
    counts=Counter(n for draw in history for n in draw["result"][:6])
    return sorted(range(1,56),key=lambda n:(-counts[n],n)),counts

def tickets(ranking):
    return [sorted(ranking[j+6*k] for k in range(6)) for j in range(6)]

def run(rows):
    ids={int(row["id"]):i for i,row in enumerate(rows)}
    outcomes=[]
    for draw_id in range(START_ID,END_ID+1):
        idx=ids[draw_id]
        assert idx>=WINDOW_LONG, "Insufficient past history"
        past=rows[idx-WINDOW_LONG:idx]
        rank,long=rank_numbers(past)
        _,short=rank_numbers(rows[idx-WINDOW_SHORT:idx])
        momentum=lambda n:short[n]/WINDOW_SHORT-long[n]/WINDOW_LONG
        removed=sorted(rank[:36],key=lambda n:(momentum(n),long[n],n))[:2]
        added=sorted(rank[36:],key=lambda n:(-momentum(n),-long[n],n))[:2]
        revised=rank.copy()
        for old,new in zip(removed,added):
            revised[revised.index(old)]=new
        actual=set(rows[idx]["result"][:6])
        def score(ts):
            hits=[len(actual.intersection(t)) for t in ts]
            return max(hits),hits
        b1,b1_hits=score(tickets(rank))
        adaptive,adaptive_hits=score(tickets(revised))
        special=rows[idx]["result"][6]
        jp2=any(len(actual.intersection(t))==5 and special in t for t in tickets(revised))
        outcomes.append(dict(draw_id=draw_id,date=rows[idx]["date"],winning=sorted(actual),special=special,
                             removed=removed,added=added,b1_tickets=tickets(rank),adaptive_tickets=tickets(revised),
                             b1_best=b1,adaptive_best=adaptive,b1_hits=b1_hits,adaptive_hits=adaptive_hits,jackpot2=jp2))
    hist=lambda key:[sum(o[key]==h for o in outcomes) for h in range(7)]
    report=dict(draws=len(outcomes),window_long=WINDOW_LONG,window_short=WINDOW_SHORT,
                baseline_hist=hist("b1_best"),adaptive_hist=hist("adaptive_best"),
                baseline_ge3=sum(o["b1_best"]>=3 for o in outcomes),
                adaptive_ge3=sum(o["adaptive_best"]>=3 for o in outcomes),
                baseline_ge4=sum(o["b1_best"]>=4 for o in outcomes),
                adaptive_ge4=sum(o["adaptive_best"]>=4 for o in outcomes),
                baseline_ge5=sum(o["b1_best"]>=5 for o in outcomes),
                adaptive_ge5=sum(o["adaptive_best"]>=5 for o in outcomes),
                adaptive_jackpot2=sum(o["jackpot2"] for o in outcomes),
                improved=sum(o["adaptive_best"]>o["b1_best"] for o in outcomes),
                worsened=sum(o["adaptive_best"]<o["b1_best"] for o in outcomes),
                tied=sum(o["adaptive_best"]==o["b1_best"] for o in outcomes),
                five_hit_draws=[o["draw_id"] for o in outcomes if o["adaptive_best"]>=5])
    return report,outcomes

if __name__=="__main__":
    if len(sys.argv)<2: raise SystemExit("Usage: python backtest.py power655.jsonl [output_directory]")
    rows=[json.loads(line) for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if line.strip()]
    output=Path(sys.argv[2]) if len(sys.argv)>2 else Path("adaptive_output")
    output.mkdir(parents=True,exist_ok=True)
    report,outcomes=run(rows)
    (output/"summary.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    (output/"per_draw.json").write_text(json.dumps(outcomes,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
