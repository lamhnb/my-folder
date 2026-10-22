# Independent challenger split — M2-P3 vs M3-R3

Two separate executable sources have been committed:
- `m2_p3_magnum_top3_momentum.py`: take the top **three** of six MAGNUM-proxy suggestions.
- `m3_r3_reverse_rejected_momentum_v2.py`: take up to three MAGNUM suggestions **rejected by the intermediate B1 rerank**.

Both start with B1 Adaptive's 36 labels, replace up to three *distinct* lowest-momentum slots, and issue six stride tickets. They use the same frozen 19-position synthetic MAGNUM weights, not verified physical ball identities.

## Independent JS replay (624 draws, zero-based indices 789–1412)
**Correction:** indices 789–1412 correspond to draw IDs **#00790–#01413**, not #00789–#01413 as earlier reports sometimes claimed.

| Model | >=3 | >=4 | >=5 | 6 |
| --- | ---: | ---: | ---: | ---: |
| Adaptive | 57 | 5 | 1 | 0 |
| M2-P3 | 62 | 5 | 1 | 0 |
| M3-R3 | 56 | 5 | 1 | 0 |

All three have the sole >=5 event at #01320. M2-P3 improves best-hit in 42 draws and worsens it in 31; M3-R3 improves 28 and worsens 32.

**Prior reported M2-P3 58/5/2 and M3-R3 56/7/1 are not reproduced under distinct-slot semantics.** The former experiments were exploratory and their exact source was not preserved. This document does not claim that the root cause of all discrepancies is proven.

## Validation status
The table is from a separate JS reconstruction using the same historical JSONL source. The two new Python sources have been committed but **have not yet been executed from a clean checkout against the frozen input file**. Tie-break equivalence and golden draw fixtures remain to be validated before calling these results certified.

## Reproduce
```bash
python vietlott-power655-research/challengers/m2_p3_magnum_top3_momentum.py --data power655.jsonl --output m2_p3_624.json
python vietlott-power655-research/challengers/m3_r3_reverse_rejected_momentum_v2.py --data power655.jsonl --output m3_r3_624.json
```

The fixed historical development sample has been reused extensively. Neither model demonstrates predictive edge. Do not promote either challenger or alter B1 Champion.
