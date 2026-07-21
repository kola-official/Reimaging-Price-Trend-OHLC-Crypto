# 价格趋势 OHLC 表示再思考

**语言：** [English](README.md) · [中文](README.zh-CN.md)

**仓库：** [`Reimaging-Price-Trend-OHLC-reasearch`](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-reasearch)  
**问题：** 相对标准日线 OHLC，用**成交量 / 成交额**加权构造高低价，能否改善基于 CNN 图像的美股趋势信号？

本仓库汇总**五臂对照**实验结果（hfdata 1 分钟 → 日线 → K 线图像 → CNN 集成）。叙述侧重**表示选择如何改变组合表现**；正式统计推断放在次要位置。机制解读见 [docs/INTERPRETATION.md](docs/INTERPRETATION.md)。

---

## 摘要

在同一训练与评估协议下，比较五种日线构造：

| 臂 | 权重 | 图像中改变的内容 |
|----|------|------------------|
| **raw** | — | 标准开 / 高 / 低 / 收 / 量 |
| **量权 expand** | 成交量 \(V\) | 开收量=raw；高/低为分位并**外扩**盖住开收 |
| **量权 clip** | \(V\) | 高/低=分位带；开/收**裁进**带内 |
| **额权 expand** | 成交额 \(pV\) | 规则同 expand；\(p=(H+L+C)/3\) |
| **额权 clip** | \(pV\) | 规则同 clip，权为成交额 |

模型为 Jiang、Kelly 与 Xiu（2023）图像 CNN 思路下的实现（*Journal of Finance*，[doi:10.1111/jofi.13268](https://doi.org/10.1111/jofi.13268)）。训练期 **1993–2002**，样本外 **2003–2025**。标签、均线与成交价一律用 **raw** 价格，仅绘制几何不同。

**主要结果（对角线、10 bps 经济路径）**

1. **额权 clip** 相对 raw 的平均净夏普约 **+0.18**，且**三格差分均为正**——包括量权臂大幅落后的 **I20/R20**。  
2. **量权 / 额权 expand** 仍是 I60 最强（相对 raw 约 **+1.9～+2.0**），但 I20 仍明显受损；三格平均约 **+0.11～0.13**。  
3. **量权 clip** 主要利好 I5，**不能**抬高三格相对 raw 的平均（约 **−0.34**）。  
4. Rank IC 差分仍小；**组合夏普**才是表示差异的主展示面。

---

## 结果亮点（提升落在何处）

### 五臂组合净夏普（对角线、共同键、10 bps）

路径：下一开盘入场 / 计划开盘离场（必要时冻结退出代理）；等权高–低十分位；年化 \(\sqrt{252}\)。

| 设定 | raw | 量权 expand | 量权 clip | 额权 expand | **额权 clip** |
|------|----:|------------:|----------:|------------:|-------------:|
| **I5 / R5**（约周频） | −0.40 | −0.30 | −0.18 | −0.31 | **−0.07** |
| **I20 / R20**（约月频） | 3.07 | 1.36 | 1.89 | 1.42 | **3.13** |
| **I60 / R60**（约季频） | 4.37 | **6.37** | 4.33 | 6.26 | 4.52 |

**相对 raw 的三格平均 Δ 净夏普**

| 臂 | 平均 Δ |
|----|--------:|
| 量权 expand | +0.13 |
| 量权 clip | −0.34 |
| 额权 expand | +0.11 |
| **额权 clip** | **+0.18** |

完整表见 [results/RESULTS.md](results/RESULTS.md) · `results/tables/five_way_economic_sharpe.csv`。

**如何阅读提升**

- **额权 clip** 是本路径下**平均最优**表示：I5 提升最大，是**唯一**不在 I20 崩塌的非 raw 臂，I60 仍略优于 raw。  
- **expand（量权或额权）** 价值集中在 **I60**（保留实体、压缩影线）；I20 仍受损。换成成交额权重**不能**消掉 expand 的 I20 惩罚。  
- 绝对夏普数值可能偏大；**优先看臂间差分**。

### 为何 expand 在 I60 大增、在 I20 受损？

**expand** 保持开收等于 raw，仅用成交量加权分位重建高低价，再略外扩以盖住开收。许多交易日上，这会**削弱量轻、极尖的影线**，使图像更少被单笔极端报价“钉住”上下界。

与上表一致、尚待消融验证的工作性解释是：**影线“纹理”的价值随预测视界而变**——

| 视界 | expand − raw（净夏普） | 解读 |
|------|------------------------|------|
| **长（I60/R60）** | 大幅**上升**（约 +2） | 多月路径中的漂移与区间形态更重要；压缩量轻极值，有助于稳定纵向缩放、减轻对单日极端影线的过拟合，近似一种**视觉正则**。 |
| **中（I20/R20）** | 大幅**下降**（约 −1.7） | 月频面板仍可能依赖更高频的不规则结构；raw 高低价保留这些痕迹，expand 的平滑可能**丢掉中频线索**。 |
| **短（I5/R5）** | 小幅**上升**（约 +0.1） | 五日图中单日极端占比大；轻度压影线或有益，而 **clip**（同时改动开收实体）在该格上更好。 |

一句话：**对长期视觉路径像噪声的东西，在中期仍可能是有用纹理。**  
另：I60 的大增益来自 **expand 而非 clip**——说明长期收益更像是「**只改影线、保留实体**」的结果，而非「任意压缩都更好」。

完整论述：[docs/INTERPRETATION.md](docs/INTERPRETATION.md)。

### 排序能力（配对 Δ Rank IC，描述性）

| 对比（对角线三格平均） | Δ Rank IC |
|------------------------|----------:|
| 量权 expand − raw | −0.0018 |
| 量权 clip − raw | −0.0037 |
| 额权 expand − raw | −0.0020 |
| 额权 clip − raw | −0.0004 |

由表示引起的**排序**变化偏小。**经济路径**上更易看到 expand 的 I60 与额权 clip 的跨视界增益。

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
| 全矩阵科学臂 | raw vs **量权 expand**（九格） |
| 五臂经济对照 | 对角线 (5,5)/(20,20)/(60,60) × raw + 量权 expand/clip + 额权 expand/clip |
| 成交 | 下一会话开盘；单边 10 bps；成交开盘一律 raw |

方法细节：[docs/METHODS.md](docs/METHODS.md)。  
协议：[量权 clip](docs/vwpq-clip-oc-protocol.md) · [额权 expand/clip](docs/vwpq-dollar-protocol.md)。

---

## 仓库结构

```text
README.md / README.zh-CN.md
CITATIONS.md · CITATION.cff · NOTICE · LICENSE (Apache-2.0)
docs/METHODS.md · docs/INTERPRETATION.md · docs/vwpq-clip-oc-protocol.md · docs/vwpq-dollar-protocol.md
results/ · configs/ · src_snapshot/
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

本文档强调**设定层面的净夏普符号与幅度**，尤其是 **I60 的 expand**、**额权 clip 的跨视界平均** 与 **I20 上量权臂的损失**。

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
| **本项目** | [kola-official/Reimaging-Price-Trend-OHLC-reasearch](https://github.com/kola-official/Reimaging-Price-Trend-OHLC-reasearch) | 结果、协议、小型变换快照 |
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
