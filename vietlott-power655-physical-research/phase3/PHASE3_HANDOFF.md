# Power 6/55 Phase 3 — bàn giao pilot thứ tự bóng

Ngày làm việc **21/10/2026, Asia/Bangkok**. Branch `research/power655-draw-order-phase3`, base `e55fd8dba5bac41c7c157a5a3bc0d7ff2718de7a` (giao thức đã đọc đầy đủ). Đã đọc bàn giao/phương pháp Phase 1, bàn giao/schema Phase 2 và hồ sơ B7 trước khi thực thi. Chỉ thêm dữ liệu/mã dưới `phase3/`.

**Trạng thái: PILOT CHƯA QUA GATE NGHIÊN CỨU.** Đã đọc số trên bóng thật ở 35/35 lần thu của năm kỳ. Chưa có reviewer độc lập thứ hai hoặc đối chiếu đầy đủ số với nguồn chính thức truy cập được. Vì vậy **0 kỳ đạt `verified_two_reviews`**; toàn bộ 35 nhãn giữ `provisional_one_review`. Chưa đạt mục tiêu 100 kỳ, chưa thực thi kiểm định chính hoặc kiểm định dự báo ngoài mẫu. Đây không phải tuyên bố đã hoàn tất Phase 3.

## Dữ liệu thực sự đã thực thi

Tận dụng năm MP4 Phase 2 và đúng 35 capture indices/timestamp đã có; không xây lại nghiên cứu sự kiện. Băm lại toàn bộ năm file, **5/5 SHA256 khớp** `phase2_sources.csv`. Không tải lại video. Trích 210 frame 1920×1080 ở PTS nguồn bằng ffmpeg; công bố 70 PNG native (hai frame mỗi lần thu), ledger đủ 210 mẫu và lệnh tái tạo. Các mẫu thừa giữ local, không phải nhãn độc lập hoặc kỳ bổ sung. Mọi PNG minh chứng đã đối chiếu hash file/pixel, PTS tick và giải mã lại từ MP4 nguồn.

Hai frame được đọc cho mỗi lần thu cách nhau 15 encoded intervals = 0,5005 s. `readable_pts_start/end` là hai mẫu quan sát đọc rõ, không chứng minh đọc rõ liên tục trong cả khoảng, không phải thời điểm chọn bóng. Đơn vị suy luận là kỳ quay, không phải frame hoặc lần thu. Contact sheets là crop/scale xem ảnh; bằng chứng gốc vẫn là PNG đầy đủ. Không dùng OCR, enhancement, frame sinh bởi AI hoặc tự điền số. Kiểm tra nhiều mẫu bởi cùng Codex vẫn chỉ là **một reviewer**.

| Kỳ | Ngày | Thứ tự sáu bóng chính đọc trên rãnh thật | Bóng đặc biệt |
|---|---|---|---|
| 01372 | 16/07/2026 | 20 → 19 → 48 → 53 → 33 → 45 | 21 |
| 01373 | 18/07/2026 | 54 → 45 → 41 → 48 → 55 → 22 | 16 |
| 01374 | 21/07/2026 | 32 → 11 → 08 → 24 → 39 → 22 | 13 |
| 01375 | 23/07/2026 | 55 → 38 → 03 → 08 → 01 → 40 | 36 |
| 01376 | 25/07/2026 | 05 → 50 → 37 → 27 → 33 → 09 | 48 |

Mỗi dòng có bảy số khác nhau trong 1..55. Thứ tự được gắn với capture đã lập chỉ mục và chuỗi thêm bóng trên rãnh; không lấy từ mảng sáu số sắp tăng. Các chữ số in trên bóng trong hai mẫu đầu đều đọc được. Với special, bóng dừng riêng ở bên phải; không coi nó là main thứ bảy. Overlay chỉ xuất hiện như một phần frame nguyên gốc; crop review loại vùng overlay dưới màn hình.

## Chất lượng và đối chiếu

- Số kỳ có source video: **5**, số kỳ mới tải thêm: **0**, số kỳ đọc đủ bảy bóng bởi một reviewer: **5**.
- Tỷ lệ hoàn thành đọc nhãn: **35/35 = 100% trong pilot**. Đây không phải accuracy được hiệu chuẩn; accuracy và agreement giữa reviewer đều **NA**.
- Số kỳ đủ hai review độc lập và đối chiếu số chính thức: **0**. Không nâng nhãn lên verified chỉ vì hai frame giống số hoặc bộ số khớp.
- Bộ sáu số không thứ tự và special của **5/5 kỳ khớp** trang kết quả Minh Ngọc. Nguồn này là thứ cấp, không đổi tên thành nguồn Vietlott. URL, SHA256 response, đoạn trích số và kết quả parser nằm trong `evidence/result_sources/` và `published_results.csv`. Nhãn vật lý ở `primary_labels.json` độc lập với mã parse kết quả.
- Nguồn [lịch lĩnh thưởng Vietlott](https://vietlott.vn/vi/trung-thuong/linh-thuong/thoi-gian-linh-thuong-655) xác nhận ID/ngày, không xác nhận bộ số. Các request đến trang kết quả chính thức trả 403 hoặc công cụ báo không truy cập được; đã thử cả mẫu query `id=...&nocatche=1` tìm được từ trang chính thức. Không có đối chiếu số chính thức được chứng nhận trong bản này.
- Không phát hiện xung đột bộ số trong phép đối chiếu thứ cấp, không có nhãn NA trong pilot. Chưa có oracle vị trí độc lập để suy ra tỷ lệ lỗi. Parser HTML ban đầu thất bại do số nằm trong div con; đã sửa bằng response cũ có hash, không thay bất kỳ nhãn bóng nào.

Nguồn là rendition public, không phải master camera đã xác thực. Channel identity, ngày ghi hình và chuỗi nguồn master còn giới hạn như Phase 2. Model/serial máy, ball-set ID và lịch thay thiết bị đều **NA**. Khác màu bóng giữa video không được dùng để điền ID thiết bị.

## Mở rộng 100 kỳ và holdout

Giao thức yêu cầu chất lượng pilot, review độc lập và provenance trước mở rộng. Gate này chưa đạt. **Chưa thử tải thêm kỳ lịch sử**, không khai 95 kỳ chưa thu là “video thiếu”, không tạo hàng dữ liệu giả. `expansion_status.json` phân biệt rõ chưa thử, thiếu dữ liệu và không xác minh được.

`analysis_plan.md` khóa cách lấy mẫu, đọc số, quy tắc NA và thống kê trước khi đọc nhãn Phase 3; hash kế hoạch nằm trong từng extraction log. Kết quả không thứ tự pilot đã gặp khi tìm nguồn nên pilot là dữ liệu phát triển, không phải blind ground truth hoặc holdout. Chưa có cohort lịch sử đã khóa; **không có holdout được sử dụng hoặc giả xưng là chưa xem**. Khi đủ điều kiện mở rộng: chọn kỳ liên tiếp theo quy tắc đã định, ghi missingness/duplicate, khóa danh sách rồi giữ 20% mới nhất chưa phân tích để đánh giá cuối.

## H1–H4 và phép tính thăm dò riêng

`order_bias_tests.csv` là kết quả **phân tích chính**: H1, H2, H3, H4 và special đều `not_testable`, p-value/effect/CI **NA**, số kỳ phân tích **0**. H1/H2 thiếu đầu vào đủ xác minh/cỡ mẫu; H3 thiếu các giai đoạn và holdout đủ lớn; H4 thiếu danh tính thiết bị. NA không đồng nghĩa không có bias và không phải p=1.

Đã chạy thêm `pilot_sensitivity.csv`, tách biệt hoàn toàn: năm chuỗi tạm xác minh, 19.999 Monte Carlo replicates, seed 20261021. Cùng các thống kê đã khai báo, không tune sau kết quả. Scope bổ sung được ghi **sau khi đọc nhãn, trước khi chạy thống kê** trong `evidence/sensitivity_scope.md`; không giả thành một đăng ký nghiên cứu mù.

| Phép tính thăm dò | Statistic | Hiệu số so trung bình null | Chuẩn hóa theo SD null | MC p thô | Holm, family 5 |
|---|---:|---:|---:|---:|---:|
| H1 number×position | 126,000 | 6,066 | 1,099 | 0,25905 | 1,000 |
| H2 directed adjacent transition | 125,000 | 1,667 | 0,924 | 0,50170 | 1,000 |
| Special, độ lệch tổng so mean 49 số còn lại | 4,265 | −24,092 | −1,164 | 0,91220 | 1,000 |

Null H1/H2 hoán vị sáu số **trong từng kỳ**, giữ nguyên tập số và clustering. Expected directed transition a→b trong một kỳ chứa cả hai là 1/6; không so với mô hình lấy có hoàn lại. Null special lấy một trong **49 số còn lại**, không hoán vị cả bảy. Holm bảo toàn family năm giả thuyết; các test chưa chạy chỉ dùng p=1 nội bộ cho correction, cột kết quả chính vẫn NA.

CSV ghi khoảng binomial chính xác 95% cho xác suất exceedance của mô phỏng; **đó không phải CI effect hoặc CI thiên lệch vật lý**. CI effect giữ NA do n<20. Mean absolute adjacent gap là 16,0 đơn vị số, chỉ mô tả. Các null-standardized discrepancies không phải lợi ích dự báo. Pilot rất thưa, với mỗi số chỉ xuất hiện một lần thì phần đóng góp H1 không thể cung cấp nhiều thông tin về bias vị trí; unit tests cũng xác nhận sự suy biến ở một kỳ.

Các phép tính thăm dò này không cho tín hiệu đáng tin cậy sau correction. Tuy nhiên với năm kỳ được chọn trước và nhãn chưa review độc lập, **chưa thể kết luận âm tính về quần thể hoặc loại trừ bias nhỏ**. H3/H4 chưa có kết quả thực nghiệm, không lấy p thăm dò H1/H2 để lấp hai mục đó.

## Năm câu hỏi về B7-100

1. **Có bias thứ tự không?** Chưa có bằng chứng đủ tin cậy; phân tích chính chưa đủ điều kiện. Thăm dò không có kết quả có ý nghĩa sau correction.
2. **Ổn định theo thời gian không?** Chưa xác định; năm kỳ trong mười ngày không kiểm định được ổn định lịch sử.
3. **Liên hệ với xác suất vào sáu main không?** Chưa kiểm định. Conditional permutation giữ cố định tập sáu số nên tự nó không đo được lợi thế inclusion.
4. **Thông tin có trước kỳ tiếp theo không?** Thứ tự kỳ đã quay chỉ biết sau kỳ đó. Chưa xác minh metadata thiết bị hoặc một cơ chế dự báo strict-past nào dùng được trước kỳ tiếp theo.
5. **Có cải thiện ngoài mẫu không?** Chưa chạy một dự báo hoặc phép chấm ngoài mẫu nào; không có bằng chứng cải thiện B7-100/Jackpot.

Tín hiệu vị trí với điều kiện đã xuất hiện, tín hiệu xác suất được chọn và tối ưu độ phủ tổ hợp là ba đại lượng khác nhau. Không sửa B7-100, B7-200, B1/C50 hoặc Champion. Không đề xuất model mới từ pilot.

## Kiểm tra và tái lập

`validation_report.json` tách software/integrity khỏi scientific gates. Đã chạy **11 unit tests**, kiểm enumeration đủ 720 hoán vị cho expected counts, sparse-statistic counterexample, null special 49, add-one MC, Holm family, duplicate/NA/source/role/PTS rejection, cấm cùng reviewer tự xác minh, cấm nguồn thứ cấp/403 thành official và tính lặp lại của Monte Carlo. Fixture tổng hợp không được trộn vào CSV thực nghiệm.

Validator kiểm 70 frame native/hash/PTS, 35 interval bindings, 5 source hashes, 5 secondary reconciliations, kế hoạch khóa và protected diff; **giải mã lại cả 70 mẫu từ nguồn** để đối chiếu BGR hash. Source video giữ ngoài Git theo Phase 2 ở `C:/vietlott-research-output/phase2-inputs/`. Hai mẫu đầu/capture được đưa vào Git; frame 02–05 và HTML gốc giữ local, ledger/hash/lệnh tái tạo vẫn được bàn giao. Không có MP4 trong commit.

Từ repo, PowerShell:

```powershell
$py = 'C:\vietlott-power655-env\Scripts\python.exe'
& $py vietlott-power655-physical-research/phase3/scripts/order_tests.py --pilot-sensitivity
& $py vietlott-power655-physical-research/phase3/scripts/validate_phase3.py --redecode-evidence
```

Để tái trích vào tag mới (từ chối ghi đè):

```powershell
& $py vietlott-power655-physical-research/phase3/scripts/extract_pilot.py --tag replay_new
```

Tái trích chính xác cần cùng MP4 có SHA đã pin, ffmpeg và OpenCV tương ứng. Nếu SHA source khác phải dừng; PNG encoder khác có thể đổi hash file nên BGR hash được lưu riêng. Runtime thực tế nằm trong validation report. `build_tables.py` tái tạo từ nhãn quan sát đã lưu; không phải OCR hoặc reviewer mới. `order_tests.py` fail closed cho primary: chưa cho chạy khi chưa có cohort/holdout sealed; H4 implementation thực nghiệm và chấm dự báo vẫn là việc chưa làm, không giả đã thực thi.

## Việc còn lại theo gate

1. Reviewer độc lập đọc blind 35 capture từ MP4/native frame, không xem primary_labels hay bộ số trước khi ghi nhãn; lưu reviewer ID, frame/PTS/hash, disagreements và adjudication. Review AI độc lập nếu dùng phải được nêu rõ, không thay thế chuyên gia được hiệu chuẩn.
2. Truy xuất bản công bố kết quả chính thức cho từng kỳ, giữ response/PDF hash và đối chiếu sáu main không thứ tự + special riêng. Giữ các log 403 trước đó.
3. Khi pilot qua gate, mở rộng ít nhất 100 kỳ thật; deduplicate, log selection/missingness, giữ metadata máy/bộ bóng ở NA khi không có chứng cứ; khóa cohort và holdout thời gian trước phân tích.
4. Chạy primary H1–H4 theo khả năng dữ liệu, ghi effect/uncertainty/multiple testing, rồi mới cân nhắc nghiên cứu inclusion và kiểm ngoài mẫu. Không nâng Champion từ kết quả exploratory.

Việc giao đủ các file và pass unit/integrity tests **không có nghĩa đạt các gate khoa học A–C hoặc hoàn tất mục tiêu 100 kỳ**.
