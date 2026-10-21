# Phase 3 analysis and recognition lock — 2026-10-21

Parent protocol: `PHASE3_RESEARCH_PROTOCOL.md` at e55fd8dba5bac41c7c157a5a3bc0d7ff2718de7a. Read Phase 1 FINAL_HANDOFF/METHODS and Phase 2 PHASE2_FINAL_HANDOFF/DATA_DICTIONARY before work. This plan is written before Phase 3 pixel labels or order statistics. Published unordered pilot outcomes have already been encountered in source discovery; the pilot is not a blind validation set.

## Recognition v1

Use only five SHA256-pinned Phase 2 local MP4s and their existing capture indices. Validate complete source bytes before extracting. Capture 1–6 main, 7 special. Decode full native 1920x1080 PNGs at source PTS, with no enhancement, interpolation, OCR filling, or generated pixels. First pass: seek Phase 2 ramp upper bound + 2.0 s; retain samples every 0.5005 s for 3.0 s. This sampling locates readable settled balls, not physical capture time. If a ball is unclear, extend within the interval before the next indexed capture; log the reason and each extraction, never pick a number from published outcomes. Read the newest physical ball on the actual result rail; inspect collector/trajectory context if association is unclear. Graphics may corroborate but never supply an otherwise unreadable ball label. Missing physical digits remain NA. Same-agent reinspection is not an independent reviewer.

Retain full native frames and hashes; contact sheets are explicitly reduced viewing aids. For each accepted label link two observed readable frames where available; start/end are observed samples, not a continuous readability interval. Every row retains primary/secondary reviewer identity, confidence (categorical visual judgment, not accuracy probability), and protocol status. Never mark verified_two_reviews without two distinct independent review records plus official reconciliation. Source/date identity is separately qualified.

Gate for historical expansion: complete seven-ball physical readings, independent second review and official unordered-result reconciliation for all five pilot draws, zero unresolved disagreements. Until this passes, do not generate 95 nominal or invented historical observations. Record an expansion gate failure explicitly. Once passed, freeze this v1 method; enumerate consecutive historical draw IDs ending before the pilot (no outcome-based selection), log missing/duplicate/graphic-only sources, and acquire at least 100 distinct eligible draws if possible. Machine/model/ball-set IDs stay NA absent documented linkage. Do not infer equipment from color.

## Statistical lock

Primary analysis accepts only complete seven-row draws with verified_two_reviews and official reconciliation. Independent unit: draw. Primary discovery requires >=80 training draws from >=100 eligible chronological draws; reserve latest ceil(20%) untouched for evaluation. Pilot labels are development data and never a future holdout. Partition and hash IDs before running outcome analyses. Missing or unavailable input is not a negative finding.

H1 omnibus: for the 55x6 number-position count table C, use sum((C[n,p]-m[n]/6)^2/(m[n]/6)) over cells with m[n]>0. Each null replicate independently permutes the six observed main numbers within each draw. This preserves each actual unordered set and clustering. No asymptotic chi-square p-value on sparse cells.

H2 omnibus: directed adjacent-number transition table across five transitions per draw. For a!=b, conditional expected count E[a,b] = sum_d 1({a,b} subset S_d)/6. Statistic sum((C-E)^2/E) over E>0. Permute within each draw as above; never shuffle across draws or treat transitions as independent trials. Report descriptive mean absolute adjacent gap in ball-number units, with draw-cluster bootstrap uncertainty only if n>=20.

H3: on a sufficient training cohort, split chronologically in half (at least 40 draws/half). Compare centered position residuals by cosine alignment; joint within-draw permutations calibrate positive alignment. Significant alignment alone is not stable inclusion prediction. Replication on the untouched latest 20% remains required; sparse/absent periods => not_testable.

H4: only with independently documented equipment IDs and at least 20 draws/configuration in each of two chronological periods. Otherwise not_testable; no imputation. Implementation is deferred until these inputs exist, rather than choosing strata from outcomes.

Special: separate diagnostic for sum(special - mean(remaining 49)). Conditional null draws one number uniformly from {1..55} minus each actual six-number main set. Never permute all seven. H1–H4 plus special are one predeclared family of five hypotheses; Holm FWER alpha .05 (nonexecuted hypotheses conservative p=1 for adjustment only, displayed p=NA). Number/cell followups require separate multiplicity correction and independent holdout.

Monte Carlo: 19,999 replicates, fixed seed 20261021, p=(1+exceedances)/(B+1); report exact binomial 95% interval for underlying null exceedance probability, not effect CI. H1/H2 effects: observed omnibus minus conditional null mean, standardized by null SD (null-standardized discrepancy, not predictive gain). For n>=20, 2,000 draw-cluster bootstrap replicates for descriptive effect intervals; small-pilot CI remains NA. No numeric p-values in primary results when eligibility/sample gates fail. Unit-test fixtures are synthetic software checks and never research data.

## Predictive boundary

Order conditional on inclusion is separate from the marginal probability of inclusion. No signal/model/B7 code is created now. Only after reproducible tests, separately preregister a pre-draw inclusion score using available strict-past equipment information; compare chronological prequential Brier/log loss to uniform 6/55 and strict-past frequency baseline, then evaluate exactly once on a future untouched holdout. Coverage optimization cannot establish increased jackpot probability. B7-100/Champion remain protected.
