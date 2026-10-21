# Phase 4 — independent label audit and chronological expansion

Parent Phase 3 commit: 3356895595426eb7d57c8a83445aa06ca79e254a. This is a work order, not evidence that the review or expansion is complete.

## Mandatory independent blind review
- Do not expose Phase 3 `primary_labels.json`, `draw_order_verified.csv`, published numbers or Phase 3 conclusions to the second reviewer before they independently transcribe all 35 capture images.
- Present original full-resolution frame pairs in randomized draw/capture order, with only source/time and capture role; record each digit or NA, source frame hash, reviewer identifier, timestamp and uncertainty.
- Freeze the independent labels before comparing against Phase 3. Keep both versions and a discrepancy/adjudication log. The same Codex process re-reading its own labels does NOT count as independent human review.
- Compare unordered six-main sets and special against a traceable official Vietlott result; if official source unavailable, retain provisional status even if secondary sources agree.
- Never infer sequence from sorted published results or overlay animations.

## Chronological expansion
After the review gate passes, lock source selection rule and select >=100 distinct historical draws with available video, not based on outcomes. Keep failed/duplicate/unreadable entries and machine/ball-set unknowns. Keep newest 20% holdout sealed until analysis locked. Do not claim missing video was checked unless it was searched.

## Statistical checks
Conditional permutation of six observed main numbers within each draw for position and directed adjacency, treating draw as independent cluster; separate special null from remaining 49. Correct multiple tests, and never equate position bias conditional on inclusion with a pre-draw inclusion edge. If no verified cohort, primary results remain NA.

## Deliverables
`phase4/PHASE4_HANDOFF.md`, `blind_labels.csv`, `review_comparison.csv`, `official_reconciliation.csv`, `source_selection_ledger.csv`, `draw_order_verified_expanded.csv`, `analysis_results.csv`, `validation_report.json`, `scripts/`, `evidence/`. All with source SHA and repeatable commands. Do not modify B1, C50, B7-100, B7-200, Champion, or merge to master.

## Acceptance
No 'verified_two_reviews' without two genuinely independent reviewers plus official reconciliation. If unavailable, report failure transparently, preserving provisional data. Pilot of five draws cannot establish predictive advantage.
