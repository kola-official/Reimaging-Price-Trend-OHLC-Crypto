> 仓库科学总览与三项研究综合论述见 [docs/SCIENTIFIC-OVERVIEW.md](../docs/SCIENTIFIC-OVERVIEW.md)。本文为研究 A 详细结果表。

# 五臂对照：raw / 量权 expand·clip / 额权 expand·clip

生成：2026-07-21T10:16:25.971171+00:00

## 五臂定义

| 标签 | 路径 id | 规则 |
|------|---------|------|
| raw | `raw` | 标准 OHLCV |
| share_expand | `vwpq` | 权重=成交量；H/L 分位外扩；O/C=raw |
| share_clip | `vwpq_clip` | 权重=成交量；O/C 裁进分位带 |
| **dollar_expand** | `vwpq_d` | 权重=典型价×量；H/L 外扩；O/C=raw |
| **dollar_clip** | `vwpq_d_clip` | 权重=典型价×量；O/C 裁进分位带 |

标签/均线/成交：一律 **raw**。矩阵：对角线三格 × 五种子。

## 经济路径（10 bps 净夏普，共同键交集）

 I  R  n_common  n_dates  cost_bps  sharpe_raw  sharpe_share_expand  sharpe_share_clip  sharpe_dollar_expand  sharpe_dollar_clip  delta_share_expand_minus_raw  delta_share_clip_minus_raw  delta_dollar_expand_minus_raw  delta_dollar_clip_minus_raw
 5  5    425670      487        10   -0.399024            -0.301342          -0.184376             -0.312141           -0.071641                      0.097681                    0.214647                       0.086882                     0.327383
20 20    270788      263        10    3.067983             1.358877           1.888979              1.424935            3.132490                     -1.709106                   -1.179003                      -1.643048                     0.064507
60 60     89876       87        10    4.372208             6.367431           4.326324              6.257739            4.523791                      1.995223                   -0.045884                       1.885531                     0.151583

### 对角线平均 Δ 净夏普（相对 raw）

- share_expand − raw：0.12793309975866377
- share_clip − raw：-0.33674646879873826
- **dollar_expand − raw：0.10978856639212047**
- **dollar_clip − raw：0.18115774944000038**

## 配对 Δ Rank IC（相对 raw）

 I  R                      vs  delta_rank_ic  n_common  n_dates
 5  5  share_expand_minus_raw       0.000273    425670      487
 5  5    share_clip_minus_raw       0.000628    425670      487
 5  5 dollar_expand_minus_raw      -0.000119    425670      487
 5  5   dollar_clip_minus_raw       0.000685    425670      487
20 20  share_expand_minus_raw      -0.006468    270788      263
20 20    share_clip_minus_raw      -0.009040    270788      263
20 20 dollar_expand_minus_raw      -0.006424    270788      263
20 20   dollar_clip_minus_raw       0.000258    270788      263
60 60  share_expand_minus_raw       0.000868     89876       87
60 60    share_clip_minus_raw      -0.002633     89876       87
60 60 dollar_expand_minus_raw       0.000686     89876       87
60 60   dollar_clip_minus_raw      -0.002174     89876       87

### 对角线平均 Δ Rank IC

- share_expand − raw：-0.0017759153276659296
- share_clip − raw：-0.003681461877942313
- dollar_expand − raw：-0.001952362858927326
- dollar_clip − raw：-0.0004100566454159104

## 读法

- 额权是量权的 refine：日内价格变动有限时二者接近，大波动日差更明显。
- 经济表与此前三臂对照同路径；非 B=5000 全局检验。

