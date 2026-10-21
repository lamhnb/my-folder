# Pilot: image motion, not calibrated paddle measurements

This run uses the parent-selected interval and geometry from direct native-frame inspection, with no subsequent parameter tuning. Input is local `IUU05082QtE_f137_ranges.mp4`, SHA256 `c4740a0cbe28ea595ebb39487629a50b5bc8c7c88d91f777a4731660e07bce9c`. The video stream is 1920×1080 H264, format-137 provenance supplied by the parent acquisition evidence. ffprobe metadata duration is 2098.229467 seconds; the input is not a five-second-only file. The original source mapping must be read alongside acquisition provenance.

Requested source interval is [1098.030267, 1103.035267) seconds. Exactly 150 native decoded frames were cross-checked against ffprobe PTS, spanning 1098.030267–1103.001900 seconds. Median PTS spacing corresponds to approximately 29.969731 samples/second; maximum spacing deviation is 0.000001 second. This is rendition timing, not camera-original frame rate or a claim of independent new images at every PTS. Global frame indices remain NA. No image resizing or temporal interpolation was used.

The fixed native crop is x=480, y=80, width=900, height=900; source-image center=(932,525); annulus radii=130–350 pixels. Six full-resolution one-second samples, contact sheet, frame ledger and the first native reference were inspected. The outer ring and hub appear stable after the preceding zoom, but subtle drift remains unquantified. Perspective and rotation-plane calibration are absent. The three apparent transparent blades do not provide a verified unique material marker. Similar appearance does not establish shared axis or speed. Blur, occlusion and moving balls remain major confounds.

| Method | Pilot observation | Interpretation |
|---|---|---|
| Unique marker | `not_observable` under the present review | Absolute physical angle and physical identity cannot be recovered here. |
| Tangential dense optical flow | Median projected increment ≈3.92×10⁻⁸ image degrees/frame across 149 pairs; median within-frame pixel IQR≈0.0211 degrees | A median dominated by static/dark/transparent structures can approach zero despite visible motion. This cannot establish a stopped or slowly rotating paddle. |
| Angular template matching | Median selected cyclic shift 15 image degrees/frame; range −107 to 144; 2/149 pairs contain multiple peaks within 0.02 of the highest correlation | Jumping image peaks and unresolved threefold ambiguity fail to establish marker identity or a physical rotation branch. This disagrees with treating the median flow as the same rigid rotation. |
| Masked h=3 autocorrelation and spectrum | Not computed | Frame 51 has a fully excluded angular sector, producing a missing coefficient. The generic software status includes several possible causes; this run failed the missing-signal condition, not the PTS-uniformity condition. No missing value was filled. |
| Unmasked h=3 image spectrum | Peak 3.596368 Hz; bin width 0.199798 Hz | Image-pattern frequency only. Harmonic order 3 is an image hypothesis. No physical RPM conversion or uncertainty interval is justified. |
| Unmasked h=3 autocorrelation | Strongest positive peak lag 0.266936 seconds | An image recurrence. Its reciprocal is approximately 3.7462 Hz, within one coarse spectrum bin of the spectral peak. That compatibility is not independent validation. |
| Moving-yellow-mask control | Spectrum peak 1.598386 Hz; strongest positive autocorrelation lag 0.200202 seconds | Mask variation has its own periodic structure; nuisance motion is not removed simply by excluding yellow pixels. |

The excluded yellow fraction varies from 8.84% to 14.21% of crop pixels (median 12.03%). The median fraction whose mask status changes between frames is 11.11%. These are heuristic image-mask quantities, not ball counts or validated occlusion measurements.

An exploratory quality screen found 24 of 149 adjacent pairs with mean absolute gray difference below 1 on the 0–255 scale, compared with the overall median of 20.709. Many such pairs recur roughly 0.2002 seconds apart. They are near-duplicate candidates, not bit-identical frames or a validated duplicate classification. Held/repeated encoded pictures are a plausible explanation; upstream processing and camera-original FPS remain unknown. No frames were deleted, time-compressed or interpolated to repair this. Uniform rendition PTS alone cannot eliminate this sampling concern.

Physical angle, physical direction, paddle IDs and physical RPM remain NA. Pixel-flow IQR and spectral bin width are not confidence intervals. This run supports an observability limitation and records conflicting image cues. It does not resolve the Phase 1 63.789/94.904 candidate discrepancy: those candidates came from a different operation-check interval and have no verified common physical marker or calibration. No H1 phase estimate can be attached to a capture event from this pilot.

Reproduce from the physical-research directory, substituting a new output directory because overwrite is refused:

```powershell
& C:\vietlott-power655-env\Scripts\python.exe phase2/scripts/motion_diagnostics.py C:\vietlott-research-output\phase2-inputs\IUU05082QtE_f137_ranges.mp4 --start 1098.030267 --end 1103.035267 --roi 480 80 900 900 --center-source 932 525 --annulus 130 350 --review phase2/evidence/pilot_motion_review.json --out phase2/evidence/pilot_motion_reproduction
& C:\vietlott-power655-env\Scripts\python.exe phase2/scripts/plot_motion_diagnostics.py phase2/evidence/pilot_motion --out phase2/charts/pilot_motion_image_diagnostics_reproduction.png
& C:\vietlott-power655-env\Scripts\python.exe phase2/scripts/summarize_motion_quality.py phase2/evidence/pilot_motion --out phase2/evidence/pilot_motion/source_frame_quality_reproduction.json
```

The delivered chart `phase2/charts/pilot_motion_image_diagnostics.png` was visually inspected for labels and layout. Software regression evidence is in `evidence/motion_software_validation.json`; synthetic checks remain separate from this real-source exploratory evidence.
