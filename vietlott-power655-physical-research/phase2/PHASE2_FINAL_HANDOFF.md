# Vietlott Power 6/55 — Phase 2: kiểm toán khả năng quan sát vật lý

Ngày thực hiện: **21/10/2026**, Asia/Bangkok. Base Phase 1: `b2b1938cf38cc976a302cd8fd6a29bd4dd3c3df5`. Branch: `research/power655-physical-phase2`. Chỉ bổ sung `phase2/`; không sửa dữ liệu Phase 1, B1, C50, B7-100, B7-200 hoặc Champion và không merge master.

## 1. Executive findings

**NO-GO cho mô hình động lực học 3D có thể hiệu chuẩn từ bộ video này.** Dữ liệu đủ để đo một số chuyển trạng thái nhìn thấy và mô tả nhịp chuyển bóng phía sau cơ cấu. Góc tay gạt vật lý, RPM thật, thời điểm bóng bị cô lập không thể quay lại và sai số vật lý thực nghiệm vẫn **NA**.

Phase 2 đã đi xa hơn metadata: tải đầy đủ và băm năm rendition thật; xem các đoạn chính thức; kiểm native frame cho **35 lần bóng rời miệng cơ cấu xuống ramp/kênh kết quả**, gồm sáu main và một special mỗi kỳ. Bàn giao **291 alias ảnh trước/sau**, manifest/hash, 261 hàng sự kiện/bối cảnh và bảng đối chiếu 35 lần thu. Các ô không quan sát được giữ NA và lý do riêng.

Pilot #01372 có 7 cận proxy rộng **0,033367–0,066733 s**, tương đương 1–2 khoảng frame encoded. Bốn kỳ đối chiếu có 28 cận rộng tối đa **0,133467 s**, tương đương 4 khoảng frame. Đó là **độ phân giải định vị trên ảnh**, không phải độ chính xác của thời điểm chọn/cô lập bóng. Không có CI hoặc accuracy vật lý được hiệu chuẩn.

Hai candidate cũ 63,789/94,904 RPM được tái tính đúng. Đặc biệt, **120/120 hash crop native và 120/120 PTS trùng Phase 1**. Cùng đoạn này thực sự có thay đổi scale/framing camera, làm ROI cố định thiếu ổn định. Đây là một yếu tố nhiễu đã thấy; chưa chứng minh nó là nguyên nhân duy nhất của bất đồng RPM.

## 2. Những gì đã đo được thật

- Năm source format 137, 1920×1080, `30000/1001` FPS rendition, với SHA256 toàn input, timebase, ffmpeg và hash script. Tải toàn file không đồng nghĩa giải mã toàn bộ: phạm vi đã xem/trích nằm trong từng ledger.
- Các cặp PTS/ảnh của trạng thái cơ cấu ngoài, bóng hiện trong hộp và bóng rời miệng hộp, với trạng thái bị che/cắt cảnh riêng. Pixel đo motion là native; contact sheet chỉ là ảnh xem thu nhỏ.
- Trên pilot, thời gian từ proxy bóng ra ramp đến số mới đọc rõ trên **overlay dưới màn hình** khoảng **3,036–4,638 s** xét bao toàn bộ cận của bảy lần. Đây không phải latency từ thời điểm chọn bóng. Số trên bóng, số ở phông trường quay, số đang animation và số đã vào ô không được đồng nhất.
- Các đại lượng **ảnh** từ 150 frame chính thức PTS 1098,030267–1103,001900: flow chiếu, template shift, hệ số ảnh và phổ/autocorrelation/control-mask. Chúng không là góc của một tay gạt có danh tính.
- Nhịp downstream theo từng kỳ, với interval arithmetic và đơn vị phân tích là kỳ; special tách khỏi main.

Không dùng số trúng để chọn ROI/harmonic hoặc sửa tham số đo. Các số nhìn thấy chỉ giúp kiểm chuỗi sự kiện; không xây thuật toán dự đoán.

## 3. Những gì chưa đo được

Không có góc tuyệt đối, physical paddle ID, RPM/chiều quay vật lý hoặc error góc theo độ. Không biết topology chung/riêng trục. Không có thời điểm cô lập vĩnh viễn đã xác nhận, trạng thái toàn bộ cửa/chốt, lệnh điều khiển điện, thời gian trộn chính xác, danh tính bóng xuyên va chạm, quỹ đạo 3D hoặc thông số vật liệu.

Audio và phụ đề ASR của pilot đã truy xuất/băm; **chưa nghe trực tiếp hoặc đồng bộ audio thủ công**. ASR chỉ hỗ trợ định vị. Review thủ công ở đây là Codex kiểm ảnh; có review AI thứ hai nhưng không có người chú giải độc lập được hiệu chuẩn, blind review hoặc phân bố lỗi reviewer.

## 4. Phân tích chi tiết #01372 — 16/07/2026

Nguồn: [IUU05082QtE](https://www.youtube.com/watch?v=IUU05082QtE). Source SHA256: `c4740a0cbe28ea595ebb39487629a50b5bc8c7c88d91f777a4731660e07bce9c`. Bản này là rendition công khai; chưa xác thực camera master hoặc serial của thiết bị.

### Ranh giới và chuẩn bị

`evidence/pilot_boundary_review.json` phân biệt ranh giới yêu cầu với những trạng thái thực sự thấy được. Kết thúc kiểm tra được ASR chỉ dẫn khoảng 1013–1020 s, cùng chuyển người nói/bối cảnh; **không có timestamp kết thúc thao tác vật lý đã xác nhận**. Không nhận dạng được sự kiện lựa chọn bộ bóng hoặc ball-set ID.

Thao tác sắp xếp/nạp trên giá được thấy trong span **1045,044000–1061,860800 s**. Hai đầu là phạm vi quan sát, không phải duration nạp đủ 55 bóng. Lần đầu cận cảnh đã có thao tác đang diễn ra; không chứng nhận mốc nạp đầu/cuối và từng ID bị che.

Sau cảnh nút điều khiển, PTS **1088,087000** đã thấy bóng rời giá; cặp native đến **1088,120367** thấy chuyển động. Onset trộn/nhả đầu tiên bị cắt cảnh, chỉ giữ cận phải và ảnh bối cảnh, không thay bằng lúc đặt tay hoặc ASR yêu cầu bấm nút. Tương tự, thấy rotor đứng và bóng lắng trong các mẫu sau quay không xác định được thời điểm stop command/deceleration. Kết thúc thủ tục quay chính thức vẫn NA; chuyển đồ họa sang sản phẩm khác là sự kiện chương trình riêng.

### Bảy lần thu: cận proxy vật lý nhìn thấy

| Lần | Vai trò | PTS leading-edge ra ramp, s | Số khoảng frame encoded | Cô lập thật / control onset |
|---:|---|---:|---:|---|
| 1 | Main | 1115,214100–1115,247467 | 1 | NA / NA |
| 2 | Main | 1127,326200–1127,359567 | 1 | NA / NA |
| 3 | Main | 1140,606133–1140,639500 | 1 | NA / NA |
| 4 | Main | 1153,018533–1153,051900 | 1 | NA / NA |
| 5 | Main | 1166,665500–1166,698867 | 1 | NA / NA |
| 6 | Main | 1179,811967–1179,878700 | 2 | NA / NA |
| 7 | Special | 1193,959433–1193,992800 | 1 | NA / NA |

`capture_event_audit.csv` giữ đủ sáu trạng thái riêng cho từng lần; `official_draw_events.csv` thêm source, ảnh/hash, cận và missingness. Năm onset của cơ cấu ngoài có cặp ảnh; onset lần 1 và 6 bị camera che/cắt. Bóng đầu **đã nằm ở hộp trên tại 1114,213100**, nên onset/entry không được đặt ở lúc ảnh thu nhỏ mới thấy nó. Sáu lần còn lại có cận first-clear visibility; đó vẫn không chứng minh thời điểm vượt mặt phẳng chọn sâu bên trong.

Lần 6 cận cảnh đã thấy cơ cấu mở; chuyển động sau đó không là onset ban đầu. Các sửa sai từ preview giữ trong `native_refinement.json`; coarse review trước đó vẫn được lưu. Special ở vị trí dừng bên phải khác nhóm sáu bóng; không mặc định cùng đường lăn cuối rãnh. Overlay special bắt đầu đọc rõ trong cận 1197,029167–1197,129267, sau khi mở rộng review; file review coarse trước đó chỉ kết luận right-censored.

### Đo tay gạt trên phần chính thức

ROI khóa `(480,80,900,900)`, tâm ảnh `(932,525)`, annulus 130–350 px. Không tìm được marker vật liệu duy nhất. Không unwrap thành góc vật lý hoặc mặc định ba tay cùng trục/tốc độ.

Flow tiếp tuyến có median gần zero trong khi template shift nhảy và có median 15° ảnh/frame; nền tối/đứng yên và tay trong suốt gây chi phối. Masked spectrum/autocorrelation bị **từ chối** vì một sector ở frame 51 bị loại hết, tạo coefficient thiếu; không nội suy. Unmasked spectrum có peak 3,596368 Hz, bin 0,199798 Hz; reciprocal của autocorrelation lag khoảng 3,7462 Hz nằm trong một bin của nó. Sự tương thích đó là trên cùng tín hiệu ảnh, không là cross-validation độc lập về RPM.

24/149 cặp có mean absolute gray difference dưới 1/255, nhiều cặp lặp nhịp khoảng 0,2002 s. Đây là near-duplicate candidates, không phải khẳng định bit-identical toàn frame hoặc chứng minh camera quay 25 FPS. Không xóa/đổi thời gian các frame. Uniform PTS không đảm bảo mỗi sample là một hình chuyển động mới độc lập.

## 5. Đối chiếu #01373–#01376

Định nghĩa, ROI motion và quality gates khóa trong `locked_protocol.json` trước các phép đo đối chiếu. Các input có thể được cache trước khi pilot hoàn tất; phân tích đối chiếu bắt đầu sau native refinement pilot. Chỉ dùng bốn kỳ đã chỉ định, không tăng bộ video.

| Kỳ / ngày liên kết | Seven downstream proxies | Mean midpoint của 5 khoảng main, s | Motion transfer |
|---|---:|---:|---|
| 01372 / 16-07 | 7 | 12,923 | Pilot; physical RPM NA |
| 01373 / 18-07 | 7 | 13,327 | Từ chối: zoom khác, khoang bị clip |
| 01374 / 21-07 | 7 | 13,040 | Từ chối: tâm/scale khác, bóng xanh làm yellow mask chưa hợp lệ |
| 01375 / 23-07 | 7 | 13,921 | Từ chối: phóng lớn hub/khoang |
| 01376 / 25-07 | 7 | 13,567 | Từ chối: vị trí tâm và scale khác |

Cả 28 cặp ra ramp được kiểm native, cận tối đa 0,133467 s, qua mục tiêu định vị 0,2002 s. ROI xem sự kiện được đổi theo camera và ghi rõ; **ROI tính motion không được recenter/retune**. Vì không qua gate tương đương camera, không chạy lại motion ở một ROI khác rồi gọi đó là replication của phép đo cũ. Không có bốn xác nhận RPM vật lý.

Overlay ở bốn kỳ chỉ có cận 2,002 s từ overview, **không đạt** mục tiêu 0,2002 s; được ghi riêng và không dùng làm capture clock. Một số onset cơ cấu/collector first visibility vẫn NA hoặc chỉ có preview spacing 0,2002 s, yếu hơn native ramp review. Có một sửa sai empty→empty của collector #01374 lần 6; canonical JSON và derived CSV dùng 1171,904067–1172,104267, bản cũ được giữ dưới tên `pre_correction`.

Các proxy ở góc khác không tự bảo đảm cùng một mặt phẳng 3D đã hiệu chuẩn. Mean của năm draw-level means là 13,355 s, SD giữa các means 0,404 s, **chỉ mô tả**. 25 khoảng main không được gọi là 25 kỳ; 5 khoảng sang special tách riêng. Không có p-value, CI suy luận hoặc kết luận timer cố định từ năm kỳ khám phá này.

## 6. Kiểm toán hai candidate RPM cũ

PTS 857,022833–860,993467 thuộc kiểm tra vận hành, không là quay chính thức. Phase slope = 63,789049874; real-signal spectrum = 94,904146812 candidate RPM. Tỷ số 1,487781163 gần 3/2 chỉ là số học; cùng h=3 chia cho cả hai thì tỷ số không đổi. Không đổi riêng divisor để ép khớp.

Giả sử h=3 thật, alias spacing khoảng 599,395 RPM; chưa có bound tốc độ độc lập để chọn nhánh. Cộng/trừ nhánh đơn giản không làm hai tần số tổng hợp đồng nhất. Cửa sổ 60 frame đầu/cuối cho các candidate rất khác; cửa sổ chồng nhau không độc lập.

Kiểm provenance mới tái tạo đúng toàn bộ 120 buffer/PTS. Trong chính input đó, scale/framing camera đổi rõ: bề rộng plate giữa có các khoảng manual thô khoảng 175–210 xuống 117–143 px ở preview cùng độ rộng 640. Đây không phải CI hoặc calibration. ROI annulus cố định lấy tín hiệu từ các vị trí vật liệu khác nhau. Nhiễu bóng, mask động, blur, phối cảnh, harmonic và alias vẫn chưa tách thành nguyên nhân định lượng riêng. Giữ **RPM NA**. Chi tiết và fixture counterexample nền tĩnh/mask quay: `evidence/legacy_rpm_audit.md`, `legacy_camera_review.md` và `legacy_crop_hash_comparison.json`.

## 7. H1–H5

| Giả thuyết | Kết quả Phase 2 |
|---|---|
| H1: pha tay gạt tại thu ổn định | Không kiểm định: không có góc vật lý và isolation/selection time đã xác nhận. |
| H2: chu kỳ trộn/thu lặp | Mô tả được downstream cadence theo 5 kỳ; timing trộn/chọn thật còn thiếu. Không chấp nhận/bác bỏ mô hình timer. |
| H3: mật độ gần cửa khác toàn khoang | Không kiểm định: detector/visibility mask/độ sâu chưa được kiểm định; mask ảnh không là mật độ bóng. |
| H4: vị trí nạp ảnh hưởng lựa chọn | Không kiểm định: thiếu chuỗi ID/initial state và can thiệp có kiểm soát. |
| H5: bộ bóng/cấu hình đổi chuyển động | Không kiểm định: khác màu/camera không xác nhận vật liệu, serial hoặc nhóm đối chứng tương đương. |

## 8. Sai lệch, thất bại và giới hạn

Giữ `evidence/failed_attempts.csv` và log gốc: IPv6 chậm, trích rỗng vì thời lượng/PTS, bản copy bị dừng không có moov, tải tuần tự quá bound; chỉ input byte-range đủ content length/SHA mới được dùng. Các lỗi UTF-8, preflight dependency, preview thiếu bóng, onset do cut, missing coefficient và geometry transfer cũng được ghi. Không có frame AI hoặc video tổng hợp làm thực nghiệm.

Một audit cuối phát hiện cận chuẩn bị ghi 1045,044200 trong khi locator thật là 1045,044000. Đã sửa canonical boundary/derived table, giữ snapshot cũ và bổ sung kiểm PTS-bound binding. Chênh 0,0002 s không đổi kết luận nhưng vẫn được sửa để provenance nhất quán.

Các giới hạn lớn hơn độ phân giải PTS gồm exposure/blur, held pictures, khúc xạ, occlusion, cut, điểm mép được chọn bởi reviewer và thiếu hình học. Không có ground truth độc lập để báo accuracy hoặc CI. Bản phát public có thể đổi/rời mạng; **nếu hash không khớp phải dừng so sánh**, không gọi re-encode là thay đổi vật lý.

## 9. Quyết định GO / LIMITED / NO-GO

**NO-GO** cho mô phỏng 3D có thể hiệu chuẩn, xác nhận động lực học hoặc dự đoán số. Khả năng hiện tại giới hạn ở các phép đo trạng thái nhìn thấy/mô tả cadence và mô hình định tính có giả định. `simulation_readiness.md` trả lời riêng cả tám câu hỏi; `unresolved_parameters.md` nêu tham số và dữ liệu cần có.

## 10. File và lệnh tái lập

Các file bắt buộc đều nằm trong thư mục này: handoff hiện tại, `phase2_sources.csv`, `official_draw_events.csv`, `capture_event_audit.csv`, `paddle_motion.csv`, `rpm_cross_validation.csv`, `phase2_hypothesis_results.csv`, `observability_matrix.csv`, `simulation_readiness.md`, `unresolved_parameters.md`, `validation_report.json`, và `evidence/`, `charts/`, `scripts/`.

`DATA_DICTIONARY.md` mô tả NA, proxy, native/reduced và uncertainty. `evidence/event_frame_manifest.csv` ánh xạ alias ảnh bàn giao sang ảnh review, source PTS, crop và SHA. Một số PNG xem thừa chỉ ở local; contact sheets và alias sự kiện được giữ. Source video/audio giữ ngoài Git ở `C:/vietlott-research-output/phase2-inputs/`; input SHA nằm trong source CSV/JSON. Code phân tích thuộc commit cuối trên branch; mỗi lần chạy giữ thêm hash script, base commit và phiên bản runtime, không giả vờ script mới đã tồn tại trong base Phase 1. Audit legacy đã lưu runtime 3.14 riêng; xử lý video/test cuối dùng Python 3.12.13 và các package được pin trong `evidence/runtime_versions.json`.

Từ `C:/vietlott-research-repo/vietlott-power655-physical-research/`:

```powershell
$py = 'C:\vietlott-power655-env\Scripts\python.exe'
& $py phase2/scripts/download_source.py IUU05082QtE --out 'C:\vietlott-research-output\phase2-inputs-new' --ranges --audio-captions
& $py phase2/scripts/inspect_local.py 'C:\vietlott-research-output\phase2-inputs\IUU05082QtE_f137_ranges.mp4' --tag reproduce_new_pilot --start 1114.2 --duration 1.5 --every 1 --crop 1500 60 420 650 --native --width 280 --cols 4 --rows 3
& $py phase2/scripts/rpm_audit.py --validate-only
& $py -m unittest discover -s scripts -p test_pipeline.py -v
& $py -m unittest discover -s phase2/scripts -p 'test_*.py' -v
```

Dùng tên output/tag mới vì các trích/raw review từ chối ghi đè. `source_<id>_ranges.json`, mọi `extraction.json`, protocol và scripts annotation chứa argument đầy đủ cho bốn nguồn còn lại. `build_results.py --refresh-derived` chỉ tái tạo bảng dẫn xuất từ canonical review, không sửa Phase 1 hoặc raw review; alias khác nội dung được version hóa. `validate_phase2.py` từ chối ghi đè validation: lưu snapshot cũ hoặc dùng checkout/output mới trước khi tái chạy. `validation_report.json` tách kiểm phần mềm/integrity khỏi scientific readiness; synthetic pass không xác nhận máy thật.

Hai chart standalone đã xem kiểm bố cục: `charts/pilot_motion_image_diagnostics.png` và `charts/visible_cadence.png`. Danh sách hash artifact bàn giao nằm trong `artifact_manifest.csv`; manifest không tự băm chính nó.

## 11. Bước tiếp theo theo thứ tự ưu tiên

1. Xin master không cắt cảnh, serial/CAD của máy và ball-set ID/log đo đúng kỳ; xác nhận quyền nghiên cứu và dữ liệu thiết bị.
2. Camera toàn khoang + cận cửa timecode chung, exposure ngắn, log control/gate, encoder/tachometer; xác định mặt phẳng cô lập và độ trễ thật.
3. Marker vật liệu duy nhất, calibration có khúc xạ/phối cảnh và bound tốc độ độc lập; giải alias trước khi báo RPM.
4. Nhiều góc đồng bộ và kiểm ID xuyên occlusion/collision bằng nhãn độc lập; đo khối lượng, friction, restitution và hình học.
5. Chỉ khi các điều kiện nhận dạng qua gate mới hiệu chuẩn mô hình và kiểm trên kỳ/cấu hình chưa dùng fit. Không tiếp tục tăng số bản phát cùng hạn chế để tạo cảm giác đủ dữ liệu.
