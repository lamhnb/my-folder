# Champion-X — Exporting mechanical draw evidence without inventing data (2026-11-04)

## What was actually found
- A third-party video *candidate* titled **"Trực Tiếp Quay Thưởng Kết Quả Xổ Số Tự Chọn Power 6/55 - Trường Quay Vietlott"**, uploaded 2017-09-30: https://www.youtube.com/watch?v=GidYNrF55XY
- Another candidate with same draw-studio title, uploaded 2017-08-17: https://www.youtube.com/watch?v=sBwazjdBKE4
- Neither video has been frame-verified as an uncut real physical draw; uploader is not the official Vietlott channel. Titles are weak evidence.
- Vietlott full live streams were confirmed by its representative as broadcast on SCTV2, Vietlott official website, and Vietlott's official YouTube at 18:00–18:30. Facebook provides only brief initial broadcast. https://tuoitre.vn/nld/vi-sao-vietlott-khong-livestream-toan-bo-cac-phien-quay-so-mo-thuong-tren-mang-xa-hoi-196250714145608742.htm
- As of this investigation, **no public uncut video file was lawfully accessed or exported**; no seven-ball physical sequence was observed. It would be misleading to report a recovered ball order.

## Practical extractor now committed
`champion_x_extract_draw_evidence.py` requires one locally available recording that the researcher is authorized to access. Dependencies Python3, ffmpeg, ffprobe.

Example once such a video exists:
```shell
python champion_x_extract_draw_evidence.py --input full_draw.mp4 --draw-id 01420 --date 2026-11-05 --every 2
```

Outputs:
- SHA256 and duration/codec metadata in `video_metadata.json`;
- `contact_0001.jpg`, etc. sampled frame-contact sheets to find relevant scenes;
- empty `seven_ball_manual_annotation.csv` with seven positions and two-reviewer columns;
- a README warning sampling may miss quick ball exits and **manual frame-by-frame checking** is mandatory.

**The script does not download/record YouTube or protected SCTV player video**; it does not do OCR or invent ball labels. Video recording/downloading is only appropriate where the source owner or platform permits it, and no access-control/DRM bypass is allowed. User does not need a PC for this source discovery task, but the video-source permission/access is a real blocker. This source file was committed but no CI video integration test has yet passed because there is no authorized video input.

## Data acquisition priorities
1. Retrieve a publicly accessible authorized full recording from Vietlott's official YouTube archive or SCTV2's account-entitled catch-up service. Confirm a real machine sequence, not a results-only montage.
2. If archives do not expose full content, send a formal research request asking Vietlott/SCTV for a viewing link or **seven-ball extraction-order CSV and ball-case/machine identifiers**; timecode or device identifiers may be redacted.
3. After a verified file exists, export frames, double annotate 7 actual emitted balls, reconcile **first six as an unordered set** and **seventh as special**, then begin the physical bias tests. Do not rely on sorted results as extraction order.

## Frozen invariants
All registered Champions, Hybrid6 and R19 Frozen remain unchanged; no new Jackpot predictive advantage asserted.
