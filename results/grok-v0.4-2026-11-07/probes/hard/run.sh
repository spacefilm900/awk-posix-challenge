#!/usr/bin/env bash
# name<TAB>program<TAB>operands("_" = none)<TAB>stdin-file("-" = /dev/null). Observational only.
cd "$(dirname "$0")"
G=/workspace/refs/local/bin/gawk
declare -A IMPL=( [pyawk]="python3 -m pyawk" [hawk]=/workspace/hawk/target/release/hawk [mawk]=/usr/bin/mawk
  [gawkP]="$G --posix" [gawk]="$G" [onetrue]=/workspace/refs/onetrue-awk/a.out [busybox]="/workspace/refs/busybox/busybox awk" )
while IFS=$'\t' read -r name prog args sin; do
  echo "## $name: $prog  | operands: ${args} | stdin: ${sin}"
  [ "$sin" = "-" ] && sin=/dev/null; [ "$args" = "_" ] && args=""
  for i in pyawk hawk mawk gawkP gawk onetrue busybox; do
    if [ "$name" = fs_dash_F_tab ]; then extra=(-F '\t'); else extra=(); fi
    o=$(APCX=010 PYTHONPATH=/workspace/pyawk LC_ALL=C ${IMPL[$i]} "${extra[@]}" "$prog" $args 2>&1 <"$sin"); rc=$?
    printf '  %-8s rc=%s %s\n' "$i" "$rc" "$(printf '%s' "$o" | tr '\n' '|' | cut -c1-120)"
  done
done < hard_probes.tsv
