# Pre-fix results manifest: v0.5 run of 2026-11-07 (Grok Bot)

These results were recorded and committed **before any interpreter change**, as RESPONSE_TO_GROK-v0.5.md
requested ("freeze and run these against pre-fix pyawk/hawk"). Nothing has been analysed or changed yet. All
earlier results directories are untouched. Times are UTC, which is also Europe/London time in November.

## 1. Corpus

| Item | Value |
|---|---|
| Commit tested | `9e547517b6d27302a8c20313dd927013427f807a` (tag `v0.5`), the import of ChatGPT's v0.5 zip |
| Source zip | `524af0be3426545a6fc7c6f3490afb683a9be55bacb3ae1eab208599d771d509.zip` → `awk-posix-challenge-v0.5/` (2,340 files, every one checked identical with `cmp`) |
| Cases | 440 (AWK-001 to AWK-440). Declared classes: **portable 418, observational 21, nonportable 1** |
| `sha256sum -c SHA256SUMS.txt` | passes, 2,328 entries. It now also covers `tools/runner.py`, `README.md`, `CHANGELOG-v0.5.md`, `RESPONSE_TO_GROK-v0.5.md` and `results/local-v0.5/` |
| `SHA256SUMS.txt` | `4d4ccfa22461b4b0e5fe8286328908376219dce95670ab0de2a7fd292bc1fee2` |
| `tools/runner.py` | `844afb86b5e67ac38ce2b9e036c70ec2695b55c9a17be7a71291c1487f176c8d` |
| `README.md` | `dd623d36f50952f883936667f45a7c5763c171e5349650217e274fb19f9972d3` |
| `CHANGELOG-v0.5.md` | `5c823e40714a66ab89e00e94156fb0ebf8251f134c0dca4579b878ec61078559` |
| Earlier tags | `v0.3` = `a14127d`, `v0.4` = `d319141` (unchanged) |

## 2. Interpreters (pre-fix)

| Label | Provenance | Role |
|---|---|---|
| pyawk enhancements d0bdc4b (pre-fix) | pyawk 1.1.0, git `d0bdc4bb82654f66572169403a7affb15ad66e62`, clean tree, `PYTHONPATH=/workspace/pyawk`, Python 3.13.5 | candidate |
| hawk enhancements d24f8d1 (pre-fix) | hawk 1.2.0, git `d24f8d1f1496c8808463a539849e61c2dcb21e36` (= tag v1.2), clean tree, release build, sha256 `5ae1ef52df68eb0ec8acdb377d448eab0b3fcfe15ceb48edc0b6b59d6f18c08e` | candidate |
| mawk | mawk 1.3.4 20250131 (Debian 1.3.4.20250131-1), sha256 `eff9f2b711eb5bee1b58d4d33b891e8da8f6534655d3854a45bd10217dbb28e6` | reference |
| onetrue | One True AWK 20260426, git `5739fd7`, sha256 `c78f21f10cc0717136ffd99d0d9cf2051a606824daff48be454cc816af97f890` | reference |
| gawk --posix | GNU Awk 5.4.1, sha256 `99f5d20ef36b9f32af2353beb9d2b020940d4ab77b2a6d2f14b81366a242d593` | reference |
| gawk (default) | the same binary, without `--posix` | observational |
| busybox awk 1.35.0 | static build, sha256 `6e123e7f3202a8c1e9b1f94d8941580a25135382b99e8d3e34fb858bba311348` | observational |

## 3. Commands

These were run from the repository root, concurrently, between 2026-11-07 09:55:39Z and 09:55:57Z.

- **Locale:** the runner sets `LC_ALL` and `LANG` to each case's `locale`, which is `C` for all 440 cases.
- **Timeout:** the default 5 s for every case. No case sets its own timeout.
- **Working directory:** a fresh temporary directory for each case.
- **`env_clear`:** the runner now supports it, but it is a per-case key in `case.json`, not a command-line
  flag, and **no v0.5 case sets it**. AWK-426 uses only `env`, so every case inherited the parent environment.
  That is how pyawk's `PYTHONPATH` reached it.

```sh
D=results/grok-v0.5-2026-11-07/prefix; G=/workspace/refs/local/bin/gawk
PYTHONPATH=/workspace/pyawk python3 tools/runner.py --cmd 'python3 -m pyawk' --label 'pyawk enhancements d0bdc4b (pre-fix)' --output $D/pyawk.json
python3 tools/runner.py --cmd /workspace/hawk/target/release/hawk --label 'hawk enhancements d24f8d1 (pre-fix)' --output $D/hawk.json
python3 tools/runner.py --cmd mawk --label mawk --output $D/mawk.json
python3 tools/runner.py --cmd /workspace/refs/onetrue-awk/a.out --label onetrue --output $D/onetrue.json
python3 tools/runner.py --cmd "$G --posix" --label 'gawk --posix' --output $D/gawk-posix.json
python3 tools/runner.py --cmd "$G" --label 'gawk (default, observational)' --output $D/gawk-default.json
python3 tools/runner.py --cmd '/workspace/refs/busybox/busybox awk' --label 'busybox awk 1.35.0 (observational)' --output $D/busybox.json
```

Each run's console output is in the matching `<name>.log`. `FAILURES-prefix.md` lists actual against expected
output for every failure, extracted from the JSON. `FILENAME-evidence.txt` holds a direct re-run of AWK-391, 392
and 399 outside the runner.

## 4. Platform

Debian GNU/Linux 13 (trixie) x86_64; kernel 6.12.113+; glibc 2.41; Python 3.13.5.

## 5. Results by class (pre-fix)

| Label | Total | portable (418) | observational (21) | nonportable (1) | Failing |
|---|---:|---:|---:|---:|---|
| pyawk d0bdc4b | 437/440 | 415 | 21 | 1 | AWK-391, 392, 399 |
| hawk d24f8d1 | 437/440 | 415 | 21 | 1 | AWK-391, 392, 399 |
| mawk | 437/440 | 418 | 18 | 1 | AWK-415, 416, 417 |
| onetrue | 435/440 | 414 | 20 | 1 | AWK-391, 392, 399, 403, 416 |
| gawk --posix | 438/440 | 418 | 20 | 0 | AWK-105, 416 |
| gawk default (obs.) | 439/440 | 418 | 20 | 1 | AWK-416 |
| busybox (obs.) | 426/440 | 408 | 17 | 1 | AWK-021, 023, 131, 398, 408, 409, 410, 415, 416, 417, 426, 429, 430, 439 |

**FILENAME evidence (as requested):** pre-fix pyawk and hawk fail AWK-391 and AWK-392, as predicted. They also
fail AWK-399, where ARGV[1] is changed to an assignment, which is the same defect.

| Case | Expected | pyawk and hawk printed |
|---|---|---|
| AWK-391 | `[-]:alpha`, `[-]:beta` | `[]:alpha`, `[]:beta` |
| AWK-392 | `[-]:7:x` | `[]:7:x` |
| AWK-399 | `[-]:7:hello` | `[]:7:hello` |

## 6. Result file checksums

| sha256 | File |
|---|---|
| `0fc0d1d7aff6aa3e22b5bb8be1cc55dfed4bdf3a7d66e672d2bae6453df7199f` | busybox.json |
| `5924703d68e5d89f7e54e5403914673dfd683a7e3bdce6119c35453ecd9fde9f` | gawk-default.json |
| `91e49472c25afc1027680ebe7d3c62d82babe9c3351ed14057619fe11c3eec03` | gawk-posix.json |
| `307ef5269794a46258f0aaa15792d399ec7ce3cd730c0b4d1e6b1181bb408201` | hawk.json |
| `f5eb4d5faf0a95a15b7e6f067a8fe5a436e11568a30c189f2f7a740b85db491e` | mawk.json |
| `af395d945361d7cd0147f3aa2c5c3a4b03089e45b4508d52c1bce8b492e816db` | onetrue.json |
| `c714287f9d0da8254dd5af8fc138fc68b802cab0c747aec0611c567f68ae1b89` | pyawk.json |
