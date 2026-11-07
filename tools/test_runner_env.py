#!/usr/bin/env python3
"""Harness test for the runner's env_clear option (not an AWK conformance case).

It copies tools/runner.py into a temporary tree containing synthetic cases
(named AWK-ENV*, because the runner only picks up AWK-* folders), runs it with an installed awk, and checks which environment variables
reach the awk program.  The harness's own environment (APC_HARNESS_LEAK,
PYTHONPATH) is kept separate from the value the cases test through ENVIRON
(APC_CASE_VALUE, set by each case's "env").

  AWK-ENV1  env_clear: true   -> harness variables are removed; case env and
                              LC_ALL are present
  AWK-ENV2  env_clear absent  -> harness variables are inherited
  AWK-ENV3  env_clear: true, with --cmd 'env PYTHONPATH=... AWK' -> an explicit
         command environment survives env_clear

With --pyawk-dir DIR it also shows the documented pitfall: under env_clear,
`python3 -m pyawk` loses PYTHONPATH and fails to import, while
`env PYTHONPATH=DIR python3 -m pyawk` works.

usage: python3 tools/test_runner_env.py [--awk mawk] [--pyawk-dir DIR]
Exit status 0 if every check passes.
"""
import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROGRAM = ('BEGIN { print ENVIRON["APC_HARNESS_LEAK"] "|" ENVIRON["APC_CASE_VALUE"] "|" '
           'ENVIRON["LC_ALL"] "|" ENVIRON["PYTHONPATH"] }\n')


def make_case(cases: pathlib.Path, cid: str, expected: str, env_clear: bool | None) -> None:
    d = cases / cid
    d.mkdir(parents=True)
    meta = {"id": cid, "name": "env-clear-harness", "group": "harness", "classification": "portable",
            "locale": "C", "expected_exit": 0, "stdin": None, "env": {"APC_CASE_VALUE": "010"}}
    if env_clear is not None:
        meta["env_clear"] = env_clear
    (d / "case.json").write_text(json.dumps(meta, indent=2) + "\n")
    (d / "program.awk").write_text(PROGRAM)
    (d / "expected.stdout").write_text(expected)
    (d / "expected.stderr").write_text("")


def run_runner(tree: pathlib.Path, cmd: str, ids: list[str], extra_env: dict[str, str]) -> dict:
    env = dict(os.environ, APC_HARNESS_LEAK="leak", PYTHONPATH="/apc-harness-pythonpath")
    env.update(extra_env)
    out = tree / "report.json"
    subprocess.run([sys.executable, str(tree / "tools" / "runner.py"), "--cmd", cmd, "--ids", *ids,
                    "--output", str(out)], env=env, stdout=subprocess.DEVNULL, check=False)
    return {r["id"]: r for r in json.loads(out.read_text())["results"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--awk", default=None, help="installed awk executable (default: mawk, gawk or awk on PATH)")
    ap.add_argument("--pyawk-dir", default=None)
    args = ap.parse_args()
    awk = args.awk or next((a for a in ("mawk", "gawk", "awk") if shutil.which(a)), None)
    if not awk or not shutil.which(awk):
        print("test_runner_env: no installed awk found; use --awk", file=sys.stderr)
        return 2
    awk = shutil.which(awk)
    failures = 0
    with tempfile.TemporaryDirectory(prefix="apc-env-test-") as td:
        tree = pathlib.Path(td)
        (tree / "tools").mkdir()
        shutil.copyfile(ROOT / "tools" / "runner.py", tree / "tools" / "runner.py")
        cases = tree / "cases"
        make_case(cases, "AWK-ENV1", "|010|C|\n", True)
        make_case(cases, "AWK-ENV2", "leak|010|C|/apc-harness-pythonpath\n", None)
        make_case(cases, "AWK-ENV3", "|010|C|/explicit\n", True)
        checks = [
            ("AWK-ENV1 env_clear removes harness variables", awk, "AWK-ENV1", "PASS"),
            ("AWK-ENV2 default inherits harness variables", awk, "AWK-ENV2", "PASS"),
            ("AWK-ENV3 explicit command environment survives env_clear",
             f"env PYTHONPATH=/explicit {awk}", "AWK-ENV3", "PASS"),
        ]
        if args.pyawk_dir:
            # Same program as AWK-ENV1; only the command differs.
            make_case(cases, "AWK-ENV4", "|010|C|\n", True)
            make_case(cases, "AWK-ENV5", f"|010|C|{args.pyawk_dir}\n", True)
            checks += [
                ("AWK-ENV4 python3 -m pyawk under env_clear loses PYTHONPATH (expected FAIL)",
                 f"{sys.executable} -m pyawk", "AWK-ENV4", "FAIL"),
                ("AWK-ENV5 env PYTHONPATH=DIR python3 -m pyawk works under env_clear",
                 f"env PYTHONPATH={args.pyawk_dir} {sys.executable} -m pyawk", "AWK-ENV5", "PASS"),
            ]
        for label, cmd, cid, want in checks:
            extra = {"PYTHONPATH": args.pyawk_dir} if cid == "AWK-ENV4" else {}
            rec = run_runner(tree, cmd, [cid], extra)[cid]
            ok = rec["status"] == want
            failures += not ok
            detail = ""
            if rec["status"] != "PASS":
                detail = f"  stderr: {rec.get('actual_stderr', '').strip().splitlines()[-1:]}"
            print(f"{'ok  ' if ok else 'BAD '} {label}: {rec['status']}{detail}")
    print(f"test_runner_env: {'all checks passed' if not failures else f'{failures} check(s) failed'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
