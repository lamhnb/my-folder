# H1–H5: thiết kế kiểm định và kết quả hiện tại

Mọi dữ liệu đã xem thuộc **khám phá**, không phải tập kiểm định độc lập. Tài liệu này là kế hoạch cho nghiên cứu tiếp theo, không được gọi là preregistration trước các video đã xem. Không sử dụng số kết quả để tinh chỉnh mô hình chuyển động hoặc chọn tham số ảnh. ASR và kết quả chỉ hỗ trợ định vị đúng phase; chúng không là oracle vật lý.

| Giả thuyết | Cần quan sát | Thiết kế và giới hạn | Hiện tại |
|---|---|---|---|
| H1: pha gạt tại thu ổn định | Góc vật lý đã hiệu chuẩn, marker/đối xứng xác minh, cùng định nghĩa capture | Circular concentration; kiểm định bằng hoán vị/shift thời điểm trong cùng pha trộn; block theo kỳ. Xử lý h=3 chỉ khi có bằng chứng cơ khí. 7 bóng không là 7 kỳ độc lập. | Không kiểm định: RPM/pha vật lý và capture phase chưa có |
| H2: thời gian trộn/thu lặp | Onset PTS từng kỳ, cận khi khuất, ID máy và phase chính thức | So sánh phân bố thời gian, CV và CI bootstrap theo kỳ; dùng mô hình interval-censored cho cận. Tách trộn trước bóng 1, giữa bóng và trước special. | Chỉ có định vị/lấy mẫu; chưa có bộ sự kiện đủ 5 kỳ kiểm từng frame |
| H3: vùng gần cửa khác toàn khoang | Detection validation, hiệu chuẩn/visibility mask, ROI cửa khóa trước | Mật độ theo diện tích quan sát và thời gian; block permutation, không coi hàng trăm frame tương quan là độc lập. So sánh trong cùng góc camera, không dùng heatmap thiếu không ngẫu nhiên làm xác suất toàn khoang. | Không kiểm định: 109 candidate từ 4 s của phần kiểm tra, chưa có nhãn/recall |
| H4: vị trí nạp còn ảnh hưởng lựa chọn | ID từng bóng từ nạp xuyên trộn tới cửa; nhiều lần nạp có kiểm soát | Thí nghiệm được chủ thiết bị cho phép; ngẫu nhiên hóa thứ tự/vị trí, khóa mixer settings; kiểm định độc lập đã định trước. Dữ liệu broadcast một góc không đủ chứng minh quan hệ nhân quả. | Không kiểm định: mất danh tính/độ sâu và initial state |
| H5: bộ bóng/cấu hình thay đổi chuyển động | ID bộ, machine serial, calibration, nhiều kỳ mỗi cấu hình | Thiết kế phân tầng và mixed-effects; tách khác camera/ánh sáng khỏi khác vật lý; xác nhận trên cấu hình/kỳ chưa dùng fit. Màu khác không tự chứng minh vật liệu/khối lượng khác. | Có khác màu nhìn thấy giữa đoạn; chưa có ID hoặc nhóm so sánh đủ |

Không tính p-value hoặc CI của thiên lệch từ các đầu vào thiếu trên. `hypothesis_results.csv` ghi `not_testable`, p_value=NA. Điều này không phải bác bỏ hoặc chấp nhận H1–H5.

H1/H2 có thể phản ánh timer và chu kỳ cơ cấu vốn được lập trình, dù bóng được trộn công bằng. H3 có thể phản ánh trọng lực/hình học/visibility. Cả ba không tự chứng minh xác suất số khác nhau. Muốn đánh giá thiên lệch xác suất cần mô hình đo đã xác nhận, ID bóng/bộ, null cơ học hợp lý và tập kiểm định độc lập với số mẫu được phân tích power trước.

Kế hoạch tiếp: khóa định nghĩa sự kiện, calibration và detector trên một pilot; băm và lưu cấu hình; chọn trước tập tối thiểu 10–20 kỳ khác, không xem kết quả khi chọn tham số; dùng reviewer thứ hai chú giải ngẫu nhiên các capture và báo độ lệch PTS. Nếu detector/alias chưa qua kiểm định, dừng suy luận cơ học thay vì tăng số lượng video thiếu khả năng quan sát.
