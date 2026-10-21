# Quyết định kỹ thuật: NO-GO cho mô phỏng 3D có thể hiệu chuẩn

Phạm vi quyết định là mô hình động lực học của thiết bị trong các bản phát tháng 07/2026, có thể hiệu chuẩn và kiểm định bằng dữ liệu. Các ảnh đủ cho một số phép đo thời gian **trạng thái nhìn thấy** và một mô hình minh họa định tính với giả định công khai. Khả năng đó không đáp ứng mục tiêu hiệu chuẩn 3D. Quyết định này không khẳng định mọi video khác hoặc dữ liệu trực tiếp từ máy đều bất khả dụng.

| Câu hỏi | Trả lời dựa trên dữ liệu Phase 2 |
|---|---|
| 1. Góc tay gạt, sai số bao nhiêu độ? | Góc vật lý và sai số thực nghiệm: **NA**. Không có marker vật liệu duy nhất hoặc hiệu chuẩn mặt phẳng quay. Đối xứng ba tay chỉ là giả thuyết ảnh; nếu đúng, các nhánh pha cách 120° vẫn chưa được phân biệt. Đây không phải sai số ±120° đã đo. |
| 2. RPM vật lý hay candidate? | **RPM vật lý NA**. Hai candidate cũ 63.789/94.904 tái tính được nhưng không qua kiểm định danh tính. Đoạn chính thức có optical flow, template, autocorrelation và spectrum ảnh; không chuyển tần số ảnh thành tốc độ máy. |
| 3. Thời điểm cô lập bóng, chính xác bao nhiêu frame? | **NA**, chưa nhận dạng được mặt phẳng ngăn cách không thể quay lại. Bảy lần rời miệng cơ cấu xuống ramp có cận ảnh ở 1–2 khoảng frame encoded trong pilot; đó là độ phân giải định vị một proxy ở phía sau cơ cấu, không phải độ chính xác thời điểm chọn/cô lập bóng. |
| 4. Trạng thái cửa thu? | Nhìn thấy phần tử ngoài thay hướng, giữ bóng và nhả bóng ở một số góc. Không xác định đầy đủ cửa/chốt sâu bên trong, tín hiệu điện, ngưỡng hoặc trạng thái đóng kín. Không gán một biến gate_open vật lý từ toàn bộ ảnh hộp. |
| 5. Theo dõi một bóng trước/sau va chạm? | Không có chuỗi danh tính đã kiểm định xuyên trộn, chồng hình và va chạm. Có thể nhìn bóng đã rời cơ cấu và đọc số khi đứng yên; điều đó không nối ngược được đến trạng thái ban đầu. Không có quỹ đạo 3D. |
| 6. Đủ hiệu chuẩn mô hình 3D? | **Không**: thiếu hình học có kích thước, topology trục/cửa, RPM độc lập, chiều sâu, ID và initial state từng bóng, thông số va chạm/ma sát. Nhiều bộ tham số khác nhau có thể tạo ảnh chiếu tương tự. |
| 7. Tham số nào không suy ra duy nhất từ các video đã xem? | Serial/revision, kích thước thật/độ sâu, tọa độ 3D, góc vật liệu tuyệt đối, nhánh alias, shutter và xử lý frame trước YouTube; khối lượng/tâm khối/ma sát/restitution riêng từng bóng; topology và độ trễ điện/cơ khí bên trong; thời điểm cô lập thật. Danh mục chi tiết: unresolved_parameters.md. |
| 8. Thêm video hay dữ liệu trực tiếp? | Ưu tiên dữ liệu trực tiếp và nguồn master liên tục đồng bộ. Thêm bản phát cùng góc cắt cảnh không giải quyết tính không xác định về độ sâu, vật liệu hoặc danh tính. |

## Căn cứ dừng hiệu chuẩn

`evidence/native_refinement.json` giữ cận ảnh của bảy chuỗi thu; hai onset bị cắt cảnh và mọi thời điểm cô lập thật vẫn thiếu. `evidence/pilot_motion/interpretation.md` ghi một lần chạy đã khóa trên 150 frame thật: marker không xác nhận, optical flow gần zero trong khi template nhảy pha, masked coefficient bị thiếu vì một sector bị loại hết, và ảnh gần lặp ở 24/149 cặp. Sai số thời gian phơi sáng và đồng bộ camera/overlay chưa được đo. Đồng thuận tương đối của autocorrelation và spectrum **trên cùng tín hiệu ảnh** không là cảm biến độc lập.

`evidence/legacy_rpm_audit.md` giữ nguyên bất đồng hai candidate. Kiểm tra framing bổ sung nằm trong `evidence/legacy_camera_review.json` nếu có; nó không tự xác định nguyên nhân duy nhất. Các kỳ lặp kiểm khả năng chuyển phương pháp, không cung cấp encoder hoặc vật chuẩn còn thiếu.

## Điều kiện mở lại GO

1. Xác minh serial, CAD/kích thước và hình học cửa; lấy ID và bảng cân/đo đúng bộ bóng.
2. Có master không cắt cảnh, camera toàn khoang và cận cửa dùng chung timecode; ghi exposure, dropped/held frames và tín hiệu điều khiển.
3. Dùng encoder/tachometer hoặc marker duy nhất có tốc độ giới hạn độc lập để giải nhánh alias; không dùng giới hạn tự suy từ unwrap.
4. Ít nhất hai góc đã hiệu chuẩn và đồng bộ; nhãn ID/occlusion được người kiểm tra độc lập đánh giá, không nội suy qua vùng khuất.
5. Đo thông số va chạm/ma sát trên thiết bị hoặc mẫu được phép, khóa mô hình và đánh giá trên các kỳ/cấu hình chưa dùng hiệu chuẩn.

Không xây simulator dự đoán hoặc chỉnh các thuật toán xổ số từ dữ liệu không đủ nhận dạng này.
