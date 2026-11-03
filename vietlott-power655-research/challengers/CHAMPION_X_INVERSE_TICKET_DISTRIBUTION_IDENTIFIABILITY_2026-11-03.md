# Champion-X — Inverse Ticket Distribution: identifiability boundary and Jackpot2 sixth-number pilot (2026-11-03)

## Research question
Can public aggregate prize-tier winner counts be inverted into the popularity of each exact six-number Power 6/55 ticket, so as to reduce jackpot-sharing exposure without pretending to predict winning balls?

## Structural identifiability theorem (negative)
For a given draw with main winning set W of size six and bonus b outside W, let x_T be the (unobserved) number of tickets purchased for each of the C(55,6)=**28,989,675** six-number combinations T. The official payout summary provides only the aggregate sums of x_T in prize categories (Jackpot1, Jackpot2, first, second, third). The full prize-category multiplicities among all combinations for a specified winning set are:
- exactly six main numbers: 1 candidate (Jackpot1);
- exactly five main numbers: C(6,5)C(49,1)=294 candidate combinations, of which **6** include bonus b (Jackpot2) and **288** exclude bonus b (First);
- exactly four main numbers: C(6,4)C(49,2)=17,640;
- exactly three main numbers: C(6,3)C(49,3)=368,480;
- exactly 0,1,2 main matches: 13,983,816; 11,441,304; 3,178,140, respectively.
Even with perfect payout reporting, knowing five aggregate prize-class sums does **not** identify the millions of x_T. For example, draw W={01,02,03,04,05,06}, bonus=07: both tickets `01 02 03 08 09 10` and `04 05 06 11 12 13` have exactly three main matches and no bonus, so moving an arbitrary number of sold copies from one to the other leaves **every class-level payout count unchanged**. This is an explicit nonidentifiability witness. The same problem applies to other ticket-pair choices within each prize class.
Across multiple draws, purchases vary and are not a single fixed x_T vector; inferring persistent exact-ticket probabilities across draws requires assumptions on stationarity or a parametric behavioral choice model not identifiable from observed payout counts alone. Exact six-set popularity is **not proven**.

## An identifiable aggregate contrast: Jackpot2 vs Prize1
The Power rules award Jackpot2 to five main matches **plus** bonus and First to five main matches **without** bonus; therefore, conditional on a uniformly selected six-number ticket containing exactly five main matches:
`P(J2 | exactly five main matches) = 6/294 = 1/49`, First=48/49, reference `J2:First=1:48`.
This ratio cancels much of the total tickets sold, and by stratifying on the drawn bonus number can test a limited form of *population choice preference for the sixth number*.

## Pinned reproducibility
- Script `champion_x_j2_sixth_number_identifiability_20261103.py`, workflow `.github/workflows/champion-x-j2-identifiability.yml`.
- **GitHub Actions PASS**: https://github.com/lamhnb/my-folder/actions/runs/41662992321
- Balls source SHA256 `3668ec0888e8ce6ef7a7bb8d0bc3508c5b2fe97250e1c7922184d1d19239fffd`; prize source SHA256 `5e7e80423a883da4c70f9e324120ada8690b282d3c779113b1b349640fdba79b`.
- 1419 number records, 1447 prize records; exactly matched date + six mains for **1415 valid draws**, with 32 unmatched; same historical data used in earlier research.
- Train 2017–2023 **976 draws**; evaluate later years 2024–2026 **439 draws**. Prior investigation had already explored number<=31, so **not a wholly untouched theory-validation sample**.
- Aggregated observed across all 1415 draws: **421 Jackpot2 winning tickets** and **20,408 First winning tickets** among **20,829 five-main matching purchased tickets**. Observed `P(J2 | five mains)=421/20829=0.0202122`, close to uniform reference **1/49=0.0204082**; expected Jackpot2 count **425.08** (simple grouped binomial reference). Naive z to this null = −0.200; dependence and heterogeneity require cautious interpretation.

## Bonus-number preferences
| Sample | Bonus class | J2 | First | 5-main exposures | Conditional P(J2) | J2 vs uniform expected ratio |
|---|---|---:|---:|---:|---:|---:|
| Train 2017–23 | 01–31 | 167 | 6633 | 6800 | 2.4559% | 1.203 |
| Train 2017–23 | 32–55 | 96 | 5179 | 5275 | 1.8199% | 0.892 |
| Test 2024–26 | 01–31 | 95 | 4579 | 4674 | 2.0325% | 0.996 |
| Test 2024–26 | 32–55 | 63 | 4017 | 4080 | 1.5441% | 0.757 |

The high-vs-low direction persists descriptively. However, using the training subgroup rates to predict conditional Jackpot2 counts in later years achieved **test logloss 0.09050623** versus **0.09049018** for uniform reference (and Brier **0.01773087** versus **0.01772870**). Thus the **absolute calibrated model is slightly worse than the parameter-free uniform model**, though it improves versus training-era unconditional fitted rate.
Relative preference may be real, but cannot be called out-of-time success on the primary proper scoring rule.

Year-by-year 2024–26:
- 2024: bonus 01–31 J2=41 of 1897 five-main tickets (2.1613%), >31 J2=26 of 1373 (1.8937%).
- 2025: bonus 01–31 J2=29 of 1688 (1.7180%), >31 J2=24 of 1465 (1.6382%).
- 2026: bonus 01–31 J2=25 of 1089 (2.2957%), >31 J2=13 of 1242 (1.0467%).
These are low event counts, unverified for detailed sampling mechanism and are not an exact ticket frequency inversion.

## Decisions
1. **No exact-six reconstruction from prize-tier aggregates**: mathematically nonidentifiable absent strong additional assumptions or direct ticket-sales histogram. Mark as infeasible for production Anti-Crowd scorer.
2. **A limited behavioral indicator survives as a research candidate**: J2/First ratio differs by bonus-number band, consistent with a possible sixth-ball preference. But current train-fitted absolute probability model fails to beat uniform expectation in later-year logloss/Brier. Do not promote.
3. If pursuing more rigorous estimation, register a new prespecified hypothesis (e.g. within-draw matched contrasts for individual bonus numbers conditional on composition of other remaining numbers), then test on genuinely future data **without threshold/number retuning**, with uncertainty for draw-clustered counts and varying sales.
4. Even with knowledge of exact-ticket popularity, **the fair draw probability is 1/C(55,6)** for every exact combination. Only the prize amount retained *conditional on a win* might change with other holders.
5. R19 Frozen, Hybrid6 and all registered Champions remain untouched. Python research script PASS does NOT certify a Frozen Python clean-checkout replay.

## References
- Power prize conditions: https://tracuuxoso.vn/vietlott/power-6-55 and https://tramso.vercel.app/san-pham/power
- Lottery number preference behavioral study: https://www.cambridge.org/core/journals/judgment-and-decision-making/article/number-preferences-in-lotteries/47BA27051627CEED421AD3AEE255521E
