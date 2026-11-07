#!/usr/bin/env python3
"""Strict-grammar WARNING check for challenge cases.

This is a warning signal, NOT an oracle. It flags two kinds of thing:

  1. Programs that a strict reference awk (One True AWK by default) rejects
     at parse time. It runs each case the way tools/runner.py does, and flags
     stderr containing "syntax error", "illegal statement" or "bailing out".
  2. Constructs that a lexical scan finds outside the POSIX awk grammar
     (awk2024.txt lines 1434-1700), or whose behaviour is unspecified:
       - an unparenthesised comparison in a print/printf expression list
         (print_expr has no comparison operators; lines 1537-1597);
       - `**` and `**=` (not POSIX operators);
       - gawk/mawk-only built-in functions, variables and keywords;
       - `func` used as a keyword (historical, see RATIONALE line 2140);
       - `|&` (gawk coprocess);
       - GNU regex operators (\\y \\< \\> \\s \\S \\w \\W \\` \\') in ERE tokens;
       - unparenthesised concatenation after `getline <` or before
         `| getline` (ambiguous; lines 1231-1233 and 1251-1253);
       - a multi-character RS (unspecified, line 827).

A flag means "review this case by hand against the grammar". It does not
show that the case is wrong. Equally, a clean result does not show the case
is valid. A case that is nonportable or observational may use flagged
constructs on purpose; their class is printed so that a reviewer can tell.

Usage: tools/grammar_check.py [--onetrue PATH] [--no-run] [--ids ...] [--json OUT]
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GAWK_FUNCS = ("gensub systime strftime mktime asort asorti patsplit and or xor lshift rshift compl "
              "strtonum isarray typeof bindtextdomain dcgettext dcngettext mkbool").split()
GAWK_VARS = ("IGNORECASE RT FPAT PROCINFO FIELDWIDTHS ERRNO ARGIND BINMODE LINT TEXTDOMAIN "
             "SYMTAB FUNCTAB").split()
GAWK_KW = "BEGINFILE ENDFILE switch".split()
GNU_RE = re.compile(r"\\[y<>sSwW`']")


def lex(src):
    """A small awk lexer. It yields (kind, text) tuples, where kind is one of
    str, ere, num, name, nl or op. It is good enough for warnings, not a full
    parser."""
    i, n, toks = 0, len(src), []
    def prev_is_operand():
        for k, t in reversed(toks):
            if k == "nl":
                return False
            return k in ("str", "ere", "num", "name") and t not in KEYWORDS_BEFORE_ERE or t in (")", "]", "$", "++", "--")
        return False
    while i < n:
        c = src[i]
        if c == "\\" and i + 1 < n and src[i + 1] == "\n":
            i += 2; continue
        if c in " \t\r":
            i += 1; continue
        if c == "#":
            while i < n and src[i] != "\n":
                i += 1
            continue
        if c == "\n":
            toks.append(("nl", "\n")); i += 1; continue
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            toks.append(("str", src[i:j + 1])); i = j + 1; continue
        if c == "/" and not prev_is_operand():
            j, inbr = i + 1, False
            while j < n and src[j] != "\n":
                if src[j] == "\\":
                    j += 2; continue
                if src[j] == "[":
                    inbr = True
                elif src[j] == "]":
                    inbr = False
                elif src[j] == "/" and not inbr:
                    break
                j += 1
            toks.append(("ere", src[i:j + 1])); i = j + 1; continue
        m = re.match(r"[A-Za-z_][A-Za-z_0-9]*", src[i:])
        if m:
            toks.append(("name", m.group())); i += m.end(); continue
        m = re.match(r"(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?", src[i:])
        if m:
            toks.append(("num", m.group())); i += m.end(); continue
        for op in ("**=", "**", "|&", "&&", "||", "==", "!=", "<=", ">=", ">>", "++", "--",
                   "+=", "-=", "*=", "/=", "%=", "^="):
            if src.startswith(op, i):
                toks.append(("op", op)); i += len(op); break
        else:
            toks.append(("op", c)); i += 1
    return toks


KEYWORDS_BEFORE_ERE = {"print", "printf", "return", "in", "case", "if", "while", "do", "else"}


def print_list_comparisons(toks):
    """Flag a print or printf whose expression list, at paren depth 0,
    contains a comparison: <, <=, ==, != or >=. ('~' and '!~' are allowed in
    print_expr, lines 1554-1572.) A '>' at depth 0
    always ends the list and starts a redirection. A '<' at depth 0 is the
    reverse ambiguity, which the grammar does not allow either."""
    out = []
    for i, (k, t) in enumerate(toks):
        if k != "name" or t not in ("print", "printf"):
            continue
        depth, j = 0, i + 1
        while j < len(toks):
            k2, t2 = toks[j]
            if k2 == "nl" and depth == 0:
                break
            if k2 == "op":
                if t2 in "([":
                    depth += 1
                elif t2 in ")]":
                    if depth == 0:
                        break
                    depth -= 1
                elif depth == 0 and t2 in (";", "}", ">", ">>", "|", "|&"):
                    break
                elif depth == 0 and t2 in ("<", "<=", "==", "!=", ">="):
                    out.append(f"{t} list contains unparenthesised '{t2}'")
                    break
            elif k2 == "name" and depth == 0 and t2 == "in" and j > i + 1:
                # `print x in a` is ambiguous with for-in; POSIX permits 'in' in non_unary_expr
                pass
            j += 1
    return out


def static_flags(src):
    toks = lex(src)
    flags = print_list_comparisons(toks)
    for i, (k, t) in enumerate(toks):
        nxt = toks[i + 1] if i + 1 < len(toks) else ("", "")
        if k == "op" and t in ("**", "**="):
            flags.append(f"non-POSIX operator '{t}'")
        if k == "op" and t == "|&":
            flags.append("gawk coprocess '|&'")
        if k == "name" and t in GAWK_FUNCS and nxt == ("op", "("):
            flags.append(f"non-POSIX function '{t}()'")
        if k == "name" and t in GAWK_VARS:
            flags.append(f"gawk-specific variable '{t}'")
        if k == "name" and t in GAWK_KW:
            flags.append(f"gawk keyword '{t}'")
        if k == "name" and t == "func" and nxt[0] == "name":
            flags.append("'func' keyword (historical; POSIX uses 'function')")
        if k == "op" and t == "@":
            flags.append("gawk directive '@...'")
        if k == "ere" and GNU_RE.search(t):
            flags.append(f"GNU regex operator in {t}")
        if k == "name" and t == "getline":
            # simple_get '<' expr: an unparenthesised concatenation here is ambiguous, lines 1251-1253
            j = i + 1
            if j < len(toks) and toks[j][0] == "name" and toks[j][1] not in ("in",):
                j += 1
            if j + 2 < len(toks) and toks[j] == ("op", "<") and toks[j + 1][0] in ("str", "name", "num") \
                    and toks[j + 2][0] in ("str", "name", "num") and toks[j + 2][1] != "in":
                flags.append("unparenthesised concatenation after 'getline <' (ambiguous, lines 1251-1253)")
        if k == "op" and t == "|" and nxt == ("name", "getline") and i >= 2:
            # cmd | getline: unparenthesised operators to the left of '|' are ambiguous (lines 1231-1233)
            a1, a2 = toks[i - 2], toks[i - 1]
            if a1[0] in ("str", "name", "num") and a2[0] in ("str", "name", "num") \
                    and a1[1] not in KEYWORDS_BEFORE_ERE and a1[1] not in ("in", "getline"):
                flags.append("unparenthesised concatenation before '| getline' (ambiguous, lines 1231-1233)")
        if k == "name" and t == "RS" and nxt == ("op", "=") and i + 2 < len(toks):
            k3, t3 = toks[i + 2]
            if k3 == "str":
                try:
                    val = t3[1:-1].encode().decode("unicode_escape")
                except Exception:
                    val = t3[1:-1]
                if len(val) > 1:
                    flags.append(f"multi-character RS {t3} (unspecified, line 827)")
    return sorted(set(flags))


def option_sources(case, cdir):
    """Return the program texts a case runs: program.awk, plus any -f files,
    which are fixtures."""
    srcs = [("program.awk", (cdir / "program.awk").read_text(errors="replace"))]
    opts = case.get("options", [])
    for i, o in enumerate(opts):
        if o == "-f" and i + 1 < len(opts) and (cdir / opts[i + 1]).is_file():
            srcs.append((opts[i + 1], (cdir / opts[i + 1]).read_text(errors="replace")))
    return srcs


PARSE_ERR = re.compile(r"syntax error|illegal statement|bailing out|non-terminated|newline in (string|regular)")


def run_strict(awk, case, cdir, timeout, program=None):
    """Run the case exactly as tools/runner.py builds it: fixtures copied into
    a temporary cwd, then argv = awk + options + ['-f', program.awk] +
    operands, with the same stdin and locale. Return the strict awk's parse
    diagnostic, or None."""
    with tempfile.TemporaryDirectory(prefix="awk-grammar-") as td:
        wd = Path(td)
        for f in case.get("fixtures", []):
            dest = wd / f
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(cdir / f, dest)
        prog = program or (cdir / "program.awk")
        argv = [awk] + case.get("options", []) + ["-f", str(prog)] + case.get("operands", [])
        env = os.environ.copy()
        env.update({"LC_ALL": case.get("locale", "C"), "LANG": case.get("locale", "C")})
        env.update(case.get("env", {}))
        sname = case.get("stdin", "stdin.txt")
        stdin = (cdir / sname).read_bytes() if sname is not None and (cdir / sname).is_file() else b""
        try:
            r = subprocess.run(argv, input=stdin, cwd=wd, env=env, capture_output=True,
                               timeout=case.get("timeout", timeout))
        except subprocess.TimeoutExpired:
            return None
        err = r.stderr.decode(errors="replace")
        if PARSE_ERR.search(err):
            return " / ".join(l.strip() for l in err.strip().splitlines()[:3])
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--onetrue", default=os.environ.get("ONETRUE_AWK", "/workspace/refs/onetrue-awk/a.out"),
                    help="strict reference awk used for the parse check")
    ap.add_argument("--no-run", action="store_true", help="static scan only")
    ap.add_argument("--ids", nargs="*")
    ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--json")
    a = ap.parse_args()
    run = not a.no_run and Path(a.onetrue).exists()
    if not a.no_run and not run:
        print(f"note: strict awk {a.onetrue} not found; static scan only", file=sys.stderr)
    report, ncase = [], 0
    for cdir in sorted((ROOT / "cases").glob("AWK-*")):
        if a.ids and cdir.name not in a.ids:
            continue
        case = json.loads((cdir / "case.json").read_text())
        ncase += 1
        flags = []
        for name, src in option_sources(case, cdir):
            flags += [f"{name}: {f}" for f in static_flags(src)]
        if run:
            d = run_strict(a.onetrue, case, cdir, a.timeout)
            if d:
                flags.append(f"strict awk rejects program: {d}")
        if flags:
            report.append({"id": cdir.name, "classification": case.get("classification"), "flags": flags})
    for r in report:
        print(f"WARN {r['id']} [{r['classification']}]")
        for f in r["flags"]:
            print(f"    {f}")
    by = {}
    for r in report:
        by[r["classification"]] = by.get(r["classification"], 0) + 1
    print(f"\n{len(report)} of {ncase} cases flagged ({', '.join(f'{k} {v}' for k, v in sorted(by.items())) or 'none'}); "
          f"strict-awk parse check {'ON (' + a.onetrue + ')' if run else 'OFF'}.")
    print("These are warnings for manual review against awk2024.txt lines 1434-1700, not verdicts.")
    if a.json:
        Path(a.json).write_text(json.dumps({"cases": ncase, "flagged": report}, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
