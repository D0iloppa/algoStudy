"""
Layer 3 · 패턴 — BFS vs DFS (인접리스트 그래프 탐색, 바닥부터)
Notion: (concept page URL 은 이 폴더 README.md 참조)

이 파일이 답하는 질문:
  "같은 그래프에서 BFS와 DFS 중 무엇을 쓸지 결정하는 기준이 무엇이고,
   왜 BFS만 무가중치 최단거리를 보장하는지 설명할 수 있는가"

포인트: 그래프는 인접리스트(dict of list)로 표현한다. 순회 자체는 둘 다 O(V+E) —
'무엇을 찾느냐'가 선택 기준이지 속도가 아니다.
- BFS (큐, 레벨 순회) : 레벨 k에서 발견되는 노드는 항상 거리 k → 무가중치 최단거리 보장
- DFS (스택/재귀, 한 방향 끝까지) : 한 갈래를 완전히 소진 후 백트래킹 → 모든 경로·연결요소 탐색에 적합
- 둘 다 O(V+E), visited 처리 없으면 사이클에서 무한루프

실행: python3 graph_search.py   (self-test, 통과 시 'OK')
"""

from collections import deque


def bfs(graph, start):
    """큐 기반 레벨 순회. 반환: (방문순서 리스트, {노드: 시작점으로부터 거리})"""
    visited = {start}
    dist = {start: 0}
    order = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph.get(node, []):
            if nxt not in visited:          # 방문처리 없으면 사이클에서 무한루프
                visited.add(nxt)             # 큐에 넣는 시점에 방문 처리(중복 enqueue 방지)
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return order, dist


def dfs_recursive(graph, start):
    """재귀 DFS. 방문 집합은 BFS/반복 DFS와 같아야 하지만 방문 '순서'는 다를 수 있다."""
    visited = set()
    order = []

    def _visit(node):
        visited.add(node)
        order.append(node)
        for nxt in graph.get(node, []):
            if nxt not in visited:
                _visit(nxt)                  # 한 갈래를 끝까지 파고든 뒤에야 다음 이웃으로

    _visit(start)
    return order, visited


def dfs_iterative(graph, start):
    """명시적 스택으로 재귀 콜스택을 대체 — 깊은 그래프에서 스택 오버플로 회피."""
    visited = {start}
    order = []
    stack = [start]
    while stack:
        node = stack.pop()
        order.append(node)
        # 방문은 스택에 넣기 전이 아니라 pop 시점에 처리해도 되지만,
        # 재귀 버전과 '먼저 발견하면 바로 방문 확정'하는 의미를 맞추려면
        # push 시점에 visited 를 찍어야 중복 push 를 막을 수 있다.
        for nxt in reversed(graph.get(node, [])):
            if nxt not in visited:
                visited.add(nxt)
                stack.append(nxt)
    return order, visited


def _selftest():
    # 손으로 만든 그래프 (무방향, 사이클 포함)
    #
    #     A
    #    / \
    #   B   C
    #   |   |
    #   D---E
    #       |
    #       F
    graph = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "E"],
        "D": ["B", "E"],
        "E": ["C", "D", "F"],
        "F": ["E"],
    }

    # (1) BFS 방문순서가 레벨별인지: A(레벨0) → B,C(레벨1) → D,E(레벨2) → F(레벨3)
    order, dist = bfs(graph, "A")
    assert order[0] == "A"
    assert set(order[1:3]) == {"B", "C"}       # 레벨 1
    assert set(order[3:5]) == {"D", "E"}       # 레벨 2
    assert order[5] == "F"                     # 레벨 3
    # 레벨이 실제로 단조증가(먼저 나온 노드가 dist도 작거나 같음)해야 한다
    for i in range(len(order) - 1):
        assert dist[order[i]] <= dist[order[i + 1]]

    # (2) 무가중치 최단거리가 손으로 센 값과 일치하는지
    expected_dist = {"A": 0, "B": 1, "C": 1, "D": 2, "E": 2, "F": 3}
    assert dist == expected_dist, dist

    # (3) DFS 재귀/반복: 방문 집합(도달 가능한 모든 노드)은 같아야 함.
    #     순서는 스택 push 순서(이웃 나열 순서)에 따라 달라질 수 있으므로
    #     "정확히 같은 순서"가 아니라 "같은 집합"만 검증한다.
    order_rec, visited_rec = dfs_recursive(graph, "A")
    order_it, visited_it = dfs_iterative(graph, "A")
    assert visited_rec == visited_it == set(graph.keys())
    assert order_rec[0] == "A" and order_it[0] == "A"
    # 둘 다 "한 방향으로 끝까지 파고드는" 성질: 두 번째 방문 노드는 BFS 레벨1 집합 안에 있다
    assert order_rec[1] in {"B", "C"}
    assert order_it[1] in {"B", "C"}

    # 연결 안 된 두 번째 성분 — DFS/BFS 둘 다 start에서 도달 못하는 노드는 방문 안 함
    graph2 = dict(graph)
    graph2["G"] = ["H"]
    graph2["H"] = ["G"]
    order2, dist2 = bfs(graph2, "A")
    assert "G" not in dist2 and "H" not in dist2

    print("OK")


if __name__ == "__main__":
    _selftest()
