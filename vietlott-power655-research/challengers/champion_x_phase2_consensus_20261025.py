#!/usr/bin/env python3
"""Champion-X Phase 2: strict-past six-state consensus Selection audit.

No Frozen source edits. Requires existing champion_x_input_sensitivity_phase1_20261025.py,
r19_crossrank_frozen_20261024.py, hybrid6_p3_r3.py alongside this file.
"""
import argparse
import collections
import hashlib
import json
import random
from pathlib import Path

from champion_x_input_sensitivity_phase1_20261025 import OFFSETS, selected_and_tickets

GOLDEN_R19 = "a7ebf4fa5216e1bfd4906087e04555044d3e58f0"
GOLDEN_HYBRID = "252f6e0e3dad70a80a4b0cf7febe92d5d080e264"
GOLDEN_DATA = "1230696771274d48b261a0cfbd728444700c299e"
NUMBERS = set(range(1, 56))

def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def verify_sources(data_path, strict_pinned):
    root = Path(__file__).resolve().parent
    files = {"r19_crossrank_frozen_20261024.py": GOLDEN_R19,
             "hybrid6_p3_r3.py": GOLDEN_HYBRID}
    for filename, expected in files.items():
        actual = git_blob((root / filename).read_bytes())
        assert actual == expected, (filename, actual, expected)
    raw = data_path.read_bytes()
    actual_data = git_blob(raw)
    if strict_pinned:
        assert actual_data == GOLDEN_DATA, ("DATA NOT PINNED", actual_data)
    return {"data_blob": actual_data, "data_sha256": hashlib.sha256(raw).hexdigest(),
            "pinned_match": actual_data == GOLDEN_DATA, "source_blobs": files}

def select36(base, votes, descending=True):
    return set(sorted(NUMBERS, key=lambda n: ((-votes[n] if descending else votes[n]), -(n in base), n))[:36])

def matched_random(base, replacements, index, replicate):
    rng = random.Random(20261025 + index * 100003 + replicate * 137)
    drop = set(rng.sample(sorted(base), replacements))
    add = set(rng.sample(sorted(NUMBERS - base), replacements))
    return (base - drop) | add

def run(rows, first, last, reps):
    records = []
    categories = {str(k): {"available": 0, "hits": 0, "x0_missed_hits": 0} for k in range(7)}
    for index in range(first, last + 1):
        states = {offset: selected_and_tickets(rows[:index], offset)[0] for offset in OFFSETS}
        assert all(len(s) == 36 for s in states.values())
        base = states[0]
        winning = set(rows[index]["result"][:6])
        assert len(winning) == 6 and winning <= NUMBERS
        votes = collections.Counter(n for s in states.values() for n in s)
        assert sum(votes.values()) == 216
        groups = {k: {n for n in NUMBERS if votes[n] == k} for k in range(7)}
        for k, members in groups.items():
            c = categories[str(k)]
            c["available"] += len(members)
            c["hits"] += len(members & winning)
            c["x0_missed_hits"] += len((members & winning) - base)
        majority = select36(base, votes)
        minority = select36(base, votes, descending=False)
        policies = {"X0": base, "majority36": majority, "minority36": minority}
        assert all(len(s) == 36 for s in policies.values())
        k = len(majority - base)
        random_hits = [len(matched_random(base, k, index, rep) & winning) for rep in range(reps)]
        records.append({
            "index": index, "id": rows[index]["id"], "date": rows[index]["date"],
            "winning": sorted(winning), "x0_missed": sorted(winning - base),
            "states": {str(x): sorted(s) for x, s in states.items()},
            "vote_groups": {str(x): {"numbers": sorted(s), "winning": sorted(s & winning),
                              "x0_missed_winning": sorted((s & winning) - base)} for x, s in groups.items()},
            "policies": {name: sorted(s) for name, s in policies.items()},
            "majority_changed": k, "random_matched_mean": sum(random_hits) / reps,
            "selection": {name: len(s & winning) for name, s in policies.items()},
            "recovered_by_majority": len((majority - base) & winning),
            "lost_by_majority": len((base - majority) & winning),
        })
    summary = {}
    for name in ("X0", "majority36", "minority36"):
        histogram = [sum(r["selection"][name] == k for r in records) for k in range(7)]
        summary[name] = {
            "selection": sum(r["selection"][name] for r in records),
            "histogram": histogram,
            "selection_ge5": histogram[5] + histogram[6],
            "selection_6": histogram[6],
            "quarters": [sum(r["selection"][name] for r in records[q:q + 156])
                         for q in range(0, len(records), 156)]
        }
    summary["groups"] = {k: {**v, "hit_rate": v["hits"] / v["available"] if v["available"] else None}
                         for k, v in categories.items()}
    summary["random_matched_mean_total"] = sum(r["random_matched_mean"] for r in records)
    summary["majority_recovered"] = sum(r["recovered_by_majority"] for r in records)
    summary["majority_lost"] = sum(r["lost_by_majority"] for r in records)
    return {"version": "CHAMPION-X-PHASE2-V1", "first": first, "last": last,
            "summary": summary, "records": records}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--first", type=int, default=789)
    ap.add_argument("--last", type=int, default=1412)
    ap.add_argument("--random-reps", type=int, default=100)
    ap.add_argument("--strict-pinned", action="store_true")
    args = ap.parse_args()
    assert args.random_reps > 0
    provenance = verify_sources(args.data, args.strict_pinned)
    rows = [json.loads(line) for line in args.data.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert 156 <= args.first <= args.last < len(rows)
    report = run(rows, args.first, args.last, args.random_reps)
    report["provenance"] = provenance
    if args.first == 789 and args.last == 1412 and provenance["pinned_match"]:
        assert report["summary"]["X0"]["selection"] == 2473, "R19 X0 golden mismatch"
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"provenance": provenance, "summary": report["summary"]},
                     ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
