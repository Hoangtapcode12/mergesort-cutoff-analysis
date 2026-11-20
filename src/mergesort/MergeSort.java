package mergesort;

/**
 * Cài đặt Mergesort chuẩn theo nội dung bài giảng (Sedgewick & Wayne COS 226 / Algorithms 4th Edition).
 * Hỗ trợ tham số CUTOFF để chuyển sang Insertion Sort khi kích thước mảng con <= CUTOFF.
 */
public class MergeSort {

    // --- Cài đặt cho Comparable[] (Chuẩn bài giảng đối tượng Java) ---

    private static void merge(Comparable[] a, Comparable[] aux, int lo, int mid, int hi) {
        // Sao chép sang mảng phụ aux[]
        for (int k = lo; k <= hi; k++) {
            aux[k] = a[k];
        }

        // Trộn hai nửa đã sắp xếp
        int i = lo;
        int j = mid + 1;
        for (int k = lo; k <= hi; k++) {
            if (i > mid) {
                a[k] = aux[j++];
            } else if (j > hi) {
                a[k] = aux[i++];
            } else if (less(aux[j], aux[i])) {
                a[k] = aux[j++];
            } else {
                a[k] = aux[i++];
            }
        }
    }

    private static void sort(Comparable[] a, Comparable[] aux, int lo, int hi, int cutoff) {
        // Cải tiến CUTOFF: Khi kích thước đoạn con (hi - lo + 1) <= cutoff thì dùng Insertion Sort
        if (cutoff > 1 && hi <= lo + cutoff - 1) {
            InsertionSort.sort(a, lo, hi);
            return;
        }
        if (hi <= lo) {
            return;
        }

        int mid = lo + (hi - lo) / 2;
        sort(a, aux, lo, mid, cutoff);
        sort(a, aux, mid + 1, hi, cutoff);
        merge(a, aux, lo, mid, hi);
    }

    public static void sort(Comparable[] a, int cutoff) {
        Comparable[] aux = new Comparable[a.length];
        sort(a, aux, 0, a.length - 1, cutoff);
    }

    public static void sort(Comparable[] a) {
        sort(a, 0); // Mặc định không áp dụng cutoff (cutoff = 0 hoặc 1)
    }

    @SuppressWarnings("unchecked")
    private static boolean less(Comparable v, Comparable w) {
        return v.compareTo(w) < 0;
    }

    // --- Cài đặt cho kiểu nguyên thủy int[] để đối chiếu hiệu năng ---

    private static void mergePrimitive(int[] a, int[] aux, int lo, int mid, int hi) {
        for (int k = lo; k <= hi; k++) {
            aux[k] = a[k];
        }

        int i = lo;
        int j = mid + 1;
        for (int k = lo; k <= hi; k++) {
            if (i > mid) {
                a[k] = aux[j++];
            } else if (j > hi) {
                a[k] = aux[i++];
            } else if (aux[j] < aux[i]) {
                a[k] = aux[j++];
            } else {
                a[k] = aux[i++];
            }
        }
    }

    private static void sortPrimitive(int[] a, int[] aux, int lo, int hi, int cutoff) {
        if (cutoff > 1 && hi <= lo + cutoff - 1) {
            InsertionSort.sort(a, lo, hi);
            return;
        }
        if (hi <= lo) {
            return;
        }

        int mid = lo + (hi - lo) / 2;
        sortPrimitive(a, aux, lo, mid, cutoff);
        sortPrimitive(a, aux, mid + 1, hi, cutoff);
        mergePrimitive(a, aux, lo, mid, hi);
    }

    public static void sortPrimitive(int[] a, int cutoff) {
        int[] aux = new int[a.length];
        sortPrimitive(a, aux, 0, a.length - 1, cutoff);
    }

    // Kiểm tra tính đúng đắn của mảng sau khi sắp xếp
    public static boolean isSorted(Comparable[] a) {
        for (int i = 1; i < a.length; i++) {
            if (less(a[i], a[i - 1])) return false;
        }
        return true;
    }

    public static boolean isSorted(int[] a) {
        for (int i = 1; i < a.length; i++) {
            if (a[i] < a[i - 1]) return false;
        }
        return true;
    }
}
