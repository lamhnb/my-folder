# Kiểm toán candidate RPM Phase 1

## Phạm vi và kết quả

Chỉ tính lại **120 hàng hệ số ảnh đã lưu**, PTS 857.022833–860.993467 s của IUU05082QtE, format 137, 1920×1080. Đoạn này thuộc kiểm tra vận hành, không thuộc quay chính thức. Không giải mã video mới trong script kiểm toán này. Nguồn, SHA256 và phiên bản thực chạy nằm trong `evidence/legacy_rpm_audit.json`.

- Phase slope có dấu: **63.789049874 candidate RPM**.
- Đỉnh periodogram phần thực: **94.904146812 candidate RPM**.
- Chênh lệch: **31.115096937 candidate RPM**; tỷ số 1.487781163.
- Fs từ median chênh PTS: 29.969730572 Hz. Độ rộng bin: 4.994955095 candidate RPM; đây không phải CI.
- **RPM vật lý, góc vật lý tuyệt đối, chiều quay và sai số góc thực nghiệm: NA.** Tái lập đúng phép tính không xác nhận đại lượng cơ học.

Sai khác lớn nhất khi tái tạo góc, biên độ, phổ và hai candidate đã lưu là 2.27e-13; các kiểm tra <1e-8 đều đạt với Python 3.14.0, NumPy 2.3.4, SciPy 1.16.3. Đây là phiên bản cài thực tế; không giả vờ đã dùng lockfile Phase 1.

## Harmonic và alias

Hai thuật toán dùng **cùng hệ số Fourier góc h=3**. Đổi cùng hệ số chia cho cả hai không đổi tỷ số. Tỷ số gần 3/2 (lệch -0.012218837) không chứng minh harmonic sai: tự chia pha cho 2 cho 95.683574812, vẫn lệch 0.779428000 RPM, và không có bằng chứng marker/hình học để thay phép đổi. Không chọn lại harmonic nhằm ép khớp.

Nếu và chỉ nếu một chu kỳ vật lý tạo h=3 chu kỳ ảnh, nhánh alias cách 599.394611 RPM và nhánh chính ±299.697306 RPM. Không có giới hạn vật lý độc lập nên không thể chọn nhánh chính. Hai tần số tổng hợp hiện tại không đồng nhất theo ±f+kFs: phần dư nhỏ nhất 1.555754847 Hz (31.115096937 candidate RPM). Do tín hiệu không phải một sinusoid đã xác nhận, điều này không loại alias khỏi video; nó chỉ bác cách sửa đơn giản bằng cộng một nhánh Fs/h cho một candidate.

## ROI, bóng, che khuất và phối cảnh

Code Phase 1 cố định crop x=510,y=60,w=900,h=900; tâm (450,450), annulus 130–400 px. Nó lấy trung bình sáng theo bán kính ở từng hướng sau khi loại màu vàng, trừ median theo thời gian, rồi lấy h3. Đây là tín hiệu ảnh tổng hợp; không theo dõi vật liệu của một tay gạt. Marker bất đối xứng, số trục, h và hiệu chuẩn mặt phẳng chưa được xác nhận.

Số pixel mask vàng toàn crop thay đổi 9507–131722 (1.17%–16.26% diện tích crop). Đây **không phải tỷ lệ che annulus**. Pearson mô tả giữa mask và hệ số thực/ảo/biên độ lần lượt -0.2404, -0.0458, 0.2425; không tính p-value trên các frame tương quan, không suy ra nguyên nhân. Mask động thay đổi mẫu nền theo bán kính; bóng không bị loại hoàn toàn và biên mask, blur, thanh nền, phối cảnh, tay trong suốt cũng có thể làm đổi pha.

Fixture đối kháng tạo nền sáng hoàn toàn đứng yên với mask loại trừ quay cho candidate gần 30 RPM. Nó chứng minh cơ chế gây nhiễu **có thể xảy ra**, không chứng minh đây là nguyên nhân ở video thật. Hệ số đã nén và tổng area không giữ thông tin đủ để chạy lại ROI/mask/camera ablation. Cần pixels và marker thật để phân biệt các nguyên nhân; chưa định lượng riêng lỗi phối cảnh hoặc blur.

## Độ ổn định và tính độc lập

`rpm_cross_validation.csv` chứa 20 hàng của bốn phép tính trên năm cửa sổ cố định (120, 60 đầu/cuối, 90 đầu/cuối). Periodogram phức và autocorrelation chỉ là chẩn đoán mới trên **cùng scalar cũ**; chúng không là phép đo video mới hoặc cảm biến độc lập. Các cửa sổ chồng nhau không là các kỳ độc lập. Không chọn cửa sổ có kết quả đẹp để thay kết luận toàn đoạn. Mỗi dòng giữ physical RPM=NA.

| Cửa sổ | Phase slope candidate RPM có dấu | Periodogram thực candidate RPM độ lớn | Autocorrelation candidate RPM độ lớn |
|---|---:|---:|---:|
| full_120 | 63.789050 | 94.904147 | 46.107278 |
| first_60 | 46.003558 | 49.949551 | 42.813901 |
| last_60 | 69.733551 | 99.899102 | 99.899102 |
| first_90 | 60.277292 | 79.919282 | 46.107278 |
| last_90 | 70.482049 | 93.239162 | 99.899102 |

Các kết quả phụ thuộc mạnh vào cửa sổ; chưa phân biệt được thay đổi tín hiệu, tốc độ thật và sai nhận dạng. Bước pha hệ số lớn nhất là 178.205746 độ, gần ngưỡng unwrap 180 độ; thiếu một giới hạn tốc độ và marker độc lập để xác minh nhánh unwrap.

Độ lệch RMS pha ảnh/3 quanh đường hồi quy toàn đoạn là 63.375386 độ. Đây là residual của mô hình tín hiệu ảnh, **không là sai số góc vật lý hoặc CI**. Không có góc tuyệt đối khi thiếu marker duy nhất; đối xứng h3 tự mang bất định 120 độ và chưa loại các nhánh alias.

## Kiểm thử và tái lập

Chạy từ thư mục dự án:

```powershell
python phase2/scripts/rpm_audit.py --validate-only
python phase2/scripts/rpm_audit.py
```

7 fixture tổng hợp đạt: tốc độ phân tích đã biết 40 RPM, dấu quay âm, hai chuyển động 40/640 RPM cho cùng mẫu ở 30 Hz, bất định góc 120 độ, nền tĩnh với mask động, PTS trùng và PTS giảm bị từ chối. Synthetic chỉ kiểm numerical logic/counterexample, không xác nhận video. Các input Phase 1 không bị ghi.

**Kết luận:** hai candidate cũ tái lập được và không đủ cơ sở chuyển thành RPM máy. Chưa thể chọn một nguyên nhân duy nhất cho bất đồng từ 120 scalar đã lưu. Cần kiểm marker và hiệu chuẩn/alias trên video liên tục hoặc encoder độc lập; H1 vẫn thiếu góc vật lý.
