"""Audit legacy scalar appearance evidence; does not decode or certify video RPM.

Only Phase2 outputs are written. The synthetic fixtures validate numerical logic
and demonstrate nonidentifiability, never validate experimental video measurements.
"""
import argparse
import csv
import hashlib
import json
import platform
import subprocess
from pathlib import Path

import numpy as np
import scipy
from scipy.signal import find_peaks, periodogram

ROOT = Path(__file__).resolve().parents[2]
PHASE2 = ROOT / "phase2"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def analyze(t, z, harmonic=3):
    t, z = np.asarray(t, float), np.asarray(z, complex)
    if len(t) < 10 or len(t) != len(z) or not np.all(np.isfinite(t)) or not np.all(np.isfinite(z)):
        raise ValueError("Need >=10 finite paired samples")
    dt = np.diff(t)
    if np.any(dt <= 0) or harmonic <= 0:
        raise ValueError("Need increasing PTS and positive harmonic")
    fs = float(1 / np.median(dt))
    phase = np.unwrap(np.angle(z))
    x = t - t[0]
    coef = np.polyfit(x, phase, 1)
    residual = phase - np.polyval(coef, x)
    f, power = periodogram(z.real, fs=fs, window="hann", detrend="linear")
    valid = (f > .5) & (f < fs / 2)
    peak_index = np.where(valid)[0][np.argmax(power[valid])]
    peak = float(f[peak_index])
    cf, cp = periodogram(z, fs=fs, window="hann", detrend="linear", return_onesided=False)
    valid_complex = (np.abs(cf) > .5) & (np.abs(cf) < fs / 2)
    ci = np.where(valid_complex)[0][np.argmax(cp[valid_complex])]
    centered = z.real - z.real.mean()
    ac = np.correlate(centered, centered, mode="full")[len(z)-1:]
    ac = ac / ac[0] if ac[0] else np.zeros_like(ac)
    # Report strongest eligible positive local maximum, never treat it as a marker.
    peaks, _ = find_peaks(ac[:len(z)//2+1])
    peaks = [int(i) for i in peaks if i >= 2 and ac[i] > 0]
    lag = max(peaks, key=lambda i: ac[i]) if peaks else None
    slope_hz = float(coef[0] / (2 * np.pi))
    return {
        "sample_count": len(t), "pts_first": float(t[0]), "pts_last": float(t[-1]),
        "sample_rate_hz_median_pts": fs,
        "pts_interval_min_seconds": float(dt.min()), "pts_interval_max_seconds": float(dt.max()),
        "assumed_harmonic": harmonic,
        "phase_slope_pattern_hz_signed": slope_hz,
        "phase_slope_candidate_rpm_signed": slope_hz * 60 / harmonic,
        "real_periodogram_peak_hz": peak,
        "real_periodogram_candidate_rpm_abs": peak * 60 / harmonic,
        "complex_periodogram_peak_hz_signed": float(cf[ci]),
        "complex_periodogram_candidate_rpm_signed": float(cf[ci] * 60 / harmonic),
        "spectrum_bin_width_hz": fs / len(t),
        "candidate_rpm_bin_width": fs / len(t) * 60 / harmonic,
        "conditional_alias_rpm_spacing": fs * 60 / harmonic,
        "conditional_principal_alias_rpm_limit": fs * 30 / harmonic,
        "coefficient_phase_fit_residual_rms_radians": float(np.sqrt(np.mean(residual**2))),
        "candidate_angle_fit_residual_rms_deg": float(np.rad2deg(np.sqrt(np.mean(residual**2))) / harmonic),
        "coefficient_phase_step_abs_max_deg": float(np.rad2deg(np.max(np.abs(np.diff(phase))))),
        "coefficient_amplitude_min": float(np.abs(z).min()),
        "coefficient_amplitude_median": float(np.median(np.abs(z))),
        "coefficient_amplitude_max": float(np.abs(z).max()),
        "real_autocorrelation_strongest_positive_local_peak_lag_samples": lag,
        "real_autocorrelation_at_reported_lag": float(ac[lag]) if lag else None,
        "real_autocorrelation_candidate_rpm_abs": fs / lag * 60 / harmonic if lag else None,
        "physical_rpm": None, "physical_direction": None, "absolute_physical_angle_deg": None,
    }


def synthetic_validation():
    """Independent analytic inputs, including adversarial alias/mask fixtures."""
    records = []
    t = np.arange(120) / 30
    z = np.exp(2j * np.pi * 2 * t)
    positive = analyze(t, z)
    assert abs(positive["phase_slope_candidate_rpm_signed"] - 40) < 1e-8
    assert abs(positive["real_periodogram_candidate_rpm_abs"] - 40) < 1e-8
    records.append({"name": "analytic_40rpm_h3_positive", "status": "passed", "expected_candidate_rpm": 40})
    negative = analyze(t, z.conj())
    assert abs(negative["phase_slope_candidate_rpm_signed"] + 40) < 1e-8
    assert abs(negative["real_periodogram_candidate_rpm_abs"] - 40) < 1e-8
    records.append({"name": "negative_direction_real_spectrum_sign_ambiguity", "status": "passed"})
    z_alias = np.exp(2j * np.pi * 32 * t)
    alias_error = float(np.max(np.abs(z - z_alias)))
    assert alias_error < 1e-10
    assert abs(analyze(t, z_alias)["phase_slope_candidate_rpm_signed"] - 40) < 1e-8
    records.append({"name": "40_and_640rpm_h3_indistinguishable_at_30hz", "status": "passed", "maximum_coefficient_difference": alias_error})
    theta = 2 * np.pi * (40 / 60) * t
    symmetry_error = float(np.max(np.abs(np.exp(3j * theta) - np.exp(3j * (theta + 2 * np.pi / 3)))))
    assert symmetry_error < 1e-10
    records.append({"name": "threefold_absolute_angle_120deg_ambiguity", "status": "passed", "maximum_coefficient_difference": symmetry_error})
    # Completely static radial brightness. Only an exclusion mask rotates.
    # Its changing radial weighting creates an h3 coefficient after averaging.
    phi = np.arange(360) * 2 * np.pi / 360
    radial = np.linspace(40, 200, 24)[:, None]
    static_polar = np.broadcast_to(radial, (24, 360))
    profiles = []
    for ti in t:
        distance = np.angle(np.exp(1j * (phi - np.pi * ti)))
        valid = np.ones((24, 360))
        valid[12:, np.abs(distance) < .3] = 0
        profiles.append(np.sum(static_polar * valid, axis=0) / valid.sum(axis=0))
    profiles = np.asarray(profiles)
    moving = profiles - np.median(profiles, axis=0)
    mask_coeff = moving @ np.exp(3j * phi) / len(phi)
    mask_result = analyze(t, mask_coeff)
    assert abs(mask_result["phase_slope_candidate_rpm_signed"] - 30) < .2
    assert abs(mask_result["real_periodogram_candidate_rpm_abs"] - 30) < 1e-8
    records.append({"name": "static_background_rotating_exclusion_mask_false_motion", "status": "passed",
                    "static_background_rpm": 0, "apparent_candidate_rpm": mask_result["phase_slope_candidate_rpm_signed"],
                    "interpretation": "Mask-only confound is possible; does not prove it caused the real-video discrepancy."})
    for name, bad in [("duplicate_pts_rejected", np.zeros(120)), ("decreasing_pts_rejected", -t)]:
        try:
            analyze(bad, z)
        except ValueError:
            records.append({"name": name, "status": "passed"})
        else:
            raise AssertionError(name)
    return {"status": "passed", "fixture_count": len(records), "experimental_validation": False, "fixtures": records}


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows({k: "NA" if v is None else v for k, v in row.items()} for row in rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--validate-only", action="store_true")
    args = ap.parse_args()
    validation = synthetic_validation()
    if args.validate_only:
        print(json.dumps(validation, indent=2))
        return
    source = ROOT / "measurements/draw_01372_857_appearance.csv"
    metadata = source.with_suffix(".json")
    spectrum = source.with_name(source.stem + "_spectrum.csv")
    with source.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    t = np.array([float(r["timestamp_seconds"]) for r in rows])
    z = np.array([complex(float(r["coefficient_real"]), float(r["coefficient_imag"])) for r in rows])
    h_values = {int(r["harmonic"]) for r in rows}
    if h_values != {3} or [int(r["clip_frame_index"]) for r in rows] != list(range(120)):
        raise ValueError("Unexpected legacy evidence identity/schema")
    old = json.loads(metadata.read_text(encoding="utf-8"))
    result = analyze(t, z)
    angle = np.rad2deg(np.unwrap(np.angle(z))) / 3
    stored_angle = np.array([float(r["candidate_appearance_angle_deg"]) for r in rows])
    stored_amplitude = np.array([float(r["amplitude"]) for r in rows])
    with spectrum.open(encoding="utf-8") as f:
        spectrum_rows = list(csv.DictReader(f))
    freq, power = periodogram(z.real, fs=result["sample_rate_hz_median_pts"], window="hann", detrend="linear")
    sf = np.array([float(r["frequency_hz"]) for r in spectrum_rows])
    sp = np.array([float(r["power"]) for r in spectrum_rows])
    reproduction = {
        "stored_angle_max_abs_error_deg": float(np.max(np.abs(angle - stored_angle))),
        "stored_amplitude_max_abs_error": float(np.max(np.abs(np.abs(z) - stored_amplitude))),
        "stored_frequency_max_abs_error_hz": float(np.max(np.abs(freq - sf))),
        "stored_power_max_abs_error": float(np.max(np.abs(power - sp))),
        "phase_candidate_vs_phase1_abs_error_rpm": abs(result["phase_slope_candidate_rpm_signed"] - old["method1_candidate_signed_rpm"]),
        "spectrum_candidate_vs_phase1_abs_error_rpm": abs(result["real_periodogram_candidate_rpm_abs"] - old["method2_pattern_spectrum_candidate_abs_rpm"]),
    }
    assert max(reproduction.values()) < 1e-8, reproduction
    phase_rpm = result["phase_slope_candidate_rpm_signed"]
    spec_rpm = result["real_periodogram_candidate_rpm_abs"]
    fs = result["sample_rate_hz_median_pts"]
    pf = result["phase_slope_pattern_hz_signed"]
    sf_peak = result["real_periodogram_peak_hz"]
    alias_residual = min(abs(pf - (sign * sf_peak + k * fs)) for sign in (-1, 1) for k in range(-3, 4))
    yellow = np.array([float(r["yellow_mask_area_px"]) for r in rows])
    yf, yp = periodogram(yellow, fs=fs, window="hann", detrend="linear")
    yvalid = (yf > .5) & (yf < fs / 2)
    yellow_peak = float(yf[yvalid][np.argmax(yp[yvalid])])
    windows = []
    cross = []
    for name, lo, hi in [("full_120", 0, 120), ("first_60", 0, 60), ("last_60", 60, 120), ("first_90", 0, 90), ("last_90", 30, 120)]:
        a = analyze(t[lo:hi], z[lo:hi])
        a.update(window=name, clip_index_first=lo, clip_index_last=hi-1)
        windows.append(a)
        for method, key, unit in [
                ("unwrapped_coefficient_phase_ols", "phase_slope_candidate_rpm_signed", "signed"),
                ("real_coefficient_periodogram", "real_periodogram_candidate_rpm_abs", "magnitude"),
                ("complex_coefficient_periodogram", "complex_periodogram_candidate_rpm_signed", "signed"),
                ("real_coefficient_autocorrelation", "real_autocorrelation_candidate_rpm_abs", "magnitude")]:
            cross.append({"draw_id": "01372", "source_id": "IUU05082QtE", "source_phase": "operation_test_legacy",
                "evidence_input": source.relative_to(ROOT).as_posix(), "window": name,
                "pts_first": a["pts_first"], "pts_last": a["pts_last"], "sample_count": a["sample_count"],
                "method": method, "shared_signal": "legacy_spatial_Fourier_h3_coefficient",
                "assumed_harmonic": 3, "candidate_rpm": a[key], "candidate_direction_type": unit,
                "physical_rpm": None, "absolute_angle_deg": None, "uncertainty_degrees": None,
                "spectrum_bin_width_candidate_rpm": a["candidate_rpm_bin_width"] if "periodogram" in method else None,
                "status": "exploratory_scalar_reanalysis_only", "independent_measurement": False,
                "limitation": "Same unverified image signal; subwindows are diagnostics, not independent draws; physical marker/geometry/alias unknown"})
    environment = {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__}
    audit = {
        "audit_kind": "recomputed_legacy_scalar_evidence_not_new_video_measurement",
        "phase1_commit": "b2b1938cf38cc976a302cd8fd6a29bd4dd3c3df5",
        "audit_execution_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "source_id": "IUU05082QtE", "source_url": "https://www.youtube.com/watch?v=IUU05082QtE",
        "source_phase": "operation_test_not_official_draw", "source_format_id": old["source_format_id"],
        "source_dimensions": [old["source_width"], old["source_height"]],
        "source_video_sha256": None, "new_video_decode_performed": False,
        "input_hashes": {p.relative_to(ROOT).as_posix(): sha256(p) for p in [source, metadata, spectrum, ROOT / "scripts/measure_stream_appearance.py"]},
        "audit_script_sha256": sha256(Path(__file__)), "environment": environment,
        "environment_note": "Audit uses installed versions shown here; Phase1 lock versions differ. Scalar replication verified numerically.",
        "recomputed": result, "reproduction_comparison": reproduction,
        "disagreement": {
            "candidate_difference_rpm": spec_rpm - phase_rpm, "spectral_to_phase_ratio": spec_rpm / phase_rpm,
            "ratio_minus_3_over_2": spec_rpm / phase_rpm - 1.5,
            "same_harmonic_change_preserves_ratio": True,
            "posthoc_phase_divisor_2_candidate_rpm": phase_rpm * 3 / 2,
            "posthoc_phase_divisor_2_minus_original_spectrum_rpm": phase_rpm * 3 / 2 - spec_rpm,
            "harmonic_conclusion": "Near 3:2 arithmetic is not evidence of different spatial harmonics; both estimates use exactly the stored h3 coefficient. Re-dividing one by 2 would be an unsupported posthoc conversion.",
            "minimum_same_harmonic_alias_frequency_residual_hz": alias_residual,
            "minimum_same_harmonic_alias_residual_rpm": alias_residual * 60 / 3,
            "alias_conclusion": "These two aggregate frequencies are not exact +/-f+kFs equivalents under a constant single h3 periodic signal. That does not exclude alias in the underlying mixed/noisy video signal.",
        },
        "mask_diagnostics": {
            "yellow_mask_area_min_px": int(yellow.min()), "yellow_mask_area_max_px": int(yellow.max()),
            "yellow_mask_area_median_px": float(np.median(yellow)), "yellow_mask_area_full_crop_fraction_min": float(yellow.min()/810000),
            "yellow_mask_area_full_crop_fraction_max": float(yellow.max()/810000),
            "whole_crop_mask_area_not_annulus_visibility": True,
            "yellow_area_real_coefficient_pearson_r_descriptive": float(np.corrcoef(yellow, z.real)[0, 1]),
            "yellow_area_imag_coefficient_pearson_r_descriptive": float(np.corrcoef(yellow, z.imag)[0, 1]),
            "yellow_area_amplitude_pearson_r_descriptive": float(np.corrcoef(yellow, np.abs(z))[0, 1]),
            "yellow_area_periodogram_peak_hz": yellow_peak,
            "inference": "Descriptive dependent-sample diagnostics only, no p-values or causal attribution. Annular profiles and pixels are not retained; mask/ROI variants cannot be recomputed from these scalars.",
        },
        "fixed_subwindow_diagnostics": windows,
        "synthetic_validation": validation,
        "unknowns": ["unique physical marker and paddle identity", "common shaft/topology and valid spatial harmonic", "camera calibration/refraction and geometric angle", "shutter exposure and blur", "physical alias branch and direction", "annulus per-angle validity and discarded pixels", "which confound caused the candidate mismatch"],
        "conclusion": "physical_rpm=NA; absolute_physical_angle=NA; empirical_physical_angle_uncertainty=NA. Numerical replication succeeds; physical identifiability does not follow.",
    }
    (PHASE2 / "evidence").mkdir(parents=True, exist_ok=True)
    (PHASE2 / "evidence/legacy_rpm_audit.json").write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(PHASE2 / "rpm_cross_validation.csv", cross)
    window_table = "\n".join(
        f"| {a['window']} | {a['phase_slope_candidate_rpm_signed']:.6f} | {a['real_periodogram_candidate_rpm_abs']:.6f} | {a['real_autocorrelation_candidate_rpm_abs']:.6f} |"
        for a in windows
    )
    markdown = f"""# Kiểm toán candidate RPM Phase 1

## Phạm vi và kết quả

Chỉ tính lại **120 hàng hệ số ảnh đã lưu**, PTS {t[0]:.6f}–{t[-1]:.6f} s của IUU05082QtE, format 137, 1920×1080. Đoạn này thuộc kiểm tra vận hành, không thuộc quay chính thức. Không giải mã video mới trong script kiểm toán này. Nguồn, SHA256 và phiên bản thực chạy nằm trong `evidence/legacy_rpm_audit.json`.

- Phase slope có dấu: **{phase_rpm:.9f} candidate RPM**.
- Đỉnh periodogram phần thực: **{spec_rpm:.9f} candidate RPM**.
- Chênh lệch: **{spec_rpm-phase_rpm:.9f} candidate RPM**; tỷ số {spec_rpm/phase_rpm:.9f}.
- Fs từ median chênh PTS: {fs:.9f} Hz. Độ rộng bin: {result['candidate_rpm_bin_width']:.9f} candidate RPM; đây không phải CI.
- **RPM vật lý, góc vật lý tuyệt đối, chiều quay và sai số góc thực nghiệm: NA.** Tái lập đúng phép tính không xác nhận đại lượng cơ học.

Sai khác lớn nhất khi tái tạo góc, biên độ, phổ và hai candidate đã lưu là {max(reproduction.values()):.3g}; các kiểm tra <1e-8 đều đạt với Python {environment['python']}, NumPy {environment['numpy']}, SciPy {environment['scipy']}. Đây là phiên bản cài thực tế; không giả vờ đã dùng lockfile Phase 1.

## Harmonic và alias

Hai thuật toán dùng **cùng hệ số Fourier góc h=3**. Đổi cùng hệ số chia cho cả hai không đổi tỷ số. Tỷ số gần 3/2 (lệch {spec_rpm/phase_rpm-1.5:.9f}) không chứng minh harmonic sai: tự chia pha cho 2 cho {phase_rpm*1.5:.9f}, vẫn lệch {phase_rpm*1.5-spec_rpm:.9f} RPM, và không có bằng chứng marker/hình học để thay phép đổi. Không chọn lại harmonic nhằm ép khớp.

Nếu và chỉ nếu một chu kỳ vật lý tạo h=3 chu kỳ ảnh, nhánh alias cách {result['conditional_alias_rpm_spacing']:.6f} RPM và nhánh chính ±{result['conditional_principal_alias_rpm_limit']:.6f} RPM. Không có giới hạn vật lý độc lập nên không thể chọn nhánh chính. Hai tần số tổng hợp hiện tại không đồng nhất theo ±f+kFs: phần dư nhỏ nhất {alias_residual:.9f} Hz ({alias_residual*20:.9f} candidate RPM). Do tín hiệu không phải một sinusoid đã xác nhận, điều này không loại alias khỏi video; nó chỉ bác cách sửa đơn giản bằng cộng một nhánh Fs/h cho một candidate.

## ROI, bóng, che khuất và phối cảnh

Code Phase 1 cố định crop x=510,y=60,w=900,h=900; tâm (450,450), annulus 130–400 px. Nó lấy trung bình sáng theo bán kính ở từng hướng sau khi loại màu vàng, trừ median theo thời gian, rồi lấy h3. Đây là tín hiệu ảnh tổng hợp; không theo dõi vật liệu của một tay gạt. Marker bất đối xứng, số trục, h và hiệu chuẩn mặt phẳng chưa được xác nhận.

Số pixel mask vàng toàn crop thay đổi {int(yellow.min())}–{int(yellow.max())} ({yellow.min()/810000:.2%}–{yellow.max()/810000:.2%} diện tích crop). Đây **không phải tỷ lệ che annulus**. Pearson mô tả giữa mask và hệ số thực/ảo/biên độ lần lượt {np.corrcoef(yellow,z.real)[0,1]:.4f}, {np.corrcoef(yellow,z.imag)[0,1]:.4f}, {np.corrcoef(yellow,np.abs(z))[0,1]:.4f}; không tính p-value trên các frame tương quan, không suy ra nguyên nhân. Mask động thay đổi mẫu nền theo bán kính; bóng không bị loại hoàn toàn và biên mask, blur, thanh nền, phối cảnh, tay trong suốt cũng có thể làm đổi pha.

Fixture đối kháng tạo nền sáng hoàn toàn đứng yên với mask loại trừ quay cho candidate gần 30 RPM. Nó chứng minh cơ chế gây nhiễu **có thể xảy ra**, không chứng minh đây là nguyên nhân ở video thật. Hệ số đã nén và tổng area không giữ thông tin đủ để chạy lại ROI/mask/camera ablation. Cần pixels và marker thật để phân biệt các nguyên nhân; chưa định lượng riêng lỗi phối cảnh hoặc blur.

## Độ ổn định và tính độc lập

`rpm_cross_validation.csv` chứa 20 hàng của bốn phép tính trên năm cửa sổ cố định (120, 60 đầu/cuối, 90 đầu/cuối). Periodogram phức và autocorrelation chỉ là chẩn đoán mới trên **cùng scalar cũ**; chúng không là phép đo video mới hoặc cảm biến độc lập. Các cửa sổ chồng nhau không là các kỳ độc lập. Không chọn cửa sổ có kết quả đẹp để thay kết luận toàn đoạn. Mỗi dòng giữ physical RPM=NA.

| Cửa sổ | Phase slope candidate RPM có dấu | Periodogram thực candidate RPM độ lớn | Autocorrelation candidate RPM độ lớn |
|---|---:|---:|---:|
{window_table}

Các kết quả phụ thuộc mạnh vào cửa sổ; chưa phân biệt được thay đổi tín hiệu, tốc độ thật và sai nhận dạng. Bước pha hệ số lớn nhất là {result['coefficient_phase_step_abs_max_deg']:.6f} độ, gần ngưỡng unwrap 180 độ; thiếu một giới hạn tốc độ và marker độc lập để xác minh nhánh unwrap.

Độ lệch RMS pha ảnh/3 quanh đường hồi quy toàn đoạn là {result['candidate_angle_fit_residual_rms_deg']:.6f} độ. Đây là residual của mô hình tín hiệu ảnh, **không là sai số góc vật lý hoặc CI**. Không có góc tuyệt đối khi thiếu marker duy nhất; đối xứng h3 tự mang bất định 120 độ và chưa loại các nhánh alias.

## Kiểm thử và tái lập

Chạy từ thư mục dự án:

```powershell
python phase2/scripts/rpm_audit.py --validate-only
python phase2/scripts/rpm_audit.py
```

{validation['fixture_count']} fixture tổng hợp đạt: tốc độ phân tích đã biết 40 RPM, dấu quay âm, hai chuyển động 40/640 RPM cho cùng mẫu ở 30 Hz, bất định góc 120 độ, nền tĩnh với mask động, PTS trùng và PTS giảm bị từ chối. Synthetic chỉ kiểm numerical logic/counterexample, không xác nhận video. Các input Phase 1 không bị ghi.

**Kết luận:** hai candidate cũ tái lập được và không đủ cơ sở chuyển thành RPM máy. Chưa thể chọn một nguyên nhân duy nhất cho bất đồng từ 120 scalar đã lưu. Cần kiểm marker và hiệu chuẩn/alias trên video liên tục hoặc encoder độc lập; H1 vẫn thiếu góc vật lý.
"""
    (PHASE2 / "evidence/legacy_rpm_audit.md").write_text(markdown, encoding="utf-8")
    print(json.dumps({"status": "passed", "synthetic_fixture_count": validation["fixture_count"], "recomputed": result,
                      "outputs": ["phase2/evidence/legacy_rpm_audit.json", "phase2/evidence/legacy_rpm_audit.md", "phase2/rpm_cross_validation.csv"]}, indent=2))


if __name__ == "__main__":
    main()
