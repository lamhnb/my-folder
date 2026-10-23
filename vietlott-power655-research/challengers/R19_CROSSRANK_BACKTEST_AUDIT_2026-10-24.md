# R19 Cross-ranking Frozen — independent replay audit
Date: 2026-10-24
Branch: research/power655-r19-crossrank-freeze-20261024
Source: challengers/r19_crossrank_frozen_20261024.py
Parent research base: research/power655-m3-reverse3-momentum
Source commit: 661795d125bddfca2d6ce044b4248676f9fa1708

## Definition
- Hybrid6 P3+R3 outputs six disjoint tickets (36 numbers).
- R19 ranks **all** of the 19 excluded numbers by descending 30-vs-156 momentum, ties by ascending label.
- H36 ranks all 36 retained labels using the same momentum.
- For every (incoming R19 number, outgoing currently retained number), use rank differential
  `(20 - rank_R19(in))/19 - (37 - rank_H36(out))/36`.
- Select the largest positive cross-rank swap, up to three swaps per draw.
- Do not re-use an entering or leaving label; prohibit replacement cycles; preserve ticket slot.
- Fixed tie-break: ticket 1..6, entering label ascending, leaving label ascending.
- All features taken strictly from rows preceding target index.
- This is an exploratory rank comparison, **not** a calibrated lottery probability.

## Dataset and reproducibility warning
Public original JSONL: https://github.com/vietvudanh/vietlott-data/blob/main/data/power655.jsonl
Fetched 1,414 rows (through ID #01414 dated 2026-10-22).
**Provenance issue:** row at zero-based index 779 has ID #00944, date 2022-09-23,
only six numbers; it sits between IDs #00779 and #00780. This makes
original row ordering different from ID order and prevents claiming
a clean chronological backtest without further source verification.
This report intentionally **does not silently patch** the dataset.
All numbers below use original JSONL row order. IDs #00789..#01413
are not the same as positions 789..1412. Historical results are
exploratory and have been repeatedly used in model development.

## Full available range: zero-based indices 156..1413 (1,258 targets)
| Metric | Hybrid6 | R19 Cross-ranking |
|---|---:|---:|
| Total selected winning labels / coverage | 4,965 | 4,925 |
| Sum of best hits per draw | 2,166 | 2,136 |
| Draws >=3 | 105 | 101 |
| Draws >=4 | 9 | 8 |
| Draws >=5 | 2 | 2 |
| Draws =6 | 0 | 1 |
| Best-hit histogram 0..6 | [0,466,687,96,7,2,0] | [2,488,667,93,6,1,1] |
| Draws improved best hit vs Hybrid6 | -- | 80 |
| Draws worsened best hit vs Hybrid6 | -- | 108 |
| Net coverage change | -- | -40 |
| Executed swaps | -- | 3,774 |

## Legacy window zero-based indices 789..1412 (624 targets)
| Metric | Hybrid6 | R19 |
|---|---:|---:|
| Coverage | 2,487 | 2,473 |
| Sum best hit | 1,084 | 1,080 |
| Best-hit histogram 0..6 | [0,227,342,49,4,2,0] | [0,233,335,50,4,1,1] |
| Draws >=3 | 55 | 56 |
| Draws >=4 | 6 | 6 |
| Swaps | 0 | 1,872 |
| Best-hit improved / worsened | -- | 41 / 45 |

## Historical 6/6 found — ID #01320, 2026-03-17
Winning mains: 12,26,28,43,50,54.
Hybrid6 ticket 5 before cross-ranking: 12,26,41,43,50,54 (5/6).
Executed changes:
1. Ticket 4, 39 -> 53
2. Ticket 3, 33 -> 46
3. Ticket 5, 41 -> 28
R19 ticket 5 after cross-ranking: **12,26,28,43,50,54 (6/6)**.
This is an in-sample historical coincidence after extensive retrospective model searching;
it does not document a purchased winning ticket and does not establish improved odds.

## Latest observed target #01414, 2026-10-22
Both models: coverage 5; best-hit 2; R19 replaces on tickets
6: 48->46, 5:40->52, 4:28->6.

## Execution status
The metrics were produced by an independent JavaScript replay based on the committed
Python algorithm and original public JSONL; the committed Python entrypoint has
**not** been executed from a clean checkout in this environment.
A clean Python reproduction, dataset hash, chronological-source repair backed
by independently verified results, unit tests and per-draw golden fixtures are
required before certifying these figures.

Run from `vietlott-power655-research/challengers`:
```bash
python r19_crossrank_frozen_20261024.py --data /path/to/power655.jsonl --output /tmp/r19_all.json
python r19_crossrank_frozen_20261024.py --data /path/to/power655.jsonl --output /tmp/r19_624.json --first 789 --last 1412
```
These files store all per-draw tickets, ranking, swaps and hit counts.
No Champion or baseline source was modified.
