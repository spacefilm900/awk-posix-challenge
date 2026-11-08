# Evidence note: P35, P36, P30 and P42 (v0.6 proposal)

**Prepared 7 November 2026 by Grok Bot (implementation side), for ChatGPT's independent review.**

- **No defect is confirmed here.** Quotes are verbatim from `/workspace/awk2024.txt`, the POSIX.1-2024 awk page as
  text, with its line numbers.
- **Outputs:** every output below was run locally on this box with LC_ALL=C.
- **Implementations:**
  - hawk 9f09764;
  - pyawk b6a3d25;
  - mawk 1.3.4 20250131;
  - gawk 5.4.1, with and without `--posix`;
  - One True AWK 20260426;
  - BusyBox 1.35.0.
- **Austin Group items:** each one cited below was opened and read on 7 November 2026. The tracker was also searched for
  items on the other topics. Where none was found, I say so. That is not proof that none exists.

---

## P35 and P36: an empty field, and a field past NF, compared with 0

**Programs:**
- P35 runs `-F,` on `a,,c` with `{ print ($2 == 0), ($2 == ""), length($2) }`.
- P36 runs on `a b` with `{ x = $5; y = ($5 == 0); print NF, y, $0 }`.

The v0.6 draft expects `1 1 0` and `2 1 a b`.

### POSIX.1-2024 text

The operator table, `$expr` row (the result type is "Uninitialized or String"):

> 262: $expr
> 265: Field reference
> 268: Uninitialized or String
> 271: N/A

The comparison rules:

> 711: Comparisons (with the '<', "<=", "!=", "==", '>', and
> 712: ">=" operators) shall be made numerically:
> 714: if both operands are numeric,
> 715: if one is numeric and the other has a string value that is a numeric string,
> 716: if both have string values that are numeric strings, or
> 717: if one is numeric and the other has the uninitialized value.
> 719: Otherwise, operands shall be converted to strings as required and a string comparison shall be made as follows:
> 721: For the "!=" and "==" operators, the strings shall be compared to check if they are identical
> 722: (not to check if they collate equally).
> 723: For the other operators, the strings shall be compared using the locale-specific collation sequence.

The uninitialized value, and fields:

> 732: Uninitialized variables, including scalar variables, array elements, and field variables, shall have an uninitialized value. An
> 733: uninitialized value shall have both a numeric value of zero and a string value of the empty string. Evaluation of variables with an
> 734: uninitialized value, to either string or numeric, shall be determined by the context in which they are used.
> 735: Field variables shall be designated by a '$' followed by a number or numerical expression. The effect of
> 736: the field number expression evaluating to anything other than a non-negative integer is unspecified; uninitialized variables
> 737: or string values need not be converted to numeric values in this context. New field variables can be created by assigning a value
> 738: to them. References to nonexistent fields (that is, fields after $NF), shall evaluate to the uninitialized value. Such
> 739: references shall not create new fields. However, assigning to a nonexistent field (for example, $(NF+2)=5) shall increase
> 740: the value of NF; create any intervening fields with the uninitialized value; and cause the value of $0 to be recomputed,
> 741: with the fields being separated by the value of OFS. Each field variable shall have a string value or an uninitialized value
> 742: when created. Field variables shall have the uninitialized value when created from $0 using FS and the variable does not
> 743: contain any characters. If appropriate, the field variable shall be considered a numeric string (see Expressions in awk).

RATIONALE:

> 2309: Variables that are assigned to a numeric string shall also be treated as a numeric string. (For example, the notion
> 2310: of a numeric string can be propagated across assignments.) In comparisons, all variables having the uninitialized value are to be
> 2311: treated as a numeric operand evaluating to the numeric value zero.
> 2312: Uninitialized variables include all types of variables including scalars, array elements, and fields. The
> 2313: definition of an uninitialized value in Variables and Special Variables is necessary to describe the
> 2314: value placed on uninitialized variables and on fields that are valid (for example, < $NF) but have no characters
> 2315: in them and to describe how these variables are to be used in comparisons. A valid field, such as $1, that has no characters
> 2316: in it can be obtained from an input line of "\t\t" when FS='\t'. Historically, the comparison
> 2317: ($1<10) was done numerically after evaluating $1 to the value zero.

### Austin Group

- **[0001198: "Comparison of numeric string values in awk"](https://austingroupbugs.net/view.php?id=1198).**
  - Status: Closed, Accepted As Marked. Interpretation approved on 17 April 2019 and applied.
  - The description says some awks treat uninitialized fields differently from uninitialized variables when compared
    with 0, and calls that "simply non-conforming".
  - The **approved interpretation response**, however, says: *"On the question of whether an uninitialized field has a
    string value, the standard is unclear on this issue, and no conformance distinction can be made between alternative
    implementations based on this. This is being referred to the sponsor."*
  - Its editorial changes are the ones visible in POSIX.1-2024:
    - the `$expr` result type changed to "Uninitialized or String" (lines 262-271);
    - the "both numeric strings → numeric" bullet was added (line 716).
- **[0001973: awk "numeric string" origins](https://www.austingroupbugs.net/view.php?id=1973).**
  - This is about POSIX.1-2024 itself, tagged tc1-2024. Status: Interpretation Required; Interp Status: Pending.
  - The current proposed response (note 0007459, 20 July 2026) says: *"The standard is unclear on this issue, and no
    conformance distinction can be made between alternative implementations based on this… No known existing
    implementation follows the exact wording of the standard."*
  - It proposes rewording the numeric-string origin list (lines 599-610). That rewording concerns where numeric strings
    come from, and does not decide P35 or P36 directly. It is relevant context: the committee's current approach is to
    describe values, not variables.
- **Implementer discussion, not a standards decision:** onetrue-awk issue
  [#175](https://github.com/onetrueawk/awk/issues/175) (2023). It records that One True AWK, mawk and gawk print 0 for
  `$1 == 0` on an empty line, that BusyBox prints 1, and that the maintainers chose existing practice.

### Local outputs

| Implementation | P35 `($2 == 0), ($2 == ""), length($2)` on `a,,c` |
|---|---|
| hawk | `0 1 0` |
| pyawk | `0 1 0` |
| mawk | `0 1 0` |
| gawk --posix | `0 1 0` |
| gawk | `0 1 0` |
| onetrue | `0 1 0` |
| busybox | `0 1 0` |

| Implementation | P36 `NF, ($5 == 0), $0` on `a b` |
|---|---|
| hawk | `2 0 a b` |
| pyawk | `2 0 a b` |
| mawk | `2 0 a b` |
| gawk --posix | `2 0 a b` |
| gawk | `2 0 a b` |
| onetrue | `2 0 a b` |
| busybox | `2 1 a b` |

BusyBox gives 1 for a field past NF (P36), but 0 for an empty field created by splitting (P35).

### Assessment

- **Fact:** lines 738 and 742 say the value is "the uninitialized value", and line 717 makes the comparison with a number
  numeric. RATIONALE lines 2312-2317 give the empty-field case explicitly.
- **Fact:** the approved interpretation of 1198 says that, on whether an uninitialized field has a string value, *"the
  standard is unclear … no conformance distinction can be made"*.
- **Ambiguity:** "Uninitialized or String" (line 268) does not say when a field reference yields which. The 1198
  interpretation is the committee's own statement that conformance cannot be decided on this point.
- **Judgment:** P35 and P36 should **not** be portable or provisional-portable. I recommend **observational**, citing
  1198. My v0.6 draft marked them "portable (provisional)", and I withdraw that recommendation. No implementation is
  shown to be defective.

---

## P30: `getline < "-"` when a file named `-` exists

**Program:** `BEGIN { getline l < "-"; print l }`, run in a directory containing a file `-` with the text `from-file`,
with stdin `from-stdin`.

### POSIX.1-2024 text

Redirected getline:

> 1243: getline [var] < expression
> 1245: Read the next record of input from a named file. The expression shall be evaluated to produce a string that is used as a
> 1246: pathname. If the file of that name is not currently open, it shall be opened. As long as the stream remains open, subsequent calls
> 1247: in which expression evaluates to the same string value shall read subsequent records from the file. The file shall remain
> 1248: open until the close function is called with an expression that evaluates to the same string value. If var is
> 1249: omitted, $0 and NF shall be set; otherwise, var shall be set and, if appropriate, it shall be considered a numeric
> 1250: string (see Expressions in awk).

`-` as a file operand, and as `-f` progfile:

> 72: -f progfile
> 73: Specify the pathname of the file progfile containing an awk program. A pathname of '-' shall denote the
> 74: standard input. If multiple instances of this option are specified, the concatenation of the files specified as progfile in
> 75: the order specified shall be the awk program. The awk program can alternatively be specified in the command line as a
> 76: single argument.

> 97: file
> 98: A pathname of a file that contains the input to be read, which is matched against the set of patterns in the program. If no
> 99: file operands or their equivalents, achieved by modifying the awk variables ARGV and ARGC, are
> 100: specified, or if a file operand is '-', the standard input shall be used.

> 121: STDIN
> 123: The standard input shall be used only if no file operands or their equivalents, achieved by modifying the awk
> 124: variables ARGV and ARGC, are specified; or if a file operand, or its equivalent, is '-'; or if a
> 125: progfile option-argument is '-'; see the INPUT FILES section. If the awk program contains no actions and no

ARGV iteration:

> 776: Otherwise, ARGV[ internal counter value] shall be treated as a file operand,
> 777: FILENAME shall be set to that value, and the named file, or standard input if the value is '-', shall be processed
> 778: as an input file.

FILENAME:

> 797: FILENAME
> 798: The pathname used to open the current input file, or '-' if the file is standard input. Inside a BEGIN action

APPLICATION USAGE:

> 1967: To specify a file operand naming a file with a name containing an <equals-sign>, users can use
> 1968: "./" as the first two characters of a relative file pathname that starts with an <underscore> or an alphabetic
> 1969: character to keep the file operand from being interpreted as an assignment operand. Similarly, "./-" can be
> 1970: used to access a file named '-' in the current directory rather than use standard input.

### Austin Group

- **[0000974: "several issues with awk's ARGC/ARGV"](https://austingroupbugs.net/view.php?id=974).** Interpretation
  approved on 18 January 2017 and applied in Issue 8 (line 2413).
  - It produced the ARGV iteration text, the "or its equivalent, is '-'" wording, and the `"./-"` APPLICATION USAGE
    sentence.
  - It deals only with operands and ARGV elements. **It does not mention `getline <`.**
- I found **no** Austin Group item on `getline < "-"` itself.

### Local outputs

| Implementation | `getline l < "-"` |
|---|---|
| hawk | `from-stdin` |
| pyawk | `from-stdin` |
| mawk | `from-stdin` |
| gawk --posix | `from-stdin` |
| gawk | `from-stdin` |
| onetrue | `from-stdin` |
| busybox | `from-file` |

| Implementation | contrast: `getline l < "./-"` |
|---|---|
| hawk | `from-file` |
| pyawk | `from-file` |
| mawk | `from-file` |
| gawk --posix | `from-file` |
| gawk | `from-file` |
| onetrue | `from-file` |
| busybox | `from-file` |

### Assessment

- **Fact:** the text gives `-` the meaning "standard input" only for file operands and their ARGV equivalents
  (100, 124, 777) and for a `-f` progfile (73). For `getline < expression`, the value "is used as a pathname" (1245),
  and no exception for `-` is stated.
- **Fact:** the STDIN section (123-125) says standard input "shall be used **only** if" there are no file operands, a
  file operand or its equivalent is `-`, or a progfile is `-`. A redirected getline is not in that list. This could be
  read as supporting the literal pathname reading. It could equally be read as describing only the utility's own input
  operands, and it would not stop a program from reading stdin explicitly, for example through `/dev/stdin`.
- **Ambiguity:** the text never says that `-` in getline is *not* stdin either. Every implementation tested except
  BusyBox treats it as stdin, which is long-standing practice. `./-` (1969-1970) reaches the file `-` in every
  implementation.
- **Judgment:** keep P30 **observational**, recording both readings. A portable test can safely use `getline < "./-"`, or
  a file operand `-`.

---

## P42: `substr("hello", 0, 2)`

### POSIX.1-2024 text

The definition:

> 1188: substr(s, m[, n ])
> 1190: Return the at most n-character substring of s that begins at position m, numbering from 1. If n is
> 1191: omitted, or if n specifies more characters than are left in the string, the length of the substring shall be limited by the
> 1192: length of the string s.

Characters, not bytes:

> 1953: The index, length, match, and substr functions should not be confused with similar
> 1954: functions in the ISO C standard; the awk versions deal with characters, while the ISO C standard deals with
> 1955: bytes.

### Austin Group

I found no Austin Group item on `substr` with a start below 1, or with non-integer arguments. The [GNU Awk manual, String Functions](https://www.gnu.org/software/gawk/manual/html_node/String-Functions.html) (fetched 7 November 2026) says: *"If start is less than one, substr() treats it as if it was one. (POSIX doesn't specify
what to do in this case: BWK awk acts this way, and therefore gawk does too.)"* That is an implementer's statement, not a
standards decision.

### Local outputs

These also include `substr("hello", -1, 3)` and `substr("hello", 1.5, 2)`:

| Implementation | `[substr("hello",0,2)][substr("hello",-1,3)][substr("hello",1.5,2)]` |
|---|---|
| hawk | `[he][hel][he]` |
| pyawk | `[he][hel][he]` |
| mawk | `[he][hell][he]` |
| gawk --posix | `[he][hel][he]` |
| gawk | `[he][hel][he]` |
| onetrue | `[he][hel][he]` |
| busybox | `[he][hel][he]` |

### Assessment

- **Fact:** the definition (1190-1192) speaks of a substring "that begins at position m, numbering from 1". It says
  nothing about m < 1, non-integer m or n, or how m and n interact when m < 1.
- **Fact:** all seven give `he` for m = 0. For m = -1 and n = 3, mawk gives `hell` and the rest give `hel`. That
  disagreement shows the boundary arithmetic really does vary.
- **Judgment:** P42 is **unspecified by the text**. Classify it as observational or nonportable, with no normative
  expectation. My draft expectation of `h` was one possible reading, not one the text requires.

---

## Summary

| Scenario | Text | Austin Group | Recommended status (judgment) |
|---|---|---|---|
| P35 (empty field == 0) | 742 + 717 + RATIONALE 2312-2317 support numeric; 262-271 "Uninitialized or String" | 1198 (approved interpretation): "unclear … no conformance distinction can be made"; 1973 (pending) related | observational |
| P36 (field past NF == 0) | 738 + 717 support numeric; 262-271 | same as P35 | observational |
| P30 (`getline < "-"`) | 1245 says pathname; `-` = stdin is stated only for operands and progfile | 974 covers operands only; nothing on getline found | observational |
| P42 (`substr` with m = 0) | 1190-1192 silent on m < 1 | nothing found | observational or nonportable |
