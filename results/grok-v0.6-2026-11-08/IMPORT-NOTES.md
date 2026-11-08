# v0.6 import reconciliation

All archive files are copied byte-identically; prior repository-only files are retained. All 440 inherited programs, inputs, expected outputs and classifications match v0.5.1. Five case.json files differ: AWK-403 loses its correction history; AWK-415/416/417 replace precise references, exact clauses, histories and implementation notes with abbreviated reconstructed notes; AWK-419 loses the exact clause, contest explanation and history in favour of an abbreviated note. The intended semantic correction/classifications are present, but the loss of provenance is reconstruction drift. Conservatively no v0.6 tag is created pending ChatGPT acceptance. No test was edited to reconcile this. Full differences are in reconciliation.diff.

Shared changes: README adopts v0.6 overview and replaces v0.5.1 reporting/isolation/grammar documentation; runner adds no_program_file and portable-only exit gating; SHA256SUMS changes for release content. Other shared files are identical. Files absent from the archive are enumerated separately and retained, not deleted.

All 2812 checksums verify, including RELEASE_MANIFEST.json; only SHA256SUMS.txt is excluded. Its manifest note incorrectly says RELEASE_MANIFEST.json is excluded. Counts agree: 528 = 475 portable + 52 observational + 1 nonportable; 88 new = 55 portable + 33 observational. No test/expectation changes have been made.

Publication is withheld because the owner has not explicitly authorized a push in the supplied conversation. Local commits preserve the requested execution/analysis ordering.
