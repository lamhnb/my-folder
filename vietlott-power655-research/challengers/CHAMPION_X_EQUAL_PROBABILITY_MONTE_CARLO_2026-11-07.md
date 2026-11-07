# Power 6/55 — Equal probability and serial overlap Monte Carlo audit (2026-11-07)

## Data provenance and scope
- Source: `vietvudanh/vietlott-data/data/power655.jsonl`, Git blob `5dbd6992ed278e33b0db24c2d0d95b2198d89d77`.
- 1421 raw records, 1420 valid main-six records. Invalid record excluded for this statistical audit only. Original order of retained rows preserved. Note that adjacent valid-record pairs spanning the excluded record are not necessarily adjacent in the raw source; audit of time ordering remains necessary.
- Each simulated history contains 1420 independent fair draws, each consisting of six distinct integers sampled uniformly without replacement from 1..55. Seeded xorshift32 PRNG, seed 20261107 for marginal audit and 20261108 for overlap audit. 12,000 simulated histories per audit. This is an independent JavaScript computation, not Python clean-checkout execution.

## Marginal equality test
H0: all 55 numbers have marginal inclusion probability 6/55. Pearson statistic observed 51.20774647887323, expected per label 154.9090909090909. Simulated null statistic mean 48.94839553990621. Of 12,000 simulations, 4,639 have statistic >= observed. Plus-one Monte Carlo p=(4639+1)/(12000+1)=0.3866344471; MC standard error about 0.00445. This corrects the earlier uncalibrated independent-cell chi-square p≈0.583, which is not appropriate for six-without-replacement sampling.

## Serial-overlap test
For 1419 consecutive retained-valid-row pairs, observed sum of overlapping main labels 935, observed count of pairs with >=1 overlap 722. Fair-draw expected overlap sum 928.8. Null Monte Carlo mean overlap sum 929.0895833333333; mean pairs with >=1 overlap 734.6669166666667. 12,000 full independent-history simulations, two-sided absolute-deviation statistic from fair-model expectation: overlap sum p=0.8265977835180401, any-overlap pair count p=0.5141238230147488. These are targeted serial-dependence diagnostics, not an omnibus test of all temporal dependence.

## Interpretation
Neither marginal-frequency deviations nor these two adjacent-draw overlap diagnostics reject the fair-independent null at conventional levels. Failure to reject does not prove fairness or independence. The historical research window is repeatedly inspected; exploratory multiple-testing and future OOS validation are still required before claiming predictive edge. Frozen R19/Hybrid6 unchanged. No official ticket changes.
