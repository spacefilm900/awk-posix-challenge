# Final independent challenge release — handover to Grok

**Date: 8 November 2026. Intended status: final proposed freeze after reconciliation.**

## Delivery

This archive comprises 528 test cases, a read-only runner, proposal provenance, an individual-case audit of all 75 implementation-side proposals, a requirements-to-tests coverage matrix, reference validation evidence, and SHA-256 checksums. It builds from the **local v0.5 source archive** plus documented reconstruction of the case changes in upstream v0.5.1. **Do not treat it as a byte-for-byte copy of upstream v0.5.1.**

## Required actions in order

1. Compare all 440 inherited case directories, including AWK-403 and metadata for AWK-415/416/417/419, against upstream tagged v0.5.1. Confirm any differences explicitly. No expected outputs of the earlier 440 were intentionally changed. The official upstream v0.5.1 tag remains the authority for unmodified history.
2. Check `SHA256SUMS.txt` and list all test classifications. Check that `no_program_file` in the runner enables AWK-471 and that `env_clear` is exercised by AWK-528. Use an installed pyawk executable or explicit PYTHONPATH in `--cmd` for the latter.
3. Import the proposal byte-identically, tag the final challenge baseline in the independent repository and **freeze the complete pre-fix pyawk and hawk results (plus reference results) in a committed directory before making any implementation change**. Save interpreter commit IDs, flags, locale, tool versions and return statuses.
4. Evaluate **portable failures first**. Separately report observational differences; do not patch the interpreter to make observational cases agree unless a normative interpretation establishes a requirement. Tests AWK-415 and 417 intentionally retain their provisional POSIX requirements despite mawk/nawk differences. AWK-416 is observational with an explicit known standards/implementation conflict.
5. Investigate any newly discovered portable failure with a minimal reproducer and an exact POSIX.1-2024 clause, then add a regression test on the implementation branch *before* a fix. After repair run the full development suites, CI and the challenge. Freeze post-fix results separately.
6. If there are no new portable failures, do not claim proof of correctness. Freeze the test suite and close the exercise with a documented coverage and limitations statement.

## Standards decisions

- AWK-475/476 (Grok P35/P36): **observational**. Austin Group 1198 explicitly states there is no conformance distinction for the uninitialised-field string-value question. Grok’s v0.6 proposal classification was superseded. Do not create defects from a literal but contested reading.
- AWK-470 (P30), AWK-482 (P42): **observational**. No unambiguous POSIX expected output established across competing readings. The expected artifacts in these cases retain the proposed hypothesis intentionally.
- AWK-483 and 489: **observational** UTF-8 byte/character disagreement in the available references. This is an investigation area, not a reason to force output agreement. The six reported escaped-UTF-8 regex discrepancies involved non-POSIX `\x` escapes and should not be counted as conformance defects.
- AWK-415 and 417: provisionally specified portable by a literal RS paragraph rule, although mawk/nawk disagree. Historical practice is documented; an Austin Group interpretation could settle this permanently.
- AWK-416: observational conflict between POSIX literal rule and documented ERE FS reference behaviour; do not change its expected output just to achieve a passing reference.
- AWK-419: observational whitespace-only blank-line interpretation.

## Independence accounting

The 75 Grok-proposed programs are explicitly identified via `v06_origin` and `v06_proposal_id`. The 13 additional independently authored cases are separately identified. The independent contribution is the selection, conservative classification, interface improvements, extra scenarios, validation, and immutable reference reports; **not** a claim that all 88 new program ideas originated independently.

## Close-out

For a freeze intended to last, retain the archive and its SHA-256 manifest, the upstream tag, initial and repaired results, software versions, and documented unresolved normative questions. No change to a test oracle should be made in place: issue a new version and record exactly why.
