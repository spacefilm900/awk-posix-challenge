#!/bin/sh
# Probe wrapper: runner.py sets LC_ALL/LANG from case.json (C); this overrides
# them to C.UTF-8 and then runs the interpreter command given as arguments.
LC_ALL=C.UTF-8 LANG=C.UTF-8 exec "$@"
