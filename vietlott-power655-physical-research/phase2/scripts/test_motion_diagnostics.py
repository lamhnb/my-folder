"""Synthetic-only regression fixtures; never machine observations or validation."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import cv2
import numpy as np

from motion_diagnostics import PHASE2, angular_match, decode, polar_profile, projected_flow, sha256, temporal_diagnostics


class SyntheticMotionTests(unittest.TestCase):
    def test_threefold_pattern_has_multiple_equally_good_shifts(self):
        phi = np.arange(360) * np.pi / 180
        original = np.cos(3 * phi)
        match = angular_match(original, np.roll(original, 7))
        self.assertGreaterEqual(match["comparable_peak_count"], 3)
        self.assertEqual(match["ambiguity"], "multiple_comparable_shifts")

    def test_unique_asymmetric_profile_known_shift(self):
        rng = np.random.default_rng(107)
        original = rng.normal(size=360)
        match = angular_match(original, np.roll(original, -13))
        self.assertEqual(match["candidate_projected_shift_deg"], -13)
        self.assertEqual(match["comparable_peak_count"], 1)

    def test_known_frequency_and_alias_are_indistinguishable(self):
        times = np.arange(600) / 30
        low = np.cos(2 * np.pi * 3 * times)
        high = np.cos(2 * np.pi * 27 * times)
        self.assertTrue(np.allclose(low, high))
        result, _, _ = temporal_diagnostics(times, low)
        self.assertAlmostEqual(result["candidate_pattern_frequency_hz"], 3, places=8)
        self.assertAlmostEqual(result["autocorrelation_peak_lag_seconds"], 1 / 3, places=8)
        self.assertFalse(result["alias_resolved"])

    def test_irregular_pts_refuse_fft_instead_of_interpolation(self):
        times = np.arange(100) / 30
        times[50:] += .02
        result, ac, spec = temporal_diagnostics(times, np.cos(times))
        self.assertEqual(result["status"], "not_computed_irregular_pts_short_or_missing")
        self.assertEqual(ac, [])
        self.assertEqual(spec, [])

    def test_mask_unavailable_sector_is_missing_not_zero(self):
        gray = np.full((128, 128), 120, np.uint8)
        excluded = np.zeros_like(gray, bool)
        excluded[:, 64:] = True
        profile, coverage = polar_profile(gray, excluded, (64, 64), (20, 40))
        self.assertTrue(np.isnan(profile[0]))
        self.assertEqual(coverage[0], 0)
        self.assertAlmostEqual(profile[180], 120)

    def test_small_counterclockwise_rotation_flow_sign_and_scale(self):
        rng = np.random.default_rng(41)
        original = cv2.GaussianBlur(rng.integers(0, 256, (128, 128), dtype=np.uint8), (3, 3), .7)
        rotation = cv2.getRotationMatrix2D((64, 64), 1, 1)
        moved = cv2.warpAffine(original, rotation, (128, 128))
        result = projected_flow(original, moved, np.zeros_like(original, bool), (64, 64), (20, 45))
        self.assertAlmostEqual(result["flow_projected_increment_deg"], 1, delta=.15)

    def test_native_decode_matches_ffprobe_with_nonzero_source_pts(self):
        # Geometry-only, generated locally. No source video data or timestamps involved.
        with tempfile.TemporaryDirectory(prefix="phase2_synthetic_") as folder:
            source = Path(folder) / "fixture.mkv"
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=128x128:rate=30:duration=2",
                            "-vf", "setpts=PTS+12/TB", "-fps_mode", "passthrough", "-c:v", "ffv1", str(source)], check=True)
            pts, pixels, _, _, _ = decode(source, 12.2, 13.2, (16, 16, 64, 64), 50, 4 * 1024 ** 2)
            self.assertEqual(pixels.shape, (30, 64, 64, 3))
            self.assertAlmostEqual(pts[0], 12.2)
            self.assertTrue(np.all(np.diff(pts) > 0))

    def test_cli_provenance_separation_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory(prefix="synthetic_test_", dir=PHASE2) as folder:
            folder = Path(folder)
            source = folder / "fixture.mkv"
            subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=128x128:rate=30:duration=2",
                            "-vf", "setpts=PTS+12/TB", "-fps_mode", "passthrough", "-c:v", "ffv1", str(source)], check=True)
            review = folder / "review.json"
            review.write_text(json.dumps({"stable_camera_reviewed": True, "source_sha256": sha256(source),
                "start_pts": 12.2, "end_pts": 13.2, "marker_status": "uncertain",
                "marker_notes": "SYNTHETIC SOFTWARE FIXTURE ONLY", "evidence_refs": ["synthetic generated testsrc2"]}))
            import sys
            command = [sys.executable, str(PHASE2 / "scripts" / "motion_diagnostics.py"), str(source),
                       "--start", "12.2", "--end", "13.2", "--roi", "16", "16", "96", "96",
                       "--center-source", "64", "64", "--annulus", "10", "30",
                       "--review", str(review), "--out", str(folder / "result")]
            result = subprocess.run(command, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            metadata = json.loads((folder / "result" / "diagnostics.json").read_text())
            self.assertIsNone(metadata["physical_rpm"])
            self.assertIsNone(metadata["physical_angle_deg"])
            self.assertFalse(metadata["synthetic_is_real_evidence"])
            original_hash = sha256(folder / "result" / "diagnostics.json")
            rerun = subprocess.run(command, capture_output=True)
            self.assertNotEqual(rerun.returncode, 0)
            self.assertEqual(original_hash, sha256(folder / "result" / "diagnostics.json"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
