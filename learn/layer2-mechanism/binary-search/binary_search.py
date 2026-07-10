"""
Layer 2 · 메커니즘 — 이진 탐색 (내장 함수 없이 바닥부터)
Notion: (concept page URL 은 이 폴더 README.md 참조)

이 파일이 답하는 질문:
  "이진 탐색이 왜 O(log n)인지 분할 트리 관점에서 설명할 수 있는가,
   그리고 lo/hi/mid 경계 조건을 무한루프 없이 다룰 수 있는가"

포인트: 정렬된 배열에서만 성립. 매 단계 탐색 구간이 절반으로 줄어든다
(높이 log2(n)짜리 이진 분할 트리를 타고 내려가는 것과 동치).
- binary_search  : 값과 정확히 일치하는 인덱스 탐색, 없으면 -1  — O(log n)
- lower_bound    : val 이상이 처음 등장하는 인덱스 (중복 중 첫 위치) — O(log n)
- upper_bound    : val 초과가 처음 등장하는 인덱스 (중복 다음 위치) — O(log n)

lo, hi 는 항상 "닫힌 구간 [lo, hi]가 답을 포함할 수 있는 범위"라는 불변식을
유지한다. mid 는 오버플로 방지를 위해 lo + (hi - lo) // 2 로 계산한다
(파이썬은 오버플로가 없지만 C와 로직을 맞추기 위해 관례를 통일한다).

실행: python3 binary_search.py   (self-test, 통과 시 'OK')
"""


def binary_search(arr, target):        # O(log n) — 값과 일치하는 인덱스
    lo, hi = 0, len(arr) - 1
    while lo <= hi:                     # 구간이 비면(lo > hi) 종료
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1                # 왼쪽 절반 버림
        else:
            hi = mid - 1                # 오른쪽 절반 버림
    return -1


def lower_bound(arr, val):              # O(log n) — val 이상이 처음 등장하는 인덱스
    lo, hi = 0, len(arr)                # hi 는 "못 찾으면 여기" 라는 반열린 경계
    while lo < hi:                      # [lo, hi) 반열린 구간
        mid = lo + (hi - lo) // 2
        if arr[mid] < val:
            lo = mid + 1
        else:
            hi = mid                    # mid 도 후보이므로 버리지 않음
    return lo


def upper_bound(arr, val):              # O(log n) — val 초과가 처음 등장하는 인덱스
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] <= val:
            lo = mid + 1
        else:
            hi = mid
    return lo


def _selftest():
    arr = [1, 3, 3, 3, 5, 7, 9]

    assert binary_search(arr, 5) == 4
    assert binary_search(arr, 1) == 0
    assert binary_search(arr, 9) == 6
    assert binary_search(arr, 4) == -1
    assert binary_search([], 1) == -1
    assert binary_search([1], 1) == 0

    # 중복값 3 은 인덱스 1,2,3 에 존재 → lower=1, upper=4
    assert lower_bound(arr, 3) == 1
    assert upper_bound(arr, 3) == 4
    assert lower_bound(arr, 0) == 0          # 모든 원소보다 작음 → 맨 앞
    assert lower_bound(arr, 10) == len(arr)  # 모든 원소보다 큼 → 맨 뒤
    assert upper_bound(arr, 10) == len(arr)
    assert lower_bound(arr, 4) == upper_bound(arr, 4) == 4  # 없는 값: lower==upper

    # 정렬 안 된 입력은 결과가 정의되지 않음(전제 위반) — 여기선 계약만 문서화
    print("OK")


if __name__ == "__main__":
    _selftest()
