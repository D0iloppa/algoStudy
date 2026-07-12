# https://www.acmicpc.net/problem/16236  아기 상어
# N×N 격자, 상어(초기 크기2)가 자기보다 작은 물고기만 먹으며 성장하는 시뮬레이션.
# 매 턴 "가장 가까운(동률이면 위쪽, 그다음 왼쪽) 먹을 수 있는 물고기"를 BFS로 새로 찾는다.
# 캐시 불가한 이유: 상어의 위치·크기가 매 턴 바뀌므로 도달 가능 경로(자신 크기 이하 칸만 통과)와
# 최단거리가 매번 달라진다 — 이전 턴의 BFS 결과를 재사용할 수 없다.
import sys
from collections import deque


def find_target(grid, N, sx, sy, size):
    """상어(sx,sy), 크기 size에서 먹을 수 있는 가장 가까운 물고기를 BFS로 탐색.
    거리 -> 행 -> 열 우선순위로 반환. 없으면 None."""
    dist = [[-1] * N for _ in range(N)]
    dist[sx][sy] = 0
    q = deque([(sx, sy)])
    candidates = []
    while q:
        x, y = q.popleft()
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < N and 0 <= ny < N and dist[nx][ny] == -1 and grid[nx][ny] <= size:
                dist[nx][ny] = dist[x][y] + 1
                if 0 < grid[nx][ny] < size:
                    candidates.append((dist[nx][ny], nx, ny))
                q.append((nx, ny))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0]


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    grid = []
    sx = sy = 0
    for i in range(n):
        row = []
        for j in range(n):
            v = int(data[idx]); idx += 1
            if v == 9:
                sx, sy = i, j
                v = 0
            row.append(v)
        grid.append(row)

    size = 2
    eaten = 0
    time = 0
    while True:
        target = find_target(grid, n, sx, sy, size)
        if target is None:
            break
        d, nx, ny = target
        time += d
        grid[nx][ny] = 0
        sx, sy = nx, ny
        eaten += 1
        if eaten == size:
            size += 1
            eaten = 0

    print(time)


main()
