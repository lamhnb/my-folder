# Champion-X Selection-origin ablation: R19 swaps 0/1/2/3 (2026-10-27)

## Scope
Research-only ablation of the already existing Frozen Hybrid6 → R19 algorithm. All source files stay immutable. Original R19 blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`, Hybrid6 blob `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`. Original-order JSONL upstream snapshot commit `52d37a1d9208fc4178b0e5be73b8653c38ff88de` ending at #01415. 624 target positions 789..1412. Independent JavaScript reconstruction, NOT clean Python PASS, and no out-of-sample guarantee.

## Intervention
Hybrid6 baseline selects 36 labels. Frozen R19 calculates the fixed original excluded19/ranked36 positions and then executes three sequential noncycling crossrank swaps. Define R19-k as **stopping the original unmodified sequence after k swaps** with k=0,1,2,3 (for k=0 return Hybrid6 tickets). No recalibration, no tuning of rank scores, no use of target result. Each variant always returns 36 distinct selected labels.

## Results
| Variant | Selection total | Selection >=5 | Selection =6 | Q1,Q2,Q3,Q4 total |
|---|---:|---:|---:|---|
| R19-3 Frozen X0 | 2473 | 203 | 53 | 606,636,613,618 |
| R19-0 (Hybrid6) | 2487 | 208 | 53 | 613,640,621,613 |
| R19-1 | 2489 | 204 | 53 | 614,644,622,609 |
| R19-2 | **2490** | 200 | **55** | 617,637,623,613 |

R19-2 vs Frozen differences: +17 selected winning label appearances; +2 targets Selection 6/6; **−3** targets Selection >=5. Quarterly deltas +11,+1,+10,−5. The better aggregate does not mean stable improvement.

## Cautions
- Historical 624 targets have repeatedly been used for parameter selection; finding a good swap-count on them is data snooping, not proof of prospective edge. This is an *ablation of an existing design*, not an independent X forecasting feature.
- Every model has 36 labels, exactly six disjoint tickets of six under the unchanged ticket geometry. Jackpot best-hit tails **have not been evaluated in this ablation**, and Selection =6 must not be called ticket jackpot.
- R19-2 and R19-1 are *hypothetical shadow models*. Do not modify the frozen source, update registered Champions or promote a new model.
- Next: derive a pre-target stopping rule only if an independent hypothesis warrants it; verify on a truly untouched future series plus matched random controls and rerun exact immutable Python with hash guards.
