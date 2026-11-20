"""
Script phân tích số liệu thực nghiệm và vẽ biểu đồ trực quan hóa kết quả tìm CUTOFF Mergesort.
Thực hiện các phân tích thống kê theo chuẩn chủ đề 1.3 / 1.4 Analysis of Algorithms:
- Thống kê mô tả: Mean, Standard Deviation, Median, Min, Max, 95% Confidence Interval (Khoảng tin cậy).
- Tính toán % cải thiện tốc độ (Speedup) so với Mergesort thuần (CUTOFF = 0).
- Trực quan hóa:
  + Đồ thị Thời gian thực thi theo CUTOFF cho các kích thước N (có đánh dấu CUTOFF=7 và CUTOFF=10).
  + Đồ thị Tỉ lệ cải thiện tốc độ (%) theo CUTOFF.
  + Biểu đồ hộp (Boxplot) phân tích độ ổn định và phân tán của thời gian chạy qua các lần lặp.
  + Đồ thị so sánh hành vi trên 4 phân phối dữ liệu (Random, Partially Sorted, Reverse, Few Unique).
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

CSV_FILE = os.path.join(RESULTS_DIR, "experiment_results.csv")
SUMMARY_CSV = os.path.join(RESULTS_DIR, "summary_statistics.csv")

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 11

def analyze_and_plot():
    if not os.path.exists(CSV_FILE):
        print(f"File {CSV_FILE} chưa tồn tại!")
        return

    df = pd.read_csv(CSV_FILE)
    print(f"Đã đọc {len(df):,} bản ghi từ {CSV_FILE}")

    # 1. Thống kê tổng hợp (Summary Statistics)
    grouped = df.groupby(['distribution', 'n', 'cutoff'])['time_ms']
    summary = grouped.agg(
        mean='mean',
        std='std',
        median='median',
        min='min',
        max='max',
        count='count'
    ).reset_index()

    # Tính khoảng tin cậy 95% (t-distribution approx with 1.96 / sqrt(n) or standard error)
    # Với n = 10 (df = 9), t_crit = 2.262
    t_crit = 2.262
    summary['ci95'] = t_crit * (summary['std'] / np.sqrt(summary['count']))

    # Tính speedup so với cutoff = 0
    baseline_map = {}
    for _, row in summary[summary['cutoff'] == 0].iterrows():
        baseline_map[(row['distribution'], row['n'])] = row['mean']

    summary['baseline_mean'] = summary.apply(lambda row: baseline_map.get((row['distribution'], row['n']), row['mean']), axis=1)
    summary['speedup_percent'] = ((summary['baseline_mean'] - summary['mean']) / summary['baseline_mean']) * 100.0

    summary.to_csv(SUMMARY_CSV, index=False)
    print(f"Đã lưu bảng thống kê tổng hợp tại: {SUMMARY_CSV}")

    # 2. Đồ thị 1: Thời gian thực thi theo CUTOFF cho dữ liệu RANDOM qua các giá trị N
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    rand_summary = summary[summary['distribution'] == 'RANDOM']

    sizes = sorted(rand_summary['n'].unique())
    colors = sns.color_palette("tab10", len(sizes))

    for idx, n_val in enumerate(sizes):
        sub = rand_summary[rand_summary['n'] == n_val].sort_values('cutoff')
        ax.errorbar(
            sub['cutoff'], sub['mean'], yerr=sub['ci95'],
            fmt='-o', color=colors[idx], label=f'N = {n_val:,}',
            capsize=3, capthick=1, markersize=5, linewidth=1.8
        )
        # Tìm điểm cực tiểu
        min_row = sub.loc[sub['mean'].idxmin()]
        ax.plot(min_row['cutoff'], min_row['mean'], marker='*', markersize=12, color='red', zorder=5)

    ax.axvline(x=7, color='orange', linestyle='--', alpha=0.7, label='CUTOFF = 7 (Giáo trình cũ)')
    ax.axvline(x=10, color='purple', linestyle='--', alpha=0.7, label='CUTOFF = 10 (Slide mới)')

    ax.set_title('Ảnh hưởng của CUTOFF đến thời gian thực thi Mergesort (Dữ liệu RANDOM)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Giá trị CUTOFF (ngưỡng chuyển sang Insertion Sort)', fontsize=11)
    ax.set_ylabel('Thời gian thực thi trung bình (ms)', fontsize=11)
    ax.set_xticks(sorted(rand_summary['cutoff'].unique()))
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    plot1_path = os.path.join(PLOTS_DIR, 'cutoff_vs_time_by_N.png')
    plt.savefig(plot1_path)
    plt.close()
    print(f"Đã lưu biểu đồ: {plot1_path}")

    # 3. Đồ thị 2: Phần trăm cải thiện tốc độ (Speedup %) theo CUTOFF
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    for idx, n_val in enumerate(sizes):
        sub = rand_summary[rand_summary['n'] == n_val].sort_values('cutoff')
        ax.plot(sub['cutoff'], sub['speedup_percent'], '-s', color=colors[idx], label=f'N = {n_val:,}', linewidth=2, markersize=5)

    ax.axhline(0, color='black', linestyle=':', linewidth=1)
    ax.axvline(x=7, color='orange', linestyle='--', alpha=0.8, label='CUTOFF = 7')
    ax.axvline(x=10, color='purple', linestyle='--', alpha=0.8, label='CUTOFF = 10')

    ax.set_title('Tỉ lệ cải thiện tốc độ (% Speedup) so với Mergesort thuần (CUTOFF = 0)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Giá trị CUTOFF', fontsize=11)
    ax.set_ylabel('Cải thiện tốc độ (%)', fontsize=11)
    ax.set_xticks(sorted(rand_summary['cutoff'].unique()))
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    plot2_path = os.path.join(PLOTS_DIR, 'speedup_comparison.png')
    plt.savefig(plot2_path)
    plt.close()
    print(f"Đã lưu biểu đồ: {plot2_path}")

    # 4. Đồ thị 3: Boxplot phân tán thời gian chạy tại N lớn nhất (N = 1,000,000)
    max_n = max(sizes)
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    sub_raw = df[(df['distribution'] == 'RANDOM') & (df['n'] == max_n)]

    sns.boxplot(x='cutoff', y='time_ms', data=sub_raw, ax=ax, palette='crest', hue='cutoff', legend=False)
    ax.set_title(f'Phân bố thời gian thực thi qua các lần lặp (N = {max_n:,}, RANDOM)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Giá trị CUTOFF', fontsize=11)
    ax.set_ylabel('Thời gian thực thi (ms)', fontsize=11)
    plt.tight_layout()
    plot3_path = os.path.join(PLOTS_DIR, 'cutoff_distribution_boxplot.png')
    plt.savefig(plot3_path)
    plt.close()
    print(f"Đã lưu biểu đồ: {plot3_path}")

    # 5. Đồ thị 4: So sánh hành vi trên 4 phân phối dữ liệu tại N = 500,000
    eval_n = 500000 if 500000 in sizes else max_n
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    dist_summary = summary[summary['n'] == eval_n]

    dist_colors = {'RANDOM': '#1f77b4', 'PARTIALLY_SORTED': '#2ca02c', 'REVERSE_SORTED': '#d62728', 'FEW_UNIQUE': '#9467bd'}
    for dist_name in df['distribution'].unique():
        sub = dist_summary[dist_summary['distribution'] == dist_name].sort_values('cutoff')
        if not sub.empty:
            ax.plot(sub['cutoff'], sub['mean'], '-o', color=dist_colors.get(dist_name, 'gray'),
                    label=f'{dist_name}', linewidth=2, markersize=5)

    ax.axvline(x=7, color='orange', linestyle='--', alpha=0.7, label='CUTOFF = 7')
    ax.axvline(x=10, color='purple', linestyle='--', alpha=0.7, label='CUTOFF = 10')
    ax.set_title(f'So sánh hành vi CUTOFF trên 4 phân phối dữ liệu khác nhau (N = {eval_n:,})', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Giá trị CUTOFF', fontsize=11)
    ax.set_ylabel('Thời gian thực thi trung bình (ms)', fontsize=11)
    ax.set_xticks(sorted(rand_summary['cutoff'].unique()))
    ax.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()
    plot4_path = os.path.join(PLOTS_DIR, 'data_distribution_comparison.png')
    plt.savefig(plot4_path)
    plt.close()
    print(f"Đã lưu biểu đồ: {plot4_path}")

    # In phân tích so sánh trực tiếp CUTOFF 7 vs CUTOFF 10
    print("\n================== SO SÁNH TRỰC DIỆN: CUTOFF = 7 vs CUTOFF = 10 ==================")
    for dist_name in df['distribution'].unique():
        print(f"\nPhân phối: {dist_name}")
        for n_val in sorted(summary[summary['distribution'] == dist_name]['n'].unique()):
            sub = summary[(summary['distribution'] == dist_name) & (summary['n'] == n_val)]
            if sub.empty or len(sub[sub['cutoff'] == 0]) == 0:
                continue
            c0 = sub[sub['cutoff'] == 0]['mean'].values[0] if len(sub[sub['cutoff'] == 0]) > 0 else 0
            c7 = sub[sub['cutoff'] == 7]['mean'].values[0] if len(sub[sub['cutoff'] == 7]) > 0 else 0
            c10 = sub[sub['cutoff'] == 10]['mean'].values[0] if len(sub[sub['cutoff'] == 10]) > 0 else 0
            best_row = sub.loc[sub['mean'].idxmin()]
            best_c = int(best_row['cutoff'])
            best_t = best_row['mean']

            sp7 = ((c0 - c7) / c0) * 100 if c0 > 0 else 0
            sp10 = ((c0 - c10) / c0) * 100 if c0 > 0 else 0
            sp_best = ((c0 - best_t) / c0) * 100 if c0 > 0 else 0

            print(f"  N = {n_val:>9,}: Thuần={c0:>7.2f}ms | C=7: {c7:>7.2f}ms (+{sp7:5.1f}%) | C=10: {c10:>7.2f}ms (+{sp10:5.1f}%) | TỐI ƯU: C={best_c:>2} ({best_t:>7.2f}ms, +{sp_best:5.1f}%)")

if __name__ == "__main__":
    analyze_and_plot()
