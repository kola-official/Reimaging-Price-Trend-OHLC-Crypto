# Errata and corrections (2026-07)

**English first; 中文在后。**

An external code and methods review (2026-07-26) of the published snapshot
identified the issues below. Code fixes ship in this repository; **published
Study A economic tables are pending recomputation on the experiment host** and
should not be quoted until refreshed. Ranking (Rank IC) tables are unaffected
except where noted.

## E1. Study A net Sharpe estimator inflated by ≈ √(R·f) — pending recomputation

The published diagonal net Sharpes were computed by spreading each cohort's
whole-period H–L net return flat over its R holding sessions
(`nav.event_driven_hl_daily_returns`) and annualising the resulting series
with √252. On the non-overlapping formation grid (K_R = 1) that series is
piecewise constant over R-session blocks: its per-session volatility
understates mark-to-market volatility by ≈ √R, so the annualised Sharpe is
inflated by ≈ √(R·f), where f is the covered-session fraction (≈ ×4.3 at
I20/R20, ≈ ×7.4 at I60/R60). Because the factor differs per cell, the
cross-cell "mean Δ vs raw" figures in the README abstract are also distorted;
back-of-envelope correction suggests the share/dollar **expand** mean gaps
(+0.13/+0.11) do not survive and the **dollar clip** gap (+0.18) shrinks
materially, with its remainder concentrated in the partially-covered I5/R5
cell (see E4).

Fix shipped: `nav.event_driven_hl_cohort_returns` +
`nav.sharpe_from_period_returns` (√(252/R) on non-overlapping period returns,
matching the crypto path's √(365/R) in `metrics_oos.py`);
`sharpe_recompute.py` reproduces both estimators side by side.
Action pending: recompute all three-way/five-way economic tables and revise
README/RESULTS/INTERPRETATION headline sentences accordingly.

## E2. Short-leg return convention biased H–L upward — pending recomputation

`nav.leg_open_open_return` used `entry/exit − 1` for the short side, which by
AM–GM never falls below the standard entry-notional convention
`−(exit/entry − 1)`; it overstated short-leg gains (price halves: +100% vs
+50%) and understated losses (price doubles: −50% vs −100%). All published
Study A Sharpes absorbed this upward bias. Fixed in code; magnitude at the
table level to be established by the E1 recomputation.

## E3. No inference behind the +0.18 headline

The only economic bootstrap shipped (share expand − raw, H2 in
`results/final_summary.md`) is insignificant: θ̂ = +0.128,
95% CI [−0.31, +0.79], null-centred p = 0.26. The dollar-clip contrast
(+0.18) has no bootstrap at all. Until the E1/E2 recomputation and a matching
bootstrap for the dollar arms exist, headline sentences should treat all mean
Sharpe gaps as descriptive, not established.

## E4. Undisclosed partial image coverage in several cells

Formation-date counts imply materially incomplete raw-arm image builds against
the 2003–2025 grid: I5/R5 487 of ≈1159 dates (42%), I5/R20 98/≈289, I5/R60
30/≈96, I20/R5 112/≈1159 (10%), I60/R5 31/≈1159 (3%); I20/R20 (263) and
I60/R60 (87) are ≈90% complete. `final_summary.json` also records
`n_raw = 425,670` vs `n_vwpq = 1,158,046` at I5/R5. Tables quoting these cells
(including the nine-cell equity Rank IC mean) must disclose per-cell coverage,
and incomplete cells should be completed or excluded from averages.

## E5. "Equity Rank IC ≈ 0.05" benchmark not evidenced in-repo

`results/crypto/RESULTS.md` and the README compare crypto results against
"US equity Rank IC near 0.05 in related US replications", but the repository's
own common-key equity tables show I20/R20 raw Rank IC ≈ 0.0017 (nine-cell
range −0.016…+0.027). The 0.05 figure needs an explicit source (pipeline,
protocol, table) or the comparison sentences need revision.

## E6. Smaller code corrections (shipped)

- Frozen exit proxy could search closes back to the chart session, before the
  position existed; now floored at the entry session (`nav.py`).
- The pure-Python Rank IC summariser propagated a single NaN date into the
  cell mean; degenerate dates are now skipped and counted
  (`n_ic_dates_skipped_nan`), with NaN semantics unified across
  `metrics_oos.spearman_ic` and `transfer_metrics.spearman_ic`.
- The transfer entry point now imports in the published snapshot layout,
  records the effective `min_names` (protocol value 50; the 2026-07-24 run
  effectively used 10), and prefers `torch.load(weights_only=True)`.
- `formation.py` docstrings now state that t+R+1 is the execution exit day
  (labels run to t+R) and that the purge cut is exactly tight under the
  C[t+R]/C[t] label convention.

Regression tests: `src_snapshot/hfdata/test_nav_fixes.py`,
`src_snapshot/crypto/test_metrics_consistency.py`.

---

# 勘误与更正（2026-07）

2026-07-26 的外部代码与方法审查发现以下问题。代码修复已随本仓库发布；**研究 A
的经济路径表格待在实验主机上重算**，刷新前请勿引用。除特别说明外，排序类
（Rank IC）表格不受影响。

## E1. 研究 A 净夏普估计量约放大 √(R·f) 倍——待重算

已发布的对角线净夏普把每个 cohort 的整段持有收益均摊到 R 个交易日
（`nav.event_driven_hl_daily_returns`），再对该序列乘 √252 年化。在非重叠形成
网格（K_R = 1）下，该序列按 R 日成块恒定：逐日波动率较真实盯市约低 √R 倍，
年化夏普因此约放大 √(R·f) 倍（f 为覆盖交易日占比；I20/R20 约 ×4.3，
I60/R60 约 ×7.4）。各格放大倍数不同，README 摘要中的“相对 raw 的三格平均
Δ”随之失真；粗略校正显示量权/额权 **expand** 的平均增益（+0.13/+0.11）
大概率不成立，**额权 clip**（+0.18）显著缩水且剩余增益集中于覆盖不全的
I5/R5 格（见 E4）。

已发布修复：`nav.event_driven_hl_cohort_returns` 与
`nav.sharpe_from_period_returns`（非重叠期收益 × √(252/R)，与加密侧
`metrics_oos.py` 的 √(365/R) 对齐）；`sharpe_recompute.py` 可并排复现两种
口径。待办：重算全部三臂/五臂经济表，并相应改写 README/RESULTS/
INTERPRETATION 的结论语句。

## E2. 空头腿收益公式向上偏——待重算

`nav.leg_open_open_return` 空头侧曾用 `entry/exit − 1`，由 AM–GM 恒不低于
标准的入场名义本金口径 `−(exit/entry − 1)`：高估空头盈利（价格腰斩：+100%
对 +50%）、低估空头亏损（价格翻倍：−50% 对 −100%）。全部已发布研究 A 夏普
含此向上偏差。代码已修复；表格层面的影响幅度以 E1 重算为准。

## E3. 头条 +0.18 缺乏推断支持

随包发布的唯一经济 bootstrap（量权 expand − raw，`results/final_summary.md`
之 H2）不显著：θ̂ = +0.128，95% CI [−0.31, +0.79]，p = 0.26；额权 clip
（+0.18）没有任何 bootstrap。在 E1/E2 重算并为额权臂补做同口径 bootstrap
之前，头条语句应将所有平均夏普差视为描述性结果。

## E4. 多个格子的图像覆盖不全且未披露

形成日计数显示 raw 臂图像相对 2003–2025 网格明显不完整：I5/R5 为 487/约
1159（42%）、I5/R20 98/约 289、I5/R60 30/约 96、I20/R5 112/约 1159（10%）、
I60/R5 31/约 1159（3%）；I20/R20（263）与 I60/R60（87）约 90% 完整。
`final_summary.json` 亦记录 I5/R5 的 `n_raw = 425,670` 对
`n_vwpq = 1,158,046`。引用相关格子的表格（含九格美股 Rank IC 均值）须披露
逐格覆盖率；不完整格子应补齐或从均值中剔除。

## E5. “美股 Rank IC ≈ 0.05” 基准在仓库内无出处

`results/crypto/RESULTS.md` 与 README 以“相关美股复现 Rank IC 约 0.05”评判
加密结果，但仓库自身 common-key 美股表格显示 I20/R20 raw Rank IC ≈ 0.0017
（九格范围 −0.016…+0.027）。0.05 需给出明确出处（管线、协议、表格），否则
应改写对比语句。

## E6. 较小的代码更正（已发布）

- 冻结退出代理曾可回看到形成日（入场之前）的收盘价，现以入场日为下界
  （`nav.py`）。
- 纯 Python Rank IC 汇总器曾让单个 NaN 日污染整格均值；现跳过退化日并计数
  （`n_ic_dates_skipped_nan`），并统一 `metrics_oos.spearman_ic` 与
  `transfer_metrics.spearman_ic` 的 NaN 语义。
- 迁移入口脚本在快照布局下可直接导入；记录生效 `min_names`（协议值 50；
  2026-07-24 发布运行实际为 10）；`torch.load` 优先 `weights_only=True`。
- `formation.py` 注释澄清 t+R+1 为执行退出日（标签只到 t+R），并说明 purge
  切点在 C[t+R]/C[t] 标签口径下恰好零冗余。

回归测试：`src_snapshot/hfdata/test_nav_fixes.py`、
`src_snapshot/crypto/test_metrics_consistency.py`。
