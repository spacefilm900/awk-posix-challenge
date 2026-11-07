# Response to the v0.3 review: deliverables (a) to (e)

Prepared by Grok Bot for Keith Haviland, for the author of the Independent POSIX AWK Challenge. 7 November 2026.

This answers the five requests in "Review of v0.3 results and instructions for the next phase". Nothing under
`cases/`, `tools/`, `SHA256SUMS.txt` or `README.md` has been changed. Every change to the tests is offered as a
proposal for the challenge author to accept, change or reject.

**How to read this document.** Statements marked **Fact** were observed on our machine; the command that shows them
is given. Statements marked **Judgment** are our reading of the POSIX text, and the author may disagree with them.
POSIX citations give the line number in our plain-text copy of the POSIX.1-2024 awk page (`awk2024.txt`, 2,456 lines,
taken from https://pubs.opengroup.org/onlinepubs/9799919799/utilities/awk.html). Line numbers are a
locator only; the quoted wording is what matters.

## Summary

- (a) A metadata-only patch for AWK-105 is in section (a) and in `proposed-AWK-105.patch`. The program, input and
  expected output are kept. `SHA256SUMS.txt` would need its AWK-105 `case.json` line updated.
- (b) A proposed v0.3.1 changelog entry is in section (b).
- (c) Audit result: apart from AWK-105, **no case has an expected result that POSIX explicitly calls unspecified,
  undefined or implementation-defined.** We do flag two smaller groups for the author to decide on: 8 cases whose
  standard input is not a POSIX "text file" (group B), and 7 cases that rely on behaviour POSIX does not state at all
  (group C: assigning to `NF`, and a function's value when no `return` value is given). Separately, all 50
  `program.awk` files of AWK-001 to AWK-050 lack a final newline (group D, hygiene only). In every probe we ran, all
  of these cases passed on every interpreter tested.
- Variant probes (14 interpreter/locale combinations x 250 cases): **pyawk and hawk never disagreed with mawk,
  onetrue-awk or default gawk.** They differ from gawk `--posix`/`--traditional` only on AWK-105, as mawk and
  onetrue-awk do. BusyBox awk 1.35.0 fails AWK-021, AWK-023 and AWK-131. Those three cases are fine; BusyBox reads
  `010` as octal, which POSIX does not allow.
- (d) The baseline manifest is `results/2026-11-07/MANIFEST.md`. All five interpreters were re-run, and every result
  matches the stored JSON.
- (e) A 140-case plan for the next tranche is in section (e), with the `case.json` fields and runner support it would
  need.

---

## (a) Proposed AWK-105 metadata patch

**Problem.** AWK-105 (`fs-char-split`) runs `BEGIN{FS=""}{print NF ":" $1 ":" $3}` on `abc` and expects `3:a:c`.
POSIX.1-2024, awk, EXTENDED DESCRIPTION, Regular Expressions, in the list of FS behaviours (awk2024.txt line 959):

> "If FS is a null string, the behavior is unspecified."

**Alternative behaviour (Fact).** `LC_ALL=C /workspace/refs/local/bin/gawk --posix -f cases/AWK-105/program.awk < cases/AWK-105/stdin.txt`
prints `1:abc:`. The whole record is one field, so `NF=1`, `$1=abc` and `$3` is empty. gawk 5.4.1 `--traditional`
does the same. pyawk, hawk, mawk, onetrue-awk, BusyBox awk and gawk without `--posix` all print `3:a:c`, in both
`C` and `C.UTF-8`. Both results are allowed by POSIX.

**Proposal.** Change only the metadata: `classification` goes from `portable` to `nonportable`, and new fields
record the extension, the POSIX clause, the alternative result and the history. `program.awk`, `stdin.txt`,
`expected.stdout` and `expected.stderr` stay byte-for-byte the same. Field names are suggestions; see (c)4 for a
schema that would apply to every case.

```diff
--- a/cases/AWK-105/case.json
+++ b/cases/AWK-105/case.json
@@ -6,6 +6,19 @@
   "specification_url": "https://pubs.opengroup.org/onlinepubs/9799919799/utilities/awk.html",
   "note": "Expected output independently specified; review ambiguous POSIX cases before treating disagreements as defects.",
   "expected_exit": 0,
-  "classification": "portable",
+  "classification": "nonportable",
+  "extension": "empty-fs-splits-characters",
+  "posix_status": "unspecified",
+  "posix_clause": "If FS is a null string, the behavior is unspecified.",
+  "posix_reference": "POSIX.1-2024 (IEEE Std 1003.1-2024), awk, EXTENDED DESCRIPTION, Regular Expressions, list of FS behaviours, first item",
+  "expected_behaviour": "Common extension: with FS set to the null string, each character of the record becomes a separate field (abc -> NF=3, $1=a, $3=c).",
+  "alternative_behaviours": [
+    {
+      "observed_in": "gawk 5.4.1 --posix and gawk 5.4.1 --traditional",
+      "stdout": "1:abc:\n",
+      "description": "The whole record is a single field (NF=1, $1=abc, $3 empty). This is permitted because POSIX leaves a null FS unspecified."
+    }
+  ],
+  "history": "v0.3.1: reclassified from portable to nonportable (extension-sensitive). Program, stdin and expected output unchanged. Reason: the expected result depends on behaviour POSIX.1-2024 explicitly leaves unspecified; gawk --posix produces a different, permitted result. Reported in the 2026-11-07 run review.",
   "locale": "C"
 }
```

The patch applies cleanly to commit `a14127d` (checked with `git apply --check`, not applied). Because
`SHA256SUMS.txt` lists `case.json` files, the author would also update one line:

```text
- 6502dc101e81ee3f60566eb428b4d5177cd4b194357248e6f39e141200a4d584  cases/AWK-105/case.json
+ a7254d43db1c330ba8c417a60053779b5dc0b34986eeae55be7ef336dc70cf57  cases/AWK-105/case.json
```

Note that `tools/runner.py` never reads `classification` (Fact: it uses only `id`, `name`, `group`, `locale` and
`expected_exit`). Until the runner or the reports use that field, AWK-105 will still count in the single pass total.
Section (c)4 proposes how to report the classes separately.

## (b) Proposed v0.3.1 changelog entry

```markdown
## v0.3.1 (proposed, 2026-11-07)

Metadata-only correction. No program, input or expected output changed.

- AWK-105 (fields/fs-char-split): reclassified from `portable` to `nonportable` (extension-sensitive).
  POSIX.1-2024 awk says "If FS is a null string, the behavior is unspecified." The expected output
  (`3:a:c`, one field per character) is the common extension and is kept for opted-in extension testing.
  gawk 5.4.1 --posix prints `1:abc:` (one field), which POSIX also permits. Reported in the 2026-11-07 run review
  (results/2026-11-07/SUMMARY.md). The case.json gains `extension`, `posix_status`, `posix_clause`,
  `posix_reference`, `alternative_behaviours` and `history` fields.
- SHA256SUMS.txt: the AWK-105 case.json line updated. All other lines unchanged.
- Portable-success subset: 249 cases (AWK-001 to AWK-250 except AWK-105). On 2026-11-07 all 249 passed pyawk
  (d0bdc4b), hawk v1.2 (d24f8d1), mawk 1.3.4 20250131, onetrue-awk 20260426 and gawk 5.4.1 --posix. That means
  the five agree on this suite. It does not certify any of them as POSIX-conformant.
- The 2026-11-07 portability audit (results/2026-11-07/RESPONSE-v0.3-review.md) found no other case that
  depends on behaviour POSIX marks unspecified, undefined or implementation-defined. Open questions on 8 cases
  that use non-text input and 7 that rely on behaviour POSIX does not state are listed there for a decision in a
  later release. They are not changed in v0.3.1.
```

If the author also accepts any group B, C or D recommendation below, add a bullet for each one. Those changes would
alter case files or hashes, so they belong in v0.3.2 or v0.4 rather than in a metadata-only v0.3.1.

## (c) Portability audit of the other 249 cases

### (c)1 Method

1. **Read every case.** We read `program.awk`, `stdin.txt` (bytes, including whether it ends in a newline),
   `expected.stdout` and `case.json` for all 250 cases.
2. **Map each case to the POSIX text.** For each case we wrote down which POSIX statements its expected output
   depends on and checked that the awk page states those statements. That page is POSIX.1-2024, with XBD
   definitions for "text file" and "line". Appendix A lists every case with its topic and line references.
3. **Search for risky features (Fact).** We grepped all 250 programs for features where POSIX leaves room:
   `srand`/`rand`, `ENVIRON`, `getline` with `<` or `|`, `close`, `system`, `%c`, `OFMT`, `CONVFMT`, `RS=""`,
   `length` without parentheses, whole-array `delete`, `substr` with a start below 1 or non-integer arguments,
   division, `int`, hexadecimal constants, `inf`/`nan` strings, output redirection, `nextfile`, `FILENAME`,
   `ARGV`, `-v`. **None of these appears in any case.** The corpus uses only plain `getline` and `getline var`
   (AWK-017, AWK-018), `exit 0` (AWK-220), assignments to `NF` (5 cases) and `FS=""` (AWK-105).
4. **Grepped the POSIX text for every use of "unspecified", "undefined" and "implementation-defined"** (56 lines, 46 of them in the normative text before the informative sections) and
   checked each one against the cases.
5. **Variant probes, used to find fragile cases only.** We re-ran every case under 14 interpreter/locale
   combinations (section (c)2). The verdicts come from the POSIX text, not from how many interpreters agree. A
   case that every interpreter passes can still be flagged, and a case one interpreter fails can still be correct.

### (c)2 Demonstrated facts: variant probes

Script: `results/2026-11-07/probes/variant_probe.py` (it does not use `runner.py`, and it compares stdout, stderr
and exit code exactly against the frozen expectations). Output: `probes/variant_probe_summary.txt`. Run with
`python3 results/2026-11-07/probes/variant_probe.py`.

| Variant | Locale | Passed | Failing cases |
|---|---|---:|---|
| pyawk (d0bdc4b) | C | 250 | none |
| pyawk | C.UTF-8 | 250 | none |
| hawk v1.2 | C | 250 | none |
| hawk v1.2 | C.UTF-8 | 250 | none |
| mawk 1.3.4 20250131 | C | 250 | none |
| mawk | C.UTF-8 | 250 | none |
| onetrue-awk 20260426 | C | 250 | none |
| onetrue-awk | C.UTF-8 | 250 | none |
| gawk 5.4.1 `--posix` | C | 249 | AWK-105 |
| gawk 5.4.1 `--posix` | C.UTF-8 | 249 | AWK-105 |
| gawk 5.4.1 `--traditional` | C | 249 | AWK-105 |
| gawk 5.4.1 (default) | C | 250 | none |
| gawk 5.4.1 (default) | C.UTF-8 | 250 | none |
| BusyBox awk 1.35.0 (static musl build) | C | 247 | AWK-021, AWK-023, AWK-131 |

- **pyawk and hawk:** no disagreement with any reference interpreter under any variant. Their only difference from
  any reference is AWK-105 against gawk `--posix`/`--traditional`, and mawk and onetrue-awk differ there in the
  same way.
- **BusyBox (Fact):** given the field `010`, BusyBox prints `0 1 0` for `($1==10), ($1<11), ($1>9)` (AWK-021),
  `1 0` for AWK-023 and `0:1` for AWK-131. It treats the numeric string `010` as octal 8.
  **Judgment:** the cases are right and BusyBox is wrong. POSIX allows only two ways to recognise a numeric string
  (lines 609-629), and both give decimal 10. Way (a) uses `strtod`, which reads `010` as decimal. Way (b) uses the
  awk NUMBER token, and line 1673 says a sequence of digits "shall be evaluated as an integer constant in decimal".
- **Locale:** every input is ASCII, so as expected `C.UTF-8` changed no result. The cases whose results could depend
  on the locale (string `<` uses collation in AWK-132, `tolower`/`toupper`, `[[:digit:]]`) are pinned to `C` by
  `case.json`, which is correct.

### (c)3 Flagged cases

Only group A has a POSIX statement that the behaviour is unspecified. Groups B and C are questions for the author
to decide. Group D is hygiene.

#### Group A: expected result depends on explicitly unspecified behaviour (1 case)

| Case | Reason | POSIX clause |
|---|---|---|
| AWK-105 fs-char-split | `FS=""` splitting into characters is an extension; gawk `--posix` gives one field | "If FS is a null string, the behavior is unspecified." (line 959) |

Recommendation: the patch in (a).

#### Group B: standard input is not a POSIX text file (8 cases)

POSIX awk, INPUT FILES (lines 131 and 137):

> "Input files to the awk program from any of the following sources shall be text files: ... Standard input in the absence of any file operands, or their equivalents"

and (lines 143-144):

> "Whether the variable RS is set to a value other than a <newline> or not, for these files, implementations shall support records terminated with the specified separator up to {LINE_MAX} bytes and may support longer records."

XBD 3.387 defines a text file as "A file that contains characters organized into zero or more lines", and XBD 3.185
defines a line as "A sequence of zero or more non-<newline> characters plus a terminating <newline> character". A
file whose last byte is not a newline ends with what XBD 3.172 calls an "Incomplete Line", so it is not a text file.

**Fact** (`od -c cases/AWK-0NN/stdin.txt`): these eight inputs do not end in a newline.

| Case | stdin bytes | What the expectation assumes |
|---|---|---|
| AWK-065 final-unterminated | `a\nb` | the incomplete last line `b` is a record |
| AWK-115 multiple-records-last-no-nl | `aa bb\ncc dd` | the incomplete last line is a record |
| AWK-015 rs-single-char | `ab:cd:ef` (RS=":") | the last record, not ended by RS, is a record |
| AWK-117 rs-single-char-not-found | `hello` (RS=";") | as AWK-015 |
| AWK-064 custom-rs | `aa;bb;cc;` (RS=";") | the file has no newline at all |
| AWK-116 custom-rs-colon | `ab:cd:ef:` (RS=":") | as AWK-064 |
| AWK-118 rs-leading-delimiter | `;abc;` (RS=";") | as AWK-064 |
| AWK-119 rs-repeated-delimiters | `a;;b;` (RS=";") | as AWK-064 |

**Judgment.** Strictly, POSIX does not say what awk does with these inputs, so none of the eight expected outputs is
required. In practice every interpreter we tried (all 14 variants) gives the expected output. The risk that a
conforming awk behaves differently is low but real. For AWK-065 and AWK-115 it is the very behaviour being tested.

**Options for the author.**
1. Reclassify AWK-065 and AWK-115 as `nonportable`, with `posix_status: "outside-requirements"` and the clause
   above. Their purpose is to test the incomplete last line, which POSIX does not cover.
2. For the six RS cases, the clean portable form is an input that ends in a newline, with the expected output
   adjusted for it. For example, AWK-064 with input `aa;bb;cc;\n` would give a fourth record consisting of a single
   newline, so `print NR ":" $0` would print `4:` followed by that newline and then ORS. Changing the input changes
   the test, so this is a new-case decision for the author, and we have not done it.
3. Or keep all eight as they are, add `"input_text_file": false` to their metadata, and report them in a
   "common behaviour" class alongside the portable class.

#### Group C: relies on behaviour POSIX does not state (7 cases)

Here POSIX says nothing either way. Every implementation we tried agrees, but the result rests on historical
consensus rather than a POSIX statement.

| Case(s) | What is relied on | POSIX text and what it leaves out |
|---|---|---|
| AWK-006 nf-truncate, AWK-054 lower-nf, AWK-103 assign-nf-zero | Assigning a smaller value to `NF` discards the fields after it and rebuilds `$0` with OFS | The only description of NF is at lines 806-810: "The number of fields in the current record. Inside a BEGIN action, the use of NF is undefined unless ... Inside an END action, NF shall retain the value it had for the last record read ...". Nothing in the awk page says what assigning to NF does. **Fact:** `grep -n -w NF awk2024.txt` finds no other description. |
| AWK-053 increase-nf, AWK-111 nf-shrink-and-extend | Assigning a larger value to `NF` creates empty fields (and, in AWK-111, shrinking first discards `b` and `c`) | Same as above. Only assigning to a *field* past `$NF` is specified (lines 739-741: "assigning to a nonexistent field ... shall increase the value of NF; create any intervening fields with the uninitialized value; and cause the value of $0 to be recomputed, with the fields being separated by the value of OFS"). |
| AWK-080 return-default, AWK-175 function-return-default | A function that ends without running `return` returns the uninitialized value (prints as empty) | Line 1279: "The return statement can be used to return a value." The grammar (line 1416) has `Return expr_opt`. The page never says what value a call has when no return expression is evaluated. |

**Judgment.** We would keep these 7 cases. The behaviour is universal, and these tests are useful because a new
implementation could easily get it wrong. We recommend marking them `posix_status: "unstated"`, so that a failure
is read as "differs from historical practice" rather than "violates POSIX". The gawk manual says the same about
both topics. It warns that some versions of awk do not rebuild `$0` when NF is decreased, and that with no return
value "the returned value is undefined". That is outside evidence, not POSIX.

#### Group D: corpus hygiene, not an expected-result problem (50 program files)

**Fact:** none of the `program.awk` files of AWK-001 to AWK-050 ends in a newline. All of AWK-051 to AWK-250 do.
Command: `for c in cases/AWK-*; do tail -c1 $c/program.awk | od -An -tx1; done`. POSIX lines 145-147:

> "If -f progfile is specified, the application shall ensure that the files named by each of the progfile option-arguments are text files and their concatenation, in the same order as they appear in the arguments, is an awk program."

**Judgment:** strictly, these 50 programs are not text files, so the test, as the application, does not meet a
POSIX requirement. No interpreter we tried is affected. We suggest adding a final newline to each of these 50
program files in a future release. That changes 50 hashes, so it is a release-level decision for the author.

### (c)4 Checked and not flagged (for the record)

- **SUBSEP default is implementation-defined** (line 835: "the default value is implementation-defined"). Cases
  AWK-033, 074, 150 and 157 use the default but only through `SUBSEP` itself (e.g. `a["x" SUBSEP "y"]`), never
  through its literal value. AWK-034, 099 and 151 set SUBSEP first. Not affected.
- **printf `%d` of a non-integer** (AWK-134: `3.9` gives `3`, `-3.9` gives `-3`). Lines 1103-1105: "the value shall
  be converted (according to the rules specified in Expressions in awk) to the appropriate type for the
  conversion specification." Neither the awk page nor `int()` (line 1135: "Truncation shall be toward 0 when x>0")
  spells out negative values. **Judgment:** we read "converted to the appropriate type" as ISO C's conversion from
  floating to integer type, which truncates toward zero. Low risk, so not flagged, but the author may prefer to
  mark it `unstated` like group C.
- **Floating-point rounding in printf** (AWK-072 `%.2f` of 1.256 gives `1.26`; AWK-227 `%.2f` of 1.25 gives `1.25`).
  Line 643: "All arithmetic shall follow the semantics of floating-point arithmetic as specified by the ISO C
  standard". These results assume IEEE-754 binary64 with round-to-nearest, which ISO C does not require but which
  every platform in scope uses. Noted as an assumption only.
- **Numeric strings with leading zeros** (AWK-021, 023, 066, 131, 248): specified, as discussed under BusyBox above.
- **String-to-number of non-numeric strings** (AWK-025, 073, 133, e.g. `"  12.5xyz"+0`): lines 575-588 allow `atof`
  or a leading-prefix rule, and both give the same value for these inputs. No hexadecimal, `inf` or `nan` input is
  used, which is where the two rules would differ.
- **`exit 0` in BEGIN still runs END** (AWK-220): line 1038, "The exit statement shall invoke all END actions".
- **String comparison with `<`** (AWK-132: `"02"<"2"`): line 723 requires "the locale-specific collation sequence".
  This is locale-dependent but pinned to `C`, which is correct.
- **Leftmost-longest matching** (AWK-041, 082, 088, 176, 177, 179): the awk page says only "first instance"
  (line 1178). Leftmost-longest comes from XBD 9.1 ("the longest of the leftmost matches") through the ERE
  reference. Specified, but the `section` field should cite XBD 9.1 as well.

### (c)5 Metadata and reporting proposal

**Counts derived from current metadata (Fact, from all 250 `case.json` files):** `classification` is `portable` for
250 of 250. `locale` is `C` for 250. `expected_exit` is 0 for 250. `expected.stderr` is empty for 250. 200 files
have `specification_url` and 50 (AWK-001 to AWK-050) do not. By group: fields 35, values 35, regex 31, records 30,
arrays 27, control 23, functions 21, strings 18, formatting 15, interactions 15.

**If (a) is accepted:** portable 249, nonportable 1. **If (a) and the group B option 1 are accepted:** portable 247,
nonportable 3.

Proposed per-case fields (optional, with defaults so existing files stay valid):

| Field | Values | Purpose |
|---|---|---|
| `classification` | `portable` / `nonportable` / `observational` | which report bucket the case counts in |
| `posix_status` | `specified` / `unspecified` / `undefined` / `implementation-defined` / `unstated` / `outside-requirements` | what POSIX says about the behaviour the expectation relies on |
| `posix_clause` | quoted sentence(s) | exact text, for review |
| `posix_reference` | section name, plus XBD reference where needed | precise traceability, beyond `section` |
| `extension` | short name | for `nonportable` cases, which extension is assumed |
| `alternative_behaviours` | list of {observed_in, stdout, description} | permitted alternatives seen in practice |
| `input_text_file` | boolean, default `true` | marks group B style inputs |
| `history` | text | what changed in which release, and why |

Proposed reporting: one total for each `classification`, and the portable total split by `posix_status`. Each
failure would be marked "candidate defect" or "suspected oracle error". The suspected-oracle-error mark would live
in the run's `results/` notes and never in `cases/`, so the oracle never moves to match an interpreter. This needs
a small change to `runner.py` (read `classification`, group the totals) or a separate report script. We have not
changed the runner.

## (d) Baseline-results manifest

Saved as `results/2026-11-07/MANIFEST.md`. It records:

- Corpus commit `a14127d` and the `SHA256SUMS.txt` hash. `sha256sum -c` passes.
- Each interpreter's version, git commit or package version, and binary sha256:
  - pyawk `d0bdc4b`, run from source;
  - hawk `v1.2` = `d24f8d1`, built with rustc 1.99.1;
  - mawk 1.3.4 20250131 (Debian `1.3.4.20250131-1`);
  - onetrue-awk 20260426 = `5739fd7`;
  - gawk 5.4.1, built from the release tarball.
- The five exact runner commands, including `PYTHONPATH` for pyawk.
- The locale (`C`, set per case by the runner) and the timeout (5 s default).
- The platform: Debian 13, kernel 6.12.113, glibc 2.41, Python 3.13.5.
- The sha256 of each result JSON.

**Re-run (Fact):** all five interpreters were run again at about 06:35 UTC on 2026-11-07 with the same commands. Every
per-case record (status, checks, return code; timing excluded) and the command list are identical to the stored
JSON. The manifest includes the comparison script.

## (e) Plan for the next 100-150 independent cases

### (e)1 Principles

1. Expected results come from the POSIX text, written before any interpreter is run (as in v0.3). Each case
   carries `posix_status` and `posix_clause`.
2. Behaviour POSIX leaves open must not go into the portable class. Each such topic gets either a test that accepts
   any permitted result or an `observational` case.
3. Every case must be deterministic. It must not depend on time, PIDs, directory order, `for (k in a)` order when
   there is more than one key, or how stdout interleaves with a child process. Output sent to a pipe or file must be
   `close()`d before the program prints anything to stdout again, or must be checked through `expected_files`.
4. Only POSIX utilities in commands (`sh`, `cat`, `echo`, `printf`, `sort`, `true`, `false`, `exit n`).
5. Every input file and program file must be a text file (lessons of groups B and D), except in cases that test
   non-text input on purpose, which are classified accordingly.

### (e)2 Categories and counts (140 cases)

The expected values shown are our reading and are given only where the clause is unambiguous. The author should
derive them independently.

**1. getline, all forms (24)**
Clauses: lines 1220-1260; NF/NR/FNR at lines 801-813.
- `getline` (4): sets `$0`, NF, NR and FNR. Check them in a main rule, at EOF (`r = getline` in the last record
  returns 0 and leaves `$0` unchanged), and inside a `while ((getline) > 0)` loop.
- `getline var` (3): sets var, NR and FNR. NF and `$0` are unchanged. var is a numeric string (`getline v` with input
  `010`, then `v==10` gives 1).
- `getline < file` (5): sets `$0` and NF only, so NR and FNR are unchanged. Example:
  `{ while ((getline l < "f2") > 0) n++; print NR, FNR, n }` with operand f1 (2 lines) and f2 (3 lines) prints
  `1 1 3` then `2 2 3`. Further cases: a second read without `close()` continues the same stream; `close()` then
  reread starts again; a missing file returns -1; `getline < "f" "x"` has unspecified precedence (lines 1251-1253),
  so use it only parenthesised.
- `getline var < file` (3): only var changes.
- `cmd | getline` (5): sets `$0` and NF. The text does not say it sets NR (line 1229). Fact: all six interpreters we
  tried leave NR unchanged; see Appendix B. Further cases: the same command string reuses the stream; `close(cmd)`
  restarts it; `"echo 010" | getline v` makes a numeric string.
- `cmd | getline var` (2).
- Interaction (2): `getline` in BEGIN reads the first record (line 984-985), so the main loop starts at record 2.
  `getline` without var, redirected, inside END changes NF (lines 808-810).

**2. Multiple input files, FNR, FILENAME, ARGV/ARGC (18)**
Clauses: lines 747-781, 797-803, 811-813, 983-995.
- FNR resets per file while NR continues (`FNR==1{print FILENAME, NR}`).
- FILENAME is unset in BEGIN, set to the last file in END, and `-` for standard input.
- An empty file in the middle of the file list.
- The operand `-` between two files.
- Adding a file to ARGV in BEGIN (`ARGV[ARGC++]="f2"`).
- Deleting `ARGV[1]` or setting it to `""` skips it (lines 772-773, 780-781).
- Lowering ARGC so that later operands are ignored.
- `nextfile` skips the rest of a file, and NR does not count skipped records (line 812).
- Records after `nextfile` in the last file.
- Do not test: ARGC<1 (unspecified, line 750), a nonexistent ARGV element (unspecified, line 770), or changing
  FILENAME (unspecified, line 800).

**3. Assignment operands `var=value` (12)**
Clauses: lines 101-116 and 607.
- `v=1 f1 v=2 f2` gives `v` per file.
- An assignment after the last file is visible in END but not in BEGIN.
- With no file operands, the assignment applies before standard input is read.
- Escapes are processed (`v=a\tb`).
- A trailing backslash is literal (line 109-110).
- The value is a numeric string (`n=010`, then `n==10` gives 1).
- An operand with `[` before `=` is a file name, not an assignment (lines 756-757).
- `-v` happens before BEGIN; an operand assignment happens after.
- `FS=: f2` changes field splitting for the next file only.
- Do not test: `-v` versus `-F` ordering (unspecified, line 67), or changing ARGC with `-v` (unspecified, line 750-751).

**4. Output redirection, close and fflush (18)**
Clauses: lines 1044-1065 and 1208-1218.
- `>` truncates on first open, then appends while open: `print "a" > "o"; print "b" > "o"` writes two lines.
- `>>` appends to existing content.
- `close("o")` then `>` truncates again.
- `close` returns 0 on success.
- `close("never-opened")` returns non-zero. Fact: BusyBox returns 0; the rest return -1.
- Output to the same name from print and printf shares one stream.
- `print | "sort"` then `close("sort")` before the next stdout print gives a fixed order.
- `print | "cat 1>&2"` (stderr content).
- `fflush()` with no argument returns 0.
- Reading back a written file with `getline < "o"` after `close`.
- The expression is evaluated to a string (`print > ("o" n)`).
- Use `observational` only: the return value of `close()` for a pipe whose command exits non-zero. POSIX says only
  "non-zero" on failure (line 1211-1212), and implementations differ: pyawk, hawk and mawk return 3, gawk `--posix`
  and onetrue-awk return 0, and BusyBox returns 768 (Appendix B).

**5. Error status and exit codes (16)**
Clauses: lines 1927-1944, 1038-1042, 1260 and 1211-1212.
Mandated by POSIX, so portable:
- An unreadable file operand gives a diagnostic and terminates "without any further action" (lines 1941-1942),
  with exit >0. Fact: all six stop, and none runs END (Appendix B).
- `exit n` sets the status.
- `exit` in END without an expression keeps the earlier status. Fact: `BEGIN{exit 3} END{exit}` exits 3 in all six.
- `exit` stops further END actions.
- `getline < missing` returns -1 and is not fatal.
Not mandated, so expected stdout and exit can only be partly fixed:
- An invalid program is **undefined behaviour** (line 1943-1944: "If the program ... is not a valid awk program ...
  the behavior is undefined"). Syntax-error cases cannot be portable negative tests. At most they can be
  `observational`, recording "non-zero exit and non-empty stderr" as common practice.
- Division by zero follows ISO C arithmetic (line 643-644), and ISO C leaves it undefined. Fact: mawk prints `+inf`
  and exits 0, while the others print an error and exit 2 (BusyBox exits 1). Observational only.
- `next` in BEGIN, `break` outside a loop, `return` outside a function: undefined (lines 1021, 1034, 1279-1280).
  Observational only.
- Harness need: `expected_exit` written as "non-zero" rather than an exact number, and stderr matched as
  "non-empty".

**6. Record and field state (20)**
Clauses: lines 50-53, 735-743, 826-830 and 959-976.
- `$0` assignment re-splits with the *current* FS. Separately, when an FS change takes effect is **not stated** in
  the POSIX text we have: we found no sentence on whether it applies to the current record. Fact: all six
  interpreters apply it from the next record (`{FS=":"; print $1}` on `a:b c` then `d:e f` prints `a:b` then `d`).
  Classify this `unstated`, or source it from elsewhere, before treating it as portable.
- `$3="x"` on a 1-field record.
- `$(NF+2)` rebuild with OFS.
- `$0` rebuilt only on field assignment: changing OFS alone leaves `$0` unchanged until `$1=$1`.
- A field assignment inside a pattern.
- RS single character with input that ends in a newline, so the newline belongs to the last record.
- RS change in the middle of the input (applies to the next record).
- `RS=""` paragraph mode:
  - leading and trailing blank lines produce no empty records;
  - several blank lines act as one separator;
  - newline is always a field separator whatever FS is (lines 827-830). Example: `BEGIN{RS="";FS=","}{print NF}` on
    `p1 x\np1 y\n\n\n\np2 z\n` prints `2` then `1`. Fact: mawk 1.3.4 prints `1` then `1`, against the clause at line
    829-830 ("a <newline> shall always be a field separator, no matter what the value of FS is"). This is a likely
    defect finder;
  - `RS=""` with FS a single space;
  - a line containing only spaces. Line 828 says records "are separated by sequences consisting of a <newline>
    plus one or more blank lines", and XBD 3.46 defines a blank line as "A line consisting solely of zero or more
    <blank> characters terminated by a <newline>". Read literally, a line with only spaces would separate
    paragraphs. Fact: all six interpreters treat only *empty* lines as separators (`a b\n   \nc d\n\ne f\n` gives
    2 records, NF 4 and 2). This is either a deviation shared by all six or a reading the author rejects. It is a
    high-value case to decide carefully, and it should not be resolved by majority vote.
- Do not test: multi-character RS (unspecified, line 827), FS="" (line 959), or assigning NF (group C) in the
  portable class.

**7. Type conversion and comparison (20)**
Clauses: lines 575-629, 712-723 and 783-785; OFMT at 815-818.
- CONVFMT versus OFMT: `CONVFMT="%.2g"; OFMT="%.3g"; x=3.14159; print x, x ""` prints `3.14 3.1`.
- Integers ignore CONVFMT (`12345678 ""` stays `12345678`).
- An array subscript uses CONVFMT: `CONVFMT="%.2f"; a[0.1]` gives key `0.10`.
- Strnum from each source on lines 600-608: fields, getline input, FILENAME, ARGV, ENVIRON, split elements,
  command-line assignment, and assignment from another strnum. For example, `split("10 010",a); print (a[1]==a[2])`
  gives 1.
- Leading and trailing blanks in a strnum (`" 10 "==10` from a field).
- `+1`/`-1` signs.
- `1e3` field equals 1000.
- `.5` field.
- A string constant never becomes a strnum (`"10"==10.0` compares as strings and gives 0).
- An uninitialized value compared with a string and with a number.
- `x = $1; x == 10` keeps strnum status.
- `$1 ""` loses it.
- Observational only:
  - hexadecimal strnum (`0x1A` from input): permitted either way, because line 609 allows `strtod`. Fact: gawk
    `--posix` and BusyBox give 26, the others give 0;
  - `inf`/`nan` strings;
  - CONVFMT that is not a floating format (unspecified, line 595).

**8. Cross-feature interactions (12)**
- getline var inside a range pattern.
- `next` inside a function called from a main rule. This is allowed: `next` is undefined only in BEGIN and END
  (line 1034), while `nextfile` is also undefined inside a function (line 1036).
- `sub` on a field and then NF.
- `split($0, a)` versus fields after FS changes.
- An assignment operand that changes FS between files, combined with FNR.
- Output to a file, then getline from it in END.
- `printf` to a pipe and `close` inside a loop.
- `delete` of a whole array passed to a function.
- `exit` in a function called from a rule (END still runs).
- `substr` of a field rebuilt with OFS.
- `getline < FILENAME` (same name as the current input) opens a separate stream.

Total: 24 + 18 + 12 + 18 + 16 + 20 + 20 + 12 = **140**.

Keep a separate observational set (not counted in the 140, about 10 cases) that records what each implementation
does where POSIX is open:
- `substr` with start below 1 or non-integer arguments. Fact: `substr("hello",-1,3)` gives `hell` in mawk and
  `hel` in the other five.
- hexadecimal strnum.
- division by zero.
- the close status of a pipe.
- `srand()` return value.
- `length arr` without parentheses.
- `printf %c` of 256.
- NF assignment.
- `FS=""`.

### (e)3 What the harness would need

Today `tools/runner.py` runs `<cmd> -f program.awk` with `stdin.txt`, in the case folder, comparing stdout, stderr and
exit code exactly. That cannot express file operands, options, assignment operands, written files or loose error
checks. Proposed optional `case.json` fields (absent means today's behaviour, so the 250 existing cases need no
change):

| Field | Example | Meaning |
|---|---|---|
| `options` | `["-v", "x=a\\tb"]`, `["-F", ":"]` | inserted before `-f program.awk` |
| `program_files` | `["lib.awk", "main.awk"]` | several `-f` files, in order (default `["program.awk"]`) |
| `program_operand` | `true` | pass the program text as an operand instead of `-f` |
| `operands` | `["v=1", "in1.txt", "-", "v=2", "in2.txt"]` | arguments after the program |
| `fixtures` | `["in1.txt", "in2.txt"]` | case-folder files copied into a fresh temporary working directory |
| `stdin` | `"stdin.txt"` or `null` | `null` means connect `/dev/null` |
| `env` | `{"GREETING": "hi"}` | extra environment (for ENVIRON); `env_clear` for a minimal environment |
| `expected_files` | `{"out.txt": "expected.out.txt"}` | files the program must have written, compared after exit |
| `expected_absent` | `["never.txt"]` | files that must not exist |
| `expected_exit` | `0`, `3`, or `"nonzero"` | `"nonzero"` for errors where POSIX mandates only >0 |
| `stdout_check` / `stderr_check` | `"exact"` / `"empty"` / `"nonempty"` / `"ignore"` | mandated diagnostics have no fixed wording |
| `requires` | `["sh", "sort"]` | utilities the case shells out to; skipped with a clear status if missing |
| `classification`, `posix_status`, `posix_clause`, `posix_reference` | see (c)5 | reporting |
| `timeout` | `5` | per-case override |

Runner behaviour this implies:
- create a temporary directory for each case, copy the fixtures into it, and run there, so that redirection
  cannot write into `cases/`;
- substitute nothing into commands;
- keep reading `case.json` read-only;
- report the totals for each class.

We have not changed `runner.py`; this is a specification for the author.

---

## Appendix A: every case, what it relies on, verdict

Legend:
- **OK**: relies only on specified behaviour.
- **A**: explicitly unspecified.
- **B**: non-text standard input.
- **C**: relies on behaviour POSIX does not state.
- **(D)**: the program file lacks a final newline (hygiene only; AWK-001 to AWK-050).

Line numbers refer to `awk2024.txt`. Totals: 234 OK, 1 A, 8 B, 7 C; 50 of the cases also carry (D).

| Case | Group/name | What the expected result relies on | awk2024.txt lines | Verdict |
|---|---|---|---|---|
| AWK-001 | fields/default-whitespace | default FS splitting | 50-51, 962-963 | OK (D) |
| AWK-002 | fields/empty-line | default FS splitting | 50-51, 962-963 | OK (D) |
| AWK-003 | fields/explicit-separator-empty | single-character FS | 964-965 | OK (D) |
| AWK-004 | fields/field-assign-rebuild | field assignment rebuilds $0 | 52-53, 1070-1072 | OK (D) |
| AWK-005 | fields/extend-nf | assignment to nonexistent field | 739-741 | OK (D) |
| AWK-006 | fields/nf-truncate | assignment to NF | 806-810 | C: not stated (D: program file lacks final newline) |
| AWK-007 | fields/zero-reassign | assignment to $0 | 53 | OK (D) |
| AWK-008 | fields/beyond-nf-read | reference to nonexistent field | 737-739 | OK (D) |
| AWK-009 | fields/fs-regex | ERE FS | 968-969 | OK (D) |
| AWK-010 | fields/ofs-dynamic-rebuild | field assignment rebuilds $0 | 52-53, 1070-1072 | OK (D) |
| AWK-011 | records/nr-fnr | newline-terminated records, NR/FNR | 46-47, 801-803, 811-813 | OK (D) |
| AWK-012 | records/next-skips | next | 1033-1034 | OK (D) |
| AWK-013 | records/range-pattern | range patterns | 1001-1003 | OK (D) |
| AWK-014 | records/begin-end | newline-terminated records, NR/FNR; BEGIN/END ordering and input reading | 46-47, 801-803, 811-813; 983-995 | OK (D) |
| AWK-015 | records/rs-single-char | single-character RS | 826-827; text-file rule 131, 137, 143-144 | B: non-text input (D: program file lacks final newline) |
| AWK-016 | records/ors-custom | print, OFS, ORS | 1070-1075 | OK (D) |
| AWK-017 | records/getline-var | getline (plain / var) from current input | 1236-1242 | OK (D) |
| AWK-018 | records/getline-record | getline (plain / var) from current input | 1236-1242 | OK (D) |
| AWK-019 | records/getline-eof | NR/FNR in END | 801-803, 811-813 | OK (D) |
| AWK-020 | records/blank-record-as-data | newline-terminated records, NR/FNR | 46-47, 801-803, 811-813 | OK (D) |
| AWK-021 | values/numeric-field-comparison | numeric-string comparison | 600-629, 712-718, 1672-1674 | OK (D) |
| AWK-022 | values/literal-string-comparison | string comparison | 719-723 | OK (D) |
| AWK-023 | values/numeric-string-field-lexical | numeric-string comparison | 600-629, 712-718, 1672-1674 | OK (D) |
| AWK-024 | values/uninitialized-arithmetic | uninitialized values | 717, 732-734 | OK (D) |
| AWK-025 | values/string-to-number | string to number (non-numeric strings) | 575-588 | OK (D) |
| AWK-026 | values/concatenation-precedence | concatenation | 397-400 | OK (D) |
| AWK-027 | values/ternary-shortcircuit | logical, conditional, short-circuit | 489-519, 632-642 | OK (D) |
| AWK-028 | values/and-shortcircuit | logical, conditional, short-circuit | 489-519, 632-642 | OK (D) |
| AWK-029 | values/or-shortcircuit | logical, conditional, short-circuit | 489-519, 632-642 | OK (D) |
| AWK-030 | values/modulo-sign | arithmetic, %, assignment operators | 643-685 | OK (D) |
| AWK-031 | arrays/key-coercion | array subscripts are strings | 687-692, 590-595 | OK (D) |
| AWK-032 | arrays/delete-element | in / delete | 706-708, 1024-1032 | OK (D) |
| AWK-033 | arrays/multisubscript | SUBSEP / multi-subscripts | 698-705, 835 | OK (D) |
| AWK-034 | arrays/custom-subsep | SUBSEP / multi-subscripts | 698-705, 835 | OK (D) |
| AWK-035 | arrays/split-basic | split | 1168-1172 | OK (D) |
| AWK-036 | arrays/split-clears-array | split | 1168-1172 | OK (D) |
| AWK-037 | arrays/array-by-reference | user functions | 1111-1113, 1270-1278 | OK (D) |
| AWK-038 | arrays/scalar-by-value | user functions | 1111-1113, 1270-1278 | OK (D) |
| AWK-039 | arrays/recursion | user functions | 1111-1113, 1270-1278 | OK (D) |
| AWK-040 | arrays/function-local-extra-param | user functions | 1111-1113, 1270-1278 | OK (D) |
| AWK-041 | regex/leftmost-longest-sub | leftmost-longest matching | 1178 (+ XBD 9.1) | OK (D) |
| AWK-042 | regex/match-offset | match, RSTART, RLENGTH | 1163-1165, 831-833 | OK (D) |
| AWK-043 | regex/match-no-result | match, RSTART, RLENGTH | 1163-1165, 831-833 | OK (D) |
| AWK-044 | regex/gsub-count | sub / gsub counts and & | 1152-1154, 1176-1183 | OK (D) |
| AWK-045 | regex/sub-ampersand | sub / gsub counts and & | 1152-1154, 1176-1183 | OK (D) |
| AWK-046 | regex/anchored-match | anchors, ~, bracket classes | 939-946, 159-166 | OK (D) |
| AWK-047 | regex/regex-in-split | split | 1168-1172 | OK (D) |
| AWK-048 | strings/substr-edge | substr | 1188-1192 | OK (D) |
| AWK-049 | strings/index-positions | index, length | 1155-1161 | OK (D) |
| AWK-050 | strings/sprintf-format | printf / sprintf | 1076-1106 | OK (D) |
| AWK-051 | fields/assign-field-rebuild | field assignment rebuilds $0 | 52-53, 1070-1072 | OK |
| AWK-052 | fields/assign-record-resplit | assignment to $0 | 53 | OK |
| AWK-053 | fields/increase-nf | assignment to NF | 806-810 | C: not stated |
| AWK-054 | fields/lower-nf | assignment to NF | 806-810 | C: not stated |
| AWK-055 | fields/field-zero-reassign | assignment to $0 | 53 | OK |
| AWK-056 | fields/fs-literal-comma | single-character FS | 964-965 | OK |
| AWK-057 | fields/ofs-record-rebuild | field assignment rebuilds $0 | 52-53, 1070-1072 | OK |
| AWK-058 | fields/empty-record | default FS splitting | 50-51, 962-963 | OK |
| AWK-059 | fields/field-numeric-index | field assignment rebuilds $0 | 52-53, 1070-1072 | OK |
| AWK-060 | fields/fs-regex-multiple | ERE FS | 968-969 | OK |
| AWK-061 | records/nr-fnr-single | newline-terminated records, NR/FNR | 46-47, 801-803, 811-813 | OK |
| AWK-062 | records/next-skips-action | next | 1033-1034 | OK |
| AWK-063 | records/begin-end-order | BEGIN/END ordering and input reading | 983-995 | OK |
| AWK-064 | records/custom-rs | single-character RS | 826-827; text-file rule 131, 137, 143-144 | B: non-text input |
| AWK-065 | records/final-unterminated | final line without newline (default RS) | 131, 137 | B: non-text input |
| AWK-066 | values/num-string-compare-input | numeric-string comparison | 600-629, 712-718, 1672-1674 | OK |
| AWK-067 | values/numeric-string-array-key | array subscripts are strings | 687-692, 590-595 | OK |
| AWK-068 | values/postincrement-evaluation | arithmetic, %, assignment operators | 643-685 | OK |
| AWK-069 | values/string-concatenation | concatenation | 397-400 | OK |
| AWK-070 | values/logical-short-circuit | logical, conditional, short-circuit | 489-519, 632-642 | OK |
| AWK-071 | values/ternary-branch-only | logical, conditional, short-circuit | 489-519, 632-642 | OK |
| AWK-072 | values/numeric-format-printf | printf / sprintf | 1076-1106 | OK |
| AWK-073 | values/conversion-leading-space | string to number (non-numeric strings) | 575-588 | OK |
| AWK-074 | values/subsep-array-tuple | SUBSEP / multi-subscripts | 698-705, 835 | OK |
| AWK-075 | values/delete-key | in / delete | 706-708, 1024-1032 | OK |
| AWK-076 | functions/array-pass-mutates | user functions | 1111-1113, 1270-1278 | OK |
| AWK-077 | functions/scalar-pass-by-value | user functions | 1111-1113, 1270-1278 | OK |
| AWK-078 | functions/recursive-factorial | user functions | 1111-1113, 1270-1278 | OK |
| AWK-079 | functions/local-scalar | user functions | 1111-1113, 1270-1278 | OK |
| AWK-080 | functions/return-default | function value without return | 1279-1280, 1416 | C: not stated |
| AWK-081 | functions/function-array-alias | user functions | 1111-1113, 1270-1278 | OK |
| AWK-082 | regex/leftmost-longest-sub | leftmost-longest matching | 1178 (+ XBD 9.1) | OK |
| AWK-083 | regex/repetition-longest | leftmost-longest matching | 1178 (+ XBD 9.1) | OK |
| AWK-084 | regex/gsub-non-overlap | sub / gsub counts and & | 1152-1154, 1176-1183 | OK |
| AWK-085 | regex/match-start-length | match, RSTART, RLENGTH | 1163-1165, 831-833 | OK |
| AWK-086 | regex/sub-only-first | sub / gsub counts and & | 1152-1154, 1176-1183 | OK |
| AWK-087 | regex/regex-range | anchors, ~, bracket classes | 939-946, 159-166 | OK |
| AWK-088 | regex/alternation-priority | leftmost-longest matching | 1178 (+ XBD 9.1) | OK |
| AWK-089 | regex/anchor-record | newline-terminated records, NR/FNR | 46-47, 801-803, 811-813 | OK |
| AWK-090 | regex/sub-replacement-ampersand | sub / gsub counts and & | 1152-1154, 1176-1183 | OK |
| AWK-091 | control/for-loop-break | control statements | 1012-1021 | OK |
| AWK-092 | control/while-continue | control statements | 1012-1021 | OK |
| AWK-093 | control/do-while-once | control statements | 1012-1021 | OK |
| AWK-094 | control/pattern-range | range patterns | 1001-1003 | OK |
| AWK-095 | control/range-rearm | range patterns | 1001-1003 | OK |
| AWK-096 | control/compound-assignment | arithmetic, %, assignment operators | 643-685 | OK |
| AWK-097 | control/printf-without-newline | print, OFS, ORS | 1070-1075 | OK |
| AWK-098 | control/nextfile-no | next | 1033-1034 | OK |
| AWK-099 | arrays/multi-dimensional-subsep | SUBSEP / multi-subscripts | 698-705, 835 | OK |
| AWK-100 | arrays/membership-vs-unset | in / delete | 706-708, 1024-1032 | OK |
| AWK-101 | fields/empty-middle-field | single-character FS | 964-965 | OK |
| AWK-102 | fields/assign-beyond-nf | assignment to nonexistent field | 739-741 | OK |
| AWK-103 | fields/assign-nf-zero | assignment to NF | 806-810 | C: not stated |
| AWK-104 | fields/rebuild-after-ofs-change | field assignment rebuilds $0 | 52-53, 1070-1072 | OK |
| AWK-105 | fields/fs-char-split | null FS | 959 | A: unspecified |
| AWK-106 | fields/fs-one-space-trims | default FS splitting | 50-51, 962-963 | OK |
| AWK-107 | fields/fs-comma-preserves-trailing | single-character FS | 964-965 | OK |
| AWK-108 | fields/field-and-record-update | assignment to $0 | 53 | OK |
| AWK-109 | fields/set-fs-before-field-read | single-character FS | 964-965 | OK |
| AWK-110 | fields/rebuild-string-field | field assignment rebuilds $0 | 52-53, 1070-1072 | OK |
| AWK-111 | fields/nf-shrink-and-extend | assignment to NF | 806-810 | C: not stated |
| AWK-112 | fields/field-assignment-expression | field assignment rebuilds $0 | 52-53, 1070-1072 | OK |
| AWK-113 | fields/preserve-leading-delimiter | single-character FS | 964-965 | OK |
| AWK-114 | fields/record-number-with-blank-lines | default FS splitting | 50-51, 962-963 | OK |
| AWK-115 | fields/multiple-records-last-no-nl | final line without newline (default RS) | 131, 137 | B: non-text input |
| AWK-116 | records/custom-rs-colon | single-character RS | 826-827; text-file rule 131, 137, 143-144 | B: non-text input |
| AWK-117 | records/rs-single-char-not-found | single-character RS | 826-827; text-file rule 131, 137, 143-144 | B: non-text input |
| AWK-118 | records/rs-leading-delimiter | single-character RS | 826-827; text-file rule 131, 137, 143-144 | B: non-text input |
| AWK-119 | records/rs-repeated-delimiters | single-character RS | 826-827; text-file rule 131, 137, 143-144 | B: non-text input |
| AWK-120 | records/nr-and-end-records | newline-terminated records, NR/FNR | 46-47, 801-803, 811-813 | OK |
| AWK-121 | records/next-in-first-rule | next | 1033-1034 | OK |
| AWK-122 | records/end-after-next | next | 1033-1034 | OK |
| AWK-123 | records/begin-only-no-stdin | BEGIN/END ordering and input reading | 983-995 | OK |
| AWK-124 | records/begin-body-end-count | newline-terminated records, NR/FNR | 46-47, 801-803, 811-813 | OK |
| AWK-125 | records/range-start-end-same | range patterns | 1001-1003 | OK |
| AWK-126 | records/range-rearm-after-end | range patterns | 1001-1003 | OK |
| AWK-127 | records/range-both-patterns-one-record | range patterns | 1001-1003 | OK |
| AWK-128 | records/next-skip-second-pattern | next | 1033-1034 | OK |
| AWK-129 | records/ors-custom | print, OFS, ORS | 1070-1075 | OK |
| AWK-130 | records/one-rule-multiple-input | newline-terminated records, NR/FNR | 46-47, 801-803, 811-813 | OK |
| AWK-131 | values/numeric-string-equality | numeric-string comparison | 600-629, 712-718, 1672-1674 | OK |
| AWK-132 | values/literal-string-comparison | string comparison | 719-723 | OK |
| AWK-133 | values/numeric-conversion-leading | string to number (non-numeric strings) | 575-588 | OK |
| AWK-134 | values/printf-truncate-integer | printf %d of a non-integer | 1103-1105 | OK |
| AWK-135 | values/printf-number-sign | printf / sprintf | 1076-1106 | OK |
| AWK-136 | values/printf-left-align | printf / sprintf | 1076-1106 | OK |
| AWK-137 | values/printf-zero-pad | printf / sprintf | 1076-1106 | OK |
| AWK-138 | values/arithmetic-precedence | arithmetic, %, assignment operators | 643-685 | OK |
| AWK-139 | values/modulo-positive | arithmetic, %, assignment operators | 643-685 | OK |
| AWK-140 | values/logical-nonzero | logical, conditional, short-circuit | 489-519, 632-642 | OK |
| AWK-141 | values/conditional-branch-evaluation | logical, conditional, short-circuit | 489-519, 632-642 | OK |
| AWK-142 | values/short-circuit-and | logical, conditional, short-circuit | 489-519, 632-642 | OK |
| AWK-143 | values/short-circuit-or | logical, conditional, short-circuit | 489-519, 632-642 | OK |
| AWK-144 | values/assignment-chain | arithmetic, %, assignment operators | 643-685 | OK |
| AWK-145 | values/sprintf-width-precision | printf / sprintf | 1076-1106 | OK |
| AWK-146 | arrays/key-zero-vs-string | number to string | 590-595 | OK |
| AWK-147 | arrays/key-01-distinct | array subscripts are strings | 687-692, 590-595 | OK |
| AWK-148 | arrays/membership-after-delete | in / delete | 706-708, 1024-1032 | OK |
| AWK-149 | arrays/membership-empty-value | in / delete | 706-708, 1024-1032 | OK |
| AWK-150 | arrays/multiindex-subsep | SUBSEP / multi-subscripts | 698-705, 835 | OK |
| AWK-151 | arrays/subsep-changing-lookup | SUBSEP / multi-subscripts | 698-705, 835 | OK |
| AWK-152 | arrays/array-value-increment | arithmetic, %, assignment operators | 643-685 | OK |
| AWK-153 | arrays/uninitialized-array-value | uninitialized values | 717, 732-734 | OK |
| AWK-154 | arrays/array-numeric-key-conversion | number to string | 590-595 | OK |
| AWK-155 | arrays/array-colon-string-key | array subscripts are strings | 687-692, 590-595 | OK |
| AWK-156 | arrays/in-after-reference | in / delete | 706-708, 1024-1032 | OK |
| AWK-157 | arrays/array-composite-key | SUBSEP / multi-subscripts | 698-705, 835 | OK |
| AWK-158 | arrays/array-string-number-values | array subscripts are strings | 687-692, 590-595 | OK |
| AWK-159 | arrays/array-conditional-operator | in / delete | 706-708, 1024-1032 | OK |
| AWK-160 | arrays/array-delete-reinsert | in / delete | 706-708, 1024-1032 | OK |
| AWK-161 | functions/recursive-sum | user functions | 1111-1113, 1270-1278 | OK |
| AWK-162 | functions/recursive-fib-small | user functions | 1111-1113, 1270-1278 | OK |
| AWK-163 | functions/scalars-passed-by-value | user functions | 1111-1113, 1270-1278 | OK |
| AWK-164 | functions/arrays-passed-by-reference | user functions | 1111-1113, 1270-1278 | OK |
| AWK-165 | functions/optional-local | user functions | 1111-1113, 1270-1278 | OK |
| AWK-166 | functions/missing-arg-default | user functions | 1111-1113, 1270-1278 | OK |
| AWK-167 | functions/early-return | user functions | 1111-1113, 1270-1278 | OK |
| AWK-168 | functions/function-global-write | user functions | 1111-1113, 1270-1278 | OK |
| AWK-169 | functions/function-array-and-scalar | user functions | 1111-1113, 1270-1278 | OK |
| AWK-170 | functions/nested-function-call | user functions | 1111-1113, 1270-1278 | OK |
| AWK-171 | functions/return-concat | concatenation | 397-400 | OK |
| AWK-172 | functions/function-sprintf | user functions | 1111-1113, 1270-1278 | OK |
| AWK-173 | functions/function-regex-match | user functions | 1111-1113, 1270-1278 | OK |
| AWK-174 | functions/function-parameter-shadow | user functions | 1111-1113, 1270-1278 | OK |
| AWK-175 | functions/function-return-default | function value without return | 1279-1280, 1416 | C: not stated |
| AWK-176 | regex/leftmost-longest-alt | leftmost-longest matching | 1178 (+ XBD 9.1) | OK |
| AWK-177 | regex/leftmost-longest-backwards | leftmost-longest matching | 1178 (+ XBD 9.1) | OK |
| AWK-178 | regex/regex-longest-prefix | leftmost-longest matching | 1178 (+ XBD 9.1) | OK |
| AWK-179 | regex/regex-alt-middle | leftmost-longest matching | 1178 (+ XBD 9.1) | OK |
| AWK-180 | regex/regex-match-offset | match, RSTART, RLENGTH | 1163-1165, 831-833 | OK |
| AWK-181 | regex/regex-no-match | match, RSTART, RLENGTH | 1163-1165, 831-833 | OK |
| AWK-182 | regex/regex-sub-count | sub / gsub counts and & | 1152-1154, 1176-1183 | OK |
| AWK-183 | regex/regex-gsub-count | sub / gsub counts and & | 1152-1154, 1176-1183 | OK |
| AWK-184 | regex/regex-sub-replacement-amp | sub / gsub counts and & | 1152-1154, 1176-1183 | OK |
| AWK-185 | regex/regex-anchored-start | anchors, ~, bracket classes | 939-946, 159-166 | OK |
| AWK-186 | regex/regex-char-class | anchors, ~, bracket classes | 939-946, 159-166 | OK |
| AWK-187 | regex/regex-group-repeat | leftmost-longest matching | 1178 (+ XBD 9.1) | OK |
| AWK-188 | regex/regex-gsub-nonoverlap | sub / gsub counts and & | 1152-1154, 1176-1183 | OK |
| AWK-189 | regex/regex-match-begin-end | match, RSTART, RLENGTH | 1163-1165, 831-833 | OK |
| AWK-190 | regex/regex-conditional-sub | sub / gsub counts and & | 1152-1154, 1176-1183 | OK |
| AWK-191 | strings/substr-middle | substr | 1188-1192 | OK |
| AWK-192 | strings/substr-longer | substr | 1188-1192 | OK |
| AWK-193 | strings/substr-one | substr | 1188-1192 | OK |
| AWK-194 | strings/substr-empty-past-end | substr | 1188-1192 | OK |
| AWK-195 | strings/index-found | index, length | 1155-1161 | OK |
| AWK-196 | strings/index-not-found | index, length | 1155-1161 | OK |
| AWK-197 | strings/length-string | index, length | 1155-1161 | OK |
| AWK-198 | strings/tolower-plain | tolower/toupper | 1193-1200 | OK |
| AWK-199 | strings/toupper-plain | tolower/toupper | 1193-1200 | OK |
| AWK-200 | strings/split-comma | split | 1168-1172 | OK |
| AWK-201 | strings/split-regexp | split | 1168-1172 | OK |
| AWK-202 | strings/split-trailing-empty | split | 1168-1172 | OK |
| AWK-203 | strings/sprintf-string-precision | printf / sprintf | 1076-1106 | OK |
| AWK-204 | strings/sprintf-two-calls | printf / sprintf | 1076-1106 | OK |
| AWK-205 | strings/split-assignments | split | 1168-1172 | OK |
| AWK-206 | control/for-loop | control statements | 1012-1021 | OK |
| AWK-207 | control/nested-loops | control statements | 1012-1021 | OK |
| AWK-208 | control/break-inner | control statements | 1012-1021 | OK |
| AWK-209 | control/continue-for | control statements | 1012-1021 | OK |
| AWK-210 | control/while-loop | control statements | 1012-1021 | OK |
| AWK-211 | control/do-while | control statements | 1012-1021 | OK |
| AWK-212 | control/if-else | control statements | 1012-1021 | OK |
| AWK-213 | control/nested-if | control statements | 1012-1021 | OK |
| AWK-214 | control/ternary | logical, conditional, short-circuit | 489-519, 632-642 | OK |
| AWK-215 | control/next-even | next | 1033-1034 | OK |
| AWK-216 | control/pattern-condition | expression patterns, multiple rules | 47-48, 996-998 | OK |
| AWK-217 | control/range-trigger | range patterns | 1001-1003 | OK |
| AWK-218 | control/two-independent-rules | expression patterns, multiple rules | 47-48, 996-998 | OK |
| AWK-219 | control/begin-and-end-only | BEGIN/END ordering and input reading | 983-995 | OK |
| AWK-220 | control/exit-status-success | exit in BEGIN runs END | 1038-1041 | OK |
| AWK-221 | formatting/escape-tab | string escapes | 855-930 | OK |
| AWK-222 | formatting/escape-newline | string escapes | 855-930 | OK |
| AWK-223 | formatting/escape-backslash | string escapes | 855-930 | OK |
| AWK-224 | formatting/string-quote | string escapes | 855-930 | OK |
| AWK-225 | formatting/printf-integer-width | printf / sprintf | 1076-1106 | OK |
| AWK-226 | formatting/printf-string-left | printf / sprintf | 1076-1106 | OK |
| AWK-227 | formatting/printf-precision-float | printf / sprintf | 1076-1106 | OK |
| AWK-228 | formatting/printf-percent | printf / sprintf | 1076-1106 | OK |
| AWK-229 | formatting/print-ofs | print, OFS, ORS; number to string | 1070-1075; 590-595 | OK |
| AWK-230 | formatting/print-ors | print, OFS, ORS | 1070-1075 | OK |
| AWK-231 | formatting/print-empty | print, OFS, ORS | 1070-1075 | OK |
| AWK-232 | formatting/printf-no-implicit-newline | print, OFS, ORS | 1070-1075 | OK |
| AWK-233 | formatting/printf-zero-width-number | printf / sprintf | 1076-1106 | OK |
| AWK-234 | formatting/sprintf-as-expression | printf / sprintf | 1076-1106 | OK |
| AWK-235 | formatting/multiple-prints | print, OFS, ORS | 1070-1075 | OK |
| AWK-236 | interactions/field-write-then-regex | field assignment rebuilds $0 | 52-53, 1070-1072 | OK |
| AWK-237 | interactions/split-and-array-membership | in / delete | 706-708, 1024-1032 | OK |
| AWK-238 | interactions/function-field-read | default FS splitting | 50-51, 962-963 | OK |
| AWK-239 | interactions/regex-and-substr | match, RSTART, RLENGTH | 1163-1165, 831-833 | OK |
| AWK-240 | interactions/array-from-fields | arrays from input fields | 687-708 | OK |
| AWK-241 | interactions/regex-rewrite-field | field assignment rebuilds $0 | 52-53, 1070-1072 | OK |
| AWK-242 | interactions/function-mutates-array-from-split | split | 1168-1172 | OK |
| AWK-243 | interactions/range-and-next | range patterns | 1001-1003 | OK |
| AWK-244 | interactions/mutable-field-nf-and-function | field assignment rebuilds $0 | 52-53, 1070-1072 | OK |
| AWK-245 | interactions/numeric-array-and-format | printf / sprintf | 1076-1106 | OK |
| AWK-246 | interactions/loop-over-fields | default FS splitting | 50-51, 962-963 | OK |
| AWK-247 | interactions/function-and-match | match, RSTART, RLENGTH | 1163-1165, 831-833 | OK |
| AWK-248 | interactions/field-string-conversion | field assignment rebuilds $0 | 52-53, 1070-1072 | OK |
| AWK-249 | interactions/array-aggregation-and-end | arrays from input fields | 687-708 | OK |
| AWK-250 | interactions/next-and-counter | next | 1033-1034 | OK |


## Appendix B: exploratory probes for section (e) (observational, not oracles)

Script: `results/2026-11-07/probes/run_plan_probes.sh`, which reads `probes/plan_probes.tsv`. Full output:
`probes/plan_probes_output.txt`. Interpreters: pyawk, hawk, mawk, gawk `--posix`, onetrue-awk and BusyBox, all
with `LC_ALL=C`. The table lists the probes where at least one interpreter differed, plus two where all six agree
but the POSIX text is open to question. All other probes agreed across all six. pyawk and hawk agreed with each other on every probe.

| Probe | Result |
|---|---|
| `BEGIN{RS="";FS=","}{print NF}` on a 2-line paragraph | mawk `1`; others `2`. POSIX lines 829-830 require newline to separate fields in paragraph mode, which supports `2` |
| `print "x" \| "cat >/dev/null; exit 3"; print close(...)` | pyawk, hawk, mawk `3`; gawk `--posix`, onetrue `0`; BusyBox `768`. POSIX: "non-zero" on failure only |
| `close("never-opened")` | BusyBox `0`; others `-1` |
| `END{ r = getline; print r }` | BusyBox `-1`; others `0` |
| `"echo 0x1A" \| getline v; print v+0` | gawk `--posix`, BusyBox `26`; others `0` (both permitted, line 609) |
| `substr("hello",-1,3)` | mawk `hell`; others `hel` (POSIX does not cover start < 1) |
| `print 1/0` | mawk `+inf`, exit 0; others error, exit 2 (BusyBox 1) |
| `BEGIN{RS=""}` on `a b\n   \nc d\n\ne f\n` | all six: 2 records (the spaces-only line does not separate). See (e)2 item 6: a literal reading of line 828 with XBD 3.46 would give 3 |
| `{FS=":"; print $1}` on `a:b c\nd:e f\n` | all six: `a:b`, `d` (the FS change applies from the next record; the POSIX text does not state this) |
| `"echo 010" \| getline v; print (v==10)` | BusyBox `0`; others `1` (POSIX: numeric string, decimal) |
