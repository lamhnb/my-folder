# Phase 2: schema và cách diễn giải

CSV dùng UTF-8, dấu phẩy, `NA` cho missing. Chữ số thập phân của PTS không là sai số vật lý ở microsecond. Mọi point timestamp sự kiện giữ NA: cận mô tả chuyển trạng thái nhìn thấy giữa frame.

| File | Nội dung và giới hạn |
|---|---|
| phase2_sources.csv | Năm URL, rendition, FPS/timebase, SHA256 toàn input đã tải, audio/caption pilot và bản ffmpeg. Full download khác full decode; chỉ những đoạn ghi trong evidence đã được phân tích. Media gốc giữ local ngoài Git. |
| official_draw_events.csv | Từng sự kiện/loại trạng thái; `lower_pts_seconds`, `upper_pts_seconds` có thể chỉ có một cận hoặc đều NA. `timestamp_seconds` và `physical_accuracy_frames` NA. `data_class` tách graphic khỏi observation_visibility_only. |
| capture_event_audit.csv | Bảng rộng bảy lần thu mỗi kỳ × sáu trạng thái bắt buộc; không biến các ô NA thành sự kiện đã đo. Capture 7 là special, khác nhóm sáu main. |
| paddle_motion.csv | Năm hàng **khả năng quan sát**, không có hàng góc/RPM vật lý được chấp nhận. Các số optical flow/template không được đưa vào trường góc tay gạt. |
| rpm_cross_validation.csv | Kiểm toán scalar Phase 1; các cửa sổ và phương pháp trên cùng tín hiệu không độc lập. Physical RPM NA. |
| phase2_hypothesis_results.csv | H1–H5 và điều kiện đầu vào; missing không chấp nhận/bác bỏ giả thuyết. H2 có mô tả cadence nhìn thấy, không là kiểm định timer chọn bóng. |
| observability_matrix.csv | Tách đại lượng đo số trên ảnh, estimate, assumption và unknown; ghi dữ liệu cần bổ sung. |
| evidence/native_refinement.json | Kiểm frame native pilot, có sửa sai từ preview và thiếu onset khi camera cắt. Manual là Codex kiểm ảnh; không phải người chú giải có calibration. |
| evidence/pilot_independent_review.json | Review thứ hai bằng AI trên ảnh thu nhỏ; giữ như lịch sử, bị native_refinement thay thế ở các chỗ có sửa. Không là cảm biến hoặc tập kiểm định độc lập. |
| evidence/replication_*.json | Review từng kỳ theo protocol khóa; tham chiếu trước/sau/crop và camera quality gates. |
| evidence/event_frame_manifest.csv | Alias PNG trước/sau được bàn giao, hash bytes, ảnh native hay reduced và crop/scale. Tham chiếu ảnh nguồn local nằm trong ledger trích. |
| evidence/*/frames.csv | Mọi sample được trích ở lần chạy, source PTS và hash; `relative_native_index` là chỉ số tương đối từ frame đầu của đoạn seek. Không là global frame index. Preview PNG thừa có thể chỉ ở local; contact sheet và các alias sự kiện được giữ trong Git. |
| evidence/*/extraction.json | Nguồn input, SHA, crop/scale, sampling, ffmpeg và code hash. Đọc `native_pixels` trước khi diễn giải độ phân giải ảnh. |
| evidence/pilot_motion/*.csv | Các tín hiệu ảnh native và chẩn đoán; không là quỹ đạo vật liệu hoặc xác suất chọn bóng. Chỗ mất coefficient không được nội suy. |
| evidence/visible_cadence_*.csv | Hiệu hai interval PTS: [a,b]−[c,d]=[a−d,b−c]. Midpoint chỉ để mô tả; không dùng midpoint như timestamp chính xác. Independent unit là kỳ. |
| validation_report.json | Kiểm integrity/schema/protected diff/software. Passing software không chứng nhận phép đo vật lý hoặc GO mô phỏng. |

`trough_entry_visible_proxy` là tên cố định trong protocol: leading edge bóng rời miệng cơ cấu xuống ramp/kênh kết quả phía sau. Mặt phẳng 3D và thời điểm chọn bóng vẫn không biết. Không trộn proxy này với bóng nằm yên ở cuối rãnh, xuất hiện số, hoặc permanent isolation.

Sai số được tách: (1) khoảng định vị trên encoded PTS; (2) blur/exposure/held pictures; (3) che khuất/cắt cảnh; (4) hiệu chuẩn/phối cảnh; (5) khác biệt reviewer. Chỉ (1) có thể ghi con số từ các cặp frame ở đây. Không có phân bố lỗi reviewer hay camera clock đã được đo để gọi đó là CI hoặc accuracy.
