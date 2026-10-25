# Champion-X Phase 2 — six-state consensus Selection audit (2026-10-25)

## Frozen identity and data fixture
- X0 is the unmodified R19-CROSSRANK-FROZEN-2026-10-24 (blob `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`).
- Hybrid6 dependency is unchanged (blob `252f6e0e3dad70a80a4b0cf7febe92d5d080e264`).
- The **original pinned raw dataset** blob is `1230696771274d48b261a0cfbd728444700c299e`, 1,414 rows. Upstream latest main currently has 1,415 rows (through 2026-10-24): do not silently treat new data as the same raw snapshot.
- Original-order anomaly at zero-based row 779: ID #00944 with only six values appears out of ID order. Do not silently repair or claim chronologically clean verification on this fixture.
- Legacy window: zero-based indices 789..1412 inclusive, 624 targets. Features only use `rows[:index]`; target `result[:6]` is for scoring.
- **Selection 6/6 is not ticket Jackpot 6/6**. This Phase 2 measures Selection only.

## Six-state frequency
For each target and each number n in 1..55, `votes[n]` counts inclusion among X0/X5/X15/X30/X60/X90 sets of 36. Per target, exactly 216 votes. Groups are `votes=0..6`, including stable 6-of-6, partial 2..5, exclusive 1-of-6, and never 0-of-6.

Report size of each group, winning-label hits, and winner hits excluded by X0. Individual draw records include six selections, every group, true winners, X0 misses, recovered and discarded winners.

## Predefined non-oracle comparators (all 36 labels)
- X0: frozen Selection.
- majority36: descending vote count; ties preserve X0 membership first, then smaller label. Take exactly 36.
- minority36: ascending vote count; intentionally anti-consensus diagnostic, same ties.
- matched random replacement: per target replace exactly `k=|majority36 - X0|` labels from X0 with k of the 19 excluded numbers; seed fixed per target and replicate, default 100 draws. This matches change magnitude only, not signal composition.

Primary selection metrics: total selected winner appearances (Selection), distribution 0..6, Selection >=5 and =6. Temporal diagnostics: disjoint 156-draw quarters. Compare majority recovered winner appearances versus lost. No selection of winning state after seeing the draw is allowed.

## Execution and promotion criteria
1. Verify original Frozen source hashes at runtime.
2. Record exact data Git blob and SHA256; `--strict-pinned` enforces original data blob.
3. **X0 must equal 2473** on the exact original 624-target window before any Phase 2 comparison is accepted. Script fails loudly otherwise.
4. Run independent Python clean-checkout and inspect per-draw golden cases, including #01320, before calling this reproduced.
5. Historical 624 targets have already influenced experimentation; even a large retrospective improvement does not establish an out-of-sample forecasting edge. For forward claims, pre-register one fixed policy and test on future draws never used in candidate selection.
6. The theoretical fair-draw expectation for any preselected 36 of 55 = `6*36/55 ≈ 3.92727` winners per draw. Mere majority sorting cannot change odds for independent uniform lottery outcomes.

## Run
Put the new Phase 2 script alongside unchanged Phase 1 and Frozen source files:

```bash
python champion_x_phase2_consensus_20261025.py --data /path/to/pinned-1414-row-power655.jsonl --output /tmp/champion_x_phase2.json --first 789 --last 1412 --random-reps 100 --strict-pinned
```

Use a new output path for any nonpinned 1,415-row fixture and record its blob. Note that extending data by one row does not change the legacy window or its preceding records, but running a different fixture is not an exact original reproducibility check.

## Status on 2026-10-25
Source Phase 2 was committed to GitHub without changing Frozen code. A complete Python replay / clean-checkout PASS, real Phase 2 group frequency counts and selection results have **not** been produced or independently verified. Do not infer new numbers from Phase 1's JS reconstruction or from this unexecuted Phase 2 source.
