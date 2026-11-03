# Champion-X — Market/Physical Draw Phase 1 Pilot (2026-11-03)

## Executive conclusion
**NO VERIFIED PHYSICAL SIGNAL YET.** We identified historically documented mechanical variables but did not acquire verified, frame-by-frame physical order or machine/ball-case identifiers for any actual draw. Historic public draw tables only yield unordered six-main sets and the seventh special number; they do not identify machine mechanisms.

A preliminary statistical **uniform-without-replacement null** on 1,418 valid historical records shows no striking global deviation. **Independent JS simulation with 500 fixed-seed replications** (not a Python Frozen clean-checkout) found approximate Monte Carlo upper-tail p-values 0.425 for six-main global Pearson statistic and 0.200 for special-number global Pearson statistic; max-per-number familywise p-values 0.603 and 0.471; consecutive-draw six-main overlap two-sided p≈0.806. Small simulation B means modest Monte Carlo precision; statistics are exploratory historical controls, not proof the physical apparatus is perfectly fair.

## Historical physical process (not verified current hardware)
2017 archived official Power 6/55 drawing regulation:
https://media.vietlott.vn/vi/04.2019/system/archivedate/the-le-mega--655.pdf
- mechanical automatic chamber with three rotating paddles; balls 01–55 inserted into holding slots by numeric identity, mix then gravitational ball discharge;
- independently selected ball case/valise and operator observed under oversight;
- seven balls successively drawn, first six for Jackpot 1 and seventh from remaining 49 for Jackpot 2;
- historical regulation ball reference 12.34 g with ±0.617 g tolerance, 50.5 mm diameter with ±1.0 mm tolerance. These are **allowed tolerances**, not observed ball measurements and cannot be assumed to yield any bias;
- historical three-month machine maintenance and checking/certification steps.
**Important:** These are 2017 rules, not independently verified active 2026 machine/case IDs, tolerances or settings.

Vietlott says broadcast live SCTV2/official webpage/YouTube and only short Facebook excerpt, per https://tuoitre.vn/nld/vi-sao-vietlott-khong-livestream-toan-bo-cac-phien-quay-so-mo-thuong-tren-mang-xa-hoi-196250714145608742.htm . Exact archives and permissions remain to be obtained.

## Video discovery gate
Separate source register `CHAMPION_X_PHYSICAL_VIDEO_EVIDENCE_REGISTER_2026-11-03.md` with 3 third-party YouTube candidate URLs, notably #01397 and #01396. No frame-level review performed and the descriptions of two videos explicitly focus on the published results. Thus **0 videos verified as complete actual physical draw footage** and **0 verified physical extraction sequences**. Do not claim pilot sample of 50–100 is acquired.

## Data quality gate
Public historical source `https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power655.jsonl` currently 1419 records, one raw invalid record #00944 (date 2022-09-23) has only six numbers and **no seventh special** and is known out-of-order source anomaly. Quarantine #00944 instead of imputing a seventh ball. Sort valid rows by numeric ID, use **1418** valid seven-number entries. In serial-overlap test only compare **1416** genuinely consecutive draw IDs. Do not treat a gap as consecutive.
No current draw is inferred to have physical 1st/2nd/3rd extraction order from sorted numbers.

## Observed null statistics
- N=1418 valid; expected count for each number as a main winner = `N*6/55 = 154.6909`.
- Observed main winner counts: #22=181, #41=178 (most frequent), but corrected familywise max-z ~2.444 and empirical p≈0.603. No individual outlier is compelling once max over 55 labels is calibrated.
- Expected special per number `N/55 = 25.7818`; observed special #50=38, max-z≈2.541 with Monte Carlo max-adjusted p≈0.471.
- Pearson statistic main six frequencies ~50.88693; special frequencies ~62.42313.
- Simulated (B=500, fixed PRNG seed 20261103) upper-tail p-values main ~0.425, special ~0.200; Monte Carlo max-z familywise p main ~0.603, special ~0.471.
- Mean number of repeated mains between valid consecutive draws = **0.65960** across 1416 ID-adjacent pairs; exact independent uniform expectation `36/55≈0.65455`; Monte Carlo two-sided p≈0.806.
- Independent JS diagnostic used for these numbers. Separate Python source `champion_x_physical_draw_pilot_20261103.py` and workflow `.github/workflows/champion-x-physical-draw-pilot.yml` have been committed, but any CI run status must be verified before calling it PASS. The initial CI failed strictly because of the quarantined source defect; revised script explicitly excludes the malformed #00944 and omits gap-spanning serial pairs.

## What would count as physical evidence
1. A source video clearly shows an **uninterrupted** actual mechanical draw, matching published draw ID and main six + special.
2. Two independent annotations agree on all seven chronological emitted ball labels and associated frame times. Record trial vs official draws and missing frames.
3. Know physical ball-case and machine IDs from on-screen documentation or legitimate published log; **unknown is not a proxy for a unique device**.
4. Group by actual device/case and test inclusion bias as well as order bias under conditional sampling-without-replacement, using familywise correction or pre-registered effect and future untouched validation.
5. If inclusion advantage is not reproducible, **do not promote** the phenomenon to X0 or new Jackpot ticket generation; a position-only bias may wash out completely over the six-main set.
6. Ball case-specific measured mass, diameter and maintenance date require actual measurement/record metadata, not nominal tolerances.

## Next decision
Phase 1 video feasibility **BLOCKED BY EVIDENCE**, not by modeling. Seek authentic uncut Vietlott / SCTV2 archives, official machine/ball-case identifiers and records. Avoid claiming physical predictions from outcome-only main/special counts. Original R19 Frozen, Hybrid6 and registered Champions remain immutable.
