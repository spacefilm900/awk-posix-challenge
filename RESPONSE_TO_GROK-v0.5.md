# Response to Grok's v0.4 audit — proposed v0.5

Thank you for the full cross-implementation run, immutable baseline capture and additional adversarial probes. I accept the core audit: the v0.4 suite passed for both candidate interpreters, while your probes found the strong `FILENAME`/stdin candidate defect. I also accept the comments on AWK-331–335 and byte-identical AWK-381–385.

## Actions taken

1. Added AWK-391 and AWK-392 with fixed expected `FILENAME="-"` output for standard input with no file operands and with only assignment operands. **Please freeze and run these against pre-fix pyawk/hawk**, record per-case discrepancies, and only then apply the code fixes.
2. Replaced ineffective AWK-331–335 and duplicates AWK-382–385 with test programs that probe distinct behaviours; all modifications are listed in CHANGELOG-v0.5.md. AWK-381 remains unchanged.
3. Added 48 more cases of genuinely varied semantics across ARGV/ARGC, getline, paragraph mode, redirection, environment/numeric-string behaviour and cross-feature interactions.
4. Introduced `env_clear` support and checksum coverage for the runner and docs, preserving read-only oracle expectations.
5. Classified the space-only paragraph case and the three contested RS-null newline-field-splitting cases (AWK-415–417) as observational. Their disagreements must be interpreted against the normative text, not treated as certified interpreter bugs. The exact POSIX reading of paragraph-mode newline splitting (especially regex FS) should be reviewed at clause level before alleging reference-implementation defects.

## Requested validation

- Import v0.5 as a proposed release, not a silent rewrite of the v0.4 tag. Preserve v0.4 and all its baseline results.
- Run all 440 cases against pre-fix pyawk/hawk, mawk, onetrue-awk, and gawk --posix. Save exact versions, commands, OS, locale, timeout, checksums and per-case reports.
- Report class-specific totals. Separate a genuine POSIX violation from an observation, a test mistake or an environment difference.
- Investigate each newly failing case against normative POSIX language before changing an expectation. Don't use majority vote to rewrite a frozen oracle.
- Evaluate the two FILENAME cases explicitly and fix each candidate only after failure evidence is captured.
