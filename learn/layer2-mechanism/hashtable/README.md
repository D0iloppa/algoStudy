# Layer 2 · 해시테이블 (내장 dict 없이 바닥부터, 체이닝)

**Notion deep-dive**: https://www.notion.so/3993bd6b405d81ed80a3db08dbdf3d42

이 개념이 답하는 질문 — *"충돌은 왜 불가피하고, 체이닝으로 처리할 때 평균 O(1)이 유지되는 조건은 무엇이며, load factor가 임계치를 넘으면 왜/어떻게 리사이즈해야 하는가"*

두 언어로 구현했다. 버킷 배열 + 각 버킷은 링크드리스트(체인). load factor 초과 시 capacity 2배 리사이즈 + 전체 재해싱까지 포함.

```bash
python3 hashtable.py              # → OK
gcc -O2 hashtable.c -o ht && ./ht # → OK
```

| 방식 | 삭제 | 캐시 지역성 | load factor 민감도 | 대표 사용처 |
| --- | --- | --- | --- | --- |
| 체이닝 | 쉬움 | 나쁨 | 완만 | Java `HashMap` |
| 오픈 어드레싱 | 까다로움(tombstone 필요) | 좋음 | 급격 | Python `dict` |
