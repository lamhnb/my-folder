"""Plot existing candidate image diagnostics; never physical angle/RPM evidence."""
import argparse
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def read(path):
    with Path(path).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def values(rows, name):
    return np.array([float(r[name]) if r.get(name) not in (None, "", "NA") else np.nan for r in rows])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    phase2 = Path(__file__).resolve().parents[1]
    out = args.out.resolve()
    if not out.is_relative_to(phase2) or out.exists():
        ap.error("New output path inside Phase2 required; overwrite refused")
    rows = read(args.run / "candidate_image_motion.csv")
    spectra = read(args.run / "pattern_spectrum.csv")
    info = json.loads((args.run / "diagnostics.json").read_text())
    pts = values(rows, "source_pts_seconds")
    relative = pts - pts[0]
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), layout="constrained")
    flow = values(rows, "flow_projected_increment_deg")
    template = values(rows, "candidate_projected_shift_deg")
    axes[0, 0].plot(relative, flow, lw=1)
    axes[0, 0].set(title="Tangential optical flow (image projection)", ylabel="Median projected increment (deg/frame)")
    axes[0, 1].plot(relative, template, lw=1)
    axes[0, 1].set(title="Angular template peak (identity ambiguous)", ylabel="Candidate cyclic shift (deg/frame)")
    for name, color in (("yellow_masked", "tab:blue"), ("unmasked_control", "tab:orange")):
        axes[0, 2].plot(relative, values(rows, name + "_harmonic_real"), label=name, color=color, lw=1)
    axes[0, 2].set(title=f"Real image harmonic h={info['arguments']['harmonic']}", ylabel="Image coefficient (gray-level units)")
    axes[0, 2].legend(fontsize=8)
    for name, color in (("yellow_masked", "tab:blue"), ("unmasked_control", "tab:orange"), ("moving_yellow_mask_control", "tab:green")):
        subset = [r for r in spectra if r["signal"] == name]
        if not subset:
            continue
        powers = values(subset, "power")
        axes[1, 0].plot(values(subset, "frequency_hz"), powers / max(float(powers.max()), 1e-30), label=name, color=color, lw=1)
    axes[1, 0].set(title="Image-pattern spectra, each scaled to own maximum", xlabel="Pattern frequency (Hz; not rotor frequency)", ylabel="Relative spectral power")
    axes[1, 0].legend(fontsize=8)
    axes[1, 1].plot(relative, values(rows, "yellow_exclusion_fraction"), label="Excluded yellow fraction")
    axes[1, 1].plot(relative, values(rows, "moving_mask_changed_fraction"), label="Mask change fraction")
    axes[1, 1].set(title="Moving-mask nuisance controls", ylabel="Fraction of native crop pixels")
    axes[1, 1].legend(fontsize=8)
    axes[1, 2].plot(relative, values(rows, "frame_mean_abs_difference_0_255"), lw=1)
    axes[1, 2].set(title="Frame difference (not automatic cut detection)", ylabel="Mean absolute gray difference (0–255)")
    for i, ax in enumerate(axes.flat):
        ax.grid(alpha=.25)
        if i != 3:
            ax.set_xlabel(f"Seconds since source PTS {pts[0]:.6f}")
    fig.suptitle("Exploratory image motion only — physical angle and RPM remain NA\n"
                 "Blur, transparent blades, moving balls, perspective and threefold ambiguity are unresolved", fontsize=13)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(out)


if __name__ == "__main__":
    main()
