# Final v0.6 rerun (8 November 2026)

Rerun of all 528 cases on all seven awk configurations after the metadata-only
reconciliation for the v0.6 tag (restored five case.json files, manifest note,
README). Corpus commit: e7f4645. pyawk at b6a3d25,
hawk at cdf59f5 (release build). Same commands as results/grok-v0.6-2026-11-08.

Result: every case has the same PASS/FAIL status as the frozen results in
results/grok-v0.6-2026-11-08 (0 differences in 7 x 528 = 3,696 comparisons).

| awk | Portable (475) | Observational (52) | Nonportable (1) |
|---|---:|---:|---:|
| pyawk | 475 | 48 | 1 |
| hawk | 475 | 48 | 1 |
| gawk --posix | 475 | 45 | 0 |
| gawk | 475 | 47 | 1 |
| mawk | 473 | 45 | 1 |
| onetrue | 472 | 43 | 1 |
| BusyBox | 461 | 43 | 1 |

Runner exit code 1 for mawk, onetrue and BusyBox is expected (portable failures gate).
