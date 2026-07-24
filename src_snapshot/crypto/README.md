# Cryptocurrency study code snapshot

Pure and near-pure helpers vendored from the engineering workspace for Study B. They document construction of the cryptocurrency experiment and are not a complete training stack.

| File | Role |
|------|------|
| `formation.py` | Non-overlapping formation grid with step equal to horizon \(R\); purge cut; out-of-sample tail guard |
| `metrics_oos.py` | Rank IC and decile long–short metrics used in the 2026-07-24 evaluation |
| `execution.py` | Delayed-entry window, exact holding period, no-close-fill rule and turnover cost primitives |
| `transfer_metrics.py` | Pure Rank IC helpers and freeze-schema checks for US→crypto transfer |
| `transfer_us_arms_to_crypto_frozen.py` | Frozen US raw/expand/clip scoring entry point |
| `test_us_to_crypto_transfer_freeze.py` | Freeze invariant tests |

## Scope

The following artefacts are not included: full Binance one-minute archives, image binaries, checkpoints and out-of-sample prediction files; shared author OHLC renderer and CNN classes, which live in the equity bootstrap workspace and follow Jiang, Kelly and Xiu (2023).

## Experiment-host layout

```text
/share/home/user/snliu/crypto_reimaging_workspace
  data/crypto/
  outputs/is/
  outputs/oos/
  scripts/
```

Compute: dual NVIDIA GeForce RTX 3090.
