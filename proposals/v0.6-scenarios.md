# v0.6 PROPOSAL: adversarial semantic scenarios (draft, not frozen)

> **These are proposals from the implementation side.** Grok Bot drafted them. Grok Bot also works on pyawk and hawk,
> two of the implementations under test. Nothing here is a challenge test. To keep the challenge independent,
> **ChatGPT should review, rewrite or discard each scenario, and freeze its own versions.** That includes
> re-deriving every expectation from POSIX.1-2024 itself.

Requested in `feedback/ChatGPT-response-to-v0.5.md` (next actions). Prepared on 7 November 2026.

## How the expectations were chosen

- **Source of the expectations.** Every expected stdout, stderr and exit status comes from the POSIX.1-2024 awk text,
  cited by line number in `/workspace/awk2024.txt`. A few scenarios also cite the XBD regular-expression rules
  that awk2024.txt line 838 incorporates.
- **Role of the recorded behaviour.** The table under each scenario shows how five implementations behave. It is for
  information only. **It was recorded after the expectations were written, and it was not used to choose them.**
- **Corrections made after the probe.** Some expectations were revised after it ran, but only where the POSIX text
  supported the change.
  - Two notes are reworded so they make no claim about history: the substr m = 0 scenario and the index empty-needle
    scenario.
  - For the two scenarios on uninitialised fields, every implementation disagrees with the text. Their status was
    changed to *provisional*, and their expectations were kept.
- **Status.**
  - `portable`: the text specifies the result.
  - `portable (provisional)`: the result rests on a reading that ChatGPT should confirm, or one that established
    implementations dispute.
  - `observational`: the text is silent or contested. The expectation shown is the literal reading, for discussion.
- **Defaults.** Expected stderr is empty, and the exit status is 0, unless stated otherwise.
- **How each scenario runs.** The program is in `prog.awk` and runs as `awk [options] -f prog.awk [operands]`, in a
  fresh directory that contains the listed files. Stdin is as given, and LC_ALL is C unless stated otherwise.
- **Reproducing the run.** `proposals/v0.6/scenarios.py` is the source, `probe.py` reruns the probe, and `render.py`
  regenerates this file. The raw results are in `results-2026-11-07.json`.

**75 scenarios:** 8 observational, 61 portable, 6 portable (provisional).

**Implementations probed:**

| Implementation | Version |
|---|---|
| mawk | 1.3.4 20250131 |
| gawk --posix | GNU Awk 5.4.1 |
| onetrue | One True AWK 20260426 (git 5739fd7) |
| pyawk | enhancements b6a3d25 |
| hawk | enhancements cdf59f5 (interpreter identical to 9f09764; release binary sha256 8eaaf242…1a19) |

Duplicates: the scenarios were checked against v0.5 only by keyword. There are no `%c`, `system()`, `getline < "-"`
or whole-array `delete` programs in v0.5. ChatGPT should still check for overlap with AWK-001 to AWK-440.

## Overview

| ID | Area | Scenario | Status | mawk | gawk --posix | onetrue | pyawk | hawk |
|---|---|---|---|---|---|---|---|---|
| P01 | -v / assignment operands | -v value with \t escape | portable | pass | pass | pass | pass | pass |
| P02 | -v / assignment operands | -v value ending in an unescaped backslash | portable | pass | pass | pass | pass | pass |
| P03 | -v / assignment operands | -v value with \\ (double backslash) | portable | pass | pass | pass | pass | pass |
| P04 | -v / assignment operands | -v value with octal escapes | portable | pass | pass | pass | pass | pass |
| P05 | -v / assignment operands | -v numeric string with leading zeros | portable | pass | pass | pass | pass | pass |
| P06 | -v / assignment operands | -v numeric string with leading and trailing blanks | portable | pass | pass | pass | pass | pass |
| P07 | -v / assignment operands | -v value that only looks numeric (1e) | portable | pass | pass | pass | pass | pass |
| P08 | -v / assignment operands | Assignment operand with \t escape | portable | pass | pass | pass | pass | pass |
| P09 | -v / assignment operands | Timing of assignment operands around BEGIN and END | portable | pass | pass | pass | pass | pass |
| P10 | -F sepstring | -F '\t' is escape-processed like -v FS= | portable | pass | pass | pass | pass | pass |
| P11 | -F sepstring | -F t means the letter t, not tab | portable (provisional) | pass | pass | **differs** | pass | pass |
| P12 | -F sepstring | -F with a single ERE metacharacter '|' is literal | portable | pass | pass | pass | pass | pass |
| P13 | -F sepstring | -F with a multi-character ERE | portable | pass | pass | pass | pass | pass |
| P14 | -F sepstring | -F ' ' is the default field splitting | portable | pass | pass | pass | pass | pass |
| P15 | -F sepstring | -F '\\.' becomes the ERE \. (a literal dot) | portable | pass | pass | pass | pass | pass |
| P16 | printf %c | %c with a numeric argument | portable | pass | pass | pass | pass | pass |
| P17 | printf %c | %c with a string constant that looks numeric | portable | pass | pass | pass | pass | pass |
| P18 | printf %c | %c with a number and a concatenated string | portable | pass | pass | pass | pass | pass |
| P19 | printf %c | %c with a numeric-string field | observational | pass | pass | pass | pass | pass |
| P20 | printf %c | %c with width and the - flag | portable | pass | pass | pass | pass | pass |
| P21 | close() / system() | system() returns the command's exit status | portable | pass | **differs** | pass | pass | pass |
| P22 | close() / system() | Output order around system() | observational | pass | pass | pass | pass | pass |
| P23 | close() / system() | close() of a stream that was never opened is non-zero | portable | pass | pass | pass | pass | pass |
| P24 | close() / system() | close() twice: 0 the first time, then non-zero | portable | pass | pass | pass | pass | pass |
| P25 | close() / system() | close() of an input pipe whose command succeeded | portable | pass | pass | pass | pass | pass |
| P26 | close() / system() | close() of an output pipe whose command exits 3 | observational | pass | **differs** | **differs** | pass | pass |
| P27 | close() / system() | Reading a file again after close() starts at the beginning | portable | pass | pass | pass | pass | pass |
| P28 | close() / system() | '>' after close() truncates again | portable | pass | pass | pass | pass | pass |
| P29 | close() / system() | getline from a missing file returns -1 and leaves NR alone | portable | pass | pass | pass | pass | pass |
| P30 | getline < "-" / "-" operands | getline < "-" when a file named "-" exists | observational | **differs** | **differs** | **differs** | **differs** | **differs** |
| P31 | getline < "-" / "-" operands | -f - reads the program from standard input | portable | pass | pass | pass | pass | pass |
| P32 | getline < "-" / "-" operands | ARGV element set to "-" at run time reads stdin | portable | pass | pass | pass | pass | pass |
| P33 | uninitialised values | An uninitialised scalar is both 0 and "" | portable | pass | pass | pass | pass | pass |
| P34 | uninitialised values | Comparisons involving an uninitialised value | portable | pass | pass | pass | pass | pass |
| P35 | uninitialised values | An empty field is uninitialised | portable (provisional) | **differs** | **differs** | **differs** | **differs** | **differs** |
| P36 | uninitialised values | Referencing a field past NF does not create it | portable (provisional) | **differs** | **differs** | **differs** | **differs** | **differs** |
| P37 | uninitialised values | 'in' does not create an element; a reference does | portable | pass | pass | pass | pass | pass |
| P38 | uninitialised values | Missing function arguments are uninitialised | portable | pass | pass | pass | pass | pass |
| P39 | uninitialised values | An uninitialised global passed to a function becomes an array | observational | pass | pass | pass | pass | pass |
| P40 | substr | substr bounds: omitted n, n too large, start past the end | portable | pass | pass | pass | pass | pass |
| P41 | substr | substr with n <= 0 is empty | portable | pass | pass | pass | pass | pass |
| P42 | substr | substr with m = 0 | observational | **differs** | **differs** | **differs** | **differs** | **differs** |
| P43 | substr | substr and length count characters in UTF-8 | portable | **differs** | pass | pass | pass | pass |
| P44 | index / match / RSTART / RLENGTH | index with an empty needle | observational | pass | pass | **differs** | pass | pass |
| P45 | index / match / RSTART / RLENGTH | index basic cases, including an empty haystack | portable | pass | pass | pass | pass | pass |
| P46 | index / match / RSTART / RLENGTH | match of an ERE that matches empty | portable | pass | pass | pass | pass | pass |
| P47 | index / match / RSTART / RLENGTH | match of /$/ is at the end of the string | portable (provisional) | pass | pass | pass | pass | pass |
| P48 | index / match / RSTART / RLENGTH | A failed match resets RSTART and RLENGTH | portable | pass | pass | pass | pass | pass |
| P49 | index / match / RSTART / RLENGTH | RSTART and RLENGTH count characters in UTF-8 | portable | **differs** | pass | **differs** | pass | pass |
| P50 | index / match / RSTART / RLENGTH | Leftmost beats longer; then longest at the same start | portable | pass | pass | pass | pass | pass |
| P51 | index / match / RSTART / RLENGTH | Other functions do not set RSTART or RLENGTH | portable | pass | pass | pass | pass | pass |
| P52 | split | split with fs " " uses default field splitting | portable (provisional) | pass | pass | pass | pass | pass |
| P53 | split | split with a single-character fs "." is literal | portable (provisional) | pass | pass | pass | pass | pass |
| P54 | split | split deletes every old element first | portable | pass | pass | pass | pass | pass |
| P55 | split | split("", A) empties the array | portable | pass | pass | pass | pass | pass |
| P56 | split | split elements are numeric strings | portable | pass | pass | pass | pass | pass |
| P57 | split | The source string is an element of the target array | portable | pass | pass | pass | pass | pass |
| P58 | split | An ERE fs with leading and trailing separators | portable | pass | pass | pass | pass | pass |
| P59 | delete array | delete A, then reuse A | portable | pass | pass | pass | pass | pass |
| P60 | delete array | delete a on an array parameter clears the caller's array | portable | pass | pass | pass | pass | pass |
| P61 | delete array | delete A[k] inside for (k in A) | portable | pass | pass | pass | pass | pass |
| P62 | stateful combinations | exit with no expression in END keeps the earlier status | portable | pass | pass | pass | pass | pass |
| P63 | stateful combinations | exit in BEGIN runs END and reads no input | portable | pass | pass | pass | pass | pass |
| P64 | stateful combinations | exit inside END stops the remaining END actions | portable | pass | pass | pass | pass | pass |
| P65 | stateful combinations | getline var < file leaves NR, FNR, NF and $0 alone | portable | pass | pass | pass | pass | pass |
| P66 | stateful combinations | Plain getline updates NR, FNR, NF and $0 | portable | pass | pass | pass | pass | pass |
| P67 | stateful combinations | getline var updates NR and FNR, not $0 or NF | portable | pass | pass | pass | pass | pass |
| P68 | stateful combinations | Assigning $(NF+2) creates empty fields and rebuilds with OFS | portable | pass | pass | pass | pass | pass |
| P69 | stateful combinations | Changing OFS without touching a field leaves $0 alone | portable | pass | pass | pass | pass | pass |
| P70 | stateful combinations | CONVFMT for subscripts and concatenation, OFMT for print, %d for integers | portable | pass | pass | pass | pass | pass |
| P71 | multi-file | FNR, NR and FILENAME with an empty middle file | portable | pass | pass | pass | pass | pass |
| P72 | multi-file | FILENAME and FNR in END when the last file is empty | observational | pass | pass | pass | pass | pass |
| P73 | multi-file | getline < FILENAME is a separate stream from the main input | portable | pass | pass | pass | pass | pass |
| P74 | multi-file | nextfile in each file: NR counts the record that called it | portable | pass | pass | pass | pass | pass |
| P75 | multi-file | An FS= operand between files applies to the next file | portable | pass | pass | pass | pass | pass |

## pyawk and hawk discrepancies found by the probe (not fixed)

As instructed, **no pyawk or hawk code was changed** because of these results. Each entry has a shell reproducer.

### P30: getline < "-" when a file named "-" exists (observational)

Affected: pyawk, hawk. References that also differ: mawk, gawk --posix, onetrue.

```sh
printf %s 'from-file
' > -
cat > prog.awk <<'EOF'
BEGIN { getline l < "-"; print l }
EOF
printf %s 'from-stdin
' | LC_ALL=C awk -f prog.awk
```

- Expected: stdout "from-file\n", exit 0
- pyawk: stdout "from-stdin\n", exit 0
- hawk: stdout "from-stdin\n", exit 0

### P35: An empty field is uninitialised (portable (provisional))

Affected: pyawk, hawk. References that also differ: mawk, gawk --posix, onetrue.

```sh
cat > prog.awk <<'EOF'
{ print ($2 == 0), ($2 == ""), length($2) }
EOF
printf %s 'a,,c
' | LC_ALL=C awk -F , -f prog.awk
```

- Expected: stdout "1 1 0\n", exit 0
- pyawk: stdout "0 1 0\n", exit 0
- hawk: stdout "0 1 0\n", exit 0

### P36: Referencing a field past NF does not create it (portable (provisional))

Affected: pyawk, hawk. References that also differ: mawk, gawk --posix, onetrue.

```sh
cat > prog.awk <<'EOF'
{ x = $5; y = ($5 == 0); print NF, y, $0 }
EOF
printf %s 'a b
' | LC_ALL=C awk -f prog.awk
```

- Expected: stdout "2 1 a b\n", exit 0
- pyawk: stdout "2 0 a b\n", exit 0
- hawk: stdout "2 0 a b\n", exit 0

### P42: substr with m = 0 (observational)

Affected: pyawk, hawk. References that also differ: mawk, gawk --posix, onetrue.

```sh
cat > prog.awk <<'EOF'
BEGIN { print "[" substr("hello", 0, 2) "]" }
EOF
printf %s '' | LC_ALL=C awk -f prog.awk
```

- Expected: stdout "[h]\n", exit 0
- pyawk: stdout "[he]\n", exit 0
- hawk: stdout "[he]\n", exit 0

## Scenarios

### P01: -v value with \t escape

- **Area:** -v / assignment operands
- **Status:** portable
- **POSIX (awk2024.txt lines):** 77-81; 101-110; 1653-1657
- **Detects:** the -v value is not processed as a STRING token (escape left as two characters)
- **Command:** `LC_ALL=C awk -v 'x=a\tb' -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "a\tb|3\n"; stderr empty; exit 0

```awk
BEGIN { printf "%s|%d\n", x, length(x) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P02: -v value ending in an unescaped backslash

- **Area:** -v / assignment operands
- **Status:** portable
- **POSIX (awk2024.txt lines):** 106-110
- **Detects:** a trailing backslash is treated as an escape, or is rejected or dropped
- **Command:** `LC_ALL=C awk -v 'x=ab\' -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "ab\\|3\n"; stderr empty; exit 0

```awk
BEGIN { printf "%s|%d\n", x, length(x) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P03: -v value with \\ (double backslash)

- **Area:** -v / assignment operands
- **Status:** portable
- **POSIX (awk2024.txt lines):** 107-110; 909-916
- **Detects:** \\ is not reduced to one backslash in assignment values
- **Command:** `LC_ALL=C awk -v 'x=a\\b' -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "a\\b|3\n"; stderr empty; exit 0

```awk
BEGIN { printf "%s|%d\n", x, length(x) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P04: -v value with octal escapes

- **Area:** -v / assignment operands
- **Status:** portable
- **POSIX (awk2024.txt lines):** 107-110; 883-892
- **Detects:** octal \ddd is not decoded in -v values
- **Command:** `LC_ALL=C awk -v 'x=\101\102C' -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "ABC|3\n"; stderr empty; exit 0

```awk
BEGIN { printf "%s|%d\n", x, length(x) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P05: -v numeric string with leading zeros

- **Area:** -v / assignment operands
- **Status:** portable
- **POSIX (awk2024.txt lines):** 599-607; 610-631; 711-717
- **Detects:** a -v value is not treated as a numeric string, or the string value is changed to 10
- **Command:** `LC_ALL=C awk -v x=010 -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "010 1 0 1\n"; stderr empty; exit 0

```awk
BEGIN { print x, (x == 10), (x < 9), (x "" == "010") }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P06: -v numeric string with leading and trailing blanks

- **Area:** -v / assignment operands
- **Status:** portable
- **POSIX (awk2024.txt lines):** 610-625
- **Detects:** blanks around a numeric string stop the numeric comparison
- **Command:** `LC_ALL=C awk -v 'x= 3 ' -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "[ 3 ] 1 1\n"; stderr empty; exit 0

```awk
BEGIN { print "[" x "]", (x == 3), (x < 10) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P07: -v value that only looks numeric (1e)

- **Area:** -v / assignment operands
- **Status:** portable
- **POSIX (awk2024.txt lines):** 610-625; 719-722
- **Detects:** '1e' is accepted as a numeric string (strtod leaves 'e', and it is not a NUMBER token)
- **Command:** `LC_ALL=C awk -v x=1e -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "0 1\n"; stderr empty; exit 0

```awk
BEGIN { print (x == 1), (x + 0) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P08: Assignment operand with \t escape

- **Area:** -v / assignment operands
- **Status:** portable
- **POSIX (awk2024.txt lines):** 101-112
- **Detects:** assignment operands are not escape-processed like -v values
- **Command:** `LC_ALL=C awk -f prog.awk 'x=1\t2' f1`
- **Files:** `f1` = "a\n"
- **Stdin:** ""
- **Expected:** stdout "1\t2|3\n"; stderr empty; exit 0

```awk
{ print x "|" length(x) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P09: Timing of assignment operands around BEGIN and END

- **Area:** -v / assignment operands
- **Status:** portable
- **POSIX (awk2024.txt lines):** 112-114
- **Detects:** an assignment is applied before BEGIN, or an assignment after the last file is not applied before END
- **Command:** `LC_ALL=C awk -f prog.awk x=1 f1 x=2`
- **Files:** `f1` = "a\n"
- **Stdin:** ""
- **Expected:** stdout "B[]\nR[1]\nE[2]\n"; stderr empty; exit 0

```awk
BEGIN { print "B[" x "]" } { print "R[" x "]" } END { print "E[" x "]" }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P10: -F '\t' is escape-processed like -v FS=

- **Area:** -F sepstring
- **Status:** portable
- **POSIX (awk2024.txt lines):** 62-65; 107-110; 960-965
- **Detects:** -F value not escape-processed (FS stays as backslash-t)
- **Command:** `LC_ALL=C awk -F '\t' -f prog.awk`
- **Stdin:** "a b\tc\n"
- **Expected:** stdout "2|c\n"; stderr empty; exit 0

```awk
{ print NF "|" $2 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P11: -F t means the letter t, not tab

- **Area:** -F sepstring
- **Status:** portable (provisional)
- **POSIX (awk2024.txt lines):** 62-65; 964-965
- **Detects:** historical -Ft special case applied in a POSIX mode
- **Note:** Historical awks map -Ft to tab. POSIX defines -F sepstring as -v FS=sepstring, so FS is the letter 't'.
- **Command:** `LC_ALL=C awk -F t -f prog.awk`
- **Stdin:** "atb\tc\n"
- **Expected:** stdout "2|a\n"; stderr empty; exit 0

```awk
{ print NF "|" $1 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | **differs** | `"2\|atb\n"` | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P12: -F with a single ERE metacharacter '|' is literal

- **Area:** -F sepstring
- **Status:** portable
- **POSIX (awk2024.txt lines):** 960-965
- **Detects:** a single-character FS is compiled as an ERE, so '|' would match the empty string
- **Command:** `LC_ALL=C awk -F '|' -f prog.awk`
- **Stdin:** "a|b|c\n"
- **Expected:** stdout "3|b\n"; stderr empty; exit 0

```awk
{ print NF "|" $2 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P13: -F with a multi-character ERE

- **Area:** -F sepstring
- **Status:** portable
- **POSIX (awk2024.txt lines):** 968-969
- **Detects:** a multi-character FS is not treated as an ERE, or one or more is not grouped
- **Command:** `LC_ALL=C awk -F '[:;]+' -f prog.awk`
- **Stdin:** "a:;b;c\n"
- **Expected:** stdout "3|b\n"; stderr empty; exit 0

```awk
{ print NF "|" $2 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P14: -F ' ' is the default field splitting

- **Area:** -F sepstring
- **Status:** portable
- **POSIX (awk2024.txt lines):** 62-65; 962-963
- **Detects:** -F ' ' splits on single spaces only, giving empty fields
- **Command:** `LC_ALL=C awk -F ' ' -f prog.awk`
- **Stdin:** "  a \t b  \n"
- **Expected:** stdout "2|a|b\n"; stderr empty; exit 0

```awk
{ print NF "|" $1 "|" $2 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P15: -F '\\.' becomes the ERE \. (a literal dot)

- **Area:** -F sepstring
- **Status:** portable
- **POSIX (awk2024.txt lines):** 62-65; 909-916; 897-904
- **Detects:** the sepstring is escape-processed twice or not at all
- **Command:** `LC_ALL=C awk -F '\\.' -f prog.awk`
- **Stdin:** "a.b\n"
- **Expected:** stdout "2|b\n"; stderr empty; exit 0

```awk
{ print NF "|" $2 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P16: %c with a numeric argument

- **Area:** printf %c
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1096-1097
- **Detects:** a numeric argument is printed as its first digit
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "Aa\n"; stderr empty; exit 0

```awk
BEGIN { printf "%c%c\n", 65, 97 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P17: %c with a string constant that looks numeric

- **Area:** printf %c
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1098-1102
- **Detects:** a string constant is converted to a number for %c
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "6|h\n"; stderr empty; exit 0

```awk
BEGIN { printf "%c|%c\n", "65", "hello" }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P18: %c with a number and a concatenated string

- **Area:** printf %c
- **Status:** portable
- **POSIX (awk2024.txt lines):** 596-598; 1096-1102
- **Detects:** concatenation result treated as numeric for %c
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "H7\n"; stderr empty; exit 0

```awk
BEGIN { x = 72; y = x ""; printf "%c%c\n", x, y }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P19: %c with a numeric-string field

- **Area:** printf %c
- **Status:** observational
- **POSIX (awk2024.txt lines):** 599-607; 1096-1099
- **Detects:** (contested) numeric-string handling of %c
- **Note:** A field '66' is a numeric string. Does it 'have a numeric value' (1096)? The literal reading gives 'B'; the alternative is '6'.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** "66\n"
- **Expected:** stdout "B\n"; stderr empty; exit 0

```awk
{ printf "%c\n", $1 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P20: %c with width and the - flag

- **Area:** printf %c
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1076-1079; 1096-1099
- **Detects:** width or flags ignored for %c
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "[  x][y  ]\n"; stderr empty; exit 0

```awk
BEGIN { printf "[%3c][%-3c]\n", "x", "y" }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P21: system() returns the command's exit status

- **Area:** close() / system()
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1255-1258
- **Detects:** system returns a raw wait status (768), or always 0
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "3 0 1\n"; stderr empty; exit 0

```awk
BEGIN { a = system("exit 3"); b = system("true"); c = system("false"); print a, b, c }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | **differs** | `"768 0 256\n"` | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P22: Output order around system()

- **Area:** close() / system()
- **Status:** observational
- **POSIX (awk2024.txt lines):** 1255-1258; 1043-1044
- **Detects:** (observational) unflushed output appears after the command's output
- **Note:** POSIX 2024 does not say that pending output is flushed before system(). Historical awks flush it.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "ab\nc0\n"; stderr empty; exit 0

```awk
BEGIN { printf "a"; r = system("echo b"); print "c" r }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P23: close() of a stream that was never opened is non-zero

- **Area:** close() / system()
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1208-1212
- **Detects:** close of an unknown stream returns 0
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "1\n"; stderr empty; exit 0

```awk
BEGIN { print (close("never-opened") != 0) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P24: close() twice: 0 the first time, then non-zero

- **Area:** close() / system()
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1208-1212; 1051-1057
- **Detects:** close of a stream that is already closed reports success
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "0 1\n"; stderr empty; exit 0

```awk
BEGIN { print "x" > "out"; a = close("out"); b = close("out"); print a, (b != 0) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P25: close() of an input pipe whose command succeeded

- **Area:** close() / system()
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1220-1228; 1208-1212
- **Detects:** close of a successful input pipe returns non-zero, or a stale status
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "a 0\n"; stderr empty; exit 0

```awk
BEGIN { "echo a" | getline x; print x, close("echo a") }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P26: close() of an output pipe whose command exits 3

- **Area:** close() / system()
- **Status:** observational
- **POSIX (awk2024.txt lines):** 1058-1065; 1208-1212
- **Detects:** (observational) close hides the command's failure
- **Note:** Is 'successful' the pclose() call, or the command's status? This is the literal reading of non-zero on failure.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "1\n"; stderr empty; exit 0

```awk
BEGIN { c = "cat >/dev/null; exit 3"; print "x" | c; r = close(c); print (r != 0) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | **differs** | `"0\n"` | 0 |
| onetrue | **differs** | `"0\n"` | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P27: Reading a file again after close() starts at the beginning

- **Area:** close() / system()
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1243-1248; 1208-1212
- **Detects:** close does not reset the read position, or reopening is cached
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Files:** `f` = "1\n2\n"
- **Stdin:** ""
- **Expected:** stdout "1 2 1\n"; stderr empty; exit 0

```awk
BEGIN { getline a < "f"; getline b < "f"; close("f"); getline c < "f"; print a, b, c }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P28: '>' after close() truncates again

- **Area:** close() / system()
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1051-1057
- **Detects:** the second '>' appends instead of truncating
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "got b\n"; stderr empty; exit 0

```awk
BEGIN { print "a" > "o"; close("o"); print "b" > "o"; close("o"); while ((getline l < "o") > 0) print "got " l }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P29: getline from a missing file returns -1 and leaves NR alone

- **Area:** close() / system()
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1260; 1243-1250
- **Detects:** the error is reported as 0 (EOF), or is fatal
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "-1 0 []\n"; stderr empty; exit 0

```awk
BEGIN { r = (getline l < "no-such-file"); print r, NR, "[" l "]" }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P30: getline < "-" when a file named "-" exists

- **Area:** getline < "-" / "-" operands
- **Status:** observational
- **POSIX (awk2024.txt lines):** 1243-1250; contrast 73, 100, 776-778
- **Detects:** (observational) literal pathname versus stdin convention
- **Note:** POSIX gives '-' a stdin meaning only for file operands (100, 777) and -f progfile (73). getline < expression uses the value as a pathname (1245). The literal reading is the file '-'. Every historical awk reads stdin.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Files:** `-` = "from-file\n"
- **Stdin:** "from-stdin\n"
- **Expected:** stdout "from-file\n"; stderr empty; exit 0

```awk
BEGIN { getline l < "-"; print l }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | **differs** | `"from-stdin\n"` | 0 |
| gawk --posix | **differs** | `"from-stdin\n"` | 0 |
| onetrue | **differs** | `"from-stdin\n"` | 0 |
| pyawk | **differs** | `"from-stdin\n"` | 0 |
| hawk | **differs** | `"from-stdin\n"` | 0 |

### P31: -f - reads the program from standard input

- **Area:** getline < "-" / "-" operands
- **Status:** portable
- **POSIX (awk2024.txt lines):** 72-76
- **Detects:** -f - opens a file named '-'
- **Command:** `LC_ALL=C awk -f -`
- **Stdin:** "BEGIN { print \"prog from stdin\" }\n"
- **Expected:** stdout "prog from stdin\n"; stderr empty; exit 0

```awk
# program read from stdin (shown above)
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P32: ARGV element set to "-" at run time reads stdin

- **Area:** getline < "-" / "-" operands
- **Status:** portable
- **POSIX (awk2024.txt lines):** 752-759; 776-778; 797-798
- **Detects:** the changed ARGV is ignored, or '-' is opened as a file
- **Command:** `LC_ALL=C awk -f prog.awk f1`
- **Files:** `f1` = "f\n"
- **Stdin:** "s\n"
- **Expected:** stdout "- s\n"; stderr empty; exit 0

```awk
BEGIN { ARGV[1] = "-"; ARGC = 2 } { print FILENAME, $0 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P33: An uninitialised scalar is both 0 and ""

- **Area:** uninitialised values
- **Status:** portable
- **POSIX (awk2024.txt lines):** 732-734
- **Detects:** the uninitialised value takes one type only
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "both\n0 0 []\n"; stderr empty; exit 0

```awk
BEGIN { if (x == 0 && x == "") print "both"; print length(x), x + 0, "[" x "]" }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P34: Comparisons involving an uninitialised value

- **Area:** uninitialised values
- **Status:** portable
- **POSIX (awk2024.txt lines):** 711-723
- **Detects:** uninitialised compared with the string constant "0" numerically, or with 1 as strings
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "1 1 0 1\n"; stderr empty; exit 0

```awk
BEGIN { print (x < "a"), (x < 1), (x == "0"), (x == 0) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P35: An empty field is uninitialised

- **Area:** uninitialised values
- **Status:** portable (provisional)
- **POSIX (awk2024.txt lines):** 741-743; 711-717
- **Detects:** an empty field compares as a string only, so $2 == 0 is false
- **Note:** Normative: 742 says an empty field created by FS splitting has the uninitialized value, and 717 says comparing it with a number is numeric. The RATIONALE (2312-2317) gives this very case. Established implementations compare it as the string "" here, so this may need a standards interpretation, as with AWK-415 and AWK-417.
- **Command:** `LC_ALL=C awk -F , -f prog.awk`
- **Stdin:** "a,,c\n"
- **Expected:** stdout "1 1 0\n"; stderr empty; exit 0

```awk
{ print ($2 == 0), ($2 == ""), length($2) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | **differs** | `"0 1 0\n"` | 0 |
| gawk --posix | **differs** | `"0 1 0\n"` | 0 |
| onetrue | **differs** | `"0 1 0\n"` | 0 |
| pyawk | **differs** | `"0 1 0\n"` | 0 |
| hawk | **differs** | `"0 1 0\n"` | 0 |

### P36: Referencing a field past NF does not create it

- **Area:** uninitialised values
- **Status:** portable (provisional)
- **POSIX (awk2024.txt lines):** 738-739
- **Detects:** a reference to $5 raises NF or rebuilds $0, or $5 compares as a string
- **Note:** 738 says a nonexistent field evaluates to the uninitialized value, and 717 makes the comparison numeric. The same caveat applies as for the previous scenario.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** "a b\n"
- **Expected:** stdout "2 1 a b\n"; stderr empty; exit 0

```awk
{ x = $5; y = ($5 == 0); print NF, y, $0 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | **differs** | `"2 0 a b\n"` | 0 |
| gawk --posix | **differs** | `"2 0 a b\n"` | 0 |
| onetrue | **differs** | `"2 0 a b\n"` | 0 |
| pyawk | **differs** | `"2 0 a b\n"` | 0 |
| hawk | **differs** | `"2 0 a b\n"` | 0 |

### P37: 'in' does not create an element; a reference does

- **Area:** uninitialised values
- **Status:** portable
- **POSIX (awk2024.txt lines):** 708-710
- **Detects:** 'in' creates the element, or a reference does not
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "absent\n1 1\n"; stderr empty; exit 0

```awk
BEGIN { if (("k" in a) == 0) print "absent"; x = a["k"]; print ("k" in a), length(a) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P38: Missing function arguments are uninitialised

- **Area:** uninitialised values
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1272-1275
- **Detects:** missing parameters are only numeric or only string
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "11\n"; stderr empty; exit 0

```awk
function f(a, b) { return (b == 0) "" (b == "") } BEGIN { print f(1) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P39: An uninitialised global passed to a function becomes an array

- **Area:** uninitialised values
- **Status:** observational
- **POSIX (awk2024.txt lines):** 1111-1113; 1272-1275
- **Detects:** (observational) by-reference passing of a not-yet-typed name
- **Note:** POSIX says arrays are passed by reference (1113), but not whether an untyped global counts as an 'array name'.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "1 1\n"; stderr empty; exit 0

```awk
function fill(arr) { arr["x"] = 1 } BEGIN { fill(A); print length(A), A["x"] }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P40: substr bounds: omitted n, n too large, start past the end

- **Area:** substr
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1188-1192
- **Detects:** an off-by-one at the end of the string
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "ello|ello||o\n"; stderr empty; exit 0

```awk
BEGIN { s = "hello"; print substr(s, 2) "|" substr(s, 2, 100) "|" substr(s, 6) "|" substr(s, 5, 1) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P41: substr with n <= 0 is empty

- **Area:** substr
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1190
- **Detects:** a negative n is taken as 'to the end', or wraps
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "[][]\n"; stderr empty; exit 0

```awk
BEGIN { print "[" substr("hello", 2, 0) "][" substr("hello", 2, -1) "]" }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P42: substr with m = 0

- **Area:** substr
- **Status:** observational
- **POSIX (awk2024.txt lines):** 1190-1192
- **Detects:** (observational) clamping a start before position 1
- **Note:** The text (1190-1192) does not define a start before position 1. The expectation shown is one reading: the characters at positions m..m+n-1 that exist, which gives 'h'. Another reading is to treat m as 1, which gives 'he'. Recommendation: ChatGPT should choose a reading, or classify this case as nonportable.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "[h]\n"; stderr empty; exit 0

```awk
BEGIN { print "[" substr("hello", 0, 2) "]" }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | **differs** | `"[he]\n"` | 0 |
| gawk --posix | **differs** | `"[he]\n"` | 0 |
| onetrue | **differs** | `"[he]\n"` | 0 |
| pyawk | **differs** | `"[he]\n"` | 0 |
| hawk | **differs** | `"[he]\n"` | 0 |

### P43: substr and length count characters in UTF-8

- **Area:** substr
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1188-1192; 1953-1955; 163-167
- **Detects:** byte-based substr or length in a UTF-8 locale
- **Command:** `LC_ALL=C.UTF-8 awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "é 3\n"; stderr empty; exit 0

```awk
BEGIN { s = "a\303\251b"; print substr(s, 2, 1), length(s) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | **differs** | `"� 4\n"` | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P44: index with an empty needle

- **Area:** index / match / RSTART / RLENGTH
- **Status:** observational
- **POSIX (awk2024.txt lines):** 1155-1157
- **Detects:** (observational) empty-needle convention
- **Note:** The text does not say whether an empty string 'occurs' in s. The literal reading is that it occurs first at position 1, including in an empty s.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "1 1\n"; stderr empty; exit 0

```awk
BEGIN { print index("abc", ""), index("", "") }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | **differs** | `"1 0\n"` | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P45: index basic cases, including an empty haystack

- **Area:** index / match / RSTART / RLENGTH
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1155-1157
- **Detects:** an off-by-one in index, or a crash on an empty haystack
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "0 3 3\n"; stderr empty; exit 0

```awk
BEGIN { print index("", "a"), index("abc", "c"), index("abcabc", "ca") }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P46: match of an ERE that matches empty

- **Area:** index / match / RSTART / RLENGTH
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1162-1165
- **Detects:** an empty match is reported as no match (0, -1)
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "1 1 0\n"; stderr empty; exit 0

```awk
BEGIN { print match("abc", /x*/), RSTART, RLENGTH }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P47: match of /$/ is at the end of the string

- **Area:** index / match / RSTART / RLENGTH
- **Status:** portable (provisional)
- **POSIX (awk2024.txt lines):** 1162-1165
- **Detects:** an empty match at the end is reported as 0, or as position 3
- **Note:** The empty match is after the last character, which is position 4 when numbering from 1.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "4 4 0\n"; stderr empty; exit 0

```awk
BEGIN { print match("abc", /$/), RSTART, RLENGTH }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P48: A failed match resets RSTART and RLENGTH

- **Area:** index / match / RSTART / RLENGTH
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1164-1165; 831-833
- **Detects:** RSTART or RLENGTH keep their values from the earlier match
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "2 1 0 -1\n"; stderr empty; exit 0

```awk
BEGIN { match("abc", /b/); a = RSTART " " RLENGTH; match("abc", /z/); print a, RSTART, RLENGTH }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P49: RSTART and RLENGTH count characters in UTF-8

- **Area:** index / match / RSTART / RLENGTH
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1162-1165; 1953-1955
- **Detects:** byte offsets in RSTART or RLENGTH
- **Command:** `LC_ALL=C.UTF-8 awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "3 2\n2 1\n"; stderr empty; exit 0

```awk
BEGIN { print match("\303\251\303\251ab", /ab/), RLENGTH; print match("x\303\251", /\303\251/), RLENGTH }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | **differs** | `"5 2\n2 2\n"` | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | **differs** | `"3 2\n0 -1\n"` | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P50: Leftmost beats longer; then longest at the same start

- **Area:** index / match / RSTART / RLENGTH
- **Status:** portable
- **POSIX (awk2024.txt lines):** 838 (XBD 9.1 and 9.4); 1162-1165; 1176-1180
- **Detects:** the longest alternative is chosen over the leftmost (an NFA or alternation-order bug)
- **Note:** This replaces redundant leftmost-longest tests. The longer alternative starts later, so the earlier, shorter match wins.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "1 2\n<za>bcd\n1 4\n"; stderr empty; exit 0

```awk
BEGIN { print match("zabcd", /abcd|za/), RLENGTH; s = "zabcd"; sub(/abcd|za/, "<&>", s); print s; print match("abcd", /ab|abcd/), RLENGTH }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P51: Other functions do not set RSTART or RLENGTH

- **Area:** index / match / RSTART / RLENGTH
- **Status:** portable
- **POSIX (awk2024.txt lines):** 831-833; 823-824; 1162-1165
- **Detects:** sub, gsub, split or index change RSTART or RLENGTH
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "3 1 1\n"; stderr empty; exit 0

```awk
BEGIN { match("abc", /c/); s = "a"; sub(/a/, "x", s); t = "b"; gsub(/b/, "y", t); n = split("a b", A); print RSTART, RLENGTH, index("abc", "a") }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P52: split with fs " " uses default field splitting

- **Area:** split
- **Status:** portable (provisional)
- **POSIX (awk2024.txt lines):** 1166-1172; 955-963
- **Detects:** fs " " is used as a single-space ERE
- **Note:** This applies the FS rules (955-969) to fs. 1169 says 'with the ERE fs', so ChatGPT should confirm the reading.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "3 a c\n"; stderr empty; exit 0

```awk
BEGIN { n = split("  a b\t c  ", A, " "); print n, A[1], A[3] }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P53: split with a single-character fs "." is literal

- **Area:** split
- **Status:** portable (provisional)
- **POSIX (awk2024.txt lines):** 1166-1172; 960-965
- **Detects:** a single-character fs is compiled as an ERE
- **Note:** This uses the same FS-rules reading as the previous scenario. A pure ERE reading gives 6 empty elements.
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "3 b\n"; stderr empty; exit 0

```awk
BEGIN { n = split("a.b.c", A, "."); print n, A[2] }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P54: split deletes every old element first

- **Area:** split
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1168-1169
- **Detects:** stale elements beyond n survive
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "2 2 0\n"; stderr empty; exit 0

```awk
BEGIN { A[1] = "old"; A[9] = "x"; n = split("p q", A); print n, length(A), (9 in A) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P55: split("", A) empties the array

- **Area:** split
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1168-1169; 2345-2346
- **Detects:** split of an empty string leaves elements, or returns 1
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "0 0\n"; stderr empty; exit 0

```awk
BEGIN { A[1]; A[2]; n = split("", A); print n, length(A) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P56: split elements are numeric strings

- **Area:** split
- **Status:** portable
- **POSIX (awk2024.txt lines):** 606; 711-717
- **Detects:** split elements compare as strings
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "1 1 0\n"; stderr empty; exit 0

```awk
BEGIN { split("10 9 abc", A); print (A[1] > A[2]), (A[3] > A[1]), ("10" > "9") }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P57: The source string is an element of the target array

- **Area:** split
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1168-1169
- **Detects:** the target is cleared before the source is read
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "3 x z\n"; stderr empty; exit 0

```awk
BEGIN { A[1] = "x y z"; n = split(A[1], A); print n, A[1], A[3] }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P58: An ERE fs with leading and trailing separators

- **Area:** split
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1166-1172; 968-969
- **Detects:** empty leading or trailing elements are dropped
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "5 [] [] []\n"; stderr empty; exit 0

```awk
BEGIN { n = split(":a::b:", A, /:/); print n, "[" A[1] "]", "[" A[3] "]", "[" A[5] "]" }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P59: delete A, then reuse A

- **Area:** delete array
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1022-1032
- **Detects:** the array is unusable after delete A, or elements remain
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "0 0\n1 5\n"; stderr empty; exit 0

```awk
BEGIN { A[1]; A[2]; A["x"]; delete A; print length(A), (1 in A); A["y"] = 5; print length(A), A["y"] }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P60: delete a on an array parameter clears the caller's array

- **Area:** delete array
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1022-1032; 1111-1113
- **Detects:** delete of a parameter clears only a local copy, or breaks the reference
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "0\n1\n"; stderr empty; exit 0

```awk
function clr(a) { delete a } BEGIN { A[1]; A[2]; clr(A); print length(A); A[3] = 1; print length(A) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P61: delete A[k] inside for (k in A)

- **Area:** delete array
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1022-1032
- **Detects:** the iteration is disturbed by deleting the current element (some elements are left)
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "0\n"; stderr empty; exit 0

```awk
BEGIN { for (i = 1; i <= 100; i++) A[i] = i; for (k in A) delete A[k]; print length(A) }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P62: exit with no expression in END keeps the earlier status

- **Area:** stateful combinations
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1038-1042
- **Detects:** a bare exit in END resets the status to 0
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** "a\n"
- **Expected:** stdout ""; stderr empty; exit 3

```awk
{ exit 3 } END { exit }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 3 |
| gawk --posix | pass |  | 3 |
| onetrue | pass |  | 3 |
| pyawk | pass |  | 3 |
| hawk | pass |  | 3 |

### P63: exit in BEGIN runs END and reads no input

- **Area:** stateful combinations
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1038-1040
- **Detects:** END is skipped, or the main rule runs
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** "x\n"
- **Expected:** stdout "b\ne\n"; stderr empty; exit 2

```awk
BEGIN { print "b"; exit 2 } { print "main" } END { print "e" }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 2 |
| gawk --posix | pass |  | 2 |
| onetrue | pass |  | 2 |
| pyawk | pass |  | 2 |
| hawk | pass |  | 2 |

### P64: exit inside END stops the remaining END actions

- **Area:** stateful combinations
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1039-1040
- **Detects:** later END actions still run
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "1\n"; stderr empty; exit 4

```awk
END { print "1"; exit 4 } END { print "2" }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 4 |
| gawk --posix | pass |  | 4 |
| onetrue | pass |  | 4 |
| pyawk | pass |  | 4 |
| hawk | pass |  | 4 |

### P65: getline var < file leaves NR, FNR, NF and $0 alone

- **Area:** stateful combinations
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1243-1250
- **Detects:** redirected getline var updates NR or FNR
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Files:** `f` = "L1\nL2\n"
- **Stdin:** "a b c\n"
- **Expected:** stdout "1 1 3 a b c L1\n"; stderr empty; exit 0

```awk
{ getline v < "f"; print NR, FNR, NF, $0, v }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P66: Plain getline updates NR, FNR, NF and $0

- **Area:** stateful combinations
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1236-1238
- **Detects:** NF is not recomputed after getline
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** "a\nb c\n"
- **Expected:** stdout "2 2 2 b c\n"; stderr empty; exit 0

```awk
NR == 1 { getline; print NR, FNR, NF, $0 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P67: getline var updates NR and FNR, not $0 or NF

- **Area:** stateful combinations
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1239-1242
- **Detects:** getline var overwrites $0, or does not count the record
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** "a\nb c\n"
- **Expected:** stdout "2 2 1 a b c\n"; stderr empty; exit 0

```awk
NR == 1 { getline v; print NR, FNR, NF, $0, v }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P68: Assigning $(NF+2) creates empty fields and rebuilds with OFS

- **Area:** stateful combinations
- **Status:** portable
- **POSIX (awk2024.txt lines):** 739-741; 50-53
- **Detects:** the intervening field is missing, or $0 is not rebuilt
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** "a b\n"
- **Expected:** stdout "a-b--z\n4\n"; stderr empty; exit 0

```awk
BEGIN { OFS = "-" } { $(NF + 2) = "z"; print; print NF }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P69: Changing OFS without touching a field leaves $0 alone

- **Area:** stateful combinations
- **Status:** portable
- **POSIX (awk2024.txt lines):** 50-53
- **Detects:** $0 is rebuilt eagerly when OFS changes, or not rebuilt after $1 = $1
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** "a b c\n"
- **Expected:** stdout "a b c\na-b-c\n"; stderr empty; exit 0

```awk
BEGIN { OFS = "-" } { print $0; $1 = $1; print $0 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P70: CONVFMT for subscripts and concatenation, OFMT for print, %d for integers

- **Area:** stateful combinations
- **Status:** portable
- **POSIX (awk2024.txt lines):** 590-595; 783-785; 815-818
- **Detects:** OFMT is used for subscripts, or CONVFMT for integers
- **Command:** `LC_ALL=C awk -f prog.awk`
- **Stdin:** ""
- **Expected:** stdout "3.1\n3.1416\n3.1\n17\n"; stderr empty; exit 0

```awk
BEGIN { CONVFMT = "%.2g"; OFMT = "%.4f"; x = 3.14159; a[x] = 1; for (k in a) print k; print x; print x ""; print 17 "" }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P71: FNR, NR and FILENAME with an empty middle file

- **Area:** multi-file
- **Status:** portable
- **POSIX (awk2024.txt lines):** 797-803; 811-814
- **Detects:** FNR is not reset for the file after an empty one, or NR is miscounted
- **Command:** `LC_ALL=C awk -f prog.awk f1 empty f2`
- **Files:** `f1` = "a\nb\n"; `empty` = ""; `f2` = "c\n"
- **Stdin:** ""
- **Expected:** stdout "f1 1\nf2 3\nf2 3 1\n"; stderr empty; exit 0

```awk
FNR == 1 { print FILENAME, NR } END { print FILENAME, NR, FNR }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P72: FILENAME and FNR in END when the last file is empty

- **Area:** multi-file
- **Status:** observational
- **POSIX (awk2024.txt lines):** 797-803
- **Detects:** (observational) END state after an empty last file
- **Note:** Is an empty file 'processed' (799, 803)? The literal reading says yes: FILENAME is 'empty' and FNR is 0.
- **Command:** `LC_ALL=C awk -f prog.awk f1 empty`
- **Files:** `f1` = "a\nb\n"; `empty` = ""
- **Stdin:** ""
- **Expected:** stdout "empty 2 0\n"; stderr empty; exit 0

```awk
END { print FILENAME, NR, FNR }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P73: getline < FILENAME is a separate stream from the main input

- **Area:** multi-file
- **Status:** portable
- **POSIX (awk2024.txt lines):** 1243-1248
- **Detects:** the redirected stream shares or moves the main input's position
- **Command:** `LC_ALL=C awk -f prog.awk f1`
- **Files:** `f1` = "1\n2\n3\n"
- **Stdin:** ""
- **Expected:** stdout "3 3\n"; stderr empty; exit 0

```awk
FNR == 1 { while ((getline l < FILENAME) > 0) n++; close(FILENAME) } END { print n, NR }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P74: nextfile in each file: NR counts the record that called it

- **Area:** multi-file
- **Status:** portable
- **POSIX (awk2024.txt lines):** 812-814; 1035-1037
- **Detects:** skipped records are counted in NR, or the record that ran nextfile is not
- **Command:** `LC_ALL=C awk -f prog.awk f1 f2`
- **Files:** `f1` = "a\nb\nc\n"; `f2` = "d\ne\n"
- **Stdin:** ""
- **Expected:** stdout "f1 1 1\nf2 1 3\n4\n"; stderr empty; exit 0

```awk
FNR == 2 { nextfile } { print FILENAME, FNR, NR } END { print NR }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

### P75: An FS= operand between files applies to the next file

- **Area:** multi-file
- **Status:** portable
- **POSIX (awk2024.txt lines):** 112-114; 955-957
- **Detects:** the FS assignment is applied too early, or to the current record
- **Command:** `LC_ALL=C awk -f prog.awk f1 FS=: f2`
- **Files:** `f1` = "a:b c\n"; `f2` = "a:b c\n"
- **Stdin:** ""
- **Expected:** stdout "a:b\na\n"; stderr empty; exit 0

```awk
{ print $1 }
```

| Implementation | Result | stdout | exit |
|---|---|---|---|
| mawk | pass |  | 0 |
| gawk --posix | pass |  | 0 |
| onetrue | pass |  | 0 |
| pyawk | pass |  | 0 |
| hawk | pass |  | 0 |

