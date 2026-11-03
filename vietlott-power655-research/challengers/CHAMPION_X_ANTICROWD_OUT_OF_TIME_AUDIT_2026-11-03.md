# Champion-X — Anti-crowd research, locked out-of-time check (2026-11-03)

## Core question
Can player-number preferences be identified on later historical years without using results to refit, and could such a signature support avoiding shared prizes *conditional on winning*, rather than trying to forecast the ball draw?

## Data and validation
- Power 6/55 winning numbers: `vietvudanh/vietlott-data/data/power655.jsonl`.
- Matched per-draw prize counts: `leoodz/vn-vietlott/results/power6x55.json`.
- Script `champion_x_anticrowd_validation_20261103.py`, action `.github/workflows/champion-x-anticrowd-validation.yml`.
- GitHub Actions completed PASS, run: https://github.com/lamhnb/my-folder/actions/runs/41658601697
- Snapshot SHA256 balls `3668ec0888e8ce6ef7a7bb8d0bc3508c5b2fe97250e1c7922184d1d19239fffd`; prizes `5e7e80423a883da4c70f9e324120ada8690b282d3c779113b1b349640fdba79b`.
- 1419 original draw records, 1447 prize records, 1415 validated matched draw-and-prize records, 32 unmatched. Validation uses exact date plus six mains, validates 3/4/5 counts, drops invalid. These are still third-party scraped records, not an official ticket purchase ledger.
- **Training:** 2017–2023, N=976. **Later chronological evaluation:** 2024–2026, N=439. No slope fitting on 2024–2026. These later years were previously used to explore player-choice associations, so *not a fully virgin hypothesis discovery or prospective holdout*.

## Fixed model
For each already-drawn six-main-number set, let `low31` be the count of balls numbered 01–31. Let normalized prize-4/prize-3 payout concentration metric be:
`r4=(n4/n3)/[P(exactly4)/P(exactly3)]`, with `P(exactly4)/P(exactly3)=0.0478723404`.
Train single-feature OLS `r4_hat = mu + slope*(low31-xmean)`, all parameters learned solely from training years:
- mu = **0.990676987659**.
- xmean = **3.331967213115**.
- slope = **+0.0152109278641** per extra number in 01–31.

Baseline is constant `r4_hat = mu` learned from training years, both scored on later records.

## Evaluated performance
| Period | N | Baseline MSE | low31 model MSE | Relative MSE reduction |
|---|---:|---:|---:|---:|
| Train 2017–2023 | 976 | 0.01274086 | 0.01242498 | 2.479% |
| Test 2024 | 156 | 0.00850896 | 0.00783734 | 7.893% |
| Test 2025 | 155 | 0.01300398 | 0.01252343 | 3.695% |
| Test 2026 | 128 | 0.00739930 | 0.00689488 | 6.817% |
| **All later 2024–2026** | **439** | **0.00977249** | **0.00921709** | **5.683%** |

Test subgroup average actual r4:
- `low31=0..2`: N=110, actual **0.97222**, prediction 0.96641.
- `low31=3`: N=120, actual **0.98204**, prediction 0.98563.
- `low31=4..6`: N=209, actual **1.01526**, prediction 1.00746.

This confirms that the **direction and modest explanatory power** of the lower-tier concentration feature transfer to later historical years under this fixed model. The results do not establish that every exact combination with more low numbers is more popular. The unit of observation is a winning draw and its entire pool of lower-tier tickets.

## Jackpot interpretation and hard limit
- For a fair independent drawing of six numbers, **every distinct six-number ticket has identical top-prize chance = 1/C(55,6)**. For six different tickets, jackpot chance = 6/C(55,6), regardless of labels or overlap.
- A pre-draw ticket popularity ranking, if calibrated on actual ticket choices, could potentially change **expected payout conditional on hitting the top prize** by reducing shared jackpots. Prize lower-tier ratio does *not* identify exact-six combination frequencies; moving directly from observed r4 to a numerical probability that others hold a particular ticket would be an unsupported extrapolation.
- Direction-C constraints conflict: six disjoint 6-number tickets maximize *breadth of distinct-number Selection* and tend to maximize probability of **any** lower-tier prize versus heavily overlapping variants studied. Six anti-crowd tickets composed exclusively of values 32..55 cannot be disjoint because there are only 24 labels in that range. Avoid changing number coverage silently.
- The original 41-event Jackpot-prize-size correlation disappeared after year+rollover-gap adjustment (r near zero). This does not give a clue to which balls will be drawn.
- Historical winner events=60 in matched prize-ledger rows. Current 4/3 concentration ratios, while useful as player-choice diagnostics, do not predict the presence of a Jackpot 1 winning ticket with reliable demonstrated out-of-time discriminative power.
- No Frozen R19 / Hybrid6 / Champion change, and no model promotion. Full Python player-choice audit PASS is separate from Frozen Power clean-checkout PASS, which remains unverified.

## Research next gate: a decision-focused popularity model
To justify a practical anti-crowd portfolio, next collect an independent **direct ticket-combination frequency** sample (or credible anonymized sales histogram), including autosel vs manual and changing prize pools. Predict the number of other holders for a *specific pre-issued six-number combination*, not the after-the-fact 4/3 ratio of a draw. Evaluate exact-ticket holdout calibration, compare with uniform ticket ownership and popular birthday/visual sequences, and score conditional top-prize payout after realistic sharing rules. Never claim a higher ball-draw or Jackpot hit probability from this approach.

The current result is a validated *descriptive behavioral signal on later historical years*, not a lottery forecasting breakthrough.
