# Champion-X — Exclusion-First / Regime Detection falsification pilot (2026-11-03)

## Scope and controls
Research-only analysis on the **same reused 624 targets**, original zero-based indices 789..1412 of the original-order 1419-record public Power 6/55 JSONL snapshot (latest target data #01419, dated 2026-11-03). No new truly untouched holdout. Dataset source Git blob as observed from GitHub `9410e9f5df02717134cd2fa417aac57be1c01497`. Historical raw row-order anomaly retained.
The original R19 Frozen source blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0` and Hybrid6 dependency `252f6e0e3dad70a80a4b0cf7febe92d5d080e264` were read; neither changed. Independent JS translation of the original algorithms, **not a Python clean-checkout PASS**. All predictions and features for target i use `rows[:i]`, winning main six numbers from row i only for scoring.

X0 remains 36 distinct labels. Observed baseline Selection=2473/624, Selection>=5=203, Selection=6=53; excluded winning appearances=1271 across 624×19=11856 excluded-number exposures. Fair lottery expectation per draw for a fixed arbitrary 36-number set is 6*36/55=3.92727 correct, and Selection=6 probability C(36,6)/C(55,6). Retrospective development bias remains significant.

## Experiment A — Conditional exclusion-group random benchmark
For every excluded group G in a target, let `M_i` be the **observed** winning count among 19 X0-excluded labels; group exposure `|G_i|` and observed group winning count `hits_i`. Compare cumulative hits to `Σ_i M_i * |G_i| / 19`, the exact expected group hit count if the M_i excluded winning labels were uniformly randomized over the 19 excluded positions *within the same target*. This is a conditional explanatory null; it does not prove a feasible prediction rule. Overlapping group definitions are not independent. Report historical exploratory numbers:

| Group | Exposures | Actual excluded wins | Conditional expected |
|---|---:|---:|---:|
| F156 top36 but final X0 excluded | 5257 | 568 | 564.158 |
| F156 below top36, excluded | 6599 | 703 | 706.842 |
| Negative momentum among excluded | 10328 | 1108 | 1106.105 |
| Nonnegative momentum among excluded | 1528 | 163 | 164.895 |
| Excluded F156 >=18 | 3637 | 381 | 389.579 |
| Excluded F156 <18 | 8219 | 890 | 881.421 |
| Vote 0–2 across six X-state selections among X0 exclusions | 5810 | 616 | 622.053 |
| Vote 3–4 among X0 exclusions | 5170 | 561 | 556.947 |
| Vote 5–6 among X0 exclusions | 876 | 94 | 92.000 |

These small deviations and direction changes by quarter do not show a usable historical exclusion signal. They provide no evidence that the number 22's recent repeated exclusion is systematic rather than retrospectively noticed.

## Experiment B — Pre-target failure-regime features
For each target, compute without current outcome:
1. `numTop`: count of X0-excluded labels belonging to original top36 F156 (range 6..11; mean 8.425).
2. `disagree`: sum over X0's 19 excluded labels of their inclusion votes in the other five rotated X states (range 39..59; mean 48.694). The six-X vote definition is the same Phase 2 sensitivity test, not a credible external forecasting signal.
3. `neg`: count of X0-excluded labels with F30/30 − F156/156 <0 (range 12..19; mean 16.551).
Response measured **after** each target is the number of winning labels missing from X0 (mean 1271/624=2.037).
Pearson correlation with missed count across 624: numTop **+0.01782**, disagree **−0.03047**, neg **−0.02056**.
The disagrement-feature correlations by consecutive quarters (156 targets each): **+0.04948, −0.18230, +0.00109, −0.00656**. A high disagreement value did not consistently predict poor Selection. The features are tested post hoc and no independent OOS calibration was attempted.

## Experiment C — One fixed Exclusion-First intervention
A simple deterministic, input-only counterfactual: after producing Frozen X0's 36 labels, select the **highest F156 excluded label** (ties ascending label) and swap it in for the **lowest F156 retained label** (ties ascending label); no target result read. Keeps exactly 36 unique labels and six ticket slots in principle, but this pilot evaluates **Selection only** (the label set, not new ticket partition).
- Original X0: Selection **2473**, Selection>=5 **203**, Selection6 **53**, quarters [606,636,613,618].
- ExclusionFirst1: Selection **2474**, Selection>=5 **200**, Selection6 **56**, quarters **[613,629,608,624]**.
- One-swap unconditional matched-random control *conditional on the actual baseline hit count for each target*: analytical expected Selection **2471.2003** (drop one uniform among 36, add one uniform among 19). This is not a significance result; conditional expectation depends on observed wins but candidate selection did not.
- Paired changes across draws: improved **65**, worsened **64**, same **495** (7 replaced pairs both winning, 488 neither), net +1. Thus ExclusionFirst1's higher Selection6 count is counterbalanced by loss in Selection>=5 and unstable quarters.
- No Jackpot or allocation metric claimed from this label-only experiment.
- Do NOT promote ExclusionFirst1 or retune based on its three extra Selection6 draws; this is a newly explored variant within a heavily reused window.

## Conclusions and research gate
Exclusion-First is a *useful forensic reframing* but mathematically equivalent to selecting 36 labels. The tested “protect high-F156 excluded labels” and “detect weak-selection regime from disagreement” hypotheses show no compelling, stable advantage in this retrospective sample. Selecting 36 predetermined numbers from a fair independent Power 6/55 draw has exactly the same probability distribution whatever the algorithm.
Do not modify Frozen / registered Champions, and do not claim statistical superiority from historical scanning. A credible next gate would freeze one explicit rule and record issued six tickets before each future draw, alongside unchanged X0 and uniform matched-random controls, for a genuinely untouched prospective test. Fix the known data chronological anomaly and obtain clean Python hash-verified replay separately before any certification.
