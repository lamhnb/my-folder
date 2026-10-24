# Champion-X Phase 1 audit — 2026-10-25

Status: research only; no registered Champion modified.

## Model identity
The repository's CHAMPION.md registers Pair-60 and Stride-365.
This pilot runs the separately frozen Hybrid6 P3+R3 reference (Git blob 252f6e0e3dad70a80a4b0cf7febe92d5d080e264) from base commit 5b951585b6d55c18ab6671b3974bb18347d40892.

## X intervention
X rotates the last 156 preceding draw records by 0, 5, 15, 30, 60, or 90 positions. The multiset of past draws and F156 counts remain identical. F30 membership changes; no target draw result is read during prediction.

IMPORTANT: X is a counterfactual perturbation that changes the meaning of the recent window. It tests sensitivity and is not a new source of predictive information.

## Exploratory 624-draw replay
Window: zero-based indices 789 through 1412, 624 targets, six main numbers only. Public dataset: vietvudanh/vietlott-data/data/power655.jsonl. Retain its original historical ordering; it has a known anomalous record.

| X | Selection | Sum best-hit | >=3 | >=4 | >=5 | >=6 | Changed labels total |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 2487 | 1084 | 55 | 6 | 2 | 0 | 0 |
| 5 | 2460 | 1081 | 59 | 2 | 0 | 0 | 2715 |
| 15 | 2460 | 1083 | 62 | 4 | 0 | 0 | 4288 |
| 30 | 2453 | 1074 | 58 | 2 | 0 | 0 | 5416 |
| 60 | 2475 | 1079 | 52 | 4 | 0 | 0 | 5294 |
| 90 | 2439 | 1064 | 47 | 7 | 0 | 0 | 5310 |

Quartile Selection:
X0 613/640/621/613;
X5 584/630/622/624;
X15 598/613/636/613;
X30 608/608/621/616;
X60 635/614/625/601;
X90 611/609/612/607.

Calculated independently in JS from upstream data and source logic. Direct Python replay and seed-based matched random controls have not been executed and are NOT certified PASS.

## Decision
The intervention generates substantially different 36-label sets but all nonzero X reduced aggregate Selection. No predictive gain established. Do not modify Pair-60, Stride-365, Hybrid6, S3, or R19 Frozen.

## Run
python vietlott-power655-research/challengers/champion_x_input_sensitivity_phase1_20261025.py --data power655.jsonl --output champion_x.json --first 789 --last 1412
