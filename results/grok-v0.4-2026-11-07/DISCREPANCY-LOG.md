# Discrepancy log: v0.4 corpus, run of 2026-11-07

Every disagreement seen in the frozen run (`MANIFEST.md`) and the variant probes. The classes are:

- **(1)** a genuine interpreter defect;
- **(2)** a test-oracle problem;
- **(3)** behaviour POSIX leaves unspecified or implementation-defined;
- **(4)** a harness or environment problem.

Line numbers refer to our plain-text copy of the POSIX.1-2024 awk page (`awk2024.txt`).

## In the 390-case corpus

| Case | Interpreter(s) | Observed | Expected | Class | Basis |
|---|---|---|---|---|---|
| AWK-105 (nonportable) | gawk 5.4.1 `--posix` (C and C.UTF-8), gawk `--traditional` | `1:abc:` | `3:a:c` | (3) | "If FS is a null string, the behavior is unspecified." (line 959). This is an expected outcome for a `nonportable` case, not a defect |
| AWK-021, AWK-023, AWK-131 (portable) | BusyBox awk 1.35.0 (observational only) | treats field `010` as octal 8 | `010` == 10 | (1), in BusyBox | numeric strings are recognised by `strtod` or as a decimal NUMBER token (lines 609-629, 1672-1674) |

**pyawk and hawk: 0 failures out of 390**, in `C` (the frozen run) and also in `C.UTF-8` (probe). No portable or
observational case failed on any of mawk, onetrue-awk, gawk `--posix` or default gawk.

## Outside the corpus: exploratory probes (`probes/hard/`)

These come from one-liners we wrote while designing harder tests, not from ChatGPT's cases. They are recorded
here because two of them involve pyawk and hawk.

| Probe | Observed | POSIX | Class |
|---|---|---|---|
| `printf 'x\n' \| awk '{print "[" FILENAME "]"}'` (no file operands) | pyawk, hawk, onetrue print `[]`. mawk, gawk (both modes) and BusyBox print `[-]` | lines 764-766: "If the internal counter is greater than or equal to the current value of ARGC and no file operands have been processed, awk shall set FILENAME to '-' and process standard input as if it was given as a file operand." Line 798: "The pathname used to open the current input file, or '-' if the file is standard input." | **(1) pyawk and hawk defect** against POSIX.1-2024. onetrue-awk 20260426 has the same deviation |
| `printf 'a,b\nc\n' \| awk 'BEGIN{RS="";FS="[,;]"}{print NF}'` | pyawk, hawk `3`. mawk, gawk (both modes), onetrue, BusyBox `2` | lines 827-830: with RS null, "a <newline> shall always be a field separator, no matter what the value of FS is" | pyawk and hawk follow the text. All four references deviate (gawk's manual says newline is not added as a separator when FS is a regexp). Not a pyawk/hawk defect |
| `printf 'a,b\nc\n' \| awk 'BEGIN{RS="";FS=","}{print NF}'` | mawk `2`; BusyBox `4`; others `3` | same clause | mawk and BusyBox deviate |
| `BEGIN{RS="";FS=","}{$0="x,y\nz"; print NF}` | mawk `2`; others `3` | the clause is about records; whether it also applies to splitting an assigned `$0` is **not stated** | (3) |
| `BEGIN{RS=""}` on `a b\n   \nc d\n\ne f\n` | all seven: 2 records (a line of spaces does not separate) | line 828 says "one or more blank lines", and XBD defines a blank line as "A line consisting solely of zero or more <blank> characters terminated by a <newline>". A literal reading gives 3 records | open question for the author; all implementations agree on 2 |
| `NR==1{getline; getline; print FILENAME, FNR, NR, $0}` across `f1` (2 lines) and `f2` | BusyBox `f1 2 2 a2`; others `f2 1 3 b1` | `getline` reads "the next input record from the current input file" and sets NR and FNR (lines 1236-1238). Moving on to the next file follows lines 760-778 | (1), in BusyBox |
| `"echo 010" \| getline v`, `getline v < f`, `ARGV[1]`, `n=010` operand, `ENVIRON`: each compared `== 10` | BusyBox `0`; others `1` | numeric-string sources, lines 600-608 | (1), in BusyBox |
| `END{ r = getline; print r }` | BusyBox `-1`; others `0` | "zero for end-of-file" (line 1260) | (1), in BusyBox |
