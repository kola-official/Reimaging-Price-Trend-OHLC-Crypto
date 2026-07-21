# 三臂对照：raw vs vwpq-expand vs vwpq-clip-OC

生成时间：2026-07-21T05:34:37.893681+00:00

## 三种表示（勿混名）

| 名称 | 日线规则 | 路径臂 id |
|------|----------|-----------|
| **raw** | 标准开高低收量 | `raw` |
| **vwpq-expand**（已完成的 v3.6 主实验） | O/C/V=raw；H/L 分位后**外扩**盖住 O/C | `vwpq` |
| **vwpq-clip-OC**（本协议） | H/L=分位带；O/C **裁进** [L,H] | `vwpq_clip` |

标签、均线、组合成交价仍用 **raw** 价格；clip 只改 CNN 看到的 K 线实体/影线几何。

## 范围

- 训练/对照矩阵：**对角线** (5,5)/(20,20)/(60,60) × 五种子。
- expand/raw 的预测复用已有 `purged_primary` 产物；**不得**把 expand 的全局 H1/H2 bootstrap 写成 clip 的结果。

## 单元 Rank IC（各自 ensemble；比较请看配对 Δ）

      arm  I  R   status   rank_ic       n  n_dates  n_ic_dates   arm_label
      raw  5  5 complete  0.008333  425670      487         487         raw
     vwpq  5  5 complete  0.006253 1158046     1122        1122 vwpq_expand
vwpq_clip  5  5 complete  0.006454 1158046     1122        1122   vwpq_clip
      raw 20 20 complete  0.001745  270788      263         263         raw
     vwpq 20 20 complete -0.004723  270788      263         263 vwpq_expand
vwpq_clip 20 20 complete -0.007295  270788      263         263   vwpq_clip
      raw 60 60 complete  0.018075   89876       87          87         raw
     vwpq 60 60 complete  0.018943   89876       87          87 vwpq_expand
vwpq_clip 60 60 complete  0.015443   89876       87          87   vwpq_clip

## 配对 ΔRankIC（共同键上）

 I  R   status     delta  n_common  n_dates                 pair                vs
 5  5 complete  0.000273    425670      487       vwpq-minus-raw  expand_minus_raw
 5  5 complete  0.000628    425670      487  vwpq_clip-minus-raw    clip_minus_raw
 5  5 complete  0.000201   1158046     1122 vwpq_clip-minus-vwpq clip_minus_expand
20 20 complete -0.006468    270788      263       vwpq-minus-raw  expand_minus_raw
20 20 complete -0.009040    270788      263  vwpq_clip-minus-raw    clip_minus_raw
20 20 complete -0.002571    270788      263 vwpq_clip-minus-vwpq clip_minus_expand
60 60 complete  0.000868     89876       87       vwpq-minus-raw  expand_minus_raw
60 60 complete -0.002633     89876       87  vwpq_clip-minus-raw    clip_minus_raw
60 60 complete -0.003501     89876       87 vwpq_clip-minus-vwpq clip_minus_expand

## 描述性平均 ΔRankIC（对角线）

- expand − raw：-0.0017759153276659296
- clip − raw：-0.003681461877942313
- clip − expand：-0.001956965300245573

## 经济路径（与 expand G5 H2 相同：下一开盘、10 bps、√252 净夏普）

三臂使用 **raw ∩ expand ∩ clip** 同一评分键；成交价仍为 **raw 开盘**。

 I  R  n_common_scored  n_dates  cost_bps                              endpoint  sharpe_raw  n_days_raw  sharpe_vwpq_expand  n_days_vwpq_expand  sharpe_vwpq_clip  n_days_vwpq_clip  delta_expand_minus_raw  delta_clip_minus_raw  delta_clip_minus_expand
 5  5           425670      487        10 next_open_exec_with_frozen_exit_proxy   -0.399024        6001           -0.301342                6001         -0.184376              6001                0.097681              0.214647                 0.116966
20 20           270788      263        10 next_open_exec_with_frozen_exit_proxy    3.067983        6001            1.358877                6001          1.888979              6001               -1.709106             -1.179003                 0.530102
60 60            89876       87        10 next_open_exec_with_frozen_exit_proxy    4.372208        6001            6.367431                6001          4.326324              6001                1.995223             -0.045884                -2.041107

### 对角线平均 Δ 净夏普（描述性）

- expand − raw：0.12793309975866377
- clip − raw：-0.33674646879873826
- clip − expand：-0.46467956855740206

说明：此为点估计对照，**不是** clip 的 B=5000 月块全局检验；
expand 的确认性 H2 仍以 `final_summary.json` 为准（且 H1 未过门时 H2 仅描述）。

## 读法

- Rank IC / 夏普差为正：后者相对前者更好（**描述性**）。
- 本表不把 expand 的全局 bootstrap 结论转贴到 clip。

### 与用户原设想的对齐

clip 协议 =「O/C 落在新 H/L 外时裁进分位带」；expand =「扩 H/L、锁 O/C」。

