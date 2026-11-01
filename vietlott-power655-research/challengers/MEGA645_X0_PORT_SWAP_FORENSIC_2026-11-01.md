# Mega-X0 Port Audit — CrossRank mechanics on 624 strict-past Mega 6/45 draws (2026-11-01)

## Reproducibility scope
- Source Mega JSONL: `vietvudanh/vietlott-data/data/power645.jsonl`, fetched 2026-11-01, 1386 rows, latest #01583 on 2026-11-01. To compare exactly with the earlier 624-target experiment, this audit uses zero-based rows 761..1384 inclusive (#00959..#01582), **not** the latest row #01583 as target. For each target i, only `rows[:i]` used to generate prediction, then `rows[i].result[:6]` used to score.
- Immutable Power source identities: R19 `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`, Hybrid6 `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`. Neither modified. Mega port is a **new research adaptation**, not Power X0 Frozen.
- Independent JS source reconstruction, not a Python clean-checkout PASS. Historical testing reused; no pristine OOS confirmation.
- Mega Hybrid6 port: 45 numbers, F156/F30, same frequency/momentum and MAGNUM order; only first nine MAGNUM weights apply to nine excluded labels. This is a deliberately mechanical port, not validated physical model. Mega CrossRank port: ranks nine excluded versus selected 36, scores `(10-r9)/9 - (37-r36)/36`, performs up to three noncycling distinct incoming/outgoing swaps. Source rank sorting and ties follow Power algorithm.

## Before versus after three swaps
| Metric | Hybrid6 Mega | 3-swap CrossRank Mega |
|---|---:|---:|
| Selection total | 3031 | 3024 |
| Selection histogram h0..h6 | [0,0,5,33,166,262,158] | [0,0,1,37,161,283,142] |
| Selection>=5 | 420 | 425 |
| Selection 6/6 | 158 | 142 |
| Best-hit histogram h0..h6 | [0,104,411,99,10,0,0] | [0,108,414,90,12,0,0] |
| Best-hit >=3 | 109 | 102 |
| Best-hit >=4 | 10 | 12 |
| Best-hit >=5 | 0 | 0 |
| Ticket six-of-six | 0 | 0 |
| Selection sum Q1..Q4 | [756,756,759,760] | [753,746,757,768] |

CrossRank Selection vs Hybrid6 per target: improved 150, same 323, worsened 151. The last quarter had positive net Selection but previous three had negative net. Not stable.

## Swap-by-swap forensic audit
Define delta = (entering label wins) - (leaving label wins), each among the six main numbers actually drawn (post-forecast scoring).

| Step | +1 draws | -1 draws | 0 draws | entering winner count | leaving winner count | net coverage | best-hit increased | best-hit decreased | best-hit unchanged |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Swap1 | 61 | 70 | 493 | 73 | 82 | -9 | 19 | 24 | 581 |
| Swap2 | 69 | 61 | 494 | 83 | 75 | +8 | 17 | 18 | 589 |
| Swap3 | 69 | 75 | 480 | 73 | 79 | -6 | 15 | 18 | 591 |

Total marginal delta -7. Results were generated on the original 624 fixed targets, no reoptimization. The fact that individual steps improve or worsen best-hit does not indicate the step can be chosen prospectively based on those future winners.

## Illustrative concentrated winning tickets
- #01075 2023-07-30: selection 4→5, best-hit 3→4; swaps ticket5 39→06, ticket6 22→17, ticket1 32→11. Winning main 03,17,23,33,42,45. Note the 4-hit outcome is not a 5-hit or jackpot.
- #01148 2024-01-17: selection 5→6, best-hit 3→4; swaps ticket5 28→36, ticket6 30→17, ticket1 35→26. Winning main 14,19,21,36,43,44.
- #01154 2024-01-31: selection 6→5, best-hit 4→3; swaps ticket5 28→34, ticket1 38→17, ticket2 01→06. Winning main 09,11,15,35,38,41. This is a direct counterexample to selective winner-only explanations.
- In all 624 targets there were zero best-hit >=5 for both models, despite 158 and 142 Selection 6/6 cases, respectively.

## Conclusions
1. CrossRank demonstrates occasional positive selection and within-ticket hit changes, but losses match or exceed wins across the same historical window. It has **not** reproduced the exceptional Power #01320 6-hit ticket in Mega.
2. Unlike a pure allocation swap, R9 CrossRank replaces label identities in the selected 36, so the observed differences mix **Selection and Allocation**. To isolate Allocation, fix exactly the 36 Hybrid6 numbers for every target and only exchange numbers between existing tickets, then score against the *same-target* random partition baseline.
3. No evidence that CrossRank substantially changes the probability of an actually fair draw; historical algorithm selection and repeated trials contaminate this sample. Any candidate promotion must await untouched future data and clean Python source-level replication.
4. Keep Power X0 Frozen, Hybrid6 and registered Champions unchanged. Mega port remains research-only, not official Frozen.
