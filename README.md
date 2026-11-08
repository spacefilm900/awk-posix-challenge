# Independent POSIX AWK Challenge v0.6 — final proposed freeze

**528 total cases:** 440 inherited from the v0.5 corpus with minimal v0.5.1 corrections reconstructed from Grok’s report, plus 75 reviewed implementation-side proposals and 13 independently authored scenarios. **This is an independent challenge artifact, not an official POSIX certification.**

**Important provenance:** This working release is based on the v0.5 ZIP available to ChatGPT, not on a byte-for-byte export of Grok’s tagged v0.5.1 tree. Reconstructed v0.5.1 edits: AWK-403 parentheses and AWK-415/416/417/419 metadata. It does NOT claim to reproduce every v0.5.1 ancillary tool or document. Grok must compare these files with tagged v0.5.1 and flag any discrepancy before adopting v0.6. The actual v0.5.1 frozen upstream tag remains authoritative.

**Execution:** `python3 tools/runner.py --cmd mawk --output results.json`. The runner checks each test in a fresh working directory. `--gate-classifications` defaults to `portable`, but the JSON still reports every disagreement. To fail the process for observational cases too, supply `--gate-classifications portable observational nonportable`. Optional `--ids AWK-...` selects cases. Test AWK-471 uses `no_program_file` to support `-f -`. Test AWK-528 sets `env_clear=true`. Runner’s isolated environment retains PATH, HOME and TMPDIR, so `python -m pyawk` requires an explicitly provided PYTHONPATH or an installed launcher.

**Classification discipline:** Observational outputs represent explicitly labelled hypotheses or compatibility observations; they are not conformance oracles, and discrepancies must never automatically trigger interpreter changes. Tests AWK-475/476 cite Austin Group 1198 and are observational. AWK-470 and AWK-482 are likewise observational. UTF-8 tests under `C.UTF-8` are observational until locale/reference evidence is adjudicated (AWK-483, 489). AWK-415/417 remain provisionally specified portable despite known mawk disagreement; AWK-416 and 419 remain observational. No expected output was changed to force a reference implementation pass.

## Full technical documentation

See `FINAL_HANDOVER_TO_GROK.md`, `V06_CASE_AUDIT.md`, `V06_REQUIREMENTS_MATRIX.md`, `VALIDATION-v0.6.md`, and `CHANGELOG-v0.6.md`. SHA256SUMS.txt lists all release files except itself.

## Previous README (v0.5)

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

## Caveats

- For the first two new FILENAME cases, the expected stdout is `[-]`; older pyawk/hawk builds reportedly print `[]`. Preserve this first-run discrepancy before fixing the interpreters.
- `RS=""` newline splitting with non-space FS (AWK-415–417) has expectations derived from a literal reading of the 2024 specification, but mawk and nawk disagree; these three are intentionally classified observational/contested pending adjudication, not declared POSIX violations. The whitespace-only separator case is also observational.
- The 390 older results in Grok's v0.4 report are not validation results for this modified v0.5 corpus.
- Run against at least gawk --posix, mawk, onetrue-awk and both candidate implementations before accepting the release.

## Local v0.5 validation results

See `results/local-v0.5/VALIDATION.md` and accompanying JSON. System mawk and nawk: 437/440, with all three disagreements in observational cases AWK-415–417. Both passed every one of 418 portable cases. Original pyawk: AWK-391 and AWK-392 reproduce the frozen stdin FILENAME defect; eight other sampled tests passed. Hawk has not been run here.
