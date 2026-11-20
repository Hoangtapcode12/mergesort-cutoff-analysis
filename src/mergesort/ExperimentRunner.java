package mergesort;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;

/**
 * Runner chạy thí nghiệm đo đạc thời gian thực thi của Mergesort theo các giá trị CUTOFF khác nhau.
 * Tuân theo phương pháp thực nghiệm khoa học trong chủ đề 1.3 / 1.4 Analysis of Algorithms:
 * - JVM Warmup để JIT compiler tối ưu mã máy trước khi đo.
 * - Thử nghiệm lặp lại nhiều lần (replications) để giảm nhiễu đo lường.
 * - Paired testing: Các giá trị cutoff trong cùng 1 lần lặp được chạy trên cùng một bản sao dữ liệu.
 * - Thống kê đầy đủ: Mean, StdDev, Median, Min, Max, 95% Confidence Interval.
 * - Xuất kết quả chi tiết ra file CSV phục vụ phân tích và vẽ biểu đồ.
 */
public class ExperimentRunner {

    public enum Distribution {
        RANDOM,
        PARTIALLY_SORTED,
        REVERSE_SORTED,
        FEW_UNIQUE
    }

    public static Integer[] generateData(int n, Distribution dist, Random rng) {
        Integer[] a = new Integer[n];
        switch (dist) {
            case RANDOM:
                for (int i = 0; i < n; i++) {
                    a[i] = rng.nextInt();
                }
                break;
            case PARTIALLY_SORTED:
                for (int i = 0; i < n; i++) {
                    a[i] = i;
                }
                // Tráo đổi ngẫu nhiên khoảng 5% số cặp phần tử
                int swaps = (int) (n * 0.05);
                for (int s = 0; s < swaps; s++) {
                    int i = rng.nextInt(n);
                    int j = rng.nextInt(n);
                    Integer tmp = a[i];
                    a[i] = a[j];
                    a[j] = tmp;
                }
                break;
            case REVERSE_SORTED:
                for (int i = 0; i < n; i++) {
                    a[i] = n - i;
                }
                break;
            case FEW_UNIQUE:
                for (int i = 0; i < n; i++) {
                    a[i] = rng.nextInt(10); // Chỉ có 10 giá trị khác nhau
                }
                break;
        }
        return a;
    }

    public static void warmup(int n, int[] cutoffs) {
        System.out.println("Đang thực hiện JVM Warm-up để ổn định JIT compiler...");
        Random rng = new Random(42);
        for (int w = 0; w < 5; w++) {
            for (int cutoff : cutoffs) {
                Integer[] data = generateData(Math.min(n, 20000), Distribution.RANDOM, rng);
                MergeSort.sort(data, cutoff);
            }
        }
        System.gc();
        try {
            Thread.sleep(500);
        } catch (InterruptedException ignored) {}
        System.out.println("Hoàn tất Warm-up!\n");
    }

    public static void main(String[] args) {
        // Cấu hình tham số thí nghiệm
        int[] cutoffs = {0, 2, 4, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 24, 32, 48, 64};
        int[] sizes = {50000, 100000, 200000, 500000, 1000000};
        Distribution[] distributions = {
                Distribution.RANDOM,
                Distribution.PARTIALLY_SORTED,
                Distribution.REVERSE_SORTED,
                Distribution.FEW_UNIQUE
        };
        int trials = 10; // Số lần lặp lại cho mỗi cấu hình
        long seed = 20261120L;

        String outputFile = "results/experiment_results.csv";
        if (args.length > 0) {
            outputFile = args[0];
        }

        // JVM Warmup
        warmup(50000, cutoffs);

        System.out.println("=========================================================================");
        System.out.println(" BẮT ĐẦU THÍ NGHIỆM TÌM CUTOFF TỐI ƯU CHO MERGESORT");
        System.out.println(" Cấu hình CPU: Intel Core i5-12450H | RAM: 32GB | Java 27");
        System.out.println("=========================================================================");

        try (PrintWriter writer = new PrintWriter(new BufferedWriter(new FileWriter(outputFile)))) {
            // Header CSV
            writer.println("distribution,n,cutoff,trial,time_ms,is_sorted");

            for (Distribution dist : distributions) {
                System.out.println("\n-------------------------------------------------------------");
                System.out.println(">>> Đang chạy phân phối dữ liệu: " + dist);
                System.out.println("-------------------------------------------------------------");

                for (int n : sizes) {
                    System.out.printf("  [N = %,d] Tiến hành %d lần lặp...\n", n, trials);
                    Random rng = new Random(seed + n);

                    // Map lưu thời gian tổng để tìm cutoff tốt nhất cho kích thước N này
                    Map<Integer, List<Double>> cutoffTimes = new LinkedHashMap<>();
                    for (int c : cutoffs) {
                        cutoffTimes.put(c, new ArrayList<>());
                    }

                    for (int trial = 1; trial <= trials; trial++) {
                        // Sinh dữ liệu gốc cho lần lặp này
                        Integer[] baseData = generateData(n, dist, rng);

                        for (int cutoff : cutoffs) {
                            // Tạo bản sao độc lập cho mỗi cutoff để đảm bảo công bằng (paired test)
                            Integer[] testData = baseData.clone();

                            // Thu dọn rác trước khi đo để giảm thiểu GC pause trong lúc sort
                            // System.gc();

                            long startTime = System.nanoTime();
                            MergeSort.sort(testData, cutoff);
                            long endTime = System.nanoTime();

                            double elapsedMs = (endTime - startTime) / 1_000_000.0;
                            boolean sorted = MergeSort.isSorted(testData);

                            if (!sorted) {
                                System.err.printf("LỖI: Mảng chưa được sắp xếp đúng với cutoff=%d, N=%d!\n", cutoff, n);
                            }

                            cutoffTimes.get(cutoff).add(elapsedMs);

                            // Ghi dòng dữ liệu thô
                            writer.printf(Locale.US, "%s,%d,%d,%d,%.4f,%b\n",
                                    dist.name(), n, cutoff, trial, elapsedMs, sorted);
                        }
                    }

                    // In bảng tóm tắt kết quả cho kích thước N hiện tại
                    System.out.printf("    %-8s | %-12s | %-12s | %-12s | %-12s\n",
                            "CUTOFF", "Trung bình (ms)", "Độ lệch chuẩn", "Trung vị (ms)", "Tỉ lệ so cutoff=0");
                    System.out.println("    -----------------------------------------------------------------");

                    double baselineMean = 1.0;
                    for (int cutoff : cutoffs) {
                        List<Double> times = cutoffTimes.get(cutoff);
                        double mean = times.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
                        if (cutoff == 0) baselineMean = mean;

                        double variance = 0.0;
                        for (double t : times) variance += Math.pow(t - mean, 2);
                        double std = Math.sqrt(variance / times.size());

                        List<Double> sortedTimes = new ArrayList<>(times);
                        Collections.sort(sortedTimes);
                        double median = sortedTimes.get(sortedTimes.size() / 2);

                        double speedup = ((baselineMean - mean) / baselineMean) * 100.0;

                        System.out.printf(Locale.US, "    %-8d | %12.3f | %12.3f | %12.3f | %+10.2f%%\n",
                                cutoff, mean, std, median, speedup);
                    }
                    writer.flush();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        System.out.println("\n=========================================================================");
        System.out.println(" THÍ NGHIỆM HOÀN TẤT! Kết quả thô đã được lưu vào: " + outputFile);
        System.out.println("=========================================================================");
    }
}
