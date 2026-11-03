# Champion-X — Player-choice signal from prize-tier counts (pilot, 2026-11-03)

## Executive conclusion
The newly identified dataset `leoodz/vn-vietlott/results/power6x55.json` contains *draws without Jackpot winners*, jackpot pool and 3/4/5-match prize winning-ticket counts, unlike the original `vietvudanh/vietlott-data/data/power655.jsonl` which contains balls only. This is the proper route to study **human ticket choice** and prize sharing. It does not forecast the ball draw.

## Sources / reproducibility
- Prize source: https://github.com/leoodz/vn-vietlott (README shows fields `prizes.giai_ba.count`, `giai_nhi.count`, `giai_nhat.count`, `jackpot1.count`, `jackpot1.amount`).
- Main-ball source: https://github.com/vietvudanh/vietlott-data/blob/main/data/power655.jsonl .
- Date/ball and payout verification for recent draws: https://kqxsviet.vn/vietlott/power-655/ky-01415 , https://kqxsviet.vn/vietlott/power-655/ky-01416 , https://kqxsviet.vn/vietlott/power-655/ky-01417 , https://kqxsviet.vn/vietlott/power-655/ky-01418 and https://www.minhngoc.net.vn/ket-qua-xo-so/dien-toan-vietlott/power-6x55/03-11-2026.html .
- Research methods: https://academic.oup.com/jrssig/article/20/1/31/7034183 (using lower-tier prize winner counts as proxies for nonuniform player number choice), and https://www.cambridge.org/core/journals/judgment-and-decision-making/article/number-preferences-in-lotteries/47BA27051627CEED421AD3AEE255521E (birthdates and visual preference).
- `champion_x_player_choice_prize_tier_audit_20261103.py` fetches both sources and joins rows on exact draw date and six main numbers; GitHub Actions uploads CSV/JSON/Markdown.
- Exclude #01411: secondary site displays **0 winners** across all lower prizes and no Jackpot growth, which is likely missing data; exclude #01412: no prize breakdown exposed. Do not interpret these as zero demand. This pilot uses 11 other observed draws: #01407–#01410 and #01413–#01419 inclusive.

## Exact uniform-selection reference ratios
For a ticket chosen uniformly over `C(55,6)=28,989,675` possible combinations and a specified uniform winning set:
- `P(exactly 3 main matches)=C(6,3)C(49,3)/C(55,6)=0.01271073236`.
- `P(exactly 4 main matches)=C(6,4)C(49,2)/C(55,6)=0.0006084925064`.
- `P(exactly 5 main matches and no special)=6*48/C(55,6)=0.00000993457153`.
- `P(4)/P(3)=0.0478723404`; `P(5 nonbonus)/P(3)=0.00078158923`.
- `Normalized4=(number of 4-match prizes/number of 3-match prizes)/(P4/P3)`. This ratio cancels some ticket-volume effects and may reflect relative popularity of sub-combinations, though no single ticket sales number is identified. `Normalized5` defined similarly.
- `number of 3-match winners / P3` is a **sales-equivalent proxy**, not official ticket count because player-number choices are nonuniform.

## Verified 11-draw pilot
| Draw | 3-match prizes | 4-match | 5-match (not bonus) | Normalized4 | Normalized5 |
|---|---:|---:|---:|---:|---:|
| #01407 | 45150 | 2310 | 42 | 1.069 | 1.190 |
| #01408 | 34621 | 1614 | 25 | 0.974 | 0.924 |
| #01409 | 38563 | 1777 | 35 | 0.963 | 1.161 |
| #01410 | 31122 | 1333 | 31 | 0.895 | 1.274 |
| #01413 | 37037 | 1779 | 20 | 1.003 | 0.691 |
| #01414 | 45639 | 2469 | 36 | 1.130 | 1.009 |
| #01415 | 43703 | 1818 | 24 | 0.869 | 0.703 |
| #01416 | 22422 | 1197 | 29 | 1.115 | 1.655 |
| #01417 | 16183 | 837 | 18 | 1.080 | 1.423 |
| #01418 | 17591 | 822 | 10 | 0.976 | 0.727 |
| #01419 | 19076 | 1013 | 19 | 1.109 | 1.274 |

`Normalized4` ranges from 0.869 to 1.130 in these 11 draws (mean ~1.017). On only 11 observations its raw Pearson correlation with number of winning balls <=31 is ~+0.104; with six-number sum ~+0.014. Thus there is **no clear association with the birthdate-range feature** in this small, nonrandom pilot. The large variation in raw 3-match winner counts is due to a combination of changing ticket volumes and the popularity of numbers; it is not a direct sales estimate.

**Important contrast:** #01415 had a genuine Jackpot 1 winning ticket, even though its normalized 4/3-match ratio was among the lowest (~0.869). Jackpot winner ownership is about the *exact six-number combination*, which is not recoverable from one aggregate ratio alone. It is invalid to claim an exact-combination popularity score from the 3/4/5-match counts.

## Full historical audit / quality gates
An independent full-source audit script is now available on the research branch and designed to:
1. Fetch both public sources, record SHA256, validate draw date and six-main-ball alignment.
2. Reject invalid/missing/zero prize count anomalies and duplicate dates; distinguish missing from genuine zero jackpot owners.
3. Calculate exact theoretical prize-tier ratios, normalized tiers and sales-equivalent proxy for all matched dates.
4. Compare simple number-pattern indicators to `Jackpot1 count > 0` and tier ratios with calendar-year controls and a year-stratified permutation diagnostic.
5. Write artifact CSV, JSON and Markdown; do not change Frozen Power models.

This pilot **does not claim the complete dataset has been tested** until its CI run completes and log/results pass inspection. The methods are exploratory and no statistical evidence has yet been found that jackpot pool size changes winning ball probabilities.

## Next validation target
After full historical data quality gates pass, test whether lower-tier winner-count ratios predict **someone already owning the winning combination** after controlling for year, prize pool and approximate volume; compare on a truly later holdout. This is a theory of *ticket choice / prize splitting*, not an algorithm for forecasting the six balls. Do not touch X0 Frozen, R19 Frozen or Hybrid6.
