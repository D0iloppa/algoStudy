# https://www.acmicpc.net/problem/14891  톱니바퀴
# 톱니바퀴 4개가 일렬로 놓여있고, 각 톱니바퀴는 8개 톱니(N=0/S=1)를 가진다.
# K번의 회전 명령(톱니바퀴 번호, 방향) 후 최종 상태에서 각 톱니바퀴 12시 방향 극으로 점수를 계산한다.
# deque.rotate가 자연스러운 이유: 톱니바퀴 회전은 원형 리스트를 한 칸씩 shift하는 연산과 정확히
# 같다 — 시계방향(dir=1)은 12시 위치에 이전 7시 자리(인덱스 7)의 값이 들어오는 것과 같아서
# deque.rotate(1)(오른쪽으로 1칸, 즉 new[i]=old[i-1])과 동일하고, 반시계(dir=-1)는 rotate(-1)과 동일하다.
# 회전 "전"에 전파를 전부 확정해야 하는 이유: 인접 톱니바퀴의 회전 여부는 서로 맞닿은 톱니의 극이
# 다른지(원래 상태 기준)로 판단한다. 만약 회전을 실행하면서 다음 톱니바퀴 판단을 하면, 이미 회전해서
# 바뀐 톱니 값을 기준으로 다음 판단을 하게 되어 잘못된 전파(엉뚱한 방향/과다 전파)가 나온다.
# 따라서 "이 회전 명령으로 4개 톱니바퀴가 각각 얼마나/어느 방향으로 돌지"를 배열로 전부 정한 뒤,
# 한 번에 실행한다.
import sys
from collections import deque

# 톱니 인덱스: 0=12시, 시계방향으로 1,2,...,7. 오른쪽 이웃과 맞닿는 톱니=2(3시), 왼쪽 이웃과
# 맞닿는 톱니=6(9시).
RIGHT, LEFT, UP = 2, 6, 0


def main():
    data = sys.stdin.read().split()
    idx = 0
    gears = []
    for _ in range(4):
        gears.append(deque(int(c) for c in data[idx]))
        idx += 1
    k = int(data[idx]); idx += 1

    for _ in range(k):
        num = int(data[idx]) - 1; idx += 1
        d = int(data[idx]); idx += 1

        directions = [0, 0, 0, 0]
        directions[num] = d

        # 왼쪽으로 전파
        cur = d
        i = num - 1
        while i >= 0:
            if gears[i][RIGHT] != gears[i + 1][LEFT]:
                cur = -cur
                directions[i] = cur
                i -= 1
            else:
                break

        # 오른쪽으로 전파
        cur = d
        i = num + 1
        while i < 4:
            if gears[i - 1][RIGHT] != gears[i][LEFT]:
                cur = -cur
                directions[i] = cur
                i += 1
            else:
                break

        for i in range(4):
            if directions[i] != 0:
                gears[i].rotate(directions[i])

    score = sum((1 << i) * gears[i][UP] for i in range(4) if gears[i][UP] == 1)
    print(score)


main()
