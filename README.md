# Independent POSIX AWK Challenge v0.4 (proposed)

A separately maintained, fixed-expectation AWK interpreter comparison corpus.
**390 cases**: 250 carried forward from v0.3 and **140 new cases (AWK-251–AWK-390)**.

## Baseline and release policy

- Programs, stdin, and expected stdout/stderr for AWK-001–AWK-250 are unchanged from v0.3. Metadata-only updates to AWK-105 and the fifteen audited cases are explicitly recorded below.
- The original v0.3 results from 7 November 2026 should remain frozen in the upstream GitHub repository; do not replace them with this release's results.
- This is a **proposed v0.4**, not an upstream release. It has not been reviewed or accepted by the repo maintainers.
- The corpus is a conformance *challenge*, not a POSIX certification. Some cases deliberately describe observational or nonportable behaviour. The new cases are designed from the POSIX AWK interface and prior audit recommendations, but the specification traceability requires further human audit.
- Expectations are fixed text files; the runner never updates them. A disagreement is a candidate defect or candidate oracle mistake, not an automatic basis to rewrite an expectation.

## Results (this evaluation environment)

| Interpreter | Cases passing | Failures | Scope |
| --- | ---: | ---: | --- |
| mawk | 390/390 | 0 | Complete v0.4 corpus |
| nawk (system alternate AWK) | 390/390 | 0 | Complete v0.4 corpus |
| pyawk (uploaded enhancements ZIP) | 32/32 | 0 | Selected new cases only; not a complete run |
| hawk (Rust) | not run | — | Executable/repository not supplied here |

The version and exact provenance of `nawk` in this container are not equivalent to Grok's independently built 2026 `onetrue-awk` binary.

## Changes from v0.3

- AWK-105 `FS=""`: metadata-only correction to `nonportable` / `unspecified`.
- The eight incomplete/non-text input cases (AWK-015, AWK-064, AWK-065, AWK-115–119) are now marked `observational` / `outside-requirements`.
- The seven cases involving assignment to NF or return without a value (AWK-006, AWK-053, AWK-054, AWK-080, AWK-103, AWK-111, AWK-175) are now marked `observational` / `unstated`.
- Original source and expected-output files remain unchanged, including the historical first 50 AWK program files lacking a trailing newline. Their POSIX text-file hygiene should be addressed in a future separate revision, if desired.
- New AWK-251–390: getline, separate input operands, FNR/NR, command-line variable assignments, redirection and reopening, exit/error behaviour, field and record state, type conversion, regex, array and function interactions.
- Runner creates a new temporary working directory for each case, stages fixtures, supports operand arguments and -v/-F options, validates output files, and supports nonzero exit / nonempty diagnostic checks.
- Existing case JSON schemas are compatible with the new runner. No shell expansion or interpolation of case commands is performed by the runner.

## Classification counts

- Portable: **374**
- Observational: **15**
- Nonportable: **1**

These counts represent declared classifications, not independently certified POSIX conformance.

## Run

```sh
python3 tools/runner.py --cmd 'mawk' --label mawk --output results/mawk.json
python3 tools/runner.py --cmd 'awk' --label system-awk --output results/system.json
PYTHONPATH=/path/to/pyawk-enhancements python3 tools/runner.py --cmd 'python3 -m pyawk' --label pyawk --output results/pyawk.json
```

To run only the new cases, list IDs `AWK-251` to `AWK-390`:

```sh
python3 tools/runner.py --cmd mawk --ids $(seq -f 'AWK-%03g' 251 390)
```

On macOS (where `seq -f` may not be available), use Python to construct the ID list or run the entire suite.

## Corpus integrity

`SHA256SUMS.txt` covers every file under `cases/`. Run `sha256sum -c SHA256SUMS.txt` on systems with sha256sum, or use `shasum -a 256 -c SHA256SUMS.txt` on macOS.

## Known constraints / follow-up review

- Several tests are parameterized variations of a scenario; 140 cases is not 140 unique semantic features. Prioritize new *semantic* coverage in the next batch.
- The tests use short input fixtures and modest output sizes, not resource-exhaustion probes.
- Some existing programs lack the final newline required of POSIX text files. Those are unchanged intentionally for historical provenance.
- Do not infer from passing the 390 cases that the interpreter is generally correct.
- POSIX utility URL: https://pubs.opengroup.org/onlinepubs/9799919799/utilities/awk.html
