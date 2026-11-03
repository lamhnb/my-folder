# Champion-X — Jackpot prize-gap vs winning-number microfeatures (2026-11-03)

## Research question and conclusion
Investigate consecutive Power 6/55 **draws with at least one actual Jackpot 1 winner**, comparing (a) monetary difference between successive winner events, (b) elapsed draw count, and (c) small-number, bonus-ball and other patterns in the six winning main numbers. Findings are **exploratory, not predictive**: prize values naturally correlate with the duration of the rollover cycle, but no number feature survives a reasonable combination of confound adjustment, sensitivity and multiple-test caution.

## Sources and data provenance
- A third-party 40-event historical Jackpot 1 table, from #00496 (2020-10-31) through #01384 (2026-08-13), including published per-ticket values: https://1682xoso.com/thong-ke-vietlott/power-6-55
- Added draw #01415 (2026-10-24, VND 199,984,640,250, one Jackpot 1 winning ticket) cross-checked from https://www.minhngoc.net.vn/ket-qua-xo-so/dien-toan-vietlott/power-6x55/24-10-2026.html and https://kqxsviet.vn/vietlott/power-655/ky-01415
- Full winning-number/bonus record lookup by draw ID from vietvudanh/vietlott-data/data/power655.jsonl, available 1419 records on 2026-11-03. Original raw order contains known anomaly; for Jackpot event sequence this analysis sorts by **numeric draw ID**, not raw row index.
- Verified Jackpot 1 winner count of **2** at #01020 (2024-04-11); actual TOTAL Jackpot pool was **314,186,714,850 VND**, while some historical tables give per-ticket 157,093,357,425 VND. Vietlott: https://vietlott.vn/vi//20140-vietlott-trao-giai-thuong-xo-so-lon-nhat-lich-su-tai-viet-nam/
- Verified winner count **2** at #01074 (2024-08-15); reported per-ticket 19,620,831,975 VND implies pool 39,241,663,950 VND. See https://www.minhngoc.net/ket-qua-xo-so/dien-toan-vietlott/power-6x55/15-08-2024.html
- Winner counts at *other* historical event IDs are NOT individually verified; provisional pool equals listed award for those rows. The 41-event list is **not certified exhaustive**, and the complete prior sales volumes/pot trajectories are unavailable.
- The detailed per-event/pair matrix and provisional prize normalization is in `CHAMPION_X_JACKPOT1_41_EVENT_MONEY_GAP_MATRIX_2026-11-03.csv`, 41 event rows, 40 successive event comparisons.

## Time and prize relationships
- 41 Jackpot 1 winner-event draws, 40 adjacent transitions in observed event list.
- Mean draw-ID gap **22.975**, median **21**, shortest **3**, longest **64**; where event list is incomplete, observed gaps could combine omitted true events.
- Pearson r between **gap in draw IDs** and **total Jackpot pool at the later winner event**: **+0.9052**.
- Pearson r between draw gap and **monetary difference (next winner-event pool minus preceding winner-event pool)**: **+0.7856**.
- Strong correlation is expected from the rollover mechanism: the pot starts from a base after winning, then grows with sales. It does **not** imply the monetary amount causes any specific six-number result.
- Money differences are **between separate Jackpot-winning events**, not within one uninterrupted rolling jackpot; positive and negative differences can occur because each new cycle resets the base.

Selected recent transitions, amounts in billions VND (pooled provisional values):
| Prior winner draw | Next winner draw | Gap draws | Prior pool | Next pool | Difference |
|---|---|---:|---:|---:|---:|
| #01315 | #01333 | 18 | 114.662 | 91.889 | -22.773 |
| #01333 | #01350 | 17 | 91.889 | 83.319 | -8.570 |
| #01350 | #01370 | 20 | 83.319 | 102.863 | +19.543 |
| #01370 | #01384 | 14 | 102.863 | 71.851 | -31.012 |
| #01384 | #01415 | 31 | 71.851 | 199.985 | +128.134 |

## Microfeature correlations vs prize pool
40 subsequent winner events after the first, each annotated by six main numbers and elapsed draw gap. Unadjusted Pearson r between later winner pool and number features:
- Count of numbers 01..31: **-0.4535**.
- Count of numbers 40..55: **+0.3583**.
- Sum of six winning numbers: **+0.3773**.
- Number of adjacent consecutive pairs: **-0.1931**.
- Span (max-min): **+0.0822**.

By prize-pool buckets (post-hoc descriptive, 40 transitions):
| Later Jackpot 1 pool | Events | Mean gap draws | Mean six-number sum | Mean 01..31 count |
|---|---:|---:|---:|---:|
| <=60B VND | 12 | 7.42 | 145.33 | 4.08 |
| (60B,120B] | 13 | 19.69 | 165.77 | 3.38 |
| >120B | 15 | 38.27 | 179.87 | 2.80 |

**Critical confound check:** larger prize pools follow more draws since prior win. If first residualize both prize pool and features against a linear draw-gap term plus calendar-year fixed effects, partial Pearson r values shrink:
- 01..31 count: **-0.2362** (approximate two-sided t reference p≈0.186).
- 40..55 count: **+0.2908** (p≈0.101).
- Sum: **+0.2673** (p≈0.133).
- Adjacent pairs: **-0.0354** (p≈0.845).
- Span: **+0.2326** (p≈0.193).
None establishes robust association. The p-values are approximate OLS partial-correlation references with approximately 31 residual degrees of freedom, not independent/out-of-sample model significance and not corrected for multiple hypothesis tests. The original unadjusted year-stratified prize-shuffle exploratory p was ~.007 for the 01..31 count, but that shuffle does **not control draw gap** and must not be treated as confirmation.

Sensitivity: removing one record at a time changes adjusted low-number correlation from approx **-0.332** to **-0.037**. Significant dependence on an individual event is possible; total sample size is small.

## Tiny signals / fine-grained checks
For **40 consecutive observed Jackpot winner-event pairs**:
- Mean number of common six-main labels between consecutive winner events: **0.725**, versus independent fair draws expected 36/55≈**0.6545**.
- Exactly **2** pairs share at least **three** main numbers. Under independent fair draws P(overlap >=3)≈**1.33294%**, giving an expected ~**0.533** such pairs over 40, and a crude binomial P(at least two)≈**0.10**. Neither is strong, especially after exploration and because these are potentially dependent event-pairs.
- The prior winning draw's **bonus number becomes a main winning number** in the next winner-event draw **1/40** times, compared with fair-draw baseline probability 6/55≈10.91% and expected **4.36** events. A crude binomial lower-tail P(<=1)≈**0.058**, before correcting multiple tests. Not convincing and not a pre-draw predictor.
- The same bonus value repeats on two successive winning events **2/40** times. The reported prize amount's final digits and divisibility are accounting/payout artifacts (especially when multiple winners divide the pool), not ball-drawing signals.

## Interpretation and guardrails
1. A **lottery combination** is uniform under a fair draw independently of rollover, jackpot size, or last winner numbers. The **event that somebody owned the winning combination** is not uniform if player purchases concentrate on popular combinations, and depends strongly on sales volume and advertised jackpot size.
2. Any number-feature association in the subset of winner events can arise from conditioning on winner ownership (selection/collider bias), purchase volume, popularity of number patterns, changes in game rules/sales, or pure noise. It does not imply next draw's six winning numbers become predictable.
3. Do **not** read `P(six-number pattern | Jackpot was won)` as `P(next draw winning pattern | amount currently high)`; those are distinct conditional probabilities.
4. Current sample is only 41 identified events from a third-party table plus a recent cross-check and cannot support strong inferential claims. A decisive next phase needs the full per-draw *official* Jackpot 1 winner count, official total pot, rollover from prior draw, and number of ticket combinations sold, preferably with auto-pick vs manual-pick mix.
5. Keep original R19 Frozen, Hybrid6 and all Champion-X models immutable. No new predictive X variable is justified by the current amount/number study.

## Next data gate
Collect all draws (including **no-winner** draws) with prize pool, official winning ticket counts, minimum guaranteed jackpot and ticket sales proxy. Then compare *likelihood a jackpot is claimed* conditional on prior pot and number-pattern characteristics, including year and sales controls. That can identify **consumer ticket-choice popularity**, which may help avoid prize sharing, but does not increase the probability of a particular combination being drawn.
