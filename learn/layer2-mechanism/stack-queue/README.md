# Layer 2 · 스택과 큐 (내장 컬렉션 없이 바닥부터)

**Notion deep-dive**: https://www.notion.so/3993bd6b405d8133bd68e968c9850e7a

이 개념이 답하는 질문 — *"스택(LIFO)과 큐(FIFO)가 각각 재귀·BFS와 어떻게 연결되는지 설명할 수 있는가"*, *"배열로 큐를 만들 때 front가 앞으로 밀리며 버려지는 공간 문제를 원형 버퍼가 어떻게 해결하는가"*

두 언어로 구현했다. **Python** 은 로직, **C** 는 배열/포인터 재할당이 명시적으로 드러난다.

```bash
python3 stack_queue.py                      # → OK
gcc -O2 stack_queue.c -o sq && ./sq          # → OK
```

| 구조 | push/pop 위치 | 비용 | 배열 구현 함정 |
| --- | --- | --- | --- |
| 스택(LIFO) | top 한쪽 끝 | O(1) | 없음 — top만 밀고 당기면 됨 |
| 큐(FIFO) | rear 삽입 / front 제거 | O(1)* | 단순 배열은 dequeue마다 front가 밀려 앞 슬롯이 영영 버려짐 → 원형 버퍼(모듈러 인덱스)로 재사용 |

\*원형 버퍼(circular buffer)로 구현했을 때. front/rear를 capacity로 모듈러 순환시켜 슬롯을 재사용한다.
