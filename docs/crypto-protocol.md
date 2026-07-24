# Cryptocurrency protocol summary

Machine-readable fields: [configs/crypto_daily_reimaging_v1.yaml](../configs/crypto_daily_reimaging_v1.yaml).

| Field | Value |
|-------|--------|
| Protocol identifier | `crypto_daily_reimaging_v1` |
| Market | Binance USDT spot |
| Image and horizon grid | \(I,R\in\{5,20,60\}\) |
| In-sample window | 2018-01-01 to 2021-12-31 |
| Out-of-sample window | 2022-01-01 to 2025-12-31 |
| Formation step | \(R\) calendar days, non-overlapping |
| Purge | \(R+(2I-2)\) beyond the last training chart index |
| Universe | Point-in-time top 200 by lagged quote volume; minimum listing age 120 days |
| Model | Jiang-style CNN; five seeds; mean probability |
| Primary hypothesis | Mean out-of-sample Rank IC positive under cryptocurrency retrain |
| Reported evaluation | Nine-cell retrain matrix dated 2026-07-24 |

Reported metrics in [results/crypto/](../results/crypto/) use close-to-close returns and zero transaction costs. Delayed VWAP execution and cost-adjusted economics are specified in the design but are not the headline freeze of the published matrix.
