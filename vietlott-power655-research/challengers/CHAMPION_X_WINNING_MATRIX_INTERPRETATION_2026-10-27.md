# Champion-X — 624 winning ticket row-matrix audit (2026-10-27)

## Source and framing
- Matrix CSV: `CHAMPION_X_WINNING_MATRIX_624_2026-10-27.csv` in this directory.
- 624 historical target positions **789..1412 inclusive**, drawn from original 1415-line upstream JSONL snapshot at `vietvudanh/vietlott-data` commit `52d37a1d9208fc4178b0e5be73b8653c38ff88de`. Preserve raw order including known ID/date anomaly.
- Each row is one six-main-number winning combination, sorted ascending, along with the five successive gaps, sum, number of odd labels, number of low labels (1..27), number of adjacent pairs, overlap with previous *matrix* row (starting at second matrix target), and span max-min.
- This is a **winning-number-only** matrix. It is **not** the six-ticket R19 overlay. Previous `CHAMPION_X_WINNING_OVERLAY_624_CONDITIONAL_NULL_2026-10-27.md` supplies ticket-overlay results; no new issued-ticket partitions have been generated or compared in the present matrix. No changes to Frozen.
- This is in-sample descriptive research, not a strict-past forecasting validation. Historical outcomes are naturally known for computing rows, and cannot be used as pre-draw features.

## Aggregates
- Total 624 draws.
- Mean six-number sum **169.3093** vs independent uniform theoretical expectation **168** (6×28).
- Mean span (max minus min) **39.7260** vs theoretical expected **40** under sampling 6 distinct numbers from 1..55.
- Counts of adjacent-pair number per draw: 0:362, 1:220, 2:34, 3:8. Hence 262/624 have at least one adjacent pair. Adjacent pair *incidences* sum **312**, vs expected **340.36**, and theoretical null requires distribution accounting for correlated pairs.
- Odd-label count 0..6: `[4,34,166,209,142,62,7]`.
- Low 1..27 count 0..6: `[5,57,179,187,140,43,13]`.
- Overlap with immediately preceding row in this 624-row matrix, excluding first: counts 0..6 = `[308,234,74,6,1,0,0]`; this is **not exactly** the prior analysis including position 788 for first draw (it excluded the first comparison).
- No exact five-gap vector was duplicated in these 624 rows (tested by grouping on the ordered differences g1..g5). There are many possible vectors, so uniqueness is not itself predictive evidence.

## By consecutive 156-draw segments
| Group | mean winning sum | mean span | adjacent pair incidences | near-gap <=3 incidences | overlap with previous matrix row |
|---|---:|---:|---:|---:|---:|
| Q1 | 170.5897 | 40.1026 | 83 | 234 | 91 |
| Q2 | 171.8269 | 39.2949 | 82 | 231 | 98 |
| Q3 | 170.9551 | 40.0962 | 77 | 205 | 113 |
| Q4 | 163.8654 | 39.4103 | 70 | 237 | 102 |

A quarter shift in winning sums is not evidence of a stable predictive rule. Features such as gap or parity computed on a known winning row are **post-draw descriptors**, not eligible inputs for predicting that row.

## What the row matrix can and cannot establish
- It permits systematic scans of low/high, odd/even, gaps, and temporal patterns without visually cherry-picking one particular winning ticket.
- It does **not** show systematic departures from the standard fair-draw model in mean sum or mean span.
- It does not identify *which* near or far numbers to group inside the six R19 tickets prior to a new draw.
- A proper follow-up should overlay each row's winning labels on the six **Frozen issued tickets** and compare predeclared pair/gap-based allocations against conditional permutation baselines. The previous overlay already establishes best-hit sum=1080, >=3=56, >=4=6, >=5=2, and =6=1 over this 624 window.
- To claim a real prospective advantage, a fixed, fully specified allocation rule must beat controls on untouched future draws, not just on this reused sample.

## Frozen guardrails
R19 source blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`; Hybrid6 blob `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`; unchanged. No Champion promotion.
