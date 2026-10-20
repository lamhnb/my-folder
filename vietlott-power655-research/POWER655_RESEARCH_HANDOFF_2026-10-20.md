# Power 6/55 — Hồ sơ nghiên cứu và bàn giao
**20/10/2026 · Bản 1.0 · Đọc kỹ trước khi tiếp tục**

## Mục tiêu và dữ liệu
Người dùng **chỉ mua sáu vé mỗi kỳ**. Các tập 20/50/100/200 vé là công cụ quan sát để tìm ra điều B1 còn thiếu, không phải tăng ngân sách, không phải chọn sáu vé từ 20 ngay. Phải dùng strict-past: kỳ t chỉ nhìn các kỳ <t, tạo vé, mở kết quả, cập nhật rồi sang t+1. Phải tách backtest khám phá với kiểm định tương lai; không gọi pattern hậu nghiệm là tín hiệu dự báo.

Nguồn đã dùng: `vietvudanh/vietlott-data/data/power655.jsonl`, đến kỳ #01413 ngày 20/10/2026, 1.413 kỳ trong dataset. Các đoạn 156 kỳ (~1 năm lịch quay), 312 kỳ (19/10/2024–20/10/2026), 624 kỳ (15/10/2022–20/10/2026). Rolling-156 = 156 kỳ, không phải ngày. `result[:6]` là sáu số chính. Jackpot 1 = đúng 6/6; Jackpot 2 còn cần số đặc biệt, phần lớn backtest cũ chưa kiểm tra số đặc biệt.

## GitHub và các phiên bản đã lưu
Repo `lamhnb/my-folder`, thư mục `vietlott-power655-research/`. Các file sau đã được đọc lại qua GitHub:
- A1 v1.0.0: `frequency_a1_stride_v1.py`, commit được báo cáo `2b2586e`.
- **B1 v1.0.0**: `frequency_b1_rolling156_v1.py`, commit `528bbeb`. Baseline tốt nhất **trong nhánh Frequency** theo số kỳ ≥3/6 được báo cáo.
- C50 v1.0.0: `frequency_c50_hybrid_v1.py`, commit `092d8463cb82dd27e2ea5aa0940f5a12856a5832`.
- B7-100 original snapshot v0.1.0: `b7_100_original_snapshot_v0_1.py`, commit `061ac07e40fa458291c2039a83205e72e840e620`. Cần audit tái lập.
- B7-200 v0.2.0: `b7_200_coverage_v0_2.py`, commit `d0d3aa65f8566e9b2f710dca060b204856a6dad8`. Đã commit code, **chưa có backtest trực tiếp 624 kỳ hoàn chỉnh**.
Không nhầm B1 với Champion Pair-60/Stride-365 của nhánh khác. Kết quả tính trong chat không tự động là log chạy file Python GitHub.

## Quá trình từ đầu đến B1
Ban đầu đã thử nóng/lạnh, cặp đồng xuất hiện, mạng Pair→kỳ sau, span/gap và số trùng liên kỳ. Cặp 07–31, 13–55, 08–39 từng nổi bật nhưng chọn bằng dữ liệu rồi kiểm tra lại gây selection bias. Mạng chuyển tiếp strict-past 156 kỳ báo cáo 94 lượt số trùng so baseline 101: không có tín hiệu ổn định.

Một thử nghiệm Adaptive Frequency 12 chiến lược Hot/Cold, cửa sổ 30/60/90/180/365/toàn lịch sử, train 40 kỳ rồi test 20 kỳ đạt 0,30 trùng/kỳ ở test. **Người dùng bác bỏ cách chia train/test đó**; yêu cầu đúng là che đoạn một năm, chọn sáu dãy, mở từng kỳ, cập nhật rồi chọn lại liên tục.

Top-6 tổ hợp theo tổng tần suất tạo sáu vé chia sẻ năm số lõi, báo cáo 156 kỳ chỉ 7 kỳ ≥3/6, 0 kỳ ≥4/6. Bài học: tối ưu score từng vé khác tối ưu danh mục.

**A1:** Đếm tần suất toàn lịch sử trước t; xếp giảm, hòa ưu tiên số nhỏ; lấy top 36; chia Stride: vé 1 nhận hạng 1,7,13,19,25,31; vé 2 nhận 2,8,14,20,26,32; ...; vé 6 nhận 6,12,18,24,30,36. Sáu vé không trùng số. 156 kỳ: 15 kỳ ≥3/6, 0 kỳ ≥4/6, coverage 616. A2 Block đạt 14 kỳ ≥3/6; A3 chia ngẫu nhiên cùng 36 số đạt 15.

**B1:** Giữ Stride, thay toàn lịch sử bằng tần suất **156 kỳ trước t**. Kết quả được báo cáo:
| Đoạn | Kỳ ≥3/6 | Kỳ ≥4/6 | Coverage |
|---|---:|---:|---:|
| 156 kỳ gần nhất | 18 | 1 | 623 |
| 312 kỳ | 32 | 2 | 1.230 |
| 624 kỳ | 59 | 5 | 2.458 |
Histogram best-hit 624 kỳ: 0:0, 1:227, 2:338, 3:54, 4:5, 5:0, 6:0. Hai nửa 312 kỳ: 27 và 32 kỳ ≥3/6. **Chưa chứng minh hơn sáu vé ngẫu nhiên rời nhau.**

## B2, B3, B3.1, B4
**B2:** Giữ top 36 B1, học các vị trí rank hay đồng xuất hiện trong 156 kỳ trước rồi greedy ghép vé. 312 kỳ: 30 kỳ ≥3/6, 1 kỳ ≥4/6 so B1 32 và 2. Chỉ 4 kỳ hai bên cùng ≥3/6; 28 kỳ chỉ B1, 26 kỳ chỉ B2. Hợp 58 kỳ là **oracle nhìn trước**, không phải sáu vé có thể chọn trước.

**B3:** Ba vé B1 + ba vé B2; chỉ trung bình 29,51 số khác nhau/kỳ vì trùng số, coverage 996 so 1.230, 312 kỳ đạt 31 kỳ ≥3/6, 1 kỳ ≥4/6. **B3.1** điền số thiếu để đủ 36, coverage phục hồi nhưng vẫn 31 và 1.

**B4:** Chọn B2 nếu trong 156 kỳ trước B2 hơn B1 ít nhất bốn kỳ đạt ≥3/6; ngược lại B1. 312 kỳ: 29 kỳ ≥3/6, 2 kỳ ≥4/6; chọn B1 221 kỳ, B2 91 kỳ. Ngưỡng bốn là heuristic chưa hiệu chuẩn.

## C50 và bù trừ
`Score_i=(1-alpha)*freq_all_i/n_all+alpha*freq_156_i/156`; C25 alpha .25, C50 .50, C75 .75; top 36 + Stride. Trên 312 kỳ: A1 25 kỳ ≥3/6 và 0 kỳ ≥4/6; B1 32/2; C25 24/2; **C50 23/3**; C75 25/0.

C50 đạt 4/6 tại #01102 19/10/2024, #01117 23/11/2024, #01293 10/01/2026; B1 chỉ 2/6 ở các kỳ đó. Hai bên vẫn chọn chung 35/36, 34/36, 33/36 số. Thắng khác nhau do rank modulo 6 gom số đúng cùng vé. B1 có kỳ 4/6 riêng #01198 03/06/2025 và #01320 17/03/2026. Đây là giải thích hậu nghiệm, chưa phải tín hiệu dự báo.

**Stable/Moved/Exclusive:** Stable = số chung cùng nhãn vé; Moved = số chung khác nhãn; Exclusive = chỉ một bên chọn. 312 kỳ mới: Stable TB 6,40 số, Moved 27,19, Exclusive 4,81; tỷ lệ xuất hiện Stable 11,66%, Moved 10,75%. 312 kỳ cũ: Stable 11,32%, Moved 10,86%. Chia 624 kỳ tám đoạn, Stable hơn Moved 5/8 đoạn; z≈1,25, khoảng tin cậy chứa 0. **Nhãn vé là tùy ý**, phải căn chỉnh nhãn hoặc dùng quan hệ cặp cùng vé. Stable-first/last 624 kỳ chỉ 52 kỳ ≥3/6, 1 kỳ ≥4/6.

**B5:** Bù trừ theo 10/25/50% số bất đồng rank; 624 kỳ B1 59 kỳ ≥3/6, C50 51, B5-10 57, B5-25 56, B5-50 50. Audit phát hiện B5-10 có 195/624 kỳ không đổi vị trí; B5-50 thay nhiều nhưng không thực sự tiến gần phân hoạch C50. B5 sai thiết kế.

**B5.1:** Greedy swap giữa các vé B1 để tăng cặp cùng vé đồng thuận với C50 (không phụ thuộc nhãn). 624 kỳ:
| Model | ≥2/6 | ≥3/6 | ≥4/6 |
|---|---:|---:|---:|
| B1 | 397 | 59 | 5 |
| C50 | 388 | 51 | 4 |
| B5.1 1 swap | 401 | 53 | 6 |
| B5.1 3 swaps | 394 | 50 | 5 |
| B5.1 6 swaps | 411 | 53 | 3 |
Đồng thuận phân hoạch tăng nhưng tỷ lệ đạt giải không tăng. Không nâng cấp.

## B6 — mở rộng 20/50/100 ứng viên
Giữ sáu vé B1 đầu, tạo thêm vé bằng biến đổi Stride trên cùng top 36. Kết quả được báo cáo trên 624 kỳ:
| Ứng viên/kỳ | Kỳ ≥3/6 | Kỳ ≥4/6 | Kỳ ≥5/6 |
|---|---:|---:|---:|
| B1-6 | 59 | 5 | 0 |
| B6-20 | 162 | 8 | 0 |
| B6-50 | 258 | 21 | 0 |
| B6-100 | 339 | 41 | 0 |
Nhiều ứng viên hơn có nhiều cơ hội trúng hơn, không chứng minh sáu vé tốt hơn. Một lần thử học chọn 6/20 chỉ đạt 49 kỳ ≥3/6 so B1 59; **đó không phải mục tiêu người dùng**.

Coverage của top 36 B1 trong 624 kỳ: số đúng nằm trong top 36 bằng 0:0 kỳ, 1:5, 2:50, 3:156, 4:211, 5:171, 6:31. Có 202 kỳ coverage ≥5, trong đó 31 kỳ đủ 6 số. `C(36,5)=376992`; 100 vé chỉ có tối đa 600 bộ năm khác nhau, tương đương 0,159% không gian bộ năm.

## B7-100 — phát hiện 5/6 nhưng chưa tái lập
B7 giữ sáu vé B1, tạo 94 vé bổ sung bằng greedy coverage bộ 4/3/2, 70 trial mỗi vé, LCG seed `712345`. Một phép tính trong chat từng báo cáo 624 kỳ: **377 kỳ ≥3/6, 32 kỳ ≥4/6, 3 kỳ ≥5/6**:
- #01275, 29/11/2025, vé #12: `20 24 27 40 41 48` hit 5.
- #01292, 08/01/2026, vé #78: `20 22 27 36 43 45` hit 5.
- #01355, 06/06/2026, vé #97: `03 11 16 39 40 41` hit 5.

**Không được coi ba kỳ 5/6 là đã xác minh.** Các lần tái triển khai sau thay hệ biểu diễn số thật/rank 0–35, seed liên tục/seed theo kỳ, 70/16 trial; kết quả 5/6 biến mất, có bản 35 hoặc 48 kỳ ≥4/6. Không được quy sự khác biệt cho một nguyên nhân khi đổi nhiều biến cùng lúc. Snapshot gốc đã commit còn nguy cơ trộn hệ tọa độ giữa sáu vé seed và 94 vé greedy; phải đối chiếu chính xác logic gốc, seed, PRNG, mapping và hash từng vé.

Các thử nghiệm momentum/reversion/rank-interleave trên 312 kỳ kiểm định: B1 32 kỳ ≥3/6, Momentum 26, Reversion 26, Interleave 22. Các tín hiệu ranking/Stable chưa đủ bằng chứng độc lập.

## B7-200 và Jackpot
`b7_200_coverage_v0_2.py` đã commit: 200 vé, sáu vé đầu B1, 194 vé greedy bổ sung, **70 trial cho từng vé**, rank 0–35 nhất quán, seed theo ID kỳ, cập nhật coverage toàn danh mục và kiểm tra 200 vé khác nhau. Đây là greedy tuần tự, chưa tối ưu toàn cục 200 vé. 100 vé đầu **không nhất thiết trùng B7-100 gốc** do thay seed/hệ tọa độ. Backtest 624 kỳ trực tiếp file Python **chưa hoàn tất** (đã gặp timeout và hạn chế môi trường). Chỉ biết 31 kỳ top 36 chứa đủ sáu số chính; số Jackpot 1 và Jackpot 2 thực tế của B7-200 **chưa xác định**, không phải 0.

## Những việc bắt buộc làm tiếp
1. Pin dataset SHA256, code commit SHA, Python version, seed; xác minh thứ tự kỳ, số đặc biệt, dữ liệu hợp lệ.
2. Chạy trực tiếp A1/B1/C50 và xuất log per-draw: rank, 36 số, mọi vé, hits, coverage; so với các mốc báo cáo. Khi lệch, ghi nguyên nhân trước khi nghiên cứu.
3. **Ablation B7-100:** giữ gốc + continuous seed + 70 trials; chỉ đổi hệ tọa độ; chỉ đổi seed; chỉ đổi số trial. So từng vé và ba kỳ từng báo 5/6. Không thay nhiều biến cùng lúc.
4. Chạy trực tiếp B7-200 đủ 624 kỳ, so 6/100/200 vé **trong cùng một run**, chấm ≥3/4/5/6 và Jackpot 2 với số đặc biệt. Nếu tối ưu hiệu năng bằng bitmask/cached combinations, phải kiểm tra output tương đương bản chuẩn.
5. Nghiên cứu trực tiếp đặc trưng 100 ứng viên trước kỳ quay: ranking, gap, đồng thuận B1/C50, coverage, vị trí số đúng bị phân tán; phân biệt feature biết trước với label chỉ biết sau. Khóa quy tắc trên discovery, kiểm định temporal holdout và random benchmark cùng số vé.
6. Chỉ nâng phiên bản nếu sáu vé cuối cùng vượt B1 và benchmark ở mục tiêu định trước; giữ B1 v1.0.0 và C50 v1.0.0 bất biến đến lúc đó.

**Kết luận trạng thái:** B1 là baseline nhánh Frequency đáng giữ nhất; C50 là nhánh nghiên cứu về rank/ghép vé; B7-100 là snapshot có ba kỳ 5/6 được báo cáo nhưng chưa tái lập; B7-200 mới commit mã, chưa xác nhận Jackpot. Không có bằng chứng thống kê chắc chắn rằng hệ thống dự đoán được kết quả quay công bằng.
