# B1 Adaptive Replacement — Momentum 30 (experimental challenger)

## Status
- **Challenger / exploratory**. B1 v1.0.0 remains Champion.
- This branch adds a standalone strict-past backtest script. Existing B1, B7 and other historical versions remain untouched.
- Evaluation period: draws **#00789–#01413**, 624 draws, 6 tickets per draw.
- Input: public historical `power655.jsonl` with ordered records containing six main numbers and a seventh special number.

## Algorithm
1. For each target draw, compute six-main-number counts on the **156 preceding draws only**. Sort descending frequency, tie-break ascending numeric label.
2. Take B1 top 36 and create six tickets with Stride 6.
3. Compute counts on the **30 preceding draws only**. Define `momentum(n) = F30(n)/30 - F156(n)/156`.
4. Remove **two** numbers with lowest momentum from the 36 B1 candidates, tie-break lower F156 then ascending number.
5. Add **two** numbers with highest momentum from ranks 37–55, tie-break higher F156 then ascending number.
6. Replace removed labels in their existing ranking positions in selection order. Keep the Stride 6 ticket layout. No lookahead or retrospective threshold optimization.
7. Evaluate best main-number matches across six tickets, and separately Jackpot 2 (five mains plus the special).

## Historical replay result (previously executed; verify with backtest.py)
| Metric | B1 | Adaptive |
|---|---:|---:|
| >=3/6 | 59 | 57 |
| >=4/6 | 5 | 5 |
| >=5/6 | 0 | 1 |
| 6/6 | 0 | 0 |

Adaptive best-hit histogram: [1, 228, 338, 52, 4, 1, 0].
B1 best-hit histogram: [0, 227, 338, 54, 5, 0].
Paired: Adaptive improved 32 draws, worsened 35, tied 557.
Jackpot 2: 0.

### Draw #01320
Actual mains: 12 26 28 43 50 54; special 52.
B1 ticket 5: 41 24 26 43 50 12 (4/6).
Adaptive ticket 5: 41 54 26 43 50 12 (5/6).
Removed: 19 (B1 rank 6, F30=1, F156=22) and 24 (rank 11, F30=1, F156=20).
Added: 25 (rank 54, F30=5, F156=11) and 54 (rank 48, F30=5, F156=14).

## Reproduction
```bash
python backtest.py path/to/power655.jsonl output/adaptive-momentum30
```
Writes `summary.json` and `per_draw.json`, including all six ticket lists and per-ticket hits for each draw.

## Research cautions
- The 624 historical draws were examined repeatedly during prior research, including draw #01320. This is **not a clean untouched holdout**.
- One 5/6 result does not establish higher predictive power, especially after multiple exploratory tests.
- Frequency momentum explains selection decisions, not physical lottery causation.
- No Champion promotion without a genuinely independent forward test and a pre-registered comparison.
