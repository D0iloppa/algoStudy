# https://school.programmers.co.kr/learn/courses/30/lessons/72410  신규 아이디 추천
# 사용자가 입력한 new_id를 카카오 아이디 규칙(3~15자, 소문자/숫자/-/_/. 만 허용,
# 마침표는 처음·끝·연속 불가)에 맞도록 정확히 정해진 7단계를 "순서대로" 적용해 변환한다.
# 이유: 이 문제는 알고리즘적 난이도가 아니라 "문자열 처리" 유형의 전형 —
#       각 단계를 하나도 안 빠뜨리고 정확한 순서로 구현하는 게 핵심이라 단계별로
#       함수를 분리해 순서 실수를 방지한다(Layer 4 §5 카카오 문자열 처리 대표문제).

import re


def step1_lower(s):
    return s.lower()


def step2_filter(s):
    return re.sub(r"[^a-z0-9\-_.]", "", s)


def step3_dedupe_dot(s):
    return re.sub(r"\.+", ".", s)


def step4_strip_dot(s):
    return s.strip(".")


def step5_default(s):
    return "a" if s == "" else s


def step6_truncate(s):
    if len(s) >= 16:
        s = s[:15]
        s = s.rstrip(".") if s.endswith(".") else s
    return s


def step7_pad(s):
    while len(s) <= 2:
        s += s[-1]
    return s


def solution(new_id):
    s = new_id
    s = step1_lower(s)
    s = step2_filter(s)
    s = step3_dedupe_dot(s)
    s = step4_strip_dot(s)
    s = step5_default(s)
    s = step6_truncate(s)
    s = step7_pad(s)
    return s


if __name__ == "__main__":
    assert solution("...!@BaT#*..y.abcdefghijklm") == "bat.y.abcdefghi"
    assert solution("z-+.^.") == "z--"
    assert solution("=.=") == "aaa"
    assert solution("123_.def") == "123_.def"
    assert solution("abcdefghijklmn.p") == "abcdefghijklmn"
    print("OK")
