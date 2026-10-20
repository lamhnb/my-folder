#!/usr/bin/env python3
"""Frequency-only A1 Stride baseline v1.0.0, strict-past replay."""
import argparse,json
from pathlib import Path
def read(path):
    rows=[json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
    ids=set();previous=""
    for row in rows:
        a=row["result"][:6]
        if len(a)!=6 or len(set(a))!=6 or any(type(n)!=int or not 1<=n<=55 for n in a):raise ValueError("Invalid draw")
        if row["id"] in ids or row["date"]<previous:raise ValueError("Duplicate or unsorted")
        ids.add(row["id"]);previous=row["date"]
    return rows
def predict(history,window=0):
    sample=history[-window:] if window else history
    c=[0]*56
    for row in sample:
        for n in row["result"][:6]:c[n]+=1
    rank=sorted(range(1,56),key=lambda n:(-c[n],n))[:36]
    tickets=[sorted(rank[j::6]) for j in range(6)]
    assert len(set(n for a in tickets for n in a))==36
    return tickets
def replay(rows,start_date="2025-10-20",end_date="2026-10-20",window=0):
    report=[]
    for i,row in enumerate(rows):
        if not start_date<=row["date"]<=end_date:continue
        tickets=predict(rows[:i],window)
        target=set(row["result"][:6])
        hits=[len(target.intersection(a)) for a in tickets]
        report.append({"id":row["id"],"date":row["date"],"tickets":tickets,"hits":hits,"best":max(hits),"coverage":sum(hits)})
    return {"version":"A1-1.0.0","window":window,"draws":len(report),
            "ge3":sum(x["best"]>=3 for x in report),"ge4":sum(x["best"]>=4 for x in report),
            "mean_best":sum(x["best"] for x in report)/len(report),
            "coverage":sum(x["coverage"] for x in report),"replay":report}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--data",required=True);p.add_argument("--window",type=int,default=0);p.add_argument("--output",default="a1_results.json")
    a=p.parse_args();r=replay(read(a.data),window=a.window)
    Path(a.output).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding="utf-8")
    print({k:r[k] for k in ("version","draws","ge3","ge4","mean_best","coverage")})
