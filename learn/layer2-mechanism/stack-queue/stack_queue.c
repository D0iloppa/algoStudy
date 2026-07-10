/*
 * Layer 2 · 메커니즘 — 스택과 큐 (C: 배열 기반 스택 + 원형 버퍼 큐)
 *
 * Python 버전과 동일 로직. C에서는 realloc/memcpy로 재할당이 명시적으로 드러난다.
 *
 * 이 파일이 답하는 질문:
 *   "단순 배열 큐가 dequeue마다 front를 밀며 앞 슬롯을 버리는 문제를
 *    원형 버퍼(모듈러 인덱싱)가 어떻게 해결하는가"
 *
 * 실행: gcc -O2 -o /tmp/sq stack_queue.c && /tmp/sq   (통과 시 'OK')
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

/* ---------- 스택: 배열 기반, top 한쪽만 push/pop ---------- */
typedef struct {
    int *data;
    int capacity;
    int top;      /* 다음 push가 들어갈 빈 인덱스 = 현재 원소 개수 */
} Stack;

static void stack_init(Stack *s, int capacity) {
    s->data = malloc(sizeof(int) * capacity);
    s->capacity = capacity;
    s->top = 0;
}

static void stack_resize(Stack *s, int new_cap) {
    int *nd = malloc(sizeof(int) * new_cap);
    for (int i = 0; i < s->top; i++) nd[i] = s->data[i];
    free(s->data);
    s->data = nd;
    s->capacity = new_cap;
}

static void stack_push(Stack *s, int val) {           /* O(1) amortized */
    if (s->top == s->capacity) stack_resize(s, s->capacity * 2);
    s->data[s->top++] = val;
}

static int stack_pop(Stack *s, int *ok) {              /* O(1) */
    if (s->top == 0) { *ok = 0; return 0; }
    *ok = 1;
    return s->data[--s->top];
}

static int stack_empty(Stack *s) { return s->top == 0; }
static void stack_free(Stack *s) { free(s->data); }

/* ---------- 큐: 원형 버퍼, front/rear를 capacity로 모듈러 순환 ---------- */
typedef struct {
    int *data;
    int capacity;
    int front;    /* 다음 dequeue가 읽을 인덱스 */
    int size;     /* front/rear만으로는 가득/빈 구분 불가 -> 별도 카운트 */
} CQueue;

static void cq_init(CQueue *q, int capacity) {
    q->data = malloc(sizeof(int) * capacity);
    q->capacity = capacity;
    q->front = 0;
    q->size = 0;
}

static void cq_resize(CQueue *q, int new_cap) {
    int *nd = malloc(sizeof(int) * new_cap);
    for (int i = 0; i < q->size; i++)
        nd[i] = q->data[(q->front + i) % q->capacity];  /* 논리 순서로 재배치 */
    free(q->data);
    q->data = nd;
    q->capacity = new_cap;
    q->front = 0;
}

static void cq_enqueue(CQueue *q, int val) {            /* O(1) amortized */
    if (q->size == q->capacity) cq_resize(q, q->capacity * 2);
    int rear = (q->front + q->size) % q->capacity;
    q->data[rear] = val;
    q->size++;
}

static int cq_dequeue(CQueue *q, int *ok) {              /* O(1) */
    if (q->size == 0) { *ok = 0; return 0; }
    int val = q->data[q->front];
    q->front = (q->front + 1) % q->capacity;              /* 슬롯을 버리지 않고 순환 */
    q->size--;
    *ok = 1;
    return val;
}

static int cq_empty(CQueue *q) { return q->size == 0; }
static void cq_free(CQueue *q) { free(q->data); }

int main(void) {
    int ok;

    /* --- 스택: LIFO --- */
    Stack s; stack_init(&s, 2);
    stack_push(&s, 1); stack_push(&s, 2); stack_push(&s, 3);  /* capacity 2 -> resize */
    assert(s.top == 3);
    assert(stack_pop(&s, &ok) == 3 && ok);
    assert(stack_pop(&s, &ok) == 2 && ok);
    assert(stack_pop(&s, &ok) == 1 && ok);
    assert(stack_empty(&s));
    stack_pop(&s, &ok);
    assert(!ok);                        /* 언더플로 감지 */
    stack_free(&s);

    /* --- 원형 큐: FIFO + 슬롯 재사용 --- */
    CQueue q; cq_init(&q, 3);
    cq_enqueue(&q, 1); cq_enqueue(&q, 2); cq_enqueue(&q, 3);   /* 꽉 참 */
    assert(cq_dequeue(&q, &ok) == 1 && ok);   /* front가 순환 이동 */
    cq_enqueue(&q, 4);                         /* 비워진 슬롯을 재사용 (resize 없이) */
    assert(q.size == 3);
    assert(cq_dequeue(&q, &ok) == 2 && ok);
    assert(cq_dequeue(&q, &ok) == 3 && ok);
    assert(cq_dequeue(&q, &ok) == 4 && ok);
    assert(cq_empty(&q));
    cq_dequeue(&q, &ok);
    assert(!ok);                        /* 언더플로 감지 */
    cq_free(&q);

    /* --- resize 후에도 FIFO 순서 유지 --- */
    CQueue q2; cq_init(&q2, 2);
    for (int v = 0; v < 5; v++) cq_enqueue(&q2, v);  /* 중간에 여러 번 resize */
    for (int v = 0; v < 5; v++) {
        int got = cq_dequeue(&q2, &ok);
        assert(ok && got == v);
    }
    cq_free(&q2);

    printf("OK\n");
    return 0;
}
