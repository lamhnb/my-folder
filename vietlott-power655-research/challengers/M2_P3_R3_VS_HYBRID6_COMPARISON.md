# M2-P3-R3 vs Hybrid6 M3-P3-R3 (36-slot)

## Source comparison
`m2_p3_r3.py` is a named alias of `hybrid6_p3_r3.py`. A source-level comparison at commit creation confirmed that they are identical after normalizing only the module docstring and model display label. Both operate on 36 Adaptive ticket slots, use the same 19-position MAGNUM weights, select MAGNUM top 3 and then up to 3 B1-rejected MAGNUM numbers (deduplicated), and replace distinct lowest-momentum slots.

## Expected exact equality
Both versions must produce identical 6 tickets, selected 36 numbers, and best-hit for every historical draw. They are NOT two independent challengers.

## Exploratory 624-draw result (indices 789..1412 = IDs #00790..#01413)
- >=3/6: 55
- >=4/6: 6
- >=5/6: 2 (#00967 and #01320)
- 6/6: 0
- best-hit histogram: [0,227,342,49,4,2,0].
- Relative to Adaptive: better 80, worse 76, tied 468.
- Winning-number occurrence difference: +336 added / -317 removed = +19.

## Status
These results were reconstructed with JS and not yet verified by running the committed Python entrypoints from a clean checkout. The underlying MAGNUM 19-position weights are a synthetic, uncalibrated physical proxy. Do not interpret historical differences as a verified increase in lottery odds. Keep both files for traceability but count as ONE model family in research comparisons.
