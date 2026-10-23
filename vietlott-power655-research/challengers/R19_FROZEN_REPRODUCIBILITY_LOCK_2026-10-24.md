# R19 Cross-ranking — frozen reproducibility contract (2026-10-24)

## Immutable algorithm identity
- Original experimental algorithm source Git blob:
  `r19_crossrank_frozen_20261024.py` = `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`
- Its imported Hybrid6 source Git blob:
  `hybrid6_p3_r3.py` = `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`
- Exact historical JSONL input Git blob:
  `vietvudanh/vietlott-data:data/power655.jsonl` = `1230696771274d48b261a0cfbd728444700c299e`, 155371 bytes, 1414 rows.
- All three Git blob IDs are **content hashes**, not floating branch names.
- This snapshot must NOT be rewritten or promoted to Champion. Fork a new branch/version for every change.

## Replay contract
Run original checkout from `vietlott-power655-research/challengers`:

```bash
python test_r19_crossrank_frozen_20261024.py /path/to/original-power655.jsonl
python r19_crossrank_frozen_20261024.py --data /path/to/original-power655.jsonl --output full.json --first 156
python r19_crossrank_frozen_20261024.py --data /path/to/original-power655.jsonl --output legacy624.json --first 789 --last 1412
```

**Expected on exact pinned data, if the clean Python execution matches the earlier independent JS reconstruction:**

- Full indices 156–1413, 1258 draws: Hybrid6 coverage 4965, histogram [0,466,687,96,7,2,0]; Cross-ranking coverage 4925, histogram [2,488,667,93,6,1,1].
- Legacy indices 789–1412, 624 draws: Hybrid6 coverage 2487, histogram [0,227,342,49,4,2,0]; Cross-ranking coverage 2473, histogram [0,233,335,50,4,1,1].
- Target #01320: Cross-ranking ticket 5 must equal [12,26,28,43,50,54], after swaps (ticket 4:39→53, ticket 3:33→46, ticket 5:41→28).

**IMPORTANT:** these are golden **expectations from a separate JS replay, not yet a clean-checkout Python PASS**. The test script is designed to FAIL loudly if the Python run differs. Do not claim verification solely from the expected values being documented.

## Known dataset anomaly
At zero-based index 779, row ID #00944 has date 2022-09-23 and only 6 results. It sits before ID #00780. This exact defect is intentionally pinned to reproduce the historical backtests, **not** corrected. A repaired chronological dataset is a *different fixture* and its backtest is not directly comparable. Any cleaned dataset must be recorded under a new name/hash and tested independently.

## Interpretation
The one historical 6/6 is retrospective after model exploration. It is not a purchased Jackpot and is not evidence of an increased winning probability. The full-history model has lower coverage and best-hit than baseline.
