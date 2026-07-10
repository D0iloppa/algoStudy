/*
 * Layer 3 · 패턴 — 트리 순회 (C: 재귀 콜스택 vs 명시적 스택이 눈에 보임)
 *
 * Python 버전과 같은 로직. C 에서는 반복 버전의 "명시적 스택"이
 * 재귀 버전의 "콜스택"과 구조적으로 동일하다는 게 배열로 그대로 드러난다.
 *
 * 실행: gcc -O2 -o /tmp/tt tree_traversal.c && /tmp/tt   (통과 시 'OK')
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#define MAX 64

typedef struct Node {
    int val;
    struct Node *left;
    struct Node *right;
} Node;

static Node *make_node(int val, Node *left, Node *right) {
    Node *n = malloc(sizeof(Node));
    n->val = val; n->left = left; n->right = right;
    return n;
}

/* ---------- 재귀 버전 ---------- */

static void preorder_recursive(Node *root, int *out, int *n) {
    if (!root) return;
    out[(*n)++] = root->val;
    preorder_recursive(root->left, out, n);
    preorder_recursive(root->right, out, n);
}

static void inorder_recursive(Node *root, int *out, int *n) {
    if (!root) return;
    inorder_recursive(root->left, out, n);
    out[(*n)++] = root->val;
    inorder_recursive(root->right, out, n);
}

static void postorder_recursive(Node *root, int *out, int *n) {
    if (!root) return;
    postorder_recursive(root->left, out, n);
    postorder_recursive(root->right, out, n);
    out[(*n)++] = root->val;
}

/* ---------- 반복 버전 (명시적 스택) ---------- */

static void preorder_iterative(Node *root, int *out, int *n) {
    Node *stack[MAX]; int sp = 0;
    if (root) stack[sp++] = root;
    while (sp) {
        Node *node = stack[--sp];
        out[(*n)++] = node->val;
        if (node->right) stack[sp++] = node->right;   /* 오른쪽 먼저 push */
        if (node->left)  stack[sp++] = node->left;     /* 왼쪽이 나중 push → 먼저 pop */
    }
}

static void inorder_iterative(Node *root, int *out, int *n) {
    Node *stack[MAX]; int sp = 0;
    Node *cur = root;
    while (cur || sp) {
        while (cur) { stack[sp++] = cur; cur = cur->left; }
        cur = stack[--sp];
        out[(*n)++] = cur->val;
        cur = cur->right;
    }
}

static void postorder_iterative(Node *root, int *out, int *n) {
    /* 두 스택 트릭: "root->right->left" 순서로 모은 뒤 뒤집으면 "left->right->root" */
    Node *stack[MAX]; int sp = 0;
    int tmp[MAX]; int tn = 0;
    if (root) stack[sp++] = root;
    while (sp) {
        Node *node = stack[--sp];
        tmp[tn++] = node->val;
        if (node->left)  stack[sp++] = node->left;
        if (node->right) stack[sp++] = node->right;
    }
    for (int i = tn - 1; i >= 0; i--) out[(*n)++] = tmp[i];
}

/* ---------- 레벨순회 (BFS, 보너스 — 스택이 아니라 큐) ---------- */

static void level_order(Node *root, int *out, int *n) {
    Node *queue[MAX]; int head = 0, tail = 0;
    if (root) queue[tail++] = root;
    while (head < tail) {
        Node *node = queue[head++];          /* 큐: 앞에서 꺼냄(FIFO) */
        out[(*n)++] = node->val;
        if (node->left)  queue[tail++] = node->left;
        if (node->right) queue[tail++] = node->right;
    }
}

static int arr_eq(int *a, int an, int *b, int bn) {
    if (an != bn) return 0;
    for (int i = 0; i < an; i++) if (a[i] != b[i]) return 0;
    return 1;
}

int main(void) {
    /*         1
     *        / \
     *       2   3
     *      / \   \
     *     4   5   6
     */
    Node *root = make_node(1,
        make_node(2, make_node(4, NULL, NULL), make_node(5, NULL, NULL)),
        make_node(3, NULL, make_node(6, NULL, NULL)));

    int pre_exp[]  = {1, 2, 4, 5, 3, 6};
    int in_exp[]   = {4, 2, 5, 1, 3, 6};
    int post_exp[] = {4, 5, 2, 6, 3, 1};
    int lvl_exp[]  = {1, 2, 3, 4, 5, 6};

    int out[MAX], n;

    n = 0; preorder_recursive(root, out, &n);
    assert(arr_eq(out, n, pre_exp, 6));
    n = 0; inorder_recursive(root, out, &n);
    assert(arr_eq(out, n, in_exp, 6));
    n = 0; postorder_recursive(root, out, &n);
    assert(arr_eq(out, n, post_exp, 6));

    int out2[MAX], n2;

    n = 0; preorder_iterative(root, out, &n);
    n2 = 0; preorder_recursive(root, out2, &n2);
    assert(arr_eq(out, n, out2, n2));

    n = 0; inorder_iterative(root, out, &n);
    n2 = 0; inorder_recursive(root, out2, &n2);
    assert(arr_eq(out, n, out2, n2));

    n = 0; postorder_iterative(root, out, &n);
    n2 = 0; postorder_recursive(root, out2, &n2);
    assert(arr_eq(out, n, out2, n2));

    n = 0; level_order(root, out, &n);
    assert(arr_eq(out, n, lvl_exp, 6));

    /* 빈 트리 */
    n = 0; preorder_recursive(NULL, out, &n);
    assert(n == 0);
    n = 0; inorder_iterative(NULL, out, &n);
    assert(n == 0);
    n = 0; postorder_iterative(NULL, out, &n);
    assert(n == 0);
    n = 0; level_order(NULL, out, &n);
    assert(n == 0);

    printf("OK\n");
    return 0;
}
