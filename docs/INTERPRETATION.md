# Interpretation of expand effects in Study A

Companion note on cryptocurrency transfer: [INTERPRETATION-crypto.md](INTERPRETATION-crypto.md).

This note organises the three-arm net-Sharpe pattern into an account of how expand alters image geometry and how that alteration may interact with short versus long forecasting windows. It does not establish causal identification of noise versus signal in the high–low range.

---

## 1. What expand changes geometrically

Under **expand**, open, close and volume remain identical to **raw**. Only the high–low span is rebuilt:

1. Volume-weighted quantiles \(q_{0.05}\) and \(q_{0.95}\) of intraday typical prices compress extreme, thinly traded ticks.  
2. The bar is then **expanded just enough** so that raw open and close still lie inside \([L,H]\).

Relative to raw, the candle’s **vertical range is therefore often shorter** on days when extremes are volume-poor, while the body (open–close) is unchanged. In image space the CNN sees a **less spiky high–low envelope** and a comparatively more stable path silhouette, especially when many days are stacked (large \(I\)).

**clip** goes further: it can move open and close into the quantile band, altering body geometry as well as the range. That is a different intervention and should not be conflated with expand.

---

## 2. Empirical pattern to be explained

On the shared economic path (next open, 10 bp, diagonal units, common keys):

| Horizon style | expand − raw (net Sharpe) | Qualitative |
|---------------|---------------------------|-------------|
| Short (I5/R5) | about **+0.10** | modest gain |
| Intermediate (I20/R20) | about **−1.71** | clear deterioration |
| Long (I60/R60) | about **+2.00** | large gain |

Mean of the three gaps remains positive (~+0.13) because the long-horizon gain outweighs the intermediate loss. Rank IC gaps stay near zero on average, so the horizon dependence is **more visible in the portfolio Sharpe path** than in mean ranking skill.

---

## 3. Working hypothesis: range compression and horizon-dependent use of “noise”

### 3.1 Expand as mild volatility / outlier attenuation in the image

By replacing raw extremes with volume-aware quantiles (then only barely expanding to cover open/close), expand **attenuates volume-light spikes** in the drawn high–low range. The image is less dominated by single-print extremes. That is a form of **visual denoising of the range channel**, not a change in label or fill prices.

### 3.2 Why long windows (I60/R60) may benefit

Over **quarterly-scale** images and holds, the CNN must summarise a long path. Persistent shape—drift, multi-week range regimes, slow oscillations—matters more than day-specific spikes. Compressing volume-poor extremes can:

- stabilise the vertical scaling of the panel (fewer days pin the top/bottom of the image to an outlier),  
- make multi-month geometry more comparable across names,  
- reduce overfitting to idiosyncratic one-day extremes that do not survive a 60-day return horizon.

Under that reading, **range denoising acts as a regulariser for long-horizon visual features**, consistent with a large **positive** expand−raw Sharpe gap at I60/R60.

### 3.3 Why intermediate windows (I20/R20) may suffer

At **monthly** scale, a non-trivial share of predictable structure—if any—may sit in **higher-frequency irregularity**: overnight gaps, sharp but volume-bearing swings, short-lived stress marks. Raw high–low keeps those marks; expand softens volume-light tails and can **blur** features that a 20-day panel still relies on for ranking and for high–low portfolio formation.

In that sense, **what looks like “noise” at long horizons can still be informative texture at intermediate horizons**. Suppressing it need not help every \(I,R\). The sharp **negative** expand−raw gap at I20/R20 is consistent with **over-smoothing of mid-frequency visual cues**, though other explanations (sample composition, cost interaction, decile sparsity) remain open.

### 3.4 Short windows (I5/R5)

Weekly images are short; a single extreme day is a large fraction of the panel. Mild range compression can either:

- remove one-day artefacts that dominate a five-bar chart, or  
- remove genuine short-horizon texture.

Empirically expand still shows a **small positive** Sharpe gap at I5/R5, while **clip**—which also reshapes open/close—does even better on this cell. Short-horizon behaviour is therefore **not pure “noise is good”**; both mild range cleaning (expand) and body adjustment (clip) can help, but the mechanisms differ.

---

## 4. How this relates to clip

| Construction | Open/close | High/low | Implied visual effect |
|--------------|------------|----------|------------------------|
| expand | fixed to raw | quantile + expand | softens extremes; body fixed |
| clip | pulled into band | quantile band | softens extremes **and** can shrink bodies |

If long-horizon gains were driven purely by “any compression helps,” clip should dominate expand at I60. It does **not**: at I60/R60, expand’s Sharpe remains far above clip’s. That pattern favours a more specific claim:

> **Keeping open and close at raw values while only editing the range** (expand) appears better aligned with long-horizon path learning than **moving open/close into a thinner band** (clip).

Clip’s relative strength at I5—and its improvement over expand at I20—suggests that **short- and mid-horizon images can benefit from body-level adjustments**, even when the same adjustments fail at long horizon.

---

## 5. What this account does *not* claim

1. **Not proven.** We did not measure image-level realised range statistics day-by-day, nor ablate “quantile only” versus “expand to cover O/C,” nor randomise noise injection. The horizon pattern **motivates** the denoising story; it does not identify it.  
2. **Not a statement that markets are noisier at short horizons in a physical sense**—only that **raw high–low extremes may be more useful as features** for some windows than others.  
3. **Not a claim of uniform improvement** from expand or clip. Intermediate deterioration under expand is part of the same empirical object as the I60 gain.  
4. **Labels and fills stay raw.** Any benefit is through **what the network sees**, not through trading a smoothed price.

---

## 6. Implications for follow-up work

| Direction | Purpose |
|-----------|---------|
| Image diagnostics | Compare raw vs expand distributions of bar range, fraction of days with \(H\) or \(L\) set by quantiles vs open/close, and vertical scaling statistics by \(I\) |
| Controlled ablations | Quantile-only H/L without expand; expand without volume weights; synthetic spike injection |
| Horizon grid | Finer \(I,R\) ladder around 20 to map where expand switches from harmful to helpful |
| Clip family | Separate “range only” from “body clip” more cleanly |

Until those checks exist, the preferred scientific language is:

> Expand’s large I60/R60 net-Sharpe gain, together with its I20/R20 deterioration, is **consistent with** a horizon-dependent trade-off in which **volume-aware compression of high–low extremes stabilises long visual paths but can discard mid-horizon texture that raw extremes still carry.**

That sentence is the analysis we stand on in the public READMEs for the **share-volume expand** arm.

---

## 7. Dollar-volume weights and the five-way extension

Dollar weights replace \(w=V\) with \(w=pV\), \(p=(H+L+C)/3\). On many days the two weight systems are close; large intraday price moves tilt mass toward high-price minutes under dollar weighting.

### 7.1 Empirical five-way pattern (10 bp diagonal)

| Arm | Mean Δ Sharpe vs raw | I20 behaviour | I60 behaviour |
|-----|---------------------:|---------------|---------------|
| share expand | +0.13 | large loss | large gain (best cell) |
| dollar expand | +0.11 | large loss (similar) | large gain (near share expand) |
| share clip | −0.34 | still below raw | ≈ raw |
| **dollar clip** | **+0.18** | **slight gain** | modest gain |

### 7.2 Working readings

1. **Expand is mostly about geometry, not share vs dollar.** Switching to \(pV\) barely moves the expand profile: I60 still wins, I20 still loses. The horizon-dependent range story above is therefore not an artefact of equal-weighting every share.  
2. **Clip geometry + dollar weights is the robust average.** Dollar clip is the only arm with **positive Δ on every diagonal cell**. Restoring I20 (where share clip and both expands fail) is the distinctive economic fact. One speculative account is that clipping O/C with dollar-aware bands removes body outliers that are **price-level** as well as volume-level extremes—more helpful when the panel must rank names over monthly holds—while still allowing some range compression. This is **not** identified by ablation.  
3. **Best single cell remains share expand at I60.** If the application is quarterly-style only, expand (share or dollar) still dominates clip.

Preferred five-way language:

> Dollar-volume weighting leaves the **expand** horizon trade-off essentially unchanged, but **dollar-weighted clip** lifts the three-setting mean net Sharpe versus raw by about **+0.18** and is the only representation that does not sacrifice the intermediate (I20) cell under this path.

