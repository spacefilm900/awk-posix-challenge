# v0.5.1 results manifest, 2026-11-07 (Grok Bot)

This is a full run of the v0.5.1 corpus on seven implementations. It is a new directory; no frozen results
directory was changed. Times are UTC, which is also UK time today.

## Corpus

| Item | Value |
|---|---|
| Commit and tag | `7a0adbf07498477312cb9364ce06dc75bb0c84fb` (tag `v0.5.1`) |
| Cases | 440: 420 portable, 19 observational, 1 nonportable |
| `sha256sum -c SHA256SUMS.txt` | passes (2,334 entries) |
| `SHA256SUMS.txt` sha256 | `e23f7e73fc6d4a74b6dd766a60f61574ac074385778c41e9800ba5344a44ec43` |
| `tools/runner.py` sha256 | `844afb86b5e67ac38ce2b9e036c70ec2695b55c9a17be7a71291c1487f176c8d` (unchanged since v0.5) |

## Implementations

| Label | Provenance |
|---|---|
| pyawk enhancements b6a3d25 | pyawk 1.1.0, git `b6a3d257d6fe09ecb15e3e383b5f56c78bb7c5cc`, clean tree, Python 3.13.5, `PYTHONPATH=/workspace/pyawk` |
| hawk enhancements 9f09764 | hawk 1.2.0, git `9f09764a48053a98e0e1953731f8f089859928dd`, clean tree, release build, sha256 `8eaaf2427d2622c11f9b4a568bd4e3e1917cb40012a4e63dd7643fb55fba1a19` |
| mawk | 1.3.4 20250131 (Debian 1.3.4.20250131-1), sha256 `eff9f2b7…28e6` |
| onetrue | One True AWK 20260426 (git `5739fd7`), sha256 `c78f21f1…f890` |
| gawk --posix / gawk (default) | GNU Awk 5.4.1, sha256 `99f5d20e…d593` |
| busybox awk 1.35.0 | static build, sha256 `6e123e7f…1348` |

## Commands

These ran from the repository root, concurrently, from 2026-11-07T14:59:42Z to 2026-11-07T15:00:01Z.
Every case used locale C, set by the runner, and the default 5 s timeout. No case sets `env_clear`.

```sh
D=results/grok-v0.5.1-2026-11-07; G=/workspace/refs/local/bin/gawk
PYTHONPATH=/workspace/pyawk python3 tools/runner.py --cmd 'python3 -m pyawk' --label 'pyawk enhancements b6a3d25' --output $D/pyawk.json
python3 tools/runner.py --cmd /workspace/hawk/target/release/hawk --label 'hawk enhancements 9f09764' --output $D/hawk.json
python3 tools/runner.py --cmd mawk --label mawk --output $D/mawk.json
python3 tools/runner.py --cmd /workspace/refs/onetrue-awk/a.out --label onetrue --output $D/onetrue.json
python3 tools/runner.py --cmd "$G --posix" --label 'gawk --posix' --output $D/gawk-posix.json
python3 tools/runner.py --cmd "$G" --label 'gawk (default)' --output $D/gawk-default.json
python3 tools/runner.py --cmd '/workspace/refs/busybox/busybox awk' --label 'busybox awk 1.35.0' --output $D/busybox.json
python3 tools/summarize.py --markdown $D/*.json
```

**Platform:** Debian GNU/Linux 13 (trixie) x86_64, kernel 6.12.113+, glibc 2.41.

## Results by class

| Implementation | Portable conformance | Observational compatibility | Nonportable (informational) | Failing: portable | Failing: observational | Failing: nonportable |
|---|---:|---:|---:|---|---|---|
| pyawk enhancements b6a3d25 | 420/420 | 19/19 | 1/1 | none | none | none |
| hawk enhancements 9f09764 | 420/420 | 19/19 | 1/1 | none | none | none |
| mawk | 418/420 | 18/19 | 1/1 | 415, 417 | 416 | none |
| onetrue | 417/420 | 18/19 | 1/1 | 391, 392, 399 | 416 | none |
| gawk --posix | 420/420 | 18/19 | 0/1 | none | 416 | 105 |
| gawk (default) | 420/420 | 18/19 | 1/1 | none | 416 | none |
| busybox awk 1.35.0 | 408/420 | 17/19 | 1/1 | 021, 023, 131, 398, 408, 409, 410, 415, 417, 426, 429, 430 | 416, 439 | none |

### What changed since v0.5

- **onetrue** now passes AWK-403, because the program was corrected.
- **mawk:** AWK-415 and AWK-417 are now counted under portable conformance, where they are failures, because
  they were reclassified. mawk's output did not change.
- **BusyBox:** the same applies to AWK-415 and AWK-417.
- **Other cases:** every implementation gives the same result as in `results/grok-v0.5-2026-11-07/`.

## Result file checksums

```
90f1057cd05783f8e80d9f1b12db9539decc252a6b07fbec49b47c5c83165241  busybox.json
396ed73039ec8d2a81f6a38896a77a0b9f5207924ccd8b5ca37fdb4435e9aac5  gawk-default.json
117b99fd9d6456fda2061dabae9a8fa8251adbf4fdcc1374e20c434a20f1b631  gawk-posix.json
7538d58e060c304cd87a83af50aadbfc563c6a2fce45f3bc0c7710a1be6b9554  hawk.json
559bf0ed00fe43cc0e0f1335b436f5609a704389f26f5faa20d94b8b75c42688  mawk.json
1af91a4456104579a50534763255936cd049882da37dd83ae7be6264e0cf8002  onetrue.json
519beebe87aabe3d13a1ca307fe6871b1eda262d1665757c4305b8f8856066fd  pyawk.json
```
