# Champion-X — Three-band sixth-number behavior test (2026-11-03)

## Objective
Explore whether public Power 6/55 **Jackpot2 vs First-prize** winning-ticket counts reveal reproducible human sixth-number preferences in three predetermined bands (01–12, 13–31, 32–55), rather than infer exact six-number tickets or assert a ball-drawing advantage.

## Frozen-research constraints
Original R19 Frozen and Hybrid6 were not modified; no Champion-X algorithm promotion. The number-band idea (birthdays, <=31) had been explored previously, so testing on years 2024–26 is chronologically later than *model training* but **not a previously untouched hypothesis holdout**.

## Reproduction and source control
- Script: `vietlott-power655-research/challengers/champion_x_j2_three_group_20261103.py`.
- Workflow: `.github/workflows/champion-x-j2-three-group.yml`.
- GitHub Actions **PASS**: https://github.com/lamhnb/my-folder/actions/runs/41666332613 .
- Balls: https://github.com/vietvudanh/vietlott-data/blob/main/data/power655.jsonl, snapshot SHA256 `3668ec0888e8ce6ef7a7bb8d0bc3508c5b2fe97250e1c7922184d1d19239fffd`.
- Payouts: https://github.com/leoodz/vn-vietlott/blob/main/results/power6x55.json, snapshot SHA256 `5e7e80423a883da4c70f9e324120ada8690b282d3c779113b1b349640fdba79b`.
- 1419 historical ball rows; 1447 prize rows; 1415 matched by exact date and six main-number labels; 32 not aligned. 976 training draws (2017–23); 439 later-year test draws (2024–26).
- Jackpot2 means five main hits **plus the bonus**; First means five main hits **without bonus**. The 49 available sixth labels exclude six drawn main numbers, and the diagnostic script explicitly tabulates remaining eligible labels for each band's actual draw.
- Under uniform choice, exactly five main matches correspond to 6*49 = 294 six-number combinations, of which 6 contain the specific bonus, and 288 do not. Therefore `P(Jackpot2 | exactly five main matches)=1/49=2.040816%`, or Jackpot2:First=1:48. This is a **null expectation conditional on five matches**, not a model of ball frequency.
- Raw cohort probabilities shrunk toward uniform at fixed strength 400 pseudo-exposures, chosen without using evaluation outcomes.

## Band-specific test results
| Bonus band | Train n(5-main ticket exposures) | Train J2 | Train J2 share | Later test n exposures | Test J2 | Test share | Test J2/uniform |
|---|---:|---:|---:|---:|---:|---:|---:|
| 01–12 | 2662 | 60 | 2.2539% | 1848 | 36 | **1.9481%** | 0.955 |
| 13–31 | 4138 | 107 | 2.5858% | 2826 | 59 | **2.0878%** | 1.023 |
| 32–55 | 5275 | 96 | 1.8199% | 4080 | 63 | **1.5441%** | 0.757 |
| Total | 12075 | 263 | 2.1781% | 8754 | 158 | **1.8049%** | 0.884 |

Training learned probabilities after shrinkage:
- 01–12: 0.0222610272
- 13–31: 0.0253775375
- 32–55: 0.0183547604

## Proper-scoring comparison on 2024–2026 (8754 five-main winning-ticket exposures)
| Frozen comparator | Logloss (lower better) | Brier (lower better) |
|---|---:|---:|
| Uniform 1/49 | **0.0904901759** | **0.0177286956** |
| Train-fitted unconditional rate | 0.0906991319 | 0.0177373517 |
| 3-band model trained <=2023 | 0.0904657354 | 0.0177290700 |

3-band: logloss improves by **+0.00002444** over uniform, while Brier **worsens by 0.0000003744**. This is **mixed**, negligible evidence, not a verified calibrated breakthrough.

Test splits:
- 2024: 3-band logloss **0.09999183**, uniform **0.09993747** (worse).
- 2025: 3-band **0.08598822**, uniform **0.08569181** (worse).
- 2026: 3-band **0.08315869**, uniform **0.08372767** (better).
2026 improvement may simply reflect noise or shifts in ticket buying patterns; do not choose model or thresholds post hoc from it.

## Why this is not the hidden jackpot solution
1. Only aggregate **conditional subcombination preference** can be studied: a particular J2/First ratio at an already-drawn main-six and bonus label does not reveal the frequency of any exact six-number purchased ticket.
2. Three bands show a directional concentration difference, but lack stable proper-scoring superiority across evaluation years. Temporal regime drift matters.
3. Ordinary jackpot-winning number probabilities are identical for all six-number combinations under a fair draw: `1/C(55,6)`. A potential human preference signal cannot change draw mechanics.
4. All number- or bonus-derived data on a target draw are used **after it is drawn** to diagnose other people's purchased tickets; this is not pre-draw knowledge about which main or bonus will appear.
5. Exact-ticket popularity inference requires direct anonymized purchase histograms, or a carefully tested identifiable *parametric* choice model with independent ticket-holding observations. Avoid promoting a fragile descriptive signal to an Anti-Crowd selection engine.

## Next credible gate
Freeze the observed 3-band hypothesis *as a descriptive question only* and monitor new, genuinely future draws' J2/First ratios. If future samples consistently improve proper-scoring versus the **uniform 1/49** reference under a preregistered temporal horizon, consider further data collection on player ticket preferences. Keep Jackpot-sharing strategy separate from Jackpot-hit forecasting.

**Decision: Research-only; NO GO for changes to X0, R19 Frozen, Hybrid6 or ticket allocation.**
