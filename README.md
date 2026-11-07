# Independent POSIX AWK Challenge v0.5 (proposal)

**440 total cases**: 390 carried from v0.4 (nine prior tests corrected with recorded changes), plus **50 distinct new scenarios (AWK-391–440)**.

The challenge is a standards-oriented comparison corpus, not a certification. In particular, observational/nonportable tests are never to be counted as evidence of POSIX violations. Every expectation is fixed, and any mismatch should be investigated independently before a change is made.

## Changes

See [CHANGELOG-v0.5.md](CHANGELOG-v0.5.md) for the precise list of modified historical test files. The original v0.4 release and its baseline results should be retained separately.

## Usage

```sh
python3 tools/runner.py --cmd mawk --label mawk --output results/mawk.json
python3 tools/runner.py --cmd 'gawk --posix' --label gawk-posix --output results/gawk.json
PYTHONPATH=/path/to/pyawk-enhancements python3 tools/runner.py --cmd 'python3 -m pyawk' --label pyawk --output results/pyawk.json
```

To run new cases only:

```sh
python3 tools/runner.py --cmd mawk --ids $(python3 -c 'print(" ".join("AWK-%03d" % i for i in range(391,441)))')
```

## Verification

```sh
sha256sum -c SHA256SUMS.txt
# On macOS: shasum -a 256 -c SHA256SUMS.txt
```

`SHA256SUMS.txt` checksums the case inputs, metadata and expectations, the runner, the README and the changelog. Runner never writes to cases/. Execution occurs in a fresh temporary working directory.

## Summary reporting by class

*Added in v0.5.1, as directed in feedback/ChatGPT-response-to-v0.5.md ("Requested next actions").*

Always report the three classes separately; never add them into one headline score.

- **Portable conformance** (`portable`). The POSIX text specifies the behaviour. A failure is a *candidate*
  POSIX violation, which still has to be adjudicated against the text.
- **Observational compatibility** (`observational`). The case records common practice, or a contested or
  unstated point. A failure is never evidence of a POSIX violation.
- **Nonportable** (`nonportable`). The behaviour is unspecified or implementation-defined, and the result is
  for information only.

```sh
python3 tools/summarize.py results/*.json              # text
python3 tools/summarize.py --markdown results/*.json   # a Markdown table
```

v0.5.1 has 440 cases: 420 portable, 19 observational and 1 nonportable.

## Environment isolation (`env_clear`)

*Added in v0.5.1, as directed in feedback/ChatGPT-response-to-v0.5.md, decision 8.*

A case may set `"env_clear": true`. The runner then starts the interpreter with only `PATH`, `HOME`, `TMPDIR`,
`LC_ALL`/`LANG` (from the case's `locale`) and the case's own `env` values. It does not pass on the caller's
environment.

**Pitfall: `env_clear` also removes `PYTHONPATH`.** An interpreter started as
`PYTHONPATH=/path/to/pyawk python3 -m pyawk` then fails with "No module named pyawk". That is a harness
failure, not an AWK result. To avoid it, use either an installed executable, or an explicit command
environment that the runner passes through unchanged:

```sh
python3 tools/runner.py --cmd 'env PYTHONPATH=/path/to/pyawk python3 -m pyawk' --label pyawk ...
```

The harness's execution environment is separate from the `ENVIRON` values that cases test. Cases set the
variables they test through their `env` field, and never rely on the caller's environment.
`tools/test_runner_env.py` is a controlled harness test of this behaviour; it is not an AWK case:

```sh
python3 tools/test_runner_env.py                         # needs an installed awk (mawk, gawk or awk)
python3 tools/test_runner_env.py --pyawk-dir /path/to/pyawk   # also demonstrates the PYTHONPATH pitfall
```

## Caveats

- For the first two new FILENAME cases, the expected stdout is `[-]`; older pyawk/hawk builds reportedly print `[]`. Preserve this first-run discrepancy before fixing the interpreters.
- `RS=""` newline splitting with non-space FS (AWK-415–417) has expectations derived from a literal reading of the 2024 specification, but mawk and nawk disagree; these three are intentionally classified observational/contested pending adjudication, not declared POSIX violations. The whitespace-only separator case is also observational.
- The 390 older results in Grok's v0.4 report are not validation results for this modified v0.5 corpus.
- Run against at least gawk --posix, mawk, onetrue-awk and both candidate implementations before accepting the release.

## Local v0.5 validation results

See `results/local-v0.5/VALIDATION.md` and accompanying JSON. System mawk and nawk: 437/440, with all three disagreements in observational cases AWK-415–417. Both passed every one of 418 portable cases. Original pyawk: AWK-391 and AWK-392 reproduce the frozen stdin FILENAME defect; eight other sampled tests passed. Hawk has not been run here.
