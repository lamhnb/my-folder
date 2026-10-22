# M3 forensic replay — 2026-10-23

## Recovered execution logic
The original interactive M3 Reverse-3 + Momentum calculation is visible in the prior execution transcript. The source code in `m3_reverse3_momentum.py` was reconstructed from that logic rather than committed from an already-tested file.

Two independently expressed JavaScript replays of the same 624-draw decision pipeline (candidate construction, frequency rerank, rejected MAGNUM selection, three lowest-momentum replacements without reusing slots) were compared slot-by-slot. **Zero differing ticket slots** across 624 draws.

## Corrected observed counts
For draw IDs #00789–#01413 (624 draws):
- Best-hit histogram for M3: [0/6:1, 1/6:232, 2/6:335, 3/6:51, 4/6:4, 5/6:1, 6/6:0].
- >=3/6: **56**; >=4/6: **5**; >=5/6: **1**; 6/6: **0**.
- Baseline Adaptive: >=3/6 57, >=4/6 5, >=5/6 1.
- M3 improves best-hit in 28 draws, worsens in 32, ties in 564.
- M3 adds 205 winning-number occurrences, loses 212 (net -7).
- Newly >=4/6: #01116. Lost >=4/6: #01198. #01320 retains 5/6.

The earlier claim of **7** >=4/6 and three new 4/6 draws is **not reproducible**. Its cause is not established. Do not infer that the committed Python source is wrong merely because it disagrees with an earlier unpersisted summary.

## Provenance limitations
The 19-position physical weights were derived from 60 synthetic Numba MAGNUM-proxy runs, not a real machine-specific ball-label map. All 624 historical draws have been reused for model development. This is a retrospective exploratory test, not a verified odds improvement.

## Required follow-up
1. Run `python m3_reverse3_momentum.py --data <frozen-data> --output <file>` on a clean checkout; compare per-draw tickets and the above histogram.
2. Add frozen fixture tests for #01116, #01198, #01229, #01271 and #01320.
3. Do not edit M3 merely to recover the previously reported 7 events.
4. Keep Champion and Adaptive untouched. M3 remains an experimental challenger.
