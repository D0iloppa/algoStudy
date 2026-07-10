# Layer 2 · 이진 탐색 (정렬된 배열 위의 O(log n))

**Notion deep-dive**: https://www.notion.so/3993bd6b405d8131aba9d2e5396619ef

이 개념이 답하는 질문 — *"이진 탐색이 왜 O(log n)인지 분할 트리 관점에서 설명할 수 있는가, 그리고 lo/hi/mid 경계 조건을 무한루프 없이 다룰 수 있는가"*

두 언어로 구현했다. **Python** 은 로직, **C** 는 mid 오버플로/경계 조건이 명시적으로 드러난다.

```bash
python3 binary_search.py                   # → OK
gcc -O2 binary_search.c -o bs && ./bs       # → OK
```

| 함수 | 구간 스타일 | 루프 조건 | 반환 |
| --- | --- | --- | --- |
| `binary_search` | 닫힌 구간 `[lo, hi]` | `lo <= hi` | 일치 인덱스, 없으면 -1 |
| `lower_bound` | 반열린 구간 `[lo, hi)` | `lo < hi` | val 이상이 처음 등장하는 인덱스 |
| `upper_bound` | 반열린 구간 `[lo, hi)` | `lo < hi` | val 초과가 처음 등장하는 인덱스 |
