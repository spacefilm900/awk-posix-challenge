#!/usr/bin/env python3
"""Read-only POSIX AWK challenge runner. Never updates expected artifacts."""
import argparse,json,os,pathlib,shlex,subprocess,sys,time,tempfile,shutil,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cmd',required=True);ap.add_argument('--label',default='candidate');ap.add_argument('--timeout',type=float,default=5);ap.add_argument('--output');ap.add_argument('--ids',nargs='*');ap.add_argument('--classifications',nargs='*');args=ap.parse_args()
 command=shlex.split(args.cmd);assert command
 results=[]
 for folder in sorted((ROOT/'cases').glob('AWK-*')):
  m=json.loads((folder/'case.json').read_text());cid=m['id']; classification=m.get('classification','portable')
  if args.ids and cid not in args.ids:continue
  if args.classifications and classification not in args.classifications:continue
  options=m.get('options',[]);fixtures=m.get('fixtures',[]);operands=m.get('operands',[])
  req=m.get('requires',[]);missing=[r for r in req if shutil.which(r) is None]
  if missing:
   record={'id':cid,'status':'SKIP','reason':'missing utilities: '+','.join(missing),'classification':classification};results.append(record);continue
  with tempfile.TemporaryDirectory(prefix='awk-challenge-') as td:
   wd=pathlib.Path(td)
   for f in fixtures:
    if not (folder/f).is_file() or '..' in pathlib.PurePosixPath(f).parts or pathlib.PurePosixPath(f).is_absolute():raise ValueError('Invalid fixture '+f)
    dest=wd/f;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(folder/f,dest)
   prog=folder/'program.awk';argv=command+options+['-f',str(prog)]+operands
   env=os.environ.copy();env.update({'LC_ALL':m.get('locale','C'),'LANG':m.get('locale','C')});env.update(m.get('env',{}))
   inp=(folder/m.get('stdin','stdin.txt')).read_bytes() if m.get('stdin','stdin.txt') is not None else b''
   t=time.monotonic()
   try:
    p=subprocess.run(argv,input=inp,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=wd,env=env,timeout=m.get('timeout',args.timeout));rc=p.returncode;out=p.stdout;err=p.stderr;timeout=False
   except subprocess.TimeoutExpired as e:rc=None;out=e.stdout or b'';err=e.stderr or b'';timeout=True
   expected_out=(folder/'expected.stdout').read_bytes();expected_err=(folder/'expected.stderr').read_bytes();er=m.get('expected_exit',0)
   def check(b,expected,mode):
    return {'exact':lambda:b==expected,'empty':lambda:not b,'nonempty':lambda:bool(b),'ignore':lambda:True}[mode]()
   ef=m.get('expected_files',{})
   file_checks={name:(wd/name).is_file() and (wd/name).read_bytes()==(folder/target).read_bytes() for name,target in ef.items()}
   checks={'stdout':check(out,expected_out,m.get('stdout_check','exact')),'stderr':check(err,expected_err,m.get('stderr_check','exact')),'exit':(rc!=0 if er=='nonzero' else rc==er),'timeout':not timeout,'files':all(file_checks.values()),'absent':all(not (wd/x).exists() for x in m.get('expected_absent',[]))}
   ok=all(checks.values());record={'id':cid,'name':m['name'],'group':m['group'],'classification':classification,'status':'PASS' if ok else 'FAIL','checks':checks,'returncode':rc,'duration_seconds':round(time.monotonic()-t,4)}
   if not ok:record.update(actual_stdout=out.decode(errors='backslashreplace')[:1000],actual_stderr=err.decode(errors='backslashreplace')[:1000],expected_stdout=expected_out.decode(errors='backslashreplace')[:1000],files=file_checks)
   results.append(record);print(f'{record["status"]:4} {cid} {m["group"]}/{m["name"]}',flush=True)
 cnt=collections.Counter((r['classification'],r['status']) for r in results);report={'label':args.label,'command':command,'cases':len(results),'passes':sum(r['status']=='PASS' for r in results),'failures':sum(r['status']=='FAIL' for r in results),'skips':sum(r['status']=='SKIP' for r in results),'by_classification':{k:{st:cnt[k,st] for st in ('PASS','FAIL','SKIP')} for k in sorted({r['classification'] for r in results})},'results':results}
 print(f'\n{args.label}: {report["passes"]}/{report["cases"]} passed; {report["failures"]} failed; {report["skips"]} skipped')
 if args.output:
  dest=pathlib.Path(args.output).resolve()
  if (ROOT/'cases') in dest.parents:ap.error('Cannot write report inside cases/')
  dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,indent=2)+'\n')
 return int(report['failures']>0)
if __name__=='__main__':sys.exit(main())
