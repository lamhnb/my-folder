# Những tham số chưa được nhận dạng

`NA` là chưa biết, không phải 0, giá trị danh định hoặc một tham số mặc định có thể đưa vào mô hình.

| Nhóm | Tình trạng sau Phase 2 | Vì sao dữ liệu hiện tại không đủ | Dữ liệu ưu tiên |
|---|---|---|---|
| Định danh máy/bộ bóng | Model, serial, revision, ball-set ID: NA | Không đọc được nhãn liên kết đúng kỳ; màu và hình dáng không xác nhận serial/vật liệu | Hồ sơ chủ thiết bị, ảnh nhãn và biên bản từng kỳ |
| Hình học | Khoang có chiều sâu; kích thước, paddle clearance, đường cửa: NA | Một ảnh phối cảnh qua mặt trong suốt không cho kích thước thật/depth và topology duy nhất | CAD/đo có vật chuẩn, intrinsics/extrinsics, refraction |
| Trục và tay gạt | Có ba dạng tay tương tự trên ảnh; số trục và góc tương đối vật lý: NA | Chưa có marker vật liệu duy nhất hoặc bản vẽ; không mặc định cùng trục/cùng tốc độ | CAD/topology, vận hành chậm và marker được phép |
| Góc, tốc độ, chiều | Vật lý: NA; các tín hiệu ảnh lưu riêng | Đối xứng, alias, blur, bóng và nền; camera/scale thay đổi; không có bound tốc độ ngoài | Encoder/tachometer + timecode và camera exposure ngắn |
| Capture | Chuỗi giữ/nhả và bóng ra ramp nhìn thấy; thời điểm cô lập thật NA | Mặt phẳng chọn, tính một chiều và trạng thái chốt sâu bị che/chưa biết | Cận cửa liên tục + bản vẽ + control/gate logs |
| Điều khiển | Tiếp xúc tay/nút đôi khi thấy; onset lệnh điện và latency NA | Bấm nút, đèn sáng, cơ cấu bắt đầu và lời công bố là các mốc khác nhau | Log tín hiệu đồng bộ với master |
| Bộ bóng | Đường kính/khối lượng/tâm khối thực và dung sai NA | Không thể cân hoặc đo tâm khối từ màu/số trong video | Đo từng serial với sai số thiết bị |
| Vật liệu | Friction/restitution/rolling resistance/damping NA | Chuyển động chiếu bị che có nhiều nghiệm cơ học; không có thí nghiệm va chạm độc lập | Thí nghiệm với mẫu/vật liệu thật được phép |
| Trạng thái ban đầu | ID/vị trí/vận tốc 3D của 55 bóng NA | Sắp xếp bằng tay bị che; không đọc xuyên suốt toàn bộ ID qua trộn | Nhiều camera đồng bộ, nhận dạng có kiểm định |
| Thời gian camera | 30000/1001 là FPS rendition; camera-original FPS và exposure NA | PTS đều vẫn có ảnh gần lặp; upstream processing chưa biết | Camera master và log/drop-frame/timecode |
| Đồng bộ | Audio/camera/graphic latency thực NA | Audio đã lấy cho pilot nhưng chưa nghe/đồng bộ thủ công; ASR chỉ định vị | Nghe/kiểm độc lập và tín hiệu đồng bộ; master |
| Tính lặp lại | Có thể mô tả khoảng giữa các proxy nhìn thấy | Đây là downstream transport trong broadcast; không xác minh timer chọn bóng hoặc cùng serial | Các mốc vật lý đúng định nghĩa, nhiều kỳ có ID máy/bóng |

Tăng số lượng video thiếu những dữ liệu trên không tự làm các tham số trở nên nhận dạng được. Phần mềm tổng hợp chỉ kiểm logic xử lý PTS/alias/missingness, không cung cấp các thông số thật này.
