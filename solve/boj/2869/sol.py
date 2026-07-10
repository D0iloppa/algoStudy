# https://www.acmicpc.net/problem/2869  달팽이는 올라가고 싶다
# 낮에 A 오르고 밤에 B 미끄러진다. 높이 V 정상까지 며칠?
# 마지막 날은 미끄러지지 않으므로 (V-A)를 하루 순증가(A-B)로 나눠 올림 + 1일.
import sys
import math

a, b, v = map(int, sys.stdin.readline().split())
print(math.ceil((v - a) / (a - b)) + 1)
