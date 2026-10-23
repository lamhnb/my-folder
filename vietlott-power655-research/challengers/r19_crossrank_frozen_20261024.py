#!/usr/bin/env python3
"""Frozen research challenger: R19 full ranking crossed with 6 Hybrid6 tickets.

Not a modification of Hybrid6 / Champion. Strict-past replay by input row order.
R19 ranks ALL 19 excluded labels by 30-vs-156 momentum. Each cross comparison
uses the original 19- and 36-label ranks; up to 3 distinct swaps, never cycling.
This score is a heuristic, not a calibrated probability of lottery outcomes.
"""
import argparse
import json
from pathlib import Path
from hybrid6_p3_r3 import predict as hybrid_predict

VERSION = "R19-CROSSRANK-FROZEN-2026-10-24"

def predict(history):
    baseline = hybrid_predict(history)
    tickets = [list(t) for t in baseline["tickets"]]
    selected = {n for ticket in tickets for n in ticket}
    assert len(selected) == 36
    excluded = sorted(set(range(1, 56)) - selected)
    f156 = [0] * 56
    f30 = [0] * 56
    for row in history[-156:]:
        for n in row["result"][:6]:
            f156[n] += 1
    for row in history[-30:]:
        for n in row["result"][:6]:
            f30[n] += 1
    def momentum(n):
        return f30[n] / 30 - f156[n] / 156

    r19 = sorted(excluded, key=lambda n: (-momentum(n), n))
    h36 = sorted(selected, key=lambda n: (-momentum(n), n))
    rpos = {n: j + 1 for j, n in enumerate(r19)}
    hpos = {n: j + 1 for j, n in enumerate(h36)}
    used_in, used_out, swaps = set(), set(), []

    for _ in range(3):
        options = []
        for n in r19:
            if n in used_in:
                continue
            for j, ticket in enumerate(tickets):
                for old in ticket:
                    if old in used_out or old in used_in:
                        continue
                    score = (20 - rpos[n]) / 19 - (37 - hpos[old]) / 36
                    options.append((score, j, n, old))
        if not options:
            break
        # Descending score, then ticket index, entering label, leaving label.
        score, j, n, old = sorted(options, key=lambda x: (-x[0], x[1], x[2], x[3]))[0]
        if score <= 0:
            break
        used_in.add(n)
        used_out.add(old)
        tickets[j][tickets[j].index(old)] = n
        swaps.append({"ticket": j + 1, "out": old, "in": n, "score": score})
    final = [sorted(t) for t in tickets]
    assert len(final) == 6 and all(len(t) == 6 for t in final)
    assert len(set(n for t in final for n in t)) == 36
    assert all(s["in"] in excluded and s["out"] in selected for s in swaps)
    return {"baseline": baseline["tickets"], "final": final,
            "r19_ranking": r19, "h36_ranking": h36, "swaps": swaps}

def replay(rows, first=156, last=None):
    last = len(rows) - 1 if last is None else min(last, len(rows) - 1)
    if first < 156:
        raise ValueError("At least 156 past draws required")
    records = []
    for i in range(first, last + 1):
        p = predict(rows[:i])
        actual = set(rows[i]["result"][:6])
        def score(tickets):
            hits = [len(actual.intersection(t)) for t in tickets]
            return {"coverage": sum(hits), "best": max(hits), "hits": hits,
                    "histogram": None}
        b = score(p["baseline"])
        c = score(p["final"])
        records.append({"index": i, "id": rows[i]["id"], "date": rows[i]["date"],
                        "winning": sorted(actual), "baseline": b, "crossrank": c, **p})
    def summary(field):
        h = [sum(r[field]["best"] == x for r in records) for x in range(7)]
        return {"coverage": sum(r[field]["coverage"] for r in records),
                "best_hit_sum": sum(r[field]["best"] for r in records),
                "histogram": h, "ge3": sum(h[3:]), "ge4": sum(h[4:]),
                "ge5": sum(h[5:]), "ge6": h[6]}
    return {"version": VERSION, "rows": len(rows), "draws": len(records),
            "first_index": first, "last_index": last,
            "baseline": summary("baseline"), "crossrank": summary("crossrank"),
            "records": records}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="chronological JSONL, including special number")
    ap.add_argument("--output", required=True)
    ap.add_argument("--first", type=int, default=156)
    ap.add_argument("--last", type=int, default=None)
    a = ap.parse_args()
    rows = [json.loads(x) for x in Path(a.data).read_text(encoding="utf8").splitlines() if x.strip()]
    for row in rows:
        main_six = row["result"][:6]
        if len(main_six) != 6 or len(set(main_six)) != 6 or not all(isinstance(n, int) and 1 <= n <= 55 for n in main_six):
            raise ValueError("Invalid main numbers: " + str(row.get("id")))
    result = replay(rows, a.first, a.last)
    Path(a.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(json.dumps({k: result[k] for k in ("version", "draws", "baseline", "crossrank")}, indent=2))

if __name__ == "__main__":
    main()
