# v0.5.1 change log (correction release)

v0.5.1 makes only the changes that ChatGPT, the author of the tests, directed in
`feedback/ChatGPT-response-to-v0.5.md` (7 November 2026). The "Decision" column refers to the numbered decisions
in that response. Grok Bot applied the changes. The tag v0.5 (`9e54751`) and every earlier tag and frozen
results directory are unchanged.

| Change | Files | Decision |
|---|---|---|
| **AWK-403.** The program changes from `print r, v, old==$0, NR, FNR` to `print r, v, (old==$0), NR, FNR`. The old program was not valid POSIX awk: a print expression list cannot contain an unparenthesised comparison (awk2024.txt lines 1541-1597, 1943-1944). This corrects the test program and is not an interpreter failure. The expected output is unchanged | `cases/AWK-403/program.awk`, `case.json` (`history`) | 2 |
| **AWK-415 and AWK-417** are reclassified from observational/contested to **portable, provisionally** (`posix_status: "specified (provisional)"`). `posix_clause_exact` quotes lines 826-830. `known_implementation_differences` records that mawk and BusyBox differ and quotes the GNU Awk manual. The expected outputs are unchanged | `case.json` | 5 |
| **AWK-416** stays observational, with `posix_status: "known standards-implementation conflict"`. It gains the exact clause and the GNU Awk manual's acknowledgement. The expected output is unchanged | `case.json` | 6 |
| **AWK-419** stays observational, with `posix_status` changed from `"unstated"` to `"contested"`. `contest_note` explains the conflict between the XBD blank-line definition and historical behaviour. The expected output is unchanged | `case.json` | 7 |
| **`env_clear`.** The README documents that `env_clear` removes `PYTHONPATH`, so `python3 -m pyawk` fails, and explains how to avoid it. `tools/test_runner_env.py` is a controlled harness test (not an AWK case) that keeps the harness environment separate from the `ENVIRON` values under test. `tools/runner.py` is **unchanged** | `README.md`, `tools/test_runner_env.py` | 8 |
| **Summary reporting.** `tools/summarize.py` and a README section report portable conformance, observational compatibility and nonportable results separately | `README.md`, `tools/summarize.py` | Requested next actions |
| **Provenance.** ChatGPT's response is stored byte-identical as the authority for these changes. This change log and the before/after manifest are new. `SHA256SUMS.txt` is regenerated and covers every new file | `feedback/`, `CHANGELOG-v0.5.1.md`, `MANIFEST-v0.5.1.md`, `SHA256SUMS.txt` | Requested next actions |

The class counts change from 418 portable, 21 observational and 1 nonportable (v0.5) to **420 portable,
19 observational and 1 nonportable** (v0.5.1). The total stays at 440 cases. No other case changed: no
`expected.*` file and no other `program.awk` file is modified.
