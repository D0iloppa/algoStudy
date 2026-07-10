"""
Layer 3 · 패턴 — 트리 순회 (전위 · 중위 · 후위)
Notion: (concept page URL 은 이 폴더 README.md 참조)

이 파일이 답하는 질문:
  "전위·중위·후위 순회가 각각 어떤 문제 유형에 쓰이는지 방문 순서로 설명할 수 있는가"

포인트: 트리는 재귀적 구조(노드 = 값 + 왼쪽 서브트리 + 오른쪽 서브트리)이므로
순회도 자연히 재귀다. 셋의 차이는 "root를 언제 방문하느냐" 뿐이다.
  - 전위(preorder)  : root → left → right  (부모를 먼저 안다 → 복제/직렬화)
  - 중위(inorder)   : left → root → right  (BST면 정렬된 순서로 나옴)
  - 후위(postorder) : left → right → root  (자식을 다 처리해야 부모 계산 가능
                       → 삭제, 디렉토리 크기 합산, 수식트리 계산)
재귀 버전은 콜스택을 언어 런타임에 맡긴다. 반복 버전은 그 콜스택을 명시적
스택으로 직접 흉내낸다(재귀 깊이 제한을 피하려 실무/코테에서 필요).
레벨순회(BFS)는 "가까운 것부터"라 스택(LIFO)이 아니라 큐(FIFO)를 쓴다.

실행: python3 tree_traversal.py   (self-test, 통과 시 'OK')
"""


class Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------- 재귀 버전 ----------

def preorder_recursive(root):
    if root is None:
        return []
    return [root.val] + preorder_recursive(root.left) + preorder_recursive(root.right)


def inorder_recursive(root):
    if root is None:
        return []
    return inorder_recursive(root.left) + [root.val] + inorder_recursive(root.right)


def postorder_recursive(root):
    if root is None:
        return []
    return postorder_recursive(root.left) + postorder_recursive(root.right) + [root.val]


# ---------- 반복 버전 (명시적 스택 — 콜스택을 직접 흉내) ----------

def preorder_iterative(root):
    # root → left → right : 스택에 (오른쪽, 왼쪽) 순서로 넣으면 왼쪽이 먼저 pop된다
    out = []
    if root is None:
        return out
    stack = [root]
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return out


def inorder_iterative(root):
    # 왼쪽 끝까지 내려가며 스택에 쌓고, 더 못 내려가면 pop → 방문 → 오른쪽으로 이동
    out = []
    stack = []
    cur = root
    while cur is not None or stack:
        while cur is not None:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        out.append(cur.val)
        cur = cur.right
    return out


def postorder_iterative(root):
    # 두 스택 트릭: "root → right → left" 순서로 모은 뒤 뒤집으면 "left → right → root"
    out = []
    if root is None:
        return out
    stack = [root]
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)
    out.reverse()
    return out


# ---------- 레벨순회 (BFS, 보너스 — 스택이 아니라 큐) ----------

def level_order(root):
    from collections import deque
    out = []
    if root is None:
        return out
    q = deque([root])
    while q:
        node = q.popleft()
        out.append(node.val)
        if node.left is not None:
            q.append(node.left)
        if node.right is not None:
            q.append(node.right)
    return out


def _build_tree():
    #         1
    #        / \
    #       2   3
    #      / \   \
    #     4   5   6
    return Node(1,
                Node(2, Node(4), Node(5)),
                Node(3, None, Node(6)))


def _selftest():
    root = _build_tree()

    assert preorder_recursive(root) == [1, 2, 4, 5, 3, 6]
    assert inorder_recursive(root) == [4, 2, 5, 1, 3, 6]
    assert postorder_recursive(root) == [4, 5, 2, 6, 3, 1]

    assert preorder_iterative(root) == preorder_recursive(root)
    assert inorder_iterative(root) == inorder_recursive(root)
    assert postorder_iterative(root) == postorder_recursive(root)

    assert level_order(root) == [1, 2, 3, 4, 5, 6]

    # 빈 트리
    assert preorder_recursive(None) == []
    assert inorder_iterative(None) == []
    assert postorder_iterative(None) == []
    assert level_order(None) == []

    print("OK")


if __name__ == "__main__":
    _selftest()
