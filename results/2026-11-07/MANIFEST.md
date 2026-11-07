# Baseline results manifest: v0.3 run of 2026-11-07

This file records exactly how the five result files in this folder were produced, so the run can be repeated.
It describes the run; it does not change any case. Times are UTC (the machine's clock is UTC, which is also
the user's local time, Europe/London, in November).

## 1. What was tested

| Item | Value |
|---|---|
| Challenge repository | `spacefilm900/awk-posix-challenge` (private) |
| Corpus commit tested | `a14127d9bed3f954cb81a0ccc22f77c4384ace67` ("Import ChatGPT's independent POSIX AWK challenge v0.3 (250 cases), unchanged from the supplied zip"), 2026-11-07 06:18:45 UTC |
| Corpus integrity | `sha256sum -c SHA256SUMS.txt` passes (1,250 entries: 5 files x 250 cases) |
| `SHA256SUMS.txt` sha256 | `f43b9f94550938f0894f5f4b74241b281ac49bf6dc0f6f9ff1d3ecda37c98de6` |
| Runner | `tools/runner.py` at the corpus commit, unmodified |
| Results written | 2026-11-07 06:19 UTC (file mtimes); results commit `c2d0945` |
| Re-confirmed | 2026-11-07 ~06:35 UTC: all five interpreters re-run with the same commands; every per-case record (status, checks, return code; durations excluded) is identical to the stored JSON |

## 2. Interpreters

| Label in JSON | Interpreter | Version / provenance | Binary sha256 |
|---|---|---|---|
| `pyawk enhancements d0bdc4b` | pyawk (Python) | `pyawk 1.1.0`, git `d0bdc4bb82654f66572169403a7affb15ad66e62` (branch `enhancements`, clean tree), run from source via `PYTHONPATH=/workspace/pyawk` | n/a (source) |
| `hawk v1.2` | hawk (Rust) | `hawk 1.2.0`, tag `v1.2` = git `d24f8d1f1496c8808463a539849e61c2dcb21e36` (clean tree), `cargo build --release`, rustc 1.99.1 (58cf8f9c3 2026-10-13) | `5ae1ef52df68eb0ec8acdb377d448eab0b3fcfe15ceb48edc0b6b59d6f18c08e` |
| `mawk` | mawk | `mawk 1.3.4 20250131`, Debian package `1.3.4.20250131-1`, `/usr/bin/mawk` | `eff9f2b711eb5bee1b58d4d33b891e8da8f6534655d3854a45bd10217dbb28e6` |
| `onetrue` | One True AWK (BWK) | `awk version 20260426`, git `5739fd79bcfc75ba7526773d0cf634521f8aca3c` of https://github.com/onetrueawk/awk, built locally (`a.out`) | `c78f21f10cc0717136ffd99d0d9cf2051a606824daff48be454cc816af97f890` |
| `gawk --posix` | GNU awk | `GNU Awk 5.4.1, API 4.1, PMA Avon 8-g1`, built from the gawk-5.4.1 release tarball into `/workspace/refs/local` | `99f5d20ef36b9f32af2353beb9d2b020940d4ab77b2a6d2f14b81366a242d593` |

## 3. Exact commands

Run from the repository root (`/workspace/awk-posix-challenge`). `runner.py` itself sets `LC_ALL` and `LANG` to each
case's `locale` field (`C` for all 250 cases), runs each case in its own subprocess with the case folder as the
working directory, passes `-f <case>/program.awk`, feeds `stdin.txt`, and compares stdout, stderr and exit code exactly.

```sh
PYTHONPATH=/workspace/pyawk python3 tools/runner.py --cmd 'python3 -m pyawk' \
    --label 'pyawk enhancements d0bdc4b' --output results/2026-11-07/pyawk.json
python3 tools/runner.py --cmd '/workspace/hawk/target/release/hawk' \
    --label 'hawk v1.2' --output results/2026-11-07/hawk.json
python3 tools/runner.py --cmd 'mawk' --label 'mawk' --output results/2026-11-07/mawk.json
python3 tools/runner.py --cmd '/workspace/refs/onetrue-awk/a.out' \
    --label 'onetrue' --output results/2026-11-07/onetrue.json
python3 tools/runner.py --cmd '/workspace/refs/local/bin/gawk --posix' \
    --label 'gawk --posix' --output results/2026-11-07/gawk.json
```

Timeout: the runner default, 5 seconds per case (`--timeout` not given). No `--ids` filter (all 250 cases).

## 4. Platform

| Item | Value |
|---|---|
| OS | Debian GNU/Linux 13 (trixie), x86_64 |
| Kernel | Linux 6.12.113+ #1 SMP PREEMPT_DYNAMIC (2026-11-05 build) |
| C library | GNU libc 2.41 (Debian 2.41-12+deb13u4) |
| Python (runner and pyawk) | 3.13.5 (`/usr/bin/python3`) |
| Locales installed | `C`, `C.utf8`, `POSIX` |
| Locale used | `LC_ALL=C`, `LANG=C` (set per case by the runner from `case.json`) |

## 5. Results

| Label | Passed | Failed | Failing cases | Result file | sha256 of result file |
|---|---:|---:|---|---|---|
| pyawk enhancements d0bdc4b | 250 | 0 | none | `pyawk.json` | `78d5a461745a41d59a502815ea5a327e354aadbbbc7435836fdd393d0ddcdabd` |
| hawk v1.2 | 250 | 0 | none | `hawk.json` | `da7e138658d899c4b6b1d78c3c83cc59df6208a19d65d9cf8852d6ff16c1ecb2` |
| mawk | 250 | 0 | none | `mawk.json` | `8a7c5a8901c094b713ee6b7a8c95724315a8cecdcadc79f9cdfd692fa67857ea` |
| onetrue | 250 | 0 | none | `onetrue.json` | `027e2c574239b604918f8521623fc1b8e9597b15ff02ad5996b14a69b943d9ee` |
| gawk --posix | 249 | 1 | AWK-105 (stdout `1:abc:` vs expected `3:a:c`) | `gawk.json` | `f0b9a767326d63257b1dcecb99bb5c467e7fae0a61f0610a40302068783b78aa` |

The JSON files include `duration_seconds` per case, so a re-run produces a file with a different hash even when every
result is the same. To compare a re-run, compare the records with `duration_seconds` removed:

```sh
for n in pyawk hawk mawk onetrue gawk; do
  python3 - results/2026-11-07/$n.json /tmp/rerun-$n.json <<'PY'
import json, sys
strip = lambda d: [{k: v for k, v in r.items() if k != 'duration_seconds'} for r in d['results']]
a, b = (json.load(open(p)) for p in sys.argv[1:3])
print(sys.argv[1], 'identical' if strip(a) == strip(b) and a['command'] == b['command'] else 'DIFFERENT')
PY
done
```

## 6. Supplementary observations (not part of the baseline)

`probes/variant_probe.py` re-runs every case under extra interpreter modes and locales (gawk without `--posix`,
gawk `--traditional`, BusyBox awk 1.35.0, and `LC_ALL=C.UTF-8` for the five baseline interpreters). It does not use
`runner.py` and its results are observational; see `RESPONSE-v0.3-review.md`, section 3, and
`probes/variant_probe_summary.txt`. The BusyBox binary used was the official static build
`https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox`, sha256
`6e123e7f3202a8c1e9b1f94d8941580a25135382b99e8d3e34fb858bba311348`.

## 7. Known limitations of this baseline

- One machine, one locale (`C`). No run under a non-C locale is part of the baseline.
- pyawk was run from a source checkout, not an installed package.
- The reference interpreters are themselves tested, not trusted oracles; the oracle is the frozen expected output.
