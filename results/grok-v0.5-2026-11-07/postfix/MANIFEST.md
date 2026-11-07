# Post-fix results manifest: v0.5, 2026-11-07 (Grok Bot)

This is a re-run of the same v0.5 corpus after the FILENAME fix, on the fixed pyawk and hawk only. The frozen
pre-fix baseline is in `../prefix/`, committed as `ac1445f` before any interpreter change. The corpus,
platform, runner, locale (C), 5 s timeout and checksums are the same as in `../prefix/MANIFEST.md`. The
reference interpreters were not re-run, because nothing about them changed.

## Interpreters

| Label | Provenance |
|---|---|
| pyawk enhancements b6a3d25 (post-fix) | git `b6a3d257d6fe09ecb15e3e383b5f56c78bb7c5cc`, which is d0bdc4b plus `5ad9d48` (tests) and `b6a3d25` (fix). Clean tree, Python 3.13.5 |
| hawk enhancements 9f09764 (post-fix) | git `9f09764`, which is d24f8d1 plus `5b544c6` (tests) and `9f09764` (fix). Clean tree. Release build from `tools/regress.sh`, sha256 `8eaaf2427d2622c11f9b4a568bd4e3e1917cb40012a4e63dd7643fb55fba1a19` |

## Commands (run 2026-11-07 10:02:00Z to 10:02:18Z)

```sh
D=results/grok-v0.5-2026-11-07/postfix
PYTHONPATH=/workspace/pyawk python3 tools/runner.py --cmd 'python3 -m pyawk' --label 'pyawk enhancements b6a3d25 (post-fix)' --output $D/pyawk.json
python3 tools/runner.py --cmd /workspace/hawk/target/release/hawk --label 'hawk enhancements 9f09764 (post-fix)' --output $D/hawk.json
```

## Results

| Label | Total | portable (418) | observational (21) | nonportable (1) | Failing |
|---|---:|---:|---:|---:|---|
| pyawk b6a3d25 | **440/440** | 418 | 21 | 1 | none |
| hawk 9f09764 | **440/440** | 418 | 21 | 1 | none |

AWK-391, 392 and 399 now pass on both. No case that passed before the fix now fails.

| sha256 | File |
|---|---|
| `0d52757f528fdf6d5fb423b9feb6808ad8277995c1d92feb17dceab2aab0c8ff` | pyawk.json |
| `3b1804dffc5a238c58b9506ec315a1cf0c8beb5c7d1087d20ef5187e3e2005ad` | hawk.json |
