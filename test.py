import sys

class SegmentTree2D:
    def __init__(self, max_x, max_y):
        """2D 세그먼트 트리 초기화"""
        self.max_x = max_x
        self.max_y = max_y
        self.tree = {}

    def update(self, x, y, value):
        """(x, y) 좌표의 값을 업데이트"""
        self.tree[(x, y)] = value

    def get_hash(self, x, y):
        """해당 좌표의 값을 가져옴 (없으면 0 반환)"""
        return self.tree.get((x, y), 0)

    def range_hash(self, x1, y1, x2, y2, w, h):
        """범위 내의 해시값을 구해서 비교"""
        hash1, hash2 = 0, 0
        for dx in range(w + 1):
            for dy in range(h + 1):
                hash1 += self.get_hash(x1 + dx, y1 + dy)
                hash2 += self.get_hash(x2 + dx, y2 + dy)

        return "1" if hash1 == hash2 else "0"

# 입력 최적화
input = sys.stdin.read
data = input().split("\n")

# 2D 세그먼트 트리 초기화
max_coord = 10**9  # 좌표 범위
segment_tree = SegmentTree2D(max_coord, max_coord)

def solution():
    """메인 실행 함수"""
    q = int(data[0])
    output = []
    index = 1

    for _ in range(q):
        inputs = list(map(int, data[index].split()))
        index += 1

        if inputs[0] == 1:
            # 색칠 (conceal)
            segment_tree.update(inputs[1], inputs[2], inputs[3])
        elif inputs[0] == 2:
            # 패턴 비교 (check)
            result = segment_tree.range_hash(inputs[1], inputs[2], inputs[3], inputs[4], inputs[5], inputs[6])
            output.append(result)

    sys.stdout.write("\n".join(output) + "\n")

solution()
