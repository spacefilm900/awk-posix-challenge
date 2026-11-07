"""v0.6 PROPOSAL scenarios (implementation side, not frozen tests).

Each expectation is taken from the text of POSIX.1-2024 awk
(awk2024.txt line numbers). The recorded behaviour of each implementation
is information only, and was NOT used to choose an expectation.
`status` is one of:
  portable                  the text specifies the result
  portable (provisional)    the text specifies it, but needs a reading that
                            ChatGPT should confirm
  observational             the text is silent, contested or ambiguous; the
                            "expected" output is the literal reading, given
                            for discussion only
"""

T = "\t"
S = []


def sc(area, title, clause, prog, out, *, args=(), operands=(), stdin="", files=None, locale="C",
       exit=0, err="empty", status="portable", defect="", note="", noprog=False):
    S.append(dict(area=area, title=title, clause=clause, prog=prog, out=out, args=list(args),
                  operands=list(operands), stdin=stdin, files=files or {}, locale=locale, exit=exit,
                  err=err, status=status, defect=defect, note=note, noprog=noprog))


# --- A. -v and assignment-operand escapes ----------------------------------
A = "-v / assignment operands"
sc(A, "-v value with \\t escape", "77-81; 101-110; 1653-1657",
   'BEGIN { printf "%s|%d\\n", x, length(x) }', "a\tb|3\n", args=["-v", r"x=a\tb"],
   defect="the -v value is not processed as a STRING token (escape left as two characters)")
sc(A, "-v value ending in an unescaped backslash", "106-110",
   'BEGIN { printf "%s|%d\\n", x, length(x) }', "ab\\|3\n", args=["-v", "x=ab\\"],
   defect="a trailing backslash is treated as an escape, or is rejected or dropped")
sc(A, "-v value with \\\\ (double backslash)", "107-110; 909-916",
   'BEGIN { printf "%s|%d\\n", x, length(x) }', "a\\b|3\n", args=["-v", r"x=a\\b"],
   defect="\\\\ is not reduced to one backslash in assignment values")
sc(A, "-v value with octal escapes", "107-110; 883-892",
   'BEGIN { printf "%s|%d\\n", x, length(x) }', "ABC|3\n", args=["-v", r"x=\101\102C"],
   defect="octal \\ddd is not decoded in -v values")
sc(A, "-v numeric string with leading zeros", "599-607; 610-631; 711-717",
   'BEGIN { print x, (x == 10), (x < 9), (x "" == "010") }', "010 1 0 1\n", args=["-v", "x=010"],
   defect="a -v value is not treated as a numeric string, or the string value is changed to 10")
sc(A, "-v numeric string with leading and trailing blanks", "610-625",
   'BEGIN { print "[" x "]", (x == 3), (x < 10) }', "[ 3 ] 1 1\n", args=["-v", "x= 3 "],
   defect="blanks around a numeric string stop the numeric comparison")
sc(A, "-v value that only looks numeric (1e)", "610-625; 719-722",
   'BEGIN { print (x == 1), (x + 0) }', "0 1\n", args=["-v", "x=1e"],
   defect="'1e' is accepted as a numeric string (strtod leaves 'e', and it is not a NUMBER token)")
sc(A, "Assignment operand with \\t escape", "101-112",
   '{ print x "|" length(x) }', "1\t2|3\n", operands=[r"x=1\t2", "f1"], files={"f1": "a\n"},
   defect="assignment operands are not escape-processed like -v values")
sc(A, "Timing of assignment operands around BEGIN and END", "112-114",
   'BEGIN { print "B[" x "]" } { print "R[" x "]" } END { print "E[" x "]" }',
   "B[]\nR[1]\nE[2]\n", operands=["x=1", "f1", "x=2"], files={"f1": "a\n"},
   defect="an assignment is applied before BEGIN, or an assignment after the last file is not applied before END")

# --- B. -F ----------------------------------------------------------------
B = "-F sepstring"
sc(B, "-F '\\t' is escape-processed like -v FS=", "62-65; 107-110; 960-965",
   '{ print NF "|" $2 }', "2|c\n", args=["-F", r"\t"], stdin="a b\tc\n",
   defect="-F value not escape-processed (FS stays as backslash-t)")
sc(B, "-F t means the letter t, not tab", "62-65; 964-965",
   '{ print NF "|" $1 }', "2|a\n", args=["-F", "t"], stdin="atb\tc\n",
   status="portable (provisional)",
   note="Historical awks map -Ft to tab. POSIX defines -F sepstring as -v FS=sepstring, so FS is the letter 't'.",
   defect="historical -Ft special case applied in a POSIX mode")
sc(B, "-F with a single ERE metacharacter '|' is literal", "960-965",
   '{ print NF "|" $2 }', "3|b\n", args=["-F", "|"], stdin="a|b|c\n",
   defect="a single-character FS is compiled as an ERE, so '|' would match the empty string")
sc(B, "-F with a multi-character ERE", "968-969",
   '{ print NF "|" $2 }', "3|b\n", args=["-F", "[:;]+"], stdin="a:;b;c\n",
   defect="a multi-character FS is not treated as an ERE, or one or more is not grouped")
sc(B, "-F ' ' is the default field splitting", "62-65; 962-963",
   '{ print NF "|" $1 "|" $2 }', "2|a|b\n", args=["-F", " "], stdin="  a \t b  \n",
   defect="-F ' ' splits on single spaces only, giving empty fields")
sc(B, "-F '\\\\.' becomes the ERE \\. (a literal dot)", "62-65; 909-916; 897-904",
   '{ print NF "|" $2 }', "2|b\n", args=["-F", "\\\\."], stdin="a.b\n",
   defect="the sepstring is escape-processed twice or not at all")

# --- C. printf %c ----------------------------------------------------------
C = "printf %c"
sc(C, "%c with a numeric argument", "1096-1097",
   'BEGIN { printf "%c%c\\n", 65, 97 }', "Aa\n",
   defect="a numeric argument is printed as its first digit")
sc(C, "%c with a string constant that looks numeric", "1098-1102",
   'BEGIN { printf "%c|%c\\n", "65", "hello" }', "6|h\n",
   defect="a string constant is converted to a number for %c")
sc(C, "%c with a number and a concatenated string", "596-598; 1096-1102",
   'BEGIN { x = 72; y = x ""; printf "%c%c\\n", x, y }', "H7\n",
   defect="concatenation result treated as numeric for %c")
sc(C, "%c with a numeric-string field", "599-607; 1096-1099",
   '{ printf "%c\\n", $1 }', "B\n", stdin="66\n", status="observational",
   note="A field '66' is a numeric string. Does it 'have a numeric value' (1096)? The literal reading gives 'B'; the alternative is '6'.",
   defect="(contested) numeric-string handling of %c")
sc(C, "%c with width and the - flag", "1076-1079; 1096-1099",
   'BEGIN { printf "[%3c][%-3c]\\n", "x", "y" }', "[  x][y  ]\n",
   defect="width or flags ignored for %c")

# --- D. close() and system() ---------------------------------------------
D = "close() / system()"
sc(D, "system() returns the command's exit status", "1255-1258",
   'BEGIN { a = system("exit 3"); b = system("true"); c = system("false"); print a, b, c }', "3 0 1\n",
   defect="system returns a raw wait status (768), or always 0")
sc(D, "Output order around system()", "1255-1258; 1043-1044",
   'BEGIN { printf "a"; r = system("echo b"); print "c" r }', "ab\nc0\n", status="observational",
   note="POSIX 2024 does not say that pending output is flushed before system(). Historical awks flush it.",
   defect="(observational) unflushed output appears after the command's output")
sc(D, "close() of a stream that was never opened is non-zero", "1208-1212",
   'BEGIN { print (close("never-opened") != 0) }', "1\n",
   defect="close of an unknown stream returns 0")
sc(D, "close() twice: 0 the first time, then non-zero", "1208-1212; 1051-1057",
   'BEGIN { print "x" > "out"; a = close("out"); b = close("out"); print a, (b != 0) }', "0 1\n",
   defect="close of a stream that is already closed reports success")
sc(D, "close() of an input pipe whose command succeeded", "1220-1228; 1208-1212",
   'BEGIN { "echo a" | getline x; print x, close("echo a") }', "a 0\n",
   defect="close of a successful input pipe returns non-zero, or a stale status")
sc(D, "close() of an output pipe whose command exits 3", "1058-1065; 1208-1212",
   'BEGIN { c = "cat >/dev/null; exit 3"; print "x" | c; r = close(c); print (r != 0) }', "1\n",
   status="observational",
   note="Is 'successful' the pclose() call, or the command's status? This is the literal reading of non-zero on failure.",
   defect="(observational) close hides the command's failure")
sc(D, "Reading a file again after close() starts at the beginning", "1243-1248; 1208-1212",
   'BEGIN { getline a < "f"; getline b < "f"; close("f"); getline c < "f"; print a, b, c }', "1 2 1\n",
   files={"f": "1\n2\n"},
   defect="close does not reset the read position, or reopening is cached")
sc(D, "'>' after close() truncates again", "1051-1057",
   'BEGIN { print "a" > "o"; close("o"); print "b" > "o"; close("o"); while ((getline l < "o") > 0) print "got " l }',
   "got b\n",
   defect="the second '>' appends instead of truncating")
sc(D, "getline from a missing file returns -1 and leaves NR alone", "1260; 1243-1250",
   'BEGIN { r = (getline l < "no-such-file"); print r, NR, "[" l "]" }', "-1 0 []\n",
   defect="the error is reported as 0 (EOF), or is fatal")

# --- E. getline < "-", and "-" operands -----------------------------------
E = 'getline < "-" / "-" operands'
sc(E, 'getline < "-" when a file named "-" exists', "1243-1250; contrast 73, 100, 776-778",
   'BEGIN { getline l < "-"; print l }', "from-file\n", files={"-": "from-file\n"}, stdin="from-stdin\n",
   status="observational",
   note=("POSIX gives '-' a stdin meaning only for file operands (100, 777) and -f progfile (73). getline < expression "
         "uses the value as a pathname (1245). The literal reading is the file '-'. Every historical awk reads stdin."),
   defect="(observational) literal pathname versus stdin convention")
sc(E, "-f - reads the program from standard input", "72-76",
   None, "prog from stdin\n", args=["-f", "-"], stdin='BEGIN { print "prog from stdin" }\n', noprog=True,
   defect="-f - opens a file named '-'")
sc(E, 'ARGV element set to "-" at run time reads stdin', "752-759; 776-778; 797-798",
   'BEGIN { ARGV[1] = "-"; ARGC = 2 } { print FILENAME, $0 }', "- s\n", operands=["f1"],
   files={"f1": "f\n"}, stdin="s\n",
   defect="the changed ARGV is ignored, or '-' is opened as a file")

# --- F. uninitialised values ----------------------------------------------
F = "uninitialised values"
sc(F, "An uninitialised scalar is both 0 and \"\"", "732-734",
   'BEGIN { if (x == 0 && x == "") print "both"; print length(x), x + 0, "[" x "]" }', "both\n0 0 []\n",
   defect="the uninitialised value takes one type only")
sc(F, "Comparisons involving an uninitialised value", "711-723",
   'BEGIN { print (x < "a"), (x < 1), (x == "0"), (x == 0) }', "1 1 0 1\n",
   defect="uninitialised compared with the string constant \"0\" numerically, or with 1 as strings")
sc(F, "An empty field is uninitialised", "741-743; 711-717",
   '{ print ($2 == 0), ($2 == ""), length($2) }', "1 1 0\n", args=["-F", ","], stdin="a,,c\n",
   status="portable (provisional)",
   note=("Normative: 742 says an empty field created by FS splitting has the uninitialized value, and 717 says "
         "comparing it with a number is numeric. The RATIONALE (2312-2317) gives this very case. Established "
         "implementations compare it as the string \"\" here, so this may need a standards interpretation, as with AWK-415 and AWK-417."),
   defect="an empty field compares as a string only, so $2 == 0 is false")
sc(F, "Referencing a field past NF does not create it", "738-739",
   '{ x = $5; y = ($5 == 0); print NF, y, $0 }', "2 1 a b\n", stdin="a b\n",
   status="portable (provisional)",
   note="738 says a nonexistent field evaluates to the uninitialized value, and 717 makes the comparison numeric. The same caveat applies as for the previous scenario.",
   defect="a reference to $5 raises NF or rebuilds $0, or $5 compares as a string")
sc(F, "'in' does not create an element; a reference does", "708-710",
   'BEGIN { if (("k" in a) == 0) print "absent"; x = a["k"]; print ("k" in a), length(a) }', "absent\n1 1\n",
   defect="'in' creates the element, or a reference does not")
sc(F, "Missing function arguments are uninitialised", "1272-1275",
   'function f(a, b) { return (b == 0) "" (b == "") } BEGIN { print f(1) }', "11\n",
   defect="missing parameters are only numeric or only string")
sc(F, "An uninitialised global passed to a function becomes an array", "1111-1113; 1272-1275",
   'function fill(arr) { arr["x"] = 1 } BEGIN { fill(A); print length(A), A["x"] }', "1 1\n",
   status="observational",
   note="POSIX says arrays are passed by reference (1113), but not whether an untyped global counts as an 'array name'.",
   defect="(observational) by-reference passing of a not-yet-typed name")

# --- G. substr ------------------------------------------------------------
G = "substr"
sc(G, "substr bounds: omitted n, n too large, start past the end", "1188-1192",
   'BEGIN { s = "hello"; print substr(s, 2) "|" substr(s, 2, 100) "|" substr(s, 6) "|" substr(s, 5, 1) }',
   "ello|ello||o\n", defect="an off-by-one at the end of the string")
sc(G, "substr with n <= 0 is empty", "1190",
   'BEGIN { print "[" substr("hello", 2, 0) "][" substr("hello", 2, -1) "]" }', "[][]\n",
   defect="a negative n is taken as 'to the end', or wraps")
sc(G, "substr with m = 0", "1190-1192", 'BEGIN { print "[" substr("hello", 0, 2) "]" }', "[h]\n",
   status="observational",
   note=("The text (1190-1192) does not define a start before position 1. The expectation shown is one reading: the characters at "
         "positions m..m+n-1 that exist, which gives 'h'. Another reading is to treat m as 1, which gives 'he'. "
         "Recommendation: ChatGPT should choose a reading, or classify this case as nonportable."),
   defect="(observational) clamping a start before position 1")
sc(G, "substr and length count characters in UTF-8", "1188-1192; 1953-1955; 163-167",
   'BEGIN { s = "a\\303\\251b"; print substr(s, 2, 1), length(s) }', "\u00e9 3\n", locale="C.UTF-8",
   defect="byte-based substr or length in a UTF-8 locale")

# --- H. index / match / RSTART / RLENGTH -----------------------------------
H = "index / match / RSTART / RLENGTH"
sc(H, "index with an empty needle", "1155-1157", 'BEGIN { print index("abc", ""), index("", "") }', "1 1\n",
   status="observational",
   note="The text does not say whether an empty string 'occurs' in s. The literal reading is that it occurs first at position 1, including in an empty s.",
   defect="(observational) empty-needle convention")
sc(H, "index basic cases, including an empty haystack", "1155-1157",
   'BEGIN { print index("", "a"), index("abc", "c"), index("abcabc", "ca") }', "0 3 3\n",
   defect="an off-by-one in index, or a crash on an empty haystack")
sc(H, "match of an ERE that matches empty", "1162-1165",
   'BEGIN { print match("abc", /x*/), RSTART, RLENGTH }', "1 1 0\n",
   defect="an empty match is reported as no match (0, -1)")
sc(H, "match of /$/ is at the end of the string", "1162-1165", 'BEGIN { print match("abc", /$/), RSTART, RLENGTH }',
   "4 4 0\n", status="portable (provisional)",
   note="The empty match is after the last character, which is position 4 when numbering from 1.",
   defect="an empty match at the end is reported as 0, or as position 3")
sc(H, "A failed match resets RSTART and RLENGTH", "1164-1165; 831-833",
   'BEGIN { match("abc", /b/); a = RSTART " " RLENGTH; match("abc", /z/); print a, RSTART, RLENGTH }', "2 1 0 -1\n",
   defect="RSTART or RLENGTH keep their values from the earlier match")
sc(H, "RSTART and RLENGTH count characters in UTF-8", "1162-1165; 1953-1955",
   'BEGIN { print match("\\303\\251\\303\\251ab", /ab/), RLENGTH; print match("x\\303\\251", /\\303\\251/), RLENGTH }',
   "3 2\n2 1\n", locale="C.UTF-8", defect="byte offsets in RSTART or RLENGTH")
sc(H, "Leftmost beats longer; then longest at the same start", "838 (XBD 9.1 and 9.4); 1162-1165; 1176-1180",
   'BEGIN { print match("zabcd", /abcd|za/), RLENGTH; s = "zabcd"; sub(/abcd|za/, "<&>", s); print s; print match("abcd", /ab|abcd/), RLENGTH }',
   "1 2\n<za>bcd\n1 4\n",
   note="This replaces redundant leftmost-longest tests. The longer alternative starts later, so the earlier, shorter match wins.",
   defect="the longest alternative is chosen over the leftmost (an NFA or alternation-order bug)")
sc(H, "Other functions do not set RSTART or RLENGTH", "831-833; 823-824; 1162-1165",
   'BEGIN { match("abc", /c/); s = "a"; sub(/a/, "x", s); t = "b"; gsub(/b/, "y", t); n = split("a b", A); print RSTART, RLENGTH, index("abc", "a") }',
   "3 1 1\n", defect="sub, gsub, split or index change RSTART or RLENGTH")

# --- I. split -------------------------------------------------------------
I = "split"
sc(I, "split with fs \" \" uses default field splitting", "1166-1172; 955-963",
   'BEGIN { n = split("  a b\\t c  ", A, " "); print n, A[1], A[3] }', "3 a c\n", status="portable (provisional)",
   note="This applies the FS rules (955-969) to fs. 1169 says 'with the ERE fs', so ChatGPT should confirm the reading.",
   defect="fs \" \" is used as a single-space ERE")
sc(I, "split with a single-character fs \".\" is literal", "1166-1172; 960-965",
   'BEGIN { n = split("a.b.c", A, "."); print n, A[2] }', "3 b\n", status="portable (provisional)",
   note="This uses the same FS-rules reading as the previous scenario. A pure ERE reading gives 6 empty elements.",
   defect="a single-character fs is compiled as an ERE")
sc(I, "split deletes every old element first", "1168-1169",
   'BEGIN { A[1] = "old"; A[9] = "x"; n = split("p q", A); print n, length(A), (9 in A) }', "2 2 0\n",
   defect="stale elements beyond n survive")
sc(I, 'split("", A) empties the array', "1168-1169; 2345-2346",
   'BEGIN { A[1]; A[2]; n = split("", A); print n, length(A) }', "0 0\n",
   defect="split of an empty string leaves elements, or returns 1")
sc(I, "split elements are numeric strings", "606; 711-717",
   'BEGIN { split("10 9 abc", A); print (A[1] > A[2]), (A[3] > A[1]), ("10" > "9") }', "1 1 0\n",
   defect="split elements compare as strings")
sc(I, "The source string is an element of the target array", "1168-1169",
   'BEGIN { A[1] = "x y z"; n = split(A[1], A); print n, A[1], A[3] }', "3 x z\n",
   defect="the target is cleared before the source is read")
sc(I, "An ERE fs with leading and trailing separators", "1166-1172; 968-969",
   'BEGIN { n = split(":a::b:", A, /:/); print n, "[" A[1] "]", "[" A[3] "]", "[" A[5] "]" }', "5 [] [] []\n",
   defect="empty leading or trailing elements are dropped")

# --- J. whole-array delete ------------------------------------------------
J = "delete array"
sc(J, "delete A, then reuse A", "1022-1032",
   'BEGIN { A[1]; A[2]; A["x"]; delete A; print length(A), (1 in A); A["y"] = 5; print length(A), A["y"] }',
   "0 0\n1 5\n", defect="the array is unusable after delete A, or elements remain")
sc(J, "delete a on an array parameter clears the caller's array", "1022-1032; 1111-1113",
   'function clr(a) { delete a } BEGIN { A[1]; A[2]; clr(A); print length(A); A[3] = 1; print length(A) }', "0\n1\n",
   defect="delete of a parameter clears only a local copy, or breaks the reference")
sc(J, "delete A[k] inside for (k in A)", "1022-1032",
   'BEGIN { for (i = 1; i <= 100; i++) A[i] = i; for (k in A) delete A[k]; print length(A) }', "0\n",
   defect="the iteration is disturbed by deleting the current element (some elements are left)")

# --- K. stateful combinations ---------------------------------------------
K = "stateful combinations"
sc(K, "exit with no expression in END keeps the earlier status", "1038-1042",
   '{ exit 3 } END { exit }', "", stdin="a\n", exit=3,
   defect="a bare exit in END resets the status to 0")
sc(K, "exit in BEGIN runs END and reads no input", "1038-1040",
   'BEGIN { print "b"; exit 2 } { print "main" } END { print "e" }', "b\ne\n", stdin="x\n", exit=2,
   defect="END is skipped, or the main rule runs")
sc(K, "exit inside END stops the remaining END actions", "1039-1040",
   'END { print "1"; exit 4 } END { print "2" }', "1\n", exit=4,
   defect="later END actions still run")
sc(K, "getline var < file leaves NR, FNR, NF and $0 alone", "1243-1250",
   '{ getline v < "f"; print NR, FNR, NF, $0, v }', "1 1 3 a b c L1\n", files={"f": "L1\nL2\n"}, stdin="a b c\n",
   defect="redirected getline var updates NR or FNR")
sc(K, "Plain getline updates NR, FNR, NF and $0", "1236-1238",
   'NR == 1 { getline; print NR, FNR, NF, $0 }', "2 2 2 b c\n", stdin="a\nb c\n",
   defect="NF is not recomputed after getline")
sc(K, "getline var updates NR and FNR, not $0 or NF", "1239-1242",
   'NR == 1 { getline v; print NR, FNR, NF, $0, v }', "2 2 1 a b c\n", stdin="a\nb c\n",
   defect="getline var overwrites $0, or does not count the record")
sc(K, "Assigning $(NF+2) creates empty fields and rebuilds with OFS", "739-741; 50-53",
   'BEGIN { OFS = "-" } { $(NF + 2) = "z"; print; print NF }', "a-b--z\n4\n", stdin="a b\n",
   defect="the intervening field is missing, or $0 is not rebuilt")
sc(K, "Changing OFS without touching a field leaves $0 alone", "50-53",
   'BEGIN { OFS = "-" } { print $0; $1 = $1; print $0 }', "a b c\na-b-c\n", stdin="a b c\n",
   defect="$0 is rebuilt eagerly when OFS changes, or not rebuilt after $1 = $1")
sc(K, "CONVFMT for subscripts and concatenation, OFMT for print, %d for integers", "590-595; 783-785; 815-818",
   'BEGIN { CONVFMT = "%.2g"; OFMT = "%.4f"; x = 3.14159; a[x] = 1; for (k in a) print k; print x; print x ""; print 17 "" }',
   "3.1\n3.1416\n3.1\n17\n", defect="OFMT is used for subscripts, or CONVFMT for integers")

# --- L. multi-file --------------------------------------------------------
L = "multi-file"
sc(L, "FNR, NR and FILENAME with an empty middle file", "797-803; 811-814",
   'FNR == 1 { print FILENAME, NR } END { print FILENAME, NR, FNR }', "f1 1\nf2 3\nf2 3 1\n",
   operands=["f1", "empty", "f2"], files={"f1": "a\nb\n", "empty": "", "f2": "c\n"},
   defect="FNR is not reset for the file after an empty one, or NR is miscounted")
sc(L, "FILENAME and FNR in END when the last file is empty", "797-803",
   'END { print FILENAME, NR, FNR }', "empty 2 0\n", operands=["f1", "empty"],
   files={"f1": "a\nb\n", "empty": ""}, status="observational",
   note="Is an empty file 'processed' (799, 803)? The literal reading says yes: FILENAME is 'empty' and FNR is 0.",
   defect="(observational) END state after an empty last file")
sc(L, "getline < FILENAME is a separate stream from the main input", "1243-1248",
   'FNR == 1 { while ((getline l < FILENAME) > 0) n++; close(FILENAME) } END { print n, NR }', "3 3\n",
   operands=["f1"], files={"f1": "1\n2\n3\n"},
   defect="the redirected stream shares or moves the main input's position")
sc(L, "nextfile in each file: NR counts the record that called it", "812-814; 1035-1037",
   'FNR == 2 { nextfile } { print FILENAME, FNR, NR } END { print NR }', "f1 1 1\nf2 1 3\n4\n",
   operands=["f1", "f2"], files={"f1": "a\nb\nc\n", "f2": "d\ne\n"},
   defect="skipped records are counted in NR, or the record that ran nextfile is not")
sc(L, "An FS= operand between files applies to the next file", "112-114; 955-957",
   '{ print $1 }', "a:b\na\n", operands=["f1", "FS=:", "f2"], files={"f1": "a:b c\n", "f2": "a:b c\n"},
   defect="the FS assignment is applied too early, or to the current record")
