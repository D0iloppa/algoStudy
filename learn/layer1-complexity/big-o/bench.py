"""
Layer 1 · 점근 표기법(Big-O) — 실측 벤치마크

의도: Big-O 논증("O(n^2) vs O(n log n)")은 종이 위에서만 맴돌면 체감이 안 된다.
같은 입력을 n을 키워가며 두 알고리즘에 직접 먹여서 실행시간을 재고,
n이 2배 될 때 O(n^2)는 ~4배, O(n log n)은 ~2배 남짓만 느려지는 증가율(기울기)
차이를 눈으로 확인한다. 상수·구현 디테일은 버리고 "커질 때 어떻게 커지는가"만 본다.

- O(n^2): 버블 정렬 (직접 구현, 이중 루프)
- O(n log n): 파이썬 내장 sorted() (Timsort)

실행: python3 bench.py
"""

import random
import time


def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def nlogn_sort(arr):
    return sorted(arr)


def timeit_ms(fn, arr):
    start = time.perf_counter()
    fn(arr)
    return (time.perf_counter() - start) * 1000


def main():
    sizes = [1000, 2000, 4000, 8000]
    rows = []

    for n in sizes:
        data = [random.randint(0, 1_000_000) for _ in range(n)]
        n2_ms = timeit_ms(bubble_sort, data)
        nlogn_ms = timeit_ms(nlogn_sort, data)
        rows.append((n, n2_ms, nlogn_ms))

    print(f"{'n':>8} | {'O(n^2) ms':>12} | {'O(n log n) ms':>14}")
    print("-" * 40)
    for n, n2_ms, nlogn_ms in rows:
        print(f"{n:>8} | {n2_ms:>12.2f} | {nlogn_ms:>14.3f}")

    # n이 2배가 될 때 O(n^2)는 이론상 ~4배 증가해야 한다.
    # 노이즈를 감안해 마지막 두 구간(4000->8000)의 배율이 3배 이상인지만 검증한다.
    ratio = rows[-1][1] / rows[-2][1]
    assert ratio >= 3.0, (
        f"O(n^2) growth ratio too low ({ratio:.2f}x) for n doubling — "
        "increase sizes if this fails on a fast machine"
    )

    print(f"\nn 2배(4000->8000)당 O(n^2) 증가율: {ratio:.2f}x (이론상 ~4x)")
    print("OK")


if __name__ == "__main__":
    main()
