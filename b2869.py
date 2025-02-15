'''
https://www.acmicpc.net/problem/2869
'''

def getDay(a, b, v):

    day = 0;
    # 현재 높이
    height = 0; 

    while True:
        day += 1;
        height += a;
        if height >= v:
            return day;

        height -= b;

    return;

def getDay_v2(a, b, v):
    import math

    return math.ceil((v - a) / (a - b)) + 1

def solution():

    # a : 낮에 올라가는 높이
    # b : 밤에 미끄러지는 높이
    # v : 나무의 높이
    a, b, v = map(int, input().split())

    day = getDay_v2(a,b,v);
    print(day);


solution();

    