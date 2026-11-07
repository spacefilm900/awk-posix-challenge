#!/usr/bin/env python3
"""Independent reproducers for the 6 regex probe lines where hawk differed from the
unanimous live references in hawk's CI differential job (run 42384847354).

Analysis only: nothing is fixed. The probe program is byte-identical to the one
in hawk tools/regex_check.py and pyawk scripts/regex_corpus.py. Run this script
from anywhere. It writes regex-reproducers.json next to itself.
"""
import json, os, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATTERN = r"\xc3\xa9"          # the corpus pattern: category utf8-escapes
POSIX_SPELLING = r"\303\251"   # the same bytes written with POSIX octal escapes (contrast only)
# The 6 input lines (bytes). 0xE9 on its own is invalid UTF-8.
INPUTS = [b"\xc3\xa9", b"\xc3\xa9e", b"a\xc3\xa9b", b"\xc3\xa9\xc3\xa9", b"\xe9\xc3\xa9",
          "aé€日😀".encode()]
G = "/workspace/refs/local/bin/gawk"
IMPLS = [
    ("hawk", ["/workspace/hawk/target/release/hawk"], {}),
    ("pyawk", ["python3", "-m", "pyawk"], {"PYTHONPATH": "/workspace/pyawk"}),
    ("mawk", ["mawk"], {}),
    ("gawk --posix", [G, "--posix"], {}),
    ("gawk", [G], {}),
    ("onetrue", ["/workspace/refs/onetrue-awk/a.out"], {}),
    ("busybox", ["/workspace/refs/busybox/busybox", "awk"], {}),
]


def probe(pattern):
    p = "/" + pattern + "/"
    return ("{ s = $0; r = match(s, P); printf \"%d %d %d\", r, RLENGTH, (s ~ P)\n"
            "  t = s; n = gsub(P, \"<&>\", t); printf \" %d %s\", n, t\n"
            "  n = split(s, A, P); printf \" %d\", n\n"
            "  for (i = 1; i <= n; i++) printf \":%s\", A[i]\n"
            "  print \"\" }\n").replace("P", p)


def run(argv, extra, prog, data, locale):
    env = dict(os.environ, LC_ALL=locale, **extra)
    p = subprocess.run([*argv, prog], input=data + b"\n", capture_output=True, env=env, timeout=20)
    return {"stdout_hex": p.stdout.hex(" "), "stdout": p.stdout.decode("utf-8", "backslashreplace").rstrip("\n"),
            "stderr": p.stderr.decode("utf-8", "backslashreplace").strip(), "exit": p.returncode}


out = {"pattern": PATTERN, "probe_program": probe(PATTERN), "cases": []}
for i, data in enumerate(INPUTS, 1):
    case = {"n": i, "input_hex": data.hex(" "), "runs": {}}
    for locale in ("C.UTF-8", "C"):
        for spelling, pat in (("corpus \\x", PATTERN), ("POSIX octal", POSIX_SPELLING)):
            key = f"{locale} | {spelling}"
            case["runs"][key] = {n: run(a, e, probe(pat), data, locale) for n, a, e in IMPLS}
    out["cases"].append(case)
(HERE / "regex-reproducers.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
for c in out["cases"]:
    print(f"#{c['n']} input {c['input_hex']}")
    for key, runs in c["runs"].items():
        print(f"  [{key}]")
        for n, r in runs.items():
            print(f"    {n:13} {r['stdout']!s:40} exit {r['exit']} {r['stderr'][:60]}")
