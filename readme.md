# algoStudy

코딩테스트 알고리즘 — **탑다운 deep-dive**의 코드 저장소.
Notion 커리큘럼(자가진단 체크리스트 + 4개 레이어 지식지도)의 "직접 구현/풀이"를 담는 실행 가능한 코드가 여기 산다.

> 철학: 알고리즘은 **설계 논증만으로 검증되지 않는다.** 각 개념은 "왜 그런가"를 말로 설명하는 동시에,
> 바닥부터 직접 구현하고 **실측**해야 통과다. 그래서 코드가 Notion 안이 아니라 실행되는 repo에 있다.

## 구조

```
learn/       탑다운 개념 deep-dive 구현 (Notion 개념페이지와 1:1)
  layer1-complexity/    복잡도 — 실측 비교
  layer2-mechanism/     자료구조 동작 원리 (내장 컬렉션 없이 바닥부터)
  layer3-patterns/      문제 유형별 전략
  layer4-practice/      실전 기출 감각
solve/       기출 풀이 (stdin→stdout)
  boj/<번호>/           백준: sol.py / sol.java / sol.c + tests/N.in,N.out
  programmers/
runtime/     다언어 로컬 채점기
  judge.sh
```

## 런타임 — `runtime/judge.sh`

풀이 파일 하나를 주면 **언어 자동감지 → 컴파일 → `tests/*.in` 실행 → `*.out` diff → 실행시간 실측(ms)**.
파이썬·자바·C(·C++) 지원. 실측 시간이 나오므로 Layer 1의 "입력 크기별 실제 실행시간 비교" 요구를 그대로 충족한다.

```bash
runtime/judge.sh solve/boj/2869/sol.py     # 언어 자동감지
runtime/judge.sh solve/boj/2869/sol.c      # 같은 테스트, C 로
runtime/judge.sh solve/boj/2869/sol.java   # java: public class 는 Main 규칙
```

테스트 케이스: 풀이 폴더 안 `tests/` 에 `N.in` / `N.out` 페어를 둔다. 두 번째 인자로 다른 폴더 지정 가능.

## 네이밍 규칙

- 백준: `solve/boj/<문제번호>/sol.<ext>` + `tests/`
- 프로그래머스: `solve/programmers/<문제번호>/...`
- 개념 구현: `learn/<layer>/<concept>/` — 각 파일은 `python3 x.py` / 컴파일·실행 시 self-test `OK` 출력

## Notion 연동

각 `learn/<concept>/` 폴더는 Notion 개념 deep-dive 페이지와 1:1로 대응한다.
페이지 구조(템플릿): ① 답해야 할 질문 → ② 개념·논증(Why) → ③ 직접 구현(이 repo 링크) → ④ 직접 풀이(기출) → ⑤ 오답 로그.
