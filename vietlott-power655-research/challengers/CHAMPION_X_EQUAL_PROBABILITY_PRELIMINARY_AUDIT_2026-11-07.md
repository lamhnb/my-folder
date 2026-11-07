# Power 6/55 — Equal-probability preliminary audit (2026-11-07)

## Data
Source: vietvudanh/vietlott-data/data/power655.jsonl, blob `5dbd6992ed278e33b0db24c2d0d95b2198d89d77`. 1421 raw records, 1420 with six distinct main numbers in 1..55 and at least seven results. One invalid record excluded for this quality-controlled audit; unlike Frozen replay, this analysis is not intended to reproduce historical Frozen input positions.

## Hypothesis
H0: Each of 55 main labels has equal marginal inclusion probability 6/55 per draw. Expected count per label over 1420 draws = 154.9090909. Counts sum to 8520.

Pearson chi-square across 55 marginal counts: statistic 51.20774648, nominal df=54, asymptotic p=0.582766. **Caveat:** six labels within each draw are sampled without replacement, so label counts are negatively correlated. Standard independent-cell multinomial chi-square calibration is not exact; under fair six-without-replacement draws, the statistic has asymptotic scale (55-6)/(55-1)=49/54 relative to chi-square_54. A correct calibrated test should use Monte Carlo simulation of complete 6/55 draws, or the adjusted chi-square approximation. The nominal p above is descriptive, not the final calibrated p.

Lowest counts: 04=126, 28=131, 37=133, 15=134. Highest: 22=181, 41=179, 51=173, 29=171, 34=171. Extreme single-number p-values are unadjusted for inspecting all 55 labels.

## Adjacent draw overlap
1419 adjacent valid-record pairs (after excluding invalid record; caveat: the pair spanning the invalid record is not necessarily truly adjacent in the original raw sequence). Overlap histogram K=0..6: [697,531,170,20,1,0,0]. Expected fair-model counts using C(6,k)C(49,6-k)/C(55,6): [684.4863,560.0342,155.5651,18.0365,0.86345,0.01439,0.000049]. Observed mean overlap 0.658915; null mean 36/55=0.654545. Descriptive agreement does not establish full temporal independence; adjacent overlaps share draws and are not independent observations.

## Conclusions
No compelling evidence of unequal marginal probabilities from these preliminary summaries. Do not infer equal probabilities are proven. Do not use unadjusted per-number deviations as predictors. Next: simulate full-draw Monte Carlo calibrated chi-square, predefine tests for serial dependence, correct for multiple comparisons, and reserve new draws for OOS confirmation.

Frozen R19/Hybrid6 source not changed. No official tickets modified.
