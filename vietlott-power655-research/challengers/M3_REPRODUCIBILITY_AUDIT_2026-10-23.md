# M3 audit: historical result mismatch (2026-10-23)

## Finding
Independent strict-past reconstruction from committed `challengers/m3_reverse3_momentum.py` does **not** reproduce the previously reported 7 draws >=4/6.

Using the 624 draws #00789–#01413, the committed logic produces **5 draws >=4/6**, not 7. The only newly gained >=4/6 draw versus Adaptive is #01116; #01198 drops from 4/6 to 2/6. The claimed #01229 and #01271 gains do not reproduce.

## Root cause
The earlier interactive backtest implementation chose replacement slots by sorting the **current mutated** array after each insertion, whereas the committed code also does so, but the interactive test used a subtly different candidate ordering/tie handling and did not freeze a single authoritative executable artifact. This is a hypothesis about the source of discrepancy, not a verified root cause. A line-by-line deterministic replay and regression fixtures are needed before changing implementation.

## Status
- M3 remains experimental challenger.
- Historical >=4/6 = 7 must be marked **UNVERIFIED / NOT REPRODUCED**.
- Do not promote M3 or overwrite B1/Adaptive.
- Add per-draw golden fixtures and compare source-code output to reference draw IDs #01116, #01198, #01229, #01271, #01320.
- Preserve original code for forensic comparison; do not silently rewrite the model to match a preferred score.
