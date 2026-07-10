"""
Layer 2 · 메커니즘 — 링크드 리스트 (내장 컬렉션 없이 바닥부터)
Notion: (concept page URL 은 이 폴더 README.md 참조)

이 파일이 답하는 질문:
  "어레이(연속 메모리)와 링크드리스트(포인터 체인)의 삽입/삭제/탐색 비용이
   왜 다른지 메모리 구조로 설명할 수 있는가"

포인트: 노드는 메모리 어디에 흩어져 있어도 되고, 서로를 '참조(next)'로 잇는다.
- push_front : O(1)   — head 참조만 갈아끼움. 뒤 원소 이동 없음(어레이는 O(n) shift)
- push_back  : O(n)   — tail 을 안 들면 끝까지 걸어가야 함
- find       : O(n)   — 인덱스 임의접근 불가. 순차 탐색뿐(어레이는 O(1) 임의접근)
- delete     : O(n)   — 노드 자체를 찾는 데 O(n), 잇기 자체는 O(1)

실행: python3 linked_list.py   (self-test, 통과 시 'OK')
"""


class Node:
    __slots__ = ("val", "next")

    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def push_front(self, val):          # O(1)
        self.head = Node(val, self.head)
        self._size += 1

    def push_back(self, val):           # O(n) — tail 미보유
        node = Node(val)
        if self.head is None:
            self.head = node
        else:
            cur = self.head
            while cur.next is not None:  # 끝까지 걸어감
                cur = cur.next
            cur.next = node
        self._size += 1

    def find(self, val):                # O(n) — 순차 탐색
        cur, idx = self.head, 0
        while cur is not None:
            if cur.val == val:
                return idx
            cur, idx = cur.next, idx + 1
        return -1

    def delete(self, val):              # O(n) 탐색 + O(1) 잇기
        prev, cur = None, self.head
        while cur is not None:
            if cur.val == val:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next   # 앞 노드가 뒤 노드를 직접 참조 → 중간 노드 분리
                self._size -= 1
                return True
            prev, cur = cur, cur.next
        return False

    def to_list(self):
        out, cur = [], self.head
        while cur is not None:
            out.append(cur.val)
            cur = cur.next
        return out

    def __len__(self):
        return self._size


def _selftest():
    ll = LinkedList()
    ll.push_back(1); ll.push_back(2); ll.push_back(3)
    ll.push_front(0)
    assert ll.to_list() == [0, 1, 2, 3], ll.to_list()
    assert len(ll) == 4
    assert ll.find(2) == 2
    assert ll.find(99) == -1
    assert ll.delete(2) is True
    assert ll.to_list() == [0, 1, 3]
    assert ll.delete(0) is True          # head 삭제
    assert ll.to_list() == [1, 3]
    assert ll.delete(99) is False
    print("OK")


if __name__ == "__main__":
    _selftest()
