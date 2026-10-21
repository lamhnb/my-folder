# Data dictionary

Tất cả CSV UTF-8, dấu phẩy; `NA` là missing/unknown, không là 0. Dữ liệu số thực có độ chính xác xuất file, không tự mang sai số thực nghiệm tương ứng. `high/medium` là đánh giá thủ công định tính, chưa hiệu chuẩn xác suất.

| Dataset | Định nghĩa / cách dùng |
|---|---|
| sources.csv | Metadata thật; ngày `claimed` giữ tách khỏi trạng thái xác minh hình ảnh. `draw_id_associated` là liên kết nguồn với kỳ, không định danh phase của mọi frame. `full_file_decoded=false` cho mọi nguồn. |
| measurements_summary.csv | `official_sampled_start/end` là cận đoạn đã khảo sát, không phải bắt đầu/kết thúc Power hoặc trộn. FPS là sample-rate của rendition suy từ PTS, camera-original FPS=NA. Candidate count=NA nếu chưa chạy detector. |
| draw_*_events.csv | Đúng schema yêu cầu. Các hàng `observed_*` là trạng thái ở frame đã xem. 27 hàng bắt buộc/kỳ còn NA là checklist thiếu, không phải phép đo hoặc bằng chứng sự kiện đã được quan sát. ball_7 là bóng đặc biệt. |
| draw_*_paddle_motion.csv | Header-only vì chưa có marker/góc/RPM vật lý đủ căn cứ. Không đưa tín hiệu ảnh thăm dò vào bảng góc vật lý. |
| draw_01372_ball_tracking.csv | 109 ứng viên màu vàng của phần kiểm tra vận hành; mỗi ID là một detection mới, không có liên kết qua frame. identity_confidence và occluded=NA, không có tâm giả cho vùng khuất. |
| Các ball_tracking khác | Header-only: chưa chạy detector đáng tin. Không biểu diễn rằng video không có bóng. |
| draw_01372_857_appearance.csv | 120 frame native, source PTS, clip index và hệ số ảnh; góc có tên `candidate_appearance_angle_deg`, không phải theta tay gạt. Hash native crop BGR 900×900, source x=510,y=60. |
| *_appearance_spectrum.csv | Periodogram của tín hiệu ảnh, đơn vị x Hz; bin resolution không phải CI. |
| manual_observations.csv | Annotation do Codex kiểm tra contact sheet thật; source PTS, ledger/hash, phase và count chỉ điền khi thấy. Chưa có reviewer thứ hai. |
| phase_assignments.csv | Phân loại hồi cứu đoạn đo: kiểm tra vận hành được ASR + bối cảnh chỉ dẫn; không xác minh bằng nghe audio thủ công. |
| hypothesis_results.csv | 5 giả thuyết không đủ đầu vào kiểm định; p_value/CI=NA. |
| frames/frame_evidence_manifest.csv | Locator và hash của samples có thể gồm cùng frame ở nhiều crop/scale; số hàng không phải số frame độc nhất. Mỗi hash chỉ so sánh đúng phép biến đổi tương ứng. |
| evidence/clips/*.json | PTS thật, format ID, sampling interval, pixel crop/scale (với phiên bản log mới), hash, HTTP transport. `frames_decoded=0` hoặc ffmpeg exit khác 0 không phải bằng chứng ảnh. |
| evidence/access/*.json | Các frame seek khảo sát, thời gian seek xấp xỉ; không có PTS đã kiểm chứng. Không dùng làm phép đo thời điểm thu. |
| evidence/caption_landmarks.json | Mốc từ khóa phụ đề ASR; không transcript, không tự động phân loại phase; không dùng timestamp ASR làm sự kiện vật lý. |

`global_frame_index=NA` và `frame_index=NA` là có chủ ý. Có thể tái trích bằng PTS/clip sampling theo các lệnh trong `evidence/reproduction_commands.csv`, sau đó kiểm hash với đúng ffmpeg và format. Những log đầu chưa có trường kích thước preview dùng mặc định 320×180; log start 860 và 960 dùng 960×540. Hai run crop 877.3 thành công lần lượt dùng 268×280 và 201×210. Đây chỉ là ảnh xem tạm; đo ảnh dùng crop native riêng.

Audio chưa được nghe/đối chiếu trực tiếp. Phụ đề ASR có thể sai cả chữ và timing. Không suy ra tính hợp pháp của quyền phân phối video từ trạng thái public hoặc license=NA.
