# Champion-X — Jackpot 1 winner-occupancy vs winning-number shape (2026-11-03)

## Research question
Are winning six-number combinations different in **draws where at least one person actually owns a Jackpot 1 winning ticket**? This is fundamentally different from asking whether a combination is more likely to be drawn. If all possible draws are uniform, every particular six-number combination has identical drawing probability. The indicator “a player won” also depends on how many tickets were sold and **which combinations players chose**.

## Sources and snapshot
- Public original Power 6/55 draw records: `vietvudanh/vietlott-data/data/power655.jsonl` from GitHub, 1419 rows through #01419 on 2026-11-03, original-order anomaly retained.
- Jackpot winner-list from 1682xoso `https://1682xoso.com/thong-ke-vietlott/power-6-55` listing Jackpot 1 winners from 2020-10-31 onward through #01384 2026-08-13.
- Added jackpot #01415 (2026-10-24) verified by VnExpress `https://vnexpress.net/jackpot-gan-200-ty-dong-co-nguoi-trung-thuong-5136482.html`.
- Other supporting context: `https://www.cambridge.org/core/journals/judgment-and-decision-making/article/number-preferences-in-lotteries/47BA27051627CEED421AD3AEE255521E`, documenting player preference for birthdates and situationally salient numbers. Also `https://rss.onlinelibrary.wiley.com/doi/full/10.1111/j.1740-9713.2012.00540.x` on how popular number combinations can increase jackpot sharing.
- **Status: third-party historical winner list is not an official exhaustive audited extraction**. The 41 identified Jackpot 1 events are a subset; do not assume omitted draws had no winners unless verified from official prize tables.

## Event sample
41 Jackpot 1 draw IDs:
`1384,1370,1350,1333,1315,1297,1253,1249,1215,1169,1139,1130,1105,1074,1070,1032,1020,966,954,951,917,878,856,837,816,783,779,755,749,714,689,669,664,600,587,572,561,525,522,496,1415`.

All IDs and dates were matched to original-source draw records. Their study time span is 2020-10-31 through 2026-10-24 inclusive. Same-period original-source pool has 920 draw records. Winner-sample counts by year: 2020:2, 2021:6, 2022:8, 2023:7, 2024:6, 2025:5, 2026:7.

## Matched-year randomization method
For each selected six-main-number draw compute features:
- count of numbers <=31;
- indicator all six <=31;
- count of numbers >=40;
- sum of six numbers;
- count of numerical consecutive adjacent pairs;
- max minus min (range).

Counterfactual controls: for each year, sample the same number of draws as its observed winner-event count without replacement from all recorded draws in that year. Pool over years and repeat 15,000 times using deterministic 32-bit LCG PRNG seed `294111`, recurrence `seed = (1664525*seed + 1013904223) modulo 2^32`. This controls only for year, **not for ticket-sales volumes, rollover amounts, draw-specific player selection, or jackpot pool size**. Two-sided Monte Carlo p-values are approximately `2*min(P(T<=observed),P(T>=observed))` capped at 1, with +1 correction.

| Feature | Actual mean across 41 winner-event draws | Matched-year null mean | Exploratory two-sided p |
|---|---:|---:|---:|
| Numbers <=31 | 3.39024 | 3.34634 | 0.8613 |
| All six <=31 | 0.02439 | 0.03020 | 1.0 |
| Numbers >=40 | 1.56098 | 1.78045 | 0.1977 |
| Sum of six main numbers | 164.85366 | 169.05825 | 0.4473 |
| Number of adjacent consecutive-number pairs | 0.48780 | 0.49791 | 1.0 |
| Span max-min | 39.34146 | 39.75226 | 0.7394 |

No tested feature shows meaningful separation at conventional statistical thresholds. These multiple retrospective feature checks should not be used to promote a forecasting rule.

## Central interpretation
1. **Draw probability**: For a fair game, any specified six-main-number combination has chance 1/C(55,6) per draw, independently of public number preferences.
2. **Winner occurrence**: A draw having at least one Jackpot 1 claim may depend on tickets sold, concentration of human number choices, autopick behavior, jackpot value and public interest. A number pattern could correlate with the *probability someone already holds that ticket* without affecting its draw probability.
3. **Prize sharing**: Depending on ticket popularity, avoiding commonly played combinations could potentially reduce the chance of splitting a top prize if that combination wins. It does not make a ticket more likely to win. Real operational value would require sales/combination-frequency data and actual rules for splitting prizes.
4. A high jackpot or growing sales volume can increase how often a winner appears **without changing which six-number combination gets drawn**.
5. The sample uses public third-party evidence; it is not fully audited and no official full winner-count series or volume sold was ingested. Therefore there is **no evidence from this sample** that winner occurrence itself predicts the next draw's six numbers.
6. No modifications to Frozen R19, Hybrid6, Champion-X variants or registered Champions. This is exploratory social/behavioral research, not a Selection/Allocation algorithm promotion.

## Next proper data gate
Join every Power 6/55 draw with the official `Jackpot 1 number_of_winning_tickets` field, `Jackpot 1 value`, jackpot rollover duration, and number of ticket combinations sold (when available); verify source/ID alignment and payout records. Then test `P(any jackpot winner | number-pattern proxies, tickets sold, jackpot size, year)` using strictly past/out-of-period validation. This can study **player choice/popularity**, not forecast winning ball draws. Recheck any apparent number-popularity signal against a year-matched negative control and correct for multiple comparisons.
