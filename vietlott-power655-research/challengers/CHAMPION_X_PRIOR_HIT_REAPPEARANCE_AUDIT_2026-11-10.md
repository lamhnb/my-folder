# Champion-X — Prior correct selection reappearance audit (2026-11-10)

## Design
- Data: vietvudanh/vietlott-data/data/power655.jsonl Git blob 5dbd6992ed278e33b0db24c2d0d95b2198d89d77; 1421 rows through #01421. Preserve original raw order, including known anomaly.
- X0 Frozen: R19 blob a7ebf4fa5216e1bfd4906087e04555044d3e58f0; Hybrid6 blob 252f6e0e3dad70a80a4b0cf7febe92d5d080e264. Replayed by independent JavaScript translation (not Python clean-checkout PASS), strict-past rows[:i], i=789..1412.
- Replay matched selection histogram [0,7,59,140,215,150,53], total 2473.
- At each anchor draw i, groups: A = selected36 intersect winning6; B = selected36 minus winning6; C = excluded19 minus winning6. Group C explicitly excludes winning labels; therefore A vs C is **not** a like-for-like comparison conditional on current draw outcome. Primary exploratory contrast A vs B also conditions on winning status and can have distinct sampling properties. A properly matched null should compare A to the other current-draw winning labels not selected by X0, or randomize membership preserving group sizes, and simulate complete fair histories.
- For horizon h, success = a label occurs at least once among six main numbers in any of next h draws. Horizons [1,2,3,5,10]. No horizon chosen based on outcomes for promotion.

| h | A successes/denominator | B successes/denominator | C successes/denominator | fair independent P(at least once) |
|---:|---:|---:|---:|---:|
| 1 | 278/2473 | 2208/19991 | 1132/10585 | 0.10909091 |
| 2 | 526/2473 | 4180/19991 | 2130/10585 | 0.20628099 |
| 3 | 712/2473 | 5958/19991 | 3025/10585 | 0.29286852 |
| 5 | 1089/2473 | 8916/19991 | 4564/10585 | 0.43873630 |
| 10 | 1695/2467 | 13770/19925 | 7240/10553 | 0.68498306 |

For horizon 10, only 622 anchor draws have complete future observations; horizons 1..5 include 624 anchors. Future draws were used for **scoring only** and not for X0 prediction.

## Interpretation
A has 11.24%, 21.27%, 28.79%, 44.04%, 68.71% at h=1,2,3,5,10. B has 11.04%,20.91%,29.80%,44.60%,69.11%. No stable positive gap. All numbers remain near fair-draw reference. These are descriptive percentages, not calibrated p-values: observations overlap across horizons and anchor draws, and group membership depends on historical X0 and current outcome. This window was reused extensively for development; no OOS advantage is established.

## Next gate
Calibrate A-B contrasts with a seeded full-history Monte Carlo under the fair-draw null, including exact same strict-past X0 algorithm, or use an appropriately defined within-anchor permutation test. Add a matched comparator of currently winning labels excluded by X0. Control for five horizons and prior hypothesis exploration. Freeze any proposed rule and test on genuinely future unseen draws.

Frozen files untouched; no official tickets modified.
