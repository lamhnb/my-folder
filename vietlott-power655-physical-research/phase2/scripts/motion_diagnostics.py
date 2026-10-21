"""Bounded, exploratory IMAGE motion only; never physical paddle identity/RPM.

Native source pixels and source PTS; polar spatial sampling is bilinear, never
temporal interpolation. No numbers/results from the lottery enter this tool.
Run --help for the manually reviewed input contract. Synthetic tests are software
checks, not validation on the machine. Phase 1 files are never written.
"""
import argparse
import csv
import hashlib
import json
import math
import platform
import re
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np
import scipy
from scipy.signal import find_peaks, periodogram

PHASE2 = Path(__file__).resolve().parents[1]
WARNINGS = [
    "Image signals do not identify a paddle, common shaft, physical angle, direction or RPM.",
    "Threefold image symmetry creates 120-degree ambiguity; harmonic order is a hypothesis.",
    "Sampling cannot exclude alias branches without an independent speed bound and marker identity.",
    "Perspective, refraction, blur, unknown shutter and occlusion are uncalibrated systematics.",
    "Yellow HSV masks are heuristic: moving masks can themselves create periodic signals.",
    "A stable-camera review is required. Cut scores are diagnostics, not automatic cut certification.",
    "Agreement between methods on the same pixels is not independent physical validation.",
]


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(command, timeout=180):
    return subprocess.run(command, capture_output=True, check=True, timeout=timeout)


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False), encoding="utf-8")


def write_csv(path, rows, fields):
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: "NA" if row.get(k) is None else row[k] for k in fields})


def yellow_mask(im):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([18, 75, 65]), np.array([42, 255, 255]))
    # Boundary exclusion reduces, but does not remove, ball-induced flow leakage.
    return cv2.dilate(mask, np.ones((5, 5), np.uint8)) > 0


def polar_profile(gray, excluded, center, annulus, bins=360, radial_samples=96):
    r = np.linspace(*annulus, radial_samples)
    phi = np.arange(bins) * 2 * np.pi / bins
    mx = (center[0] + r[:, None] * np.cos(phi)).astype(np.float32)
    my = (center[1] - r[:, None] * np.sin(phi)).astype(np.float32)
    values = cv2.remap(gray.astype(np.float32), mx, my, cv2.INTER_LINEAR)
    valid = cv2.remap((~excluded).astype(np.float32), mx, my, cv2.INTER_NEAREST)
    count = valid.sum(axis=0)
    profile = np.divide((values * valid).sum(axis=0), count,
                        out=np.full(bins, np.nan), where=count > 0)
    return profile, count / radial_samples


def angular_match(previous, current):
    """All cyclic shifts, pairwise finite bins; retain multiple comparable peaks."""
    scores = []
    for shift in range(len(previous)):
        shifted = np.roll(previous, shift)
        ok = np.isfinite(shifted) & np.isfinite(current)
        if ok.sum() < len(previous) * .7:
            scores.append(np.nan)
            continue
        a, b = shifted[ok], current[ok]
        a, b = a - a.mean(), b - b.mean()
        denom = np.linalg.norm(a) * np.linalg.norm(b)
        scores.append(float(a @ b / denom) if denom > 1e-10 else np.nan)
    scores = np.asarray(scores)
    if not np.isfinite(scores).any():
        return {"candidate_projected_shift_deg": None, "peak_correlation": None,
                "comparable_peak_count": 0, "ambiguity": "insufficient_texture_or_mask_coverage"}
    # Triple tiling permits peak detection across the circular boundary.
    clean = np.nan_to_num(scores, nan=-2.)
    peaks, _ = find_peaks(np.tile(clean, 3), distance=max(1, len(clean) // 36))
    peaks = peaks[(peaks >= len(clean)) & (peaks < 2 * len(clean))] - len(clean)
    best = int(np.nanargmax(scores))
    comparable = [int(x) for x in peaks if scores[x] >= scores[best] - .02]
    if best not in comparable:
        comparable.append(best)
    signed = (best + len(clean) // 2) % len(clean) - len(clean) // 2
    return {"candidate_projected_shift_deg": float(signed * 360 / len(clean)),
            "peak_correlation": float(scores[best]), "comparable_peak_count": len(comparable),
            "ambiguity": "multiple_comparable_shifts" if len(comparable) > 1 else "single_image_peak_not_physical_identity"}


def projected_flow(previous, current, excluded, center, annulus):
    flow = cv2.calcOpticalFlowFarneback(previous, current, None, .5, 3, 15, 3, 5, 1.2, 0)
    yy, xx = np.indices(previous.shape)
    dx, dy = xx - center[0], yy - center[1]
    radius2 = dx * dx + dy * dy
    valid = (~excluded) & (radius2 >= annulus[0] ** 2) & (radius2 <= annulus[1] ** 2)
    # Image y points down; positive increment means counterclockwise on the image.
    increments = np.rad2deg((dy * flow[:, :, 0] - dx * flow[:, :, 1]) /
                           np.maximum(radius2, 1))[valid]
    if len(increments) < 100:
        return {"flow_projected_increment_deg": None, "flow_increment_iqr_deg": None,
                "flow_valid_pixels": int(len(increments))}
    q = np.percentile(increments, [25, 50, 75])
    return {"flow_projected_increment_deg": float(q[1]), "flow_increment_iqr_deg": float(q[2] - q[0]),
            "flow_valid_pixels": int(len(increments))}


def temporal_diagnostics(times, signal):
    """No resampling: reject irregular PTS for conventional FFT/lag autocorrelation."""
    times, signal = np.asarray(times), np.asarray(signal)
    dt = np.diff(times)
    median = float(np.median(dt))
    jitter = float(np.max(np.abs(dt - median)))
    if len(times) < 16 or median <= 0 or jitter > median * .01 or not np.isfinite(signal).all():
        return {"status": "not_computed_irregular_pts_short_or_missing", "max_dt_deviation_seconds": jitter}, [], []
    centered = signal - signal.mean()
    energy = float(centered @ centered)
    if energy < 1e-10:
        return {"status": "not_computed_flat_signal"}, [], []
    corr = np.correlate(centered, centered, mode="full")[len(signal) - 1:] / energy
    peaks, _ = find_peaks(corr[1:len(corr) // 2])
    peaks = peaks + 1
    positive = [int(i) for i in peaks if corr[i] > 0]
    strongest = max(positive, key=lambda x: corr[x]) if positive else None
    frequencies, powers = periodogram(signal, fs=1 / median, window="hann", detrend="linear")
    best = 1 + int(np.argmax(powers[1:]))
    summary = {"status": "exploratory_pattern_only", "sampling_hz_from_pts": 1 / median,
               "max_dt_deviation_seconds": jitter,
               "candidate_pattern_frequency_hz": float(frequencies[best]),
               "bin_width_hz": float(frequencies[1] - frequencies[0]),
               "autocorrelation_peak_lag_seconds": strongest * median if strongest else None,
               "nyquist_hz": .5 / median, "alias_resolved": False,
               "warning": "Lag and spectrum can select different harmonics; no automatic RPM conversion or CI."}
    ac = [{"lag_frames": i, "lag_seconds": i * median, "normalized_autocorrelation": float(v)} for i, v in enumerate(corr)]
    spec = [{"frequency_hz": float(f), "power": float(p)} for f, p in zip(frequencies, powers)]
    return summary, ac, spec


def decode(source, start, end, roi, max_frames, max_bytes):
    x, y, w, h = roi
    # ffprobe independently pins local demuxed source PTS; no frame/FPS arithmetic.
    probe_cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-read_intervals", f"{start}%{end}",
                 "-show_frames", "-show_entries", "frame=best_effort_timestamp_time", "-of", "json", str(source)]
    probed = json.loads(run(probe_cmd).stdout)["frames"]
    expected = [float(f["best_effort_timestamp_time"]) for f in probed
                if "best_effort_timestamp_time" in f and start <= float(f["best_effort_timestamp_time"]) < end]
    if not expected or len(expected) > max_frames or len(expected) * w * h * 3 > max_bytes:
        raise ValueError("No PTS, too many frames, or RAM bound exceeded; choose a shorter reviewed interval")
    stream_info = json.loads(run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                 "stream=start_time", "-of", "json", str(source)]).stdout)
    origin = float(stream_info["streams"][0].get("start_time", 0))
    # Input -ss is relative to file start. Preserve absolute source PTS with copyts.
    command = ["ffmpeg", "-hide_banner", "-loglevel", "info", "-ss", str(max(0, start - origin - 2)),
               "-copyts", "-noautorotate", "-i", str(source), "-an", "-vf",
               f"trim=start={start}:end={end},showinfo,crop={w}:{h}:{x}:{y}:exact=1",
               "-frames:v", str(max_frames + 1), "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "bgr24", "pipe:1"]
    result = run(command)
    stderr = result.stderr.decode(errors="replace")
    pts = [float(v) for v in re.findall(r"\bn:\s*\d+\s+pts:\s*-?\d+\s+pts_time:([0-9.e+\-]+)", stderr)]
    n = len(result.stdout) // (w * h * 3)
    if len(result.stdout) != n * w * h * 3 or n != len(pts) or n != len(expected) or n > max_frames:
        raise ValueError(f"Incomplete decode or bound exceeded: pixels={n}, showinfo={len(pts)}, ffprobe={len(expected)}")
    if np.any(np.diff(pts) <= 0) or not np.allclose(pts, expected, atol=5e-5, rtol=0):
        raise ValueError("ffprobe/ffmpeg PTS mismatch, duplicate/reordered PTS, or missing frames")
    # Higher precision ffprobe timestamps retained; showinfo six-digit values are cross-checks.
    return np.asarray(expected), np.frombuffer(result.stdout, np.uint8).reshape(n, h, w, 3), command, probe_cmd, stderr


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", type=Path)
    ap.add_argument("--start", type=float, required=True, help="source PTS inclusive")
    ap.add_argument("--end", type=float, required=True, help="source PTS exclusive; max 30 seconds")
    ap.add_argument("--roi", type=int, nargs=4, required=True, metavar=("X", "Y", "W", "H"))
    ap.add_argument("--center-source", type=float, nargs=2, required=True, help="native SOURCE pixel coordinates")
    ap.add_argument("--annulus", type=float, nargs=2, required=True, metavar=("R_MIN", "R_MAX"))
    ap.add_argument("--harmonic", type=int, default=3, help="image harmonic hypothesis; no physical rotor assumption")
    ap.add_argument("--review", type=Path, required=True, help="JSON: stable_camera_reviewed=true, start_pts/end_pts, source_sha256, evidence_refs[], marker_status, marker_notes")
    ap.add_argument("--out", type=Path, required=True, help="new directory inside Phase2; overwrite refused")
    ap.add_argument("--max-frames", type=int, default=300)
    args = ap.parse_args()
    if not (0 <= args.start < args.end <= args.start + 30) or not (16 <= args.max_frames <= 900):
        ap.error("Require finite positive interval <=30 seconds and 16..900 frame cap")
    if not 1 <= args.harmonic <= 12:
        ap.error("Harmonic must be 1..12")
    out = args.out.resolve()
    if not out.is_relative_to(PHASE2) or out == PHASE2 or out.exists():
        ap.error("Output must be a new directory below Phase2; overwrite refused")
    source = args.source.resolve(strict=True)
    source_hash = sha256(source)
    review = json.loads(args.review.read_text(encoding="utf-8-sig"))
    if review.get("stable_camera_reviewed") is not True or review.get("source_sha256") != source_hash or \
       review.get("start_pts") != args.start or review.get("end_pts") != args.end or \
       not review.get("evidence_refs") or review.get("marker_status") not in ("confirmed_unique", "not_observable", "uncertain") or \
       not review.get("marker_notes"):
        ap.error("Manual review must bind exact hash, interval, stability and marker feasibility evidence")
    info = json.loads(run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(source)]).stdout)
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    x, y, w, h = args.roi
    cx, cy = args.center_source[0] - x, args.center_source[1] - y
    r0, r1 = args.annulus
    if min(x, y) < 0 or min(w, h) < 32 or w * h > 1_000_000 or x + w > video["width"] or y + h > video["height"]:
        ap.error("ROI must be bounded within native source pixels (max 1M pixels)")
    if not (0 < r0 < r1 and r1 <= min(cx, cy, w - 1 - cx, h - 1 - cy)):
        ap.error("Annulus must fit entirely inside ROI around reviewed source-pixel center")
    out.mkdir(parents=True, exist_ok=False)
    dump(out / "input_provenance.json", {"source_sha256": source_hash, "review": review,
         "arguments": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
         "script_sha256": sha256(__file__), "status": "started_not_yet_verified"})
    try:
        pts, images, command, probe_cmd, stderr = decode(source, args.start, args.end, args.roi, args.max_frames, 512 * 1024 ** 2)
        if len(images) < 16:
            raise ValueError("At least 16 native frames required")
    except Exception as exc:
        detail = {"status": "failed_no_measurement", "exception": type(exc).__name__, "message": str(exc)}
        if isinstance(exc, subprocess.CalledProcessError):
            detail["stderr_tail"] = exc.stderr.decode(errors="replace")[-10000:]
        dump(out / "failure.json", detail)
        raise
    (out / "decode.log").write_text(stderr, encoding="utf-8")
    center = (cx, cy)
    profiles, unmasked_profiles, rows = [], [], []
    previous = previous_mask = previous_profile = None
    for i, image in enumerate(images):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mask = yellow_mask(image)
        profile, coverage = polar_profile(gray, mask, center, args.annulus)
        raw_profile, _ = polar_profile(gray, np.zeros_like(mask), center, args.annulus)
        profiles.append(profile)
        unmasked_profiles.append(raw_profile)
        row = {"clip_frame_index": i, "source_frame_index": None, "source_pts_seconds": float(pts[i]),
               "native_crop_bgr_sha256": hashlib.sha256(image.tobytes()).hexdigest(),
               "yellow_exclusion_fraction": float(mask.mean()), "polar_min_coverage": float(coverage.min()),
               "physical_angle_deg": None, "physical_rpm": None}
        if previous is not None:
            row.update(projected_flow(previous, gray, previous_mask | mask, center, args.annulus))
            row.update(angular_match(previous_profile, profile))
            row["frame_mean_abs_difference_0_255"] = float(np.abs(gray.astype(float) - previous).mean())
            row["moving_mask_changed_fraction"] = float((mask != previous_mask).mean())
        rows.append(row)
        previous, previous_mask, previous_profile = gray, mask, profile
    phi = np.arange(360) * 2 * np.pi / 360
    analyses, ac_rows, spectrum_rows = {}, [], []
    for label, sequence in (("yellow_masked", profiles), ("unmasked_control", unmasked_profiles)):
        values = np.asarray(sequence)
        # Strictly missing coefficients when any angular bin is unavailable.
        coefficients = (values - np.nanmedian(values, axis=0)) @ np.exp(1j * args.harmonic * phi) / 360
        summary, ac, spec = temporal_diagnostics(pts, coefficients.real)
        analyses[label] = summary
        for i, coefficient in enumerate(coefficients):
            rows[i][label + "_harmonic_real"] = float(coefficient.real) if np.isfinite(coefficient.real) else None
            rows[i][label + "_harmonic_imag"] = float(coefficient.imag) if np.isfinite(coefficient.imag) else None
        ac_rows += [dict(signal=label, **r) for r in ac]
        spectrum_rows += [dict(signal=label, **r) for r in spec]
    mask_summary, mask_ac, mask_spec = temporal_diagnostics(pts, [r["yellow_exclusion_fraction"] for r in rows])
    analyses["moving_yellow_mask_control"] = mask_summary
    ac_rows += [dict(signal="moving_yellow_mask_control", **r) for r in mask_ac]
    spectrum_rows += [dict(signal="moving_yellow_mask_control", **r) for r in mask_spec]
    fields = list(dict.fromkeys(key for row in rows for key in row))
    write_csv(out / "candidate_image_motion.csv", rows, fields)
    write_csv(out / "pattern_autocorrelation.csv", ac_rows, ["signal", "lag_frames", "lag_seconds", "normalized_autocorrelation"])
    write_csv(out / "pattern_spectrum.csv", spectrum_rows, ["signal", "frequency_hz", "power"])
    commit = run(["git", "-C", str(PHASE2.parents[1]), "rev-parse", "HEAD"]).stdout.decode().strip()
    dump(out / "diagnostics.json", {"status": "exploratory_image_motion_not_physical_measurement", "source_file": str(source),
         "source_sha256": source_hash, "source_stream": video, "source_format": info.get("format"),
         "manual_review": review, "arguments": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()},
         "source_pts_first": float(pts[0]), "source_pts_last": float(pts[-1]), "native_frame_count": len(pts),
         "source_frame_index": None, "source_pts_origin_note": "Local packet-copy source timestamps; upstream source mapping requires acquisition provenance.",
         "marker_feasibility": review["marker_status"], "physical_angle_deg": None, "physical_rpm": None,
         "calibration_status": "not_implemented_or_verified", "analyses": analyses, "warnings": WARNINGS,
         "commands": {"decode": command, "probe_frames": probe_cmd}, "code_commit": commit,
         "script_sha256": sha256(__file__), "phase1_requirements_lock_sha256": sha256(PHASE2.parent / "requirements-lock.txt"),
         "environment": {"python": sys.version, "platform": platform.platform(), "opencv": cv2.__version__,
                         "numpy": np.__version__, "scipy": scipy.__version__,
                         "ffmpeg": run(["ffmpeg", "-version"]).stdout.decode().splitlines()[0],
                         "ffprobe": run(["ffprobe", "-version"]).stdout.decode().splitlines()[0]},
         "spatial_sampling": "native crop; bilinear polar remap only; no new temporal frames", "frames_saved": False,
         "confidence_intervals": None, "synthetic_is_real_evidence": False})
    print(json.dumps({"out": str(out), "status": "image_diagnostics_only", "frames": len(pts)}))


if __name__ == "__main__":
    main()
