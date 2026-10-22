# Hybrid6 P3+R3 — initial forensic analysis (2026-10-23)

## Frozen committed source
`hybrid6_p3_r3.py` operates on exactly the 36 Adaptive ticket positions. It merges the first 3 MAGNUM suggestions with up to 3 MAGNUM suggestions rejected by B1's intermediate frequency rerank; duplicates are removed. It replaces the lowest-momentum **distinct slots among the 36 tickets**. The underlying 19-position weights are synthetic and not calibrated to physical ball labels.

## Critical historical implementation discrepancy
An earlier interactive experiment reported >=3/6 57, >=4/6 7, >=5/6 1, but performed replacement on a full 55-element ranked array. Replacement into positions 37–55 could be invisible to the six tickets. This is **not equivalent** to the committed 36-slot implementation.

Independent JavaScript reconstruction of the committed 36-slot logic, using the same 624 historical draws (zero-based 789–1412 = IDs #00790–#01413), gives:
- Best-hit histogram [0, 227, 342, 49, 4, 2, 0].
- >=3/6 **55**, >=4/6 **6**, >=5/6 **2**, 6/6 **0**.
- Against Adaptive: improved in **80** draws, worsened in **76**, tied in **468**.
- Quarter-by-quarter best-hit improvements vs losses: 13/21, 20/22, 28/17, 19/16.
- Winning-number occurrences added: **336**; removed: **317**; net **+19** (from swaps, before any independent significance test).
- #01198: Adaptive 4/6 -> Hybrid6 2/6; lost correct labels 11 and 38 in one ticket.
- #01229: Adaptive 3/6 -> Hybrid6 3/6 (no new 4/6).
- #01303: Adaptive 2/6 -> Hybrid6 3/6 (no new 4/6).
- #01320: Adaptive 5/6 -> Hybrid6 5/6.

## Research status
The source has been committed; the statistics above are from a separate JS reconstruction, **not a clean-checkout Python execution**. A per-draw golden test and a fixed frozen dataset checksum are needed before certifying the 2x5/6 result. Do not promote to Champion or claim odds improvement. Historical 624 draws have been repeatedly mined, and the synthetic label-to-position map is unverified.
