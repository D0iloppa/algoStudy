#!/usr/bin/env bash
# judge.sh — 다언어 코딩테스트 로컬 채점기
#
# 사용법:
#   runtime/judge.sh <solution-file> [test-dir]
#
#   solution-file : 풀이 파일. 확장자로 언어 자동 감지 (.py .java .c .cpp)
#   test-dir      : 테스트 케이스 폴더. 생략 시 <풀이파일 폴더>/tests
#
# 테스트 케이스 규칙:
#   test-dir 안에 N.in / N.out 페어를 둔다 (1.in, 1.out, 2.in, ...).
#   *.in 을 stdin 으로 넣고 stdout 을 *.out 과 비교(줄끝 공백 무시).
#
# 언어 규칙:
#   java  : public class 는 반드시 Main (백준 규칙과 동일)
#   c/cpp : gcc/g++ -O2 로 컴파일
#
# 출력: 케이스별 PASS/FAIL + 실행시간(ms), 마지막에 요약.
set -u

sol="${1:-}"
if [[ -z "$sol" || ! -f "$sol" ]]; then
  echo "usage: runtime/judge.sh <solution-file> [test-dir]" >&2
  exit 2
fi

sol_dir="$(cd "$(dirname "$sol")" && pwd)"
sol_base="$(basename "$sol")"
ext="${sol_base##*.}"
testdir="${2:-$sol_dir/tests}"

if [[ ! -d "$testdir" ]]; then
  echo "no test dir: $testdir" >&2
  exit 2
fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# --- 컴파일 / 실행 커맨드 준비 -------------------------------------------------
run_cmd=()
case "$ext" in
  py)
    run_cmd=(python3 "$sol")
    ;;
  java)
    cp "$sol" "$tmp/Main.java"
    if ! javac -d "$tmp" "$tmp/Main.java" 2> "$tmp/cc.log"; then
      echo "[compile error]"; cat "$tmp/cc.log"; exit 1
    fi
    run_cmd=(java -cp "$tmp" Main)
    ;;
  c)
    if ! gcc -O2 -o "$tmp/a.out" "$sol" 2> "$tmp/cc.log"; then
      echo "[compile error]"; cat "$tmp/cc.log"; exit 1
    fi
    run_cmd=("$tmp/a.out")
    ;;
  cpp|cc|cxx)
    if ! g++ -O2 -o "$tmp/a.out" "$sol" 2> "$tmp/cc.log"; then
      echo "[compile error]"; cat "$tmp/cc.log"; exit 1
    fi
    run_cmd=("$tmp/a.out")
    ;;
  *)
    echo "unsupported extension: .$ext" >&2; exit 2 ;;
esac

# --- 케이스 실행 --------------------------------------------------------------
norm() { sed -e 's/[[:space:]]*$//' "$1" | sed -e '${/^$/d}'; }  # 줄끝 공백 + 마지막 빈줄 정규화

pass=0; fail=0; total=0
shopt -s nullglob
infiles=("$testdir"/*.in)
if [[ ${#infiles[@]} -eq 0 ]]; then
  echo "no *.in cases in $testdir" >&2; exit 2
fi

echo "sol=$sol  lang=$ext  tests=$testdir"
echo "------------------------------------------------------------"
for infile in $(printf '%s\n' "${infiles[@]}" | sort -V); do
  name="$(basename "$infile" .in)"
  expected="$testdir/$name.out"
  total=$((total+1))

  start="$(date +%s%N)"
  "${run_cmd[@]}" < "$infile" > "$tmp/out.txt" 2> "$tmp/err.txt"
  rc=$?
  end="$(date +%s%N)"
  ms=$(( (end - start) / 1000000 ))

  if [[ $rc -ne 0 ]]; then
    printf "  %-6s RUNTIME-ERR (rc=%d, %dms)\n" "$name" "$rc" "$ms"
    head -3 "$tmp/err.txt" | sed 's/^/         /'
    fail=$((fail+1)); continue
  fi

  if [[ ! -f "$expected" ]]; then
    printf "  %-6s NO-EXPECTED (%dms)  -- 실제출력:\n" "$name" "$ms"
    sed 's/^/         /' "$tmp/out.txt"
    continue
  fi

  if diff -q <(norm "$tmp/out.txt") <(norm "$expected") > /dev/null; then
    printf "  %-6s PASS  (%dms)\n" "$name" "$ms"
    pass=$((pass+1))
  else
    printf "  %-6s FAIL  (%dms)\n" "$name" "$ms"
    echo "         --- expected ---"; sed 's/^/         /' "$expected" | head -10
    echo "         --- got ---";      sed 's/^/         /' "$tmp/out.txt" | head -10
    fail=$((fail+1))
  fi
done
echo "------------------------------------------------------------"
echo "result: $pass passed, $fail failed, $total total"
[[ $fail -eq 0 ]]
