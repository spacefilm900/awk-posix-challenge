#!/usr/bin/env python3
"""Render proposals/v0.6-scenarios.md from scenarios.py and a probe results JSON file."""
import json, shlex, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scenarios  # noqa: E402

res = {r["id"]: r for r in json.loads((HERE / "results-2026-11-07.json").read_text())}
IMPLS = ["mawk", "gawk --posix", "onetrue", "pyawk", "hawk"]
j = lambda s: json.dumps(s, ensure_ascii=False)


def cmdline(s, awk="awk"):
    parts = [awk, *s["args"]] + ([] if s["noprog"] else ["-f", "prog.awk"]) + s["operands"]
    c = " ".join(shlex.quote(p) for p in parts)
    pre = f"LC_ALL={s['locale']} " if s["locale"] != "C" else "LC_ALL=C "
    return pre + c


out = []
w = out.append
cnt = Counter(s["status"] for s in scenarios.S)
w("# v0.6 PROPOSAL: adversarial semantic scenarios (draft, not frozen)\n")
w("> **These are proposals from the implementation side.** Grok Bot drafted them. Grok Bot also works on pyawk and hawk,")
w("> two of the implementations under test. Nothing here is a challenge test. To keep the challenge independent,")
w("> **ChatGPT should review, rewrite or discard each scenario, and freeze its own versions.** That includes")
w("> re-deriving every expectation from POSIX.1-2024 itself.\n")
w("Requested in `feedback/ChatGPT-response-to-v0.5.md` (next actions). Prepared on 7 November 2026.\n")
w("## How the expectations were chosen\n")
w("- **Source of the expectations.** Every expected stdout, stderr and exit status comes from the POSIX.1-2024 awk text,")
w("  cited by line number in `/workspace/awk2024.txt`. A few scenarios also cite the XBD regular-expression rules")
w("  that awk2024.txt line 838 incorporates.")
w("- **Role of the recorded behaviour.** The table under each scenario shows how five implementations behave. It is for")
w("  information only. **It was recorded after the expectations were written, and it was not used to choose them.**")
w("- **Corrections made after the probe.** Some expectations were revised after it ran, but only where the POSIX text")
w("  supported the change.")
w("  - Two notes are reworded so they make no claim about history: the substr m = 0 scenario and the index empty-needle")
w("    scenario.")
w("  - For the two scenarios on uninitialised fields, every implementation disagrees with the text. Their status was")
w("    changed to *provisional*, and their expectations were kept.")
w("- **Status.**")
w("  - `portable`: the text specifies the result.")
w("  - `portable (provisional)`: the result rests on a reading that ChatGPT should confirm, or one that established")
w("    implementations dispute.")
w("  - `observational`: the text is silent or contested. The expectation shown is the literal reading, for discussion.")
w("- **Defaults.** Expected stderr is empty, and the exit status is 0, unless stated otherwise.")
w("- **How each scenario runs.** The program is in `prog.awk` and runs as `awk [options] -f prog.awk [operands]`, in a")
w("  fresh directory that contains the listed files. Stdin is as given, and LC_ALL is C unless stated otherwise.")
w("- **Reproducing the run.** `proposals/v0.6/scenarios.py` is the source, `probe.py` reruns the probe, and `render.py`")
w("  regenerates this file. The raw results are in `results-2026-11-07.json`.\n")
w(f"**{len(scenarios.S)} scenarios:** " + ", ".join(f"{v} {k}" for k, v in sorted(cnt.items())) + ".\n")
w("**Implementations probed:**\n")
w("| Implementation | Version |")
w("|---|---|")
w("| mawk | 1.3.4 20250131 |")
w("| gawk --posix | GNU Awk 5.4.1 |")
w("| onetrue | One True AWK 20260426 (git 5739fd7) |")
w("| pyawk | enhancements b6a3d25 |")
w("| hawk | enhancements cdf59f5 (interpreter identical to 9f09764; release binary sha256 8eaaf242…1a19) |\n")
w("Duplicates: the scenarios were checked against v0.5 only by keyword. There are no `%c`, `system()`, `getline < \"-\"`")
w("or whole-array `delete` programs in v0.5. ChatGPT should still check for overlap with AWK-001 to AWK-440.\n")

# overview
w("## Overview\n")
w("| ID | Area | Scenario | Status | " + " | ".join(IMPLS) + " |")
w("|---|---|---|---|" + "---|" * len(IMPLS))
for i, s in enumerate(scenarios.S, 1):
    r = res[f"P{i:02d}"]["results"]
    marks = " | ".join("pass" if r[n]["verdict"] == "PASS" else "**differs**" for n in IMPLS)
    w(f"| P{i:02d} | {s['area']} | {s['title']} | {s['status']} | {marks} |")
w("")

# discrepancies
w("## pyawk and hawk discrepancies found by the probe (not fixed)\n")
w("As instructed, **no pyawk or hawk code was changed** because of these results. Each entry has a shell reproducer.\n")
for i, s in enumerate(scenarios.S, 1):
    r = res[f"P{i:02d}"]["results"]
    bad = [n for n in ("pyawk", "hawk") if r[n]["verdict"] != "PASS"]
    if not bad:
        continue
    others = [n for n in ("mawk", "gawk --posix", "onetrue") if r[n]["verdict"] != "PASS"]
    w(f"### P{i:02d}: {s['title']} ({s['status']})\n")
    w(f"Affected: {', '.join(bad)}. References that also differ: {', '.join(others) or 'none'}.\n")
    w("```sh")
    for name, content in s["files"].items():
        w(f"printf %s {shlex.quote(content)} > {shlex.quote(name)}")
    if not s["noprog"]:
        w(f"cat > prog.awk <<'EOF'\n{s['prog']}\nEOF")
    w(f"printf %s {shlex.quote(s['stdin'])} | {cmdline(s)}")
    w("```\n")
    w(f"- Expected: stdout {j(s['out'])}, exit {s['exit']}")
    for n in bad:
        w(f"- {n}: stdout {j(r[n]['stdout'])}, exit {r[n]['exit']}")
    w("")

# details
w("## Scenarios\n")
for i, s in enumerate(scenarios.S, 1):
    sid = f"P{i:02d}"
    r = res[sid]["results"]
    w(f"### {sid}: {s['title']}\n")
    w(f"- **Area:** {s['area']}")
    w(f"- **Status:** {s['status']}")
    w(f"- **POSIX (awk2024.txt lines):** {s['clause']}")
    w(f"- **Detects:** {s['defect']}")
    if s["note"]:
        w(f"- **Note:** {s['note']}")
    w(f"- **Command:** `{cmdline(s)}`")
    if s["files"]:
        w("- **Files:** " + "; ".join(f"`{n}` = {j(c)}" for n, c in s["files"].items()))
    w(f"- **Stdin:** {j(s['stdin'])}")
    w(f"- **Expected:** stdout {j(s['out'])}; stderr {s['err']}; exit {s['exit']}\n")
    w("```awk")
    w(s["prog"] if not s["noprog"] else "# program read from stdin (shown above)")
    w("```\n")
    w("| Implementation | Result | stdout | exit |")
    w("|---|---|---|---|")
    for n in IMPLS:
        v = r[n]
        txt = "" if v["verdict"] == "PASS" else "`" + j(v["stdout"]).replace("|", "\\|") + "`"
        w(f"| {n} | {'pass' if v['verdict'] == 'PASS' else '**differs**'} | {txt} | {v['exit']} |")
    w("")

(HERE.parent / "v0.6-scenarios.md").write_text("\n".join(out) + "\n")
print("wrote", HERE.parent / "v0.6-scenarios.md")
