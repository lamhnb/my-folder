# Champion-X — Jackpot #01320 provenance and multiple-testing trace (2026-11-07)

## Verified source evidence
- Frozen R19 blob a7ebf4fa5216e1bfd4906087e04555044d3e58f0 and Hybrid6 dependency blob 252f6e0e3dad70a80a4b0cf7febe92d5d080e264 were fetched on research/power655-champion-x-input-sensitivity-20261025 and matched handoff hashes.
- CHAMPION_X_PHASE1_AUDIT_2026-10-25.md already documents X0 historical 624-draw benchmark and a historical ticket jackpot.
- CHAMPION_X_PHASE2_PROTOCOL_2026-10-25.md explicitly names #01320 as a golden-case replay target, showing it was known by that protocol.
- CHAMPION_X_SELECTION6_MATRIX_53_AUDIT_2026-10-30.md records winning main numbers #01320 = 12 26 28 43 50 54 and X0 hit pattern [0,0,0,0,6,0]. The matrix is conditioned on historical Selection=6.
- CHAMPION_X_SELECTION_R19_SWAP_ABLATION_2026-10-27.md evaluates four stopping variants R19-0/1/2/3 on the same 624 draws; R19-2 selection total 2490 vs Frozen 2473, but ticket-level jackpot was not evaluated in this ablation.
- CHAMPION_X_DIRECTION_C_EXACT_PORTFOLIO_AUDIT_2026-11-03.md proves by exhaustive combinatorics that any six distinct fixed tickets have identical fair-draw jackpot probability 6/C(55,6), and disjoint partition geometry is isomorphic under relabeling.

## Timeline and limits
R19 source version name contains 2026-10-24, Phase1/Phase2 dated 2026-10-25, matrix dated 2026-10-30. These are report/version dates, not sufficient proof of original authorship or all earlier optimization decisions. Repository commit search returned incomplete matches for R19; an exhaustive path-level commit genealogy and earliest introduction of its exact blob have NOT been established. It is therefore **not proven** that #01320 was intentionally targeted while constructing Frozen R19. What is established is that #01320 was inspected during later development and cannot serve as untouched OOS evidence for that development.

## Multiple-testing interpretation
The unadjusted conditional allocation null for one frozen six-ticket policy is a counterfactual random partition. If dozens of historical policies were inspected and one was highlighted for its jackpot, its extreme unadjusted tail probability is selection-biased. The effective number of distinct tried policies and their dependency structure are not known from the currently reviewed reports; no defensible family-wise corrected p-value can be computed yet. Do not multiply the nominal p by a guessed trial count or claim an adjusted significance.

## Decision
Classify #01320 as a **retrospective discovery in a reused development set**, not a prospective prediction success. Do not modify Frozen, promote a challenger, or increase ticket budget. Next forensic gate: enumerate all historical candidate commits/scripts and trial logs, determine when #01320 was first observed relative to the creation of R19 Frozen, and perform a frozen-policy prospective evaluation only on genuinely unseen draws.
