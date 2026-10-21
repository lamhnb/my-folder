# Vietlott Power 6/55 — bàn giao nghiên cứu vật lý và video forensics

**Trạng thái: bàn giao dữ liệu khám phá có thể kiểm toán; chưa đạt bộ đo vật lý hoàn chỉnh.** Thu thập bắt đầu 20/10/2026 UTC, tiếp tục 21/10/2026 UTC. Múi giờ người dùng: Asia/Bangkok. Có truy cập và giải mã video thật; không chỉ đọc metadata. Chưa có RPM vật lý đã xác nhận, chưa có quỹ đạo bóng định danh, chưa có kiểm định độc lập về thiên lệch hay khả năng dự đoán.

Điểm cần tránh hiểu nhầm nhất: đoạn 857,022833–860,993467 s của IUU05082QtE được dùng thử đo ảnh thuộc **phần kiểm tra vận hành được phụ đề ASR và bối cảnh chỉ dẫn**, không được dùng như dữ liệu quay chính thức. Cùng một video có kiểm tra thiết bị, đổi bộ/nạp bóng, rồi quay chính thức và sản phẩm khác. Timestamp overlay và lời công bố không phải timestamp thu bóng.

## 1. Đã truy cập và phân tích bao nhiêu video thực tế?

Đã đọc metadata 8 URL và giải mã được hình ảnh thật của cả 8:

- 7 URL có hình trường quay/máy thật tại các đoạn đã xem, bao phủ 6 ngày liên quan Power; hai URL cùng ngày 25/07 không tính thành hai kỳ.
- 1 URL ngày 21/07 chỉ hiện bảng kết quả đồ họa tại các mẫu 900, 1200, 1500, 1800 s, bị loại khỏi nhóm đo cơ học. Không khẳng định đã kiểm tra toàn bộ gần 12.000 giây của URL này.
- 5 ngày năm 2026 được khảo sát riêng phần quay chính thức từ vùng nạp/trộn đến hiển thị bảy bóng, bằng lấy mẫu có PTS. Có thêm video lịch sử 30/09/2017, mã 00027 đọc trực tiếp trên slate PTS 0.
- Không lưu hoặc giải mã tuần tự toàn bộ file của bất kỳ URL nào. Không có đủ 5 kỳ với mọi sự kiện thu đã kiểm từng frame. Đây là phần tiêu chí hoàn thành **chưa đạt**, không được suy ra từ việc đã thấy bảy bóng trên rãnh.

Danh mục đầy đủ: [sources.csv](sources.csv). Theo ledger hiện tại: 508 hàng locator/hash (có lặp frame ở các crop/scale), 468 giá trị PTS khác nhau theo video ID, 36 annotation trạng thái thủ công; không gọi các con số đó là số frame gốc đã lưu. Một đoạn riêng có 120 frame native liên tiếp để thử đo ảnh. Chi tiết và ngày giờ từng truy cập nằm trong `evidence/`.

## 2. Video nào có đủ quá trình trộn và thu bóng?

Các đoạn dưới đã được giải mã, xem contact sheet từ frame thật và ghi PTS. “Có chuỗi thao tác” là đánh giá ở mức lấy mẫu; không chứng minh mọi frame hoặc mọi chuyển trạng thái cơ học đều nhìn thấy. Khoảng thời gian trong bảng là **đoạn đã khảo sát**, không là mốc bắt đầu/kết thúc Power chính xác.

| Ngày / kỳ liên kết | Video | Đoạn khảo sát phần chính thức, PTS s | Bước lấy mẫu | Bằng chứng cuối đoạn |
|---|---|---:|---:|---|
| 16/07/2026 / 01372 | [IUU05082QtE](https://www.youtube.com/watch?v=IUU05082QtE) | 1060,025633–1210,175633 | 150 frame ≈5,005 s | 7 bóng; xem 1210,175633 s |
| 18/07/2026 / 01373 | [LUEP3hWibQw](https://www.youtube.com/watch?v=LUEP3hWibQw) | 1040,005633–1220,185633 | 300 frame ≈10,010 s | 7 bóng; xem 1220,185633 s |
| 21/07/2026 / 01374 | [Eid9PPhMn_0](https://www.youtube.com/watch?v=Eid9PPhMn_0) | 1050,015633–1220,185633 | 150 frame ≈5,005 s | 7 bóng; xem 1200,165633 s |
| 23/07/2026 / 01375 | [is8GgE2gQu8](https://www.youtube.com/watch?v=is8GgE2gQu8) | 1030,029000–1210,209000 | 150 frame ≈5,005 s | 7 bóng; xem 1195,194000 s |
| 25/07/2026 / 01376 | [diq_elyRXjo](https://www.youtube.com/watch?v=diq_elyRXjo) | 990,022367–1170,202367 | 150 frame ≈5,005 s | 7 bóng; xem 1150,182367 s |

URL bổ sung [oCXvnnydIbY](https://www.youtube.com/watch?v=oCXvnnydIbY) có máy thật, cùng ngày được nêu 25/07; đã xem các seek 810, 900, 960, 1100 s. Chưa căn chỉnh chính xác hai bản phát, không dùng chênh lệch duration để chuyển timestamp giữa chúng.

Nguồn lịch sử [GidYNrF55XY](https://www.youtube.com/watch?v=GidYNrF55XY): slate PTS 0 ghi Power, 00027, 30/09/2017; khảo sát thêm 940–1240 s. Phase kiểm tra/chính thức trong đoạn này chưa xác minh đầy đủ, không đưa vào so sánh timer của nhóm 2026.

Nguồn đồ họa [tUoxKM647iE](https://www.youtube.com/watch?v=tUoxKM647iE): tiêu đề 21/07, metadata upload 22/07, release 21/07; không coi ngày upload là ngày quay. Tên kênh của mọi nguồn được giữ nguyên trong CSV; chưa chứng minh channel ID của các kênh có tên giống công ty thuộc kênh chính thức. Một địa chỉ YouTube mà Vietlott từng công bố [ở đây](https://vietlott.vn/vi/tin-tuc/tin-trung-thuong/19650-vietlott-trao-giai-cho-1-trong-2-khach-hang-trung-jackpot-gan-100-ty/) không resolve thành bằng chứng identity trong phiên này.

Ngày/kỳ 2026 được đối chiếu thêm với [lịch hạn lĩnh thưởng của Vietlott](https://vietlott.vn/vi/trung-thuong/linh-thuong/thoi-gian-linh-thuong-655). Các trường `claimed`, `associated`, `draw_identity_status` giữ giới hạn: không phải mọi ngày/kỳ đã đọc lại trên slate đủ rõ. Riêng slate 16/07 và 30/09/2017 đã nhìn thấy trực tiếp; summary cuối 18/07 và 23/07 nhất quán với metadata. Không chứng nhận nguồn master hoặc ngày ghi hình chỉ từ tiêu đề.

## 3. Có xác định chính xác model máy không?

**Chưa.** [equipment_research.md](equipment_research.md) chứa nguồn kỹ thuật chính thức đã đọc và phân biệt phạm vi lịch sử/2026. PDF ban hành năm 2017 xác nhận nguyên lý và một số thông số quy định của Power; không cung cấp serial/model gắn với video tháng 07/2026. Không dùng thông số một máy Smartplay tương tự để điền cho máy đang xem.

Các nguồn manufacturer nói Vietlott hoặc Mega 6/45 không xác minh model Power. Chưa có manual, CAD, nhãn máy đọc rõ, hồ sơ mua sắm hoặc biên bản kiểm định serial tương ứng. Không thể định danh model chỉ bằng màu đế và hình khoang.

## 4. Đã đo RPM và thời gian trộn chưa?

**Chưa đo RPM vật lý đủ tin cậy hoặc thời gian trộn chính xác của 5 kỳ.** Đã thực hiện một lần thử đo thực, không giấu kết quả thất bại:

| Đại lượng | Kết quả | Ý nghĩa |
|---|---:|---|
| Đoạn ảnh | 857,022833–860,993467 s, IUU05082QtE | Kiểm tra vận hành được ASR chỉ dẫn; 120 frame native |
| Rendition | Format 137, 1920×1080 | H264 công khai; không phải master camera |
| Khoảng frame | ≈0,0333667 s | Xấp xỉ 29,970 fps; metadata làm tròn 30 |
| Cách 1 | 63,789 candidate RPM có dấu | Độ dốc pha hình ảnh / giả định harmonic 3 |
| Cách 2 | 94,904 candidate RPM độ lớn | Đỉnh periodogram / cùng giả định |
| Độ rộng bin | ≈4,995 candidate RPM | Độ phân giải phổ, không phải CI |
| RPM máy, chiều quay vật lý | NA | Hai cách không thống nhất; marker, đối xứng, phối cảnh và nhánh alias chưa xác nhận |

Tại Fs≈29,97 Hz, nếu tín hiệu thực sự lặp ba lần/vòng, các nhánh alias cách khoảng 599,4 RPM và khoảng chính là ±299,7 RPM. Đây là tính toán lấy mẫu có điều kiện, không phải bằng chứng máy chạy dưới giới hạn đó. Có blur và che khuất; shutter time chưa biết. Không chọn lại harmonic/cửa sổ để ép hai số khớp nhau.

CSV, spectrum và tham số ROI đầy đủ nằm ở `measurements/draw_01372_857_appearance*`. Ba biểu đồ trong `charts/` đã được xem để kiểm bố cục và nhãn. `draw_*_paddle_motion.csv` giữ header-only vì chưa có theta/omega/RPM vật lý có căn cứ. Mã tính từ marker thủ công và cách qua chu kỳ đã được kiểm tra bằng fixture tổng hợp, chưa tạo ra kết quả máy thật được xác nhận.

PTS lấy mẫu của 5 đoạn chính thức cho khoảng 29,970 fps; không được tính thời điểm bằng `frame/30`. Camera-original FPS và dropped/duplicate frames trước khi YouTube mã hóa vẫn chưa biết. Sai số nhận dạng sự kiện lớn hơn độ chính xác chữ số của PTS: khoảng hở lấy mẫu 5–10 s, cắt cảnh và độ trễ overlay. Vì vậy mixing duration, capture period và pha tại thu còn NA.

## 5. Có quan sát được cơ cấu thu ở độ phân giải hiện tại không?

**Quan sát được một phần.** Cận cảnh cho thấy hộp/cơ cấu bên phải và bóng chuyển xuống rồi vào rãnh chạy sang trái trên ảnh. Lần kiểm tra từng frame native ở đoạn 877,309767–878,410867 s thấy rõ chuỗi chuyển động; ledger có 34 mẫu, không nội suy. Các mốc trạng thái xem được gồm 877,977100 s (ứng viên bóng đang đi xuống trong hộp) và 878,410867 s (bóng đi vào kênh hiển thị). Không gọi chúng là thời điểm bóng đầu tiên được chọn trong kỳ chính thức.

Chưa xác định được từ ảnh mặt phẳng chính xác nơi bóng bị cô lập vĩnh viễn, trạng thái mọi chốt, hoặc cơ cấu đóng/mở sâu bên trong. Nút điều khiển thấy trước đó, camera dissolve, cơ cấu bắt bóng và bóng được người dẫn đọc số là các sự kiện khác nhau.

Trong phần chính thức, ở Eid9PPhMn_0 PTS 1110,075633 s đã có bóng trong rãnh trong khi overlay chưa điền số; is8GgE2gQu8 có hiện tượng tương tự ở 1105,104000 s. Đây là bằng chứng trực tiếp không nên dùng overlay làm clock chọn bóng. Sai lệch chính xác của overlay chưa được đo thành phân bố.

## 6. Có theo dõi được từng quả bóng không?

**Chưa.** Detector màu tạo 109 thành phần ứng viên trên 120 frame của phần kiểm tra vận hành. Mỗi hàng có ID detection riêng; không phải 109 quả bóng và không có liên kết định danh giữa hai frame. Precision, recall, tỷ lệ occlusion và khả năng đọc số trong lúc chuyển động chưa được đánh giá bằng nhãn độc lập.

Không báo vận tốc một quả bóng từ các detection chưa liên kết. Không điền tâm vùng bị che hoặc dựng quỹ đạo 3D. `identity_confidence=NA`, `occluded=NA`. Heatmap là biểu đồ các candidate thấy trong crop ngắn, không là phân bố toàn bộ 55 bóng hoặc xác suất chọn. Nhánh Hough/Hungarian cho file local được cung cấp như công cụ candidate, chưa chạy trên một master Power được cấp phép.

## 7. Có dấu hiệu thiên lệch cơ học nào không?

**Chưa có bằng chứng đủ để khẳng định.** Quan sát được trạng thái cơ cấu lặp, bóng ở vùng thấp và màu bộ bóng khác nhau ở các đoạn; chưa kiểm định phần nào thành thiên lệch xác suất. Tác động trọng lực và hình học nhìn thấy không tự suy ra số nào có lợi thế.

H1–H5 đều `not_testable` trong bảng kết quả hiện tại. Không có p-value hoặc CI được tạo từ dữ liệu thiếu đầu vào. Hai con số candidate RPM không phải kiểm định thiên lệch. Chưa dùng kết quả quay để fit hoặc chấm giả thuyết trên cùng kỳ; số hiển thị chỉ hỗ trợ đối chiếu đúng phase.

## 8. Tham số nào còn chưa biết?

Danh mục hành động chi tiết nằm ở [unknown_parameters.md](unknown_parameters.md): model/serial, CAD khoang và tay gạt, topology các trục, RPM thật, timing/hình học cửa, tọa độ nạp, ID và số cân của bộ bóng thực tế, ma sát, restitution, rolling resistance, camera calibration, shutter/refraction và đồng bộ audio/camera/overlay.

Các giá trị danh định trong tài liệu lịch sử được lưu với nguồn/trang/phạm vi, không dùng như phép cân hoặc vật chuẩn 2026. Chưa biết lịch thay máy/bộ bóng; khác màu nhìn thấy không chứng minh khác khối lượng hoặc vật liệu.

## 9. Có đủ dữ liệu xây dựng mô phỏng 3D có thể hiệu chuẩn không?

**Chưa đủ cho mô phỏng gần 1:1 hoặc kiểm định xác suất.** Có thể viết một mô hình minh họa với tham số giả định, nhưng nhiều cấu hình 3D/ma sát/đàn hồi khác nhau có thể cho ảnh chiếu tương tự. Dữ liệu hiện có không đủ phân biệt chúng hoặc hiệu chuẩn initial state của 55 bóng.

Một camera bị cắt cảnh không đo được độ sâu/va chạm khuất và danh tính xuyên thời gian; chưa có RPM vật lý độc lập hay hình học cửa. Khớp ảnh hoặc một vài thời gian rơi không xác nhận được động lực học đúng. Nghiên cứu này không tạo simulator hoặc thuật toán dự đoán.

## 10. Cần thêm dữ liệu hoặc thiết bị gì?

Ưu tiên: master không cắt cảnh được cấp phép, nhãn rõ kiểm tra/chính thức, machine serial và ball-set ID, log cân/đo đúng kỳ; camera cố định nhìn toàn khoang và camera close-up cửa có timecode chung; encoder/tachometer để kiểm RPM.

Sau đó mới bổ sung 2–3 camera hiệu chuẩn đồng bộ, shutter ngắn và FPS chọn theo tốc độ thực. Cần đo vật liệu/va chạm, hình học và initial state có kiểm soát để hiệu chuẩn ensemble mô phỏng. Một chiến dịch 10–20 kỳ phải giữ riêng các kỳ kiểm định chưa dùng tune detector/tham số. Không tăng số lượng bản phát có cùng hạn chế rồi coi đó là cải thiện khả năng quan sát.

## 11. Kết quả nào đáng tin cậy, kết quả nào chỉ là giả thuyết?

**Đã kiểm tra trực tiếp:** công cụ đọc được pixels video thật; các PTS và hash trong ledger; có chuỗi nạp/trộn/bảy bóng ở các đoạn được liệt kê; slate lịch sử và slate 16/07; các trạng thái được annotation; metadata có ngày upload/release tách biệt; hai phương pháp ảnh cho kết quả không thống nhất; số hàng detector là 109; không có physical ball ID được xác nhận.

**Ước lượng có điều kiện:** sample rate của rendition từ khoảng PTS; pha ảnh Fourier, candidate RPM và heatmap. Các con số này có đầu vào/mã tái lập nhưng chưa là thông số máy.

**Bằng chứng hỗ trợ, chưa là xác minh độc lập:** mốc từ ASR và phân loại phần kiểm tra/chính thức. Chưa nghe audio thủ công, không dùng timestamp ASR để điền sự kiện vật lý.

**Chưa biết/giả thuyết:** model, rotor topology, RPM/hướng thật, phase lock H1, timer H2, phân bố cửa H3, memory vị trí nạp H4 và khác biệt vật lý giữa bộ/cấu hình H5. Không có kết luận dự đoán xổ số.

## 12. Nên tiếp tục mô phỏng hay dừng?

**Tạm dừng mục tiêu mô phỏng 3D gần 1:1 có hiệu chuẩn bằng bộ dữ liệu này.** Tiếp tục nghiên cứu khả năng quan sát và thu dữ liệu được phép trước. Không kết luận việc đo RPM từ mọi video là bất khả thi chỉ vì hai phương pháp thăm dò này thất bại; cần marker/hiệu chuẩn hoặc phép đo độc lập để thử tiếp.

Điều kiện để chuyển sang mô phỏng: hình học có kích thước được xác minh; một chuỗi RPM/cửa đồng bộ được kiểm; nhãn ID/occlusion đạt kiểm định trên tập riêng; tham số bóng và ít nhất hai góc camera; sau đó khóa cấu hình và đánh giá trên kỳ chưa xem. Nếu không đạt các điều kiện này, chỉ nên dùng mô hình định tính có ghi rõ giả định, không diễn giải thành dự báo.

## Dữ liệu bàn giao và giới hạn tái lập

Có mã Python thực sự đã dùng, CSV có PTS/hash, metadata đã lược signed URLs, lỗi và biện pháp khắc phục, 3 biểu đồ tự tạo, tài liệu phương pháp/schema và kế hoạch H1–H5. Có 198 hàng events: 36 snapshot đã xem và 162 placeholder NA (27 loại sự kiện ×6 kỳ); các placeholder không phải quan sát. Các file góc gạt vật lý chưa có hàng đo. Bảng detector chỉ chứa candidate của đoạn kiểm tra.

Không có video/audio/frame pixels của bên thứ ba trong Git hoặc ZIP: quyền lưu/phân phối chưa được xác nhận; người dùng đã chọn bàn giao URL và dữ liệu, loại video khỏi ZIP. Vì vậy yêu cầu “ảnh frame minh chứng bàn giao” chưa được đáp ứng bằng file ảnh; được thay bằng URL+PTS+hash và lệnh tái trích. Không có SHA256 video hoàn chỉnh; hash buffer 16 MB trong log thử chỉ là hash buffer. Chưa có master bất biến nên YouTube có thể thay đổi/gỡ/re-encode nguồn; khi hash không khớp phải dừng so sánh, không tự coi đó là thay đổi cơ học.

`METHODS.md`, `DATA_DICTIONARY.md`, `evidence/reproduction_commands.csv` và manifest hash giải thích bước tái chạy. Pipeline local được kiểm bằng video hình học tự tạo tạm thời, không được sử dụng làm dữ liệu thực nghiệm. Tám kiểm tra phần mềm đã chạy qua, bao gồm từ chối alias, chiều quay, ambiguity và đối chiếu PTS/frame native. Chúng không xác nhận độ chính xác khoa học trên máy Power. Validator kiểm schema có thể pass khi phép đo vật lý vẫn còn thiếu; trạng thái đó được giữ rõ.

Lỗi đầy đủ nằm ở `evidence/known_failures.csv`: browser không khởi tạo được, mạng sandbox, ffmpeg direct URL timeout, một crop sai thứ tự có 0 frame, bộ lọc ASR từ khóa cần sửa và hai phép ước lượng không qua cross-check. Không xóa log thất bại. Frame index toàn video vẫn NA, không giả bằng time×30. Bộ bridge chỉ đọc URL công khai không DRM trong RAM, không cookie/xác thực hoặc cache video.

## Repository và bước tiếp theo cụ thể

Workspace tách biệt: `C:/vietlott-research-repo/vietlott-power655-physical-research/`. Repository `lamhnb/my-folder`, base commit `8d53901feedc9027a370dd9b4e1a1d10ba0448c1`, branch `research/power655-physical-20261020`. Chỉ folder nghiên cứu mới thuộc thay đổi này. Không chạy/sửa B1, C50, B7-100, B7-200, Champion; không merge vào master. Hash và Git diff cuối cùng được kiểm trước commit; kết quả push/commit được báo riêng sau khi thực hiện.

Researcher tiếp nhận nên làm theo thứ tự:

1. Kiểm file_manifest và ZIP checksum, chạy tests/validator, đọc phân biệt NA/ảnh thăm dò/phase.
2. Xin nguồn master và quyền lưu/chia sẻ; xác minh channel/source chain, ngày/slate và bộ bóng cho 5 kỳ.
3. Đối chiếu lại ASR với audio thật; reviewer thứ hai kiểm ranh giới phần thử/chính thức.
4. Chú giải liên tiếp các frame trước/sau từng lần thu chính thức, tách cửa/ball exit/display/announcement, ghi cận khi cắt cảnh. Chưa được coi bộ events hiện tại là hoàn chỉnh.
5. Hiệu chuẩn trục/marker và cross-check RPM bằng tachometer hoặc cycle marker có danh tính; khóa detector rồi đánh giá precision/recall/ID trên tập riêng.
6. Chỉ khi các bước trên đạt yêu cầu mới thu thêm 10–20 kỳ và bắt đầu hiệu chuẩn mô phỏng/kiểm định H1–H5 theo thiết kế độc lập.
