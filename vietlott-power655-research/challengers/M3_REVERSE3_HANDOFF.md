# M3 Reverse-3 Momentum — research challenger

Status: **CHALLENGER / EXPERIMENTAL**, not Champion. No verified physical prediction advantage.

## Frozen algorithm
1. B1 ranks 55 labels by frequency in the 156 preceding draws (tie: lower label first).
2. Adaptive replaces two lowest-momentum labels among B1 top 36 with two highest-momentum labels outside top 36. Momentum = F30/30 - F156/156. Replacement retains the original slot, and six tickets use stride 6.
3. Take the 19 labels excluded by Adaptive, sort ascending, map the frozen **19-position physical proxy weights** to those labels, and select six highest-weight labels (tie: lower label).
4. Merge the 36 Adaptive labels and six MAGNUM labels. B1 reranks the 42 by F156 (tie: lower label); the six MAGNUM labels not retained in the resulting top 36 form the reverse-selection candidate list.
5. Sort these rejected MAGNUM labels by ascending F156, then label; force up to three into Adaptive, replacing at each step the current lowest-momentum slot (tie: earliest slot), without reusing slots.
6. Output six disjoint stride tickets. Main six winning numbers only; special ball excluded from scoring.

## Historical exploratory result
Strict-past replay on draw IDs #00789–#01413 (624 draws): >=3/6 **56**, >=4/6 **7**, >=5/6 **1**, 6/6 **0**. Baseline Adaptive: 57 / 5 / 1 / 0 respectively. Total new winning labels added **205**, winning labels removed **203**. Historical 4/6 examples gained: #01116, #01229, #01271; #01198 fell from 4/6 to 2/6. #01320 retained 5/6.

These are exploratory results on a heavily reused development period, **not** independently validated. No change to B1 Champion or Adaptive challenger.

## Proxy limitations
Weights are from 60 approximate 19-ball MAGNUM II Numba simulation runs at hypothetical RPM values 40/65/90 (20 runs each). The ordered 19 labels are mapped to simulated positions by assumption, not certified real loading positions. No real ball-set serial, loading map, per-ball metrology or pre-close mechanical state is known. Do not present this as a calibrated MAGNUM II or a lottery-odds advantage.

## Reproduce
Use the frozen Power 6/55 JSONL dataset ordered chronologically (at least through draw #01413):

```bash
python vietlott-power655-research/challengers/m3_reverse3_momentum.py --data power655.jsonl --output m3_reverse3_624.json
```

Before promotion: rerun from clean checkout, confirm deterministic tie-breaking, add independent unit tests, and evaluate against label-permutation/random-rescue controls and genuinely future draws. Do not tune on the same 624 draws.
