# Proposed v0.5 change log

- Preserves AWK-001–330, AWK-336–381 and AWK-386–390 case files exactly as in supplied v0.4.
- Repairs AWK-331–335 to actually observe `$0` before and after field assignment following an `OFS` change. Changes program, input, output, metadata, and checksums.
- Replaces exact-duplicate AWK-382–385 programs with distinct longest-match regex scenarios. Changes program, output, metadata, and checksums.
- Adds AWK-391–440: 50 new cases, including two tests designed to detect the `FILENAME` stdin bug on pyawk/hawk at the frozen v0.4 baseline.
- Adds optional `env_clear` case handling in the runner for future environment-variable tests; its previous default remains unchanged.
- SHA256SUMS now covers `tools/runner.py`, `README.md`, and `CHANGELOG-v0.5.md` as well as cases.
- Fixed expectations are not automatically changed by the runner. New test classifications are provisional pending separate clause-level audit.
- The v0.4 baseline and its archived results must remain preserved at their original tag.
