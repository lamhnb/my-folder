# Champion Registry — v0.2.1 (2026-10-08)

**Status: frozen experimental champion candidates, not proven predictive edge.**

- **Pair-60**: 6/28 held-out draws with at least one ticket >=3 main-number matches; 0/28 >=4. 112 training draws: 16 draws >=3, 1 draw >=4.
- **Stride-365**: 6/28 held-out draws >=3; 0/28 >=4. 112 training draws: 9 draws >=3, 1 draw >=4.
- The results above came from exploratory replay and must be independently reproduced from committed code before being called verified.
- Do not replace champion based on the same 28 draws repeatedly: the holdout has already been inspected. A new unseen chronological window is needed for an honest promotion decision.
- Physical jackpot odds for six distinct tickets remain 6/28,989,675 if drawings are fair.

**Champion selection policy**: freeze both Pair-60 and Stride-365; train challengers on earlier draws; compare against both with exactly the same six-ticket budget and untouched evaluation windows; record >=3, >=4, mean best, and random benchmark.
