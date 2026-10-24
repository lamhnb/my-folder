#!/usr/bin/env python3
"""Champion-X Phase 1: input sensitivity, RESEARCH ONLY.

The registered Pair-60 and Stride-365 Champions remain untouched.
This pilot probes R19 Frozen as the X0 reference,
by cyclically rotating order of its most recent 156 historical draw rows.
Rotating keeps the exact 156 draw multiset / F156 unchanged but changes F30.
It is a counterfactual robustness probe, NOT a forecastable intervention.

Never use winning data from target/current draw to generate a prediction.
"""
import argparse
import json
import random
from pathlib import Path
from r19_crossrank_frozen_20261024 import predict as r19_predict

VERSION = "CHAMPION-X-R19-BASE-PHASE1-2026-10-25-V2"
OFFSETS = (0, 5, 15, 30, 60, 90)
HISTORY = 156

def rotate_recent_history(history, shift):
    """Counterfactually roll complete rows (no synthetic draw numbers)."""
    if len(history) < HISTORY:
        raise ValueError("156 earlier draws required")
    if not 0 <= shift < HISTORY:
        raise ValueError("shift outside 0..155")
    recent = history[-HISTORY:]
    rolled = recent[shift:] + recent[:shift] if shift else recent[:]
    return history[:-HISTORY] + rolled

def selected_and_tickets(history, shift=0):
    tickets = r19_predict(rotate_recent_history(history, shift))["tickets"]
    selected = {n for ticket in tickets for n in ticket}
    assert len(tickets) == 6 and all(len(t) == 6 for t in tickets)
    assert len(selected) == 36
    return selected, tickets

def metrics(selected, tickets, win):
    hits = [len(set(t) & win) for t in tickets]
    return {"selection": len(selected & win), "best_hit": max(hits),
            "ge3": int(max(hits) >= 3), "ge4": int(max(hits) >= 4),
            "ge5": int(max(hits) >= 5), "ge6": int(max(hits) >= 6)}

def seeded_same_difference_control(base, altered, draw_index, shift):
    """Deterministic random same-sized label exchange from H's 19 excluded labels.

    Matches the candidate's number of changed labels; DOES NOT preserve
    the distribution of the original six tickets (Selection-only control).
    """
    k = len(altered - base)
    rng = random.Random(20261025 + draw_index * 1009 + shift * 31)
    excluded = list(sorted(set(range(1, 56)) - base))
    drops = rng.sample(sorted(base), k)
    adds = rng.sample(excluded, k)
    return (base - set(drops)) | set(adds)

def replay(rows, first=789, last=1412):
    summary = {
        str(shift): {"draws": 0, "selection": 0, "best_hit": 0,
                     "ge3": 0, "ge4": 0, "ge5": 0, "ge6": 0,
                     "changed_labels": 0, "random_matched_selection": 0,
                     "selection_quarters": [0, 0, 0, 0]}
        for shift in OFFSETS
    }
    records = []
    for i in range(first, last + 1):
        history = rows[:i]  # Strict-past; target draw only used for scoring.
        win = set(rows[i]["result"][:6])
        base, _ = selected_and_tickets(history, 0)
        per_draw = {"id": rows[i]["id"], "date": rows[i]["date"],
                    "results": {}}
        for shift in OFFSETS:
            selected, tickets = selected_and_tickets(history, shift)
            delta = len(selected - base)
            control = seeded_same_difference_control(base, selected, i, shift)
            m = metrics(selected, tickets, win)
            s = summary[str(shift)]
            s["draws"] += 1
            s["changed_labels"] += delta
            s["random_matched_selection"] += len(control & win)
            for key in ("selection", "best_hit", "ge3", "ge4", "ge5", "ge6"):
                s[key] += m[key]
            s["selection_quarters"][(i - first) // 156] += m["selection"]
            per_draw["results"][str(shift)] = {
                **m, "changed_labels": delta,
                "added": sorted(selected - base), "removed": sorted(base - selected),
                "random_matched_selection": len(control & win),
            }
        records.append(per_draw)
    return {"version": VERSION, "offsets": list(OFFSETS),
            "window": {"first": first, "last": last},
            "summary": summary, "records": records}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--first", type=int, default=789)
    parser.add_argument("--last", type=int, default=1412)
    args = parser.parse_args()
    rows = [json.loads(line) for line in Path(args.data).read_text(encoding="utf-8").splitlines() if line.strip()]
    if args.first < HISTORY or args.last >= len(rows):
        parser.error("invalid replay window for supplied data")
    report = replay(rows, args.first, args.last)
    Path(args.output).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
