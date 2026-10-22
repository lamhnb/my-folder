# B1 → Physical Simulator, Version A (rank-to-position)

Base physical simulator commit: 01a56ea5f1f453960bf662ac64b0c129b1aa2006. This is an experimental challenger, not a champion.

## Fixed design
For each historical draw t in the same 624-draw B1 evaluation window:
1. Compute rolling counts of the previous 156 draws, six main numbers only. Sort by descending count and ascending number on ties. Never read draw t when creating its prediction.
2. Construct deterministic initial ball slots using the existing simulator packing routine with fixed packing seed, independent of draw outcomes. Rank slots by (z,x,y,physical_id) lexicographically; assign B1 rank[0] to slot[0] ... rank[54] to slot[54]. Document coordinate system and orientation. Avoid any dependence on future draw data.
3. Use exactly the same physical configuration and simulation seeds for every t. Freeze all geometry, physics and capture rules. Run a fixed ensemble of seeds; record all failures and valid-run counts. Do not change physics based on target results.
4. Count main-capture frequencies by label. Rank all 55 labels by simulated main frequency (tie-break B1 rank then numeric). Take top 36; allocate six disjoint tickets using B1 stride-6 layout.
5. Compare to B1 six-ticket baseline and random-permutation control using exactly the same draws, ticket budget and evaluation. Report best-hit histogram 0..6, >=3/4/5/6, Jackpot 1 and Jackpot 2, as well as paired differences and null permutation distribution.
6. Lock protocol and random seeds before running historical targets. Treat 624-draw historical performance as exploratory, not a clean future holdout. No parameter/seed search to maximize historical hit rates.

## Critical scientific check
If physical IDs and ball properties are exchangeable, any apparent advantage can be produced by arbitrary rank-to-slot assignment. Randomize the mapping while preserving each draw's B1 ranking and the identical physical simulation, and compare Version A against these controls. Mapping is an assumed mechanism, not documented Vietlott loading order.

## Artifacts
Write source and tests under digital-twin/experiments/b1_physical_a/ without changing existing simulator, B1, B7 or Champion. Include mapping manifest, strict-past test, seed plan, simulation failure ledger, per-draw tickets, score summary, paired control and full handoff. Explicitly separate code implemented, simulation executed, and historical replay executed.

## Execution
Run the experiments, not merely this plan, where PyBullet and source data are available. Do not call unexecuted output a backtest. Commit to this branch only.
