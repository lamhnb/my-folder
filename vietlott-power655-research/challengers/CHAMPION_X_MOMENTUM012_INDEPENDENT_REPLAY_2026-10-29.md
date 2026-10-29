# Champion-X — Fresh independent X-Momentum 0.12 replay (2026-10-29)

## Reproducibility and scope
- Reconstructed the original frozen R19 Python algorithm from GitHub source, then independently replayed in JavaScript. **This is NOT a clean-checkout Python PASS**; local container network fetch failed, and there was no clean local Python execution.
- Original frozen R19 blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0` and Hybrid6 dependency `252f6e0e3dad70a80a4b0cf7febe92d5d080e264` were read and not modified.
- Data: GitHub upstream public JSONL main fetched 2026-10-29, **1416 rows** ending with `01416`, draw 2026-10-27, main numbers [9,18,27,28,31,35], special 50. Original row-order anomaly at zero-based index 779 not repaired.
- Original 624 targets are zero-based positions **789..1412** inclusive. For each target i, construct all signals from rows before i, then only inspect actual target main numbers for scoring. The additional 3 targets are positions 1413..1415 (#01414..#01416).
- This is an **independent replay implementation**, NOT an independent virgin historical OOS dataset: all or part of this timeline has been inspected by prior Champion-X research. No thresholds reoptimized.
- Every prediction consists of six disjoint tickets of six distinct main numbers, Selection = union winning hits; ticket Jackpot 6/6 is separate.

## Policy implementation
For every target, first compute original Hybrid6 six tickets and original R19 proposed three sequential swaps with its fixed ranking, no cycling, immutable source ties. Frozen X0 applies all three; R19-2 applies only first two; **X-Momentum 0.12** applies each of the original hypothetical three swaps independently iff
`[F30(in)/30 - F156(in)/156] - [F30(out)/30 - F156(out)/156] >= 0.12`.
Rejected swaps do not cause reranking or resampling. The original R19 swaps are disjoint, so the resulting ticket partition preserves the 36-number invariant.

## Exact 624-row replay summary
| Method | Selection sum | Selection >=5 | Selection =6 | best-hit histogram h0..h6 | ticket best-hit>=5 | ticket Jackpot=6 |
|---|---:|---:|---:|---|---:|---:|
| Frozen X0 | 2473 | 203 | 53 | [0,233,335,50,4,1,1] | 2 | 1 |
| Fixed R19-2 | 2490 | 200 | 55 | [0,225,344,50,3,2,0] | 2 | 0 |
| X-Momentum 0.12 | **2494** | **208** | 54 | [0,224,348,47,3,2,0] | 2 | 0 |
| Hybrid6 0-swap | 2487 | 208 | 53 | [0,227,342,49,4,2,0] | 2 | 0 |

Quarter Selection totals:
- Frozen X0 [606,636,613,618]
- R19-2 [617,637,623,613]
- X-Momentum [617,641,618,618]
- Hybrid6 [613,640,621,613].

Paired X-Momentum vs Frozen by target Selection: improved 138 draws, same 366, worsened 120. X-Momentum vs fixed R19-2 improved 88, tied 450, worsened 86. These are **reused in-sample results**, after prior parameter selection. Do not treat as evidence of superiority.

## Three newer historical targets
These are only **three** target draws beyond the legacy benchmark window; not virgin OOS and far too few to measure predictive ability.

| Draw | Date | Frozen X0 Selection/best | R19-2 Selection/best | X-Momentum Selection/best |
|---|---|---|---|---|
| #01414 | 2026-10-22 | 5/2 | 5/2 | 5/2 |
| #01415 | 2026-10-24 | 5/3 | 5/3 | 4/3 |
| #01416 | 2026-10-27 | 5/2 | 5/2 | 5/2 |
| **Total** | | **15** | **15** | **14** |

For all three targets, `dm` for the three proposed R19 swaps was below .12, so X-Momentum rejected all three:
- #01414 proposed out→in: 48→46 (dm=.0589744), 40→52 (.0589744), 28→06 (.0576923)
- #01415: 39→52 (.0653846), 48→06 (.0576923), 28→03 (.0525641)
- #01416: 53→04 (.0782051), 16→52 (.0769231), 39→03 (.0589744).

For #01416, X0 reconstructed six final tickets match earlier user-issued X0 tickets exactly; main winning set [09,18,27,28,31,35]. No 6/6 Selection under these three models.

## Evaluation limitations
1. Exact Git blob of the newly fetched 1416-row dataset was not recorded in this JS replay. To obtain an audit-certified result, pin its bytes and hash and independently run Python from clean checkout, verifying source hashes and per-draw tickets.
2. Historical 624 draws and more recent draws have been used for model exploration; cannot retrospectively label them untouched holdout. The earlier rule was selected on an inspected split.
3. The null expectation for any predetermined 36-number set in fair Power 6/55 is 6*36/55=3.92727 hits per draw; apparent modest uplift over this baseline cannot establish a predictive edge.
4. No modifications to Frozen source, Hybrid6, registered Champions, or the original 0.12 threshold. No promotion.

## Next validation gate
Pre-register and persist immutable future ticket sets for Frozen, R19-2 and X-Momentum 0.12 **before** each new draw; evaluate a sufficiently long future uninspected block with Selection and best-hit tails, plus random matched controls, per-draw hashes and source provenance. Do not change 0.12 or tune to #01415.
