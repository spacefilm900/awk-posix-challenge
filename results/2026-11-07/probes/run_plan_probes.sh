#!/usr/bin/env bash
# Re-runs the exploratory one-liners in plan_probes.tsv (name<TAB>program<TAB>operands)
# against six interpreters. Observational only: these are NOT oracles.
set -u
cd "$(dirname "$0")"; work=$(mktemp -d); cp plan_probes.tsv "$work"; cd "$work"
printf 'a1\na2\n' > f1; printf 'b1\nb2\nb3\n' > f2; printf 'p1 x\np1 y\n\n\n\np2 z\n\n' > para; printf 'a b\n   \nc d\n\ne f\n' > blank; printf 'a:b c\nd:e f\n' > fsin
G=/workspace/refs/local/bin/gawk
declare -A IMPL=( [pyawk]="python3 -m pyawk" [hawk]=/workspace/hawk/target/release/hawk [mawk]=/usr/bin/mawk
  [gawkP]="$G --posix" [onetrue]=/workspace/refs/onetrue-awk/a.out [busybox]="/workspace/refs/busybox/busybox awk" )
while IFS=$'\t' read -r name prog args; do
  echo "## $name: $prog  ${args}"
  for i in pyawk hawk mawk gawkP onetrue busybox; do
    rm -f out o2
    o=$(PYTHONPATH=/workspace/pyawk LC_ALL=C ${IMPL[$i]} "$prog" $args 2>&1 </dev/null); rc=$?
    printf '  %-8s rc=%s %s\n' "$i" "$rc" "$(echo "$o" | tr '\n' '|' | cut -c1-110)"
  done
done < plan_probes.tsv
