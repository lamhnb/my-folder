"""Descriptive diagnostics from existing image signals; never physical estimates."""
import argparse
import csv
import json
from pathlib import Path

import numpy as np


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    phase2 = Path(__file__).resolve().parents[1]
    out = args.out.resolve()
    if not out.is_relative_to(phase2) or out.exists():
        ap.error("New output path below Phase2 required")
    with (args.run / "candidate_image_motion.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    fields = ["flow_projected_increment_deg", "flow_increment_iqr_deg", "candidate_projected_shift_deg",
              "peak_correlation", "comparable_peak_count", "yellow_exclusion_fraction",
              "moving_mask_changed_fraction", "polar_min_coverage", "frame_mean_abs_difference_0_255"]
    summaries = {}
    for field in fields:
        values = np.array([float(r[field]) for r in rows if r.get(field) not in (None, "NA", "")])
        summaries[field] = {"n": len(values), "min": float(values.min()), "median": float(np.median(values)),
                            "max": float(values.max()), "quartiles": np.percentile(values, [25, 75]).tolist()}
    near = [{"clip_frame_index": int(r["clip_frame_index"]), "source_pts_seconds": float(r["source_pts_seconds"]),
             "mean_abs_gray_difference": float(r["frame_mean_abs_difference_0_255"])}
            for r in rows if r.get("frame_mean_abs_difference_0_255") not in (None, "NA", "")
            and float(r["frame_mean_abs_difference_0_255"]) < 1]
    result = {"status": "descriptive_image_quality_only", "fields": summaries,
              "masked_harmonic_missing_clip_indices": [int(r["clip_frame_index"]) for r in rows if r["yellow_masked_harmonic_real"] == "NA"],
              "template_multiple_peak_pairs": sum(int(r.get("comparable_peak_count", "0")) > 1 for r in rows if r.get("comparable_peak_count") not in (None, "NA", "")),
              "adjacent_pairs": len(rows) - 1, "near_duplicate_candidate_pairs_count": len(near),
              "near_duplicate_screening_threshold_mean_abs_gray_0_255": 1,
              "near_duplicate_candidate_pairs": near,
              "near_duplicate_screening_note": "Exploratory post-output quality screen, not validated duplicate detection. Low crop change suggests held/repeated pictures; camera FPS and upstream processing remain unknown. No frames removed or interpolated.",
              "physical_angle_deg": None, "physical_rpm": None}
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2, allow_nan=False)
    print(out)


if __name__ == "__main__":
    main()
