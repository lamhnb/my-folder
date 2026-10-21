# Development failures retained

1. Initial deep pocket, dt=0.001: no captures and >2 mm contacts. `development_failure_escapement.json` records the result. A stacked next ball prevented the clear-plane closure rule. The revised 60 mm pocket and beveled upper gate physically lift the queued ball.
2. Initial isolated elastic collision: default contact positional stabilization caused 4–10% numerical kinetic-energy gain. `development_failure_energy.json` records it. Ideal isolated fixtures now explicitly set contactERP=0/contactSlop=0; driven full-system stabilization remains distinct and declared.
3. JSON output originally contained a NumPy integer for remaining count; a short-run serialization regression test now checks every report with strict JSON. Unsampled velocity is null, never NaN.
4. First ensemble, protocol v1: eight baseline runs completed; seven passed and seed1004 exceeded penetration limit at 0.004104 m (read exact JSON), pair upper gate25 and ball body62 at t23.2505, during fifth ISOLATE. The initial progress suspicion of special-stop insertion was **disproved by persisted contact/time evidence**; it was a queued ball against the upper bevel. The batch was stopped; eight in-flight next jobs were interrupted with unknown outcomes. Only completed runs are in `results/development_gate_v1/`; the unexecuted remainder of the old protocol is not counted as results.

The upper actuator now pauses when its prior contact penetration reaches 0.4 mm, allowing engine contacts to lift/clear a queued sphere before further motion. If contacts cannot resolve, the run remains jammed. Prescribed gate velocities now equal actual boundary displacement/dt, including transition and paused steps. This is an explicit idealized contact-feedback controller, **not a claimed Vietlott sensor/control law**. The exact thresholds are declared simulator assumptions; the global 2 mm physical gate has not been relaxed.

Seed1004 is a development regression seed, never an independent validation sample. The new complete ensemble is a fresh run of the same declared seed set with the repaired model; sensitivity conclusions must refer to final `results/runs/`, with old evidence separate. `regression_gate1004.json` and final system checks record repair outcomes. No failed history is deleted.

The pre-feedback gate source has now been recovered by inverse patch and verified byte-exact against SHA `d51283076d13a9e54735ce3960650d48dbf8c44c44832c42638572b33ce70d75` recorded in the original eight runs. This is a post-failure source recovery, not a claim that an earlier GitHub prototype existed. Archive: `results/development_gate_v1/replay/`, including the matching geometry, original config and `source_recovery.json`. Replay from `digital-twin/`:

```powershell
& $py results/development_gate_v1/replay/replay.py --seed 1004 --out results/development_gate_v1/replay_recheck1004.json
```

Compare physical events and penetration, not wall-clock runtime. Earlier exploratory flat-gate/packing prototypes in `results/development_prototypes/` retain their logs/configs/traces but do not have a verified exact source snapshot and are not presented as byte-replayable runs. The final engine and the eight pre-feedback runs have source hashes; keep these scopes separate.

The trajectory CSV exporter initially decompressed NPZ arrays in its inner loop; its process was stopped and rerun after caching arrays once. This affected export time, not physics. No original video/data or protected algorithm was modified.
