# v0.6 candidate freeze — changes

- Preserved 440-case v0.5 baseline except reconstructed v0.5.1 case correction AWK-403 and metadata-only AWK-415, 416, 417, 419. No existing expected stdout/stderr was changed.
- Added AWK-441 to AWK-515 from 75 Grok proposals, after independent review and conservative reclassification.
- Added AWK-516 to AWK-528: 13 independent scenarios including one isolated-environment harness test.
- Extended runner to permit `no_program_file` so `-f -` can be tested; defaults to portable-only exit-status gating while still reporting all classes.
- Removed no earlier cases. Expectations remain a frozen hypothesis where observational and are not reverse-engineered from reference AWK outputs.
- Known normative-vs-reference discrepancies are documented; candidate and reference runs are recorded separately.
- This is a reconstruction built from the v0.5 ZIP, not a byte-identical derivative of upstream v0.5.1. Grok must reconcile against upstream v0.5.1 before tagging a shared release.
