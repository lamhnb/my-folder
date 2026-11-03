# Champion-X Physical Draw — acquisition gate 2026-11-03

## Status
**Evidence discovery ONLY**. As of 2026-11-03, zero full original uncut Power 6/55 extraction sequences have been visually verified; zero verified machine/ball-case IDs. No sequence may be fabricated from ascending results lists, results-only videos, captions, or former ball-insertion order.

## New verified distribution paths
1. **Vietlott official site / YouTube live**: Vietlott's representative reportedly states the full 18:00–18:30 lottery draw is live-streamed via Vietlott.vn and its official YouTube as well as SCTV2, while Vietlott's Facebook stream covers only the ~5-minute introduction. Source: https://tuoitre.vn/nld/vi-sao-vietlott-khong-livestream-toan-bo-cac-phien-quay-so-mo-thuong-tren-mang-xa-hoi-196250714145608742.htm . The articles confirm a live broadcast, **not that the entire video is archived publicly or downloadable today**.
2. **SCTV2 broadcast / licensed replay**: SCTV Online official docs state some channels/programs have a replay window for the previous **3 days**, subject to supported channel and account plan. Confirm that SCTV2 includes Power 6/55 on the user's actual SCTV service; do not assume so. https://sctv.com.vn/dich-vu/sctv-online ; https://sctv.com.vn/dich-vu/sctv-online-new . Contact SCTV Online: `ttvts@sctv.vn`, hotline `1900 1878`; https://sctv.com.vn/dich-vu/sctv-online .
3. **Vietlott** contact page: https://vietlott.vn/vi/vietlott/lien-he , customer service 1900 55 88 89, Hanoi main office 024 62 686 818. Ask for accessible full official video, seven-ball physical extraction-order spreadsheet, and *non-sensitive* machine/ball-valise identifier by draw, where available.
4. **Do not confuse third-party “trực tiếp kết quả” videos with actual mechanical footage**. Prior discovered #01396/#01397 results-channel videos explicitly describe published results, not an uninterrupted original draw.

## Immediate pilot schedule
Target upcoming regularly scheduled Power draw Thursday **2026-11-05, 18:00–18:30 Asia/Ho_Chi_Minh**, subject to actual program confirmation. The exact draw ID should be verified from Vietlott's published result after the event; #01420 would be expected after #01419 but is NOT pre-certified here.

* Before 18:00: locate official live player on vietlott.vn and official Vietlott YouTube; verify channel ownership/domain. Also test SCTV Online to see SCTV2 availability and replay eligibility; do not purchase a plan without checking channel support.
* During or after: only access/download/record where permitted by service terms and rights. Do not bypass DRM, paywalls, authentication, copyright/access controls, or pretend a source was recorded.
* Archive source URI, video timestamp, source institution, publication time, author/content rights, complete-vs-cut status and file digest if lawful copy is available.
* Annotate emitted ball 1..7 in actual mechanical sequence, frame time and confidence; first six *set* must match official main numbers and seventh ball must match official special. Never use result-screen sorting as physical sequence.
* Optional: identify machine ID and ball-case ID ONLY if visible and reproducibly verified from official records.
* A second independent reading must confirm order; any unreadable ball is recorded as MISSING, not inferred.
* If source archive is absent, request an authorized copy from Vietlott or SCTV and keep case **blocked**.

## Proposed machine-readable record
Fields:
`draw_id,date,source_url,source_type,original_full_draw_verified,archive_access_rights,source_digest,extract_1,extract_2,extract_3,extract_4,extract_5,extract_6,extract_7,extract_timecodes,machine_id,machine_id_evidence,ball_case_id,ball_case_evidence,video_gaps,reviewer_1,reviewer_2,verified`.

## Statistical gate after enough usable records
- **Position-specific conditional null**: for the j-th physical extraction conditional on j-1 already-selected numbers, every remaining number has probability 1/(56-j). This is different from treating all 7 positions as independent.
- **Six-main inclusion probability**: unconditional 6/55. Position bias can exist without helping inclusion prediction; evaluate separately.
- **Device-conditioned likelihood**: only stratify if the device/case ID is grounded, with prespecified effect size and multiple-comparison control. Must not infer mass or diameter bias from permitted tolerance limits.
- **Do not optimize/pick bets from 10–100 annotated draws**: this sample could test feasibility and large artifacts but does not reliably detect modest physical effects.
- Hold future verified draws untouched after preregistration for any real test of an inclusion signal. Use random-extraction simulation and negative controls.
- Frozen invariants: R19, Hybrid6, registered Champions unchanged.

## Outcome as of registration
No usable physical sequence recovered. New actionable discovery is access to *broadcast/replay and official information request*. Next work is collection and verification, not another F30/F156 strategy.
