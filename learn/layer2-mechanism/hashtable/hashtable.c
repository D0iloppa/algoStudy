/*
 * Layer 2 · 메커니즘 — 해시테이블 (C: 체이닝, 버킷마다 링크드리스트)
 *
 * Python 버전이 감추는 것을 C 는 그대로 보여준다:
 *   - 버킷 배열은 연속 메모리(Node* 포인터 배열), 각 버킷은 malloc 으로 흩어진 노드 체인
 *   - hash(key) % capacity 로 인덱스를 구하고, 충돌 시 체인 맨 앞에 노드를 붙인다
 *   - load factor(size/capacity) 가 임계치를 넘으면 capacity 를 2배로 늘리고
 *     모든 노드를 새 배열로 재해싱(rehash)한다 — 이때 인덱스가 전부 바뀐다
 *
 * 실행: gcc -O2 -o /tmp/ht hashtable.c && /tmp/ht   (통과 시 'OK')
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#define LOAD_FACTOR_LIMIT 0.75

typedef struct Node {
    char *key;
    int   val;
    struct Node *next;      /* 같은 버킷 안 다음 노드의 주소 — 체인의 실체 */
} Node;

typedef struct {
    Node **buckets;         /* 버킷 배열 자체는 연속, 각 원소는 체인의 head */
    int    capacity;
    int    size;
} HashTable;

static unsigned long djb2_hash(const char *s) {   /* 단순 해시함수 */
    unsigned long h = 5381;
    int c;
    while ((c = (unsigned char)*s++))
        h = ((h << 5) + h) + c;                   /* h * 33 + c */
    return h;
}

static void ht_init(HashTable *t, int capacity) {
    t->capacity = capacity;
    t->buckets = calloc(capacity, sizeof(Node *));
    t->size = 0;
}

static char *dup_str(const char *s) {
    char *d = malloc(strlen(s) + 1);
    strcpy(d, s);
    return d;
}

static void ht_resize(HashTable *t, int new_capacity);

static void ht_put(HashTable *t, const char *key, int val) {
    unsigned long idx = djb2_hash(key) % t->capacity;
    Node *cur = t->buckets[idx];
    while (cur) {                                 /* 같은 키면 값만 갱신 */
        if (strcmp(cur->key, key) == 0) { cur->val = val; return; }
        cur = cur->next;
    }
    Node *n = malloc(sizeof(Node));
    n->key = dup_str(key);
    n->val = val;
    n->next = t->buckets[idx];                    /* 체인 맨 앞에 삽입 O(1) */
    t->buckets[idx] = n;
    t->size++;
    if ((double)t->size / t->capacity > LOAD_FACTOR_LIMIT)
        ht_resize(t, t->capacity * 2);
}

static int ht_get(HashTable *t, const char *key, int *out) {
    unsigned long idx = djb2_hash(key) % t->capacity;
    for (Node *cur = t->buckets[idx]; cur; cur = cur->next)
        if (strcmp(cur->key, key) == 0) { *out = cur->val; return 1; }
    return 0;
}

static int ht_delete(HashTable *t, const char *key) {
    unsigned long idx = djb2_hash(key) % t->capacity;
    Node *prev = NULL, *cur = t->buckets[idx];
    while (cur) {
        if (strcmp(cur->key, key) == 0) {
            if (!prev) t->buckets[idx] = cur->next;
            else       prev->next = cur->next;
            free(cur->key);
            free(cur);
            t->size--;
            return 1;
        }
        prev = cur; cur = cur->next;
    }
    return 0;
}

static void ht_resize(HashTable *t, int new_capacity) {
    Node **old_buckets = t->buckets;
    int old_capacity = t->capacity;

    t->buckets = calloc(new_capacity, sizeof(Node *));
    t->capacity = new_capacity;
    t->size = 0;

    for (int i = 0; i < old_capacity; i++) {       /* 전체 재해싱 */
        Node *cur = old_buckets[i];
        while (cur) {
            Node *nx = cur->next;
            ht_put(t, cur->key, cur->val);         /* 새 capacity 기준으로 재삽입 */
            free(cur->key);
            free(cur);
            cur = nx;
        }
    }
    free(old_buckets);
}

static void ht_free(HashTable *t) {
    for (int i = 0; i < t->capacity; i++) {
        Node *cur = t->buckets[i];
        while (cur) { Node *nx = cur->next; free(cur->key); free(cur); cur = nx; }
    }
    free(t->buckets);
    t->buckets = NULL; t->capacity = 0; t->size = 0;
}

int main(void) {
    HashTable t;
    ht_init(&t, 4);

    ht_put(&t, "a", 1);
    ht_put(&t, "b", 2);
    ht_put(&t, "c", 3);
    int out;
    assert(ht_get(&t, "a", &out) && out == 1);
    assert(ht_get(&t, "b", &out) && out == 2);
    assert(!ht_get(&t, "z", &out));
    ht_put(&t, "a", 100);                          /* 갱신, size 불변 */
    assert(ht_get(&t, "a", &out) && out == 100);
    assert(t.size == 3);

    /* 리사이즈 유발: capacity 4로 시작해 다수 삽입 */
    HashTable t2;
    ht_init(&t2, 2);
    char buf[16];
    int n = 50;
    for (int i = 0; i < n; i++) {
        sprintf(buf, "k%d", i);
        ht_put(&t2, buf, i * i);
    }
    assert(t2.capacity > 2);                       /* 실제로 리사이즈 발생 */
    for (int i = 0; i < n; i++) {
        sprintf(buf, "k%d", i);
        assert(ht_get(&t2, buf, &out) && out == i * i);
    }
    assert(t2.size == n);

    assert(ht_delete(&t, "b") == 1);
    assert(!ht_get(&t, "b", &out));
    assert(ht_delete(&t, "nope") == 0);
    assert(t.size == 2);

    ht_free(&t);
    ht_free(&t2);
    printf("OK\n");
    return 0;
}
