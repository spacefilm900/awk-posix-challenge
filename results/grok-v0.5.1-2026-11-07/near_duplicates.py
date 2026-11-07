#!/usr/bin/env python3
# Near-duplicate survey of the v0.5.1 corpus (analysis only; no case is changed).
# Run from the repository root: python3 results/grok-v0.5.1-2026-11-07/near_duplicates.py
# Program skeleton = token stream from tools/grammar_check.lex with string, number and ERE literals masked.
# A shared skeleton is NOT proof of redundancy: different literals often test different semantics.
import re, json, glob, collections, sys
sys.path.insert(0,'tools'); import grammar_check as g
groups=collections.defaultdict(list)
for d in sorted(glob.glob('cases/AWK-*')):
    src=open(d+'/program.awk').read()
    m=json.load(open(d+'/case.json'))
    toks=g.lex(src)
    sk=[]
    for k,t in toks:
        if k=='str': sk.append('S')
        elif k=='num': sk.append('N')
        elif k=='ere': sk.append('R')
        elif k=='nl': continue
        else: sk.append(t)
    groups[' '.join(sk)].append(d.split('/')[1])
dups={k:v for k,v in groups.items() if len(v)>1}
print(f"cases: {sum(len(v) for v in groups.values())}; distinct program skeletons (literals masked): {len(groups)}; skeletons shared by >1 case: {len(dups)} covering {sum(len(v) for v in dups.values())} cases")
for k,v in sorted(dups.items(), key=lambda kv:-len(kv[1])):
    print(f"{len(v):3d}  {', '.join(v)}\n     {k[:150]}")

print("\n# Exact duplicates: same token stream (whitespace ignored), same stdin, options/operands/fixtures and expected output")
ex=collections.defaultdict(list)
for d in sorted(glob.glob('cases/AWK-*')):
    m=json.load(open(d+'/case.json'))
    toks=tuple((k,t) for k,t in g.lex(open(d+'/program.awk').read()) if k!='nl')
    sname=m.get('stdin','stdin.txt')
    sb=open(d+'/'+sname,'rb').read() if sname and __import__('os').path.exists(d+'/'+sname) else b''
    key=(toks, sb, json.dumps(m.get('options',[])), json.dumps(m.get('operands',[])), open(d+'/expected.stdout','rb').read(),
         tuple(open(d+'/'+f,'rb').read() for f in m.get('fixtures',[])))
    ex[key].append(d.split('/')[1])
n=0
for v in ex.values():
    if len(v)>1: n+=1; print('  ' + ', '.join(v))
print(f"exact-duplicate groups: {n}")
