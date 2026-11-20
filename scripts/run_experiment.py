"""
Script điều khiển toàn bộ quy trình thí nghiệm:
1. Biên dịch mã nguồn Java
2. Chạy thí nghiệm Java ExperimentRunner và xuất kết quả CSV
3. Chạy phân tích thống kê và vẽ biểu đồ kết quả
4. Tổng hợp báo cáo
"""

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JDK_BIN = r"C:\Users\tienh\.jdks\openjdk-27\bin"
JAVAC = os.path.join(JDK_BIN, "javac.exe")
JAVA = os.path.join(JDK_BIN, "java.exe")

def run():
    print("=== BẮT ĐẦU QUY TRÌNH THÍ NGHIỆM TỰ ĐỘNG ===")
    os.chdir(BASE_DIR)

    # 1. Biên dịch Java
    print("\n[Bước 1] Biên dịch mã nguồn Java...")
    os.makedirs(os.path.join(BASE_DIR, "bin"), exist_ok=True)
    compile_cmd = [JAVAC, "-d", "bin", "src/mergesort/InsertionSort.java", "src/mergesort/MergeSort.java", "src/mergesort/ExperimentRunner.java"]
    res = subprocess.run(compile_cmd)
    if res.returncode != 0:
        print("Lỗi biên dịch Java!")
        sys.exit(1)
    print("Biên dịch thành công!")

    # 2. Chạy thí nghiệm
    print("\n[Bước 2] Thực thi thí nghiệm Java (ExperimentRunner)...")
    res_csv = os.path.join(BASE_DIR, "results", "experiment_results.csv")
    java_cmd = [JAVA, "-Xmx4g", "-cp", "bin", "mergesort.ExperimentRunner", res_csv]
    res = subprocess.run(java_cmd)
    if res.returncode != 0:
        print("Lỗi chạy thí nghiệm Java!")
        sys.exit(1)

    # 3. Phân tích và vẽ đồ thị
    print("\n[Bước 3] Phân tích số liệu và xuất đồ thị trực quan...")
    plot_script = os.path.join(BASE_DIR, "scripts", "analyze_and_plot.py")
    subprocess.run([sys.executable, plot_script])

    print("\n=== HOÀN TẤT TOÀN BỘ QUY TRÌNH THÍ NGHIỆM! ===")

if __name__ == "__main__":
    run()
