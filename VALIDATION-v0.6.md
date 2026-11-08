# Independent local validation — v0.6

**Date:** 8 November 2026 (UTC). **Environment:** local container with mawk and nawk. This report is an independent execution record, not an assertion of universal compliance.

**Total:** 528 cases: nonportable 1, observational 52, portable 475.
**New v0.6:** 88 cases: observational 33, portable 55.

| Interpreter | Portable | Observational | Nonportable | Total |
|---|---:|---:|---:|---:|
| mawk | 473/475 | 45/52 | 1/1 | 519/528 |
| nawk | 473/475 | 45/52 | 1/1 | 519/528 |

The two portable disagreements in both references are **AWK-415 and AWK-417**, pre-existing `RS=""` paragraph-mode tests classified provisionally per POSIX.1-2024 literal language and documented GNU AWK historical divergence. **Do not silently rewrite these expectations.** Seven observational disagreements appear in both, involving AWK-416, 470, 475, 476, 482, 483, 489. The latter group is intentionally non-gating.

### Every mismatch (both local reference programs)

| Test | Class | Nature |
|---|---|---|
| AWK-415 | portable | Paragraph-mode newline-as-field with literal FS; known mawk incompatibility |
| AWK-416 | observational | Paragraph-mode newline-as-field with ERE FS; documented standards/practice conflict |
| AWK-417 | portable | Paragraph-mode newline-as-field with single-character FS; known mawk incompatibility |
| AWK-470 | observational | `getline < "-"` pathname vs stdin special case, observational |
| AWK-475 | observational | Empty field compared to zero; Austin Group 1198, observational |
| AWK-476 | observational | Nonexistent field compared to zero; Austin Group 1198, observational |
| AWK-482 | observational | `substr` start 0 outside specified range, observational |
| AWK-483 | observational | UTF-8 string length / `substr` interpreted as bytes by mawk/nawk, observational |
| AWK-489 | observational | UTF-8 regex offsets interpreted as bytes by mawk/nawk, observational |

### Python interpreter spot-check

The older **3 November 2026 pyawk-enhancements.zip** is not the Grok-fixed v0.5.1 code. A 12-case selected run passed 6/12; known earlier `FILENAME` failures at 391/392/399 are expected from that older version. AWK-475/476 are observational unresolved comparison probes; the AWK-528 initial import failure is caused by `env_clear` removing `PYTHONPATH`, not an AWK failure. After explicitly supplying `PYTHONPATH` in the command, AWK-528 passed 1/1. Full Python or Rust v0.6 validation **has not** been completed here; Grok must execute current versions and freeze pre-fix reports.

### Runner integrity

- Fresh temporary working directory for each case.
- Isolated stdout, stderr, exit and optional file comparisons.
- CLI option `--gate-classifications portable` is default, allowing documented observational mismatches to be reported without failing a process.
- `no_program_file` now allows a valid `-f -` test; AWK-471 passed on both references and the older pyawk sample.
- `env_clear` is exercised by AWK-528; the PYTHONPATH caveat is explicit.
- Corpus does not overwrite expected outputs during test runs.

### Known remaining limitations

- This corpus is substantial but not exhaustive. Some scenarios overlap and cannot be treated as independent Bernoulli trials.
- The locale C.UTF-8 can differ across systems, especially multibyte offsets and escaped characters.
- Grammar checks were reported by Grok for upstream v0.5.1 but not independently rerun here for every new program using a strict POSIX grammar parser.
- The reference AWK versions here are narrower than Grok’s seven-implementation matrix; there is no locally installed gawk or onetrue-awk.
- The v0.5.1 baseline was reconstructed from the local v0.5 archive and must be compared with Grok’s upstream tag.
