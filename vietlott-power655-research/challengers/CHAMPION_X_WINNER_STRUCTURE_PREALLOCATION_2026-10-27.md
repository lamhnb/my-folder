# Champion-X Winning-number structure pre-allocation audit (2026-10-27)

## Goal and status
Investigate actual six main winners before further allocation optimization. Strict-past forensic reconstruction on the same legacy **624 targets, zero-based rows 789..1412**, not a fresh holdout. 1415 historical JSONL rows through #01415, upstream snapshot commit `52d37a1d9208fc4178b0e5be73b8653c38ff88de`. Historical row anomaly left unmodified. This script-level JS analysis uses only main six numbers and no target-result information when assigning pair ranks. R19 Frozen and Hybrid6 **unchanged**. Not Python clean-checkout PASS. No Champion promotion.

## Pair frequency rank test
At each target i, count unordered pair co-occurrence over rows i-156..i-1 (156 previous draws); rank all C(55,2)=1485 possible pairs by descending co-occurrence with deterministic ascending-number tie-break. Select **150 top** and **150 bottom** pairs from the ranking. Only after ranking, inspect current target's six winners and its 15 pairs. The top and bottom sets each have exact exposure fraction 150/1485 among all possible pairs under the fair independent-draw null. Repeat 624 targets. This is a *diagnostic test chosen after model development*, not a preregistered OOS confirmation.

| Statistic | Observed | Uniform-null expectation |
|---|---:|---:|
| Total winner pair slots | 9360 | 9360 |
| Top-150 pair hits | 945 | 945.4545 |
| Bottom-150 pair hits | 945 | 945.4545 |

Four contiguous 156-target quarters, top-150 hits: 232,229,259,225 vs null 236.3636 each. Bottom-150 hits: 241,224,236,244 vs null 236.3636 each. Top historical pair-frequency ranking shows no pooled enrichment.

## Additional simple structure diagnostics
- Number of winning labels repeated from immediately preceding source row: observed **405** over 624 targets; expectation under independent uniform draws = 624*(6*6/55)=**408.4364**.
- Adjacent-value unordered winning pairs (1-2, 2-3 etc): observed **312** over 624 targets; expectation = 624 * (15*54/1485) = **340.3636**. This is a descriptive deviation, not proof of exploitable nonuniformity. Historical row-order anomaly is retained.
- Number of odd winning labels histogram for 0..6 odd: **[4,34,166,209,142,62,7]**. Null distribution would be hypergeometric with 28 odd labels / 27 even labels; no formal test in this run.

## Interpretation and next analysis boundary
Top versus bottom pair co-occurrence rankings show no aggregate advantage on this reused research window. PairMax allocation experiments on the same 624 historical targets are therefore unlikely to establish reliable prediction solely from previous pair counts. Before changing allocation algorithms, test pair features with matched controls on an actually untouched future slice and assess clusters of selected R19 winners **conditioned on the frozen 36-number selection**, while keeping the target winning combination blinded until after allocation. Such conditioned-pair work has not yet been executed here.

No changes to Frozen versions or registered Champions. No inference of reliable future prediction from these descriptive backtests.