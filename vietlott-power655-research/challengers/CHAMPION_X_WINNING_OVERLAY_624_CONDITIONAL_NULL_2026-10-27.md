# Champion-X — Overlay winning numbers on six issued R19 tickets (2026-10-27)

## Provenance and reproduction
- Research-only. R19 Frozen source Git blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`; Hybrid6 dependency blob `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`. Neither changed.
- Historical source commit `52d37a1d9208fc4178b0e5be73b8653c38ff88de`: 1415 JSONL lines ending at #01415. Preserve original raw line ordering and anomaly.
- Exact 624-target historical positions 789..1412 inclusive. Predict from `rows[:i]`; only then overlay `rows[i].result[:6]`. The target has no role in constructing tickets.
- This report is from independent JavaScript reconstruction matching historical frozen baseline. It is **not** Python clean-checkout PASS and not a new holdout.
- Six disjoint six-number tickets, 36 selected numbers, unchanged Selection. Main numbers only; any special-number Jackpot 2 claim is out of scope.

## Overlay pattern
For target i, define six ticket hit counts `hits[t]=|ticket[t] ∩ winning6|`, and sort descending as a six-position pattern (e.g., `2-1-1-0-0-0`). This is **post-draw diagnostic** only. `Selection = sum(hits)`; `best-hit = max(hits)`. Example #01416 X0 issued ticket counts `[2,0,0,2,0,1]` sorted to `2-2-1-0-0-0`, Selection 5, best-hit 2, missed #35 (separate forensic audit).
 
## Frozen baseline independently reproduced (624 targets)
- Selection = **2473**, by-draw Selection histogram for S=0..6: **[0,7,59,140,215,150,53]**.
- Best-hit sum = **1080**, per-draw best-hit histogram h=0..6: **[0,233,335,50,4,1,1]**.
- Best-hit >=3: **56**; >=4: **6**; >=5: **2**; =6: **1**.
- 418 targets have Selection 4, 5 or 6; this subgroup can be described retrospectively, but cannot be used as a pre-target model selector.

Most common sorted hit-count patterns:
- `2-1-1-0-0-0`: 126 draws (Selection 4, best 2).
- `1-1-1-0-0-0`: 79 draws (Selection 3, best 1).
- `1-1-1-1-0-0`: 71 draws (Selection 4, best 1).
- `2-1-1-1-0-0`: 69 draws (Selection 5, best 2).
- `2-1-0-0-0-0`: 58 draws (Selection 3, best 2).
- `1-1-0-0-0-0`: 53 draws (Selection 2, best 1).
- `2-2-1-0-0-0`: 35 draws (Selection 5, best 2).
- `1-1-1-1-1-0`: 22 draws (Selection 5, best 1).
- `3-1-1-0-0-0`: 20 draws (Selection 5, best 3).
These frequent split patterns alone cannot establish faulty Allocation, because combinatorially most preselected random partitions with few selected winners also produce split outcomes.

## Exact conditional random-partition control
Condition on the actual Frozen 36 selected numbers and observed number S of winning numbers within them. Reallocate the **same 36 labels** uniformly at random to six disjoint 6-number tickets, without looking at which numbers won. The exact null probability of ticket hit count vector `(h1,...,h6)` with `sum hj=S` is:
`Pr(h1..h6 | S) = ∏_{j=1..6} binom(6,hj) / binom(36,S)`.
For `best-hit=k`, sum over all ordered vectors with max hj = k. These probabilities are exact combinatorial quantities, **not a Monte Carlo and not a validation of R19 predictive edge**.

| S | P(best=1) | P(best=2) | P(best=3) | P(best=4) | P(best=5) | P(best=6) |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 0.605042 | 0.378151 | 0.016807 | 0 | 0 | 0 |
| 4 | 0.330023 | 0.607334 | 0.061115 | 0.001528 | 0 | 0 |
| 5 | 0.123759 | 0.730519 | 0.138464 | 0.007162 | 0.00009549 | 0 |
| 6 | 0.023953 | 0.708341 | 0.247049 | 0.020100 | 0.00055447 | 0.0000030804 |

The remaining nonzero best-hit probabilities for S=1 and S=2 were included in the exact expectations.

Expected best-hit histogram over all 624 targets (condition on the **actual selection histogram**):
`[0,233.0656,339.0665,49.3560,2.4681,0.04371,0.0001633]`.
Expected best-hit sum **1069.3584**, >=3 **51.868**, >=4 **2.51195**, >=5 **0.043874**, =6 **0.00016326**.

| Metric | Frozen observed | Exact random-partition expectation |
|---|---:|---:|
| Best-hit sum | 1080 | 1069.36 |
| Best-hit >=3 | 56 | 51.87 |
| Best-hit >=4 | 6 | 2.512 |
| Best-hit >=5 | 2 | 0.04387 |
| Ticket =6 | 1 | 0.0001633 |

**Important**: Frozen's rare 5/6 and 6/6 historical hits substantially exceed random-partition expected counts, but this is a heavily reused *model-selected research history*, not a clean independent statistical test. Published retrospective discoveries, chosen algorithms, and selection/reporting after seeing data produce strong selection bias; this is not proof of an edge or of unfair lottery physics. Avoid naïvely turning the tiny exact probability into a p-value for performance after strategy search.

## Interpretation and research gate
1. 36-label Selection is still the primary prerequisite. With S<6, ticket Jackpot 6/6 is impossible.
2. Hit clustering can be diagnosed from sorted six-ticket hit-count vectors; frequent `2-1-1` splits are typical random combinatorics conditional on S.
3. Investigate specific counterfactual reallocations and pair interactions *only as oracle upper bounds* if they use target winners.
4. To evaluate a prospective new Allocation scheme, lock its pre-target algorithm and use truly untouched future outcomes, same 36 Frozen labels and ticket budget. Do not optimize on already-known #01320 Jackpot or #01416 outcome.
5. No new allocation candidate promoted; no modifications to Frozen versions.
