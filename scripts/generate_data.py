"""
Script sinh bộ dữ liệu thí nghiệm mẫu với nhiều phân phối khác nhau:
1. RANDOM: Dãy số nguyên ngẫu nhiên đều.
2. PARTIALLY_SORTED: Dãy gần như đã sắp xếp (95% có thứ tự, 5% xáo trộn).
3. REVERSE_SORTED: Dãy có thứ tự giảm dần.
4. FEW_UNIQUE: Dãy có rất nhiều giá trị trùng lặp (chỉ gồm các giá trị từ 0 đến 9).

Dữ liệu được lưu trữ trong thư mục data/ với định dạng file văn bản (mỗi dòng một số),
có kèm file manifest / metadata JSON để phục vụ lưu trữ và tái lập thí nghiệm.
"""

import os
import random
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

SEED = 20261120
random.seed(SEED)

SIZES = [10000, 50000, 100000, 200000]
DISTRIBUTIONS = ["RANDOM", "PARTIALLY_SORTED", "REVERSE_SORTED", "FEW_UNIQUE"]

def generate_array(dist, n, rng):
    if dist == "RANDOM":
        return [rng.randint(-1_000_000_000, 1_000_000_000) for _ in range(n)]
    elif dist == "PARTIALLY_SORTED":
        arr = list(range(n))
        swaps = int(n * 0.05)
        for _ in range(swaps):
            i = rng.randint(0, n - 1)
            j = rng.randint(0, n - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif dist == "REVERSE_SORTED":
        return list(range(n, 0, -1))
    elif dist == "FEW_UNIQUE":
        return [rng.randint(0, 9) for _ in range(n)]
    else:
        raise ValueError(f"Unknown distribution: {dist}")

def main():
    manifest = []
    print(f"Đang sinh bộ dữ liệu thí nghiệm tại: {DATA_DIR}")

    for dist in DISTRIBUTIONS:
        for n in SIZES:
            rng = random.Random(SEED + n + hash(dist))
            data = generate_array(dist, n, rng)
            filename = f"dataset_{dist.lower()}_n{n}.txt"
            filepath = os.path.join(DATA_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                for val in data:
                    f.write(f"{val}\n")

            meta = {
                "filename": filename,
                "distribution": dist,
                "size": n,
                "seed": SEED,
                "file_size_bytes": os.path.getsize(filepath)
            }
            manifest.append(meta)
            print(f"  -> Đã tạo {filename} ({n:,} phần tử, {meta['file_size_bytes']:,} bytes)")

    manifest_path = os.path.join(DATA_DIR, "dataset_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nHoàn tất! Manifest lưu tại {manifest_path}")

if __name__ == "__main__":
    main()
