# Interpretation of Study C: frozen US-to-cryptocurrency transfer

Study C applies frozen United States equity image-CNN weights for raw, expand and clip representations to Binance USDT spot out-of-sample images without retraining. Numbers are from [results/crypto/transfer/](../results/crypto/transfer/). Study B retrain figures are from [results/crypto/RESULTS.md](../results/crypto/RESULTS.md). Repository spine: [SCIENTIFIC-OVERVIEW.md](SCIENTIFIC-OVERVIEW.md).

---

## 1. Design intent

Study A shows that equity portfolio performance can move when daily bars are drawn as raw, expand or clip geometries. Study C asks whether those US-trained weights retain ranking skill on cryptocurrency spot when held fixed. Evaluation uses identical cryptocurrency out-of-sample keys for all arms, close-to-close returns and zero costs, matching the diagnostic path of Study B.

Expand and clip US weights are applied to raw cryptocurrency images. The raw arm is geometry-matched; expand and clip are cross-representation transfers and are labeled as such in the metrics schema.

---

## 2. Principal result

On the primary cell I20/R20, Rank IC is negative for raw, expand and clip, with approximate values −0.051, −0.041 and −0.051. AUC values lie below one half. The three arms share identical sample keys, so arm differences are not driven by unequal coverage.

Cryptocurrency-local retrain on the same cell yields Rank IC −0.0495. Frozen US transfer therefore does not remedy retrain failure. The primary-cell sign remains negative whether weights are learned on cryptocurrency images or imported frozen from equities.

The diagonal extension is likewise non-positive for all arms at I5/R5, I20/R20 and I60/R60. Failure is not confined to a single horizon pairing.

---

## 3. Relation to Study A

In equities, representation choice moves net Sharpe substantially: expand at long horizons and dollar clip across the diagonal. In frozen transfer to cryptocurrency, representation choice does not restore a positive Rank IC. Expand is only marginally less negative than raw and clip on I20/R20. The equity finding that bar geometry matters economically does **not** imply that those same frozen weights generalise to cryptocurrency ranking skill.

---

## 4. Joint reading with Study B

Studies B and C jointly bound asset-class transfer for Jiang-style image CNNs. Local retrain fails at the equity-style primary cell. Direct transfer of US raw, expand and clip weights also fails. The limitation is therefore not only that cryptocurrency-local optimisation is insufficient; equity-trained visual trend weights themselves do not rank cryptocurrency names productively out of sample under this protocol.

A coherent structural reading remains limited cross-sectional depth and short effective history on the cryptocurrency side, as developed in [INTERPRETATION-crypto.md](INTERPRETATION-crypto.md). Shared exchange, quote asset and market-wide shocks reduce residual idiosyncrasy that cross-sectional image features require. Importing US weights does not supply that missing residual structure.

---

## 5. Scope

The results do not evaluate dollar-volume US arms. They do not claim matched expand or clip cryptocurrency image geometry. They do not report delayed-VWAP net-of-cost implementation. They do not assert that no cryptocurrency signal exists under other models, features or horizons.

**Synthesis.** Frozen equity representation models and cryptocurrency-local retrain agree on primary-cell failure. Study C strengthens the conclusion that the transfer boundary is a property of the method–market pairing, not an artefact of optimising only on cryptocurrency samples.
