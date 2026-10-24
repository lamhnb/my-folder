# Champion-X X0 versus X60 — Disagreement Audit (2026-10-25)

## Scope
X0 = R19 Frozen, unmodified. X60 = same frozen R19 receiving a cyclically rotated most-recent-156-draw history, strict past.
Same 624 eval targets, zero-based indices 789..1412. Winning set is result[:6]. Dataset upstream vietvudanh/vietlott-data data/power655.jsonl, 1415 rows at inspection.
Source base R19 Git blob a7ebf4fa5216e1bfd4906087e04555044d3e58f0, Hybrid6 dependency 252f6e0e3dad70a80a4b0cf7febe92d5d080e264.

## Reproducible JS reconstruction results
- X0 Selection 2473.
- X60 Selection 2478.
- X60 recovered winner appearances absent X0: 808.
- X60 discarded winner appearances present X0: 803.
- Changed labels across all draws: 7371 (11.8125/draw).
- Coverage 6/6 overlapping: both 7, X0-only 46, X60-only 37, neither 534.
- Selection delta distribution by draw: -4:8, -3:25, -2:73, -1:124, 0:153, +1:137, +2:72, +3:28, +4:3, +5:1.
- Quarterly net X60-X0: +29, -22, +4, -6.
- Draw #01320: X0 6 correct, X60 3 correct, X60 adds zero winning labels and drops three winning labels.
- Strict-past switching based on trailing observed X60-X0 coverage delta (choose X60 iff trailing mean > 0):
  K30: X60 chosen 291 times, net -5, total Selection 2468, quarterly [+10,-15,-4,+4];
  K60: X60 chosen 331 times, net +9, Selection 2482, quarterly [+24,-12,-3,0];
  K120: chosen 312, net -8, Selection 2465, quarterly [+24,-11,-1,-20];
  K240: chosen 334, net +6, Selection 2479, quarterly [+24,-24,0,+6].
  Those policy variants were explored on the same inspected 624 draws. No valid holdout or random-matched control, so no predictive edge.
  
## Implementation correction
Champion-X Phase1 script now calls R19 predict(...)["final"] (R19 does not return "tickets"). This correction was committed separately.
An intermediate JS audit erroneously permitted R19 to swap out newly inserted numbers. That produced a false X60=2481 result and false overlap counts; discard it. The corrected reconstruction excludes labels previously used as incoming numbers from the outgoing candidates, exactly as R19 source does.

## Limits / next step
No Python clean-checkout PASS or independent data provenance audit yet. The X60 transformation rearranges past chronology, so the only legitimate interpretation is input sensitivity stress testing. It is not a new independent signal, and selecting historical winning shifts after the draw is leakage. Do not modify Frozen sources or promote an X variant.
