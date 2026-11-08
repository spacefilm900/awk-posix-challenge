# v0.6 case audit

Each proposal scenario was examined against the supplied rationale. `portable` denotes a specific expected outcome; observational outputs are diagnostic hypotheses, not correctness gates. The references shown are from Grok’s proposal and have not all been independently fetched from the full POSIX text.

| Proposal | New test | Case | Classification | Decision / standards caveat |
|---|---|---|---|---|
| P01 | AWK-441 | -v value with \t escape | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P02 | AWK-442 | -v value ending in an unescaped backslash | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P03 | AWK-443 | -v value with \\ (double backslash) | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P04 | AWK-444 | -v value with octal escapes | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P05 | AWK-445 | -v numeric string with leading zeros | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P06 | AWK-446 | -v numeric string with leading and trailing blanks | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P07 | AWK-447 | -v value that only looks numeric (1e) | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P08 | AWK-448 | Assignment operand with \t escape | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P09 | AWK-449 | Timing of assignment operands around BEGIN and END | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P10 | AWK-450 | -F '\t' is escape-processed like -v FS= | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P11 | AWK-451 | -F t means the letter t, not tab | observational | Historical One True AWK `-Ft` exception; classify observational pending mode interpretation. |
| P12 | AWK-452 | -F with a single ERE metacharacter '/' is literal | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P13 | AWK-453 | -F with a multi-character ERE | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P14 | AWK-454 | -F ' ' is the default field splitting | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P15 | AWK-455 | -F '\\.' becomes the ERE \. (a literal dot) | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P16 | AWK-456 | %c with a numeric argument | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P17 | AWK-457 | %c with a string constant that looks numeric | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P18 | AWK-458 | %c with a number and a concatenated string | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P19 | AWK-459 | %c with a numeric-string field | observational | Numeric-string argument type for `%c` remains unsettled. |
| P20 | AWK-460 | %c with width and the - flag | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P21 | AWK-461 | system() returns the command's exit status | observational | `system()` exit statuses are implementation-sensitive; check exact POSIX exit-status wording and environment. |
| P22 | AWK-462 | Output order around system() | observational | Observational: Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P23 | AWK-463 | close() of a stream that was never opened is non-zero | observational | `close` unknown stream status; monitor compatibility. |
| P24 | AWK-464 | close() twice: 0 the first time, then non-zero | observational | Repeated close success/failure; monitor compatibility. |
| P25 | AWK-465 | close() of an input pipe whose command succeeded | observational | Pipe close exit status and command wait semantics; monitor. |
| P26 | AWK-466 | close() of an output pipe whose command exits 3 | observational | Observational: Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P27 | AWK-467 | Reading a file again after close() starts at the beginning | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P28 | AWK-468 | '>' after close() truncates again | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P29 | AWK-469 | getline from a missing file returns -1 and leaves NR alone | observational | Error diagnostics are not text-standardised; ignore stderr. |
| P30 | AWK-470 | getline < "-" when a file named "-" exists | observational | Literal pathname `-` versus special stdin handling; do not use for gating. |
| P31 | AWK-471 | -f - reads the program from standard input | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P32 | AWK-472 | ARGV element set to "-" at run time reads stdin | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P33 | AWK-473 | An uninitialised scalar is both 0 and "" | observational | Observational: Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P34 | AWK-474 | Comparisons involving an uninitialised value | observational | Observational: Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P35 | AWK-475 | An empty field is uninitialised | observational | Austin Group 1198: no conformance distinction for uninitialised-field string value. |
| P36 | AWK-476 | Referencing a field past NF does not create it | observational | Austin Group 1198: no conformance distinction for nonexistent field comparison. |
| P37 | AWK-477 | 'in' does not create an element; a reference does | observational | Observational: Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P38 | AWK-478 | Missing function arguments are uninitialised | observational | Observational: Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P39 | AWK-479 | An uninitialised global passed to a function becomes an array | observational | Passing previously untyped variable as array; observational. |
| P40 | AWK-480 | substr bounds: omitted n, n too large, start past the end | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P41 | AWK-481 | substr with n <= 0 is empty | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P42 | AWK-482 | substr with m = 0 | observational | `substr` start below 1 unspecified; observational. |
| P43 | AWK-483 | substr and length count characters in UTF-8 | observational | Multibyte C.UTF-8 support differs across references; observational. |
| P44 | AWK-484 | index with an empty needle | observational | Empty needle convention for index unresolved. |
| P45 | AWK-485 | index basic cases, including an empty haystack | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P46 | AWK-486 | match of an ERE that matches empty | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P47 | AWK-487 | match of /$/ is at the end of the string | observational | Empty match at string end; provisional, reference consensus is supporting evidence only. |
| P48 | AWK-488 | A failed match resets RSTART and RLENGTH | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P49 | AWK-489 | RSTART and RLENGTH count characters in UTF-8 | observational | Multibyte regex offsets are locale-sensitive; observational. |
| P50 | AWK-490 | Leftmost beats longer; then longest at the same start | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P51 | AWK-491 | Other functions do not set RSTART or RLENGTH | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P52 | AWK-492 | split with fs " " uses default field splitting | observational | split fs literal space vs FS special rule: caution/provisional. |
| P53 | AWK-493 | split with a single-character fs "." is literal | observational | split fs single character vs ERE: caution/provisional. |
| P54 | AWK-494 | split deletes every old element first | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P55 | AWK-495 | split("", A) empties the array | observational | Observational: Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P56 | AWK-496 | split elements are numeric strings | observational | Observational: Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P57 | AWK-497 | The source string is an element of the target array | observational | Observational: Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P58 | AWK-498 | An ERE fs with leading and trailing separators | observational | Leading/trailing empty split elements: monitor. |
| P59 | AWK-499 | delete A, then reuse A | observational | Whole-array delete: POSIX.1-2024, confirm historical support. |
| P60 | AWK-500 | delete a on an array parameter clears the caller's array | observational | Delete array through parameter: possible historical variation. |
| P61 | AWK-501 | delete A[k] inside for (k in A) | observational | Observational: Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P62 | AWK-502 | exit with no expression in END keeps the earlier status | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P63 | AWK-503 | exit in BEGIN runs END and reads no input | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P64 | AWK-504 | exit inside END stops the remaining END actions | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P65 | AWK-505 | getline var < file leaves NR, FNR, NF and $0 alone | portable | Redirected getline must not alter main input counters; test valid. |
| P66 | AWK-506 | Plain getline updates NR, FNR, NF and $0 | portable | Plain getline changes record state; test valid. |
| P67 | AWK-507 | getline var updates NR and FNR, not $0 or NF | portable | getline variable preserves main record; test valid. |
| P68 | AWK-508 | Assigning $(NF+2) creates empty fields and rebuilds with OFS | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P69 | AWK-509 | Changing OFS without touching a field leaves $0 alone | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P70 | AWK-510 | CONVFMT for subscripts and concatenation, OFMT for print, %d for integers | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P71 | AWK-511 | FNR, NR and FILENAME with an empty middle file | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P72 | AWK-512 | FILENAME and FNR in END when the last file is empty | observational | Observational: Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P73 | AWK-513 | getline < FILENAME is a separate stream from the main input | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P74 | AWK-514 | nextfile in each file: NR counts the record that called it | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
| P75 | AWK-515 | An FS= operand between files applies to the next file | portable | Retain: defined mechanism; expected output independently cross-checked on mawk and nawk where available. |
