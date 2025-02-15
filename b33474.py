'''
https://www.acmicpc.net/problem/33474
'''


def get_hash(x, y, c):
    global P, Q, MOD;
    # 좌표 (x, y)와 색상 c의 해시값 계산
    return (c * pow(P, x, MOD) * pow(Q, y, MOD)) % MOD


def conceal(x, y, c):
    '''
    global coordinates;
    coordinates[(x, y)] = c
    return;
    '''

    #  (x, y)에 색상 c 저장 및 해시 갱신
    key = (x, y)
    if key in coordinates:
        old_hash = get_hash(x, y, coordinates[key])
        hash_values[key] -= old_hash
        hash_values[key] %= MOD

    coordinates[key] = c
    new_hash = get_hash(x, y, c)
    hash_values[key] = hash_values.get(key, 0) + new_hash
    hash_values[key] %= MOD

# 패턴이 동일한지 확인
def check(x1, y1, x2, y2, w, h):
    '''
    global coordinates;

    pattern1 = []
    pattern2 = []

    for dx in range(w + 1):
        for dy in range(h + 1):
            # pattern1.append(str(coordinates.get((x1 + dx, y1 + dy), 0)))
            # pattern2.append(str(coordinates.get((x2 + dx, y2 + dy), 0)))
            p1 = str(coordinates.get((x1 + dx, y1 + dy), 0))
            p2 = str(coordinates.get((x2 + dx, y2 + dy), 0))

            if p1 != p2:
                return "0";

    return "1";
    '''
    # 두 구역의 해시값 비교
    hash1, hash2 = 0, 0

    for dx in range(w + 1):
        for dy in range(h + 1):
            key1 = (x1 + dx, y1 + dy)
            key2 = (x2 + dx, y2 + dy)
            hash1 += hash_values.get(key1, 0)
            hash2 += hash_values.get(key2, 0)

    return "1" if hash1 % MOD == hash2 % MOD else "0"




import sys;

def subtask():
    # 입력 받은 문자열을 공백을 기준으로 리스트로 변환
    # inputs = list((input().split()))
    inputs = sys.stdin.readline().split()


    op = inputs[0];

    if(op == '1'):
        # 3개의 인자
        x = int(inputs[1]);
        y = int(inputs[2]);
        c = int(inputs[3]);
        conceal(x, y, c);

        
    elif(op == '2'):
        # 6개의 인자
        x1 = int(inputs[1]);
        y1 = int(inputs[2]);
        x2 = int(inputs[3]);
        y2 = int(inputs[4]);
        w = int(inputs[5]);
        h = int(inputs[6]);

        result = check(x1, y1, x2, y2, w, h);
        print(result);

    return;

# 스태가노그라피 기록을 위한 좌표평면
# 변조된 좌표의 값만을 기록, 변조되지 않은 경우 0
coordinates = {};

# 모든 셀을 검사하지 않기 위하여 Rolling Hash 사용
# 해시값 저장을 위한 딕셔너리 선언
hash_values = {}  

MOD = 10**9 + 7
P, Q = 31, 37  # 소수 기반 해싱

def solution():
    # 첫 번째 줄 시행하는 행동의 수
    q = int(input())

    # 
    for _ in range(q): 
        subtask();


solution();