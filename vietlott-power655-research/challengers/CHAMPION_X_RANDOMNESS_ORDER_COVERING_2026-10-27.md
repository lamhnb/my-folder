# Champion-X sequential investigations: randomness, order statistics and covering limits (2026-10-27)

## Provenance and protocol
Dataset: original upstream `vietvudanh/vietlott-data` JSONL at commit `52d37a1d9208fc4178b0e5be73b8653c38ff88de`, 1415 rows through draw #01415 (2026-10-24). Evaluation window: original row positions **789..1412**, 624 draws; known row-order anomaly deliberately not repaired. Six main numbers only. No new prediction method has been fitted, and no R19/Hybrid6/Frozen source modified. This is descriptive exploratory research on previously reused outcomes, not a clean chronological or forward holdout.

## 1. Number frequency and baseline randomness
Across 624 draws: 3744 appearances among labels 1..55, null marginal expectation `3744/55 = 68.072727` appearances per label.
- Pearson frequency chi-square `Σ_n(observed_n-68.072727)^2/68.072727 = 53.321047`, reference df=54 under an **approximate** chi-square model. Draws choose six labels without replacement, so category counts within draws are dependent; use draw-level permutation/Monte Carlo for calibrated significance, not a naive multinomial exact claim.
- Highest observed counts: 22:85, 13:84, 01:81, 34:81, 41:79, 51:79, 08:78, 38:76.
- Lowest counts: 04:49, 15:53, 28:53, 49:54, 06:55, 35:57, 02:59, 19:59.
- Contiguous 156-draw blocks chi-square references: Q1=45.0684, Q2=53.5299, Q3=55.5278, Q4=42.3654.
- No evident large pooled deviation from frequency-uniformity in this simple statistic. That is not a proof of independently random physical draws.

## 2. Order statistics (ascending six winning main numbers)
For a uniform random unordered six-number subset from 1..55, expected ascending position j=1..6 is `56*j/7` (8,16,24,32,40,48).
- Observed position means: `[8.1298,16.2083,24.6458,32.2372,40.2324,47.8558]`.
- Mean adjacent sorted differences: `[8.0785,8.4375,7.5913,7.9952,7.6234]`.
- Mean sum 169.3093 vs reference 168; mean range 39.7260 vs reference 40, per previous matrix audit.
- Adjacent pairs counted across all targets: 312 (prior reported reference expectation 340.36).
- The near-eight gap is an expected order-statistic feature, not evidence of a hidden draw-generation cycle. Significance testing of joint gaps and serial dependence remains an unperformed next gate.

## 3. Coverage combinatorics of exactly six **disjoint** six-number tickets
Holding a fixed selected set of 36 labels, there are `C(36,k)` k-subsets. Six disjoint tickets collectively contain exactly `6*C(6,k)` k-subsets completely inside one ticket. Regardless of how the same 36 numbers are rearranged among six disjoint tickets, these **total counts are invariant**.

| k | within-ticket k-subsets | all k-subsets of selected 36 | covered fraction |
|---|---:|---:|---:|
| 2 | 90 | 630 | 14.285714% |
| 3 | 120 | 7140 | 1.680672% |
| 4 | 90 | 58905 | 0.152788% |
| 5 | 36 | 376992 | 0.009549% |
| 6 | 6 | 1947792 | 0.000308% |

Important: no Allocation can increase these aggregate subset counts while keeping six *disjoint* six-number tickets, but **which** subsets are covered does vary by arrangement. Meaningful improvement requires forecasting which subsets of selected numbers are likelier to win; pattern-fitting from already-known outcomes is leakage/selection bias.

Conditional on Selection=6, a uniformly random allocation of the fixed 36 selected labels achieves a ticket six-of-six with probability `6/C(36,6) = 0.000003080411...` (fraction), or `0.0003080411%`; compare to prior exact conditional random-allocation audit.

## Assessment
- No independently verified predictable deviation found in these three exploratory tests.
- Small marginal frequency deviations, sorting features, and total subset-coverage invariants do not establish a new independent X variable.
- Next responsible experiment: preregister a single potentially meaningful temporal statistic (e.g., serial covariance of the 55-vector of winners or lagged gap bins), calibrated against full simulated draws and evaluated prospectively. Do not choose among scanned indicators by the 624 historical outcomes. For Allocation, test fixed independent feature-based groupings against exact/random same-36 controls on future untouched data.
- R19 Frozen, Hybrid6 and registered Champions unchanged. No clean-checkout Python PASS implied.
