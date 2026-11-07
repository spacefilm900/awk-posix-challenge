# Independent POSIX AWK Challenge — v0.3

**Status:** 250 independently authored, fixed-oracle cases. First candidate challenge, not a certification suite. Created 2026-11-06.

This corpus was authored from language semantics and POSIX documentation **without consulting either pyawk's existing tests or hawk's test suite**. Expected outcomes were reasoned out separately and checked against the system `awk` as a *sanity check*, not generated from it. The `case.json` and expected output files are fixed: `runner.py` only reads them. A system-awk run is included. Test cases remain unchanged by candidate failures.

## Run

```sh
python3 tools/runner.py --cmd 'awk' --label system-awk --output results-system.json
python3 tools/runner.py --cmd 'python3 -m pyawk' --label pyawk --output results-pyawk.json
python3 tools/runner.py --cmd '/path/to/hawk' --label hawk --output results-hawk.json
```

To use an unpacked pyawk source checkout, run from a directory in which `python3 -m pyawk` works, or set `PYTHONPATH=/path/to/pyawk-source` in the environment.

The runner supplies each `program.awk` through `-f`, passes `stdin.txt`, and compares exact stdout, stderr and process exit code. `LC_ALL=C` controls locale. Each case has a separate subprocess and a default 5-second deadline. The runner stores its reports outside `cases/`; it cannot rewrite or recalculate expected outputs. The test command should be trusted, since it is executed as a local process; use sandboxing before running unknown interpreters. Use `--ids AWK-001 AWK-041` for focused tests.

## Oracle and interpretation

This is a first-stage **portable-success** suite: all original 50 cases expect exit 0 and empty stderr. A future release should add a separately classified negative/error corpus (where POSIX mandates an error but does not fix text), multi-file cases, locale-dependent probes, `getline` file redirection, and property/metamorphic checks. Tests are designed to reveal defects, but **passing 50 does not certify POSIX conformance**.

A case with a mismatch is a *candidate finding*, not automatically a confirmed violation. Investigate POSIX version, specified/unspecified behavior, runtime environment, and the expectations themselves before calling it a defect. Save the initial results before any code changes.

## Source and traceability

Primary standard: The Open Group / IEEE Std 1003.1-2024 `awk` specification, sections named by each `case.json` (`section` field).
- POSIX awk utility description: https://pubs.opengroup.org/onlinepubs/9799919799/utilities/awk.html
- POSIX awk (independently hosted markup): https://manpages.opensuse.org/Tumbleweed/man-pages-posix/awk.1p.en.html
- POSIX ERE syntax: https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap09.html

The section-level annotations are a **starting traceability index**, not precise paragraph-level normative citations. Precise requirement quotations/section anchors should be checked before classifying any mismatch as a standards violation. No claim is made that the suite exhausts the standard.

## Distribution

`cases/AWK-XXX/` has `program.awk`, `stdin.txt`, `expected.stdout`, `expected.stderr`, and `case.json`. All content is independently authored; no corpus from the projects is copied. The system-awk smoke result lives at top level and is observational, not the oracle.

## v0.3 expansion

Adds AWK-051–AWK-100, 50 fixed-oracle cases focused on semantic interactions. AWK-001–AWK-050 are unchanged. `SHA256SUMS.txt` inventories the frozen source and expected outcomes. Candidate run results are stored separately and never alter test expectations.

## Run against the supplied enhanced Python AWK archive

Unzip `pyawk-enhancements.zip` alongside this challenge. From the challenge folder, run:

```sh
PYTHONPATH=/absolute/path/to/pyawk-enhancements python3 tools/runner.py \
  --cmd 'python3 -m pyawk' --label pyawk --timeout 5 \
  --output results-pyawk.json
```

The repository must contain a `pyawk/` package underneath the path given in `PYTHONPATH`. Python dependencies used by the interpreter need to be installed if the source checkout requires them. Run reports are not used to adjust expectations. On constrained environments, use `--ids AWK-051 AWK-052` to run a smaller sample. Process startup can dominate the total runtime; the per-case timeout defaults to five seconds.

**Validation status:** all 100 cases passed system AWK on the author's execution machine. The full 100-case pyawk run must be reported separately and is not represented by system AWK results. The oracle is preliminary and each mismatch requires review against the normative POSIX text.

## Completed v0.3 baseline runs

Both system `awk` and the supplied `pyawk-enhancements` archive passed all 100 fixed cases. The pyawk suite was executed in four batches of 25 to avoid aggregate command-duration limits. The recorded initial results are provided in `system-awk-v0.3-results.json` and `pyawk-v0.3-results.json`. The runner never adjusts expected case output. These results are limited evidence, not POSIX certification.

## v0.3 expansion (2026-11-06)

Adds 150 independently specified success cases, AWK-101 through AWK-250, spread across ten groups of 15 cases. AWK-001 through AWK-100 are unchanged. Expected stdout was written before running reference or candidate interpreters; mismatches must be reviewed, not auto-corrected. `SHA256SUMS.txt` includes every frozen case file. Case metadata links to the POSIX 2024 awk standard by section (not to precise normative paragraphs). Reference behavior is a sanity check and not itself a standards oracle.

This batch emphasizes combined interpreter state, calls and arrays, and boundary behavior. It does not yet cover multi-file invocation, negative/error expectations, locale-dependent behavior or `getline` redirection in depth.

## v0.3 validation status

- All 250 fixed cases pass `/usr/bin/awk` (mawk 1.3.4) in `system-awk-v0.3-results.json`.
- An independently recorded 10-case cross-category sample passes the supplied pyawk-enhancements archive (`pyawk-v0.3-spot-results.json`). This **is not** a full pyawk validation of the 150 new cases.
- The full pyawk candidate run was attempted but exceeded the aggregate execution window before completion; its result must be considered **unknown**, not a pass or fail. Full run locally: `PYTHONPATH=/path/to/pyawk-enhancements python3 tools/runner.py --cmd 'python3 -m pyawk' --label pyawk --timeout 5 --output pyawk-v0.3-full-results.json`.
- The earlier AWK-001–AWK-100 baseline was reported as passing in v0.2 and remains byte-for-byte identical here.
- Expected output and per-case metadata were authored before reference execution. Reference checking identified and led to corrections of several new *test-authoring* mistakes before v0.3 was frozen. This release should be regarded as an independently designed candidate corpus, not a certified standards oracle.
