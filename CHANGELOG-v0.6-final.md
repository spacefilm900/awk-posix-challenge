# v0.6 final reconciliation change log

These changes make only the housekeeping corrections that ChatGPT, the author of the tests, directed
in its final review of the v0.6 results (8 November 2026, stored unchanged as
`feedback/ChatGPT-final-review-v0.6.pdf`, section 3 and section 5 step 1). Grok Bot applied them with the
owner's approval. **No test program, input, expected output or classification changed.** The frozen
pre-fix results in `results/grok-v0.6-2026-11-08/` and ChatGPT's imported files are unchanged.

| Change | Files |
|---|---|
| Restored the five case.json files that lost v0.5.1 metadata in ChatGPT's reconstruction, byte-for-byte from tag v0.5.1 (`7a0adbf`). v0.6 had added no new fields to them; its short `v051_note` summaries are superseded | `cases/AWK-403,415,416,417,419/case.json` |
| Corrected the stale checksum-coverage note (SHA256SUMS.txt does include RELEASE_MANIFEST.json) | `RELEASE_MANIFEST.json` |
| Merged the v0.5.1 README additions (class reporting, `env_clear`) into the v0.6 README | `README.md` |
| Documented the locale assumptions for the UTF-8 tests (AWK-483, AWK-489) | `README.md` |
| Reran all 528 cases on all seven awks: identical to the frozen results | `results/grok-v0.6-final-2026-11-08/` |
| Stored ChatGPT's final review; regenerated `SHA256SUMS.txt` over every tracked file except itself | `feedback/`, `SHA256SUMS.txt` |

Class counts are unchanged: 475 portable, 52 observational, 1 nonportable (528 cases).
