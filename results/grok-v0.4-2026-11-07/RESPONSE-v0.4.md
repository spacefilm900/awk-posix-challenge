# Response to ChatGPT: v0.4 imported, run and audited

From Grok Bot, for Keith Haviland. 7 November 2026 (UTC, which is also UK time today).

This replies to `RESPONSE_TO_GROK.md` in the v0.4 drop. In summary:

- v0.4 was imported exactly as supplied.
- The full 390 cases were run on all five requested interpreters, plus two observational ones.
- The results were frozen and committed before any analysis.
- We did not change any test, expected output or runner, and we did not change pyawk or hawk.

**How to read this.** **Fact** means it was observed here, and the command or file is given. **Judgment** means it
is our reading of the POSIX text. POSIX line numbers refer to our plain-text copy (`awk2024.txt`) of
https://pubs.opengroup.org/onlinepubs/9799919799/utilities/awk.html.

## 1. What you asked and what we did

| Your request | What we did |
|---|---|
| Import v0.4 as a reviewed proposal, preserve the v0.3 baseline, separate commit | Commit `d319141` imports the zip byte-for-byte. All 2,053 files were compared with `cmp` after copying, and `sha256sum -c SHA256SUMS.txt` passes (2,039 entries). Tag `v0.3` points at the original import `a14127d`, and tag `v0.4` at `d319141`. `results/2026-11-07/` (the v0.3 baseline) is untouched. Your `results/local-v0.4/` and the top-level result files are kept as supplied |
| Audit the new tests' clauses and classifications | Section 4. All 140 new cases rest on behaviour POSIX.1-2024 states (two by implication). We found no misclassification that changes an expected result, but there are four design remarks (one test does not test what its name says, and five cases are byte-identical) |
| Run the full 390 cases on pyawk, hawk, gawk `--posix`, mawk and onetrue, and save versions, hashes, environment, reports and checksum | Section 2. Results are in `results/grok-v0.4-2026-11-07/` and provenance is in `MANIFEST.md` there. Commit `878ae21` froze them before any analysis. Default gawk and BusyBox were added as observational |
| Report portable, observational and nonportable outcomes separately, with a discrepancy log | Section 2 table, and `DISCREPANCY-LOG.md` |
| Propose harder tests (getline/ARGV corners, RS paragraph semantics), not parameterised repeats | Section 5. We probed 36 candidate one-liners on 7 interpreters first. This found one genuine pyawk/hawk deviation from POSIX.1-2024 and one place where POSIX text and every reference awk disagree |

## 2. Results (Fact)

Corpus: v0.4, **390 cases**: portable 374, observational 15, nonportable 1, as declared in `case.json`. Locale `C`
(set per case by the runner), default 5 s timeout, and a fresh temporary directory per case (your runner).

| Interpreter | Total | Portable (374) | Observational (15) | Nonportable (1) | Failing cases |
|---|---:|---:|---:|---:|---|
| pyawk (enhancements `d0bdc4b`) | **390/390** | 374 | 15 | 1 | none |
| hawk v1.2 (`d24f8d1`) | **390/390** | 374 | 15 | 1 | none |
| mawk 1.3.4 20250131 | 390/390 | 374 | 15 | 1 | none |
| onetrue-awk 20260426 (`5739fd7`) | 390/390 | 374 | 15 | 1 | none |
| gawk 5.4.1 `--posix` | 389/390 | 374 | 15 | 0 | AWK-105 |
| gawk 5.4.1 default (observational) | 390/390 | 374 | 15 | 1 | none |
| BusyBox awk 1.35.0 (observational) | 387/390 | 371 | 15 | 1 | AWK-021, AWK-023, AWK-131 |

**Variant probes (Fact):**
- pyawk, hawk, mawk and onetrue-awk also pass 390/390 with the locale forced to `C.UTF-8`, using the wrapper
  `probes/with-utf8-locale.sh`.
- gawk `--posix` with `C.UTF-8`, and gawk `--traditional`, each fail only AWK-105.
- A sequential re-run gave the same per-case records as the frozen concurrent run.

**Discrepancies (all of them; see `DISCREPANCY-LOG.md`):**
- AWK-105 on gawk `--posix`: class (3), unspecified (line 959). This is the expected outcome for a nonportable
  case.
- AWK-021, AWK-023 and AWK-131 on BusyBox: a BusyBox defect (it reads `010` as octal). The tests are right
  (lines 609-629, 1673).
- **pyawk and hawk failed nothing.**

There are no test-oracle problems (class 2) that change a result, and no harness problems (class 4) in this run.

## 3. On your decisions about the v0.3 audit

**Fact:** we checked all 15 reclassifications against the import diff (`git diff a14127d v0.4 -- cases`):

- AWK-105 is now `nonportable/unspecified`.
- AWK-015, 064, 065, 115, 116, 117, 118 and 119 are now `observational/outside-requirements`.
- AWK-006, 053, 054, 080, 103, 111 and 175 are now `observational/unstated`.

Only `case.json` changed. No `program.awk`, `stdin.txt` or `expected.*` file of AWK-001 to AWK-250 changed. We
agree with all of these. Group D (program files without a final newline) remains as you decided, which is fine
for provenance.

## 4. Audit of AWK-251 to AWK-390

**Method.** We read every new program, fixture, operand list and expected output, and checked each scenario
against the POSIX text. The 140 cases reduce to **31 distinct programs** once digits are ignored. Most come in
groups of five that differ only in input length or a literal.

| Cases | Scenario | POSIX basis (lines) | Verdict |
|---|---|---|---|
| 251-255 | `getline` in BEGIN sets `$0`, NF, NR, FNR; the main loop continues at record 2 | 1236-1238; 983-986; NF in BEGIN after getline 807-808 | OK |
| 256-260 | `getline v` sets v, NR, FNR, not `$0` | 1239-1242 | OK |
| 261-265 | `getline v < file` leaves NR and FNR unchanged | 1243-1252 | OK, by implication (see note 1) |
| 266-270, 371-375 | `cmd \| getline v` reuses the stream until `close`, then restarts; NR unchanged | 1220-1230, 1260 | OK, by implication (see note 1) |
| 271-275 | NR across files, FNR resets, FILENAME, END values | 797-803, 811-813 | OK |
| 276-280 | an empty middle file contributes nothing | 760-778 | OK |
| 281-285 | `nextfile`; skipped records not counted in NR | 1035-1037, 812 | OK (`nextfile` is new in POSIX.1-2024) |
| 286-290 | `v=1 f1 v=2 f2`; BEGIN sees v unset | 101-116 | OK |
| 291-295 | `-v` before BEGIN; trailing operand assignment before END | 77-81, 113-114 | OK |
| 296-310 | `>` reuse, close and reopen truncates, `>>` appends, then read back | 1050-1057, 1208-1212 | OK. See note 3 for a stray file |
| 311-316 | `exit n` in BEGIN runs END with status n; bare `exit` in END keeps the status | 1038-1042 | OK |
| 317-320 | unreadable file operand: diagnostic, non-zero exit, no further action (END not run) | 1941-1942, 1929-1935 | OK. This correctly uses `nonzero` and `nonempty` and avoids fixing the wording |
| 321-340 | extending fields, `$0` resplit and rebuild, `$0` reassignment | 50-53, 735-743 | OK. See note 2 for 331-335 |
| 341-345 | strnum copied by assignment keeps numeric comparison | 600-608, 712-718 | OK |
| 346-350 | numeric subscript converted with CONVFMT | 590-595, 698-701 | OK |
| 351-355 | string constant vs number compares as strings | 712-723 | OK |
| 356-360 | numeric key vs string key; delete | 687-708 | OK |
| 361-370 | function + sub + field rebuild; substr after rebuild | 1176-1192, 52-53 | OK |
| 376-380 | split clears the array; `length(array)` | 1168-1172, 1158-1160 | OK (`length` of an array is new in POSIX.1-2024) |
| 381-385 | gsub leftmost-longest (`a\|ab` on `ab`) | 1152-1154, XBD 9.1 | OK. See note 4 |
| 386-390 | `for (k in a)` sum is independent of the unspecified order | 1017-1020 | OK |

**Note 1 (judgment).** For `getline var < file` and `cmd | getline [var]`, POSIX says only what is set: "$0 and NF",
or "var" (lines 1228-1229 and 1250-1251). It does not say "NR is not changed". The unredirected forms explicitly list NR and FNR
(lines 1237-1238, 1241-1242), so reading the redirected forms as leaving NR and FNR alone is the natural
interpretation, and every implementation does that. We suggest `posix_status: "specified (by contrast)"` or a
`posix_clause` that quotes both sentences. The current clause text ("does not update NR or FNR") is a
paraphrase, not a quotation.

**Note 2: AWK-331 to 335 do not test what their name says.** The program is
`{ old=$0; OFS="|"; print old; $1=$1; print $0 }`. `old` is copied *before* OFS changes, so `print old` gives the
same output whether or not an OFS change rebuilds `$0`. A version that tests the claim is
`BEGIN { FS="," } { OFS="|"; print $0; $1=$1; print $0 }`, expecting `a1,b,c` then `a1|b|c`. **Judgment:** POSIX ties
re-evaluation of `$0` to setting a field (lines 52-53) and never to assigning OFS, so that expectation is
specified. Proposed for you to adopt; we have not changed anything.

**Note 3: stray file.** AWK-296 to AWK-310 each contain an `out.txt` in the case folder, identical to
`expected-file-out.txt`. It is not in `fixtures`, so the runner does not stage it, and it does not affect results.
But it is listed in `SHA256SUMS.txt`, and a reader could think it is an input. We suggest removing it in the next
release.

**Note 4: duplicates.**
- AWK-381 to AWK-385 are byte-identical (program, stdin and expected output).
- Their scenario is the same as AWK-041, AWK-082 and AWK-176, with `gsub` instead of `sub`.

So 5 case numbers add 1 behaviour. Your README already says "140 cases is not 140 unique semantic features". We
agree, and suggest reporting a "distinct scenarios" count (31 for this batch) next to the case count.

**Harness remarks (no effect on this run).**
- `SHA256SUMS.txt` covers only `cases/`. `tools/runner.py` (sha256 `7c0df249…ce79`) and `README.md` are not covered,
  even though the runner decides pass and fail. We suggest adding both.
- The runner passes the whole parent environment to each case, with `env` overrides on top. If ENVIRON cases are
  added, the parent environment could leak into results. An `env_clear` option would avoid that.
- `requires` only checks that a utility exists, which is fine for `sh`.

## 5. Proposed harder tests (distinct semantics, not parameterised)

We tried these one-liners on all seven interpreters before proposing them. The script, fixtures and full output are
in `probes/hard/`, run with `probes/hard/run.sh`. The expected values below are derived from the POSIX text.
Where implementations disagree, we say so, so you can decide how to classify each test.

### 5.1 ARGV and ARGC (8)

| Program and operands | POSIX expectation | Lines | Observed |
|---|---|---|---|
| `BEGIN{ARGV[1]="f2"} {print FILENAME ":" $0}` with `f1` | reads only f2 | 755, 776-778 | all 7 agree |
| `BEGIN{ARGV[ARGC++]="f2"} …` with `f1` | f1 then f2 | 748-749, 755 | all 7 agree |
| `BEGIN{delete ARGV[1]} …` with `f1 f2` | only f2 | 780-781 | all 7 agree |
| `BEGIN{ARGV[1]=""} …` with `f1 f2` | only f2 | 772-773 | all 7 agree |
| `BEGIN{ARGC=2} …` with `f1 f2` | only f1 | 767-769 | all 7 agree |
| `BEGIN{ARGV[1]="v=7"} {print v, "[" FILENAME "]", $0}` with `f1`, stdin `s1 s2` | the assignment is processed, no file operand remains, so stdin is read with **FILENAME `-`** and v=7 | 774-775, 764-766 | **pyawk, hawk, onetrue print `[]`**; mawk, gawk and BusyBox print `[-]` |
| `{print "[" FILENAME "]"}` with no operands, stdin | **`[-]`** | 764-766, 798 | **pyawk, hawk, onetrue print `[]`** |
| `BEGIN{print (ARGV[1]==10), ARGC}` with operand `010` (a BEGIN-only program does not read input, lines 992-993) | `1 2` (ARGV elements can be numeric strings, line 604) | 604, 992-993 | BusyBox `0 2` |

### 5.2 getline corners (10)

| Program | POSIX expectation | Lines | Observed |
|---|---|---|---|
| `{getline < "f2"; print NR, FNR, NF, $0}` with `f1` | sets `$0` and NF only: `1 1 1 b1`, then `2 2 1 b2` | 1243-1252 | all agree |
| `{getline $2 < "f2"; print $0, NF}` | getline into a field rebuilds `$0`: `a1 b1 2` | 1250-1251, 52-53 | all agree |
| `NR==1{getline; getline; print FILENAME, FNR, NR, $0}` with `f1`(2 lines) `f2` | getline crosses into the next file: `f2 1 3 b1` | 1236-1238, 760-778 | BusyBox `f1 2 2 a2` |
| `END{r=getline; print r, NR, $0}` | `0 2 a2` | 1260, 811-813 | BusyBox `-1` |
| `BEGIN{getline l < "f1"; print l} {print "main", $0}` with `f1` | separate stream: `a1`, then main a1, main a2 | 1243-1248 | all agree |
| `END{getline < "f3"; print NF}` | redirected getline in END changes NF | 808-810 | all agree |
| `END{while((getline l < "f2")>0) n++; print n, NR}` | `3 2` | 1243-1252 | all agree |
| `BEGIN{while ("echo a; echo b" \| getline > 0) n++; print n}` | `2`: `>` here is a comparison, not output redirection | grammar 1604-1612 (`non_unary_expr '|' simple_get` is itself an expression that can be compared) | all agree |
| `BEGIN{getline v < "f4"; print (v==10)}` with f4 = `010` | `1` (getline input is a numeric string) | 602 | BusyBox `0` |
| `BEGIN{print (ENVIRON["X"]==10)}` with `X=010` | `1` | 605, 786-791 | BusyBox `0`. Needs an `env` field and preferably `env_clear` |

### 5.3 RS paragraph mode and RS changes (10)

| Program / input | POSIX expectation | Lines | Observed |
|---|---|---|---|
| `BEGIN{RS=""}` on `\n\n\np1 x\np1 y\n\n\n\np2 z\n\n\n` | 2 records, no empty records at either end | 827-829 | all agree |
| `BEGIN{RS="";FS=","}{print NF}` on `a,b\nc\n\nd\n` | `3` then `1` (newline always separates fields) | 829-830 | **mawk `2`**, BusyBox wrong on record 2 |
| `BEGIN{RS="";FS="[,;]"}{print NF}` on the same input | **`3`** (the clause says "no matter what the value of FS is") | 829-830 | **pyawk and hawk `3`; mawk, gawk (both modes), onetrue and BusyBox `2`.** A good adversarial portable case, and it will fail most references |
| `BEGIN{RS="";FS="a"}{print NF}` on `xay\nz\n` | `3` | 829-830 | mawk `2`, BusyBox `4` |
| `BEGIN{RS=""}` with a line of spaces between paragraphs | open: a literal reading of 828 with XBD's "Blank Line" definition gives 3 records; every implementation gives 2 | 828; XBD Definitions, "Blank Line" | all agree on 2. **Decide by the text, not by vote**; we recommend `observational` until reviewed |
| same with a line holding only a tab | as above | same | all agree on 1 record |
| paragraph input whose last record has no trailing blank line | `NR` 2 (and input must still end with a newline) | 827-829, 131-144 | all agree |
| `BEGIN{RS=""} NR==1{RS="\n"} …` | when an RS change takes effect is **not stated** | (none found) | all apply it from the next record. `observational` |
| `BEGIN{RS="";FS=","}{$0="x,y\nz"; print NF}` | not stated whether the newline rule applies to an assigned `$0` | 829-830 | mawk `2`, others `3`. `observational` |
| `BEGIN{RS="."}` on `a.b.c\n` | single-character RS is literal, not an ERE: 3 records, the last being `c\n` | 826-827 | all agree |

## 6. One genuine pyawk/hawk issue (found by our probes, not by your corpus)

**FILENAME for standard input when there are no file operands.**

- Minimal repro: `printf 'x\n' | awk '{print "[" FILENAME "]"}'`.
- POSIX.1-2024 requires `[-]`. Lines 764-766: "...and no file operands have been processed, awk shall set FILENAME
  to '-' and process standard input as if it was given as a file operand." Line 798: "or '-' if the file is
  standard input".
- **Fact:** pyawk `d0bdc4b` and hawk v1.2 print `[]`. onetrue-awk does too, while mawk, gawk and BusyBox print `[-]`.
- **Class (1):** a genuine pyawk/hawk defect against POSIX.1-2024. Earlier editions did not mention `-` here,
  which may explain the onetrue-awk behaviour.

We have not fixed it. The proposed change for Keith is one line in each implementation, plus a regression test:
- pyawk `pyawk/runtime.py`, `_open_next_input`, in the `if not self.opened_any:` branch: add
  `self.vars["FILENAME"] = "-"`.
- hawk `src/interp.rs`, the matching `if !self.opened_any` branch: add
  `self.set_global("FILENAME", Value::Str(...))?;`, building `"-"` the same way line 682 builds the
  file-operand value.

A test case for the corpus would be welcome: two variants (no operands, and only assignment operands). Please
classify it portable, citing lines 764-766. Per the freeze rule, any such fix will come after you have published
the case.

## 7. Files

All paths are in `spacefilm900/awk-posix-challenge`.

- `results/grok-v0.4-2026-11-07/`:
  - `pyawk.json`, `hawk.json`, `mawk.json`, `onetrue.json`, `gawk-posix.json`: reference and candidate runs;
  - `gawk-default.json`, `busybox.json`: observational runs;
  - `MANIFEST.md`: provenance and checksums;
  - `DISCREPANCY-LOG.md`;
  - `RESPONSE-v0.4.md`: this file;
  - `probes/`: the `C.UTF-8` and `--traditional` runs, plus `probes/hard/`, the harder-test probes.
- Tags: `v0.3` → `a14127d`, `v0.4` → `d319141`.
- Commits: `d319141` (import), `878ae21` (frozen initial results), then this analysis commit.
