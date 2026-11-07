# Results manifest: v0.4 run of 2026-11-07 (Grok Bot)

These are the first results for the proposed v0.4 corpus. They were recorded and committed before any analysis
or change. pyawk and hawk were not modified. ChatGPT's own results are kept, as supplied, in
`results/local-v0.4/`. Our v0.3 baseline in `results/2026-11-07/` is untouched. Times are UTC, which is also
Europe/London local time in November.

## 1. Corpus

| Item | Value |
|---|---|
| Corpus commit tested | `d319141d961afac3c255487ea7f7ad464c652eb0` (tag `v0.4`): "Import ChatGPT's proposed v0.4 challenge (390 cases), unchanged from the supplied zip" |
| Source | zip `556b2e1c…77d2.zip`, unpacking to `awk-posix-challenge-v0.4/` (2,053 files). Every file was compared with `cmp` after import, and all are identical |
| Cases | 390 (AWK-001 to AWK-390). Declared classes: portable 374, observational 15, nonportable 1 |
| `sha256sum -c SHA256SUMS.txt` | passes (2,039 entries, all under `cases/`) |
| `SHA256SUMS.txt` sha256 | `883a339011d35dd2769f42987b7ad92c6f2626a48e0707ada88c75381a1353dd` |
| `tools/runner.py` sha256 | `7c0df249b5407b900ac92fb0b3c4a694be14d4d4412ce1a3ceb21f68dbe3ce79` (not covered by SHA256SUMS.txt) |
| `README.md` sha256 | `baa37a8a7619118f118c21285a6724ecc1276a07290f77f729038c9c02bf4e7a` |
| Previous release | tag `v0.3` = `a14127d` |

## 2. Interpreters

These are the same builds as in `results/2026-11-07/MANIFEST.md`. The binary hashes were re-checked today.

| Label | Interpreter and provenance | Role |
|---|---|---|
| `pyawk enhancements d0bdc4b` | pyawk 1.1.0, git `d0bdc4bb82654f66572169403a7affb15ad66e62`, clean tree, `PYTHONPATH=/workspace/pyawk`, Python 3.13.5 | candidate |
| `hawk v1.2` | hawk 1.2.0, tag `v1.2` = `d24f8d1f1496c8808463a539849e61c2dcb21e36`, clean tree, release build (rustc 1.99.1), sha256 `5ae1ef52df68eb0ec8acdb377d448eab0b3fcfe15ceb48edc0b6b59d6f18c08e` | candidate |
| `mawk` | mawk 1.3.4 20250131 (Debian `1.3.4.20250131-1`), `/usr/bin/mawk`, sha256 `eff9f2b7…28e6` | reference |
| `onetrue` | One True AWK 20260426, git `5739fd79bcfc75ba7526773d0cf634521f8aca3c`, sha256 `c78f21f1…f890` | reference |
| `gawk --posix` | GNU Awk 5.4.1 (built from the release tarball), sha256 `99f5d20e…a242d593` | reference |
| `gawk (default, observational)` | the same gawk binary, without `--posix` | observational |
| `busybox awk 1.35.0 (observational)` | official static musl build, sha256 `6e123e7f…1348` | observational |

## 3. Commands

Run from the repository root. The runner sets `LC_ALL` and `LANG` from each case's `locale` (C for all 390). It
creates a fresh temporary directory per case, stages the fixtures, and uses the default 5 s timeout (no
per-case `timeout` is set).

```sh
D=results/grok-v0.4-2026-11-07; G=/workspace/refs/local/bin/gawk
PYTHONPATH=/workspace/pyawk python3 tools/runner.py --cmd 'python3 -m pyawk' --label 'pyawk enhancements d0bdc4b' --output $D/pyawk.json
python3 tools/runner.py --cmd '/workspace/hawk/target/release/hawk' --label 'hawk v1.2' --output $D/hawk.json
python3 tools/runner.py --cmd 'mawk' --label 'mawk' --output $D/mawk.json
python3 tools/runner.py --cmd '/workspace/refs/onetrue-awk/a.out' --label 'onetrue' --output $D/onetrue.json
python3 tools/runner.py --cmd "$G --posix" --label 'gawk --posix' --output $D/gawk-posix.json
python3 tools/runner.py --cmd "$G" --label 'gawk (default, observational)' --output $D/gawk-default.json
python3 tools/runner.py --cmd '/workspace/refs/busybox/busybox awk' --label 'busybox awk 1.35.0 (observational)' --output $D/busybox.json
```

The seven runs were started concurrently at about 08:45 UTC. A sequential re-run a few minutes later gave
identical per-case records (status, checks and return code; durations excluded) for all seven.

## 4. Platform

Debian GNU/Linux 13 (trixie) x86_64; kernel 6.12.113+; glibc 2.41; Python 3.13.5; locales `C`, `C.utf8`, `POSIX`.

## 5. Results

| Label | Total | portable (374) | observational (15) | nonportable (1) | Failing |
|---|---:|---:|---:|---:|---|
| pyawk enhancements d0bdc4b | 390/390 | 374 | 15 | 1 | none |
| hawk v1.2 | 390/390 | 374 | 15 | 1 | none |
| mawk | 390/390 | 374 | 15 | 1 | none |
| onetrue | 390/390 | 374 | 15 | 1 | none |
| gawk --posix | 389/390 | 374 | 15 | 0 | AWK-105 (nonportable) |
| gawk default (obs.) | 390/390 | 374 | 15 | 1 | none |
| busybox 1.35.0 (obs.) | 387/390 | 371 | 15 | 1 | AWK-021, AWK-023, AWK-131 |

## 6. Result file checksums

| File | sha256 |
|---|---|
| `6e62a1a1278474b815eb588bb8cd7b8b9cf2cd64fc95212a709728783c368193` | `busybox.json` |
| `c980f5ad65ab12d78bc22361ffedb1e0620bede1c559b3793c11a7ac965fd895` | `gawk-default.json` |
| `f86a421a3a71352f7f08457952b6461d78800f90edad1953a184aff58906d716` | `gawk-posix.json` |
| `42e31a9bd537ab2e9787a5247f634ee866498565d03fb4cdea0d6e1101509433` | `hawk.json` |
| `8470b96924ec1dc1410c237cba78ef1295fc93392599cb486beb4cd4cc9b44c1` | `mawk.json` |
| `6f31a970387d8d2c1fa77625d530d8a0b361528cfa706069b813cb78958a48c4` | `onetrue.json` |
| `d8e4745403bac0bdf42bd704b2a272b88dc9580e2ec6d5001f966a59b7326be4` | `pyawk.json` |
