# Mega 6/45 strict-past rolling backtest — 624 draws (2026-11-01)

## Provenance and data
- Public source: `vietvudanh/vietlott-data/data/power645.jsonl`, as fetched from GitHub main on 2026-11-01. Git blob reported by the source directory: `4315d019ebc764b2b7e3fbb33255216cefde9c76`.
- 1385 rows of Mega 6/45, first #00198 on 2017-10-25, last #01582 on 2026-10-30.
- Evaluation window: zero-based indices **761..1384** (624 targets), first #00959 dated 2022-10-28, last #01582 dated 2026-10-30.
- For every target i, prediction uses `rows[:i]` only. Score using six actual main numbers in `rows[i]` after prediction. No target leakage. Raw source order used; source completeness and chronological integrity have **not** been independently audited.
- This was an **independent JavaScript implementation of ported Python logic**, not an executed clean-checkout Python PASS.
- Original Power 6/55 R19 Frozen blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0` and Hybrid6 dependency blob `252f6e0e3dad70a80a4b0cf7febe92d5d080e264` have **not** been changed.

## Exact experimental versions
All methods produce six disjoint tickets of six labels each, a total of 36 distinct labels among 1..45. All calculations at target i rely on earlier rows only:
1. **Top-36 F156**: rank 1..45 by descending frequency over last 156 results (ties ascending number), take top 36; split round-robin positions modulo six into tickets.
2. **Hybrid6 Mega port**: execute original Hybrid6 sequence with 45-number label domain: F156 and F30; drop two weak-momentum labels from original top36; promote two from nine outside top36; apply original MAGNUM fixed weight list to the sorted nine currently excluded labels (only first nine weights participate); retain original top-6, rejected, incoming and unique-slot momentum-swap logic; divide resulting 36 labels by index modulo six. The weight list was designed for 19 exclusions in 6/55, so applying its first nine values to 6/45 is experimental and **not** a validated equivalent model.
3. **CrossRank Mega port**: build on Hybrid6 Mega; rank the **nine** remaining excluded labels by descending momentum, and 36 selected labels by descending momentum; use score `(10-rankExcluded)/9 - (37-rankSelected)/36` to greedily apply up to three noncycling swaps with the original tie-break and ticket slot preservation. This changes the R19 denominator and is a NEW ADAPTATION; it must **not** be labeled R19 Frozen or X0.

Validation assertions passed in JS: six six-number tickets, 36 unique selected numbers for every model and every evaluated draw; no errors from the 624-target run. No independent Python clean-checkout pass.

## 624-draw results
| Metric | Top36-F156 | Hybrid6 Mega port | CrossRank Mega port |
|---|---:|---:|---:|
| Selection sum | 2994 | **3031** | 3024 |
| Mean Selection/draw | 4.7981 | **4.8574** | 4.8462 |
| Selection histogram (0..6) | [0,0,9,39,165,267,144] | [0,0,5,33,166,262,158] | [0,0,1,37,161,283,142] |
| Selection >=5 | 411 | 420 | **425** |
| Selection =6 | 144 | **158** | 142 |
| Best-hit histogram (0..6) | [0,124,402,89,9,0,0] | [0,104,411,99,10,0,0] | [0,108,414,90,12,0,0] |
| Best-hit >=3 | 98 | **109** | 102 |
| Best-hit >=4 | 9 | 10 | **12** |
| Best-hit >=5 | 0 | 0 | 0 |
| Ticket jackpot =6 | 0 | 0 | 0 |
| Selection sum Q1..Q4 (156 draws each) | [752,745,757,740] | [756,756,759,760] | [753,746,757,768] |

## Exact fair-draw null
For any predetermined 36 of 45:
- Mean Selection = `6*36/45 = 4.8` hits/draw.
- Expected Selection sum in 624 draws = **2995.2**.
- Probability all six winning labels are in the selected 36 = `C(36,6)/C(45,6) = 0.2391378332`; expected **149.222** Selection 6/6.
- Probability Selection>=5 = `[C(36,5)C(9,1) + C(36,6)]/C(45,6)=0.6557005105`; expected **409.157** over 624.
- Each six-ticket portfolio of distinct combinations has unconditional Jackpot 6/6 probability `6/C(45,6)` per target, expected **0.0004597** jackpots per 624 draws. Zero jackpots is the overwhelmingly likely outcome.
- **No valid evidence of forecast advantage** is established merely by Hybrid6's 158 full-Selection targets versus null 149.2. The port details are arbitrary, historical inspection risks remain, and all methods have very similar performance to chance.

## Decisions
- Walk-forward test protocol preserved.
- Power 6/55 Frozen versions left immutable.
- Mega port is a NEW experimental model family, NOT official X0.
- None is promoted to an actionable forecasting model; user should not interpret retrospective differences as improved lottery odds under a fair independent draw.
- For a reproducible engineering-grade rerun, implement explicit Python scripts for the exact Mega ports, pin dataset SHA and replay per-target tickets, verify clean-checkout and evaluate blinded future targets; do not select model after seeing results.
