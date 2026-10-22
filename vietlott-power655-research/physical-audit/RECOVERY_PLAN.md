# Remaining actionable recovery gaps

Completed recovery is in `AUDIT_REPORT.md`. Do not repeat broad model-guessing searches or rebuild the simulator as a substitute for acquiring evidence. The model and nominal specification are now documented by R10/R11. The actions below remain open; none has been reported executed merely because it is listed here.

| Priority | Gap | Concrete next action | Acceptance evidence / stopping condition |
|---|---|---|---|
| P0 | Draw-to-asset and set-to-ball identity | Obtain a published or operator-supplied allocation register for #01372–#01376: machine serial/revision, case/set code dictionary, physical ball/batch identifiers and which set was loaded for trial/official draw. Ask specifically what VC2/VC4 identify and whether contents can be replaced without relabeling the case. | Signed/traceable record tied to draw/date and case/unit. An unsupported verbal match or color similarity does not pass. If disclosure refused, record exact scope/reason and then consider NOT_PUBLIC for that record only. |
| P0 | Actual per-number measurements | Locate/obtain the inspection sheets prescribed by R10: all 55 mass/dimension readings, dates, set/batch keys, instrument calibration certificates/uncertainties and replacements. | Raw readings linked to the actual numbered units and draw-use periods. Nominal values and pass/fail statements cannot substitute for numeric measurements. |
| P1 | Maintenance/replacement chronology | Obtain the witnessed quarterly maintenance records and independent-auditor checks prescribed on R10 pp7–10, service orders, commissioning/retirement records and case/individual-ball replacement logs. Include Berjaya/operator custodians where appropriate. | Actual dates, affected serial/set/unit, work performed and source provenance. The 2025 venue amendment and backup-count rule changes are not maintenance events. |
| P1 | Geometry and drive of confirmed MAGNUM II | Request/locate a serial/revision-appropriate dimensioned manual/CAD, chamber cross-section, arm/shaft geometry, collector drawings and measured encoder/controller logs. Resolve the 0.61 m surface reference and ambiguous 50 mm holding-chamber term. | Exact model/revision applicability, measured dimensions/uncertainties and rotation/control time series. Catalogs of generic Magnum/Halogen or 50 Hz supply do not pass. |
| P1 | Independent reading/provenance of case codes | Have a separate reviewer read randomized native frame pairs from the committed URL/PTS/hash ledger, without the new labels first; freeze their labels and adjudicate disagreement. Review #01372's clipped case inscription at other native frames if accessible. | Two independent transcriptions and a discrepancy log. Re-reading by the same auditor is not independent. Keep set IDs UNKNOWN without an allocation dictionary. |
| P2 | Official-source video continuity | Use the operator-embedded link ledger; retry the bounded failed Power link when accessible, authenticate channel ownership for old source IDs, and acquire uncut preparation/loading/control footage or original camera recordings. | Operator linkage, file SHA and uncut coverage before/after critical transitions. Current footer channel errors do not prove the old video sources false. Retention is at least 60 days by rule, not a guarantee older masters remain. |
| P2 | Contact/material/marking behavior | Once actual set specimens or certified test data are available, measure restitution over impact speeds, static/dynamic/rolling behavior on the real surfaces, sphericity, CoM, compliance, surface roughness and ink effects. | Calibrated experiment protocol, uncertainty and unit-level identity. Do not infer friction/restitution from the phrase solid foam plastic. |
| P2 | Public procurement gap | Search the official procurement portal by the confirmed model/vendor, operator and service dates; inspect actual tender/award attachments if publicly accessible. The audit only reached the public portal/index and did not complete an authenticated tender-attachment history. | Traceable original contract/specification/asset serial. Generic filming contracts or third-party tender summaries do not fill physical data. |
| P3 | Pre-close availability | Establish when machine/set assignment and any predictive physical measurements become available relative to actual ticket-close time. | Timestamped publication/decision record available before close. Post-close preparation footage cannot count. Only then design independent forecast evaluation. |

No message/request to Vietlott, Smartplay, Berjaya or another person has been sent by this audit. The user may obtain or authorize a specific records request. No consent is inferred for sending messages.

## Reproduce this audit

From `vietlott-power655-research/physical-audit/`:

```powershell
$py = 'C:/vietlott-digital-twin-env/Scripts/python.exe'
& $py scripts/build_audit_tables.py
& $py scripts/validate_audit.py
```

The inventory commands are read-only but a fresh run reflects the then-current refs/files, not the frozen as-of snapshot. Existing extraction scripts deliberately refuse to overwrite their native-frame output directories. To re-extract on another machine, first set a new local output directory in a copied script, preserve the input SHA checks and record any dependency/tool-version changes.

```powershell
& $py scripts/collect_inventory.py
& $py scripts/check_other_checkouts.py
& $py scripts/fetch_sources.py
& $py scripts/extract_official_metadata.py
& $py scripts/check_official_embeds.py
& $py scripts/inspect_identity_frames.py
& $py scripts/inspect_case_details.py
pdftoppm -r 120 -png C:/vietlott-research-output/physical-audit-20261022/documents/CURRENT_LINKED_POWER_RULE.pdf C:/vietlott-research-output/physical-audit-20261022/documents/power2022-page
& $py scripts/record_current_rule.py
```

The native source MP4s, PDF/HTML bytes and rendered pages remain local-only under `C:/vietlott-research-output/`; manifests and facts are committed. Fetch scripts do not bypass access controls. Manual visual transcription is a stated input to the table builder, not an automatic reader or an independent review. A different source digest must not be treated as the same evidence snapshot.
