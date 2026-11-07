#!/usr/bin/env python3
"""Variant probe: runs every challenge case under several interpreters/locales.
Read-only with respect to cases/; writes variant_probe.json next to this script.
Observational only: the frozen expected outputs are the oracle, not these interpreters."""
import json, os, pathlib, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
ROOT = pathlib.Path('/workspace/awk-posix-challenge')
G = '/workspace/refs/local/bin/gawk'
VARIANTS = {
 'pyawk':         (['python3','-m','pyawk'], 'C'),
 'pyawk.utf8':    (['python3','-m','pyawk'], 'C.UTF-8'),
 'hawk':          (['/workspace/hawk/target/release/hawk'], 'C'),
 'hawk.utf8':     (['/workspace/hawk/target/release/hawk'], 'C.UTF-8'),
 'mawk':          (['/usr/bin/mawk'], 'C'),
 'mawk.utf8':     (['/usr/bin/mawk'], 'C.UTF-8'),
 'onetrue':       (['/workspace/refs/onetrue-awk/a.out'], 'C'),
 'onetrue.utf8':  (['/workspace/refs/onetrue-awk/a.out'], 'C.UTF-8'),
 'gawk-posix':    ([G,'--posix'], 'C'),
 'gawk-posix.utf8':([G,'--posix'], 'C.UTF-8'),
 'gawk-trad':     ([G,'--traditional'], 'C'),
 'gawk':          ([G], 'C'),
 'gawk.utf8':     ([G], 'C.UTF-8'),
 'busybox':       (['/workspace/refs/busybox/busybox','awk'], 'C'),
}
env0 = dict(os.environ, PYTHONPATH='/workspace/pyawk')
def run(case, v):
    cmd, loc = VARIANTS[v]
    env = dict(env0, LC_ALL=loc, LANG=loc)
    try:
        p = subprocess.run(cmd+['-f', str(case/'program.awk')], input=(case/'stdin.txt').read_bytes(),
                           capture_output=True, env=env, timeout=10, cwd=case)
        o, e, rc = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired:
        o, e, rc = b'', b'TIMEOUT', None
    exp = (case/'expected.stdout').read_bytes(); experr = (case/'expected.stderr').read_bytes()
    ok = o == exp and e == experr and rc == 0
    return case.name, v, ok, o.decode('utf-8','backslashreplace'), e.decode('utf-8','backslashreplace')[:300], rc
cases = sorted((ROOT/'cases').glob('AWK-*'))
jobs = [(c, v) for c in cases for v in VARIANTS]
res = {}
with ThreadPoolExecutor(16) as ex:
    for name, v, ok, o, e, rc in ex.map(lambda a: run(*a), jobs):
        res.setdefault(name, {})[v] = {'ok': ok, 'stdout': o, 'stderr': e, 'rc': rc}
json.dump(res, open(pathlib.Path(__file__).with_name('variant_probe.json'),'w'), indent=1)
print('variant'.ljust(18), 'pass  fails')
for v in VARIANTS:
    f = [n for n in res if not res[n][v]['ok']]
    print(v.ljust(18), str(len(res)-len(f)).rjust(4), ' '.join(f))
