#!/usr/bin/env python3
"""Research-only S3 source policy; DO NOT modify Hybrid6/R19 Frozen.

Given a strict-past Hybrid6 baseline, generate top-3 excluded Momentum and top-3
excluded longest-gap candidates, union them, then choose 3 using ascending rolling historical source hit-rate.
IMPORTANT: this reproduces the EXPLORATORY S3=222 observed in chat;
it is an inverted historical-rate policy, NOT a validated predictor. This predicts candidates only; it DOES NOT issue six tickets.
"""
import argparse
import json
from pathlib import Path
from hybrid6_p3_r3 import predict as hybrid_predict

VERSION = "S3-SOURCE-POLICY-RESEARCH-2026-10-24-V1"
WINDOW = 312
PRIOR_HITS = 6
PRIOR_TRIALS = 55

def candidates(history):
    assert len(history) >= 156
    selected = set(sum(hybrid_predict(history)["tickets"], []))
    excluded = sorted(set(range(1, 56)) - selected)
    f156, f30 = [0] * 56, [0] * 56
    for draw in history[-156:]:
        for n in draw["result"][:6]:
            f156[n] += 1
    for draw in history[-30:]:
        for n in draw["result"][:6]:
            f30[n] += 1
    def mom(n):
        return f30[n] / 30 - f156[n] / 156
    def gap(n):
        for j, draw in enumerate(reversed(history[-156:]), 1):
            if n in draw["result"][:6]:
                return j
        return 157
    M = sorted(excluded, key=lambda n: (-mom(n), n))[:3]
    G = sorted(excluded, key=lambda n: (-gap(n), n))[:3]
    union = list(dict.fromkeys(M + G))
    # A label in both sources belongs to source 2 (overlap), excluded from
    # M-only and G-only historical rate denominators.
    labels = [
        {"n": n, "source": 2 if n in M and n in G else 0 if n in M else 1,
         "rank": (M.index(n) + 1) if n in M else (G.index(n) + 1),
         "f30": f30[n], "f156": f156[n], "gap": gap(n)}
        for n in union
    ]
    return {"momentum_top3": M, "gap_long_top3": G, "union": union,
            "labels": labels}

def predict_at(rows, target_index):
    """Only rows[:target_index] are available at prediction time."""
    if target_index < 157:
        raise ValueError("Need at least one labeled historical candidate draw")
    current = candidates(rows[:target_index])
    counters = {0: [0, 0], 1: [0, 0]}
    for t in range(max(156, target_index - WINDOW), target_index):
        earlier = candidates(rows[:t])
        winners = set(rows[t]["result"][:6])
        for candidate in earlier["labels"]:
            src = candidate["source"]
            if src in counters:
                counters[src][0] += int(candidate["n"] in winners)
                counters[src][1] += 1
    probabilities = {
        src: (hits + PRIOR_HITS) / (trials + PRIOR_TRIALS)
        for src, (hits, trials) in counters.items()
    }
    def key(c):
        # Historical S3 V1 behavior: prefer LOWER historical source hit rate.\n        # This counterintuitive ordering is intentional to reproduce 222.\n        # Overlap source 2 receives the G rate.
        return (probabilities[0 if c["source"] == 0 else 1],
                c["rank"], c["n"])
    picks = [c["n"] for c in sorted(current["labels"], key=key)[:3]]
    return {**current, "selected_three": picks,
            "source_rates": probabilities,
            "version": VERSION}

def replay(rows, first=789, last=1412):
    totals = {"count": 0, "hits": 0, "quarters": [0, 0, 0, 0]}
    records = []
    for i in range(first, last + 1):
        result = predict_at(rows, i)
        hit = len(set(result["selected_three"]) & set(rows[i]["result"][:6]))
        totals["count"] += 1
        totals["hits"] += hit
        totals["quarters"][(i - first) // 156] += hit
        records.append({"id": rows[i]["id"], "selected_three": result["selected_three"],
                        "hits": hit})
    return {"version": VERSION, "totals": totals, "records": records}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--first", type=int, default=789)
    ap.add_argument("--last", type=int, default=1412)
    args = ap.parse_args()
    rows = [json.loads(s) for s in Path(args.data).read_text(encoding="utf-8").splitlines() if s.strip()]
    result = replay(rows, args.first, args.last)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["totals"])
