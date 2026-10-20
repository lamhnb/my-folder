#!/usr/bin/env python3
"""C50 v1.0.0: equal-weight normalized all-history and rolling-156 frequency, six disjoint stride tickets."""
import argparse,json
from pathlib import Path
def load(path):
    rows=[json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]
    last="";seen=set()
    for r in rows:
        a=r["result"][:6]
        if len(a)!=6 or len(set(a))!=6 or any(type(n)!=int or not 1<=n<=55 for n in a):raise ValueError("Invalid draw")
        if r["date"]<last or r["id"] in seen:raise ValueError("Unsorted or duplicate draw")
        last=r["date"];seen.add(r["id"])
    return rows
def predict(history,window=156):
    if not history:raise ValueError("Need prior draws")
    all_counts=[0]*56;recent=[0]*56
    for r in history:
        for n in r["result"][:6]:all_counts[n]+=1
    for r in history[-window:]:
        for n in r["result"][:6]:recent[n]+=1
    n=len(history);w=min(window,n)
    ranked=sorted(range(1,56),key=lambda x:(-(.5*all_counts[x]/n+.5*recent[x]/w),x))[:36]
    tickets=[sorted(ranked[j::6]) for j in range(6)]
    assert len(set(sum(tickets,[])))==36
    return tickets
def replay(rows,start="2024-10-19",end="2026-10-20"):
    results=[]
    for i,row in enumerate(rows):
        if not start<=row["date"]<=end:continue
        tickets=predict(rows[:i])
        actual=set(row["result"][:6])
        hits=[len(actual.intersection(t)) for t in tickets]
        results.append({"id":row["id"],"date":row["date"],"tickets":tickets,"hits":hits,"best":max(hits),"coverage":sum(hits)})
    return {"version":"C50-1.0.0","draws":len(results),"ge3":sum(r["best"]>=3 for r in results),
            "ge4":sum(r["best"]>=4 for r in results),
            "mean_best":sum(r["best"] for r in results)/len(results),
            "records":results,"next_tickets":predict(rows)}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--data",required=True);p.add_argument("--output",default="c50_results.json")
    a=p.parse_args();result=replay(load(a.data))
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print({k:result[k] for k in ("version","draws","ge3","ge4","mean_best")})
