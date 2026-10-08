# Vietlott Power 6/55 Research

Version: **v0.1.0** (2026-10-08) — experimental baseline, not validated predictive edge.

## Purpose
Reproducible strict-past walk-forward training and portfolio selection for Power 6/55. This code is a clean implementation inspired by our experiments, **not** an exact reproduction of every exploratory run in chat. No guaranteed advantage over random lottery selection.

## Data
Provide `draws.jsonl`, one JSON object per line, sorted chronologically, e.g.
`{"date":"2026-10-08","id":"01408","result":[1,7,12,27,31,52,6]}`.
First six entries are main numbers; seventh is special and excluded from modeling. A public example source is https://github.com/vietvudanh/vietlott-data (verify provenance before use). No data file is committed here.

## Run
Python 3.10+; standard library only:
```bash
python vietlott-power655-research/train.py --data draws.jsonl --holdout 14 --train-window 112 --output results.json
```
The last 14 draws are concealed for sequential replay. Each hidden draw is revealed only after its prediction is saved and scored. The model updates strategy weights after each reveal. The earlier training window chooses a fixed configuration; no future leakage.

## Methods
- Individual frequency scores (60/120/365/all prior draws), Laplace-style smoothing.
- Six disjoint valid tickets via block, stride, or deterministic pair-swap optimization.
- Pair-swap greedily increases historical pair co-occurrence score while retaining six unique numbers per ticket.
- Training selects the best strategy by number of draws with at least one ticket >=3 matches, then >=4, then mean best match.
- Holdout sequentially updates expert weights by multiplicative reward. Reports all candidate outcomes and portfolio picks.
- Includes a random six-ticket benchmark with a fixed seed.

## Caveats
- The holdout is used for online learning, so it is not a fully untouched final evaluation of the *final* adaptive model.
- Trying many strategies on the same holdout can overfit; reserve a separate later time period for final confirmation.
- For a fair independent draw, each six-number combination has Jackpot 1 probability 1/28,989,675.

## Versioning
- **v0.1.0**: reproducible loader, validation, walk-forward learner, pair-swap portfolio, JSON report.

## v0.2.0 (experimental, 2026-10-08)
Run `python vietlott-power655-research/train_v020.py --data draws.jsonl --train-window 112 --holdout 28 --output results_v020.json`.

Adds online exponentially weighted probability ensemble (five lookback horizons), pair-aware swap portfolio search with an overlap penalty, training-only selection of overlap penalty, chronological hidden-period replay, and random baseline. Predictions are generated before each hidden result is revealed; model weights update afterward. This implementation has been committed but has **not yet been executed or validated in this GitHub workflow**. Compare with v0.1.0 on identical time windows before promotion. Model scores do not imply increased physical jackpot odds.
