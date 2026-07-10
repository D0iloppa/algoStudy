/*
 * Layer 2 · 메커니즘 — 링크드 리스트 (C: 포인터 체인이 명시적으로 드러남)
 *
 * Python 버전이 감추는 것을 C 는 그대로 보여준다:
 *   - 노드는 malloc 으로 힙 아무 데나 할당된다(연속 아님)
 *   - '연결'은 다음 노드의 주소(Node*)를 필드에 저장하는 것일 뿐
 *   - 삭제는 앞 노드의 next 를 뒤 노드 주소로 바꾸고, 중간 노드를 free
 *
 * 실행: gcc -O2 -o /tmp/ll linked_list.c && /tmp/ll   (통과 시 'OK')
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

typedef struct Node {
    int val;
    struct Node *next;   /* 다음 노드의 '주소' — 이게 포인터 체인의 실체 */
} Node;

typedef struct {
    Node *head;
    int   size;
} List;

static void list_init(List *l) { l->head = NULL; l->size = 0; }

static void push_front(List *l, int val) {            /* O(1) */
    Node *n = malloc(sizeof(Node));
    n->val = val;
    n->next = l->head;
    l->head = n;
    l->size++;
}

static void push_back(List *l, int val) {             /* O(n) — tail 미보유 */
    Node *n = malloc(sizeof(Node));
    n->val = val; n->next = NULL;
    if (!l->head) { l->head = n; }
    else {
        Node *cur = l->head;
        while (cur->next) cur = cur->next;            /* 끝까지 걸어감 */
        cur->next = n;
    }
    l->size++;
}

static int find(List *l, int val) {                   /* O(n) — 순차 탐색 */
    int idx = 0;
    for (Node *cur = l->head; cur; cur = cur->next, idx++)
        if (cur->val == val) return idx;
    return -1;
}

static int delete_val(List *l, int val) {             /* O(n) 탐색 + O(1) 잇기 */
    Node *prev = NULL, *cur = l->head;
    while (cur) {
        if (cur->val == val) {
            if (!prev) l->head = cur->next;
            else       prev->next = cur->next;        /* 중간 노드 분리 */
            free(cur);                                /* 메모리 해제(Python 은 GC 가 함) */
            l->size--;
            return 1;
        }
        prev = cur; cur = cur->next;
    }
    return 0;
}

static void free_all(List *l) {
    Node *cur = l->head;
    while (cur) { Node *nx = cur->next; free(cur); cur = nx; }
    l->head = NULL; l->size = 0;
}

int main(void) {
    List l; list_init(&l);
    push_back(&l, 1); push_back(&l, 2); push_back(&l, 3);
    push_front(&l, 0);                 /* [0,1,2,3] */
    assert(l.size == 4);
    assert(find(&l, 2) == 2);
    assert(find(&l, 99) == -1);
    assert(delete_val(&l, 2) == 1);    /* [0,1,3] */
    assert(delete_val(&l, 0) == 1);    /* head 삭제 [1,3] */
    assert(l.head->val == 1 && l.head->next->val == 3);
    assert(delete_val(&l, 99) == 0);
    free_all(&l);
    printf("OK\n");
    return 0;
}
