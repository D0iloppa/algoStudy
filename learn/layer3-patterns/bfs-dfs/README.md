# Layer 3 · BFS vs DFS — 최단거리냐 모든 경로냐

**Notion deep-dive**: https://www.notion.so/3993bd6b405d81df83b2e5ace35f6b97

이 개념이 답하는 질문 — *"같은 그래프에서 BFS와 DFS 중 무엇을 쓸지 결정하는 기준(최단거리 vs 모든 경로 탐색)을 설명할 수 있는가"*

두 언어로 구현했다. 인접리스트로 그래프를 표현하고, BFS(큐)+DFS(재귀+반복) 둘 다 넣었다.

```bash
python3 graph_search.py                                  # → OK
gcc -O2 -o /tmp/gs graph_search.c && timeout 10 /tmp/gs  # → OK
```

```
    A
   / \
  B   C
  |   |
  D---E
      |
      F
```

| | 자료구조 | 순회 방식 | 적합한 상황 |
| --- | --- | --- | --- |
| BFS | 큐(FIFO) | 레벨 순회 — 가까운 노드부터 퍼짐 | 무가중치 최단거리 (레벨 k = 거리 k 불변식) |
| DFS | 스택/재귀(LIFO) | 한 방향 끝까지 파고든 뒤 백트래킹 | 모든 경로 탐색·연결 요소·백트래킹 |

**핵심**: 둘 다 O(V+E) — 속도 차이가 아니라 "무엇을 찾고 싶은가"가 선택 기준이다. visited 처리는 반드시 큐/스택에 **push하는 시점**에 해야 사이클에서 무한루프를 피한다.
