# Champion-X: R19 Frozen as X0 — correction 2026-10-25

## Required baseline
**X0 = R19-CROSSRANK-FROZEN-2026-10-24**, not Hybrid6.
Immutable base commit: 5b951585b6d55c18ab6671b3974bb18347d40892.
R19 source blob a7ebf4fa5216e1bfd4906087e04555044d3e58f0.
Hybrid6 dependency blob 252f6e0e3dad70a80a4b0cf7febe92d5d080e264.

All X variants run **the same frozen R19 algorithm** on perturbed earlier history. The original R19 source and its dependency are untouched.

## Retired benchmark
Previous X0=Hybrid6 statistics (Selection 2487, best-hit sum 1084 over 624 draws) belong ONLY to the initial pilot and MUST NOT be labeled Champion-X R19 baseline or compared as if the updated script reproduced them.

## R19 X0 expected historical benchmark
Target indices 789..1412 inclusive: Selection **2473**, best-hit sum **1080**, >=3 **56**, >=4 **6**, >=5 **2**, >=6 **1**. These are prior independently reconstructed figures, NOT a fresh direct Python execution PASS.

## Experimental X variable
Take exactly 156 earlier draw rows and cyclically rotate them by X in [0,5,15,30,60,90]. No target draw is read before scoring. F156 remains unchanged, F30 changes, and then full original R19 runs on that transformed history.
X>0 intentionally destroys the chronological interpretation of recent 30 draws. It is only a sensitivity stress test, NOT a real independent forecasting signal.

## Reproduction
python vietlott-power655-research/challengers/champion_x_input_sensitivity_phase1_20261025.py --data power655.jsonl --output champion_x_r19.json --first 789 --last 1412

Data: vietvudanh/vietlott-data/data/power655.jsonl; six main numbers only, and known historical anomaly in raw data. Record data snapshot hash when running.

## Status
Updated source committed but R19-X0 end-to-end Python replay and all X>0 statistics NOT YET EXECUTED OR VERIFIED. Do not reuse the prior Hybrid6-X figures for this experiment. No changes to R19 Frozen, Hybrid6, S3 or registered Pair-60 / Stride-365.
