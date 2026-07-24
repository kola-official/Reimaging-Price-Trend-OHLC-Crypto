# 价格趋势 OHLC 再思考 — 美股表示与加密迁移

**语言：** [English](README.md) · [中文](README.zh-CN.md)

**仓库：** [`Reimaging-Price-Trend-OHLC-Crypto`](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-Crypto)  
（原名 `Reimaging-Price-Trend-OHLC-reasearch`）

本仓库打包**两项共享 Jiang–Kelly–Xiu（2023）图像 CNN 设计语言**的实证研究（*Journal of Finance*，[doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268)）：

| 研究 | 科学杠杆 | 问题 |
|------|----------|------|
| **A — 美股 OHLC 表示** | **怎么画 K 线**（raw / 量权·额权 expand·clip） | 表示选择能否改善美股图像信号？ |
| **B — 加密资产类别迁移** | **换成谁的横截面**（Binance USDT 现货） | 同一日频图像配方能否离开股票市场？ |

完整 1 分钟库、图像张量与检查点**不**放在 GitHub；此处提供设计冻结、结果表、解读与小型纯 Python 快照。

---

## 摘要

### 研究 A — 成交量 / 成交额加权 OHLC（美股）

五臂对照、统一训练路径（hfdata 1 分钟 → 日线 → 灰度图 → 五 seed CNN；IS 1993–2002，OOS 2003–2025）。**额权 clip** 相对 raw 对角线平均净夏普约 **+0.18**；**expand** 在 **I60/R60** 大增、在 **I20/R20** 受损。Rank IC 差分小，**组合夏普**才是主展示面。  
→ [研究 A 亮点](#研究-a--美股-ohlc-表示) · [docs/METHODS.md](docs/METHODS.md) · [docs/INTERPRETATION.md](docs/INTERPRETATION.md)

### 研究 B — 加密现货本地重训（资产类别迁移）

同一 \(I,R\in\{5,20,60\}\) 图像 CNN，在 **Binance USDT 现货**上重训（IS 2018–2021，OOS 2022–2025）。**主对照格 I20/R20 失败**（Rank IC **−0.0495**）。在 20 日预测中，**I60/R20** 是最连贯的正格子（Rank IC **+0.032**，LS Sharpe 代理最高），但**仍远弱于美股复现量级**——与「**加密可交易横截面偏薄、样本偏短、共动偏强**」的工作性解释一致。  
→ [研究 B 亮点](#研究-b--加密资产类别迁移) · [docs/METHODS-crypto.md](docs/METHODS-crypto.md) · [docs/INTERPRETATION-crypto.md](docs/INTERPRETATION-crypto.md)

---

## 研究 A — 美股 OHLC 表示

### 五臂组合净夏普（对角线、共同键、10 bps）

| 设定 | raw | 量权 expand | 量权 clip | 额权 expand | **额权 clip** |
|------|----:|------------:|----------:|------------:|-------------:|
| **I5 / R5** | −0.40 | −0.30 | −0.18 | −0.31 | **−0.07** |
| **I20 / R20** | 3.07 | 1.36 | 1.89 | 1.42 | **3.13** |
| **I60 / R60** | 4.37 | **6.37** | 4.33 | 6.26 | 4.52 |

**相对 raw 的三格平均 Δ 净夏普：** 额权 clip **+0.18**；量权/额权 expand 约 **+0.11～0.13**；量权 clip **−0.34**。

完整表：[results/RESULTS.md](results/RESULTS.md)。视界依赖解读：[docs/INTERPRETATION.md](docs/INTERPRETATION.md)。

---

## 研究 B — 加密资产类别迁移

### 设计（简表）

| 项目 | 选择 |
|------|------|
| 市场 | Binance **USDT 现货**（v1 不含永续） |
| 数据 | 1 分钟 K 线 → UTC 日线 OHLC |
| 宇宙 | 点时点、滞后成交额 top-200；身份冻结（断点切段） |
| IS / OOS | **2018–2021** / **2022–2025** |
| 网格 | \(I,R\in\{5,20,60\}\) 九格；形成步长 \(=R\)（非重叠） |
| 模型 | Jiang 风格 CNN；五 seed；概率均值 |
| 报告路径 | 收盘到收盘 Rank IC；LS Sharpe 为 **0 成本代理**（非 delayed VWAP） |

方法：[docs/METHODS-crypto.md](docs/METHODS-crypto.md) · 协议摘要：[docs/crypto-protocol.md](docs/crypto-protocol.md) · 配置：[configs/crypto_daily_reimaging_v1.yaml](configs/crypto_daily_reimaging_v1.yaml)

### 九格 OOS Rank IC（2026-07-24，RTX 3090 审计）

|  | R5 | R20 | R60 |
|--|---:|---:|---:|
| **I5** | +0.014 | **+0.034** | +0.026 |
| **I20** | +0.018 | **−0.049** | +0.002 |
| **I60** | +0.009 | **+0.032** | −0.009 |

部分 LS Sharpe 代理（0 bp、收盘价）：**I60/R20 ≈ 1.36**，**I5/R20 ≈ 0.72**，**I20/R20 ≈ −1.52**。  
全表：[results/crypto/RESULTS.md](results/crypto/RESULTS.md) · CSV：[results/crypto/tables/crypto_nine_cell_oos.csv](results/crypto/tables/crypto_nine_cell_oos.csv)

### 研究 B 怎么读（先解读、再数字）

1. **美股配方在主格子上迁移失败。**  
   I20/R20 是股票侧最自然的「月频」工作单元；此处 Rank IC **为负**、AUC **&lt; 0.5**。这是**否定性确认结果**，不是「略弱但仍为正」。

2. **20 日预测里，更长的 60 日输入更站得住。**  
   对 \(R=20\)，**I60/R20** 的 Rank IC 接近最优，且 LS Sharpe 代理**最高**——网络似乎需要比预测视界**更长的视觉历史**。经典的 I20 上下文并不享有特权。

3. **即便最好的加密格子，也达不到美股量级。**  
   相关美股 I20 管线 Rank IC 约 **0.05** 量级，且多年 H–L 夏普在扣费后仍可观。加密最优 Rank IC 约 **0.03**，九格符号不一，R20 仅约 **72** 个非重叠形成日（R60 仅 **23**）。

4. **工作性解释：对这套方法而言，加密「盘子偏小」。**  
   更准确地说：点时点可交易横截面**偏薄、历史偏短、共动偏强**（top-200、2017 后流动性、同所同报价冲击），难以支撑 Jiang 风格图像 CNN 在股票上依赖的面板厚度。这是关于 **方法 × 市场匹配** 的假说，**不是**「任何模型都预测不了加密」。

完整论述：[docs/INTERPRETATION-crypto.md](docs/INTERPRETATION-crypto.md)。

---

## 仓库结构

```text
README.md / README.zh-CN.md
CITATIONS.md · CITATION.cff · NOTICE · LICENSE
docs/METHODS.md · INTERPRETATION.md          ← 研究 A
docs/METHODS-crypto.md · INTERPRETATION-crypto.md · crypto-protocol.md
configs/  protocol_vwpq_*.json · crypto_daily_reimaging_v1.yaml
results/  （研究 A）· results/crypto/ （研究 B）
src_snapshot/hfdata/ · src_snapshot/crypto/
```

---

## 数据与代码引用（摘要）

| 层级 | 来源 | 是否随仓分发 |
|------|------|----------------|
| 方法论文 | Jiang, Kelly & Xiu (2023), *JF* | 否（仅引用） |
| 美股分钟 | HF Data Library | 否 |
| 论文美股 | CRSP / WRDS | 否 |
| 加密分钟 | Binance spot 1m（实验机清单） | 否 |
| 本仓库 | 表格、协议、小型 Python 快照 | 是（Apache-2.0） |

权威表述见 [CITATIONS.md](CITATIONS.md)。

---

## 一句话对照

| 研究 | 一句话 |
|------|--------|
| **A** | 改 OHLC **画法**能系统性移动美股组合夏普；额权 clip 平均最优，expand 利好长视界。 |
| **B** | 同一图像 CNN **换到加密现货后主格失效**；I60→R20 相对最稳但仍远弱于美股，指向横截面「盘小、样本短」的方法边界。 |
