#!/usr/bin/env python3
"""M3 Reverse-3 Momentum research challenger. Not a validated predictive edge."""
import argparse, json
from pathlib import Path

WEIGHTS_19 = [16,16,20,17,22,20,20,20,19,20,18,17,18,20,19,23,22,19,14]
START_INDEX, END_INDEX = 789, 1413  # zero-based, inclusive

def tickets(sequence):
    return [sorted(sequence[j::6]) for j in range(6)]

def predict(history, weights=WEIGHTS_19):
    if len(history) < 156:
        raise ValueError("156 past draws required")
    if len(weights) != 19:
        raise ValueError("19 physical-position weights required")
    f156, f30 = [0]*56, [0]*56
    for row in history[-156:]:
        for n in row["result"][:6]:
            f156[n] += 1
    for row in history[-30:]:
        for n in row["result"][:6]:
            f30[n] += 1
    momentum = lambda n: f30[n]/30 - f156[n]/156
    rank = sorted(range(1,56), key=lambda n: (-f156[n],n))
    removed = sorted(rank[:36], key=lambda n: (momentum(n),f156[n],n))[:2]
    added = sorted(rank[36:], key=lambda n: (-momentum(n),-f156[n],n))[:2]
    adaptive = rank[:]
    for old,new in zip(removed,added):
        adaptive[adaptive.index(old)] = new
    selected = adaptive[:36]
    outside = sorted(set(range(1,56))-set(selected))
    magnum = [n for n,w in sorted(zip(outside,weights),key=lambda x:(-x[1],x[0]))[:6]]
    b1_kept = set(sorted(selected+magnum,key=lambda n:(-f156[n],n))[:36])
    reverse = sorted((n for n in magnum if n not in b1_kept),key=lambda n:(f156[n],n))
    final = selected[:]
    swaps = []
    used = set()
    for n in reverse[:3]:
        options = sorted(((momentum(v),j) for j,v in enumerate(final) if j not in used))
        _,index = options[0]
        used.add(index)
        swaps.append({"out":final[index],"in":n,"slot":index})
        final[index] = n
    assert len(set(final))==36 and len(tickets(final))==6
    return {"tickets":tickets(final),"adaptive_tickets":tickets(selected),
            "magnum_six":magnum,"b1_rejected_magnum":reverse,
            "swaps":swaps,"selected_36":sorted(final)}

def replay(rows, first=START_INDEX, last=END_INDEX):
    hist = [0]*7
    records = []
    for i in range(first,last+1):
        p = predict(rows[:i])
        winning = set(rows[i]["result"][:6])
        hits = [len(winning.intersection(t)) for t in p["tickets"]]
        best = max(hits)
        hist[best] += 1
        records.append({"id":rows[i]["id"],"date":rows[i]["date"],
                        "winning":sorted(winning),"hits":hits,"best":best,**p})
    return {"model":"M3 Reverse-3 Momentum","draws":len(records),
            "best_hit_histogram":hist,"ge3":sum(hist[3:]),
            "ge4":sum(hist[4:]),"ge5":sum(hist[5:]),
            "records":records}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--data",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    rows=[json.loads(line) for line in Path(args.data).read_text(encoding="utf-8").splitlines() if line.strip()]
    result=replay(rows)
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print({k:result[k] for k in ("draws","ge3","ge4","ge5")})
