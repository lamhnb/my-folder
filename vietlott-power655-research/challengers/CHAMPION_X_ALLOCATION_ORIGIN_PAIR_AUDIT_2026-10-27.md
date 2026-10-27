# Champion-X: Origin-of-selection and pair provenance audit (2026-10-27)

## Scope and provenance
- Read frozen R19 source blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0` and Hybrid6 blob `252f6e0e3dad70a80a4b0cf7febe92d5d080e264` from branch `research/power655-champion-x-input-sensitivity-20261025`. Both **untouched**.
- Independent JS reconstruction, not Python clean-checkout PASS.
- Data: 1415-row original-order upstream JSONL at commit `52d37a1d9208fc4178b0e5be73b8653c38ff88de`, through #01415, preserving known row-order anomaly. Fixed 624 targets, row positions 789..1412, with history strictly `rows[:i]` and target result used only for scoring.
- X0 total Selection reconstructed to **2473** exactly. Every target selects exactly 36 distinct numbers.

## Exclusive source labels within final 36
- `Top36_retained`: number in top-36 F156 before Hybrid6 modifications that survived into final R19 selection.
- `Hybrid_outside_top`: number not in original top-36 F156, inserted by Hybrid6 and retained in final R19 selection.
- `R19_in`: number injected by R19 crossrank swaps into final tickets, taking precedence over all other origin groups.
- All three groups are mutually exclusive and exhaustive. The number of labels in each group varies by target. Historical hit rate is winning-label appearances divided by selected-label appearances; **not** calibrated future probabilities.

| Origin | candidate instances | winning instances | win rate | Q1 successes/exposures | Q2 | Q3 | Q4 |
|---|---:|---:|---:|---|---|---|---|
| Top36_retained | 17207 | 1890 | 10.9839% | 460/4331 | 478/4305 | 467/4288 | 485/4283 |
| Hybrid_outside_top | 3385 | 382 | 11.2851% | 95/817 | 105/843 | 103/860 | 79/865 |
| R19_in | 1872 | 201 | 10.7372% | 51/468 | 53/468 | 43/468 | 54/468 |
| **Total** | **22464** | **2473** | **11.0096%** | | | | |

For fair uniform independent draws, an individual predetermined label has probability 6/55 ≈ 10.9091% of being drawn. The small observed group differences, especially instability of `Hybrid_outside_top` in Q4, cannot by themselves justify promotion.

## Pair origin matrix
Per target the 36 selected labels generate `C(36,2)=630` candidate pairs, 624×630=393120 candidate pairs. Two labels are marked both-winning only **after** the draw.

| Pair origin | candidate pair instances | both-winning pair instances | empirical rate |
|---|---:|---:|---:|
| Top36 + Top36 | 228889 | 2312 | 1.0101% |
| Hybrid + Top36 | 92846 | 1015 | 1.0932% |
| R19 + Top36 | 51621 | 551 | 1.0674% |
| Hybrid + Hybrid | 7737 | 78 | 1.0081% |
| Hybrid + R19 | 10155 | 99 | 0.9749% |
| R19 + R19 | 1872 | 9 | 0.4808% |
| **All** | **393120** | **4064** | **1.0338%** |

**Warning about small origin groups:** R19 always injects three labels; thus there are just three R19+R19 candidate pairs per target. Only nine co-winning pair observations across 624 targets is too little to claim a structural exclusion relationship. Group/quarter rates mix variation in per-target Selection with changes in group sizes; they need selection-conditioned adjustment before testing.

### Per-quarter both-winning counts / candidate exposures
- Hybrid+Top: Q1 242/22578, Q2 283/23120, Q3 275/23498, Q4 215/23650.
- Top+Top: Q1 543/58007, Q2 589/57320, Q3 568/56859, Q4 612/56703.
- R19+Top: Q1 145/12993, Q2 145/12915, Q3 114/12864, Q4 147/12849.
- Hybrid+Hybrid: Q1 19/1783, Q2 26/1928, Q3 22/2011, Q4 11/2015.
- Hybrid+R19: Q1 16/2451, Q2 37/2529, Q3 22/2580, Q4 24/2595.
- R19+R19: Q1 3/468, Q2 3/468, Q3 1/468, Q4 2/468.

## Interpretation and next gate
1. This is a first provenance audit, not an evaluated new Allocation strategy. All results are retrospective and source data were repeatedly used in earlier strategy searches.
2. The Hybrid+Top pair type has nominally higher observed both-winning frequency than Top+Top; the difference is not yet corrected for Selection, group sizes, or correlated pairs. Do not use this number to upweight or force cross-origin pair grouping.
3. A robust conditioned null keeps each target's observed number S of selected winners fixed and randomly assigns S winning labels to its 36 selected positions; for a specified candidate pair, both-win probability is `S(S-1)/(36*35)`. Aggregate expected both-winning counts by origin-pair type using its own per-target candidate counts, and evaluate per-target permutation variability / blocked quarters. No such significance test has been run here.
4. To demonstrate prospective value, preregister a single partition-construction algorithm using only source origin, F156, F30, and historical information, and test it on draws genuinely untouched by model design. Under independent uniform draws, no precommitted partition of the same 36 numbers has a physical statistical advantage.
5. **Frozen R19 / Hybrid6 / registered Champions unchanged. No promotion.**
