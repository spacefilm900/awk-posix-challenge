#!/usr/bin/env python3
"""Run the v0.6 proposal scenarios on the local implementations, for information only.

usage: proposals/v0.6/probe.py [--json OUT] [--markdown OUT] [--impl NAME=CMD ...]

The expectations in scenarios.py come from the POSIX text. This script only
records what each implementation does: it never changes an expectation.
"""
import argparse, json, os, shlex, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scenarios  # noqa: E402

DEFAULT = [
    ("mawk", "mawk"),
    ("gawk --posix", "/workspace/refs/local/bin/gawk --posix"),
    ("onetrue", "/workspace/refs/onetrue-awk/a.out"),
    ("pyawk", "env PYTHONPATH=/workspace/pyawk python3 -m pyawk"),
    ("hawk", "/workspace/hawk/target/release/hawk"),
]


def run(cmd, s):
    with tempfile.TemporaryDirectory(prefix="v06-") as td:
        wd = Path(td)
        for name, content in s["files"].items():
            (wd / name).write_bytes(content.encode())
        argv = shlex.split(cmd) + s["args"]
        if not s["noprog"]:
            (wd / "prog.awk").write_text(s["prog"] + "\n")
            argv += ["-f", "prog.awk"]
        argv += s["operands"]
        env = dict(os.environ, LC_ALL=s["locale"], LANG=s["locale"])
        try:
            p = subprocess.run(argv, input=s["stdin"].encode(), cwd=wd, env=env, capture_output=True, timeout=10)
            return p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace"), p.returncode
        except subprocess.TimeoutExpired:
            return "<timeout>", "", None


def verdict(s, out, err, rc):
    ok = out == s["out"] and (rc == s["exit"] if isinstance(s["exit"], int) else rc not in (0, None))
    if s["err"] == "empty":
        ok = ok and err == ""
    return "PASS" if ok else "DIFF"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--impl", action="append", default=[])
    ap.add_argument("--json")
    a = ap.parse_args()
    impls = [tuple(x.split("=", 1)) for x in a.impl] or DEFAULT
    res = []
    for i, s in enumerate(scenarios.S, 1):
        sid = f"P{i:02d}"
        row = {"id": sid, "title": s["title"], "status": s["status"], "results": {}}
        for name, cmd in impls:
            out, err, rc = run(cmd, s)
            row["results"][name] = {"verdict": verdict(s, out, err, rc), "stdout": out, "stderr": err, "exit": rc}
        res.append(row)
        print(sid, s["status"][:13].ljust(13), " ".join(f"{n}={r['verdict']}" for n, r in row["results"].items()))
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
