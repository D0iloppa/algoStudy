/*
 * Layer 2 · 메커니즘 — 이진 탐색 (C: 오버플로/경계 조건이 명시적으로 드러남)
 *
 * Python 버전과 동일 로직. C 는 mid 계산의 오버플로 함정을 그대로 보여준다:
 *   - (lo + hi) / 2 는 lo, hi 가 크면 int 오버플로로 음수 mid 가 나올 수 있다
 *   - lo + (hi - lo) / 2 로 계산하면 오버플로 없이 항상 [lo, hi] 안에 머문다
 *
 * 실행: gcc -O2 -o /tmp/bs binary_search.c && /tmp/bs   (통과 시 'OK')
 */
#include <stdio.h>
#include <assert.h>

static int binary_search(const int *arr, int n, int target) {   /* O(log n) */
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;      /* 오버플로 방지 */
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) lo = mid + 1;   /* 왼쪽 절반 버림 */
        else hi = mid - 1;                          /* 오른쪽 절반 버림 */
    }
    return -1;
}

static int lower_bound(const int *arr, int n, int val) {        /* O(log n) */
    int lo = 0, hi = n;                    /* [lo, hi) 반열린 구간 */
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] < val) lo = mid + 1;
        else hi = mid;                      /* mid 도 후보이므로 버리지 않음 */
    }
    return lo;
}

static int upper_bound(const int *arr, int n, int val) {        /* O(log n) */
    int lo = 0, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] <= val) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

int main(void) {
    int arr[] = {1, 3, 3, 3, 5, 7, 9};
    int n = 7;

    assert(binary_search(arr, n, 5) == 4);
    assert(binary_search(arr, n, 1) == 0);
    assert(binary_search(arr, n, 9) == 6);
    assert(binary_search(arr, n, 4) == -1);
    assert(binary_search(arr, 0, 1) == -1);

    assert(lower_bound(arr, n, 3) == 1);
    assert(upper_bound(arr, n, 3) == 4);
    assert(lower_bound(arr, n, 0) == 0);
    assert(lower_bound(arr, n, 10) == n);
    assert(upper_bound(arr, n, 10) == n);
    assert(lower_bound(arr, n, 4) == upper_bound(arr, n, 4));

    printf("OK\n");
    return 0;
}
