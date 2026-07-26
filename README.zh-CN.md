# 价格趋势 OHLC 表示再思考与加密货币迁移

**语言：** [English](README.md) · [中文](README.zh-CN.md)  
**仓库：** [Reimaging-Price-Trend-OHLC-Crypto](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-Crypto)

> **⚠️ 勘误（2026-07）。** 代码审查发现下文研究 A 经济路径的夏普值因均摊日化
> 口径被放大约 √(R·f) 倍，且空头腿公式存在向上偏差；三格平均 Δ（含 +0.18 的
> 额权 clip 头条）在重算前不可靠，另有若干格子图像覆盖不全。刷新前请勿引用
> 本文件中研究 A 的经济数字。详情、修正估计量与进度见
> [docs/ERRATA.md](docs/ERRATA.md)。

## 摘要

基于灰度 OHLC 图像的横截面预测，是检验视觉价格趋势信号的标准路径，方法谱系见 Jiang、Kelly 与 Xiu（2023），*The Journal of Finance*（[doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268)）。两个关键设计问题仍未充分厘清：日线 K 线如何绘制，以及股票配方能否延伸至股票之外。

本仓库在同一图像 CNN 族下报告三项关联实证。**研究 A** 在美股上改变 raw、量权与额权 expand/clip 的日线几何。额权 clip 相对 raw 的对角线平均净夏普约提高 0.18；expand 在 I60/R60 占优、在 I20/R20 恶化，而 Rank IC 差分较小。**研究 B** 在 Binance USDT 现货上重训同一 \(I,R\in\{5,20,60\}\) 网格。主对照格 I20/R20 的 Rank IC 为 −0.0495；中期预测中 I60/R20 相对最稳，但仍低于相关美股复现约 0.05 的 Rank IC 量级。**研究 C** 将冻结的美股 raw、expand 与 clip 权重用于同一加密样本外键，不进行梯度更新。三臂在 I20/R20 上均为负，且未优于本地重训。

综合结论是：**表示选择能够改变美股组合表现**；而在本加密现货样本上，**Jiang 风格日频图像 CNN 无论本地重训还是冻结股权重迁移，均未恢复与股票相当的排序能力**。结论受市场、样本分割与评估路径约束，并不主张任意模型下加密收益均不可预测。

科学总览见 [docs/SCIENTIFIC-OVERVIEW.md](docs/SCIENTIFIC-OVERVIEW.md)。

| 研究 | 干预 | 问题 |
|------|------|------|
| A | 美股日线几何 | raw、expand、clip 是否改变样本外组合表现 |
| B | 加密本地重训 | 股票图像设定在 Binance USDT 现货上是否仍具排序能力 |
| C | 冻结美股权重 | 不重训时，股权重表示模型能否迁移 |

完整一分钟行情、图像张量与检查点保留在实验主机；本仓库发布协议、结果表、解读与精简纯 Python 工具。

---

## 研究 A. 美股 OHLC 表示

在 hfdata 一分钟数据、灰度图像与五种子 CNN 的统一路径下，样本内为 1993–2002 年，样本外为 2003–2025 年。标签、均线与成交使用 raw 价格，各臂仅改变绘制的 OHLC 几何。

### 对角线净夏普，单边十个基点

等权高减低十分位；下一开盘入场、计划开盘离场；年化因子 \(\sqrt{252}\)。

| 设定 | raw | 量权 expand | 量权 clip | 额权 expand | 额权 clip |
|------|----:|------------:|----------:|------------:|----------:|
| I5 / R5 | −0.40 | −0.30 | −0.18 | −0.31 | −0.07 |
| I20 / R20 | 3.07 | 1.36 | 1.89 | 1.42 | 3.13 |
| I60 / R60 | 4.37 | 6.37 | 4.33 | 6.26 | 4.52 |

相对 raw 的三格平均变化：额权 clip +0.18，量权与额权 expand 约 +0.11 至 +0.13，量权 clip −0.34。额权 clip 平均最优，且是唯一未在 I20/R20 崩塌的非 raw 臂；expand 增益集中于长视界。全表见 [results/RESULTS.md](results/RESULTS.md)。方法见 [docs/METHODS.md](docs/METHODS.md)。视界依赖解读见 [docs/INTERPRETATION.md](docs/INTERPRETATION.md)。

---

## 研究 B. 加密货币现货重训

图像与模型族保持不变；宇宙为 Binance USDT 现货，采用点时点流动性筛选与身份断点切段，样本内 2018–2021 年，样本外 2022–2025 年。形成步长等于 \(R\)。排序指标基于收盘到收盘收益；零成本多空夏普仅作经济示意。

### 样本外 Rank IC

|  | R5 | R20 | R60 |
|--|---:|---:|---:|
| I5 | +0.014 | +0.034 | +0.026 |
| I20 | +0.018 | −0.049 | +0.002 |
| I60 | +0.009 | +0.032 | −0.009 |

股票侧主对照格 I20/R20 在此失败：Rank IC 为 −0.0495，AUC 为 0.450。对二十日预测，I60/R20 在组合型指标上最连贯，Rank IC 亦接近最优，表明可检出的中期排序更依赖长于预测视界的视觉历史。即便最优格子仍弱于美股复现，且形成日稀疏。

方法见 [docs/METHODS-crypto.md](docs/METHODS-crypto.md)。结果见 [results/crypto/RESULTS.md](results/crypto/RESULTS.md)。解读见 [docs/INTERPRETATION-crypto.md](docs/INTERPRETATION-crypto.md)。

---

## 研究 C. 冻结美股 raw / expand / clip 迁移

将美股 `purged_primary` 的 raw、expand 与 clip 检查点用于同一加密样本外键，不进行梯度更新，也不在加密数据上重估美股训练集归一化。expand 与 clip 权重作用于 raw 加密图像，记为跨表示迁移。

### 主对照格 I20/R20

| 臂 | Rank IC | ICIR | AUC | 行数 |
|----|--------:|-----:|----:|-----:|
| raw | −0.051 | −0.494 | 0.478 | 13852 |
| expand | −0.041 | −0.383 | 0.482 | 13852 |
| clip | −0.051 | −0.494 | 0.473 | 13852 |

同格加密本地重训 Rank IC 为 −0.0495。冻结迁移未能扭转主格失败。对角线 I5/R5 与 I60/R60 上三臂亦均为非正。

方法见 [docs/METHODS-us-to-crypto-transfer.md](docs/METHODS-us-to-crypto-transfer.md)。结果与出处见 [results/crypto/transfer/RESULTS.md](results/crypto/transfer/RESULTS.md)。解读见 [docs/INTERPRETATION-us-to-crypto-transfer.md](docs/INTERPRETATION-us-to-crypto-transfer.md)。

---

## 综合

| 研究 | 主要发现 |
|------|----------|
| A | 日线几何改变美股组合夏普；额权 clip 平均最强；expand 具视界依赖性。 |
| B | 加密本地重训在 I20/R20 失败；中期结构若存在则偏向更长回看，但仍弱于股票。 |
| C | 冻结的美股 raw / expand / clip 权重在相同加密键上同样失败，强化该方法族的资产类别迁移边界。 |

对研究 B 与 C 的结构解读是横截面深度不足：相对数十年股票面板，点时点加密宇宙更薄、更短、共动更强。该解读针对 Jiang 风格图像 CNN 与本市场的匹配关系，而非加密可预测性的全称否定。

---

## 仓库结构

```text
README.md
README.zh-CN.md
CITATIONS.md
CITATION.cff
NOTICE
LICENSE
docs/
  SCIENTIFIC-OVERVIEW.md
  ERRATA.md
  METHODS.md
  INTERPRETATION.md
  METHODS-crypto.md
  INTERPRETATION-crypto.md
  METHODS-us-to-crypto-transfer.md
  INTERPRETATION-us-to-crypto-transfer.md
  crypto-protocol.md
  vwpq-clip-oc-protocol.md
  vwpq-dollar-protocol.md
configs/
results/
  RESULTS.md
  crypto/
  crypto/transfer/
src_snapshot/
  hfdata/
  crypto/
```

---

## 数据与代码

| 层级 | 来源 | 是否随仓分发 |
|------|------|----------------|
| 方法论文 | Jiang, Kelly and Xiu (2023), *Journal of Finance* | 否 |
| 美股分钟 | HF Data Library 美股一分钟 OHLCV | 否 |
| 论文美股样本 | CRSP，经 WRDS | 否 |
| 加密分钟 | 实验主机上的 Binance 现货一分钟 K 线 | 否 |
| 本仓库 | 表格、协议与纯 Python 快照 | 是，Apache-2.0 |

权威表述见 [CITATIONS.md](CITATIONS.md)。

---

## 统计范围

研究 A 强调设定层面净夏普的符号与幅度；expand 臂的共享 bootstrap 为次要诊断。研究 B 与 C 报告描述性 Rank IC、ICIR 与零成本多空夏普。并不主张全部加密格子联合为正。研究 B 与 C 在主对照格上的失败，足以否定“股票月频工作单元可简单迁移至本加密样本”的叙述。
