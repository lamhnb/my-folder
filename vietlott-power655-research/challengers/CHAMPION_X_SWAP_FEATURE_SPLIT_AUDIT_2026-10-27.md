# Champion-X swap feature decision — chronological exploratory split (2026-10-27)

## Provenance
Frozen R19 blob a7ebf4fa5216e1bfd4906087e04555044d3e58f0 and Hybrid6 dependency 252f6e0e3dad70a80a4b0cf7febe92d5d080e264 unchanged. Data from upstream commit 52d37a1d9208fc4178b0e5be73b8653c38ff88de, 1415 rows ending #01415, raw original order retaining anomaly. Fixed targets index 789..1412 (624). Predictions generated from rows[:index] only. Independent JS reconstruction, **NOT clean-checkout Python PASS**.

## Features and policy
For each of R19's three original hypothetical swaps, compute candidate features before the target outcome:
- `dm = momentum(in)-momentum(out)`, momentum=f30/30-f156/156
- `df=f156(in)-f156(out)`
- `d30=f30(in)-f30(out)`
- Candidate simple policies keep each proposed swap iff feature compared against a threshold in the chosen direction. All 36 labels retained; R19 Frozen itself not changed.
- Exploration checked 3 features x 7 thresholds (-.12,-.06,-.03,0,.03,.06,.12) x 2 directions = 42 candidates. This is a limited *retrospective parameter scan*, not preregistration.
- First 312 targets index 789..1100 for candidate selection by Selection; latter 312 index 1101..1412 for a fixed-rule replay. **Not a virgin out-of-sample holdout:** full 624 targets have already informed prior Champion-X research.
- Best first-half candidate under deterministic sort: `dm >= 0.12`. Source's rank CrossRank score itself is constant by swap stage and unsuitable for threshold calibration.

## Results
| Policy | first312 Selection | last312 Selection | first312 Sel>=5 | last312 Sel>=5 | first312 Sel=6 | last312 Sel=6 |
|---|---:|---:|---:|---:|---:|---:|
| Hybrid6 / 0 swap | 1253 | 1234 | 104 | 104 | 29 | 24 |
| R19 / 1 swap | 1258 | 1231 | 105 | 99 | 32 | 21 |
| R19 / 2 swaps | 1254 | 1236 | 102 | 98 | 34 | 21 |
| R19 Frozen / 3 swaps | 1242 | 1231 | 99 | 104 | 31 | 22 |
| dm>=.12 independent swap acceptance | 1258 | 1236 | 105 | 103 | 30 | 24 |

The candidate's second-half Selection 1236 is +5 above frozen 1231, **equal** to fixed R19-2Swap 1236. Candidate second-half Selection>=5 is 103 vs frozen 104; Selection 6/6 is 24 vs frozen 22. Differences are small; no stable or independent predictive edge established.

## Methodology caveats
1. This is a sequential-branch *independent per-swap keep/delete* experiment: R19's original incoming/outgoing labels are generated under the complete three-swap hypothetical baseline before evaluating the gate. This differs from reranking and regenerating the next swap after a declined swap; subsequent swaps in the frozen algorithm use original rank lists and avoid reuse. Source-level Python consistency test is still required.
2. The 42 candidate feature/threshold rules were compared in the first half; there is selection bias. Earlier experiments already examined the second half too, so it cannot be called pristine OOS.
3. The raw source has known historical row-order anomaly. Independent draw process remains unproven. No claim of predictive advantage.
4. The fair-draw expectation for any predetermined final set of 36 is 6*36/55=3.92727 winning labels per target; selection differences shown are modest.

## Decision
Keep both X0 R19 Frozen and registered Champions unchanged. `dm>=0.12` is a shadow candidate only. Next defensible validation is a fully frozen policy compared with fixed R19-2Swap and original X0 on **future never-before-inspected draws**, with no changes after results. No version promotion.
