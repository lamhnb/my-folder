# Phase 3 — Draw-order dataset and positional-bias audit

Base: research/power655-physical-phase2 @ dae213662171d1066876de0095b44b1f2cad12cd.
Status: research protocol; **no verified draw-order dataset yet**. Do not modify B1/C50/B7 or champion.

## Research question
Can independently verified physical capture order of Power 6/55 balls support a repeatable, pre-draw predictive signal? Distinguish order-conditioned effects from inclusion probability. Sorted main-number arrays in power655.jsonl are **not** physical draw order.

## Stage A: five-draw pilot
Use source videos and provenance in phase2/phase2_sources.csv and 35 indexed captures in phase2/capture_event_audit.csv for #01372–#01376. Decode actual stills/footage, not metadata. For each of 7 captures, read the numbered ball after it has settled and before the next capture, using image and (when possible) audio; record PTS, source ID, evidence image path/hash, confidence, and independent reviewer result. Use only authorized media. If illegible, NA. Capture 7 is the special ball. Verify unordered first-six set against independently sourced official six numbers and special separately. Never infer order by sorting or by a changing broadcast graphic without checking whether it preserves capture order.

## Required CSV
draw_order_verified.csv columns:
draw_id,draw_date,source_id,source_sha256,capture_index,ball_type,ball_number,readable_pts_start,readable_pts_end,evidence_image_path,evidence_sha256,primary_review,secondary_review,confidence,verification_status,notes

Allowed verification_status: verified_two_reviews, provisional_one_review, ambiguous, unavailable, source_conflict. Only verified_two_reviews enters the primary analysis. Retain conflicts; no guessing. Record 7 distinct numbers 1..55 for each fully verified draw, with first 6 matching the published unordered main set, seventh matching published special.

## Stage B: expand without tuning to outcomes
Once pilot recognition quality is measured, freeze extraction/review protocol, then extend to at least 100 distinct chronological draws if accessible. Preserve original source and exact dates; multiple uploads of one draw count once. Record selection/missingness and machine/ball-set metadata if actually available. Reserve latest 20% chronological draws untouched for final evaluation. Five draws alone are insufficient for reliable per-number-by-position inference.

## Stage C: statistical tests
Primary null: conditional on the observed six main numbers, their physical capture order is uniformly random over 6! permutations. For each draw use permutations of that draw's observed six, preserving unordered inclusion and temporal clustering by draw. Test a predeclared omnibus position-number association statistic, calibrate with draw-level Monte Carlo permutations, and report uncertainty/multiple testing. Do not mistake sorted order for capture order. Special capture is sampled from remaining 49, not exchangeable with the six main positions; analyze separately using correct conditional null.

Secondary question (distinct): whether **inclusion** of a number is predictable before the draw, versus only position given inclusion. Compare chronological prequential log loss/Brier to uniform and strict-past baseline, use separate future holdout. No model promotion based on exploratory data. Consider machine/ball-set stratification only when independently identified. Do not use observed outcome to tune detection thresholds or hypothesis definitions.

## Deliverables
phase3/PHASE3_HANDOFF.md, phase3/draw_order_verified.csv, phase3/source_registry.csv, phase3/quality_audit.csv, phase3/order_bias_tests.csv, phase3/analysis_plan.md, phase3/scripts/, phase3/evidence/ and phase3/validation_report.json. Report number of complete verified draws, ambiguous cases, coverage, cross-review agreement, source conflicts, effect sizes and Monte Carlo p-values. If fewer than 100 verified draws, present pilot and power limitations, not predictive claims.

## Acceptance gates
A: 35 capture labels inspected, full seven-number reconciliation and review quality documented. B: independent second review; clear source provenance. C: locked protocol, conditional permutation test, holdout untouched. Do not claim predictive advantage from a position bias alone. Commit only on this branch, no merge to master.
