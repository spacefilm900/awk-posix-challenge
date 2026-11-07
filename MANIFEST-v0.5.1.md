# v0.5.1 before/after manifest

"Before" is tag `v0.5` (`9e547517b6d27302a8c20313dd927013427f807a`). "After" is the v0.5.1 release (tag `v0.5.1`).
`SHA256SUMS.txt` is regenerated and covers every file below, including this manifest, so it is not listed itself.

## Case classification

| Case | v0.5 class / posix_status | v0.5.1 class / posix_status | Expected output |
|---|---|---|---|
| AWK-403 | portable / specified | portable / specified | unchanged |
| AWK-415 | observational / contested | portable / specified (provisional) | unchanged |
| AWK-416 | observational / contested | observational / known standards-implementation conflict | unchanged |
| AWK-417 | observational / contested | portable / specified (provisional) | unchanged |
| AWK-419 | observational / unstated | observational / contested | unchanged |

**Totals.** v0.5: 418 portable, 21 observational, 1 nonportable. v0.5.1: 420 portable, 19 observational, 1 nonportable; 440 cases.

## File hashes (sha256)

| File | v0.5 | v0.5.1 |
|---|---|---|
| `README.md` | `dd623d36f50952f8…` | `00053f82dc396f52…` |
| `tools/runner.py` | `844afb86b5e67ac3…` | `844afb86b5e67ac3…` (unchanged) |
| `cases/AWK-403/program.awk` | `ce7841b1746ff637…` | `d9ef236becc33cbd…` |
| `cases/AWK-403/case.json` | `15ec2cede0429b9e…` | `a2a0a1f077136e18…` |
| `cases/AWK-403/expected.stdout` | `7227e7d49ecf5f6d…` | `7227e7d49ecf5f6d…` (unchanged) |
| `cases/AWK-415/case.json` | `ee3fc47abf73e927…` | `4cdabdf051c60631…` |
| `cases/AWK-415/expected.stdout` | `660d0b9c6e0082c2…` | `660d0b9c6e0082c2…` (unchanged) |
| `cases/AWK-416/case.json` | `f5ebbc53108e342b…` | `a9242dc7f8c5f8a5…` |
| `cases/AWK-416/expected.stdout` | `5beb24a85b63254b…` | `5beb24a85b63254b…` (unchanged) |
| `cases/AWK-417/case.json` | `a78b6156a5360df4…` | `73ae724952c0a850…` |
| `cases/AWK-417/expected.stdout` | `762ac6af9e9bcc74…` | `762ac6af9e9bcc74…` (unchanged) |
| `cases/AWK-419/case.json` | `65ab99d5ef525e80…` | `daff4fa6d2c8a5f6…` |
| `cases/AWK-419/expected.stdout` | `079957bacc33ff6d…` | `079957bacc33ff6d…` (unchanged) |
| `tools/summarize.py` | (new) | `e07d209623f33e7c…` |
| `tools/test_runner_env.py` | (new) | `bfcbddc71737a585…` |
| `feedback/ChatGPT-response-to-v0.5.md` | (new) | `600bfc762a7fee7b…` |
| `feedback/ChatGPT-response-to-v0.5.docx` | (new) | `fddd45c0878a1320…` |
| `CHANGELOG-v0.5.1.md` | (new) | `6391dcd2d5f477a0…` |

Full hashes are in `SHA256SUMS.txt`. All other files under `cases/` are byte-identical to v0.5.
