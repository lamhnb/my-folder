# Champion-X — Matrix of 53 Selection=6 target draws (2026-10-30)

## Scope and provenance
Reconstructed the original R19 Frozen six disjoint tickets per target with independently translated JavaScript logic from the immutable GitHub code. **Not a Python clean-checkout PASS.** Original R19 blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`, Hybrid6 dependency `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`; neither modified. Source JSONL through #01417, original order retained; historical 624 target row positions 789..1412. Each target uses only prior rows for ticket generation; actual target winning six numbers are overlaid only afterward.

The full 53-row ticket-level matrix is `CHAMPION_X_SELECTION6_TICKET_MATRIX_53_2026-10-30.csv`. Each row contains ID, date, winning numbers, all six original X0 Frozen tickets, six ticket hit counts, their sorted occupancy pattern, and best-hit. The 53 draws were **conditioned on their observed Selection 6/6** and were already in a repeatedly inspected development window; this subgroup must never be treated as a pre-draw strategy selector.

## Distribution of the complete six winning labels across six X0 tickets
| Sorted ticket occupancy | Draw count |
|---|---:|
| 2-1-1-1-1-0 | 18 |
| 2-2-1-1-0-0 | 17 |
| 3-2-1-0-0-0 | 7 |
| 3-1-1-1-0-0 | 6 |
| 4-2-0-0-0-0 | 1 |
| 4-1-1-0-0-0 | 1 |
| 5-1-0-0-0-0 | 1 |
| 6-0-0-0-0-0 | 1 |
| 1-1-1-1-1-1 | 1 |
| **Total** | **53** |

Observed best-hit histogram h0..h6 = **[0,1,35,13,2,1,1]**. Thus best-hit >=3 in 17/53; >=4 in 4/53; >=5 in 2/53; ticket Jackpot=6 in 1/53. These are *retrospective* ticket-hit events, **not new predictions**.

Exact random-ticket partition null conditional on Selection=6 and same 36 labels:
`P(best=1..6)=[0.0239532763,0.7083405210,0.2470489662,0.0200996821,0.0005544740,0.0000030804]`.
For 53 such targets, expected best-hit counts approximately [1.2695,37.5420,13.0936,1.0653,0.0294,0.0001633]. Observe that in-sample rare higher tails can arise from model-search selection/inspection and cannot be treated as prospectively validated performance. A planned comparison must account for the many earlier allocation policies and exploratory hypotheses.

Ticket-position totals of selected winning numbers across these 53 draws: ticket1=51,ticket2=54,ticket3=65,ticket4=52,ticket5=52,ticket6=44; sum=318=53×6. Because all ticket labels/positions are algorithm-defined and have different origin/rank exposures, this is not evidence that ticket 3 is prospectively superior.

Four particularly concentrated examples:
- #00967 winning 09 13 28 33 50 53, ticket hits [0,0,5,1,0,0].
- #01179 winning 05 11 15 32 42 49, ticket hits [0,2,0,4,0,0].
- #01260 winning 03 05 11 13 24 27, ticket hits [0,0,4,1,1,0].
- #01320 winning 12 26 28 43 50 54, ticket hits [0,0,0,0,6,0].

## Conclusions and next gate
- In the 53 full-Selection draws, **35** drew a best hit of only two. This is not surprising by itself: a random reallocation also typically has best hit two when S=6.
- To identify possible Allocation improvements, the next forensic step should compare within-ticket winner-pair membership and their *pre-draw features* across all 53 cases to similarly-featured nonwinning pairs. Avoid conditioning training decisions on the winners.
- Frozen, Hybrid6 and registered Champions unchanged. No new Allocation promoted; findings not independently OOS-verified.
