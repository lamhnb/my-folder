# Power 6/55 — simulator vật lý 3D cho nghiên cứu

**Mô hình cơ khí giả định có kiểm thử, chưa phải bản sao 1:1 của máy Vietlott. Không có lợi thế dự báo được chứng minh.** Dùng PyBullet, 55 rigid spheres, khoang cầu có cửa vật lý, ba tay gạt truyền động qua khớp quay, hai cửa trượt có trạng thái, túi giữ, rãnh dốc và chốt giữ special. Bóng được thu khi đi qua cơ cấu và tiếp xúc rãnh; không chọn bóng gần cửa tại timestamp.

Đọc [FINAL_DIGITAL_TWIN_HANDOFF.md](FINAL_DIGITAL_TWIN_HANDOFF.md), [parameter_registry.csv](parameter_registry.csv), [source_review.md](source_review.md) và [validation/README.md](validation/README.md) trước khi diễn giải kết quả. Bản chạy này kế thừa Phase 4 `f329cab`; không sửa các phiên bản A1/B1/C50/B7/Champion hoặc dữ liệu Phase 1–3.

## Cài đặt

Đã chạy với **Python 3.11.15**, Windows x64, PyBullet 3.2.7. Phiên bản và hash binary thực tế ở [results/runtime.json](results/runtime.json). PyBullet có thể phải biên dịch C++ trên Windows; lần cài trong môi trường này đã biên dịch thành công. Không cần GPU, GUI, dữ liệu video hoặc tài khoản ngoài để chạy simulator.

```powershell
cd C:\vietlott-research-repo\vietlott-power655-physical-research\digital-twin
uv venv --python 3.11 .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
$py = '.venv\Scripts\python.exe'
```

Trong workspace đã cài sẵn có thể dùng `$py = 'C:\vietlott-digital-twin-env\Scripts\python.exe'`.

## Các lệnh chính

```powershell
# Một seed và quỹ đạo đầy đủ 55 bóng ở các thời điểm lấy mẫu
& $py scripts/cli.py run --seed 0 --config configs/baseline.json --out results/seed0.json --trajectory results/seed0.npz

# Unit tests; numerical validation; physical validation của khoang 55 bóng và jam
& $py -m pytest -q tests
& $py scripts/cli.py validate

# Monte Carlo một cấu hình; chỉ chạy sau khi hai validation gate đã qua
& $py scripts/cli.py monte-carlo --seeds 20 --start 1000 --out results/monte_carlo.json

# Bộ 78 lần chạy / 23 cấu hình, 8 process: baseline, sensitivity, convergence, metamorphic checks
& $py scripts/cli.py experiment

# Quỹ đạo CSV, GIF 3D và ảnh PNG từ trạng thái đã lưu
& $py scripts/cli.py export-tracks --trajectory results/seed0.npz --out results/trajectory_seed0.csv
& $py scripts/cli.py render --trajectory results/seed0.npz --out renders/seed0.gif
& $py -m scripts.collector_figure

# Calibration mô tả/identifiability từ bảng Phase 2, không đọc số trúng
& $py scripts/cli.py calibrate

# Tạo biểu đồ và báo cáo thống kê từ các run JSON đã thực thi
& $py scripts/cli.py report
& $py scripts/build_handoff.py

# Hình học có tham số; inventory/registry và biểu đồ nguồn
& $py scripts/cli.py geometry
& $py -m scripts.mesh_quality
& $py scripts/research.py
& $py scripts/evidence_charts.py
& $py scripts/audit.py
```

Các lệnh ghi lại output cùng tên trong `digital-twin/`; dùng Git diff hoặc tên output khác khi so sánh tái lập. Byte hash của JSON chứa wall-clock runtime có thể thay đổi; phép tái lập động lực học so physical IDs, thời điểm và tọa độ với cùng binary/config/seed. Không hứa bit-identical giữa OS, CPU hoặc bản build Bullet khác nhau.

## Cấu hình và mô hình

Mọi độ dài theo m, khối lượng kg, thời gian s; tham số CLI `rpm` dùng vòng/phút, được đổi sang rad/s trong engine và registry. `diameter_tolerance` là ±tolerance của **đường kính**, bán kính được thay ±tolerance/2. `mass_tolerance` là ±kg. Hệ số per-body restitution/friction được Bullet kết hợp ở tiếp xúc; chúng chưa được đo trên máy thật. `linear_damping` và `rolling_friction` có kiểm soát, không thay cho một định luật vật liệu đã hiệu chuẩn.

Baseline dùng bán kính khoang 0,32 m, bóng radius 0,02525 m, mass 0,01234 kg, tốc độ yêu cầu 25 RPM và bước 0,0005 s; toàn bộ hình học, RPM, cửa và tiếp xúc là giả định. Ball nominal chỉ được ghi nhận từ quy định **2017**, chưa liên kết với bộ bóng 2026. Hai candidate 63,789/94,904 RPM không được dùng.

**Giới hạn đã đo trong mô phỏng:** motor baseline thường stall dưới tải; mean tốc độ đạt được post-ramp chỉ khoảng **5,124 RPM** trên20 seed, khác lệnh25 RPM. Vì vậy baseline chưa tái hiện/kiểm định được động lực học broadcast. `charts/motor_tracking.png` phân biệt lệnh và tốc độ đạt được; `results/torque_diagnostic/` giữ ba run stress mô-men bổ sung, tách khỏi78 run chính.

```powershell
# Diagnostic bổ sung sau khi phát hiện stall; không đổi baseline
& $py -m scripts.torque_diagnostic
```

Nhãn số là metadata gán ngẫu nhiên độc lập với seed vật lý/packing; không tác động lực. `label_shift` cho phép kiểm biến đổi nhãn; `reverse_insertion` kiểm thứ tự tạo body. Special chỉ bắt đầu sau sáu main; **49 trước special, 48 sau bảy lần thu**. Captured balls vẫn tồn tại và va chạm trong rãnh, không teleport/xóa/disable collision.

`configs/video_cadence.json` chỉ thay lịch yêu cầu bằng nhịp proxy downstream đã đo. Nó **không xác nhận chu kỳ điều khiển thật** và không hiệu chuẩn RPM, hình học hoặc xác suất. Baseline dùng chu kỳ 4 s để kiểm cơ cấu nhanh; không tuyên bố đó là nhịp của video.

## Bằng chứng và giới hạn

- Kết quả validation nằm trong `validation/`; run JSON, event CSV và trajectories trong `results/`.
- `charts/` và `renders/` là ảnh/GIF tự tạo từ dữ liệu số. Các chấm trong replay biểu diễn tâm bóng; kích thước marker không phải bản dựng quang học hoặc thước đo đường kính. Gate bevel được vẽ đơn giản hóa.
- `geometry/chamber.obj` là mesh va chạm giả định; `chamber_clean.obj` là bản hàn đỉnh cho CAD, không thay mesh của các run đã khóa. `mesh_quality.json` ghi kiểm manifold và sagitta của mặt cầu giả định. Các phần chuyển động được tạo có tham số trong `simulator/geometry.py` và `core.py`.
- Source video không nằm trong commit. Chạy mô phỏng/calibration bảng không cần video; tái đo hình học cần nguồn có hash đã pin, quyền sử dụng và camera calibration mới.
- Thiếu CAD/model/serial, RPM thật, bộ bóng/đặc tính từng bóng, control logs, camera đa góc đồng bộ và holdout chưa xem. Chưa tái hiện được động lực học máy thật hoặc chấm dự báo ngoài mẫu.

## Bố cục

`simulator/`: động lực học; `geometry/`: mesh/landmarks; `configs/`: giả định; `validation/`: bài thử số học/vật lý; `tests/`: unit tests; `calibration/`: timing và identifiability; `experiments/`: giao thức sweep; `scripts/`: CLI/replay/audit/report; `results/`, `charts/`, `renders/`: bằng chứng đã chạy.
