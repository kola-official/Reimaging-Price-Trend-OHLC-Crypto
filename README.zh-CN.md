# 价格趋势 OHLC 表示再思考

**语言：** [English](README.md) · [中文](README.zh-CN.md)

**仓库：** [`Reimaging-Price-Trend-ohcl-reasearch`](https://github.com/kola-official/Reimaging-Price-Trend-ohcl-reasearch)  
**问题：** 相对标准日线 OHLC，用成交量加权方式构造高低价，能否改善基于 CNN 图像的美股趋势信号？

本仓库汇总三臂对照的**实验结果**（hfdata 1 分钟 → 日线 → K 线图像 → CNN 集成）。叙述侧重**表示选择如何改变组合表现**；正式统计推断放在次要位置。

---

## 摘要

在同一训练与评估协议下，比较三种日线构造：

| 臂 | 图像中改变的内容 |
|----|------------------|
| **raw** | 标准开 / 高 / 低 / 收 / 量 |
| **expand** | 开、收、量与 raw 相同；高/低为成交量加权分位，并**外扩**使开收仍落在区间内 |
| **clip** | 高/低同为分位带；开/收若落在带外则**裁剪进**该带 |

模型为 Jiang、Kelly 与 Xiu（2023）图像 CNN 思路下的实现（*Journal of Finance*，[doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268)）。训练期 **1993–2002**，样本外 **2003–2025**。标签、均线与成交价一律用 **raw** 价格，仅绘制几何不同。

**主要结果**

1. **经济路径（单边 10 bps、下一开盘多空）：** 在对角线图像/持有期设定上，**expand 相对 raw 的平均净夏普约 +0.13**。增益主要来自 **I60/R60（约 +2.00）**，**I5/R5 亦约 +0.10**。  
2. **clip** 在 **I5/R5** 上净夏普同时优于 raw 与 expand（clip **−0.18** vs raw **−0.40**、expand **−0.30**），在 **I20/R20** 上优于 expand（约 **+0.53**），但**不能**拉高三格相对 raw 的平均。  
3. 截面排序（Rank IC）跨设定**有正有负**；表示差异在**组合夏普路径**上比在平均 Rank IC 上更清晰。

expand 臂的 bootstrap 诊断见 [results/](results/)，**不是**本报告主线。

---

## 结果亮点（提升落在何处）

### 组合净夏普（对角线、共同键、10 bps）

路径：下一开盘入场 / 计划开盘离场（必要时冻结退出代理）；等权高–低十分位；年化 \(\sqrt{252}\)。

| 设定（图像天数 × 持有天数） | raw | expand | clip | expand − raw | clip − raw |
|----------------------------|----:|-------:|-----:|-------------:|-----------:|
| **I5 / R5**（约周频） | −0.40 | −0.30 | **−0.18** | **+0.10** | **+0.21** |
| **I20 / R20**（约月频） | 3.07 | 1.36 | 1.89 | −1.71 | −1.18 |
| **I60 / R60**（约季频） | 4.37 | **6.37** | 4.33 | **+2.00** | −0.05 |
| **三格等权平均** | — | — | — | **+0.13** | −0.34 |

**如何阅读提升**

- **expand 相对 raw：** 平均净夏普差为**正（+0.13）**。最大贡献来自 **I60/R60**（约两个夏普单位）；I5 也有改善；I20 方向相反，故平均是得失相抵，而非处处抬升。  
- **clip 相对 raw：** 提升**局部**。在 **I5/R5**，clip 为**三臂最优**；I20 介于 raw 与 expand 之间（优于 expand，仍低于 raw）；I60 与 raw 接近、远低于 expand。  
- 绝对夏普数值可能偏大；**优先看臂间差分**，不宜把单一数字当作实盘年化夏普。

### 排序能力（配对 Δ Rank IC，描述性）

| 对比（对角线三格平均） | Δ Rank IC |
|------------------------|----------:|
| expand − raw | −0.0018 |
| clip − raw | −0.0037 |
| clip − expand | −0.0020 |

由表示引起的**排序**变化偏小，平均并不有利。**经济路径**上更易看到 expand 的 I60 与 clip 的 I5 改善。

### expand 相对 raw 的九格 Rank IC 矩阵

raw 与 expand 各完成九个 \((I,R)\) 单元（五种子）。九格平均 Δ Rank IC 接近零（约 +0.00018），格子符号不一（如 I20/R20 为负，部分 I5 略正）。详见 `results/tables/unit_rank_ic.csv`。

---

## 实验设计（简表）

| 项目 | 选择 |
|------|------|
| 股票宇宙 | hfdata 美股 1 分钟库（约 1,391 只） |
| 样本内 | 1993–2002 |
| 样本外 | 2003–2025（排除 2026） |
| 模型 | 固定尺寸灰度 OHLC+均线图像 CNN；五随机种子；概率均值集成 |
| 训练协议 | 时间块训练/验证 + 净化间隔（`purged_primary`） |
| 全矩阵科学臂 | raw vs **expand** |
| 三臂经济对照 | 仅对角线 (5,5)、(20,20)、(60,60) |
| 成交 | 下一会话开盘；单边 10 bps；即使图像为 clip，成交开盘仍用 raw |

方法细节：[docs/METHODS.md](docs/METHODS.md)。  
clip 协议冻结：[docs/vwpq-clip-oc-protocol.md](docs/vwpq-clip-oc-protocol.md)。

---

## 仓库结构

```text
README.md                 ← 英文
README.zh-CN.md           ← 中文（本文件）
CITATIONS.md              ← 数据、代码、文献引用（权威清单）
CITATION.cff              ← GitHub 引用元数据
NOTICE                    ← 第三方归属
LICENSE                   ← Apache License 2.0
docs/ · configs/ · results/ · src_snapshot/
```

完整 1 分钟库、图像二进制与训练检查点**不**放在本仓库。

---

## 推断附录（次要）

仅对 **expand** 臂报告了共享月块 bootstrap（\(B=5000\)）：

| 估计量 | 点估计 | 在本仓库中的角色 |
|--------|--------|------------------|
| 九格平均 Δ Rank IC | ≈ +0.00018 | 接近零；排序非主线 |
| 三格平均 Δ 净夏普 | ≈ +0.13 | 与上表经济结果一致 |
| 5% 单侧支持 θ>0 | 不作主结论 | 见 `results/json/final_summary.json` |

本文档强调**设定层面的净夏普符号与幅度**，尤其是 **I60/R60 的 expand** 与 **I5/R5 的 clip**。

---

## 数据来源

| 层级 | 来源 | 说明 |
|------|------|------|
| **本实验（分钟→日线）** | **HF Data Library** 美股高频 OHLCV（实验机 1 分钟 parquet） | 公开页：[Hugging Face `elkassabgi/hfdatalibrary`](https://huggingface.co/datasets/elkassabgi/hfdatalibrary)。实验路径示例：`/share/home/user/snliu/hfdata_us_1min`。**本仓库不分发原始分钟数据。** |
| **Jiang–Kelly–Xiu（2023）论文** | **CRSP** 美股日频（通常经 WRDS） | 标识为 PERMNO；论文样本多描述自 1990 年代初至 2019 年。**本仓库不包含 CRSP 数据。** |
| **派生日线** | 本管线生成的 raw / expand / clip | 见 [docs/METHODS.md](docs/METHODS.md)。 |

本实验标识为**源 ticker / 序列文件**，不是 CRSP PERMNO；结论条件于该面板。

完整表述：[CITATIONS.md §2](CITATIONS.md)。

---

## 参考代码仓库

| 仓库 | 链接 | 作用 |
|------|------|------|
| **本项目** | [kola-official/Reimaging-Price-Trend-ohcl-reasearch](https://github.com/kola-official/Reimaging-Price-Trend-ohcl-reasearch) | 结果、协议、小型变换快照 |
| **ReImagining_Price_Trends** | [gaoym4321/ReImagining_Price_Trends](https://github.com/gaoym4321/ReImagining_Price_Trends) | 作者风格/社区实现，用于结构对照（本地 bootstrap 配置中有 pin 提交） |
| **Stock_CNN** | [lich99/Stock_CNN](https://github.com/lich99/Stock_CNN) | 轻量 smoke / 结构交叉检查 |

第三方仓库保留**各自许可证**。见 [CITATIONS.md §3](CITATIONS.md) 与 [NOTICE](NOTICE)。

---

## 参考论文

> Jiang, J., Kelly, B., & Xiu, D. (2023). *(Re-)Imag(in)ing price trends.*  
> *The Journal of Finance*, 78(6), 3193–3249.  
> https://doi.org/10.1111/jofi.13268

本研究聚焦**表示**，**不**声称复现该文在官方 CRSP 图像档案上的绝对 Accuracy / Rank IC / Sharpe。问题是：在固定 CNN 管线与 hfdata 派生日线下，**不同高低价构造**是否改变行为。

BibTeX 与扩展文献：[CITATIONS.md](CITATIONS.md)。

---

## 开源协议

| 项目 | 选择 |
|------|------|
| **开源许可证** | **[Apache License 2.0](LICENSE)** |
| **归属说明** | [NOTICE](NOTICE) |
| **选用理由** | 适合研究代码发布；含专利授权；便于用 NOTICE 声明第三方数据与软件且不必再分发其本体 |

**本许可证不覆盖：** CRSP 数据、HF Data Library 全量转储、Journal of Finance 论文 PDF/图、以及第三方 GitHub 完整代码树。请按各自条款获取。

---

## 如何引用本仓库

见 [CITATION.cff](CITATION.cff) 与 [CITATIONS.md §4](CITATIONS.md) 中的 BibTeX。讨论图像 CNN 价格趋势框架时，请同时引用 **Jiang, Kelly & Xiu（2023）**。
