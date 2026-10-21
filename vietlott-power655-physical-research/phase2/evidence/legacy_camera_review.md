# Bổ sung kiểm toán camera trong đoạn thử RPM cũ

Đã xem lại contact sheet và bốn PNG **từ video thật mới giải mã bởi pipeline của parent**, cùng video IUU05082QtE, format137, tại PTS857.022833,858.023833,859.024833,860.025833. Preview full-frame cùng kích thước640×360, không crop; nguồn1920×1080 có SHA256 `c4740a0cbe28ea595ebb39487629a50b5bc8c7c88d91f777a4731660e07bce9c`.

**Quan sát:** phần đĩa trong suốt quanh trục nhỏ dần; ngày càng thấy nhiều vành khoang và sườn phải máy. Mép trong vành trắng cố định dịch sang trái rõ rệt trên ảnh. Bolt vẫn gần tâm ảnh; không cần giả định tâm dịch lớn để thấy tỷ lệ ảnh thay đổi.

**Ước lượng ảnh thủ công, cố ý lấy khoảng rộng:**

| PTS s | Khoảng bề rộng đĩa chiếu, pixel preview | Mép trong vành trắng tại y≈170, x pixel preview |
|---:|---:|---:|
|857.022833|175–210|590–607|
|858.023833|157–183|557–572|
|859.024833|137–162|526–542|
|860.025833|117–143|493–511|

Các khoảng này là biên ước lượng thị giác chủ quan, **không phải CI thống kê, sai số hiệu chuẩn hoặc kích thước vật lý**. Khoảng tỷ số bề rộng cuối/đầu bảo thủ là0.557–0.817: vật thể chiếu nhỏ đi khoảng18–44% theo các biên thô này. Mép vành trắng dịch khoảng79–114pixelpreview. Không dùng các số đó để suy ra tiêu cự, chuyển động camera hay đường kính thật.

**Hệ quả với code Phase1:** crop900×900, tâm(450,450) trong crop và annulus130–400pixel giữ cố định. Khi tỷ lệ ảnh thay đổi, annulus lấy các phần cấu trúc/ảnh khác nhau theo thời gian. Đây là bằng chứng thị giác thực về camera-image scale không ổn định, bổ sung cho giả thuyết nhiễu trước đây. Chưa tách camera khỏi bóng/mask/blur hoặc đo phần đóng góp vào chênh lệch63.789/94.904candidateRPM; không kết luận đây là nguyên nhân duy nhất.

Đã bổ sung phép đối chiếu bounded bằng `verify_legacy_crop_hashes.py`: giải mã đúng120crop900×900 tại(510,60), pixel formatBGR24, PTS857.022833–860.993467. **120/120SHA256crop và120/120PTS trùng dữ liệu Phase1**; không lưu lại120ảnh, không đổi ROI hoặc format để ép khớp. Vì vậy thay đổi tỷ lệ ảnh quanh đĩa trục thuộc chính buffer đầu vào đã tạo hai candidate cũ. `legacy_crop_hash_comparison.json` lưu nguồn, lệnh và kết quả. Điều này không chứng nhận mastercamera, SHA256videoPhase1đầy đủ, hay nguyên nhân duy nhất của chênh lệch.

Giữ **RPM/góc/chiều quay vật lý=NA**. Chưa có camera calibration, marker vật lý duy nhất hoặc nhánh alias độc lập. Hash trùng chứng nhận tính tái lập pixel/PTS của120crop, không xác nhận các phép suy luận vật lý.

Đây là bằng chứng bổ sung ở file riêng. `rpm_audit.py` vẫn chỉ tái tính scalar cũ và không giải mã video mới; các file audit cũ không bị ghi đè. Chi tiết tọa độ, giả định và SHA256 nằm trong `legacy_camera_review.json` và manifest nguồn `pretest_rotor_reference/frames.csv`.

```powershell
python phase2/scripts/verify_legacy_crop_hashes.py 'C:\vietlott-research-output\phase2-inputs\IUU05082QtE_f137_ranges.mp4'
```
