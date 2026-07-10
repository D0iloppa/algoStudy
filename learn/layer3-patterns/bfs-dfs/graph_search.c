/*
 * Layer 3 · 패턴 — BFS vs DFS (인접리스트 그래프 탐색, C)
 * Notion: 이 폴더 README.md 참조
 *
 * python 버전과 같은 무방향 그래프 (사이클 포함):
 *
 *     A
 *    / \
 *   B   C
 *   |   |
 *   D---E
 *       |
 *       F
 *
 * 그래프 표현은 인접리스트 — 노드마다 이웃 배열(가변 크기, 정점 수가 적으니
 * 고정 상한 배열로 충분하다). 인접행렬은 O(V^2) 공간이라 희소 그래프엔 낭비.
 *
 * 주의(무한루프 함정): visited 처리는 반드시 큐/스택에 push 하는 시점에 한다.
 * pop 시점에 하면 같은 노드가 여러 번 큐/스택에 들어가고, 사이클이 있는 그래프에서는
 * 이게 무한루프로 이어질 수 있다(힙 코드에서 실제로 CPU를 멈춘 전례가 있다).
 *
 * 실행: gcc -O2 -o /tmp/gs graph_search.c && timeout 10 /tmp/gs   (통과 시 'OK')
 */

#include <stdio.h>
#include <string.h>
#include <assert.h>

#define N 6          /* A,B,C,D,E,F -> 0..5 */
#define MAX_DEG 4

static const char *NAMES = "ABCDEF";

typedef struct {
    int nbr[N][MAX_DEG];
    int deg[N];
} Graph;

static void add_edge(Graph *g, int u, int v) {
    g->nbr[u][g->deg[u]++] = v;
    g->nbr[v][g->deg[v]++] = u;
}

static Graph make_graph(void) {
    Graph g;
    memset(&g, 0, sizeof(g));
    add_edge(&g, 0, 1); /* A-B */
    add_edge(&g, 0, 2); /* A-C */
    add_edge(&g, 1, 3); /* B-D */
    add_edge(&g, 2, 4); /* C-E */
    add_edge(&g, 3, 4); /* D-E */
    add_edge(&g, 4, 5); /* E-F */
    return g;
}

/* BFS: 큐(배열+head/tail). 방문처리는 반드시 enqueue 시점. */
static void bfs(const Graph *g, int start, int order[N], int *order_len,
                 int dist[N]) {
    int queue[N];
    int head = 0, tail = 0;
    int visited[N] = {0};

    for (int i = 0; i < N; i++) dist[i] = -1;

    visited[start] = 1;
    dist[start] = 0;
    queue[tail++] = start;
    *order_len = 0;

    while (head < tail) {
        int node = queue[head++];
        order[(*order_len)++] = node;
        for (int i = 0; i < g->deg[node]; i++) {
            int nxt = g->nbr[node][i];
            if (!visited[nxt]) {
                visited[nxt] = 1;        /* push(enqueue) 시점에 방문 확정 */
                dist[nxt] = dist[node] + 1;
                queue[tail++] = nxt;
            }
        }
    }
}

/* DFS 재귀: 방문처리는 함수 진입(=스택에 쌓이는 시점) 직후. */
static void dfs_rec_visit(const Graph *g, int node, int visited[N],
                           int order[N], int *order_len) {
    visited[node] = 1;
    order[(*order_len)++] = node;
    for (int i = 0; i < g->deg[node]; i++) {
        int nxt = g->nbr[node][i];
        if (!visited[nxt]) {
            dfs_rec_visit(g, nxt, visited, order, order_len);
        }
    }
}

static void dfs_recursive(const Graph *g, int start, int order[N],
                           int *order_len, int visited[N]) {
    memset(visited, 0, N * sizeof(int));
    *order_len = 0;
    dfs_rec_visit(g, start, visited, order, order_len);
}

/* DFS 반복: 명시적 스택(배열). push 시점에 방문처리 — 재귀 콜스택을
 * 대체하므로 깊은 그래프에서도 스택 오버플로 없이 동작한다. */
static void dfs_iterative(const Graph *g, int start, int order[N],
                           int *order_len, int visited[N]) {
    int stack[N];
    int top = 0;
    memset(visited, 0, N * sizeof(int));
    *order_len = 0;

    visited[start] = 1;
    stack[top++] = start;

    while (top > 0) {
        int node = stack[--top];
        order[(*order_len)++] = node;
        /* 역순으로 push 해야 재귀 버전과 방문 우선순위가 비슷해진다(필수 아님) */
        for (int i = g->deg[node] - 1; i >= 0; i--) {
            int nxt = g->nbr[node][i];
            if (!visited[nxt]) {
                visited[nxt] = 1;    /* push 시점에 방문 확정 -> 중복 push 방지 */
                stack[top++] = nxt;
            }
        }
    }
}

static int visited_set_eq(const int a[N], const int b[N]) {
    for (int i = 0; i < N; i++) {
        if (a[i] != b[i]) return 0;
    }
    return 1;
}

static void selftest(void) {
    Graph g = make_graph();

    /* (1) BFS 레벨 순서: A=0, B/C=1, D/E=2, F=3 */
    int order[N], dist[N], order_len;
    bfs(&g, 0 /*A*/, order, &order_len, dist);
    assert(order_len == N);
    assert(order[0] == 0); /* A */
    /* order[1],order[2] 는 {B,C} = {1,2} */
    assert((order[1] == 1 && order[2] == 2) || (order[1] == 2 && order[2] == 1));
    /* order[3],order[4] 는 {D,E} = {3,4} */
    assert((order[3] == 3 && order[4] == 4) || (order[3] == 4 && order[4] == 3));
    assert(order[5] == 5); /* F */

    /* dist 가 단조증가(먼저 나온 노드가 dist도 작거나 같음) */
    for (int i = 0; i + 1 < order_len; i++) {
        assert(dist[order[i]] <= dist[order[i + 1]]);
    }

    /* (2) 무가중치 최단거리: A=0,B=1,C=1,D=2,E=2,F=3 */
    int expected_dist[N] = {0, 1, 1, 2, 2, 3};
    for (int i = 0; i < N; i++) assert(dist[i] == expected_dist[i]);

    /* (3) DFS 재귀/반복: 방문 집합은 같아야 함(순서는 달라도 됨) */
    int order_rec[N], order_it[N], len_rec, len_it, vis_rec[N], vis_it[N];
    dfs_recursive(&g, 0, order_rec, &len_rec, vis_rec);
    dfs_iterative(&g, 0, order_it, &len_it, vis_it);

    int all_visited[N] = {1, 1, 1, 1, 1, 1};
    assert(visited_set_eq(vis_rec, all_visited));
    assert(visited_set_eq(vis_it, all_visited));
    assert(order_rec[0] == 0 && order_it[0] == 0);
    /* 한 방향으로 끝까지 파고드는 성질: 두 번째 방문 노드는 BFS 레벨1(B/C) 안에 있음 */
    assert(order_rec[1] == 1 || order_rec[1] == 2);
    assert(order_it[1] == 1 || order_it[1] == 2);

    printf("OK\n");
}

int main(void) {
    selftest();
    return 0;
}
