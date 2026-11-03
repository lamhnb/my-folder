# Champion-X — Anti-Crowd Exact-Six Jackpot Ownership: locked later-year test, 2026-11-03

## Decision
**NO GO for promoting a current Anti-Crowd number selection engine**. The previously detected number-01–31 effect on lower-tier prize concentration cannot be reliably transferred to **the probability that another person owns an entire identical 6/55 ticket**. A model using the number of balls <=31 performed worse than the training-only baseline on a later-year Jackpot1-owner indicator. Adding low31 to a Jackpot-pool model also worsened the out-of-time Brier score. The observed jackpot size is a better (but weak and temporally unstable) correlate of ownership. Nothing predicts which winning balls will be drawn.

## Locked data and reproducibility
- Data sources: https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power655.jsonl and https://raw.githubusercontent.com/leoodz/vn-vietlott/main/results/power6x55.json .
- SHA256 at evaluation: balls `3668ec0888e8ce6ef7a7bb8d0bc3508c5b2fe97250e1c7922184d1d19239fffd`; prize records `5e7e80423a883da4c70f9e324120ada8690b282d3c779113b1b349640fdba79b`.
- Python `champion_x_anticrowd_owner_holdout_20261103.py`, GitHub Actions `.github/workflows/champion-x-anticrowd-owner.yml`, PASS: https://github.com/lamhnb/my-folder/actions/runs/41660856580 .
- 1419 raw ball outcomes; 1447 prize records; 1415 matched exact date+winning-six validated prize rows; 32 unmatched; 1411 observations with contiguous prior-draw Jackpot values available.
- Train <=2023 (N=974 with **41 owner events**); later-year test 2024–2026 (N=437, **19 owner events**).
- **Historical caution:** The hypothesis was already explored over the 2024–26 period in prior audits, so this is a prelocked train-then-later-year score, but **NOT a completely untouched OOS scientific confirmation**. No explicit selected exact-six combinations and their contemporaneous frequency of ownership were available.
- Pre-draw Jackpot input: previous draw's displayed prize amount (or nominal guaranteed 30B VND following a Jackpot1 win), a *proxy* for an advertised current prize, not a direct sale ledger. Prize currency scraper fields need verified normalization.
- All model feature scalings and regularized logistic slopes fitted on training years only. Models: constant training owner rate; prior Jackpot size; low31 count; pot+low31; pot+low31+adjacent pairs. No result of target draw used to form the prior jackpot feature, but **the low31 and adjacency count of the winning set are only known post-draw**; this test evaluates ownership conditional on a candidate winning set, not future ball prediction.
- Positive event definition `jackpot1.count >0`; 2 historical draws had 2 jackpot owners, but labels here are binary.

## Chronologically later evaluation
| Model | Test AUC | Test Brier (lower better) | Test logloss (lower better) |
|---|---:|---:|---:|
| Constant training mean | 0.5000 | 0.04158982 | 0.17886841 |
| Low31 only | 0.5200 | **0.04164194** | **0.17934345** |
| Prior jackpot pot only | **0.6048** | **0.04131770** | **0.17604320** |
| Prior pot + low31 | 0.6041 | 0.04147658 | 0.17659892 |
| Prior pot + low31 + adjacent | 0.6004 | 0.04148110 | 0.17668364 |

Year-level AUC for **prior pot only**: 2024 = **0.681** (6 positive), 2025 = **0.425** (5 positive), 2026 = **0.743** (8 positive). Unstable. With only 19 positive test events, no precise estimate of true discrimination can be defended. No exact-ticket popularity calibration is established.

The regression trained on 2017–23 and scored later-years **does not gain predictive quality from the drawn-number low31 pattern** at the exact-Jackpot1 owner level. Lower-tier standardized r4/r3 concentration improvement on 2024–26, shown in `CHAMPION_X_ANTICROWD_OUT_OF_TIME_AUDIT_2026-11-03.md`, is a different target entirely.

## Economic / probabilistic scenario — six different tickets
- Fair six-number outcome space: `C(55,6)=28,989,675`.
- If each of six tickets is a different six-number combination, `P(at least one of six wins Jackpot1)=6/28,989,675 = 1/4,831,612.5` every draw, whatever anti-crowd composition.
- Let `K` = number of other people holding the exact winning ticket. Under a **hypothetical** Poisson K~Poisson(lambda) with all claimants equally sharing a pool, expected Jackpot fraction retained conditional on this ticket winning: `E[1/(1+K)]=(1-exp(-lambda))/lambda`, tending to 1 as lambda→0.
- For arbitrary assumed lambda values only (no empirical calibration): lambda=0.05→97.54% of pool, lambda=0.2→90.63%, lambda=0.5→78.69%, lambda=1→63.21%, lambda=2→43.23%.
- If whole Jackpot1 pool were **100 billion VND** in a hypothetical constant-prize example, 6-ticket *unconditional Jackpot1 component* equals about **20,188 VND** for lambda=.05 versus **13,083 VND** for lambda=1. This is NOT total ticket expected value, does not include other prizes, ticket costs, taxes, actual varying pools, pool-sharing rules beyond the toy assumption, or real lottery ticket selection frequencies.
- Code: `champion_x_anticrowd_share_scenarios_20261103.py`. Critical: no live payout model should use any hypothetical lambda as a calibrated number.
- Creating six disjoint high-number-only tickets is impossible if only numbers 32..55 are allowed (24 distinct labels < 36). Avoid quietly changing the locked 36-number Selection/Allocation specification when creating anti-crowd candidates.

## Forensic audit and scientific gates
1. No test demonstrated elevated hit probability. The fair Jackpot chance is fixed for any six different tickets. Purchase-volume effects cannot change ball-draw likelihood.
2. The available lower-tier winner-count ratios reveal some nonuniform *subcombination* popularity, not the frequency of *specific six-number tickets*. Aggregated payout counts cannot uniquely solve for a 28.99-million dimensional purchased-ticket histogram. Exact-6 ownership labels are exceptionally sparse (60 matched Jackpot1 owner draws over 1415), and do not support high-resolution ticket ranking.
3. Explanatory model improvement in a post-draw ownership label is not a claim that someone can know which six-number ticket will win.
4. A valid next research dataset would contain anonymized actual combination frequencies at point of sale, or independent public studies with empirically measured exact-six selections. Until then, any Anti-Crowd score is only a sensitivity assumption and cannot safely be promoted.
5. If the primary objective is literally *raise the probability of hitting a Jackpot*, the mathematically relevant controls under fair Power 6/55 are the number of **different** combinations purchased and cost. With fixed six distinct tickets, no layout, birthdate penalty, number popularity score, or historical rollover pattern will increase this hit probability.
6. No Frozen R19, Hybrid6 or Champions were modified. This Python anti-crowd audit PASS is not a Python Frozen algorithm clean-checkout PASS.
