# Champion-X — Forensic audit of draw #01416 and 624-draw consensus (2026-10-27)

## Status and provenance

**Method:** independent JavaScript reconstruction of the exact GitHub Python Frozen source logic, using GitHub connector-fetched JSONL. Not a Python clean-checkout PASS. No Frozen or Hybrid6 modification. Research branch: `research/power655-champion-x-input-sensitivity-20261025`; predecessor head `669baea9f8061b898a9bd4e20c0ba9b310ded3b4`.

Frozen R19 Git blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`, Hybrid6 blob `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`. Historical upstream snapshot used for all replays: commit `52d37a1d9208fc4178b0e5be73b8653c38ff88de`, 1415 rows ending with ID #01415 on 2026-10-24. Historical 624-target window is zero-based positions 789..1412, as in Phase 1, not corrected by ID order; source row-order anomaly is retained. For 624 target positions, predictions use rows strictly before each position. For #01416 the 1415 rows are entirely past; supplied winners are *not* appended to the input.

Winning main set provided by user for #01416 = 09,18,27,28,31,35. Special 50 is not part of Selection scoring.

## #01416 exact Frozen X0 verification

The JS reconstruction's six R19 final tickets match **all 36 labels and ticket partition** in the user-issued X0 tickets:

1. 03 07 09 17 31 50
2. 04 10 24 41 51 52
3. 01 05 06 26 36 55
4. 08 13 14 18 28 40
5. 11 19 21 23 34 45
6. 02 25 27 38 47 48

Hybrid6 before R19:
1. 07 09 17 31 39 50
2. 10 16 24 41 51 53
3. 01 05 06 26 36 55
4. 08 13 14 18 28 40
5. 11 19 21 23 34 45
6. 02 25 27 38 47 48

R19 swaps in exact source order: ticket 2 53→04 (score 0.972222222222), ticket 2 16→52 (0.891812865497), ticket 1 39→03 (0.811403508772). All three have zero marginal Selection effect in #01416. Final X0 Selection = 5/6; best-hit = 2/6; missed label = 35.

**Correction to handoff:** rank 35 in all-number F156 sort = 52/55; rank 35 in **R19 excluded momentum ranking = 12/19**, NOT 9/19. F156(35)=12, F30(35)=1, momentum = -0.04358974359. It was already outside the pre-R19 Hybrid6 set and never reintroduced by R19.

## Six counterfactual X states at #01416

Each state uses rotated past 156 rows exactly as Phase 1; all have 36 distinct labels. `added` / `removed` are relative to X0, not altered ticket positions.

| X | selection | best hit | 35 present | added relative X0 | removed relative X0 | winner gained | winner lost |
|---|---:|---:|---|---|---|---|---|
| X0 | 5 | 2 | No | — | — | — | — |
| X5 | 5 | 2 | No | 20,29,33,54 | 03,26,40,48 | — | — |
| X15 | 5 | 2 | Yes | 12,15,16,20,29,30,33,35,42,54 | 03,04,08,09,21,26,45,47,50,51 | 35 | 09 |
| X30 | 5 | 2 | Yes | 12,15,16,20,22,29,30,32,33,35,37,39,42,54 | 01,03,04,06,07,09,13,17,23,25,45,47,50,51 | 35 | 09 |
| X60 | 4 | 2 | No | 12,15,16,20,22,29,30,32,43,46,49,53,54 | 01,03,04,06,08,09,11,19,24,38,40,47,52 | — | 09 |
| X90 | 3 | 2 | No | 12,15,16,22,29,30,32,33,39,44,49,53 | 01,03,04,05,11,14,18,19,23,24,27,55 | — | 18,27 |

**No X achieves Selection 6/6.** None achieves ticket Jackpot 6/6.

### All tickets

**X5**
1. 07 09 29 31 33 50
2. 04 10 24 41 52 54
3. 01 05 17 36 47 55
4. 08 13 14 18 28 51
5. 11 20 21 23 34 45
6. 02 06 19 25 27 38

**X15**
1. 07 29 31 33 52 54
2. 10 16 19 24 41 42
3. 01 05 12 15 36 55
4. 13 14 17 18 28 40
5. 06 11 20 23 34 35
6. 02 25 27 30 38 48

**X30**
1. 15 29 31 33 37 39
2. 10 16 24 32 35 41
3. 05 12 22 26 36 55
4. 08 14 18 28 40 42
5. 11 20 21 34 52 54
6. 02 19 27 30 38 48

**X60**
1. 07 29 31 43 46 51
2. 10 16 32 41 53 54
3. 05 15 22 26 36 55
4. 13 14 18 28 49 50
5. 12 20 21 23 34 45
6. 02 17 25 27 30 48

**X90**
1. 07 09 29 31 33 39
2. 10 12 16 32 41 53
3. 15 22 26 36 44 51
4. 08 13 17 28 40 52
5. 06 21 34 45 47 50
6. 02 25 30 38 48 49

X0 ticket details are in the previous section. Thus six-state 36-label membership equals the union of each state's six listed tickets; there is no separate Allocation optimization.

### Number 35 across state transitions

| X | F156 | F30 | momentum | pre-R19 Hybrid6 | R19 excluded rank | final |
|---|---:|---:|---:|---|---:|---|
| X0 | 12 | 1 | −0.04358974 | No | 12/19 | No |
| X5 | 12 | 2 | −0.01025641 | No | 5/19 | No |
| X15 | 12 | 4 | +0.05641026 | No | 1/19 | Yes, R19 swap 21→35 |
| X30 | 12 | 5 | +0.08974359 | Yes | n/a | Yes |
| X60 | 12 | 2 | −0.01025641 | No | 7/19 | No |
| X90 | 12 | 1 | −0.04358974 | No | 11/19 | No |

Number 35 has 2/6 votes, not 2/5 (5 alternative variants). The 156-row cyclic roll artificially reinterprets recency; it does not predict the true draw.

## Comparable negative examples (prevent post-hoc story)

Pre-R19 excluded candidates with F156 around 9..15 and F30 <=2 in the actual unrotated X0 (all *non-winning* except 35):

| number | excluded R19 rank | F156 | F30 | momentum | winning #01416 |
|---|---:|---:|---:|---:|---|
| 37 | 7 | 12 | 2 | −0.01026 | No |
| 15 | 8 | 13 | 2 | −0.01667 | No |
| 46 | 9 | 13 | 2 | −0.01667 | No |
| 12 | 10 | 14 | 2 | −0.02308 | No |
| 49 | 11 | 10 | 1 | −0.03077 | No |
| **35** | **12** | **12** | **1** | **−0.04359** | **Yes** |
| 43 | 14 | 15 | 1 | −0.06282 | No |

Thus identical or nearby F156/F30/negative momentum do not single out #35. In X0, R19 is rank-based with only three swaps and does not enter 35.

## 624-draw Phase 2 consensus reconstruction

All six states independently reconstructed on same 624 targets and same 36-label budget. X0 = 2473 and X60 = 2478 match earlier JS benchmark; X60 recovered 808 winner appearances and lost 803, matching prior audit. Historical 624 targets are in-sample for exploration, not a fresh forecast holdout.

| State | Selection | Selection >=5 | Selection 6/6 | 156-draw quarters |
|---|---:|---:|---:|---|
| X0 | 2473 | 203 | 53 | 606,636,613,618 |
| X5 | 2441 | 194 | 42 | 593,617,619,612 |
| X15 | 2457 | 197 | 52 | 605,613,619,620 |
| X30 | 2463 | 207 | 36 | 608,612,605,638 |
| X60 | 2478 | 208 | 44 | 635,614,617,612 |
| X90 | 2438 | 175 | 30 | 609,605,617,607 |

**Selection >=5 is not ticket best-hit >=5.** Under unmodified X0, best-hit >=5 is 2/624, as previously documented.

For 55 labels per target, vote count by number of state-36 sets containing each label, and observed hit frequency:

| Votes | instances | winning instances | hit rate | winner instances missed by X0 |
|---:|---:|---:|---:|---:|
| 0 | 553 | 57 | 10.31% | 57 |
| 1 | 2468 | 268 | 10.86% | 255 |
| 2 | 3881 | 422 | 10.87% | 304 |
| 3 | 5149 | 580 | 11.26% | 339 |
| 4 | 7337 | 766 | 10.44% | 222 |
| 5 | 9833 | 1072 | 10.90% | 94 |
| 6 | 5099 | 579 | 11.36% | 0 |

Sum of voting-instance winners = 3744 (6*624), sum instances = 34320 (55*624). The category 0 group of 553 and its 57 winning appearances **cannot** be recovered by any of the six X states. High vote count does not exhibit monotonic enrichment.

### Same-budget Selection controls

Majority36: sort labels by descending six-state vote, tie preserve X0, then ascending label. Minority36: ascending vote, same ties. Both choose exactly 36 distinct labels per target. Random-matched exact expectation: replace the identical number k as Majority36 from the X0 set with k randomly chosen among 19 X0 exclusions, uniformly without replacement; evaluate the exact conditional expected Selection per target. This is a mathematically exact random baseline, not an actual Monte Carlo run of Python's Random.

| policy | Selection | Selection >=5 | Selection 6/6 | quarters |
|---|---:|---:|---:|---|
| X0 | 2473 | 203 | 53 | 606,636,613,618 |
| Majority36 | **2436** | 189 | 40 | 602,615,611,608 |
| Minority36 | 2448 | 198 | 40 | 632,611,596,609 |
| Random matched, exact expected value | **2463.798** | n/a | n/a | n/a |

Majority36 made 2811 replacement positions in aggregate; 279 formerly absent winning numbers added; 316 formerly retained winning numbers lost; net **−37**. Under this protocol majority loses to X0 across all four 156-draw quarters and is below expected matched-random Selection (2436 versus 2463.8). This is an in-sample diagnostic, not a precise claim of statistical significance. Do not promote.

### Conclusions and boundary

1. X0 missed 35 because its historical frequency/momentum was weak, 35 was absent from Hybrid6, and R19 only selected three other positive crossrank swaps.
2. X15 and X30 include 35, but both remove winning 09, hence Selection remains 5 rather than 6.
3. There is **no demonstrated strict-past rule** that identifies the correct X in advance. X transformation is a synthetic chronology stress probe rather than an independent informative feature.
4. #01416 is **a Selection miss** (5 of 6 unique labels); grouping five retained winners across three or more tickets is a separate Allocation issue. No allocation alone could create a 6/6 ticket while 35 is absent.
5. Recovery and loss patterns repeat widely over 624 targets. A naive consensus Selection policy loses. Results do not warrant Champion promotion.
6. Independently verified Python clean-checkout replay remains **NOT PASS / NOT EXECUTED**. Do not silently repair source anomaly or change Frozen versions.
