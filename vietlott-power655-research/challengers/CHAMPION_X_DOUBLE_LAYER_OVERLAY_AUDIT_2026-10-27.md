# Champion-X — Double-layer 624-draw winning-ticket overlay (2026-10-27)

## Reproduction
Independent JavaScript reconstruction of frozen R19 algorithm and Hybrid6 dependency; **not a Python clean-checkout PASS**. Source frozen blobs R19 `a7ebf4fa5216e1bfd4906087e04555044d3e58f0`, Hybrid6 `252f6e0e3dad70a80a4b0cf7febe92d5d080e264` unchanged. Upstream JSONL data fetched from commit `52d37a1d9208fc4178b0e5be73b8653c38ff88de`, 1415 rows through draw #01415. Known row-order anomaly retained. Exactly 624 target positions 789..1412, all predictions based strictly on rows[:index]. Winners only overlaid after tickets computed. Research-only, extensively used historical in-sample.

## Deliverable
`CHAMPION_X_DOUBLE_LAYER_OVERLAY_624_2026-10-27.csv`: 624 rows. Per row: dataset index, ID, date, Selection, best-hit, canonical sorted ticket-hit pattern, six winning main numbers sorted ascending, six issued original R19 final tickets, six per-winning-label details. The per-number detail token is `number:ticket-or-minus:origin:rF156_rank:fF156_count:mF30_count`. `TOP` = retained from original 36 highest F156, `HYBRID` = Hybrid6 added outside top36 retained after R19, `R19` = newly entered during R19 swaps, `MISS` = absent from all six final tickets (ticket '-'). Rank is F156 sorting position with ascending label tie break. This table overlays winning labels onto tickets, not a new allocation.

## Invariants checked
- Source selection histogram S=0..6: `[0,7,59,140,215,150,53]` (sum 624).
- Source Frozen best-hit histogram h=0..6: `[0,233,335,50,4,1,1]` (sum 624).
- All six main winner appearances = `624*6=3744`. Origin classification: `TOP=1890, HYBRID=382, R19=201, MISS=1271`. Selected sum `1890+382+201=2473`; total `2473+1271=3744`.
- Historic sorted hit-pattern leaders: `2-1-1-0-0-0` 126, `1-1-1-0-0-0` 79, `1-1-1-1-0-0` 71, `2-1-1-1-0-0` 69, `2-1-0-0-0-0` 58, `1-1-0-0-0-0` 53, `2-2-1-0-0-0` 35.
- Count of winning R19-entered labels across ticket indices 1..6: `[30,35,35,30,34,37]` (sum 201). Any apparent index difference should be interpreted using group exposure, not direct success counts.
- F156 rank bin of all six main winning labels, bins 1–10, 11–20, 21–30, 31–40, 41–50, 51–55: `[685,664,675,703,690,327]`. Last bin only 5 possible labels, so do not compare raw bin totals across unequal bin sizes.
- Original raw row-order anomaly can affect strict chronological interpretation. Not silently repaired.

## Interpretation
1. The overlay explicitly separates Selection failure (MISS labels) from ticket Allocation (selected labels distributed across ticket indices).
2. An oracle after seeing winners could regroup same-target selected winners into one ticket, but this does not establish a usable prediction rule. Existing best-hit distributions versus exact random partition controls are in `CHAMPION_X_WINNING_OVERLAY_624_CONDITIONAL_NULL_2026-10-27.md`.
3. Common split patterns alone are combinatorially expected; they should not be promoted as discovered mechanisms.
4. Feature evaluations by label origin and F156/F30 must be conditioned on label exposures and per-target Selection, and verified with strict-past or genuinely future holdouts. Row inclusion based on winning Selection=4..6 is a retrospective diagnostic and not a pre-draw selector.
5. No frozen model source, registered Champion or ticket prediction was changed. No new allocation was promoted.
