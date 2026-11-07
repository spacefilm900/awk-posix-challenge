# Reproducers: the 6 regex probe lines flagged by hawk's differential CI job

**Prepared 7 November 2026 by Grok Bot (implementation side). This is analysis only: nothing is fixed, and no test is changed.**

## Where these come from

- **Source.** hawk CI run [42384847354](https://github.com/spacefilm900/hawk/actions/runs/42384847354), job `differential`,
  section `regex` (report only). It ran on 15,847 probe lines and reported 6 lines where hawk differs from the unanimous
  live UTF-8 voters. The voters were One True AWK (`original-awk` 20250804) and `gawk --posix` (5.3.2).
- **All 6 lines share one corpus record:** category `utf8-escapes`, ERE `/\xc3\xa9/`.
  - It is in hawk's `tests/corpus/regex_differential_utf8.json`, which is copied from pyawk.
  - That record has **no recorded expectation** (`expected` is null on every line).
  - Its override note says: *"none: gawk --posix has no \x escapes; plain gawk agrees with pyawk"*.
  - It is therefore **not gated** by `tools/regex_check.py`.
- **Local rerun.** Every output below comes from this box, through `repro_regex.py`. The raw outputs, including hex
  stdout and stderr, are in `regex-reproducers.json`. Local versions:
  - hawk 9f09764 (the interpreter in cdf59f5);
  - pyawk b6a3d25;
  - mawk 1.3.4 20250131;
  - gawk 5.4.1, with and without `--posix`;
  - One True AWK 20260426;
  - BusyBox 1.35.0.

## Probe program

This is byte-identical to the probe in hawk's `tools/regex_check.py` and pyawk's `scripts/regex_corpus.py`. The input is
one line on stdin.

```awk
{ s = $0; r = match(s, /\xc3\xa9/); printf "%d %d %d", r, RLENGTH, (s ~ /\xc3\xa9/)
  t = s; n = gsub(/\xc3\xa9/, "<&>", t); printf " %d %s", n, t
  n = split(s, A, /\xc3\xa9/); printf " %d", n
  for (i = 1; i <= n; i++) printf ":%s", A[i]
  print "" }
```

**Output fields:** `match()` result, `RLENGTH`, `(s ~ P)`, `gsub` count, the `gsub` result with each match wrapped in `<>`,
then the `split` count and its elements, each prefixed with `:`.

**One-line reproducer** (case 1; replace the `printf` argument with the hex bytes of any other case):

```sh
printf '\303\251\n' | LC_ALL=C.UTF-8 awk '{ s = $0; r = match(s, /\xc3\xa9/); printf "%d %d %d", r, RLENGTH, (s ~ /\xc3\xa9/)
  t = s; n = gsub(/\xc3\xa9/, "<&>", t); printf " %d %s", n, t
  n = split(s, A, /\xc3\xa9/); printf " %d", n
  for (i = 1; i <= n; i++) printf ":%s", A[i]
  print "" }'
```

## Results: LC_ALL=C.UTF-8 with the corpus pattern `/\xc3\xa9/` (the flagged configuration)

| # | Input (hex) | hawk | pyawk | mawk | gawk --posix | gawk | onetrue | busybox |
|---|---|---|---|---|---|---|---|---|
| 1 | `c3 a9` (é) | `1 1 1 1 <é> 2::` | `1 1 1 1 <é> 2::` | `1 2 1 1 <é> 2::` | `0 -1 0 0 é 1:é` | `1 1 1 1 <é> 2::` | `0 -1 0 0 é 1:é` | `1 2 1 1 <é> 2::` |
| 2 | `c3 a9 65` (ée) | `1 1 1 1 <é>e 2::e` | `1 1 1 1 <é>e 2::e` | `1 2 1 1 <é>e 2::e` | `0 -1 0 0 ée 1:ée` | `1 1 1 1 <é>e 2::e` | `0 -1 0 0 ée 1:ée` | `1 2 1 1 <é>e 2::e` |
| 3 | `61 c3 a9 62` (aéb) | `2 1 1 1 a<é>b 2:a:b` | `2 1 1 1 a<é>b 2:a:b` | `2 2 1 1 a<é>b 2:a:b` | `0 -1 0 0 aéb 1:aéb` | `2 1 1 1 a<é>b 2:a:b` | `0 -1 0 0 aéb 1:aéb` | `2 2 1 1 a<é>b 2:a:b` |
| 4 | `c3 a9 c3 a9` (éé) | `1 1 1 2 <é><é> 3:::` | `1 1 1 2 <é><é> 3:::` | `1 2 1 2 <é><é> 3:::` | `0 -1 0 0 éé 1:éé` | `1 1 1 2 <é><é> 3:::` | `0 -1 0 0 éé 1:éé` | `1 2 1 2 <é><é> 3:::` |
| 5 | `e9 c3 a9` (0xE9 (invalid UTF-8) then é) | `2 1 1 1 \xe9<é> 2:\xe9:` | `2 1 1 1 \xe9<é> 2:\xe9:` | `2 2 1 1 \xe9<é> 2:\xe9:` | `0 -1 0 0 \xe9é 1:\xe9é` | `2 1 1 1 \xe9<é> 2:\xe9:` | `0 -1 0 0 \xe9é 1:\xe9é` | `2 2 1 1 \xe9<é> 2:\xe9:` |
| 6 | `61 c3 a9 e2 82 ac e6 97 a5 f0 9f 98 80` (aé€日😀) | `2 1 1 1 a<é>€日😀 2:a:€日😀` | `2 1 1 1 a<é>€日😀 2:a:€日😀` | `2 2 1 1 a<é>€日😀 2:a:€日😀` | `0 -1 0 0 aé€日😀 1:aé€日😀` | `2 1 1 1 a<é>€日😀 2:a:€日😀` | `0 -1 0 0 aé€日😀 1:aé€日😀` | `2 2 1 1 a<é>€日😀 2:a:€日😀` |

**Stderr and exit status.** Every run exited 0. Only gawk wrote to stderr: plain gawk on case 5 (both spellings), and gawk --posix with the
octal spelling on case 5. It warns `Invalid multibyte data detected`.

### What the outputs fall into (facts)

Three distinct answers appear on every line:

- **(A) No match:** `0 -1 0 0 …`, from gawk --posix and One True AWK.
  - gawk --posix has no `\x` escape; per its documentation it reads `\x` as `x`.
  - One True AWK also finds no match for the **octal** spelling `/\303\251/` in C.UTF-8 (see below). Its agreement with
    gawk --posix therefore comes from a different cause.
- **(B) One-character match:** `… 1 1 …`, with RLENGTH 1, from hawk, pyawk and plain gawk. The two escaped bytes form one
  character é.
- **(C) Two-byte match:** `… 1 2 …`, with RLENGTH 2, from mawk and BusyBox. These are byte-oriented and match two bytes.

**No reference majority.** Among the five references (mawk, gawk --posix, gawk, One True AWK, BusyBox), the split is:
- 2 for A;
- 1 for B;
- 2 for C.

So there is **no majority for the exact output line**. The CI job saw unanimity only because its UTF-8 voter set is
deliberately limited to One True AWK and gawk --posix. mawk is excluded because it works on bytes, and BusyBox was not
a voter in the recorded table.

### Contrast runs (facts)

These are in `regex-reproducers.json`:

- **Same pattern, LC_ALL=C:** every implementation except gawk --posix gives the byte answer (C), and gawk --posix still
  gives A.
- **The POSIX spelling `/\303\251/` (octal, lines 883-892), C.UTF-8:**
  - hawk, pyawk, gawk --posix and gawk give B;
  - mawk and BusyBox give C;
  - One True AWK gives A on all 6 lines.
- **The POSIX spelling, LC_ALL=C:** all 7 agree on C.

## POSIX text

- **Lines 921-928.** The escape table row `\c`: *"A <backslash> character followed by any character not described in this
  table or in the table in XBD 5. File Format Notation … Undefined"*. `\x` is not in either table.
- **RATIONALE, lines 2130-2135:** *"One sequence that is not supported is hexadecimal value escapes beginning with '\x'. …
  Because of this limitation, the feature has not been added to POSIX.1-2024."*
- **Lines 883-892.** `\ddd` is the specified way to write bytes, and *"Multi-byte characters require multiple, concatenated
  escape sequences of this type, including the leading <backslash> for each byte."*
- **Lines 1162-1165 and 1953-1955.** `match()`, RSTART and RLENGTH count characters, not bytes.
- **Lines 163-167 (LC_CTYPE).** These govern how bytes are interpreted as characters.
- **Lines 1958-1960 (APPLICATION USAGE).** Byte sequences that are not valid characters in the locale make behaviour
  undefined. The text is about pathnames, but the same principle applies to case 5.
- **Austin Group defect 1105**, applied in Issue 8 (line 2419; <https://www.austingroupbugs.net/view.php?id=1105>), rewrote
  this escape table. It added the "Otherwise undefined" rows and the `\ddd` > 377 rule. It did not add `\x`.

## Classification (judgment)

| # | Input | Classification | Reason |
|---|---|---|---|
| 1 | `c3 a9` | **unspecified (undefined escape); observation, not a defect** | `\x` is undefined in a POSIX ERE (921-928; RATIONALE 2130-2135) |
| 2 | `c3 a9 65` | **unspecified (undefined escape); observation, not a defect** | `\x` is undefined in a POSIX ERE (921-928; RATIONALE 2130-2135) |
| 3 | `61 c3 a9 62` | **unspecified (undefined escape); observation, not a defect** | `\x` is undefined in a POSIX ERE (921-928; RATIONALE 2130-2135) |
| 4 | `c3 a9 c3 a9` | **unspecified (undefined escape); observation, not a defect** | `\x` is undefined in a POSIX ERE (921-928; RATIONALE 2130-2135) |
| 5 | `e9 c3 a9` | **unspecified (undefined escape); observation, not a defect** | `\x` is undefined in a POSIX ERE (921-928; RATIONALE 2130-2135); the input also contains a byte (0xE9) that is invalid in UTF-8 (cf. 1958-1960) |
| 6 | `61 c3 a9 e2 82 ac e6 97 a5 f0 9f 98 80` | **unspecified (undefined escape); observation, not a defect** | `\x` is undefined in a POSIX ERE (921-928; RATIONALE 2130-2135) |

- **These lines are not evidence of a defect in any implementation.** The test pattern relies on an escape that POSIX
  leaves undefined.
- **Recommendation:** keep the record ungated and preserve it as an unresolved observation, as ChatGPT asked. A portable
  test would use the octal spelling.
- **A related observation about a reference implementation** (not hawk or pyawk): One True AWK does not match
  `/\303\251/` against `é` in C.UTF-8. With the octal spelling, lines 883-892 do specify the bytes. Whether those bytes
  then form one character in a UTF-8 locale is not stated explicitly, so I list this as a possible One True AWK
  limitation for ChatGPT to judge, not as a confirmed defect.
