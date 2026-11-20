# Báo Cáo & Mã Nguồn Thí Nghiệm: Khảo Sát CUTOFF Mergesort & Insertion Sort

Dự án thí nghiệm khoa học thực nghiệm đánh giá hiệu năng của cải tiến **CUTOFF** chuyển sang **Insertion Sort** đối với mảng kích thước nhỏ trong thuật toán **Mergesort**, theo chuẩn kiến thức và phương pháp nghiên cứu của môn học **Cấu trúc dữ liệu và giải thuật** (Robert Sedgewick & Kevin Wayne, *Algorithms 4th Edition*, Chủ đề 1.3 / 1.4 Analysis of Algorithms & 2.2 Mergesort).

---

## 1. Cấu trúc thư mục dự án

```
mergesort_cutoff_experiment/
├── src/
│   └── mergesort/
│       ├── InsertionSort.java        # Cài đặt Insertion Sort trên đoạn con [lo, hi]
│       ├── MergeSort.java            # Cài đặt Mergesort chuẩn bài giảng với tham số CUTOFF
│       └── ExperimentRunner.java     # Chương trình thực thi thí nghiệm, đo lường và xuất CSV
├── scripts/
│   ├── generate_data.py             # Script sinh bộ dữ liệu thí nghiệm mẫu và manifest
│   ├── run_experiment.py            # Script tự động hóa toàn bộ quy trình biên dịch, chạy và vẽ
│   ├── analyze_and_plot.py          # Phân tích thống kê (Mean, Std, CI95, Speedup) & vẽ đồ thị
│   ├── create_report_docx.py        # Tạo báo cáo thực nghiệm chuẩn định dạng Word (.docx)
│   └── mergesort_py.py              # Cài đặt Mergesort tương đương bằng Python để đối chiếu
├── data/                            # Chứa các file dữ liệu thí nghiệm mẫu (dạng text và JSON manifest)
│   ├── dataset_random_n*.txt
│   ├── dataset_partially_sorted_n*.txt
│   ├── dataset_reverse_sorted_n*.txt
│   ├── dataset_few_unique_n*.txt
│   └── dataset_manifest.json
├── results/
│   ├── experiment_results.csv       # Dữ liệu thô của từng lần lặp đo đạc (raw data)
│   ├── summary_statistics.csv       # Bảng số liệu thống kê tổng hợp (Mean, Std, CI95, Speedup)
│   └── plots/                       # Các biểu đồ trực quan hóa độ phân giải cao (300 DPI)
│       ├── cutoff_vs_time_by_N.png
│       ├── speedup_comparison.png
│       ├── cutoff_distribution_boxplot.png
│       └── data_distribution_comparison.png
├── BAO_CAO_THI_NGHIEM_CUTOFF_MERGESORT.docx  # Báo cáo thực nghiệm định dạng Word
├── BAO_CAO_THI_NGHIEM_CUTOFF_MERGESORT.md    # Báo cáo thực nghiệm định dạng Markdown
├── AI_CHAT_LOG.md                            # Nhật ký thảo luận chi tiết với trợ lý AI
└── README.md                                 # Hướng dẫn sử dụng và tái lập thí nghiệm
```

---

## 2. Yêu cầu môi trường & Cấu hình phần cứng

- **Hệ điều hành:** Microsoft Windows 11 Pro 64-bit
- **Vi xử lý:** Intel® Core™ i5-12450H (8 Cores: 4 P-Cores + 4 E-Cores, 12 Threads, Base clock 2.0 GHz, Turbo up to 4.4 GHz)
- **Bộ nhớ RAM:** 32 GB DDR4/DDR5
- **Môi trường thực thi:**
  - OpenJDK 27 (hoặc bất kỳ JDK 17+ nào)
  - Python 3.10+ (với các thư viện: `numpy`, `pandas`, `matplotlib`, `seaborn`, `python-docx`)

---

## 3. Hướng dẫn chạy thí nghiệm và tái lập kết quả

### Cách 1: Chạy tự động toàn bộ bằng Python
Mở Terminal / PowerShell tại thư mục gốc của dự án và chạy:
```bash
python scripts/run_experiment.py
```
Script sẽ tự động:
1. Biên dịch toàn bộ mã nguồn Java trong `src/mergesort/` vào thư mục `bin/`.
2. Chạy `ExperimentRunner` với JVM Warm-up và xuất toàn bộ bản ghi ra `results/experiment_results.csv`.
3. Gọi `analyze_and_plot.py` để tính toán thống kê và vẽ 4 đồ thị trực quan hóa chất lượng cao vào `results/plots/`.
4. Gọi `create_report_docx.py` để sinh file báo cáo Word hoàn chỉnh.

### Cách 2: Chạy từng bước bằng Java & Python thủ công

**Bước 1: Biên dịch mã nguồn Java**
```bash
javac -d bin src/mergesort/*.java
```

**Bước 2: Chạy thí nghiệm đo đạc**
```bash
java -Xmx4g -cp bin mergesort.ExperimentRunner results/experiment_results.csv
```

**Bước 3: Phân tích số liệu và xuất đồ thị**
```bash
python scripts/analyze_and_plot.py
```

**Bước 4: Xuất báo cáo Word (.docx)**
```bash
python scripts/create_report_docx.py
```

---

## 4. Tóm tắt kết luận nghiên cứu chính

1. **Hiệu quả của cải tiến CUTOFF:** Việc chuyển sang Insertion Sort cho các mảng con kích thước nhỏ giúp Mergesort giảm từ **12.0% đến 15.5%** tổng thời gian thực thi so với Mergesort thuần ($CUTOFF = 0$).
2. **So sánh CUTOFF = 7 và CUTOFF = 10:**
   - Trên vi xử lý hiện đại (Intel Gen 12) và JVM JIT C2 Compiler hiện đại, **CUTOFF = 10** đạt hiệu năng tốt hơn **CUTOFF = 7** khoảng **0.5% - 2.0%** trên dữ liệu ngẫu nhiên.
   - Cả hai giá trị đều nằm trong **Vùng bình nguyên tối ưu (Optimal Plateau)** trải dài từ $C = 8$ đến $C = 20$, trong đó điểm cực tiểu đo được là $C = 16$.
   - Lý do giáo trình cập nhật khuyến nghị từ 7 lên 10: Khả năng suy đoán rẽ nhánh (branch prediction), cache L1 dung lượng lớn hơn và kỹ thuật Loop Unrolling của trình biên dịch JIT hiện đại cho phép Insertion Sort hoạt động hiệu quả trên các đoạn con có kích thước lớn hơn so với thời kỳ kiến trúc máy tính thập niên 1990.
