# Vietlott Power 6/55 — physical observations

Nghiên cứu độc lập ngày 20/10/2026. **Đọc FINAL_HANDOFF.md trước khi sử dụng số liệu.**
Không có mô hình dự đoán, kết luận thiên lệch, hay RPM vật lý đã được xác nhận.

## Nội dung và quyền sử dụng

Video công khai được giải mã tạm trong RAM. Chủ sở hữu quyền chưa cho phép lưu/phân phối bản video; người dùng đã chọn bàn giao URL và dữ liệu, loại video khỏi ZIP. Không có video, âm thanh hoặc frame của bên thứ ba trong commit/ZIP. `frames/` chứa danh mục locator và hash, không chứa ảnh. Các ảnh trong `charts/` là biểu đồ tự tạo từ CSV. Không có AI-generated frame, nội suy, enhancement hay chuyển FPS trong dữ liệu đo. Contact sheet thu nhỏ chỉ được xem tạm, không phải đầu vào đo.

`measurements/*appearance*` và các phát hiện màu vàng là **tín hiệu ảnh thăm dò chưa kiểm định**, không phải góc tay gạt thật hoặc danh tính bóng. `NA` nghĩa là chưa biết/không đo được, không phải 0.

## Tái lập trong Windows PowerShell

Yêu cầu Python 3.12, ffmpeg/ffprobe trong PATH; xem `requirements-lock.txt` và `evidence/environment.json`.

```powershell
uv venv .venv
uv pip install --python .venv/Scripts/python.exe -r requirements-lock.txt
.venv/Scripts/python.exe scripts/test_pipeline.py
.venv/Scripts/python.exe scripts/validate_measurements.py . --out evidence/validation.json
```

Tái đọc nguồn công khai (cần Internet; YouTube có thể thay đổi nội dung/định dạng):

```powershell
.venv/Scripts/python.exe scripts/inspect_clip.py IUU05082QtE --start 850 --duration 110 --every 150
.venv/Scripts/python.exe scripts/measure_stream_appearance.py IUU05082QtE --draw-id 01372 --start 857 --count 120 --roi 510 60 900 900 --center 450 450 --annulus 130 400 --harmonic 3
```

Lệnh đo từ chối ghi đè kết quả cùng tên. Tái lập trong bản sao thư mục mới, hoặc dùng thư mục làm việc tách biệt và giữ nguyên bản bàn giao. So sánh PTS và hash crop BGR trước khi so sánh giá trị. Signed URLs chỉ được lấy mới trong RAM, không lưu vào artifact. Bộ chuyển tiếp byte chỉ lắng nghe localhost, không lưu cache hoặc vượt xác thực/DRM.

Nếu sau này có file nguồn được phép dùng, `extract_frames.py --rights-confirmed` tạo PNG không mất dữ liệu và manifest PTS đầy đủ; xem `METHODS.md`. Chưa có file nguồn hợp lệ đi kèm nên nhánh local-file của pipeline chỉ được kiểm tra bằng fixture tổng hợp.

## File chính

| File | Ý nghĩa |
|---|---|
| FINAL_HANDOFF.md | Kết quả, giới hạn, 12 câu trả lời và bước tiếp theo |
| sources.csv | URL, metadata, trạng thái xác minh, quyền và tính đầy đủ |
| equipment_research.md | Thông số tài liệu, tách phạm vi lịch sử và hiện tại |
| unknown_parameters.md | Tham số còn thiếu và cách bổ sung |
| physical_hypotheses.md | H1–H5, thiết kế kiểm định, trạng thái thiếu dữ liệu |
| measurements_summary.csv | Tổng hợp theo nguồn/kỳ; phép đo chưa xác nhận là NA |
| measurements/ | Quan sát PTS, tín hiệu ảnh, phát hiện vô danh, thiếu dữ liệu công khai |
| frames/frame_evidence_manifest.csv | URL + PTS + hash để kiểm lại, không có ảnh gốc |
| evidence/ | Metadata đã loại URL ký số; log truy cập, phiên bản, QA |
| scripts/ | Mã đọc luồng, phân tích, kiểm tra và đóng gói |

Không chạy hoặc sửa `../vietlott-power655-research/`; B1, C50, B7-100, B7-200 và Champion nằm ngoài phạm vi.
