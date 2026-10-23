#!/usr/bin/env python3
"""Hybrid6 Cap2: max two replacements per ticket; experimental challenger."""
import argparse, json
from pathlib import Path
WEIGHTS = [16,16,20,17,22,20,20,20,19,20,18,17,18,20,19,23,22,19,14]
def predict(history):
    if len(history)<156: raise ValueError("Need 156 previous draws")
    f156=[0]*56; f30=[0]*56
    for r in history[-156:]:
        for n in r["result"][:6]: f156[n]+=1
    for r in history[-30:]:
        for n in r["result"][:6]: f30[n]+=1
    mom=lambda n:f30[n]/30-f156[n]/156
    rank=sorted(range(1,56),key=lambda n:(-f156[n],n))
    removed=sorted(rank[:36],key=lambda n:(mom(n),f156[n],n))[:2]
    added=sorted(rank[36:],key=lambda n:(-mom(n),-f156[n],n))[:2]
    adaptive=rank[:36]
    for old,new in zip(removed,added): adaptive[adaptive.index(old)]=new
    outside=sorted(set(range(1,56))-set(adaptive))
    magnum=[n for n,w in sorted(zip(outside,WEIGHTS),key=lambda x:(-x[1],x[0]))[:6]]
    b1_kept=set(sorted(adaptive+magnum,key=lambda n:(-f156[n],n))[:36])
    rejected=sorted((n for n in magnum if n not in b1_kept),key=lambda n:(f156[n],n))
    incoming=list(dict.fromkeys(magnum[:3]+rejected[:3]))
    final=adaptive[:]; used=set(); swaps=[]; ticket_counts=[0]*6
    for n in incoming:
        options=sorted(((mom(v),j) for j,v in enumerate(final) if j not in used and ticket_counts[j%6]<2))
        _,j=options[0]; used.add(j); ticket_counts[j%6]+=1
        swaps.append({"out":final[j],"in":n,"slot":j})
        final[j]=n
    assert len(set(final))==36
    tickets=lambda x:[sorted(x[j::6]) for j in range(6)]
    return {"tickets":tickets(final),"adaptive_tickets":tickets(adaptive),
            "magnum_six":magnum,"rejected_magnum":rejected,"swaps":swaps}
def replay(rows,first=789,last=1412):
    hist=[0]*7; records=[]
    for i in range(first,last+1):
        p=predict(rows[:i]); W=set(rows[i]["result"][:6])
        hits=[len(W.intersection(t)) for t in p["tickets"]]
        best=max(hits); hist[best]+=1
        records.append({"id":rows[i]["id"],"date":rows[i]["date"],"winning":sorted(W),"best":best,"hits":hits,**p})
    return {"model":"HYBRID6-CAP2","histogram":hist,"ge3":sum(hist[3:]),
            "ge4":sum(hist[4:]),"ge5":sum(hist[5:]),"records":records}
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--data",required=True);ap.add_argument("--output",required=True)
    args=ap.parse_args()
    rows=[json.loads(x) for x in Path(args.data).read_text(encoding="utf8").splitlines() if x.strip()]
    result=replay(rows)
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print({k:result[k] for k in ("model","ge3","ge4","ge5")})
