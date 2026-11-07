# Pre-fix failures: actual vs expected (extracted from the runner JSON in this directory)

## pyawk (pyawk enhancements d0bdc4b (pre-fix)): 437/440

- **AWK-391** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'[-]:alpha\n[-]:beta\n'`
  - actual stdout: `'[]:alpha\n[]:beta\n'`
- **AWK-392** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'[-]:7:x\n'`
  - actual stdout: `'[]:7:x\n'`
- **AWK-399** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'[-]:7:hello\n'`
  - actual stdout: `'[]:7:hello\n'`

## hawk (hawk enhancements d24f8d1 (pre-fix)): 437/440

- **AWK-391** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'[-]:alpha\n[-]:beta\n'`
  - actual stdout: `'[]:alpha\n[]:beta\n'`
- **AWK-392** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'[-]:7:x\n'`
  - actual stdout: `'[]:7:x\n'`
- **AWK-399** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'[-]:7:hello\n'`
  - actual stdout: `'[]:7:hello\n'`

## mawk (mawk): 437/440

- **AWK-415** (observational) failed checks ['stdout'], rc=0
  - expected stdout: `'3:a:c\n1:e:e\n'`
  - actual stdout: `'2:a:b\nc\n1:e:e\n'`
- **AWK-416** (observational) failed checks ['stdout'], rc=0
  - expected stdout: `'3:a:d\n'`
  - actual stdout: `'2:a:b\nd\n'`
- **AWK-417** (observational) failed checks ['stdout'], rc=0
  - expected stdout: `'3:x:z\n'`
  - actual stdout: `'2:x:y\nz\n'`

## onetrue (onetrue): 435/440

- **AWK-391** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'[-]:alpha\n[-]:beta\n'`
  - actual stdout: `'[]:alpha\n[]:beta\n'`
- **AWK-392** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'[-]:7:x\n'`
  - actual stdout: `'[]:7:x\n'`
- **AWK-399** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'[-]:7:hello\n'`
  - actual stdout: `'[]:7:hello\n'`
- **AWK-403** (portable) failed checks ['stdout', 'stderr', 'exit'], rc=2
  - expected stdout: `'1 ZZ 1 1 1\n'`
  - actual stdout: `''`
  - actual stderr: `'/workspace/refs/onetrue-awk/a.out: syntax error at source line 1 source file /workspace/awk-posix-challenge/cases/AWK-403/program.awk\n context is\n\t{old=$0; r=getline v < "other"; print r, v, >>>  old='`
- **AWK-416** (observational) failed checks ['stdout'], rc=0
  - expected stdout: `'3:a:d\n'`
  - actual stdout: `'2:a:b\nd\n'`

## gawk-posix (gawk --posix): 438/440

- **AWK-105** (nonportable) failed checks ['stdout'], rc=0
  - expected stdout: `'3:a:c\n'`
  - actual stdout: `'1:abc:\n'`
- **AWK-416** (observational) failed checks ['stdout'], rc=0
  - expected stdout: `'3:a:d\n'`
  - actual stdout: `'2:a:b\nd\n'`

## gawk-default (gawk (default, observational)): 439/440

- **AWK-416** (observational) failed checks ['stdout'], rc=0
  - expected stdout: `'3:a:d\n'`
  - actual stdout: `'2:a:b\nd\n'`

## busybox (busybox awk 1.35.0 (observational)): 426/440

- **AWK-021** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'1 1 1\n'`
  - actual stdout: `'0 1 0\n'`
- **AWK-023** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'1 1\n'`
  - actual stdout: `'1 0\n'`
- **AWK-131** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'1:0\n'`
  - actual stdout: `'0:1\n'`
- **AWK-398** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'1 2\n'`
  - actual stdout: `'0 2\n'`
- **AWK-408** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'f2:1:3:b1\n'`
  - actual stdout: `'f1:2:2:a2\n'`
- **AWK-409** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'0 2 two\n'`
  - actual stdout: `'-1 2 two\n'`
- **AWK-410** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'1 1\n'`
  - actual stdout: `'0 1\n'`
- **AWK-415** (observational) failed checks ['stdout'], rc=0
  - expected stdout: `'3:a:c\n1:e:e\n'`
  - actual stdout: `'3:a:c\n2:e:\n'`
- **AWK-416** (observational) failed checks ['stdout'], rc=0
  - expected stdout: `'3:a:d\n'`
  - actual stdout: `'2:a:b\n'`
- **AWK-417** (observational) failed checks ['stdout'], rc=0
  - expected stdout: `'3:x:z\n'`
  - actual stdout: `'4:x:\n'`
- **AWK-426** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'1\n'`
  - actual stdout: `'0\n'`
- **AWK-429** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'0 1\n'`
  - actual stdout: `'0 0\n'`
- **AWK-430** (portable) failed checks ['stdout'], rc=0
  - expected stdout: `'1\n'`
  - actual stdout: `'0\n'`
- **AWK-439** (observational) failed checks ['stdout'], rc=0
  - expected stdout: `'2:XbX\n'`
  - actual stdout: `'3:XXbX\n'`

