# Champion-X forensic audit #01417 — 2026-10-30

## Identity and provenance
- Target #01417, draw date 2026-10-29, main winners 09,29,33,38,45,46; special 53.
- Forecast history: 1416 rows through #01416. Target #01417 excluded from all inputs, used for scoring only.
- Data fetched from vietvudanh/vietlott-data main, 1417 rows at inspection.
- Original R19 Frozen blob a7ebf4fa5216e1bfd4906087e04555044d3e58f0 and Hybrid6 blob 252f6e0e3dad70a80a4b0cf7febe92d5d080e264 unchanged.
- Rebuilt in independent JS, **not Python clean-checkout PASS**.
- Original exact six tickets matched the issued pre-draw X0 ticket list. This target was already known when forensic audit was conducted; counterfactual X variants are not pre-draw choices.

## Issued X0 and hits
1. 04 07 10 27 31 **38** (1)
2. 19 24 39 42 50 55 (0)
3. 05 06 08 **09** 36 41 (1)
4. 01 11 13 14 26 40 (0)
5. 18 23 25 34 **45** 52 (1)
6. 02 17 21 28 47 51 (0)

Selection 3/6; best-hit 1/6; misses 29,33,46.

## Missed-number diagnostic
| Number | F156 | F30 | Momentum | F156 rank among 55 | Excluded R19 momentum rank |
|---|---:|---:|---:|---:|---:|
| 29 | 21 | 2 | -0.067948718 | 6 | 14/19 |
| 33 | 19 | 1 | -0.088461538 | 20 | 17/19 |
| 46 | 13 | 2 | -0.016666667 | 49 | 9/19 |

All three were absent from the Hybrid6 output and absent from the original R19 final output. High F156 alone does not guarantee retention. Frozen R19 swaps: ticket1 53→04, ticket5 20→52, ticket2 16→42, all zero impact on actual Selection #01417.

## Rotated X-state Selection (all use same frozen R19 on rotated 156-row strict-past history)
| X | Selection | Best-hit | Recovered true winners absent X0 | Lost true winners present X0 |
|---|---:|---:|---|---|
| X0 | 3 | 1 | — | — |
| X5 | 5 | 1 | 29,33 | — |
| X15 | 3 | 1 | 29,33 | 09,45 |
| X30 | 3 | 1 | 29,33 | 09,45 |
| X60 | 4 | 1 | 29,46 | 09 |
| X90 | 5 | 1 | 29,33 | — |

No state achieved Selection=6. **X5 and X90 retrospective recovery is not a forecasting signal:** rotating the past destroys the recent-30 chronology. Choosing the best X after viewing the result is oracle leakage.

Changed labels relative to X0:
- X5 added 16,20,29,33,35,54; removed 21,26,39,40,42,52.
- X15 added 12,15,16,20,29,30,33,35,48,54; removed 05,08,09,21,26,39,45,47,50,51.
- X30 added 12,15,16,20,22,29,30,32,33,35,37,48,54; removed 01,04,07,09,13,17,18,25,34,45,47,50,51.
- X60 added 12,15,16,20,22,29,30,32,43,46,48,49,53,54; removed 04,06,08,09,11,17,18,23,24,39,40,42,47,52.
- X90 added 12,15,16,22,29,30,32,33,44,48,53; removed 02,04,05,11,14,18,24,27,40,42,55.

## Swap-count controls
X0 3-swap: Selection 3, best-hit 1.
R19 2-swap: Selection 3, best-hit 1.
X-Momentum 0.12: Selection 3, best-hit 1.
0-swap Hybrid6: Selection 3, best-hit 1.
For 0.12, the three proposed swap momentum differences were .078205128, .078205128 and .070512821, so none passed the gate.

## Research interpretation
#01417 is primarily a Selection miss, with a secondary Allocation split 1/0/1/0/1/0. With only three winning labels in the selected 36, no allocation can produce a 4/6 ticket. X5/X90 achieved Selection 5/6 retrospectively but still best-hit only 1/6. The number 46 was included only by X60 among the inspected alternatives, with lost winning label 09.

**No promotion/no change to Frozen**. Compare such cases in a locked historical protocol with strict-past rules and future holds; do not choose winning X retroactively. Original dataset row-order anomaly remains unresolved. No Python clean-checkout PASS.
