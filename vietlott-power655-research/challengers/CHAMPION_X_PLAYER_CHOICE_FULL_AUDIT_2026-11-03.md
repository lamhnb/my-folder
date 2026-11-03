# Champion-X — Full historical player-choice and Jackpot prize-gap audit (2026-11-03)

## Executive finding
**Two phenomena must be separated.** (1) Lower-tier prize counts show a consistent, modest concentration effect for draws with many winning balls numbered 01–31: players appear to select such sub-combinations nonuniformly. (2) The previously noticed "large Jackpot ↔ fewer numbers 01–31" relationship **collapses after controlling for both calendar year and the draw gap since the previous Jackpot-winning event**. No new forecastable winning-ball signal or validated exact six-number ticket-popularity score emerged.

## Sources and audited pipeline
- Detailed historical **winning-ticket counts for Jackpot1, Jackpot2, prizes 1/2/3**: https://github.com/leoodz/vn-vietlott/blob/main/results/power6x55.json
- Ball outcomes and draw identities: https://github.com/vietvudanh/vietlott-data/blob/main/data/power655.jsonl
- Official Power 6/55 prize criteria: https://info.vietlottsms.vn/game_power.html .
- Research literature: https://academic.oup.com/jrssig/article/20/1/31/7034183 and https://www.cambridge.org/core/journals/judgment-and-decision-making/article/number-preferences-in-lotteries/47BA27051627CEED421AD3AEE255521E .
- Script: `champion_x_player_choice_prize_tier_audit_20261103.py` in this research directory; workflow: `.github/workflows/champion-x-player-choice-audit.yml` on research branch. Latest execution **GitHub Actions PASS** on commit `2b44afcbffec888fed1636f179b41e16e856ebec`; run https://github.com/lamhnb/my-folder/actions/runs/41657448783 .
- Original raw rows: 1419 from number source, 1447 prize-source records. **1415** distinct dates passed exact date and six-main-number match and prize-count requirements; **32** prize-source rows rejected for nonunique/unmatched alignment. Invalid source values are *not* treated as zero winners. The historical out-of-order anomaly in the original ball JSONL is not silently repaired.
- SHA256 of number and prize source files as collected in the original full run: `3668ec0888e8ce6ef7a7bb8d0bc3508c5b2fe97250e1c7922184d1d19239fffd` and `5e7e80423a883da4c70f9e324120ada8690b282d3c779113b1b349640fdba79b`. Workflow artifact provides time-specific CSV/JSON/Markdown. Source may update in later runs.
- Source scraper contains concatenated currency strings. Initial monetary output was **invalid**. This was corrected by extracting only the first properly formatted currency amount; known #01415–#01418 Jackpot1 amounts now match independent published references **exactly**. All earlier pre-correction monetary correlations are discarded.

## Full dataset: 1415 matched draws, 60 actual Jackpot1 winning events
- 60 draws had at least one Jackpot1 owner; two events had two winning tickets (#01020, #01074).
- 59 transitions between winner events, mean **21.966** draw-ID positions.
- Historical winning amount at later event (total pool provisionally = reported per-ticket prize × count) correlates with elapsed draw gap **r=+0.7698**. This is expected from rollover mechanics and sales, not a causal relationship between money and winning balls.

## Number-pattern vs jackpot amount (the central falsification)
Among 59 later winning events, draw winning six-number set features:
- Raw Pearson correlation of total jackpot amount with count of winning numbers in **01–31**: **−0.2703**.
- After controlling for calendar year alone: **−0.2783**.
- **After controlling for calendar year AND elapsed draws since prior winning event: −0.00472**.
- Same year+gap adjusted correlation for winning six-number *sum*: **−0.00177**.
This strongly weakens the prior 41-event headline that larger jackpots "favor higher numbered winners". The apparent trend is explained by changing draw gaps and sample selection; **no evidence of a predictive relationship remains in this linear conditional check**. It does not prove all nonlinear effects absent.

## The independently interesting signal: relative sub-combination popularity
Power 6/55 uniform-ticket reference probabilities:
- `P(exactly 3 main matches)=C(6,3)C(49,3)/C(55,6)=0.0127107323556`.
- `P(exactly 4 main matches)=C(6,4)C(49,2)/C(55,6)=0.0006084925064`.
- `P(exactly 5 main matches excluding bonus)=6*48/C(55,6)=0.00000993457153`.
- Uniform `P4/P3=0.0478723404`.
Define **normalized 4:3 = (observed count of 4-match winners / observed count of 3-match winners) / (P4/P3)**. 1 means the basic uniform-combination expectation for the given ratio, not an individually calibrated jackpot claim.

| Count of drawn main balls numbered 01–31 | Draws | Mean normalized 4:3 | Jackpot1 owner events |
|---|---:|---:|---:|
| 0–2 | 346 | **0.9697** | 10 |
| 3 | 423 | **0.9812** | 19 |
| 4–6 | 646 | **1.0113** | 31 |

Difference in mean normalized ratio between high and low groups ≈**4.3% relative**. Year-adjusted Pearson r(low31,normalized4)=**+0.18522**, year-stratified 3,000-shuffle exploratory two-sided p≈**0.000333**. The association has the same positive direction in all ten individual calendar years (weakest 2020 ~+0.036; strongest 2024 ~+0.312). Multiple feature comparisons and historical inspection remain caveats. This effect is a **player ticket-selection distribution signature**, not a winning-ball forecast.

The count low31 vs Jackpot1-winning-draw indicator is only **r=+0.0301** after year adjustment, year-stratified exploratory p≈**0.2483**. Thus lower-tier popularity cannot automatically be extrapolated to exact six-number Jackpot ownership or prizes shared.

## Previously advertised jackpot value and purchase-volume proxy
Use previous matched draw's displayed Jackpot1 amount when the prior draw had no winner, or the guaranteed **30 billion VND** base after a prior Jackpot winner. This is an approximate **pre-draw advertised-pot proxy**, NOT an independently observed ticket-sales series. Matched contiguous prior draws available for 1411 observations.
- Year-adjusted corr(pre-draw prize proxy, `3-match winners / P3` sales-equivalent) **+0.7431**. Jackpot excitement plausibly attracts purchase volume; note the sales-equivalent is distorted by nonuniform number preferences and cannot be treated as official sales.
- Year-adjusted corr(pre-draw prize proxy, normalized4 ratio) **+0.0161**, approximately zero.
- Year-adjusted corr(pre-draw prize proxy, Jackpot1-winning-draw indicator) **+0.0608**, weak; this sample is observational and events are rare.
- Approximate pre-draw pot bands:
  - <=60B: n=743, 24 winning-owner events, sales-equivalent mean ~1.04 million, normalized4 ~0.9887.
  - 60–150B: n=509, 23 winning-owner events, sales-equivalent mean ~1.65 million, normalized4 ~0.9963.
  - >150B: n=159, 13 winning-owner events, sales-equivalent mean ~2.80 million, normalized4 ~0.9959.
- Correlations of count 01–31 with normalized4 within these pot bands: +0.177, +0.194, +0.237, respectively. This exploratory pattern has **not** been subjected to an independent interaction significance test; do not claim the Jackpot causes it.

## Exact-six ownership heuristic and microfeatures
Treat the 3-match count / P3 as a **sales-equivalent**, then assume hypothetical uniform independently selected six-number tickets to estimate chance at least one owner:
`1-exp(-sales_equivalent / C(55,6))`. Summed over 1415 observed draws: predicted **68.72 winner events** vs observed **60**. Differences may reflect biased number selection, approximation error or variable ticket sales; this is NOT a calibrated probability and not an actionable betting rule.
- By drawn low31 count, observed vs approximate expected: 0–2: 10 vs 15.37; 3: 19 vs 20.13; 4–6: 31 vs 33.22. Small counts and model assumptions prevent strong claims.
- Between the 59 consecutive observed winning events, mean number of overlapping *main* labels is **0.7288**, vs fair-draw baseline `36/55≈0.6545`; three pairs share at least three main labels. Previous event's bonus is among next event's six mains **3** times vs expected **6.44**, and bonus repeats **2** times. These were opportunistically inspected and are not predictive evidence.

## Decision
1. **Validated as an interesting behavioral signature:** prize-tier winner count ratios contain nonuniform population number-selection information (01–31 bias). Consistent with published literature, not uniquely diagnostic for any one exact ticket.
2. **Rejected as a ball-prediction claim:** larger jackpot amount does not meaningfully correlate with low-ball frequency after accounting for calendar year and time since preceding jackpot-winning event.
3. **No change to X0 R19 Frozen, Hybrid6 or Champions.** No new Selection/Allocation algorithm is promoted. A future share-avoidance model would need exact-combination ticket sales or more direct purchase distribution and independent prospective testing; high-risk naive inferences about Jackpot ownership are not permitted.
4. The historical dataset and extracted money are secondary; to certify, reconcile dates, rules and jackpot counts against official Vietlott ledgers. No Python clean-checkout PASS for the original Frozen Power model is claimed; the **Python prize-tier research script** passed GitHub Actions only.
