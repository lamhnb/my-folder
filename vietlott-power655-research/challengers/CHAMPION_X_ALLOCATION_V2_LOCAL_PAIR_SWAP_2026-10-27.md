# Champion-X Allocation V2 — Local pair-swap experiment (2026-10-27)

## Scope
Unchanged X0 = original R19 Frozen with Hybrid6 dependency. Frozen source blobs: R19 `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`; Hybrid6 `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`. 1415-line public JSONL through draw #01415 on 2026-10-24, upstream commit `52d37a1d9208fc4178b0e5be73b8653c38ff88de`. Historical row-order anomaly remains unchanged. Retrospective evaluation at zero-based indices 789..1412, 624 draws, strict-past `rows[:i]`.

The experimental computations here use an **independent JS reconstruction**, verified by reproducing the original 624-draw R19 best-hit histogram `[0,233,335,50,4,1,1]` and total 1080, but **are not Python clean-checkout PASS**. Nothing was changed in Frozen/Hybrid6/registered Champions.

## Allocation-only transformation
At each target, generate original R19 six tickets and preserve their **entire set of 36 distinct numbers**. Build symmetric 55×55 co-occurrence counts for pairs in the last 156 historical six-main-number results, strictly before the target. Test two directions:
- `PairMax`: maximize sum of historical co-occurrence counts among pairs of numbers **within** each ticket.
- `PairMin`: minimize same sum (negative-control direction).

Search all current cross-ticket swaps (choose two distinct tickets j<m and one number from each), compute delta in their combined within-ticket pair score, choose the swap with maximal strictly positive directed delta. Iterate 1, 3, or 10 swaps; stop early if no positive delta. All score ties keep first encountered by fixed loops j,m,u,v. Number of swaps is a *pilot design choice*, not validated for predictive strength. All final tickets remain exactly six disjoint tickets of six and keep original X0 Selection.

## Observed results

| Model | best-hit histogram 0..6 | Best-hit sum | >=3 | >=4 | >=5 | ticket 6/6 | Q1,Q2,Q3,Q4 best-hit sums |
|---|---|---:|---:|---:|---:|---:|---|
| Frozen | [0,233,335,50,4,1,1] | 1080 | 56 | 6 | 2 | 1 | 254,279,268,279 |
| PairMax1 | [0,249,319,52,3,0,1] | 1061 | 56 | 4 | 1 | 1 | 246,271,269,275 |
| PairMax3 | [0,249,310,62,2,1,0] | 1068 | 65 | 3 | 1 | 0 | 252,265,265,286 |
| PairMax10 | [0,239,334,49,2,0,0] | 1062 | 51 | 2 | 0 | 0 | 259,267,267,269 |
| PairMin1 | [0,234,334,50,5,0,1] | 1078 | 56 | 6 | 1 | 1 | 249,276,275,278 |
| PairMin3 | [0,244,333,43,3,1,0] | 1056 | 47 | 4 | 1 | 0 | 243,273,269,271 |
| PairMin10 | [0,237,351,36,0,0,0] | 1047 | 36 | 0 | 0 | 0 | 244,273,264,266 |

Paired best-hit comparison (higher/equal/lower than original Frozen):
- PairMax1: 24 / 557 / 43
- PairMax3: 77 / 456 / 91
- PairMax10: 134 / 346 / 144
- PairMin1: 24 / 574 / 26
- PairMin3: 59 / 482 / 83
- PairMin10: 111 / 380 / 133

Every alternative retains exactly the original X0 Selection total 2473, including 53 historical Selection 6/6 events. No replacement model dominates Frozen on >=4, >=5, ticket jackpots or aggregate best-hit score. PairMax3 gets 65 >=3 vs Frozen 56, but gives up higher-grade hits. The parameter 3 is selected for **analysis only**, not promotion; choosing it retrospectively is multiple-testing/selection bias.

## Interpretation
The pilot is consistent with local pair-cohesion-based regrouping changing where occasional low-tier clusters occur; it is **not** evidence that pair frequencies forecast future co-occurrences. Under independent uniform Power 6/55 draws, all preselected partitions into six disjoint 6-number tickets have identical true win-probability distributions. In particular, changing partitions cannot generate an expected lottery edge without an independently validated nonuniform outcome-generating mechanism. Previous exploration of these 624 draws contaminates them as a validation holdout.

## Research guardrails / next gate
Keep the Frozen source unchanged. Do not promote PairMax3. If exploring a stronger allocation transformation, **pre-register fixed feature engineering and development/validation split before inspecting untouched future draws**; compare same 36-number sets, exact per-draw best-hit, tail events, shuffled-history and matched-random partition controls, and assess both hit-rate stability and incremental lift. Investigate whether pair-level associations have demonstrated out-of-sample persistence *before* tuning swaps to maximize ticket-level historical hits.
