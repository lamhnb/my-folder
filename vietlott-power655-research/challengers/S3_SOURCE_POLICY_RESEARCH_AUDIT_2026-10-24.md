# S3 Source Policy V1 — Reproducibility & Sensitivity Audit (2026-10-24)

## Status
RESEARCH ONLY — NOT CHAMPION; NOT R19 FROZEN. Do not deploy as demonstrated forecasting advantage.

## Provenance
Base commit: `5b951585b6d55c18ab6671b3974bb18347d40892`.
Hybrid6 source Git blob: `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`.
R19 frozen source Git blob: `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`.
Data: `vietvudanh/vietlott-data/data/power655.jsonl`, raw historical pinned blob `1230696771274d48b261a0cfbd728444700c299e` (1,414 rows through #01414). Current public source may additionally contain #01415; freeze first 1,414 rows to reproduce original development context. Known anomalous #00944 row in source; no retroactive edits.
Evaluation: zero-based rows 789..1412 inclusive = 624 draws; prior history only; 6 main winning labels, not 7th special.

## Algorithm
1. Use untouched Hybrid6 to form its six tickets and 19 excluded labels.
2. Rank excluded 19 by descending momentum F30/30 - F156/156, take top 3 M.
3. Rank excluded 19 by descending previous gap (up to 156 draws, 157 if absent), take top 3 G.
4. Take unique union M+G, normally six candidates.
5. For every past draw in the last 312, classify selected union labels: M-only (source 0), G-only (source 1), overlap (source 2). Count source-specific appearances in that past draw's six winning labels. Exclude overlap observations from denominators for both source rates.
6. Estimate source hit rates with (hits + 6)/(candidate observations + 55).
7. CRITICAL HISTORICAL QUIRK: sort candidates ASCENDING by historical source hit rate (lower first), then local source rank ascending, then numeric label. Source 2 receives G source rate. Select first three.
8. The ranking direction above is intentionally contrary to an intuition of selecting better-performing sources. The original exploratory 222 score used ascending sorting. Changing to DESCENDING is a different strategy: only 184 hits for 312-draw lookback.
9. No six final lottery tickets are generated; this is candidate selection only.

## Exploratory replay — all 624 draws
Original Momentum top 3: 201 candidate hits.
Original Gap-long top 3: 201 candidate hits.
S3 V1 inverse-history policy, window 312: 222 candidate hits, quarters [49,52,58,63].
Candidate union: 400 hits, ~5.98 candidates/draw; random-three expected ~200.7 hits conditional on union.
All results exploratory, no clean-checkout Python PASS yet; golden test is committed but not yet executed.

## Sensitivity, independently reconstructed from committed algorithm
| Rolling lookback | S3 V1 LOW-rate-first | HIGH-rate-first control |
|---|---:|---:|
| 78 | 196 | 201 |
| 156 | 214 | 186 |
| 234 | 199 | 201 |
| 312 | 222 | 184 |
| 468 | 216 | 185 |
| 624 | 203 | 200 |
| 936 | 196 | 206 |

Interpretation: V1 only performs well in some lookback choices. Since 312 was evaluated in previously explored data, 222 is subject to model-selection bias. Moreover, inverted sorting implies possible regression-to-mean/data-mining rather than learned advantage. No proof of superiority to randomized choices, no prospective holdout.

## Exact replay
```sh
python vietlott-power655-research/challengers/s3_source_policy_research_20261024_v1.py --data data/power655.jsonl --output s3_replay.json --first 789 --last 1412
python vietlott-power655-research/challengers/test_s3_source_policy_research_20261024_v1.py --data data/power655.jsonl
```
Import sibling files from `challengers/`. Confirm pinned historical data and SHA before attributing numbers to the frozen version. Never change the frozen source or champion.

## Research decision
Preserve S3 V1 for provenance. Do NOT promote to trading/purchase guidance or claim predictive signal. Compare as-of-frozen decision against truly future outcomes; include repeated seeded random controls, uncertainty and multiple-comparison safeguards.
