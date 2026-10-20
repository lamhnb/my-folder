#!/usr/bin/env python3
"""Power 6/55 B1 v1.0.0: rolling-156 frequency + six disjoint stride tickets.
Strict-past sequential replay; experimental research, not a proven predictive edge.
"""
import argparse,json
from pathlib import Path
VERSION="B1-1.0.0"
WINDOW=156
def load(path):
    rows=[json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
    seen=set();last=""
    for row in rows:
        d=row["result"][:6]
        if len(d)!=6 or len(set(d))!=6 or any(type(x)!=int or not 1<=x<=55 for x in d):raise ValueError("Invalid draw")
        if row["id"] in seen or row["date"]<last:raise ValueError("Duplicate/unsorted draws")
        seen.add(row["id"]);last=row["date"]
    return rows
def predict(history):
    c=[0]*56
    for row in history[-WINDOW:]:
        for n in row["result"][:6]:c[n]+=1
    ranked=sorted(range(1,56),key=lambda n:(-c[n],n))[:36]
    tickets=[sorted(ranked[j::6]) for j in range(6)]
    assert all(len(t)==6 and len(set(t))==6 for t in tickets)
    assert len(set(n for t in tickets for n in t))==36
    return tickets
def replay(rows,start="2025-10-20",end="2026-10-20"):
    records=[]
    for i,row in enumerate(rows):
        if not start<=row["date"]<=end:continue
        tickets=predict(rows[:i]) # current draw not yet visible
        actual=set(row["result"][:6])
        hits=[len(actual.intersection(t)) for t in tickets]
        records.append({"id":row["id"],"date":row["date"],"tickets":tickets,
                        "hits":hits,"best":max(hits),"coverage":sum(hits)})
    if not records:raise ValueError("No draws in selected date range")
    return {"version":VERSION,"window":WINDOW,"draws":len(records),
            "ge2":sum(x["best"]>=2 for x in records),
            "ge3":sum(x["best"]>=3 for x in records),
            "ge4":sum(x["best"]>=4 for x in records),
            "mean_best":sum(x["best"] for x in records)/len(records),
            "coverage":sum(x["coverage"] for x in records),
            "records":records,"next_tickets":predict(rows)}
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",required=True)
    ap.add_argument("--output",default="frequency_b1_results.json")
    ap.add_argument("--start",default="2025-10-20")
    ap.add_argument("--end",default="2026-10-20")
    a=ap.parse_args()
    report=replay(load(a.data),a.start,a.end)
    Path(a.output).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print({k:report[k] for k in ("version","draws","ge2","ge3","ge4","mean_best","coverage")})
