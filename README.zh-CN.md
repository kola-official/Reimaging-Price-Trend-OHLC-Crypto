# 价格趋势 OHLC 表示再思考与加密资产类别迁移

**语言：** [English](README.md) · [中文](README.zh-CN.md)

**仓库：** [Reimaging-Price-Trend-OHLC-Crypto](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-Crypto)

本仓库报告两项共享 Jiang、Kelly 与 Xiu（2023）图像卷积设计语言的实证研究，原文刊于 *The Journal of Finance*（[doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268)）。研究 A 在固定学习协议下改变美股日线 OHLC 的构造方式；研究 B 保持该协议不变，将股票宇宙替换为单一交易所的加密货币现货横截面。完整一分钟行情、图像张量与模型检查点保留在实验主机；本仓库发布设计说明、结果表、解读文字与精简的纯 Python 工具。

| 研究 | 实验杠杆 | 研究问题 |
|------|----------|----------|
| A. 美股 OHLC 表示 | raw、量权与额权 expand/clip 下的日线几何 | 表示选择是否改变样本外组合表现 |
| B. 加密资产类别迁移 | Binance USDT 现货与本地重训 | 同一日频图像设定在股票之外是否仍具横截面排序能力 |

---

## 摘要

### 研究 A. 美股成交量与成交额加权 OHLC 几何

在 hfdata 一分钟数据、灰度 OHLC 图像与五种子 CNN 的统一路径下，样本内为 1993–2002 年，样本外为 2003–2025 年。额权 clip 相对 raw 的对角线平均净夏普约提高 0.18。expand 构造在 I60/R60 占优，但在 I20/R20 明显恶化。各臂之间的 Rank IC 差分较小；组合夏普是表示效应的主要表现面。

文档见 [docs/METHODS.md](docs/METHODS.md)、[docs/INTERPRETATION.md](docs/INTERPRETATION.md)、[results/RESULTS.md](results/RESULTS.md)。

### 研究 B. 加密货币现货本地重训

同一网格 \(I,R\in\{5,20,60\}\) 在 Binance USDT 现货上重训，样本内 2018–2021 年，样本外 2022–2025 年。主对照格 I20/R20 的 Rank IC 为 −0.0495，AUC 为 0.450。对二十日预测，I60/R20 的 Rank IC 为 0.032，并在矩阵中取得最强的零成本多空夏普代理，但仍明显低于相关美股复现中约 0.05 的 Rank IC 量级。该模式与横截面偏薄、历史偏短且共动偏强的加密现货结构相一致，难以支撑与股票相当的视觉趋势提取。

文档见 [docs/METHODS-crypto.md](docs/METHODS-crypto.md)、[docs/INTERPRETATION-crypto.md](docs/INTERPRETATION-crypto.md)、[results/crypto/RESULTS.md](results/crypto/RESULTS.md)。

---

## 研究 A. 美股 OHLC 表示

### 对角线组合净夏普，单边十个基点

下一交易时段开盘入场，按计划开盘离场；等权高减低十分位；夏普年化因子为 \(\sqrt{252}\)。

| 设定 | raw | 量权 expand | 量权 clip | 额权 expand | 额权 clip |
|------|----:|------------:|----------:|------------:|----------:|
| I5 / R5 | −0.40 | −0.30 | −0.18 | −0.31 | −0.07 |
| I20 / R20 | 3.07 | 1.36 | 1.89 | 1.42 | 3.13 |
| I60 / R60 | 4.37 | 6.37 | 4.33 | 6.26 | 4.52 |

相对 raw 的三格平均净夏普变化：额权 clip 为 +0.18，量权与额权 expand 约为 +0.11 至 +0.13，量权 clip 为 −0.34。额权 clip 平均最优，且是唯一未在 I20/R20 崩塌的非 raw 臂；expand 的增益集中于 I60/R60。视界依赖解读见 [docs/INTERPRETATION.md](docs/INTERPRETATION.md)，完整表见 [results/RESULTS.md](results/RESULTS.md)。

---

## 研究 B. 加密资产类别迁移

### 设计

| 要素 | 设定 |
|------|------|
| 市场 | Binance USDT 现货；不含永续合约 |
| 数据 | 一分钟 K 线聚合为 UTC 日线 OHLC |
| 宇宙 | 点时点、按滞后成交额取前 200；身份断点处切段 |
| 样本 | 样本内 2018–2021；样本外 2022–2025 |
| 网格 | \(I,R\in\{5,20,60\}\)；形成步长等于 \(R\) |
| 模型 | Jiang 风格 CNN；五种子；概率均值集成 |
| 报告指标 | 收盘到收盘 Rank IC；零成本多空夏普仅作经济示意 |

详见 [docs/METHODS-crypto.md](docs/METHODS-crypto.md)、[docs/crypto-protocol.md](docs/crypto-protocol.md) 与 [configs/crypto_daily_reimaging_v1.yaml](configs/crypto_daily_reimaging_v1.yaml)。

### 样本外 Rank IC 矩阵

评估日期 2026-07-24，计算设备为双 RTX 3090。

|  | R5 | R20 | R60 |
|--|---:|---:|---:|
| I5 | +0.014 | +0.034 | +0.026 |
| I20 | +0.018 | −0.049 | +0.002 |
| I60 | +0.009 | +0.032 | −0.009 |

零成本收盘价多空夏普代理中，I60/R20 为 1.36，I5/R20 为 0.72，I20/R20 为 −1.52。全表见 [results/crypto/RESULTS.md](results/crypto/RESULTS.md) 与 [results/crypto/tables/crypto_nine_cell_oos.csv](results/crypto/tables/crypto_nine_cell_oos.csv)。

### 解读

美股图像设定在主对照格上的迁移失败。I20/R20 在股票应用中是标准的月频工作单元，但在本样本中 Rank IC 为负且分类 AUC 低于 0.5。这是否定性确认结果，而非正信号的轻微衰减。

对二十日标签，六十日图像输入构成最连贯的正结果。I60/R20 的 Rank IC 接近最优，并取得网格中最强的多空夏普代理。在存在可检出排序结构时，模型似乎需要长于预测视界的视觉历史；\(I\) 与 \(R\) 相等在加密设定中并不具有特权。

即便最优加密格子也弱于美股基准。相关美股 I20 集成的 Rank IC 约 0.05，且多年高减低夏普在扣费后仍可观。加密最优 Rank IC 约 0.03，九格符号不一致，并基于仅 72 个非重叠二十日形成日估计；六十日形成日仅 23 个。

合理的解释是横截面深度不足。点时点合格标的上限为 200，流动性历史主要集中于 2017 年之后，且标的共享交易所、报价资产与全市场冲击，面板因而比 Jiang 风格图像 CNN 所依赖的股票宇宙更薄、更短、共动更强。该判断限于本方法与本市场的匹配关系，并不主张任意模型下加密收益均不可预测。

展开论述见 [docs/INTERPRETATION-crypto.md](docs/INTERPRETATION-crypto.md)。

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
  METHODS.md
  INTERPRETATION.md
  METHODS-crypto.md
  INTERPRETATION-crypto.md
  crypto-protocol.md
  vwpq-clip-oc-protocol.md
  vwpq-dollar-protocol.md
configs/
  protocol_vwpq_clip_oc.json
  protocol_vwpq_dollar.json
  crypto_daily_reimaging_v1.yaml
  asset_exclusions_v1.json
results/
  RESULTS.md
  tables/
  json/
  crypto/
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

完整引用表述见 [CITATIONS.md](CITATIONS.md)。

---

## 统计范围

研究 A 对 expand 臂报告共享月块 bootstrap，作为次要诊断，见 `results/json/final_summary.json`。研究 B 报告描述性 Rank IC、ICIR 与零成本多空夏普。并不主张九格联合为正；主对照格 I20/R20 已否定该叙述。仓库强调研究 A 中设定层面的符号与幅度，以及研究 B 中有边界的迁移失败与格子图谱。

---

## 对照总结

| 研究 | 结论 |
|------|------|
| A | 改变 OHLC 几何可系统移动美股组合夏普；额权 clip 平均最优，expand 利好长视界。 |
| B | 同一图像 CNN 迁移至加密现货后主格失效；六十日输入对二十日预测相对最稳，但整体仍远弱于美股，指向横截面偏薄与样本偏短的方法边界。 |
