# Protocol freeze: `vwpq_clip` / `vwpq_clip_oc`

| Field | Value |
|-------|--------|
| Protocol id | `vwpq_clip` (alias `vwpq_clip_oc`) |
| Frozen at | 2026-07-21 |
| Parent plan | hfdata-raw-vs-vwpq-experiment-plan.md **v3.6** (expand arm unchanged) |
| Distinct from | `vwpq` / `vwpq_expand` (O/C/V = raw; H/L expand-not-clip) |

## Bar construction

1. Aggregate RTH 1-min bars to a raw session bar (open=first open, high=max high, low=min low, close=last close, volume=sum).
2. Typical price \(p_t=(H_t+L_t+C_t)/3\), weights = minute volume.
3. Volume-weighted quantiles \(q_{05}, q_{95}\) (same helper as expand).
4. Set **\(L=q_{05}\), \(H=q_{95}\)** (no expand to cover raw O/C).
5. **Clip open/close into [L, H]**:
   - \(O'=\mathrm{clip}(O_{\mathrm{raw}}, L, H)\)
   - \(C'=\mathrm{clip}(C_{\mathrm{raw}}, L, H)\)
6. Volume \(V=V_{\mathrm{raw}}\).
7. Zero-volume / invalid: `vwpq_valid=false`; **do not** fall back to raw OHLC as a valid clip representation, and **do not** apply expand.

## Labels, MA, execution (representation-only clip)

| Stream | Source |
|--------|--------|
| Classification labels / Rank IC returns | **raw close** (unchanged) |
| Moving average on images | **raw close** rolling mean (unchanged) |
| Portfolio entry/exit open | **raw open** (unchanged) |
| Image O/H/L/C body geometry | **clip arm** O′/H/L/C′ |

Interpretation: clip changes **what the CNN sees**, not the economic fill prices or label definition.

## Outer split & training (parity with expand run)

- IS **1993–2002**, OOS **2003–2025**, exclude **2026**
- Primary training protocol: `purged_primary`
- Seeds: 0–4 ensemble mean probability

## Frozen matrix scope (GPU)

**Reduced priority matrix (frozen for this goal):** diagonal only

\[
(I,R)\in\{(5,5),(20,20),(60,60)\}\times\{\texttt{vwpq\_clip}\}
\]

with 5 seeds each (15 train jobs). Off-diagonal (I,R) for clip are **out of scope** for this freeze; expand/raw full 9-unit Rank IC tables may still be cited for context with clear scope notes.

## Output namespaces (must not clobber expand)

| Artifact | Path pattern |
|----------|----------------|
| Daily bars | `data/hfdata/daily/vwpq_clip/year=YYYY/*.parquet` |
| Images | `data/hfdata/images/vwpq_clip/i{I}/year=YYYY/` |
| Models / OOS preds | `outputs/hfdata/purged_primary/vwpq_clip/i{I}_r{R}/seed{s}/` |
| Freeze JSON | `manifests/hfdata/protocol_vwpq_clip_oc.json` |
| Comparison | `outputs/hfdata/reports/three_way_raw_expand_clip.*` |
