# Layer 3 · 트리 순회 (전위 · 중위 · 후위)

**Notion deep-dive**: https://www.notion.so/3993bd6b405d814982d4ee8f26dbe0de

이 개념이 답하는 질문 — *"전위·중위·후위 순회가 각각 어떤 문제 유형에 쓰이는지 방문 순서로 설명할 수 있는가"*

두 언어로 구현했다. **Python** 은 로직, **C** 는 재귀 콜스택과 명시적 스택 반복 버전의 대응이 배열로 명확히 드러난다.

```bash
python3 tree_traversal.py                     # → OK
gcc -O2 tree_traversal.c -o tt && ./tt         # → OK
```

```
        1
       / \
      2   3
     / \   \
    4   5   6

전위(root→left→right): 1 2 4 5 3 6
중위(left→root→right): 4 2 5 1 3 6
후위(left→right→root): 4 5 2 6 3 1
레벨순회(BFS, 큐)     : 1 2 3 4 5 6
```

| 순회 | 방문 순서 | 대표 용도 |
| --- | --- | --- |
| 전위(preorder) | root → left → right | 트리 복제/직렬화 (부모 먼저 만들어야 자식을 붙임) |
| 중위(inorder) | left → root → right | BST에서 정렬된 순서로 나옴 |
| 후위(postorder) | left → right → root | 트리 삭제, 디렉토리 크기 합산, 수식트리 계산 (자식 먼저 처리) |
| 레벨순회(BFS) | 레벨 단위, 큐 사용 | 최단 깊이 탐색, 레벨별 처리 |

각 순회는 재귀 버전과 명시적 스택을 쓴 반복 버전 둘 다 구현했고, 두 결과가 일치함을 self-test로 검증한다.
