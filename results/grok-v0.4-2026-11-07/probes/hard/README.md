# Harder-test probes (exploratory; not part of the corpus)

- `hard_probes.tsv` has four tab-separated columns: name, program, operands (`_` = none), and stdin file (`-` = /dev/null).
- `run.sh` runs every probe on pyawk, hawk, mawk, gawk --posix, gawk, onetrue-awk and BusyBox with `LC_ALL=C`.
  Run it from this directory.
- `hard_probes_output.txt` is the recorded output. Re-running reproduced it byte for byte on 2026-11-07.
- `f1`–`f5`, `sin`, `p1`–`p7`, `r1` and `r2` are the fixtures.
