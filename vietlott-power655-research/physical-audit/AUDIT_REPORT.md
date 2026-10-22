# Power 6/55 physical data audit and recovery

Audit date: 2026-10-22 UTC. Repository: `lamhnb/my-folder`. Audit branch: `audit/power655-physical-data-recovery`, based on Digital Twin commit `01a56ea5f1f453960bf662ac64b0c129b1aa2006`. This is an audit and recovery deliverable; the existing simulator and prediction implementations were not rebuilt or edited.

## Findings that change the prior handoff

**A public, operator-issued specification was missed.** The official [drawing-process page](https://vietlott.vn/vi/trung-thuong/quay-so-mo-thuong/quy-trinh-qsmt) links a [16-page Power PDF](https://media.vietlott.vn//main.vi/08.2022/cms/power655.pdf). Its base rule is Decision **125/QD-VIETLOTT dated 03/03/2023**, followed by a 2025 venue amendment. The directory name `08.2022` is not its issue date. Article 8, PDF page 7, explicitly identifies **MAGNUM II, manufacturer SMART PLAY**, and supplies machine dimensions. This is documentary identification of the Power product configuration, independent of visual resemblance. It is not a serial-to-draw register. R10/R11; `extracted/current_rule_facts.csv`.

The source SHA256 is `9819e0a0d18696d98438e37b4c4ab5caf8b285b7e0edf6c8acfba7a712be4b8e`. Text extraction returned zero characters on every page; all 16 scanned pages were rendered with Poppler and visually inspected. Pages 12, 14 and 16 are blank scans. The appended amendment identifies the base date unambiguously and changes the venue effective **22/01/2025**; it is not evidence that a machine was replaced. R10; `current_rule_review.json`, `rule_page_manifest.csv`.

**Recoverable case markings were also missed.** New inspection of the five already cached, hash-matched July videos recovered preparation-case inscriptions `VC2`, `VC4`, `VC2`, `VC2` for #01373–#01376. The suffix for #01372 is partly outside the reviewed images and remains UNKNOWN. These are literal case markings, not certified persistent ball-set IDs. No dictionary, serial inventory or complete continuity record binds them to the same numbered physical balls across draws. F01372–F01376.

The four requested operational datasets remain incomplete. No per-draw machine serial, certified ball-set identity, dated maintenance/replacement event, or measured per-number property vector was recovered. Those gaps are **NOT_FOUND in the stated search scope**, not proven NOT_PUBLIC. The new public PDF makes a blanket claim that machine specifications are unavailable untenable.

## 1. Original project and search coverage

The original project is `vietlott-power655-physical-research/`. The implemented simulator is its `digital-twin/` subdirectory on [research/power655-physical-digital-twin](https://github.com/lamhnb/my-folder/tree/research/power655-physical-digital-twin), commit `01a56ea5f1f453960bf662ac64b0c129b1aa2006`. It is not on master. The new audit is intentionally under `vietlott-power655-research/physical-audit/`, a different directory.

`git fetch --all` recovered two more recent branches, B1 physical challenger A and B1 Adaptive Momentum 30. The former adds only a protocol; the latter contains a frequency backtest script/report. Neither supplies asset identities or ball metrology. G13/G14.

| Phase / branch | Frozen SHA | What was actually completed | What was not completed |
|---|---|---|---|
| Phase 1, `research/power655-physical-20261020` | `b2b1938cf38cc976a302cd8fd6a29bd4dd3c3df5` | Metadata and actual sampled pixels for eight URLs; seven show studio machinery across six associated dates, one is graphics-only. Historical 2017 rule extracted. Exploratory image-motion code, source/evidence/uncertainty logs and package. | No verified model then, serial/set register, actual per-ball measurements, physical RPM or identified 3D tracks. The 63.789/94.904 image candidates were explicitly rejected as physical RPM. G02/G03. |
| Phase 2, `research/power655-physical-phase2` | `dae213662171d1066876de0095b44b1f2cad12cd` | Five full public MP4 renditions hashed; 35 native downstream appearance proxies, 291 before/after aliases, 261 event/context rows, observability and failed-method audit; 30 reported software checks. | Actual selection/isolation times, physical RPM/angle, calibrated geometry/materials and set identity. Concluded NO-GO for a reliably calibrated dynamics model from these videos. Downloading full files did not mean viewing every frame. G04/G15. |
| Phase 3, `research/power655-draw-order-phase3` | `3356895595426eb7d57c8a83445aa06ca79e254a` | Five provisional seven-ball orders, 70 committed evidence frames, source integrity checks, 11 reported unit tests and an explicitly exploratory conditional-permutation pilot. | Zero two-review verified draws; official numeric reconciliation and independent review unfulfilled. The >=100-draw expansion was explicitly not attempted after the pilot gate failed. Primary H1–H4 remained not_testable. No equipment-dependence or prediction result. G05. |
| Phase 4, `research/power655-draw-order-phase4` | `f329cab62a64c081d635eac8033a7029f7b4d51a` | A 22-line execution plan for blind independent review, official reconciliation, chronological expansion and holdout. | No Phase 4 handoff, labels, expanded cohort or execution results found. Published Phase 4 execution is NOT_EXECUTED; an undisclosed cloud run would be NOT_AUDITABLE, not disproved. G06. |
| Digital Twin implementation | `01a56ea5f1f453960bf662ac64b0c129b1aa2006` | 55-body PyBullet research model, hypothetical collector, numerical/system checks, 78 runs/23 configurations, 3 separate posthoc torque diagnostics, trajectories, CAD/mesh, GIF and charts. | Verified actual collector, motor/geometry calibration, true per-ball properties, asset history and independently demonstrated forecasting advantage. G07–G12. |

The complete machine-readable inventory contains **17,071 rows**, 24 local/remote ref snapshots and **1,670 distinct committed path/blob pairs**, with 1,671 historical file-change rows. There were 18 remote branch heads and six local heads at collection time. One worktree of this repository was found. Thirteen discovered/likely local Git repositories were checked for the requested origin; only `C:/vietlott-research-repo` matched. See G01, `refs.csv`, `commit_file_history.csv`, `other_checkout_scan.json`.

Selected local output roots contained **3,161 untracked/ignored prior files**: chiefly 3,098 PNGs and 35 JPGs, eight MP4s (five complete pinned renditions plus partial/failed inputs), audio/captions, five HTMLs and three research ZIPs. This establishes useful local-only evidence, not an unpushed complete physical dataset. The three ZIPs passed CRC; their 362 member hashes were compared. Four members differ from current files: packaging code/manifests/attributes in older packages, not a hidden machine or ball register. All v3 members match current files. G16 and inventory.

Git 2.17 in this partial-clone checkout reported 138 commits as unreachable using `fsck --no-reflogs`. All 138 also appear in `rev-list --all`; the 15 lottery-related ones are already reachable history. This audit cross-checks that contradictory raw diagnostic and does not call those commits lost/unpushed work. No genuinely unreachable lottery commit was established. Raw output is preserved.

Scope limits: the scan covers fetched advertised refs, current local Git objects/reflogs, selected accessible output/user roots, app-visible relevant threads and this task's attachments. It does not cover deleted server branches, undisclosed repositories, other computers, unavailable Cowork containers or arbitrary cloud account exports. App-visible ChatGPT assistant messages in two related chats were returned as content-reference placeholders, so those bodies are NOT_AUDITABLE. No external Cowork artifact was attached to this task. No claim of complete global conversation coverage is made.

## 2. Audit of the four critical datasets

Requirement evidence is in `extracted/task_requirements.md` (T1–T3/TDT), including original visible task/attachment locations. The subjects were requested; the exact new eight-question/per-draw audit schema was not a mandatory table in every earlier task.

### A. Machine identification by draw — PARTIAL

1. **Requested?** Phase 1 explicitly requested manufacturer/model, changes and replacement history; Phase 3 requested verified equipment context; the Digital Twin master task explicitly requested model/serial and maintenance/replacement.
2. **Responsible phase?** Phase 1 technical identification, carried into Digital Twin Task A. Phase 3 equipment-dependence was conditional on available identities; Phase 4 did not perform the expansion.
3. **Executed?** Technical search and video geometry inspection occurred. A serial-to-draw recovery pipeline was not delivered. New R10 recovers the documented product model.
4. **Sources examined?** Archived 2017 Power rule, Smartplay Magnum/Halogen/deployment pages, sampled footage and later bounded technical/procurement queries. The current process-page-linked 2023/2025 PDF was absent from old source inventories and Git string history. G03, source_review.md, visible query summaries, R10/R11.
5. **Extracted data?** Previously: generic spherical/paddle/gravity mechanism and unknown model/serial. Now: explicit SMART PLAY/MAGNUM II, nominal dimensions/mass/power, one used plus at least one backup required; two similar circular units visible in a new reviewed frame. No serial is readable. R10/FMULTI.
6. **Stored where?** Old `equipment_research.md`, `unknown_parameters.md`, `digital-twin/parameter_registry.csv`; new rule facts/status/history/evidence tables here.
7. **Why missing?** Public source discovery was incomplete. Old handoffs transparently reported unknown model, but the public operator specification now recovered shows that this part could be improved. A model name still cannot fill a per-draw serial column.
8. **Recoverable without repetition?** Yes: original artifacts/MP4s reused; new official-link navigation recovered the missed source. Serial allocation remains NOT_FOUND, requiring further records or readable asset labels.

### B. Ball-set identification by draw — PARTIAL

1. **Requested?** Phase 1 sections 8–9 asked whether sets were disclosed/identifiable and how selected; Phase 3 Task B requested verified set context; Digital Twin Task A asked for set codes/replacement schedule.
2. **Responsible phase?** Initial equipment/video work and Digital Twin technical search; later cohort joins were conditional and uncompleted.
3. **Executed?** Phase 2 reviewed loading boundaries and explicitly recorded no identified selection event/set ID. It concentrated on later motion/collector intervals. No dedicated case-label transcription table existed.
4. **Sources examined?** Existing five cached MP4s, preparatory/ramp/rotor frames and source metadata, archived rules; current audit adds earlier preparation frames and the new operator rule. G04/G15, F01372–F01376, R10.
5. **Extracted data?** Previously only unknown IDs and appearance differences. Now four case inscriptions: #01373 VC2, #01374 VC4, #01375 VC2, #01376 VC2; #01372 UNKNOWN. Cases contain yellow/green-looking numbered balls in corresponding open-case frames. These observations do not certify set manufacturer, batch or persistent individual balls.
6. **Stored where?** `extracted/visual_review.csv`, native frame manifests and `MACHINE_BALLSET_HISTORY.csv`. Source pixels remain local, with URL/PTS/hash/replay script committed.
7. **Why missing?** The input files contained earlier case presentations that were outside the focused identity-unaware extraction. This is recoverable unextracted evidence in cached video, not evidence that a verified set table was lost after being created. Case-code semantics and chain of custody remain unsupported.
8. **Recoverable without repetition?** Yes for inscriptions; no redownload was needed. Persistent IDs require a case-code dictionary plus allocation/replacement/inspection records. Repetition of VC2 does not prove the same physical balls were reused.

### C. Replacement and maintenance history — NOT_FOUND for actual events; VERIFIED procedures

1. **Requested?** Explicit in Phase 1 technical search and Digital Twin Task A; equipment changes also part of Phase 3 conditional context.
2. **Responsible phase?** Phase 1 and Digital Twin technical research; no later dedicated operational-history acquisition was completed.
3. **Executed?** Rules and bounded searches were examined. No dated operator service-log extraction, supplier response or signed per-draw operational ledger is evidenced. Unlogged/private work is NOT_AUDITABLE, not assumed performed.
4. **Sources examined?** 2017 rule and vendor material previously; current audit adds the operator's 2023 rule/2025 amendment and procurement portal/index searches. R01/R02/R09/R10, SSEARCH.
5. **Extracted data?** Three-calendar-month maintenance requirement; witnessed log/auditor confirmation in the newer rule; inspection and nonconforming-ball-case replacement requirements. Venue change effective 22/01/2025 is documented. No actual maintenance date, changed unit serial or ball replacement date was obtained.
6. **Stored where?** Earlier equipment/unresolved notes; now rule facts/status table. `extracted/maintenance_events.csv` intentionally has a header and zero event rows.
7. **Why missing?** A procedure was available but does not supply historical execution records. The changed backup requirement (2017 two; 2023 at least one) is not evidence of retirement. Further public availability of the actual logs remains unknown; NOT_PUBLIC is not justified.
8. **Recoverable without repetition?** Requirements and record-custodian routes are recovered. Event chronology cannot be manufactured from those requirements; actual dated records still need acquisition.

### D. Physical specifications of individual numbered balls — PARTIAL nominals; NOT_FOUND measurements

1. **Requested?** Phase 1 requested diameters, nominal mass/tolerance, material and contact properties if available. Digital Twin explicitly requested per-ball differences, tolerances, contact properties and set linkage. Neither allowed invented measurements.
2. **Responsible phase?** Phase 1 technical investigation, then Digital Twin Task A; not the draw-order labels of Phase 3.
3. **Executed?** Nominal extraction occurred and was committed. No experiment weighing or measuring actual Vietlott numbered balls is evidenced. The simulator's randomized tolerances are synthetic scenarios.
4. **Sources examined?** Historical 2017 rule, vendor catalog/model pages and bounded searches; new 2023 operator specification and generic ball-validation-tool catalog. R01/R05/R06/R10.
5. **Extracted data?** 0.01234 kg ±0.000617 kg; 0.0505 m ±0.001 m; solid foam plastic; underlined numeral printed twelve times. These normative values are confirmed again by R10 page 8. Actual individual mass/diameter, sphericity, polymer, surface roughness, CoM, restitution and friction remain UNKNOWN.
6. **Stored where?** Old `equipment_research.md` and registry already contained size/mass. New `PHYSICAL_DATA_STATUS.csv`, `current_rule_facts.csv`, and `individual_ball_specs.csv` preserve distinct nominal/actual columns for labels 01–55.
7. **Why missing?** Nominal specs were delivered; actual per-number measurements and identifying batch/unit keys were never recovered in the auditable artifacts. No source gives the 55 actual readings or their measurement certificates. Vendor capabilities are not Vietlott measurements.
8. **Recoverable without repetition?** Nominals are fully recovered and versioned. Actual metrology requires the corresponding numbered physical units and traceable certificates/records. Video alone does not identify those quantities uniquely.

## 3. Newly recovered operator specification

| Quantity | Published value in SI | Location / scope |
|---|---:|---|
| Manufacturer / model | SMART PLAY / MAGNUM II | R10 p7, explicit Power operator specification |
| Overall height | 1.78 m | Published exterior nominal |
| Base length / width | 0.86 / 0.84 m | Base, not chamber depth |
| Mixing-chamber diameter | 0.61 m | No inner/outer reference or tolerance stated |
| Separate ball-holding-chamber diameter | 0.050 m | Literal published term; reference geometry ambiguous |
| Total machine mass | 159 kg | Not the rotor mass |
| Supply | 220–240 V, 50 Hz | Not motor RPM |
| Use / backup requirement | 1 / at least 1 | Actual per-draw allocation remains unknown |
| Balls and nominals | 55; 0.01234 ±0.000617 kg; 0.0505 ±0.001 m | R10 p8, standards rather than observations |
| Marking / material | 12 underlined numeral prints; solid foam plastic | Ink properties/polymer/actual manufacturer unspecified |

The 0.050 m holding-chamber term and 0.0505 m nominal ball diameter should be retained literally with ambiguity, not resolved by guessing a gate clearance. The 0.61 m mixing diameter supports a nominal geometry scenario; it does not independently measure the simulator's inner collision radius, depth, arm shape or collector dimensions. No dimensioned CAD/manual or serial-specific measurement was recovered.

The [Smartplay Magnum catalog](https://www.smartplay.com/lottery-products/lottery-draw-machines/magnum) is corroborative at vendor/operator level; it is not substituted for MAGNUM II documentation. Its capacity/ball-size marketing does not replace the operator's Power-specific values. Generic DBVS/RFID capabilities and claims about fairness were not adopted as facts about Vietlott. R02/R05/R06.

## 4. Evidence from real frames and provenance limits

The audit newly decoded **255 overview frames** (51 per source, native PTS approximately 600.032767–1100.532767 s) and **60 adaptive detail frames**. All five full-source SHA256 values matched the frozen Phase 2 ledger. All contact sheets were reviewed; case reading used full-resolution native frames and, where helpful, a lossless crop/180-degree display rotation. No AI enhancement or inferred OCR digits were used. One auditor performed the new reading; independent second review remains NOT_EXECUTED.

| Draw | Case-label frame PTS pair (s) | Reading | Open-case PTS (s) |
|---|---|---|---|
| 01372 | 689.021667 / 690.022667 | UNKNOWN, clipped suffix | 694.026667 |
| 01373 | 692.024667 / 693.025667 | VC2 | 697.029667 |
| 01374 | 689.021667 / 690.022667 | VC4 | 697.029667 |
| 01375 | 680.012667 / 681.013667 | VC2 | 683.015667 |
| 01376 | 640.006033 / 641.007033 | VC2 | 647.013033 |

A frame at #01374 PTS 860.292767 visibly contains two distinct circular mixer assemblies. This supports multiple units present in that scene, not a total fleet count, serial identity or both units being used for that Power draw. FMULTI. Similar bases, hubs, screw patterns and colors were not treated as asset IDs.

The pilot's existing ASR suggests selection of a storage compartment and then Power/Max cases around 628–714 s. This is navigation evidence only; no fresh direct audio listening was performed. An observed card 1 or 2 is not promoted to a ball-set ID. `extracted/visual_review.csv` is the observation authority for the case readings.

The official website's current footer links a channel different from the old source metadata IDs. A bounded check of that footer channel returned a termination message; the claim itself was not investigated. Fourteen YouTube embeds were recovered directly from the official video page. A check of its 29/09/2026 Power link timed out after 90 seconds; no pixels from it are claimed. Thus the five cached renditions remain public broadcast copies with associated dates, not authenticated camera masters or proven official channel ownership. R07/R12 and `official_embeds.json`.

The six-row history covers only the six traceable draw/date records in the prior physical research (#00027 and #01372–#01376). It is not a fabricated full-history calendar or a claim all other draws were searched frame by frame. Machine ID and certified ball-set ID remain UNKNOWN in every row; product-level model and observed case code are separate fields.

## 5. Root cause findings

| Candidate cause | Finding and specific evidence |
|---|---|
| Requirement omitted | The subjects were in the original tasks. The missing output is not explained by absence of a request. A dedicated per-draw asset/metrology acquisition table and closure check was not delivered; task focus narrowed to motion, labels and later implementation. T1–TDT, G04–G07. |
| Attempted but unsuccessful | Supported for video motion/identifiability, old exact-model searches and prior 403 responses. Those failures do not prove public documents absent. G02–G07. |
| Public data missed | **Confirmed for product model/dimensions:** R10/R11 is a current public operator link absent from previous inventories and all-history string searches. The PDF is scanned, which explains why text extraction alone would not reveal it, but does not establish the prior agent's internal reason for missing it. |
| Available input not extracted | **Confirmed for case-label evidence:** all five full files existed locally in Phase 2; new earlier-frame review reads four inscriptions. Old later-stage observability outputs did not contain a case-code table. G15/F01373–F01376. |
| Extracted but not committed | Local-only raw media and extra frames exist. No completed four-dataset table or actual ball metrology was found there. No evidence supports claiming a complete asset dataset was lost at push. Inventory/G16. |
| Committed elsewhere | The Digital Twin exists on its own branch, not master. Two newer B1 branches add no recovered hardware data. No other matching local checkout was found. G01/G13/G14. |
| Insufficient evidence | Applies to serial-to-draw joins, persistent set/individual-ball identity, actual maintenance/replacement dates and actual metrology. Case repetition and normative requirements cannot fill them. R10 and history/status tables. |
| Nonpublic records required | Operational records are the most direct remaining route. Their existence is prescribed by the operator rule, but their disclosure/access status is not established. Therefore no item is classified NOT_PUBLIC. R10 pp8–10. |
| Workflow/access failure | Primary-source discovery/versioning and preparation-frame coverage were incomplete. Phase 3's scientific gate and Phase 4's unexecuted plan blocked expansion. Cloud assistant bodies and private/unretained execution outputs are unavailable for audit; motives or hidden execution are not inferred. |

The supported root cause is a combination: **a real public-source discovery omission**, **recoverable but unextracted preparation footage**, and **remaining operational traceability/metrology gaps**. It is not justified to attribute all four missing datasets to secrecy, or to claim they were secretly completed and merely not pushed.

## 6. Impact on the existing simulator

The original registry has 99 entries: 55 assumed, 33 unknown, seven documented, two measured image/rendition observables and two derived estimates. This is its frozen pre-audit classification, not 99 measured machine parameters. R10 now upgrades the product-level manufacturer/model and supplies additional nominal geometry. It does not erase the unknown per-draw asset status. G08–G10; full dependency map in `SIMULATOR_PARAMETER_GAPS.md` and `extracted/parameter_dependency_map.csv`.

The ball mass/size nominals already match R10, so they are corroborated rather than newly calibrated. The baseline chamber radius is 0.32 m, while half the published 0.61 m mixing diameter is 0.305 m; the latter is a candidate nominal scenario pending surface/depth interpretation. Total machine mass 159 kg cannot replace the assumed 0.8 kg rotor. Supply 50 Hz cannot become RPM. The ambiguous 50 mm holding-chamber term cannot be entered as mouth diameter without checking its physical reference.

No simulator file/config/result is changed here. Future code can use a separately versioned nominal-geometry scenario. Case codes can enrich metadata, but cannot supply ball masses/friction. The current implementation has seeded uniform perturbations, not a measured per-number property-vector importer; adding such an importer would be separate implementation work after measurements exist.

Existing frozen run JSONs support the handoff's 78-run result: 66 pass their engineering gate, nine are incomplete/jammed, three fail penetration at 1 ms timestep; baseline 18/20 pass. The achieved baseline mean rotor speed was approximately 5.124 RPM against a 25 RPM command. Numerical/unit checks and hypothesis-model runs are useful, but do not validate real machine fidelity. The audit rechecks saved run integrity/counts; it does not rerun or recalibrate the simulator.

| Capability | Assessment after recovery |
|---|---|
| Run an approximate simulation | Yes; already implemented. Newly documented nominal dimensions can support future separately validated scenarios. |
| Calibrate actual dynamics to footage | Partly constrained by model and diameter; still underidentified without depth/CAD, motor trajectory, material tests, gate/command state and calibrated cameras. Downstream cadence alone cannot identify them. |
| Test persistent mechanical bias | Not yet attributable to actual hardware/balls. Need stable unit/set keys, maintenance epochs, per-ball measurements and independent cohorts. Synthetic model bias is not Vietlott bias. |
| Forecast before sales close | Not supported. The operator's procedural order locks ticket issuance before case selection (R10 p5). Observations during preparation cannot silently be used as pre-close inputs. Actual release/availability times and independent forecast testing are absent. |

## 7. Validation, reproducibility and limits

`scripts/validate_audit.py` checks CSV schemas, status vocabulary, evidence references, source/manifest hashes, six draw/date joins, all 55 unknown actual-ball records, the distinction between case codes/model and persistent IDs, 99-parameter coverage, nominal SI conversions, current-rule PDF page provenance, frozen run totals/source hashes, and protected-file preservation. Results are in `extracted/validation_report.json`. Passing these checks validates the audit package's consistency and recovered provenance; it does not certify actual ball measurements or predictions.

Reproduce from the audit directory using the existing research Python environment, or install `requirements.txt` into a new environment:

```powershell
$py = 'C:/vietlott-digital-twin-env/Scripts/python.exe'
& $py scripts/build_audit_tables.py
& $py scripts/validate_audit.py
```

To repeat source retrieval/extraction, see `RECOVERY_PLAN.md` and the source scripts. Frame extractors refuse overwrite and require the five exact MP4s from the old local-only source ledger. Source documents/pixels are local-only; no copyrighted source video, new frame pixel or PDF is committed. The rule can be fetched again by URL and checked against its SHA256. Frozen prior research bytes and B1/B1 Adaptive/B7/Champion refs are preserved; no master merge is performed.

The audit is complete only as a bounded evidence-backed audit and recovery package. The underlying asset history and metrology collection remains incomplete. The most important unresolved blocker is **a traceable operational register binding each draw to a machine unit, ball set and numbered physical balls, with dated inspection/replacement records**. Without that join, persistent physical effects cannot be assigned to the same equipment or balls, even after recovering the model specification.
