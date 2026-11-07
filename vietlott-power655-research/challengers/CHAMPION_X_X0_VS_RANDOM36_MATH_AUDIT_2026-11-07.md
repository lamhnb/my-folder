# X0 Frozen vs Random36 — mathematical audit (2026-11-07)

## Provenance
- Branch: `research/power655-champion-x-input-sensitivity-20261025`
- Source: `vietvudanh/vietlott-data/data/power655.jsonl`; Git blob `5dbd6992ed278e33b0db24c2d0d95b2198d89d77`; 1421 chronological input records in original file order, including anomaly #00944.
- Frozen R19 blob: `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`; Hybrid6 blob: `252f6e0e3dad70a80a4b0cf7febe92d5d080e264` (verified through GitHub fetch).
- Target zero-based indices: 789–1412 inclusive, n=624. Strict-past history `rows.slice(0,i)`.
- **Execution caveat:** this replay used an independent JavaScript translation of both Python Frozen files, not a Python clean-checkout execution. The historical X0 total benchmark was 2473; compare below before accepting parity.

## Selection histogram and exact null
For any fixed 36 of 55 labels, `P(K=k)=C(36,k)C(19,6-k)/C(55,6)`.

| K | Observed | Expected Random36 | Probability |
|---:|---:|---:|---:|
| 0 | 0 | 0.584 | 0.09359% |
| 1 | 7 | 9.010 | 1.44399% |
| 2 | 59 | 52.561 | 8.42327% |
| 3 | 140 | 148.923 | 23.86595% |
| 4 | 215 | 216.815 | 34.74601% |
| 5 | 150 | 154.180 | 24.70827% |
| 6 | 53 | 41.926 | 6.71892% |

- Total observed Selection: **2473**, exact-null expectation **2450.618**.
- Selection ≥5 observed: **203**; expected **196.106**; one-sided exact binomial tail **0.289422**.
- Selection =6 observed: **53**; expected **41.926**; one-sided exact binomial tail **0.0491453**.
- Best-hit histogram 0..6: **[0,233,335,50,4,1,1]** (replay; allocation comparisons remain exploratory).

## Interpretation and limitations
Under independent fair draws, the hypergeometric distribution is exact even if the selected 36 numbers depend arbitrarily on prior draws. Binomial tails assume independent future draws across targets. This is an *unadjusted, retrospective* diagnostic; many champions and challengers were tried on the same development window. No confirmed OOS forecasting advantage follows from these p-values.

## Next experiment: allocation conditional null
For each of the same 624 frozen 36-label sets, retain the actual winning six only for scoring, and randomly shuffle the 36 selected labels into six disjoint six-number tickets using a seeded Fisher–Yates shuffle. Repeat at least 10,000 portfolio allocations per target (or compute exact occupancy probabilities), recording best-hit ≥3, ≥4, ≥5 and jackpot. Stratify by Selection K=0..6. Compare the actual frozen allocation to the conditional random-partition distribution with Monte Carlo confidence intervals and paired per-target differences. Do not re-optimize after observing results. Add multiple-testing adjustment and reserve genuinely future draws for confirmation.

## Frozen integrity
No Frozen source file modified by this report commit. This report does not authorize ticket changes or increased budget.
