"""
Layer 2 · 메커니즘 — 스택과 큐 (내장 컬렉션 없이 바닥부터)
Notion: (concept page URL 은 이 폴더 README.md 참조)

이 파일이 답하는 질문:
  "스택(LIFO)과 큐(FIFO)가 각각 재귀·BFS와 어떻게 연결되는지 설명할 수 있는가"
  "배열로 큐를 만들 때 front가 앞으로 밀리며 버려지는 공간 문제를 원형 버퍼가
   어떻게 해결하는지 설명할 수 있는가"

포인트:
- 스택은 배열 뒤쪽(top) 한 곳만 건드린다 — push/pop 모두 O(1)
- 단순 배열 큐는 dequeue마다 front를 앞으로 옮기며 그 앞 슬롯을 영영 버린다
  → 원형 버퍼(circular buffer): front/rear를 capacity로 모듈러 순환시켜 슬롯 재사용
- enqueue/dequeue O(1), 꽉 찼을 때만 재할당(resize)

실행: python3 stack_queue.py   (self-test, 통과 시 'OK')
"""


class Stack:
    """배열 기반 스택. top 쪽 끝 한 곳만 push/pop — O(1)."""

    def __init__(self, capacity=4):
        self._data = [None] * capacity
        self._capacity = capacity
        self._top = 0  # 다음 push가 들어갈 빈 인덱스 = 현재 원소 개수

    def push(self, val):                # O(1) amortized
        if self._top == self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._top] = val
        self._top += 1

    def pop(self):                       # O(1)
        if self._top == 0:
            raise IndexError("pop from empty stack")
        self._top -= 1
        val = self._data[self._top]
        self._data[self._top] = None
        return val

    def peek(self):
        if self._top == 0:
            raise IndexError("peek from empty stack")
        return self._data[self._top - 1]

    def is_empty(self):
        return self._top == 0

    def __len__(self):
        return self._top

    def _resize(self, new_cap):
        new_data = [None] * new_cap
        for i in range(self._top):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_cap


class CircularQueue:
    """원형 버퍼 큐. front/rear를 capacity로 모듈러 순환 — dequeue로 버려지는 슬롯 없음."""

    def __init__(self, capacity=4):
        self._data = [None] * capacity
        self._capacity = capacity
        self._front = 0   # 다음 dequeue가 읽을 인덱스
        self._size = 0     # 현재 원소 개수 (front/rear만으로는 가득/빈 구분 불가하므로 별도 카운트)

    def enqueue(self, val):              # O(1) amortized
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        rear = (self._front + self._size) % self._capacity
        self._data[rear] = val
        self._size += 1

    def dequeue(self):                   # O(1)
        if self._size == 0:
            raise IndexError("dequeue from empty queue")
        val = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % self._capacity  # 슬롯을 버리지 않고 순환
        self._size -= 1
        return val

    def peek(self):
        if self._size == 0:
            raise IndexError("peek from empty queue")
        return self._data[self._front]

    def is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def _resize(self, new_cap):
        # 논리적 순서(front부터)로 새 배열에 재배치하고 front를 0으로 리셋
        new_data = [None] * new_cap
        for i in range(self._size):
            new_data[i] = self._data[(self._front + i) % self._capacity]
        self._data = new_data
        self._capacity = new_cap
        self._front = 0


def _selftest():
    # --- 스택: LIFO ---
    s = Stack(capacity=2)
    s.push(1); s.push(2); s.push(3)      # capacity 2 -> resize 트리거
    assert len(s) == 3
    assert s.peek() == 3
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty()
    try:
        s.pop()
        assert False, "언더플로가 감지되지 않음"
    except IndexError:
        pass

    # --- 원형 큐: FIFO + 슬롯 재사용 확인 ---
    q = CircularQueue(capacity=3)
    q.enqueue(1); q.enqueue(2); q.enqueue(3)   # 꽉 참 (front=0)
    assert q.dequeue() == 1                    # front가 1로 순환 이동, 슬롯 0은 비지만 버려지지 않음
    q.enqueue(4)                                # 비워진 슬롯 0을 rear로 재사용 (resize 없이)
    assert len(q) == 3
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.dequeue() == 4
    assert q.is_empty()
    try:
        q.dequeue()
        assert False, "언더플로가 감지되지 않음"
    except IndexError:
        pass

    # --- resize 후에도 FIFO 순서 유지 ---
    q2 = CircularQueue(capacity=2)
    for v in range(5):
        q2.enqueue(v)                           # 중간에 여러 번 resize
    out = [q2.dequeue() for _ in range(5)]
    assert out == [0, 1, 2, 3, 4], out

    print("OK")


if __name__ == "__main__":
    _selftest()
