# Crypto protocol freeze (summary)

Authoritative machine-readable fields: [`configs/crypto_daily_reimaging_v1.yaml`](../configs/crypto_daily_reimaging_v1.yaml).

| Field | Value |
|-------|--------|
| Protocol id | `crypto_daily_reimaging_v1` |
| Market | Binance USDT **spot** only |
| I / R grid | \(\{5,20,60\}^2\) (nine cells) |
| IS | 2018-01-01 … 2021-12-31 |
| OOS | 2022-01-01 … 2025-12-31 |
| Formation step | \(R\) days (non-overlapping) |
| Purge | \(R+(2I-2)\) beyond last train chart index |
| Universe | PIT top-200 by lagged quote ADV; min listing age 120d |
| Model | Jiang-style CNN; 5 seeds; mean probability |
| Primary H1 | Mean OOS Rank IC &gt; 0 under crypto retrain (global, then cells) |
| Reported audit | Crypto retrain nine-cell matrix (2026-07-24) |

**Status note.** The YAML still carries `draft_for_freeze` from the engineering workspace. Numbers in `results/crypto/` are a **CUDA audit** with documented path limitations (close-to-close, 0 bp). Delayed-VWAP + cost economics remain future work, not silently assumed.
