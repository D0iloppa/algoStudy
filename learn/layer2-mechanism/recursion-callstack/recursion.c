/*
 * Layer 2 · 메커니즘 — 재귀와 콜 스택 (C: 프레임/복귀주소가 실제로 스택에 쌓임)
 *
 * Python 버전이 감추는 것을 C 는 그대로 보여준다:
 *   - 함수 호출 = 콜스택에 프레임 push (인자, 지역변수, '복귀 주소')
 *   - return = 프레임 pop, 복귀 주소로 점프
 *   - 재귀가 너무 깊으면 스택 메모리가 바닥나 세그폴트(스택 오버플로) —
 *     C는 파이썬의 RecursionError 같은 안전장치가 없어 그냥 크래시한다.
 *     (그래서 이 파일은 오버플로를 '일으키지' 않고 자료구조 레벨로만 보여준다.)
 *
 * 실행: gcc -O2 -o /tmp/rc recursion.c && /tmp/rc   (통과 시 'OK')
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

/* ---------------------------------------------------------------------
 * 1) 재귀 버전 — 팩토리얼 / 피보나치
 * --------------------------------------------------------------------- */
static long factorial_rec(int n) {           /* 호출마다 프레임 push, n단 깊이 */
    if (n <= 1) return 1;                    /* 종료조건 */
    return n * factorial_rec(n - 1);         /* 복귀 후 곱셈 → 꼬리호출 아님 */
}

static long fib_rec(int n) {                 /* 트리 재귀 — 중복계산의 대표 예 */
    if (n <= 1) return n;
    return fib_rec(n - 1) + fib_rec(n - 2);
}

/* ---------------------------------------------------------------------
 * 2) 재귀 → 반복 변환 — 명시적 스택(배열)으로 콜스택을 손으로 흉내
 * --------------------------------------------------------------------- */
static long factorial_iter(int n) {
    int stack[64];                           /* 콜스택 대신 쓰는 명시적 스택 */
    int top = 0;
    while (n > 1) {                          /* 재귀 호출이 쌓이던 지점 → push */
        stack[top++] = n--;
    }
    long result = 1;
    while (top > 0) {                        /* return하며 곱셈하던 지점 → pop */
        result *= stack[--top];
    }
    return result;
}

/* frame: 피보나치 재귀호출 하나를 흉내내는 명시적 스택 원소 */
typedef struct { int k; int visit; } Frame;

static long fib_iter(int n) {
    if (n <= 1) return n;

    long memo[64];
    int has[64] = {0};
    memo[0] = 0; memo[1] = 1; has[0] = has[1] = 1;

    Frame stack[128];
    int top = 0;
    stack[top++] = (Frame){n, 1};

    while (top > 0) {
        Frame *f = &stack[top - 1];
        if (has[f->k]) { top--; continue; }
        if (f->visit == 1) {                 /* 아직 하위 호출을 안 만들었으면 자식 push */
            f->visit = 2;
            if (!has[f->k - 1]) stack[top++] = (Frame){f->k - 1, 1};
            if (!has[f->k - 2]) stack[top++] = (Frame){f->k - 2, 1};
        } else {                             /* 두 하위 결과 준비됨 → '복귀' */
            memo[f->k] = memo[f->k - 1] + memo[f->k - 2];
            has[f->k] = 1;
            top--;
        }
    }
    return memo[n];
}

/* ---------------------------------------------------------------------
 * 3) 꼬리재귀 형태 — C 컴파일러는 -O2 에서 TCO를 적용해줄 수 있지만
 *    (gcc가 알아서 루프로 변환), 언어 명세가 보장하는 건 아니다.
 * --------------------------------------------------------------------- */
static long factorial_tail(int n, long acc) {   /* 마지막 동작이 재귀호출 자체 */
    if (n <= 1) return acc;
    return factorial_tail(n - 1, acc * n);      /* 복귀 후 할 일 없음 → 꼬리호출 */
}

int main(void) {
    assert(factorial_rec(5) == 120);
    assert(factorial_iter(5) == 120);
    assert(factorial_tail(5, 1) == 120);
    assert(factorial_rec(0) == 1 && factorial_iter(0) == 1);

    for (int n = 0; n < 15; n++) {
        assert(fib_rec(n) == fib_iter(n));
    }

    printf("OK\n");
    return 0;
}
