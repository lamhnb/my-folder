# Champion-X — Exact Allocation Conditional Null Audit (2026-11-07)

## Scope and provenance
Target 624 indices 789..1412, strict-past historical X0 benchmark. The independently reconstructed X0 selection histogram was K=0..6: [0,7,59,140,215,150,53], total 2473. X0 best-hit histogram B=0..6: [0,233,335,50,4,1,1]. Frozen R19 blob a7ebf4fa5216e1bfd4906087e04555044d3e58f0; Hybrid6 blob 252f6e0e3dad70a80a4b0cf7febe92d5d080e264. No Frozen modifications.

## Exact conditional null
Condition on each target's observed X0 Selection K. Randomly partition the same selected 36 distinct labels into six unlabeled six-label tickets, uniformly over partitions. Conditional on K, the K winning labels are a uniform K-subset of the 36 ticket positions. Enumerate all occupancy vectors (x1..x6) with sum xi=K and 0<=xi<=6; weight each vector by product_i C(6,xi)/C(36,K). Best-hit B=max(xi). This is an **exact** combinatorial null, not Monte Carlo. It does not require storing the 36 identities once K and X0 best-hit histogram are known. Across draws, the null assumes independent random allocations per draw.

| Threshold | X0 observed | Exact conditional expected | Unadjusted one-sided P(null >= observed) |
|---|---:|---:|---:|
| B>=3 | 56 | 51.86795510 | 0.28772793 |
| B>=4 | 6 | 2.51194583 | 0.04178155 |
| B>=5 | 2 | 0.04387429 | 0.000926613 |
| B=6 | 1 | 0.000163262 | 0.000163249 |

Exact one-sided tail computed from a Poisson-binomial distribution with 624 per-draw success probabilities based on K. Null probabilities for K=6: P(B=1..6)=[0.0239532763,0.7083405210,0.2470489662,0.0200996821,0.0005544740,0.0000030804].

## Crucial interpretation
The low conditional p-values for B>=5 and jackpot are **not** evidence of an OOS predictive advantage. This X0 algorithm was selected/evaluated among many challengers using the same historical data and the known jackpot event #01320; these tail probabilities ignore the research selection process and are severely vulnerable to data snooping / multiple testing. The conditional null tests allocation given X0's selected set; it does not test whether X0 selected 36 numbers better than random. Under independent fair draws, any six *distinct* prespecified tickets have the same jackpot probability 6/C(55,6), regardless of their allocation or number overlap. A single retrospective jackpot is not a reason to increase ticket spending.

## Next gates
1. Retrieve a complete per-draw ticket matrix and independently replay frozen Python clean-checkout to verify the benchmark and draw-level B/K table.
2. Audit all previously tested allocations/challengers, explicitly account for model selection (family-wise adjusted or nested holdout) and treat the existing 624 draws as development-only.
3. Freeze an allocation hypothesis before evaluating genuinely future draws. For B>=3, there is no clear positive evidence in this audit.

This report is an exact conditional audit of supplied and independently reproduced historical aggregate counts, not a new forward-test. Frozen sources untouched.
