#!/usr/bin/env python3
"""Read-only corpus runner. Never updates expectations."""
import argparse, json, os, pathlib, shlex, subprocess, sys, time
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--cmd',required=True,help='Command argv prefix, e.g. "awk" or "python -m pyawk"; runner appends -f program.awk')
    ap.add_argument('--label',default='candidate')
    ap.add_argument('--timeout',type=float,default=5)
    ap.add_argument('--output',help='Optional JSON report path (not in cases/)')
    ap.add_argument('--ids',nargs='*',help='Optional case IDs')
    args=ap.parse_args(); command=shlex.split(args.cmd)
    if not command: ap.error('--cmd cannot be empty')
    results=[]
    for folder in sorted((ROOT/'cases').glob('AWK-*')):
        case=json.loads((folder/'case.json').read_text())
        if args.ids and case['id'] not in args.ids: continue
        argv=command+['-f',str(folder/'program.awk')]
        env=os.environ.copy();env.update({'LC_ALL':case['locale'],'LANG':case['locale']})
        start=time.monotonic()
        try:
            p=subprocess.run(argv,input=(folder/'stdin.txt').read_bytes(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,timeout=args.timeout, cwd=folder)
            out=p.stdout;err=p.stderr;rc=p.returncode;timeout=False
        except subprocess.TimeoutExpired as e:
            out=e.stdout or b'';err=e.stderr or b'';rc=None;timeout=True
        duration=round(time.monotonic()-start,4)
        expout=(folder/'expected.stdout').read_bytes();experr=(folder/'expected.stderr').read_bytes();exprc=case['expected_exit']
        checks={'stdout':out==expout,'stderr':err==experr,'exit':rc==exprc,'timeout':not timeout}
        ok=all(checks.values())
        record={'id':case['id'],'name':case['name'],'group':case['group'],'status':'PASS' if ok else 'FAIL','checks':checks,'returncode':rc,'duration_seconds':duration}
        if not ok:
            record['actual_stdout']=out.decode('utf-8','backslashreplace')[:2000]
            record['actual_stderr']=err.decode('utf-8','backslashreplace')[:2000]
            record['expected_stdout']=expout.decode('utf-8','backslashreplace')[:2000]
        results.append(record)
        print(f"{record['status']:4} {case['id']} {case['group']}/{case['name']} ({duration:.3f}s)")
    report={'label':args.label,'command':command,'cases':len(results),'passes':sum(x['status']=='PASS' for x in results),'failures':sum(x['status']=='FAIL' for x in results),'results':results}
    print(f"\n{args.label}: {report['passes']}/{report['cases']} passed, {report['failures']} failed")
    if args.output:
        path=pathlib.Path(args.output).resolve()
        if ROOT/'cases' in path.parents: ap.error('report must not be written into corpus cases')
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(report,indent=2)+'\n')
    return 1 if report['failures'] else 0
if __name__=='__main__':sys.exit(main())
