# Crypto study — code snapshot

Small, pure (or near-pure) helpers vendored from the engineering workspace
`crypto-reimaging-price-trends`. They document **how** the crypto experiment was
constructed; they are **not** a full training stack.

| File | Role |
|------|------|
| `formation.py` | Non-overlapping formation grid (`step = R`), purge cut helper, OOS tail guard |
| `metrics_oos.py` | Rank IC / decile LS proxy used in the 2026-07-24 CUDA audit |
| `execution.py` | Delayed-entry window, exact hold, no-close-fill, turnover cost primitives |

## Not included (by design)

- Full Binance 1-minute archives (~129 GB content-set used on the experiment host)
- Image binaries, checkpoints, and OOS prediction CSVs
- Shared author OHLC renderer / CNN classes (live in the equity bootstrap workspace; architecture follows Jiang, Kelly & Xiu, 2023)

## Host-side layout (experiment machine)

```text
/share/home/user/snliu/crypto_reimaging_workspace
  data/crypto/          # daily bars, PIT universe, I×R IS/OOS datasets
  outputs/is/           # nine cells × five seeds
  outputs/oos/          # metrics_audit + predictions (audit)
  scripts/              # builders, audits, verify_oos_inference.py
```

Compute: 2× NVIDIA GeForce RTX 3090.
