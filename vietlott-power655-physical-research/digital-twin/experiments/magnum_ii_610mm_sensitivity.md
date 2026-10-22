# MAGNUM II nominal diameter sensitivity — preliminary gate

## Provenance and scope
The official operator-linked Power 6/55 rule documents SMART PLAY MAGNUM II and a **610 mm mixing-chamber diameter**. This is a published nominal dimension, not a verified inner collision surface or unit-specific CAD measurement. Existing baseline uses radius 0.320 m (diameter 640 mm); this isolated challenger uses radius 0.305 m. All other parameters remain baseline assumptions, including 25 RPM command, motor torque, collector, paddles and label assignment. The 55 numbered balls are **not** mapped to certified real physical units.

## Static checks performed
- JSON scenario has the same keys and values as `configs/baseline.json`, except `model` and `radius`.
- Radius 0.305 m exceeds the arm length 0.275 m and outlet radius 0.033 m. The simple clearance to arm tip is 0.030 m, only slightly larger than nominal ball radius 0.02525 m; this is **not** a swept collision clearance certification.
- 100 random-volume rejection-packing trials for seeds 0–99 successfully generated 55 nonoverlapping nominal spheres for both baseline radius 0.320 m and scenario radius 0.305 m, using the same Python/Numpy placement logic. This tests initial packing only, not Bullet contacts, run completion or unbiased capture.

## Execution status
**PyBullet was not installed in the independent evaluation environment.** Therefore no full rigid-body run, numerical/system validation, capture-success comparison, or sensitivity statistics were executed here. The configuration was committed to enable reproducible full testing in the existing Codex environment. Never describe this as a completed dynamics test or evidence of increased lottery odds.

## Required full comparison
Run with the frozen existing PyBullet 3.2.7 / Python 3.11.15 environment, same seeds for both configurations, without changing other physics parameters:

```powershell
cd vietlott-power655-physical-research/digital-twin
$py = 'C:/vietlott-digital-twin-env/Scripts/python.exe'
& $py -m pytest -q tests
& $py scripts/cli.py validate
& $py scripts/cli.py monte-carlo --config configs/baseline.json --start 1000 --seeds 20 --out results/magnumii_comparison_baseline.json
& $py scripts/cli.py monte-carlo --config configs/magnum_ii_diameter_sensitivity.json --start 1000 --seeds 20 --out results/magnumii_comparison_610mm.json
```

Record run-level failure flags, seven-ball completion, jamming, peak penetration, mean achieved motor RPM (not command), capture cadence, numerical convergence and paired differences. If validation fails, stop; do not present capture counts as reliable. Compare seed-by-seed and run an independent 40–80 seed replication only after stability checks. Do not overwrite original baseline results.

## Interpretation
A smaller chamber changes dynamics, but does not automatically improve fidelity or forecasting. The baseline motor is documented to stall under load (~5.124 achieved RPM vs 25 commanded); this must be measured again. Do not change torque and radius simultaneously. Do not treat the 610 mm nominal dimension as proof of internal contact geometry. A future separate hypothesis may vary motor torque, with a new pre-registered protocol.
