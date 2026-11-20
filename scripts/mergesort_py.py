"""
Cài đặt Mergesort với cải tiến CUTOFF sang Insertion Sort bằng Python.
Chuẩn theo nội dung bài giảng giải thuật (Robert Sedgewick).
"""

def insertion_sort(a, lo, hi):
    for i in range(lo + 1, hi + 1):
        key = a[i]
        j = i - 1
        while j >= lo and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key

def merge(a, aux, lo, mid, hi):
    for k in range(lo, hi + 1):
        aux[k] = a[k]

    i = lo
    j = mid + 1
    for k in range(lo, hi + 1):
        if i > mid:
            a[k] = aux[j]
            j += 1
        elif j > hi:
            a[k] = aux[i]
            i += 1
        elif aux[j] < aux[i]:
            a[k] = aux[j]
            j += 1
        else:
            a[k] = aux[i]
            i += 1

def _sort(a, aux, lo, hi, cutoff):
    if cutoff > 1 and hi <= lo + cutoff - 1:
        insertion_sort(a, lo, hi)
        return
    if hi <= lo:
        return

    mid = lo + (hi - lo) // 2
    _sort(a, aux, lo, mid, cutoff)
    _sort(a, aux, mid + 1, hi, cutoff)
    merge(a, aux, lo, mid, hi)

def mergesort(a, cutoff=0):
    aux = [None] * len(a)
    _sort(a, aux, 0, len(a) - 1, cutoff)

def is_sorted(a):
    for i in range(1, len(a)):
        if a[i] < a[i - 1]:
            return False
    return True

if __name__ == "__main__":
    import random
    arr = [random.randint(1, 100) for _ in range(20)]
    print("Mảng ban đầu:", arr)
    mergesort(arr, cutoff=7)
    print("Mảng sau sort (cutoff=7):", arr)
    assert is_sorted(arr), "Lỗi: Mảng chưa sắp xếp!"
    print("Kiểm thử tính đúng đắn: THÀNH CÔNG!")
