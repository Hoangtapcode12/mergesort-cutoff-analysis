package mergesort;

/**
 * Cài đặt Insertion Sort trên đoạn con [lo, hi] của mảng Comparable[]
 * Chuẩn theo nội dung bài giảng môn Cấu trúc dữ liệu và giải thuật (Sedgewick & Wayne).
 */
public class InsertionSort {

    public static void sort(Comparable[] a, int lo, int hi) {
        for (int i = lo + 1; i <= hi; i++) {
            Comparable key = a[i];
            int j = i - 1;
            // Dời các phần tử lớn hơn key sang phải một vị trí
            while (j >= lo && less(key, a[j])) {
                a[j + 1] = a[j];
                j--;
            }
            a[j + 1] = key;
        }
    }

    // Phiên bản cho kiểu nguyên thủy int[] để đối chiếu
    public static void sort(int[] a, int lo, int hi) {
        for (int i = lo + 1; i <= hi; i++) {
            int key = a[i];
            int j = i - 1;
            while (j >= lo && key < a[j]) {
                a[j + 1] = a[j];
                j--;
            }
            a[j + 1] = key;
        }
    }

    @SuppressWarnings("unchecked")
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }
}
