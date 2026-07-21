# Protocol freeze: dollar-volume VWPQ expand and clip

| Field | Value |
|-------|--------|
| Frozen at | 2026-07-21 |
| Parent | hfdata-raw-vs-vwpq-experiment-plan.md v3.6 + vwpq-clip-oc |

## Protocol IDs (do not reuse share-volume names)

| Protocol id | Path arm | O/C rule | Weights |
|-------------|----------|----------|---------|
| `vwpq_dollar_expand` | `vwpq_d` | O/C/V = raw; H/L expand to cover O/C | \(w_t = p_t V_t\), \(p_t=(H+L+C)/3\) |
| `vwpq_dollar_clip` | `vwpq_d_clip` | H/L = dollar quantile band; O/C clipped into [L,H] | same |

Share-volume arms remain: `vwpq` / `vwpq_expand`, `vwpq_clip` / `vwpq_clip_oc` with \(w_t=V_t\).

## Quantiles

- \(q_{0.05}\), \(q_{0.95}\) of typical prices with the chosen weights (stable weighted quantile).
- Zero volume / invalid: `vwpq_valid=false`; no silent fallback to raw as a valid representation.

## Labels / MA / execution

Always **raw** close (labels, MA) and **raw** open (fills). Representation-only image OHLC.

## Frozen matrix (GPU)

Diagonal only: \((I,R)\in\{(5,5),(20,20),(60,60)\}\) × 5 seeds × {`vwpq_d`, `vwpq_d_clip`}.

## Output namespaces

```text
data/hfdata/daily/vwpq_d/
data/hfdata/daily/vwpq_d_clip/
data/hfdata/images/vwpq_d/
data/hfdata/images/vwpq_d_clip/
outputs/hfdata/purged_primary/vwpq_d/
outputs/hfdata/purged_primary/vwpq_d_clip/
manifests/hfdata/protocol_vwpq_dollar.json
```
