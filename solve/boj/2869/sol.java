// https://www.acmicpc.net/problem/2869  달팽이는 올라가고 싶다
// 백준 규칙: public class 이름은 Main.
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        long a = Long.parseLong(st.nextToken());
        long b = Long.parseLong(st.nextToken());
        long v = Long.parseLong(st.nextToken());
        // ceil((v-a)/(a-b)) + 1  — 정수 나눗셈 올림
        long days = (v - a + (a - b) - 1) / (a - b) + 1;
        System.out.println(days);
    }
}
