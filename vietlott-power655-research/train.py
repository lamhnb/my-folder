#!/usr/bin/env python3
"""Power 6/55 strict-past research baseline v0.1.0. Standard library only."""
import argparse
import json
import math
import random
from pathlib import Path

VERSION = "0.1.0"
P = 6 / 55

def load_draws(path):
    rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    ids = set()
    previous = ""
    for row in rows:
        values = row["result"]
        main = values[:6]
        assert len(values) >= 6 and len(main) == len(set(main))
        assert all(isinstance(n, int) and 1 <= n <= 55 for n in main)
        assert row["date"] >= previous, "Input must be chronological"
        assert row["id"] not in ids, "Duplicate draw ID"
        previous = row["date"]
        ids.add(row["id"])
    return rows

def ranking(history, window):
    sample = history[-window:] if window else history
    counts = [0] * 56
    for row in sample:
        for n in row["result"][:6]:
            counts[n] += 1
    scores = [(counts[n] + 15 * P) / (len(sample) + 15) for n in range(1, 56)]
    return sorted(range(1, 56), key=lambda n: (-scores[n-1], n))

def pair_matrix(history, window=120):
    matrix = [[0] * 56 for _ in range(56)]
    for row in history[-window:]:
        d = row["result"][:6]
        for i, a in enumerate(d):
            for b in d[i+1:]:
                matrix[a][b] += 1
                matrix[b][a] += 1
    return matrix

def build_tickets(history, window, method):
    numbers = ranking(history, window)[:36]
    if method == "block":
        tickets = [numbers[i*6:(i+1)*6] for i in range(6)]
    else:
        tickets = [numbers[i::6] for i in range(6)]
    if method == "pair":
        matrix = pair_matrix(history)
        def pair_score(ticket):
            return sum(matrix[a][b] for i, a in enumerate(ticket) for b in ticket[i+1:])
        for _ in range(3):
            improved = False
            for a in range(6):
                for b in range(a+1, 6):
                    for i in range(6):
                        for j in range(6):
                            before = pair_score(tickets[a]) + pair_score(tickets[b])
                            tickets[a][i], tickets[b][j] = tickets[b][j], tickets[a][i]
                            after = pair_score(tickets[a]) + pair_score(tickets[b])
                            if after > before:
                                improved = True
                            else:
                                tickets[a][i], tickets[b][j] = tickets[b][j], tickets[a][i]
            if not improved:
                break
    assert all(len(t) == 6 and len(set(t)) == 6 for t in tickets)
    assert len(set(n for t in tickets for n in t)) == 36
    return [sorted(t) for t in tickets]

def score(tickets, actual):
    target = set(actual["result"][:6])
    hits = [len(target.intersection(t)) for t in tickets]
    return {"hits": hits, "best": max(hits), "ge3": int(max(hits) >= 3),
            "ge4": int(max(hits) >= 4), "coverage": sum(hits)}

def candidate_configs():
    return [(window, method) for window in (60, 120, 365, 0)
            for method in ("block", "stride", "pair")]

def train_config(rows, start, stop):
    records = []
    for window, method in candidate_configs():
        outcomes = [score(build_tickets(rows[:t], window, method), rows[t])
                    for t in range(start, stop)]
        records.append({"window": window, "method": method,
                        "ge3": sum(x["ge3"] for x in outcomes),
                        "ge4": sum(x["ge4"] for x in outcomes),
                        "best_total": sum(x["best"] for x in outcomes)})
    selected = max(records, key=lambda x: (x["ge3"], x["ge4"], x["best_total"]))
    return selected, records

def run(rows, holdout, train_window, eta=0.45, seed=20261008):
    assert len(rows) > holdout + train_window + 365
    boundary = len(rows) - holdout
    selected, training = train_config(rows, boundary-train_window, boundary)
    configs = candidate_configs()
    weights = [1/len(configs)] * len(configs)
    rng = random.Random(seed)
    replay = []
    for t in range(boundary, len(rows)):
        history = rows[:t]
        # All predictions are created before opening the current result.
        predictions = [build_tickets(history, w, m) for w, m in configs]
        random_numbers = rng.sample(range(1, 56), 36)
        random_tickets = [sorted(random_numbers[i*6:(i+1)*6]) for i in range(6)]
        actual = rows[t]
        outcomes = [score(tickets, actual) for tickets in predictions]
        random_result = score(random_tickets, actual)
        pre = weights[:]
        rewards = [o["ge3"] + 3*o["ge4"] + .1*o["best"] for o in outcomes]
        weights = [w*math.exp(eta*r) for w, r in zip(weights, rewards)]
        total = sum(weights)
        weights = [w/total for w in weights]
        replay.append({"id": actual["id"], "date": actual["date"],
                       "predictions": [{"window": c[0], "method": c[1], "tickets": tickets,
                                        "outcome": outcome}
                                       for c, tickets, outcome in zip(configs, predictions, outcomes)],
                       "random": random_result,
                       "weights_before": pre, "weights_after": weights})
    final_tickets = build_tickets(rows, selected["window"], selected["method"])
    return {"version": VERSION, "draws": len(rows), "holdout": holdout,
            "training_config": selected, "training_results": training,
            "replay": replay, "final_weights": [
                {"window": c[0], "method": c[1], "weight": w}
                for c, w in zip(configs, weights)],
            "next_tickets_from_selected_training_config": final_tickets}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--holdout", type=int, default=14)
    parser.add_argument("--train-window", type=int, default=112)
    parser.add_argument("--output", default="results.json")
    args = parser.parse_args()
    report = run(load_draws(args.data), args.holdout, args.train_window)
    Path(args.output).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"v{VERSION}: saved {args.output}; selected {report['training_config']}")

if __name__ == "__main__":
    main()
