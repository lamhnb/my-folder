# Tham số còn thiếu và dữ liệu cần bổ sung

`NA` không phải giá trị mặc định để đưa vào mô phỏng. Các giá trị văn bản lịch sử nằm riêng trong equipment_research.md.

| Nhóm | Chưa biết | Bằng chứng cần có |
|---|---|---|
| Định danh | Hãng, model, serial, revision, lịch thay máy | Nhãn máy + hồ sơ chủ thiết bị + liên kết kỳ/serial |
| Khoang | Đường kính trong, chiều sâu, độ dày acrylic, sai lệch cầu | CAD/bản vẽ hoặc đo trực tiếp có vật chuẩn |
| Tay gạt | Chiều dài, tiết diện, độ cong, khe hở, góc tương đối, số trục | CAD; video tĩnh nhiều góc; vận hành chậm được phép |
| Trục/động cơ | Hướng trục, RPM thật, điều tốc, biến thiên tải, độ rơ | Encoder/tachometer độc lập, log động cơ đồng bộ |
| Thu bóng | Cửa chọn/giữ/nhả khác nhau; hành trình, ngưỡng, timing và độ trễ | Camera close-up đồng bộ + tín hiệu điều khiển và bản vẽ |
| Rãnh/hiển thị | Góc dốc, tiết diện, chốt chặn, bề mặt | Đo trực tiếp; ảnh hiệu chuẩn trước/sau |
| Bộ bóng | ID bộ, serial từng bóng, lịch thay, màu/số, tình trạng bề mặt | Biên bản dùng bộ bóng theo từng kỳ; ảnh nhận dạng tĩnh |
| Mỗi bóng | Khối lượng thật, đường kính theo nhiều trục, tâm khối, độ tròn | Bảng cân/đo của chính bộ đã dùng, với sai số thiết bị |
| Vật liệu | Mật độ, đàn hồi theo vận tốc, ma sát tĩnh/động/lăn, damping | Thí nghiệm va chạm và mặt nghiêng trên mẫu được phép |
| Môi trường | Nhiệt độ, ẩm, tĩnh điện, bụi, rung nền | Cảm biến/log và quy trình kiểm soát |
| Nạp | Thứ tự thật, tọa độ/độ cao/vận tốc ban đầu, thời điểm cửa | Camera có thể đọc ID toàn bộ quá trình, không cắt cảnh |
| Camera | Intrinsics/extrinsics, shutter, rolling shutter, refraction | Calibration grid, tiêu cự/zoom, thời gian phơi sáng |
| Đồng bộ | Độ lệch camera/audio/overlay, dropped/duplicate frames | Timecode chung, đèn đồng bộ, master recording |
| Quan sát 3D | Depth và ID khi bóng chồng nhau, va chạm khuất | Ít nhất 2–3 camera đồng bộ, góc giao nhau đủ lớn |
| Thời gian | Onset/offset mỗi hành động trong kỳ chính thức | Review liên tiếp frame native, không thay bằng ASR/overlay |
| Quyền | Quyền lưu master video, stills và chuyển cho researcher | Xác nhận từ chủ quyền hoặc license áp dụng cụ thể |

Ưu tiên đầu tiên: master liên tục góc cố định, quyền nghiên cứu rõ, nhãn phase kiểm tra/chính thức, ID máy/bộ bóng, video close-up cửa và một phép đo RPM độc lập. Sau đó mới thiết kế chiến dịch 120–240 fps với shutter ngắn và ánh sáng đủ. Tốc độ FPS cần chọn theo RPM thật và số chi tiết lặp; 240 fps không tự loại bỏ mọi alias hoặc blur.

Không thể xác định duy nhất các tham số va chạm từ một quỹ đạo chiếu 2D bị che khuất. Một mô hình tái tạo hình thức hình ảnh vẫn có thể có thông số vật lý và xác suất chọn khác thực tế. Cần kiểm định trên các kỳ/cấu hình chưa dùng hiệu chuẩn.
