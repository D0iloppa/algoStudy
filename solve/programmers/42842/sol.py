# https://school.programmers.co.kr/learn/courses/30/lessons/42842  카펫
# 갈색(brown)+노란색(yellow) 격자 수가 주어지면 카펫의 가로/세로[가로,세로](가로>=세로)를 구한다.
# 이유: 전체 넓이 total = brown+yellow = 가로*세로 는 고정이므로, 후보는 total의 약수쌍뿐이다.
#       -> total의 약수쌍(가로>=세로)을 완전탐색하며, 내부 노란 사각형 넓이
#          (가로-2)*(세로-2) == yellow 인 조합을 찾는다. 약수쌍은 O(sqrt(total))개뿐이라
#          완전탐색이 충분히 빠르다(Layer 3 완전탐색 패턴 — 탐색 공간을 제약조건으로 좁힘).


def solution(brown, yellow):
    total = brown + yellow
    for h in range(1, int(total ** 0.5) + 1):
        if total % h != 0:
            continue
        w = total // h
        if w < h:
            continue
        if (w - 2) * (h - 2) == yellow:
            return [w, h]
    return []


if __name__ == "__main__":
    assert solution(10, 2) == [4, 3]
    assert solution(8, 1) == [3, 3]
    assert solution(24, 24) == [8, 6]
    print("OK")
