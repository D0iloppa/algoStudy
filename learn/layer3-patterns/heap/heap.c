/*
 * Layer 3 · 패턴 — 힙 / 우선순위 큐 (C: 배열 기반, 동적 리사이징)
 *
 * Python 버전과 동일 로직이지만, C 는 '배열이 곧 완전이진트리'라는 사실을
 * 그대로 드러낸다 — 포인터가 하나도 없고 인덱스 산술(2i+1, 2i+2, (i-1)/2)뿐이다.
 *
 * 실행: gcc -O2 -o /tmp/hp heap.c && /tmp/hp   (통과 시 'OK')
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

typedef struct {
    int *data;
    int  size;
    int  cap;
} Heap;

static void heap_init(Heap *h) {
    h->cap = 4;
    h->data = malloc(sizeof(int) * h->cap);
    h->size = 0;
}

static void heap_grow(Heap *h) {
    if (h->size < h->cap) return;
    h->cap *= 2;
    h->data = realloc(h->data, sizeof(int) * h->cap);
}

static void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }

static void sift_up(Heap *h, int i) {
    while (i > 0) {
        int parent = (i - 1) / 2;
        if (h->data[parent] <= h->data[i]) break;   /* 부모가 이미 더 작음 → 종료 */
        swap(&h->data[parent], &h->data[i]);
        i = parent;
    }
}

static void sift_down(Heap *h, int i) {
    while (1) {
        int left = 2 * i + 1, right = 2 * i + 2, smallest = i;
        if (left < h->size && h->data[left] < h->data[smallest]) smallest = left;
        if (right < h->size && h->data[right] < h->data[smallest]) smallest = right;
        if (smallest == i) break;                   /* 두 자식보다 작거나 같음 */
        swap(&h->data[i], &h->data[smallest]);
        i = smallest;
    }
}

static void heap_push(Heap *h, int val) {            /* O(log n) */
    heap_grow(h);
    h->data[h->size] = val;
    h->size++;
    sift_up(h, h->size - 1);
}

static int heap_pop(Heap *h) {                       /* O(log n) */
    assert(h->size > 0);
    int top = h->data[0];
    h->size--;
    h->data[0] = h->data[h->size];                   /* 맨 끝 원소를 루트로 */
    if (h->size > 0) sift_down(h, 0);
    return top;
}

static int heap_peek(Heap *h) {                      /* O(1) */
    assert(h->size > 0);
    return h->data[0];
}

/* O(n) — 리프 바로 위 노드부터 역순으로 sift-down 하면 전체가 힙이 된다 */
static void heap_heapify(Heap *h, int *arr, int n) {
    if (h->cap < n) {
        h->cap = n;
        h->data = realloc(h->data, sizeof(int) * h->cap);
    }
    for (int i = 0; i < n; i++) h->data[i] = arr[i];
    h->size = n;
    for (int i = n / 2 - 1; i >= 0; i--) sift_down(h, i);
}

static void heap_free(Heap *h) { free(h->data); h->data = NULL; h->size = h->cap = 0; }

static int is_heap(Heap *h) {
    for (int i = 0; i < h->size; i++) {
        int left = 2 * i + 1, right = 2 * i + 2;
        if (left < h->size && h->data[i] > h->data[left]) return 0;
        if (right < h->size && h->data[i] > h->data[right]) return 0;
    }
    return 1;
}

static int cmp_int(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

int main(void) {
    Heap h; heap_init(&h);
    int values[] = {5, 3, 8, 1, 9, 2, 7, 4, 6, 0};
    int n = sizeof(values) / sizeof(values[0]);
    for (int i = 0; i < n; i++) {
        heap_push(&h, values[i]);
        assert(is_heap(&h));                          /* push 후에도 항상 heap 성질 유지 */
    }
    assert(h.size == n);
    assert(heap_peek(&h) == 0);

    int sorted_vals[10]; for (int i = 0; i < n; i++) sorted_vals[i] = values[i];
    qsort(sorted_vals, n, sizeof(int), cmp_int);

    int popped[10];
    for (int i = 0; i < n; i++) {
        assert(is_heap(&h));
        popped[i] = heap_pop(&h);
    }
    for (int i = 0; i < n; i++) assert(popped[i] == sorted_vals[i]);   /* 오름차순 */
    heap_free(&h);

    /* heapify: 임의 배열을 O(n)에 힙으로 */
    int arr[8] = {40, -3, 17, 5, -20, 8, 0, 33};
    int arr_sorted[8]; for (int i = 0; i < 8; i++) arr_sorted[i] = arr[i];
    qsort(arr_sorted, 8, sizeof(int), cmp_int);

    Heap h2; heap_init(&h2);
    heap_heapify(&h2, arr, 8);
    assert(is_heap(&h2));
    int drained[8];
    for (int i = 0; i < 8; i++) drained[i] = heap_pop(&h2);
    for (int i = 0; i < 8; i++) assert(drained[i] == arr_sorted[i]);
    heap_free(&h2);

    printf("OK\n");
    return 0;
}
