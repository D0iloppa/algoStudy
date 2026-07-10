"""
Layer 2 · 메커니즘 — 해시테이블 (내장 dict 없이 바닥부터, 체이닝 방식)
Notion: (concept page URL 은 이 폴더 README.md 참조)

이 파일이 답하는 질문:
  "충돌은 왜 불가피하고, 체이닝으로 처리할 때 평균 O(1)이 유지되는 조건은
   무엇이며, load factor가 임계치를 넘으면 왜/어떻게 리사이즈해야 하는가"

포인트: 키를 해시함수로 버킷 인덱스(hash(key) % capacity)로 변환해 저장.
버킷마다 링크드리스트(체인)를 둬서 같은 인덱스로 몰린 키들을 처리한다.
- put/get/delete : 평균 O(1)  — 균등 분포 가정, 버킷당 원소 수가 상수에 가까울 때
- load factor(n/capacity) 가 임계치(0.75)를 넘으면 capacity 를 2배로 늘리고
  기존 원소를 전부 재해싱(rehash)한다 — amortized O(1) 유지의 핵심
- 최악의 경우(나쁜 해시로 모든 키가 한 버킷에 몰림) O(n)

실행: python3 hashtable.py   (self-test, 통과 시 'OK')
"""


class _Entry:
    __slots__ = ("key", "val", "next")

    def __init__(self, key, val, nxt=None):
        self.key = key
        self.val = val
        self.next = nxt


class HashTable:
    LOAD_FACTOR_LIMIT = 0.75

    def __init__(self, capacity=8):
        self._capacity = capacity
        self._buckets = [None] * capacity   # 각 버킷 = 체인의 head(_Entry) or None
        self._size = 0

    def _bucket_index(self, key):
        return hash(key) % self._capacity   # 해시함수 → 버킷 인덱스

    def put(self, key, val):
        idx = self._bucket_index(key)
        cur = self._buckets[idx]
        while cur is not None:              # 같은 키면 값만 갱신
            if cur.key == key:
                cur.val = val
                return
            cur = cur.next
        self._buckets[idx] = _Entry(key, val, self._buckets[idx])  # 체인 맨 앞에 삽입 O(1)
        self._size += 1
        if self._size / self._capacity > self.LOAD_FACTOR_LIMIT:
            self._resize(self._capacity * 2)

    def get(self, key):
        idx = self._bucket_index(key)
        cur = self._buckets[idx]
        while cur is not None:
            if cur.key == key:
                return cur.val
            cur = cur.next
        raise KeyError(key)

    def delete(self, key):
        idx = self._bucket_index(key)
        prev, cur = None, self._buckets[idx]
        while cur is not None:
            if cur.key == key:
                if prev is None:
                    self._buckets[idx] = cur.next
                else:
                    prev.next = cur.next
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def _resize(self, new_capacity):
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * new_capacity
        self._size = 0
        for head in old_buckets:            # 전체 재해싱 — capacity 가 바뀌었으니 인덱스도 재계산
            cur = head
            while cur is not None:
                self.put(cur.key, cur.val)
                cur = cur.next

    def __len__(self):
        return self._size

    def __contains__(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False


def _selftest():
    ht = HashTable(capacity=4)              # 작게 시작 → 리사이즈 경로 강제 유발
    ht.put("a", 1)
    ht.put("b", 2)
    ht.put("c", 3)
    assert ht.get("a") == 1
    assert ht.get("b") == 2
    assert "c" in ht
    assert "z" not in ht
    ht.put("a", 100)                        # 갱신, size 불변
    assert ht.get("a") == 100
    assert len(ht) == 3

    # 같은 버킷에 여러 키를 강제로 몰아넣어 체이닝 검증
    class Collide:
        __slots__ = ("tag",)
        def __init__(self, tag):
            self.tag = tag
        def __hash__(self):
            return 0                        # 모두 같은 해시 → 항상 같은 버킷
        def __eq__(self, other):
            return isinstance(other, Collide) and self.tag == other.tag

    ht2 = HashTable(capacity=8)
    keys = [Collide(i) for i in range(5)]
    for i, k in enumerate(keys):
        ht2.put(k, i * 10)
    for i, k in enumerate(keys):
        assert ht2.get(k) == i * 10          # 체인을 끝까지 훑어도 값이 맞아야 함
    assert len(ht2) == 5

    # 리사이즈 후에도 기존 값이 유지되는지
    ht3 = HashTable(capacity=2)
    n = 50
    for i in range(n):
        ht3.put(i, i * i)
    assert ht3._capacity > 2                 # 리사이즈가 실제로 일어났는지
    for i in range(n):
        assert ht3.get(i) == i * i
    assert len(ht3) == n

    assert ht.delete("b") is True
    assert "b" not in ht
    assert ht.delete("nope") is False
    assert len(ht) == 2

    print("OK")


if __name__ == "__main__":
    _selftest()
