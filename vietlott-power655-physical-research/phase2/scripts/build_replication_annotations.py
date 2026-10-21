"""Materialize manually reviewed 01373/01374 annotations; no inferred hidden events.

The literal endpoint selections below are review data, not an automatic event
detector. Reproduction verifies files/hashes and writes new JSONs only.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ref(tag, t=None, index=None):
    rows = list(csv.DictReader((ROOT / "evidence" / tag / "frames.csv").open(encoding="utf-8")))
    row = rows[index] if index is not None else min(rows, key=lambda r: abs(float(r["source_pts_seconds"]) - t))
    if t is not None and abs(float(row["source_pts_seconds"]) - t) > 1e-6:
        raise ValueError((tag, t, row["source_pts_seconds"]))
    if digest(ROOT / row["file"]) != row["sha256"]:
        raise ValueError("Endpoint hash changed")
    return {"file": row["file"], "source_pts_seconds": float(row["source_pts_seconds"]),
            "sha256": row["sha256"], "bgr_sha256": row["bgr_sha256"],
            "sample_index": int(row["sample_index"]), "relative_native_index": int(row["relative_native_index"]),
            "native_crop_width": int(row["width"]), "native_crop_height": int(row["height"])}


def event(kind, before=None, after=None, status="NA_not_observable", note=""):
    lo = before["source_pts_seconds"] if before else None
    hi = after["source_pts_seconds"] if after else None
    return {"event_type": kind, "event_timestamp_seconds": None, "lower_pts_seconds": lo, "upper_pts_seconds": hi,
            "bracket_width_seconds": round(hi - lo, 6) if lo is not None and hi is not None else None,
            "before": before, "after": after, "status": status,
            "confidence_class": "qualitative_AI_visual_review_unvalidated", "note": note}


def main():
    configs = {
        "01373": {
            "id": "LUEP3hWibQw",
            "ramps": [(1126.358567, 1126.391933), (1138.437300, 1138.537400), (1152.084267, 1152.151000),
                      (1164.630133, 1164.730233), (1178.544033, 1178.677500), (1192.958433, 1193.058533), (1207.005800, 1207.105900)],
            "mechanism_indices": [None, (3, 4), (3, 4), (3, 4), (4, 5), (6, 7), (6, 7)],
            "collector_indices": [None, (4, 5), (3, 4), (5, 6), (4, 5), (7, 8), (7, 8)],
            "overlay": [(1130.095633, 1132.097633), (1142.107633, 1144.109633), (1156.121633, 1158.123633),
                        (1168.133633, 1170.135633), (1180.145633, 1182.147633), (1196.161633, 1198.163633), (1210.175633, 1212.177633)],
            "first_collector_index": 5, "first_mixing_state": 1092.057633,
            "rotor_reference": 1096.061633,
            "camera_difference": "Rotor close-up is substantially tighter than pilot: outer chamber is clipped by frame and hub diameter is much larger. Locked annulus would cover a different radial fraction. Native reference reviewed; no recenter/rescale or motion run.",
        },
        "01374": {
            "id": "Eid9PPhMn_0",
            "ramps": [(1108.140367, 1108.240467), (1120.819700, 1120.919800), (1133.365567, 1133.432300),
                      (1145.544400, 1145.644500), (1159.525033, 1159.625133), (1173.338833, 1173.438933), (1187.186000, 1187.286100)],
            "mechanism_indices": [None, None, (1, 2), (4, 5), (0, 1), None, None],
            "collector_indices": [None, None, (2, 3), (4, 5), (4, 5), (7, 8), (7, 8)],
            "overlay": [(1112.077633, 1114.079633), (1124.089633, 1126.091633), (1136.101633, 1138.103633),
                        (1148.113633, 1150.115633), (1162.127633, 1164.129633), (1176.141633, 1178.143633), (1190.155633, 1192.157633)],
            "first_collector_index": 5, "first_mixing_state": 1082.047633,
            "rotor_reference": 1088.053633,
            "camera_difference": "Native rotor image has hub around source x1045 rather than locked x932; chamber framing/radius and neighboring-machine visibility differ. This rough visual locator is not calibrated measurement. Balls are green, so the unchanged yellow exclusion also has unverified transfer validity. No recenter/rescale, color retuning or motion run.",
        },
    }
    for draw, cfg in configs.items():
        out = ROOT / "evidence" / f"replication_{draw}.json"
        if out.exists():
            raise ValueError(f"Refusing overwrite: {out}")
        source = json.loads((ROOT / "evidence" / f"source_{cfg['id']}_ranges.json").read_text(encoding="utf-8"))
        source_file = Path(source["video"]["file"])
        source_hash = digest(source_file)
        if source_hash != source["video"]["sha256"]:
            raise ValueError("Input differs from acquired source")
        overview = f"replication_{draw}_overview"
        captures = []
        for i in range(7):
            cap = i + 1
            six = f"replication_{draw}_cap{cap}_six"
            native = f"replication_{draw}_cap{cap}_native"
            events = [event("control_command_onset", note="Electrical command onset is not observed. Button-view samples, where present, do not bound actual contact/command; no electrical log or synchronized audio reviewed.")]
            pair = cfg["mechanism_indices"][i]
            if pair is not None:
                events.append(event("mechanism_first_visible_motion", ref(six, index=pair[0]), ref(six, index=pair[1]),
                                    "observed_image_state_transition", "First clearly visible collector/frame motion in reviewed samples; earlier subpixel/hidden motion not excluded. This is not rotor motion or electrical command timing."))
            elif cap == 1:
                events.append(event("mechanism_first_visible_motion", after=ref(six, index=cfg["first_collector_index"]),
                                    status="left_censored_by_camera_cut", note="Outlet is first shown with a ball already in the collector; mechanism onset occurred off-view or is unresolved."))
            else:
                events.append(event("mechanism_first_visible_motion", note="Collector onset hidden by view or already underway at selected native window start; do not substitute later release as first capture onset."))
            pair = cfg["collector_indices"][i]
            if pair is not None:
                events.append(event("ball_first_visible_in_upper_collector", ref(six, index=pair[0]), ref(six, index=pair[1]),
                                    "observed_image_state_transition", "First clearly visible ball patch in upper collector; an image visibility change, not entry across a calibrated surface. Occlusion/blur prevent claiming the earlier true entry time."))
            elif cap == 1:
                events.append(event("ball_first_visible_in_upper_collector", after=ref(six, index=cfg["first_collector_index"]),
                                    status="left_censored_already_visible", note="Ball already present at first usable outlet shot; do not manufacture a preceding empty collector from a control-panel camera shot."))
            else:
                events.append(event("ball_first_visible_in_upper_collector", note="Long ramp shot does not show upper collector sufficiently for a defensible first-visibility bracket."))
            events.append(event("permanent_ball_isolation", note="Internal one-way gate/selection plane and irreversibility are not visible. A visibly held ball is not proof of permanent isolation."))
            lo, hi = cfg["ramps"][i]
            events.append(event("leading_edge_exit_onto_downstream_ramp_proxy", ref(native, lo), ref(native, hi),
                                "observed_image_state_transition", "Leading ball silhouette becomes visibly extended beyond front housing/post edge toward downstream ramp. Native endpoints checked individually. Wider than one frame where blur makes a touching silhouette ambiguous. Screen-space proxy only; not final seated-ball time, 3D crossing, permanent isolation or electrical selection time."))
            lo, hi = cfg["overlay"][i]
            events.append(event("overlay_number_first_clearly_readable", ref(overview, lo), ref(overview, hi),
                                "observed_image_state_transition_coarse", "Graphic gains the corresponding result token between two overview samples, 60 native frame intervals apart. This is a separate broadcast graphic event; audio announcement not reviewed. Number values were not used to choose motion parameters."))
            captures.append({"capture_index": cap, "capture_type": "main" if cap <= 6 else "special", "events": events,
                             "physical_capture_selection_timestamp_seconds": None, "permanent_isolation_timestamp_seconds": None,
                             "empirical_physical_event_accuracy_frames": None})
        rotor = ref(f"replication_{draw}_rotor_native", cfg["rotor_reference"])
        windows = []
        for tag in [overview, f"replication_{draw}_rotor_native"] + [f"replication_{draw}_cap{n}_{s}" for n in range(1, 8) for s in ("six", "native")]:
            log = json.loads((ROOT / "evidence" / tag / "extraction.json").read_text(encoding="utf-8"))
            windows.append({"extraction_json": f"evidence/{tag}/extraction.json", "source_sha256": log["input_sha256"],
                            "arguments": log["arguments"], "count": log["count"], "first_pts": log["first_pts"], "last_pts": log["last_pts"]})
        result = {"schema_version": "1.0", "review_kind": "locked_definition_replication_same_AI_session",
                  "human_review": False, "blind_review": False, "reviewer_calibrated": False,
                  "statistically_independent_experimental_validation": False,
                  "source": {"id": cfg["id"], "draw_id_context": draw, "input_sha256": source_hash, "format_id": "137",
                             "source_dimensions": [1920, 1080], "source_frame_rate": "30000/1001", "camera_original_frame_rate": None,
                             "shutter_exposure_seconds": None, "physical_clock_accuracy_seconds": None},
                  "protocol_source": "evidence/native_refinement.json",
                  "protocol_source_sha256_at_replication": digest(ROOT / "evidence" / "native_refinement.json"),
                  "ramp_proxy_quality_target_seconds": .2002,
                  "timing_interpretation": ["Bounds describe reviewed encoded-image states, not empirical physical accuracy or confidence intervals.",
                    "No exact point event times, interpolation, hidden positions or physical RPM are supplied.",
                    "Seven attempts within one draw are not seven independent draw-level samples.",
                    "Native before/after crops were inspected individually for ramp proxies. Other visible-state onsets use native-crop contact sheets at every six encoded frames; graphic onsets use overview samples every sixty frames.",
                    "Control/collector/ramp/graphic are separate definitions. Camera cuts and missing upper-collector views do not become precise capture selection times."],
                  "mixer_start": event("official_mixing_start", after=ref(overview, cfg["first_mixing_state"]),
                      status="left_censored_first_mixing_state_after_cut", note="First clear close-up with balls visibly moving after control view. Actual mixer-start transition is not continuously visible; this is an upper bound/first observed mixing state, not an exact start timestamp."),
                  "captures": captures, "sampling_windows": windows,
                  "motion_transfer": {"status": "refused_camera_geometry_mismatch", "locked_roi": [480,80,900,900],
                                      "locked_center_source": [932,525], "locked_annulus": [130,350],
                                      "representative_native_evidence": rotor, "note": cfg["camera_difference"],
                                      "physical_angle_deg": None, "physical_rpm": None},
                  "changed_camera_details": "First transfer uses longer ramp view; subsequent outlet close-up and ramp cameras switch. For event inspection only, crops are source x1400,y80,w520,h720 for attempt1 and x800,y180,w1100,h700 for attempts2–7. These are logged native-pixel viewing crops, not retuned motion ROIs. Every six-frame search is followed by one-frame bounded review near the ramp proxy.",
                  "reviewed_contact_sheets": [str(p.relative_to(ROOT)).replace('\\','/') for p in sorted((ROOT / "evidence").glob(f"replication_{draw}_*/sheet_*.jpg"))],
                  "summary": {"capture_attempts": 7, "ramp_proxy_brackets": 7, "all_ramp_proxy_brackets_meet_target": True,
                              "physical_angles_available": False, "physical_rpm_available": False, "permanent_isolation_observed": False},
                  "builder_sha256": digest(__file__)}
        for capture in captures:
            ramp = capture["events"][4]
            assert ramp["bracket_width_seconds"] <= .200201
        with out.open("x", encoding="utf-8") as f:
            json.dump(result, f, indent=2, allow_nan=False)
        print(out)


if __name__ == "__main__":
    main()
