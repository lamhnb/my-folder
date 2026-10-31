# Champion-X forensic audit #01418 — 2026-10-31

## Locked provenance and scope
- Draw #01418 (2026-10-31): winning main numbers 12,18,22,26,28,55; special 11.
- Strict-past forecast history ends at #01417 (2026-10-29), 1417 historical records. #01418 is not in forecast history.
- Original Frozen R19 Git blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0` and Hybrid6 blob `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`; unchanged.
- Independent JS reconstruction from Frozen source. Not a clean-checkout Python PASS. The six X0 final tickets matched the prepublished #01418 tickets exactly.
- Original raw data order preserved including known anomaly; no retroactive alteration of issued prediction.

## X0 result
Tickets:
1. 02 04 07 19 21 23 — 0 main hits
2. 11 16 24 27 **28 55** — 2 main hits, special 11
3. 05 06 36 38 49 52 — 0 main hits
4. 08 15 25 **26** 40 41 — 1 main hit
5. 01 13 14 34 47 51 — 0 main hits
6. 09 17 **18** 31 45 50 — 1 main hit

X0 Selection=4/6, best ticket hit=2/6, missing main labels 12 and 22. Special 11 is not included in main Selection count.

## Missed labels through stages
| Number | F156 | F30 | Momentum=F30/30−F156/156 | rank F156 | original top36 | Hybrid6 | excluded R19 rank |
|---|---:|---:|---:|---:|---|---|---:|
| 12 | 14 | 2 | −0.0230769231 | 41/55 | no | no | 11/19 |
| 22 | 23 | 1 | −0.1141025641 | 3/55 | yes | no | 19/19 |

22 was highly ranked by F156 but eliminated in Hybrid6's momentum-oriented logic and not restored by R19. 12 was below F156 top36 and never restored. Neither was directly removed by R19's last three swaps.
Original X0 R19 swaps: ticket1 53→04, ticket6 33→17, ticket3 20→52. Each has zero marginal Selection impact this target.

## Six-state rotations, strict past
| State | Selection | Best-hit | true winners recovered vs X0 | true winners lost vs X0 |
|---|---:|---:|---|---|
| X0 | 4 | 2 | — | — |
| X5 | 3 | 2 | — | 26 |
| X15 | 4 | 2 | 12 | 26 |
| X30 | 5 | 2 | 12,22 | 18 |
| X60 | 5 | 2 | 12,22 | 18 |
| X90 | 3 | 1 | 22 | 18,55 |

X30 and X60 recover both misses but lose winning 18, net Selection +1. The rotated histories are counterfactual sensitivity probes, **not calibrated prospective signals**; selecting the successful X after observing outcome would be oracle leakage.

## Interpretation
This is principally a Selection miss. Allocation cannot recover missing 12 and 22 from the original 36 labels. The 22 case illustrates a possible **long-term hot / short-term cold** category, but one draw cannot justify downgrading the recency component: nearby similar candidates who did not win must be included in any population-level test. X30/X60 better in this draw but their other historical draws have no stable demonstrated advantage.

No Frozen or registered Champion code changed, no model promoted, and clean-checkout Python reproduction remains unverified.
