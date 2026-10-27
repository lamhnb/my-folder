# Champion-X Allocation-only audit — first controlled comparison (2026-10-27)

## Scope and method
- R19 Frozen = original source blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`; Hybrid6 = `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`.
- Independent JS reconstruction of Python algorithm, NOT Python clean-checkout PASS. Source fetched from GitHub research branch `research/power655-champion-x-input-sensitivity-20261025`.
- JSONL 1415-row input ends #01415 dated 2026-10-24, upstream commit `52d37a1d9208fc4178b0e5be73b8653c38ff88de`, including original known out-of-order row. Window zero-based 789..1412 (624 targets); per target prediction history = strictly `rows[:i]`, not result of target.
- **All methods use exact 36-number selection of R19 Frozen on each target.** No method alters or tunes Selection and no method uses current draw result to allocate. Each outputs six disjoint tickets of six numbers.
- Frozen output consists of Hybrid6's stride ticket partition, then three slot-specific R19 swaps. New comparators deliberately repartition the final 36 numbers, **not** rerun or alter Frozen.
- Results are retrospective on a previously inspected research window; no promotion or evidence of out-of-sample forecasting.
- Selection coverage is always 2473, histogram across 624 draws: 0=0,1=7,2=59,3=140,4=215,5=150,6=53.

## Comparator definitions (pre-target deterministic)
- `strideF156`: sort final 36 labels by descending previous-156-draw frequency, ties ascending label; distribute ranks round-robin to six tickets.
- `blockF156`: same rank; consecutive blocks of six make each ticket.
- `strideSorted`: ascending numeric labels; round-robin partition.
- `blockSorted`: ascending labels; contiguous blocks of six.
- `pair156`: scan 156 past draws and calculate symmetric co-occurrence counts for pairs of main numbers. Order the 36 final labels by descending 156-frequency (ties label ascending); greedily put each number in a ticket with max sum of its pair co-occurrences with already placed numbers, constrained ticket size <=6; tie preference smaller current group size and then smaller ticket index. This is a lightweight **untrained heuristic**, not a validated predictive relationship, and greedy ordering should be investigated.
- `random0..random19`: ascending final 36 labels; Fisher–Yates pseudo-random shuffle seeded by unsigned `20261027 + target_index*10007 + replicate*733` using 32-bit LCG recurrence `seed=1664525*seed+1013904223 (mod 2^32)`; partition into blocks of six. 20 fixed runs per target; mean is only a reference, not robust uncertainty estimate.

## Retrospective 624-target results

| method | best-hit sum | best histogram [0..6] | >=3 | >=4 | >=5 | ticket jackpot | quarter best sums |
|---|---:|---|---:|---:|---:|---:|---|
| Frozen | 1080 | [0,233,335,50,4,1,1] | 56 | 6 | 2 | 1 | [254,279,268,279] |
| strideF156 | 1074 | [0,230,341,50,3,0,0] | 53 | 3 | 0 | 0 | [252,278,264,280] |
| blockF156 | 1058 | [0,246,325,50,3,0,0] | 53 | 3 | 0 | 0 | [261,265,270,262] |
| strideSorted | 1063 | [0,238,335,49,2,0,0] | 51 | 2 | 0 | 0 | [267,260,271,265] |
| blockSorted | 1062 | [0,241,328,55,0,0,0] | 55 | 0 | 0 | 0 | [262,285,252,263] |
| pair156 | 1065 | [0,244,322,55,3,0,0] | 58 | 3 | 0 | 0 | [265,263,271,266] |

20 deterministic random runs, averaged: best sum 1066.05 (range 1042..1101); >=3 count 50.1 (range 39..65); >=4 count 2.8 (range 1..6); >=5=0 and jackpot=0 in all 20 runs. **20 seeded replicates are insufficient to infer true tails or calibrated p-values.**

### Paired best-hit comparisons vs Frozen (624 targets)
| Comparator | higher | same | lower |
|---|---:|---:|---:|
| strideF156 | 132 | 355 | 137 |
| blockF156 | 132 | 343 | 149 |
| strideSorted | 152 | 316 | 156 |
| blockSorted | 139 | 338 | 147 |
| pair156 | 133 | 345 | 146 |

## Interpretation
- Frozen had 2 retrospective ticket hits >=5 (one 5/6 and one 6/6); none of five deterministic alternative allocations reproduced them. This observation was drawn from an extensively inspected dataset and is not confirmation of a predictive advantage.
- Pair-based greedy grouping slightly raises count >=3 (58 vs 56) while losing half the >=4 (3 vs 6), and does not dominate the paired hit comparison (133 improvement, 146 deterioration).
- Allocation cannot repair a Selection 5/6 miss (e.g. #01416 number 35 absent from final 36), although it can theoretically achieve a ticket hit of 5 from 5 retained winners; such ideal allocation would be an oracle if conditioned on target draw results.
- Unconditional fair-draw expected best-hit behavior depends only on the same six disjoint tickets of six labels; no predetermined permutation improves actual lottery probabilities if outcomes are uniform and independent. Ranking against this null, not just Frozen, is necessary.
- This experiment assesses **Allocation mechanics**, not whether the past 156 pair co-occurrences predict future co-occurrences; robust OOS evaluation and negative/control pair models remain to be done.
- No changes to any Frozen code or registered Champion; **do not promote** a challenger on this backtest.

## Next research gate
Design a *pre-registered* pair-validation protocol before new optimizations: compare observed future within-ticket co-occurrence against appropriate independent/frequency-matched and shuffled history controls, with temporal holdout. If no stable transferable pair signal is present, stop allocation tuning and preserve Frozen. Run original Python sources from clean checkout and verify fixed Git hashes before labeling results Python PASS.
