#!/usr/bin/env python3
"""Summarise runner reports, keeping the three kinds of result apart.

  portable       -> portable CONFORMANCE: a failure is a candidate POSIX
                    violation (still to be adjudicated against the text)
  observational  -> observational COMPATIBILITY: agreement with recorded
                    practice; a failure is never evidence of a POSIX violation
  nonportable    -> unspecified/implementation-defined behaviour; reported for
                    information only

usage: python3 tools/summarize.py REPORT.json [REPORT.json ...] [--markdown]
"""
import json
import sys

KINDS = [("portable", "Portable conformance"), ("observational", "Observational compatibility"),
         ("nonportable", "Nonportable (informational)")]


def summarise(path: str) -> tuple[str, dict, dict]:
    report = json.load(open(path))
    totals = {k: [0, 0] for k, _ in KINDS}
    failing = {k: [] for k, _ in KINDS}
    for r in report["results"]:
        k = r["classification"]
        totals.setdefault(k, [0, 0])
        failing.setdefault(k, [])
        totals[k][1] += 1
        if r["status"] == "PASS":
            totals[k][0] += 1
        else:
            failing[k].append(r["id"].removeprefix("AWK-"))
    return report["label"], totals, failing


def main(argv: list[str]) -> int:
    markdown = "--markdown" in argv
    paths = [a for a in argv if a != "--markdown"]
    if not paths:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2
    rows = [summarise(p) for p in paths]
    if markdown:
        print("| Implementation | " + " | ".join(f"{t}" for _, t in KINDS) + " | Failing: portable | Failing: observational | Failing: nonportable |")
        print("|---|" + "---:|" * len(KINDS) + "---|---|---|")
        for label, totals, failing in rows:
            cells = [f"{totals[k][0]}/{totals[k][1]}" for k, _ in KINDS]
            fails = [", ".join(failing[k]) or "none" for k, _ in KINDS]
            print(f"| {label} | " + " | ".join(cells) + " | " + " | ".join(fails) + " |")
    else:
        for label, totals, failing in rows:
            print(label)
            for k, title in KINDS:
                p, n = totals[k]
                print(f"  {title:30} {p:4}/{n:<4} failing: {', '.join(failing[k]) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
