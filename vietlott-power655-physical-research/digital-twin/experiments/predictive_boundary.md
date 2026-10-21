# Prediction assessment gate

Four separate outcomes:

1. Producing seven physical exits is a software/mechanical-function result.
2. Reproducing actual dynamics requires independently measured geometry, per-ball properties, control timing and validation trajectories. This gate is **not passed**.
3. Detecting real machine bias requires an identified, numerically stable and externally validated physical model plus sufficient independent trials. Sensitivity or asymmetry in an assumed pocket proves neither Vietlott bias nor a number-specific effect.
4. Pre-draw forecasting requires strict-past available state and independently scored future draws. No such initial-state measurements or previously unseen holdout exist here. **No probability forecast or Jackpot performance is reported.**

Uniform inclusion probability is 6/55 for a label among six main balls. Special selection is conditional on the remaining 49 after mains. These are different nulls. Randomized labels are metadata independent of mass, diameter, insertion order and physical seed. An exact permutation check should leave trajectories and physical IDs unchanged and transform only printed labels. Solver insertion order is a separate numerical check; different trajectories under reverse creation order are expected in a chaotic contact system and cannot establish physical label bias.

B1 and B7-100 source were read but protected. A fair eventual predictive benchmark must freeze **six tickets per draw** for every policy, including uniform, B1 and a prespecified six-ticket reduction of B7-100 chosen without access to targets. One cannot compare 100 B7 tickets to six twin tickets or cherry-pick six after the draw. Score pre-draw marginal Brier/log loss and ticket metrics on the same chronological holdout with draw-cluster uncertainty. An ensemble generated inside this simulator is not a dataset of actual future lottery draws and must not be used to manufacture backtest Jackpot gains.

The limited 20-seed baseline ensemble is a diagnostic of a hypothetical machine. With 120 main captures, expected main count per number is only 2.18. Per-label event counts are too sparse for asymptotic chi-square inference or claims of fairness. All failures remain in completion denominators; valid-run-only descriptive timing is labelled. Any apparent effect must first be traced to geometry, loading, parameter choice and solver stability. No real hardware per-ball property evidence supports a number preference.

Scenario attribution is limited: friction scenarios change sliding and rolling parameters together; the ball-tolerance scenario changes mass and diameter together, and conservative packing spacing also changes initial positions. These are combined sensitivity scenarios, not separately identified causal mass/diameter effects. `results/physical_property_diagnostics.json` reconstructs the exact property RNG for a descriptive selected-versus-all comparison; three ensembles cannot establish a physical selection preference. `results/power_planning.json` supplies an explicitly theoretical independent-draw power illustration, not evidence about real lottery bias.
