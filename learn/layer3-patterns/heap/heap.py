"""
Layer 3 · 패턴 — 힙 / 우선순위 큐 (배열 기반, heapq 없이 바닥부터)
Notion: (concept page URL 은 이 폴더 README.md 참조)

이 파일이 답하는 질문:
  "정렬보다 힙이 유리해지는 순간이 언제인지, 그리고 push/pop 이
   왜 O(log n)인지 완전이진트리의 배열 표현으로 설명할 수 있는가"

포인트: 힙은 완전이진트리를 포인터 없이 '배열 인덱스'로 표현한다.
  부모 i  → 왼쪽 자식 2i+1, 오른쪽 자식 2i+2
  자식 i  → 부모 (i-1)//2
- push (sift-up)   : O(log n) — 맨 끝에 넣고 부모와 비교하며 위로 올림
- pop  (sift-down) : O(log n) — 루트를 빼고 맨 끝을 루트로 올린 뒤 아래로 내림
- peek             : O(1)     — 루트가 항상 최솟값(min-heap)
- heapify          : O(n)     — 배열 뒤쪽 절반(리프)부터가 아니라 리프 '바로 위'부터 sift-down

실행: python3 heap.py   (self-test, 통과 시 'OK')
"""

import random


class MinHeap:
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def peek(self):                     # O(1) — 루트가 항상 최솟값
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    def push(self, val):                # O(log n) — sift-up
        self._data.append(val)
        self._sift_up(len(self._data) - 1)

    def pop(self):                      # O(log n) — sift-down
        if not self._data:
            raise IndexError("pop from empty heap")
        top = self._data[0]
        last = self._data.pop()         # 맨 끝 원소를 뽑아
        if self._data:
            self._data[0] = last        # 루트 자리에 앉히고
            self._sift_down(0)          # 아래로 내리며 heap 성질 복구
        return top

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._data[parent] <= self._data[i]:
                break                    # 부모가 이미 더 작음 → heap 성질 만족, 종료
            self._data[parent], self._data[i] = self._data[i], self._data[parent]
            i = parent

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and self._data[left] < self._data[smallest]:
                smallest = left
            if right < n and self._data[right] < self._data[smallest]:
                smallest = right
            if smallest == i:
                break                    # 두 자식보다 작거나 같음 → 더 내려갈 필요 없음
            self._data[i], self._data[smallest] = self._data[smallest], self._data[i]
            i = smallest

    def heapify(self, arr):             # O(n) — 배열 전체를 힙으로
        self._data = list(arr)
        n = len(self._data)
        # 리프(n//2 이상 인덱스)는 이미 단일 원소 힙이므로 건너뛰고,
        # 리프 바로 위 노드부터 역순으로 sift-down 하면 O(n)에 완성된다.
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)

    def to_list(self):
        return list(self._data)


def _is_heap(arr):
    """부모 <= 자식 성질이 배열 전체에서 유지되는지 검사."""
    n = len(arr)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n and arr[i] > arr[left]:
            return False
        if right < n and arr[i] > arr[right]:
            return False
    return True


def _selftest():
    h = MinHeap()
    values = [5, 3, 8, 1, 9, 2, 7, 4, 6, 0]
    for v in values:
        h.push(v)
        assert _is_heap(h.to_list()), h.to_list()   # push 후에도 항상 heap 성질 유지
    assert len(h) == len(values)
    assert h.peek() == 0

    popped = []
    while len(h):
        assert _is_heap(h.to_list())
        popped.append(h.pop())
    assert popped == sorted(values), popped         # pop 순서가 오름차순이어야 함(heap sort와 동치)

    # heapify: 임의 배열을 O(n)에 힙으로
    random.seed(0)
    arr = [random.randint(-50, 50) for _ in range(30)]
    h2 = MinHeap()
    h2.heapify(arr)
    assert _is_heap(h2.to_list()), h2.to_list()
    drained = []
    while len(h2):
        drained.append(h2.pop())
    assert drained == sorted(arr)

    # 빈 힙 예외 처리
    empty = MinHeap()
    try:
        empty.pop()
        assert False, "empty pop should raise"
    except IndexError:
        pass

    print("OK")


if __name__ == "__main__":
    _selftest()
