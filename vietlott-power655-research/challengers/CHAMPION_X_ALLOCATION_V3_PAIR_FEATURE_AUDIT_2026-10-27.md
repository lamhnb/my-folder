# Champion-X Allocation V3 — pair-feature forensic audit (2026-10-27)

## Reproduction & scope
- Independent **JavaScript reconstruction**, **not** Python clean-checkout PASS.
- Frozen R19 blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`, Hybrid6 dependency `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`. Neither changed.
- Dataset upstream commit `52d37a1d9208fc4178b0e5be73b8653c38ff88de`, 1415 raw JSONL records through #01415; known original row-order anomaly retained.
- Window zero-based 789..1412 inclusive, 624 targets. For target i, generate Frozen tickets and all feature values from earlier `rows[:i]`, then score using `rows[i].result[:6]`. Six disjoint tickets of six, same 36-number selection.
- These 624 targets have been used for repeated model exploration. Descriptive results are **not** independent OOS validation.

## Pair-level overlay
Each 36-number selection has `C(36,2)=630` unordered candidate pairs. Total 624×630=**393120** candidate pair instances. In a target with Selection S, exactly `C(S,2)` selected-label pairs have both numbers winning. Aggregating gives **4064** winning-pair instances. Of these **603** were in the same Frozen ticket and **3461** in different tickets; conditional co-ticket fraction 603/4064=**14.8376%** vs random-partition pair co-ticket probability 5/35 = **14.2857%**. A co-ticket fraction close to random does not establish a reliable pair grouping advantage.

## Strict-past descriptive predictors
- `pair_history_ge2`: two labels co-occurred as main winners at least twice in previous 156 source rows.
- `momentum_close`: absolute difference between labels' `F30/30 - F156/156` ≤ 0.02.
- `number_near`: numerical absolute distance ≤5.
- `number_far`: numerical absolute distance ≥25.

For each feature, count candidate pair instances satisfying it, subset where **both** numbers truly won the current target, and subset of winning pairs already in same Frozen ticket. Groups overlap.

| feature | candidate pair instances | both-win pairs | both-win / candidate | both-win and same ticket |
|---|---:|---:|---:|---:|
| pair_history_ge2 | 202079 | 2132 | 1.05503% | 297 |
| momentum_close | 104854 | 1117 | 1.06529% | 180 |
| number_near | 69542 | 710 | 1.02097% | 98 |
| number_far | 124465 | 1232 | 0.98984% | 176 |
| all candidate pairs | 393120 | 4064 | 1.03378% | 603 |

Feature-specific quarterly both-winning / candidate rates:
- pair_history_ge2: Q1 .98599%, Q2 1.12388%, Q3 1.03639%, Q4 1.07385%.
- momentum_close: Q1 1.06140%, Q2 1.14747%, Q3 1.04836%, Q4 .99742%.
- number_near: Q1 .92396%, Q2 1.19900%, Q3 .87643%, Q4 1.08566%.
- number_far: Q1 .97955%, Q2 .99016%, Q3 1.08009%, Q4 .90277%.

## Analytical limitations
1. **Selection-conditioned null still needed:** comparing a feature's global pair rate to 4064/393120 does not fully adjust for variation in Selection S across targets or candidate composition. Each pair within a target has random-label conditional probability `C(S,2)/C(36,2)`; compare feature actual counts with sum across targets of `eligiblePairs_i × C(S_i,2)/630`. This is a randomized-within-selection diagnostic, not a real draw prediction model.
2. Observations inside a target share labels; pair events are correlated, not independent Bernoulli trials. Standard binomial p-values based on 393120 observations would be invalid. Use per-target randomization or block-resampling.
3. Current results describe a fixed feature set chosen after extensive historical inspection. No training/test lock and no untouched future results. Therefore no causal/predictive claim or significance yet.
4. Candidate pairs in the selection are only one possible statistical unit. Relative to real lottery physics every predetermined pair has the same fair-draw probability `(6/55)(5/54)` of appearing. Selection-conditioned patterns after the fact are not evidence of a predictable physical signal.
5. Frozen source and registered Champion untouched. No Allocation V3 promotion.

## Next gate
Perform per-target conditional-expectation normalization and an exact or Monte Carlo within-36 permutation that keeps each target's Selection S unchanged. Then check signed enrichment in each chronological quarter, and benchmark prospective allocation methods against the *same six tickets* with a blinded future holdout. Until then, the small observed enrichments above should not drive swaps or weights.
