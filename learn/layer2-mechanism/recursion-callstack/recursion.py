"""
Layer 2 · 메커니즘 — 재귀와 콜 스택
Notion: (concept page URL 은 이 폴더 README.md 참조)

이 파일이 답하는 질문:
  "재귀 호출마다 콜 스택에 실제로 무엇이 쌓이는지, 그리고 왜 모든 재귀는
   명시적 스택을 쓰는 반복문으로 바꿀 수 있는지 설명할 수 있는가"

포인트:
- 함수 호출 = 스택 프레임 push(인자 + 지역변수 + 복귀 주소). return = pop.
- 재귀 깊이 = 스택에 쌓이는 프레임 수 → 너무 깊으면 스택 오버플로.
- 재귀는 "콜 스택을 인터프리터/CPU에게 맡기는 것"뿐이다.
  같은 순서를 내가 직접 리스트(=명시적 스택)로 흉내내면 반복문으로 바뀐다.
- 꼬리재귀(tail recursion)는 마지막 동작이 재귀호출 자체라 프레임을 재사용할
  여지가 있지만, CPython/JVM은 기본적으로 이 최적화(TCO)를 하지 않는다
  (스택 트레이스 보존을 우선시하는 설계 선택).

실행: python3 recursion.py   (self-test, 통과 시 'OK')
"""

import sys


# ---------------------------------------------------------------------------
# 1) 재귀 버전 — 팩토리얼 / 피보나치
# ---------------------------------------------------------------------------
def factorial_rec(n):                 # 호출마다 프레임 하나 push, n번 깊이
    if n <= 1:                        # 종료조건 — 없으면 무한재귀 → 오버플로
        return 1
    return n * factorial_rec(n - 1)   # 복귀 후 곱셈을 해야 하므로 '꼬리호출 아님'


def fib_rec(n):                       # 트리 재귀 — 중복 계산 함정의 대표 예
    if n <= 1:
        return n
    return fib_rec(n - 1) + fib_rec(n - 2)   # fib(n-2)가 여러 경로에서 반복 계산됨


# ---------------------------------------------------------------------------
# 2) 재귀 → 반복 변환 — 명시적 스택으로 콜 스택을 손으로 흉내
# ---------------------------------------------------------------------------
def factorial_iter(n):                # 콜 스택 대신 파이썬 list를 스택으로 사용
    stack = []
    while n > 1:                      # 재귀 호출이 쌓이던 지점 → push
        stack.append(n)
        n -= 1
    result = 1
    while stack:                      # 복귀(return)하며 곱셈하던 지점 → pop
        result *= stack.pop()
    return result


def fib_iter(n):                      # 트리 재귀를 명시적 스택 DFS로
    if n <= 1:
        return n
    stack = [(n, 1)]                  # (인자, 방문횟수) — call frame을 흉내
    memo = {0: 0, 1: 1}
    while stack:
        k, visit = stack[-1]
        if k in memo:
            stack.pop()
            continue
        if visit == 1:                 # 아직 하위 호출을 안 만들었으면 자식 push
            stack[-1] = (k, 2)
            if k - 1 not in memo:
                stack.append((k - 1, 1))
            if k - 2 not in memo:
                stack.append((k - 2, 1))
        else:                          # 두 하위 결과가 준비됨 → '복귀'
            memo[k] = memo[k - 1] + memo[k - 2]
            stack.pop()
    return memo[n]


# ---------------------------------------------------------------------------
# 3) 꼬리재귀 형태 — 파이썬은 TCO가 없어 깊으면 여전히 오버플로 난다는 예시
# ---------------------------------------------------------------------------
def factorial_tail(n, acc=1):          # 마지막 동작이 재귀호출 자체 = 꼬리호출
    if n <= 1:
        return acc
    return factorial_tail(n - 1, acc * n)   # 복귀 후 할 일이 없다 → 이론상 프레임 재사용 가능


def _selftest():
    assert factorial_rec(5) == 120
    assert factorial_iter(5) == 120
    assert factorial_tail(5) == 120
    assert factorial_rec(0) == factorial_iter(0) == factorial_tail(0) == 1

    for n in range(15):
        assert fib_rec(n) == fib_iter(n), (n, fib_rec(n), fib_iter(n))

    # 재귀 한도 확인 — CPython 기본값 근처에서 오버플로 나는 걸 직접 관찰
    limit = sys.getrecursionlimit()
    assert limit > 0

    # 꼬리재귀도 TCO가 없으니 recursionlimit을 넘기면 RecursionError가 난다
    try:
        sys.setrecursionlimit(200)
        factorial_tail(500)            # 200단보다 깊은 재귀 → 반드시 실패해야 함
        raise AssertionError("expected RecursionError (TCO 없음을 증명 못 함)")
    except RecursionError:
        pass
    finally:
        sys.setrecursionlimit(limit)

    print("OK")


if __name__ == "__main__":
    _selftest()
