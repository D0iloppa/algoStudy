# https://school.programmers.co.kr/learn/courses/30/lessons/42888  오픈채팅방
# Enter/Leave/Change 기록을 유저ID 기준으로 최종 닉네임까지 확정한 뒤,
# 기록을 다시 순회하며 출력 문구를 만든다(2단계 순회).
# 이유: 기록 도중의 닉네임은 최종값으로 전부 덮어써야 하므로, 기록을 재생하며
#       동시에 출력을 만들면 나중에 바뀐 닉네임을 앞선 줄에 반영할 수 없다.
#       -> 1) 해시맵(uid -> 최종 닉네임)으로 상태를 먼저 확정
#          2) 같은 기록을 다시 훑으며 Enter/Leave만 최종 닉네임으로 출력 생성


def solution(record):
    nickname = {}
    for line in record:
        parts = line.split()
        cmd, uid = parts[0], parts[1]
        if cmd in ("Enter", "Change"):
            nickname[uid] = parts[2]

    result = []
    for line in record:
        parts = line.split()
        cmd, uid = parts[0], parts[1]
        if cmd == "Enter":
            result.append(f"{nickname[uid]}님이 들어왔습니다.")
        elif cmd == "Leave":
            result.append(f"{nickname[uid]}님이 나갔습니다.")
        # Change는 출력을 만들지 않는다.

    return result


if __name__ == "__main__":
    record = [
        "Enter uid1234 Muzi",
        "Enter uid4567 Prodo",
        "Leave uid1234",
        "Enter uid1234 Prodo",
        "Change uid4567 Ryan",
    ]
    expected = [
        "Prodo님이 들어왔습니다.",
        "Ryan님이 들어왔습니다.",
        "Prodo님이 나갔습니다.",
        "Prodo님이 들어왔습니다.",
    ]

    assert solution(record) == expected
    print("OK")
