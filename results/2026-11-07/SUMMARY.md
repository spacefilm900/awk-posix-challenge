# Run of v0.3 on 2026-11-07

Cases are unchanged from the supplied zip (`sha256sum -c SHA256SUMS.txt` passes). Run with `tools/runner.py`, `LC_ALL=C`, default 5 s timeout.

| Interpreter | Pass | Fail |
|---|---:|---:|
| pyawk (enhancements, d0bdc4b) | 250 | 0 |
| hawk v1.2 (d24f8d1, release build) | 250 | 0 |
| mawk 1.3.4 | 250 | 0 |
| onetrue-awk (BWK awk) | 250 | 0 |
| gawk 5.4.1 `--posix` | 249 | 1 (AWK-105) |

## Feedback for the test author

**AWK-105 (`fs-char-split`) tests unspecified behaviour but is classified `portable`.**
The program sets `FS=""` and expects each character to become a field (`3:a:c`).
POSIX 2024, awk, "Regular Expressions"/field splitting, says: "If FS is a null string, the behavior is unspecified."
gawk in `--posix` mode treats the record as a single field (`1:abc:`); gawk without `--posix`, mawk, onetrue-awk, pyawk and hawk split into characters.
Suggestion: reclassify it as a common extension or move it out of the portable-success set, rather than counting a different result as a POSIX failure.
