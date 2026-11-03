# Champion-X — Anti-Crowd Geometry and Exact-Ticket Identifiability Gate (2026-11-03)

## Executive decision
**Do not promote an Anti-Crowd exact-six ticket-ranking engine from current public data.** A small out-of-year improvement in predicting *aggregate lower-tier prize concentration* from ticket-pattern features is real in the specified scoring experiment, but does not give the frequency with which any exact six-number combination was purchased. Identifying a 28,989,675-category distribution from ~1,415 draws of class-level payout summaries is mathematically underdetermined, even under an optimistic (false) stationarity assumption.

## Published research / official product context
- Vietlott Power 6/55 supports manual number choices and machine-selected combinations: https://vietlott.vn/vi/choi/power-6-55/cach-choi . Therefore the player-choice population is a **mixture** of manual and system-selected tickets, which no currently ingested prize-tier count breaks apart.
- Wang et al., *Number preferences in lotteries* (2016): https://www.cambridge.org/core/journals/judgment-and-decision-making/article/number-preferences-in-lotteries/47BA27051627CEED421AD3AEE255521E . Actual transaction data in **other lotteries** show personal-number, slip-position, and aesthetic patterns. This does not establish that the same effect sizes apply to Vietlott.
- Aggregate inverse approach reference: https://academic.oup.com/jrssig/article/20/1/31/7034183 .

## Source data / reproducibility
- Source script: `vietlott-power655-research/challengers/champion_x_anticrowd_geometry_20261103.py`.
- Workflow: `.github/workflows/champion-x-anticrowd-geometry.yml`.
- PASS workflow: https://github.com/lamhnb/my-folder/actions/runs/41669287492 .
- Original results: 1,419 draw records, 1,447 prize records, 1,415 validated joined rows, 32 unmatched; 976 training 2017–2023, 439 later years 2024–2026.
- The 2024–2026 data had been inspected before model finalization, so this is chronological later-year model scoring but not truly untouched **prospective** validation.
- Data snapshot SHA256 for balls `3668ec0888e8ce6ef7a7bb8d0bc3508c5b2fe97250e1c7922184d1d19239fffd`, prize `5e7e80423a883da4c70f9e324120ada8690b282d3c779113b1b349640fdba79b`.

## Pilot model
Target is draw-specific `R4=(prize2_count/prize3_count) / [P(exactly4)/P(exactly3)]` under fair uniform combinatorial reference. Models all fit **only** 2017–23:
1. Training-average constant.
2. Ridge(20 pseudo observations per standardized feature), number of six winning main labels in 01–31.
3. Same ridge with seven predetermined features: low31 count, count of neighboring consecutive pairs, squared-gap variance, total six-number sum, count of odd labels, count of multiples of five, and count of labels in 01–06/50–55.
The seven-feature model is deliberately low-dimensional and regularized; no refit on years 2024–26.

## Later-year performance
| Model | 2024–26 N | Test MSE | Improvement vs training constant |
|---|---:|---:|---:|
| Constant | 439 | 0.00977249297 | 0% |
| low31 only | 439 | 0.00922143348 | 5.6389% |
| low31 + geometry | 439 | **0.00917119177** | **6.1530%** |

**Marginal geometric benefit compared with low31-only: 0.5448% relative MSE**; calendar-year breakdown:
- 2024: geometry better than low31 by **2.058%**.
- 2025: geometry **worse by 3.543%**.
- 2026: geometry better by **7.435%**.
Unstable and small; no model promotion. The actual quantity being predicted is a *post-draw aggregate lower-tier prize ratio*, not purchases of any exact combination.

## Impossibility bound under idealized stationarity
Let `x_T` denote a *fixed across all draws* purchase probability or expected ticket mass for each of the `M=C(55,6)=28,989,675` possible exact six-label tickets. This unrealistic assumption is deliberately favorable to reconstruction. In each draw, at most five observed paying-tier count totals (Jackpot1, Jackpot2, First, Second, Third) provide **at most five linear constraints** on x when the ticket count/sales scale is known. Plus one normalization equation, 1,415 draws give at most **7,076 independent linear constraints**. Matrix rank ≤7076, so any such full linear map has nullspace dimension at least:

`28,989,675 − 7,076 = 28,982,599`.

Thus at least **99.9756%** of the original coordinate dimensions remain unconstrained at the linear-algebra level. Even if six independent prize-class aggregates per draw were available, 1,415*6+1=8,491 constraints, with nullity ≥28,981,184. These are rank upper bounds, not directly “percent of tickets unobserved.” They mean that a general **unrestricted exact-combination purchase distribution cannot be uniquely identified**. Nonnegativity could reduce feasible solutions on boundaries, but under a positive interior distribution small nullspace perturbations yield multiple distinct valid distributions with identical aggregates.

The real world is **harder**, because the number and distribution of purchased tickets changes from draw to draw; without sales totals, the observed aggregated prize totals add time-varying scale unknowns. Treat any exact six-ticket probability proposed without direct sales data as a parametric assumption, not an empirical reconstruction.

## Concrete next-data gate
To learn/popularity-rank a *specific* prospective exact six-number ticket, acquire at least one of:
- anonymized per-combination purchase frequency from a legitimate official data provider;
- sufficiently broad and representative voluntarily shared receipts/number choices with a verified selection mechanism, dates and manual-vs-machine flags, **not** a biased social media sample;
- a public, independently validated player-choice histogram for the same game/market, with explicit extrapolation limits.
Otherwise only report aggregate preference proxies and uncertainty intervals. Avoid buying extra tickets because of an unvalidated “prediction.” For a fair draw and six distinct tickets, Jackpot hit probability stays `6/C(55,6)`; pattern geometry does not alter it.

## Frozen invariant
R19 Frozen, Hybrid6 and registered Champions unchanged. Python PASS is for the independent research analysis, not a clean-checkout certification of the Frozen forecasting algorithm.
