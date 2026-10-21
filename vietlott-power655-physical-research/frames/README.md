# Frame provenance, không phân phối pixels

Không có ảnh video gốc trong thư mục này. Quyền phân phối lại chưa được xác nhận; lựa chọn của người dùng là bàn giao URL và dữ liệu. Contact sheets đã xem được tạo từ frame thật trong RAM rồi hủy, không phải ảnh AI.

`frame_evidence_manifest.csv` cung cấp video ID, format ID, PTS, hash và phương pháp tái trích. Hash preview là BGR của ảnh thu nhỏ **trước khi** chèn timestamp. Hash native crop là BGR của crop nguyên pixel; hai loại hash không hoán đổi. Không có SHA256 video hoàn chỉnh, vì không có video hoàn chỉnh được lưu. Xem `scripts/inspect_clip.py` và `scripts/measure_stream_appearance.py`.
