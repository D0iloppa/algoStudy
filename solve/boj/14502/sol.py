# https://www.acmicpc.net/problem/14502  연구소
# N×M 격자에 빈칸(0)/벽(1)/바이러스(2)가 있다. 빈칸 중 정확히 3개를 새 벽으로 세운 뒤
# 바이러스가 상하좌우로 퍼진다(BFS). 벽 세우기 조합을 완전탐색해서 안전 영역
# (끝까지 빈칸으로 남는 칸) 개수의 최댓값을 구한다.
#
# 왜 "빈칸 3개 조합 완전탐색"이 통하는가: N,M ≤ 8이라 격자 전체가 최대 64칸이고, 빈칸이
# 아무리 많아도 조합 수는 최악의 경우 64C3 = 41,664 수준이다. 조합마다 O(NM) BFS 한 번씩
# 돌려도 전체가 수백만 연산 안쪽이라 2초 제한을 넉넉히 통과한다 — Layer 1에서 다룬
# "N 제한을 보고 허용 복잡도를 역산"하는 삼성식 전형(N이 작으면 브루트포스를 그대로 허용)이
# 이 문제에 정확히 들어맞는다.
#
# 조합마다 격자를 "새로 만들어서" 벽을 세우고 BFS하는 이유: 원본 grid를 그대로 두고 벽을
# 세웠다가 되돌리는 방식은 실수하기 쉽다(얕은 복사로 원본이 오염되는 흔한 함정). 매 조합마다
# 원본 2차원 리스트를 행 단위로 새로 복사(`[row[:] for row in grid]`)해서 원본을 건드리지
# 않고 그 위에서만 벽을 세우고 BFS를 돌린다.
import sys
from collections import deque
from itertools import combinations


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1

    grid = []
    for _ in range(n):
        row = [int(data[idx + j]) for j in range(m)]
        idx += m
        grid.append(row)

    empties = [(r, c) for r in range(n) for c in range(m) if grid[r][c] == 0]
    viruses = [(r, c) for r in range(n) for c in range(m) if grid[r][c] == 2]

    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]

    best = 0
    for walls in combinations(empties, 3):
        sim = [row[:] for row in grid]
        for r, c in walls:
            sim[r][c] = 1

        visited = [row[:] for row in sim]
        q = deque(viruses)
        while q:
            r, c = q.popleft()
            for k in range(4):
                nr, nc = r + dr[k], c + dc[k]
                if 0 <= nr < n and 0 <= nc < m and visited[nr][nc] == 0:
                    visited[nr][nc] = 2
                    q.append((nr, nc))

        safe = sum(row.count(0) for row in visited)
        if safe > best:
            best = safe

    print(best)


main()
