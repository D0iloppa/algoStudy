/* https://www.acmicpc.net/problem/2869  달팽이는 올라가고 싶다 */
#include <stdio.h>

int main(void) {
    long long a, b, v;
    scanf("%lld %lld %lld", &a, &b, &v);
    /* ceil((v-a)/(a-b)) + 1 — 정수 올림 나눗셈 */
    long long days = (v - a + (a - b) - 1) / (a - b) + 1;
    printf("%lld\n", days);
    return 0;
}
