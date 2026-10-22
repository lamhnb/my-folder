# Power 6/55 physical audit

Start with [AUDIT_REPORT.md](AUDIT_REPORT.md). New recovery identifies the **operator-documented SMART PLAY MAGNUM II**, with nominal dimensions, from a 2023 rule/2025 amendment linked on Vietlott's official process page. Four visible case codes were also recovered. Per-draw serials, certified set identities, actual maintenance dates and actual per-ball measurements remain unresolved.

| Deliverable | Contents |
|---|---|
| [ARTIFACT_INVENTORY.csv](ARTIFACT_INVENTORY.csv) | Prior artifacts by ref snapshot/location/SHA; local-only files; fsck/reachability cross-check. Snapshot SHA is not necessarily file introduction SHA. Full change history is in `extracted/commit_file_history.csv`. |
| [PHYSICAL_DATA_STATUS.csv](PHYSICAL_DATA_STATUS.csv) | 143 entries, including every original registry parameter and recovered normative data. `value_SI`, basis/scope and `actual_2026_asset_status` prevent a documented nominal from masquerading as a measurement. |
| [MACHINE_BALLSET_HISTORY.csv](MACHINE_BALLSET_HISTORY.csv) | Six traceable draw/date records. Machine ID/certified set ID UNKNOWN; documented model and observed case code in separate columns. Not a fabricated complete national draw-history dataset. |
| [EVIDENCE_REGISTER.csv](EVIDENCE_REGISTER.csv) | 45 evidence records: primary URLs, pages/PTS, file hashes, method, scope, confidence and limitations. |
| [SIMULATOR_PARAMETER_GAPS.md](SIMULATOR_PARAMETER_GAPS.md) | Physical-fidelity impact and full 99-row dependency-map link. |
| [RECOVERY_PLAN.md](RECOVERY_PLAN.md) | Only remaining actionable data gaps, plus reproduction commands. |

Statuses: VERIFIED supports the exact scoped statement, PARTIAL has some verified records but an unresolved join/coverage, ESTIMATED is a stated derivation, NOT_FOUND is a negative bounded search outcome, NOT_EXECUTED is explicitly unperformed work, NOT_AUDITABLE means execution evidence unavailable. NOT_PUBLIC requires affirmative evidence about access; it is not assigned here.

CSV text uses UTF-8 and RFC-compatible quoting via Python `csv`. Unknown identities/measurements use literal `UNKNOWN`; original registry `NA` values are preserved only in simulator columns. Source IDs in `evidence_ids` are semicolon-separated. `actual_2026_asset_status=NOT_FOUND` can coexist with VERIFIED normative specification: these are different claims. Implementation controls are verified as code settings, not hardware measurements.

`extracted/current_rule_facts.csv` contains 32 visually transcribed facts with PDF page numbers and source SHA. `individual_ball_specs.csv` has 55 label rows with separate nominal/actual fields, not 55 actual specimens. `maintenance_events.csv` has zero actual event rows; `operator_history_events.csv` separately records the documented venue amendment. Native images, videos, source PDF/HTML and display crops remain local-only; URL/PTS/hash manifests and replay scripts are committed. Single-auditor readings are not relabeled as independent review.

From this directory:

```powershell
$py = 'C:/vietlott-digital-twin-env/Scripts/python.exe'
& $py scripts/build_audit_tables.py
& $py scripts/validate_audit.py
```

Portable validation skips unavailable local media checks explicitly. This environment validated local media/PDF hashes as well. No simulator run or physical recalibration is performed. All pre-audit code/data and protected branches remain unchanged; no master merge.
