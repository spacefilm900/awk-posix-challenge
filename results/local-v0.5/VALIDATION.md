# v0.5 validation, 7 November 2026

Commands ran using `tools/runner.py`, C locale, five-second case timeout.

| Interpreter | Pass | Fail | Explanation |
|---|---:|---:|---|
| mawk | 437 | 3 | AWK-415, 416, 417; observational disputed paragraph-field splitting |
| nawk (local system alternate) | 437 | 3 | Same three observational discrepancies |
| pyawk (uploaded enhanced baseline; selected tests only) | 8 | 2 | AWK-391, 392: `FILENAME` when stdin is implicit |

Both reference implementations passed **418/418 currently portable** cases, plus the nonportable case and 18 of 21 observational cases. The three remaining observational cases deliberately preserve disputed expectations and are not confirmed POSIX violations.

Python AWK's original version reproduced the shared FILENAME defect: AWK-391 gives `[]:alpha`, `[]:beta` rather than `[-]:alpha`, `[-]:beta`; AWK-392 gives `[]:7:x` rather than `[-]:7:x`. Other eight sampled Python cases passed, including all three disputed paragraph cases. Rust hawk not available in this environment and has not been run.

These are local validation results; see JSON files for each case. `nawk` is the local system alternate and should not be assumed equivalent to Grok's onetrue-awk 20260426.
