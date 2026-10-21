# Conservative image-motion diagnostics

`motion_diagnostics.py` supplements Phase 1 without writing its files or the physical `paddle_motion.csv` table. It never accepts winning numbers. It requires a local source file and an interval, native-pixel ROI, center and annulus chosen from direct frame inspection. Do not pass a camera cut/dissolve, zoom or changed view as a stable interval. Different apparent arms are not assumed to share an axis or speed.

The required review JSON binds the exact local input SHA256 and source-PTS interval:

```json
{
  "stable_camera_reviewed": true,
  "source_sha256": "INSERT_ACTUAL_LOCAL_SOURCE_SHA256",
  "start_pts": 0,
  "end_pts": 1,
  "evidence_refs": ["INSERT_REVIEWED_NATIVE_FRAME_LOCATORS"],
  "marker_status": "uncertain",
  "marker_notes": "INSERT_DIRECT_OBSERVATION_AND_LIMITATIONS"
}
```

Those times are syntax examples, not a selected video interval. `marker_status` permits `confirmed_unique`, `not_observable`, or `uncertain`. Marker assessment is a manual feasibility gate; this tool does not automatically follow a unique physical marker or implement plane calibration. Physical angle and RPM therefore remain NA even when a reviewer identifies a possible marker.

Example command structure, replacing all placeholders with reviewed measurements:

```powershell
& C:\vietlott-power655-env\Scripts\python.exe phase2/scripts/motion_diagnostics.py LOCAL_SOURCE.mp4 --start SOURCE_PTS_START --end SOURCE_PTS_END --roi X Y WIDTH HEIGHT --center-source SOURCE_CX SOURCE_CY --annulus R_MIN R_MAX --review REVIEW.json --out phase2/evidence/NEW_RUN
```

Center coordinates refer to the encoded source image, before ROI cropping. Rotation metadata is not automatically applied. The annulus must fit wholly inside the crop. Frames are not resized. Polar profiles sample the existing pixels with bilinear spatial interpolation; no temporal frame interpolation or timing resampling occurs. ffprobe PTS are cross-checked against ffmpeg `showinfo` with `-copyts`. Global source frame index remains NA. Acquisition evidence must independently establish whether a packet-copy local clip preserved original YouTube source PTS.

Five methods are represented:

1. Marker feasibility: manual, evidence-bound status; no invented marker identity or reconstructed hidden tip.
2. Dense Farneback optical flow: median small-displacement projected angular increment from tangential pixel flow about the reviewed image center. It is not a rigid-rotation estimate or an unwrapped paddle angle. Pixel-wise IQR measures image-flow spread; it is not physical measurement uncertainty or a confidence interval.
3. Angular template matching: circular normalized correlations of adjacent masked polar profiles, retaining the number of peaks within 0.02 of the highest correlation. Threefold repeated texture returns multiple equivalent shifts. One image peak still does not prove marker identity or absence of aliasing.
4. Temporal autocorrelation: lag peaks of the real image-harmonic coefficient.
5. Temporal spectrum: Hann-window periodogram of the same real coefficient. Harmonic order is a declared image hypothesis, default 3, never a recovered rotor count. Spectrum bin spacing is resolution, not a confidence interval. No automatic conversion into RPM occurs.

Autocorrelation and FFT require at least 16 frames and maximum PTS interval deviation of at most 1% of the median. Otherwise they remain uncomputed; the tool does not fill gaps. A finite missing-data sector invalidates that frame's coefficient. Periodicity can come from balls, static structures, highlights or lighting. Masked and unmasked image signals plus the moving yellow-mask area signal are retained as controls. HSV exclusion uses the Phase 1 yellow range with a 5-pixel dilation; it is an unvalidated exclusion heuristic, not a certified ball detector. Moving-mask changes and per-frame absolute image differences are diagnostic columns, not automatic proof of camera stability.

Outputs are `candidate_image_motion.csv`, `pattern_autocorrelation.csv`, `pattern_spectrum.csv`, `diagnostics.json`, `input_provenance.json`, and `decode.log`. Input SHA256, native crop hashes, source stream information, ffmpeg/ffprobe versions, source code SHA256, environment versions and code commit are recorded. Failures after run creation leave `failure.json`; reruns must use a new directory. Source pixels are kept in RAM and not written by this tool.

Bounds: interval <=30 seconds, crop <=1 million pixels, native frame cap 16–900 (default 300), anticipated decoded crop memory <=512 MiB. The current implementation may also hold temporary copies and flow arrays; the cap is a crop-buffer limit, not a bound on total process RAM.

Run synthetic software checks from `phase2/scripts`:

```powershell
& C:\vietlott-power655-env\Scripts\python.exe -m unittest test_motion_diagnostics -v
```

Eight fixtures check known template displacement, threefold ambiguity, known signal frequency, indistinguishable 3/27 Hz sampling aliases, irregular PTS refusal, masked missingness, small-rotation flow direction/scale, source-PTS preservation, and end-to-end provenance/overwrite behavior. Some checks share one fixture. Synthetic images and testsrc video are locally generated and removed; they are never real-video evidence. Passing these tests does not establish accuracy on Vietlott video.
