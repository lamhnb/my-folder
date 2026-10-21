# Quy trình, định nghĩa và sai số

## Nguồn thời gian

`source_pts_seconds` là PTS của frame trong rendition YouTube, lấy từ ffmpeg `showinfo` với `-copyts`. Nó không phải đồng hồ hiện trường hoặc thời điểm lời nói. Mốc này liên kết bằng video ID + format ID + phiên bản ffmpeg. Một số luồng có offset PTS và xấp xỉ 30000/1001 fps, dù metadata ghi 30. Không tính thời gian bằng `frame/30`.

`frame_index` toàn video là NA vì chưa đối chiếu toàn bộ bảng PTS/frame count. `clip_frame_index` là chỉ số 0-based trong đoạn giải mã, có thể xác minh bằng lệnh đã lưu. Với file local hợp lệ, `extract_frames.py` giải mã tuần tự toàn video và đối chiếu số frame với ffprobe, rồi mới gán chỉ số toàn file.

Timestamp hiển thị sáu số lẻ phản ánh cách ffmpeg xuất PTS, không phải độ chính xác sự kiện ở microsecond. Một frame native khoảng 33,37 ms trong đoạn 2026 đã kiểm tra. Lấy mẫu mỗi 150 hoặc 300 frame tạo khoảng hở khoảng 5,005 hoặc 10,010 s; không thể khẳng định sự kiện xảy ra đúng tại mẫu đầu tiên nhìn thấy.

## Phân đoạn và kiểm tra thủ công

Những ảnh máy đang chạy, bóng trên giá nạp hoặc bóng trong rãnh được ghi là **trạng thái quan sát**, không đổi tên thành sự kiện bắt đầu/trúng/thu bóng. Camera close-up người bấm nút không xác nhận cửa thu đã mở. Overlay kết quả và lời công bố không thay thế frame cơ cấu thu. `manual_observations.csv` lưu nhận xét của một người kiểm tra (Codex), chưa có người kiểm tra độc lập thứ hai.

Mỗi sự kiện cần hai frame kề nhau trước/sau chuyển trạng thái, hoặc khoảng bị che/cắt cảnh. Trường hợp bị che: ghi hai cận PTS, giữ timestamp sự kiện là NA. Cửa thu mở/đóng, bóng rời vùng trộn, bóng qua mặt phẳng thu, bóng vào rãnh và overlay là các định nghĩa khác nhau. Không trộn chúng để tính chu kỳ.

## Góc và RPM

Với marker đã định danh và tâm đã hiệu chuẩn, góc quy ước là atan2(cy-y,x-cx): dương ngược chiều kim đồng hồ trên ảnh. Tọa độ ảnh chưa hiệu chuẩn chỉ cho góc chiếu; không mặc định đó là góc vật lý trong mặt phẳng quay. Dừng và tạo segment mới khi đổi cảnh, zoom, mất dấu hoặc thay góc camera.

`track_paddles.py` dùng marker do người kiểm tra chú giải; so sánh hồi quy góc theo PTS với chu kỳ qua cùng một hướng. Đây là hai cách tính trên cùng một nguồn, không phải hai cảm biến độc lập. Mã yêu cầu bằng chứng marker duy nhất và giới hạn tốc độ từ bên ngoài trước khi unwrap. Giới hạn này không được suy ra từ kết quả unwrap. Sai số góc do bấm điểm xấp xỉ sqrt(2)*sigma_px/r rad; sai số phối cảnh, blur, tâm và hiệu chuẩn phải đánh giá riêng. Không có khoảng tin cậy RPM thực nghiệm khi các điều kiện đó chưa thỏa.

`measure_stream_appearance.py` là lần thử riêng: lấy vùng 900×900 pixel native, loại pixel màu vàng trong annulus, trừ median thời gian cho mỗi hướng rồi lấy hệ số Fourier góc bậc 3. Nội suy bilinear chỉ để lấy giá trị trên tọa độ cực của ảnh có sẵn, không tạo frame mới; tọa độ bóng vẫn lấy từ pixel native. Góc pha/3 chỉ là pha hình ảnh giả định. Hai phép tính: độ dốc pha unwrapped và đỉnh periodogram phần thực. Bóng di chuyển, thanh nền, tay gạt trong suốt, thay đổi ánh sáng và góc camera đều gây nhiễu. Sự không thống nhất được giữ nguyên, không tinh chỉnh để ép khớp.

Với một cấu trúc lặp h lần/vòng và sample rate Fs, nhánh alias RPM cách nhau 60*Fs/h; giới hạn chính là ±30*Fs/h. Bậc h chưa được kiểm chứng từ marker đồng nhất, nên nhánh và cả hệ số quy đổi đều có thể sai. Nyquist không tự chứng minh tốc độ thật nằm trong nhánh chính; blur cũng không cho biết tốc độ nếu thiếu shutter time.

## Bóng

Phát hiện màu dùng HSV H=[18,42], S≥75, V≥65; thành phần area 350–7000 px², circularity≥0,45, enclosing radius 12–55 px. Đây là heuristic chưa tune bằng tập nhãn, không phải detector bóng đã kiểm định. Không biết precision/recall. Không thay thế vùng bị che; `occluded=NA`. Mỗi phát hiện của lần thử stream có ID mới, không liên kết sang frame kế tiếp; `identity_confidence=NA`. Không đọc số, không suy ra vận tốc của một bóng cụ thể.

`detect_ball_events.py` là công cụ candidate cho file local: Hough circles và Hungarian matching có gate, kết thúc track khi nhập nhằng hoặc mất dấu. Gate không đủ để chứng minh danh tính vật lý. Đầu ra không tự động tạo sự kiện thu bóng đã xác nhận. Chưa áp dụng nhánh này lên file nguồn Power được cấp phép.

Heatmap chỉ phản ánh các thành phần màu được thấy trong một crop ngắn. Nó không ước lượng mật độ toàn bộ 55 bóng, xác suất được chọn hoặc thiên lệch số. Che khuất và kích thước chiếu phụ thuộc độ sâu làm dữ liệu thiếu không ngẫu nhiên.

## Chạy với file local được phép dùng

```powershell
python scripts/extract_frames.py source.mp4 --out frames/new_run --indices 0 100 101 --rights-confirmed
python scripts/track_paddles.py annotations.csv --manifest frames/new_run/frame_manifest.csv --draw-id 01372 --out measurements/new_paddle_motion.csv --maximum-rpm 120 --unique-marker-confirmed
python scripts/detect_ball_events.py source.mp4 --manifest frames/new_run/frame_manifest.csv --draw-id 01372 --out measurements/new_ball_tracking.csv --start-frame 100 --end-frame 200 --roi 0 0 900 900 --radius 12 55 --gate-px 40
```

Các giá trị ROI, radius, gate và maximum-rpm trong ví dụ là cú pháp minh họa, **không phải thông số đã đo của máy**. Với camera nghiêng, hiệu chuẩn mặt phẳng trước rồi mới dùng `--rectified-plane`. Không truyền các cờ xác nhận nếu chưa có bằng chứng tương ứng. Giữ audio nguyên bản trong input và kiểm tra riêng tiếng điều khiển/công bố khi có quyền dùng file.
