#!/usr/bin/env python3
"""Zero-shot transfer: frozen US equity representation CNNs → crypto OOS images.

Loads US purged_primary checkpoints for raw / vwpq (expand) / vwpq_clip without
any optimizer step. Uses each seed's US train-only mean/std from the checkpoint;
does not re-fit normalization on crypto. Crypto images are the existing author-
exact raw OHLC tensors unless a matched expand/clip crypto dataset is supplied.

This is direct frozen transfer, not retrain or fine-tune.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    # Engineering-workspace layout (package name crypto_reimaging)
    from crypto_reimaging.transfer_metrics import (  # noqa: E402
        ARM_ALIASES,
        ARM_DISPLAY,
        TRANSFER_MODE,
        summarise_rank_ic_by_date,
    )
except ImportError:  # pragma: no cover - published snapshot layout
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from transfer_metrics import (  # noqa: E402
        ARM_ALIASES,
        ARM_DISPLAY,
        TRANSFER_MODE,
        summarise_rank_ic_by_date,
    )


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_crypto_oos(dataset_dir: Path) -> tuple[dict[str, Any], np.memmap, list[dict[str, str]], int, int]:
    man = json.loads((dataset_dir / "dataset_manifest.json").read_text(encoding="utf-8"))
    total = int(man["samples"])
    _, rows, cols = (int(x) for x in man["shape"])
    mm = np.memmap(dataset_dir / "images.uint8.bin", dtype=np.uint8, mode="r", shape=(total, rows, cols))
    with (dataset_dir / "metadata.csv").open("r", newline="", encoding="utf-8") as handle:
        meta = list(csv.DictReader(handle))
    if len(meta) != total:
        raise RuntimeError(f"metadata rows {len(meta)} != samples {total}")
    return man, mm, meta, rows, cols


def score_arm(
    *,
    us_root: Path,
    shared_root: Path,
    arm_dir_name: str,
    cell: str,
    crypto_ds: Path,
    device: torch.device,
    batch: int,
    seeds: list[int],
    min_names: int = 50,
) -> dict[str, Any]:
    sys.path.insert(0, str(shared_root))
    from src.hfdata.models import build_model  # type: ignore

    man, mm, meta, rows, cols = load_crypto_oos(crypto_ds)
    image_window = int(cell.split("_")[0][1:])
    horizon = int(cell.split("_")[1][1:])
    cell_dir = us_root / arm_dir_name / cell
    if not cell_dir.is_dir():
        raise FileNotFoundError(f"missing US cell dir: {cell_dir}")

    seed_probs: list[np.ndarray] = []
    seed_records: list[dict[str, Any]] = []
    for seed in seeds:
        seed_dir = cell_dir / f"seed{seed}"
        ck_path = seed_dir / "best_checkpoint.pt"
        if not ck_path.is_file():
            raise FileNotFoundError(ck_path)
        try:
            # Prefer the safe loader; our checkpoints contain a state dict and
            # scalar stats only, which weights_only=True accepts.
            ckpt = torch.load(ck_path, map_location="cpu", weights_only=True)
        except Exception:
            print(f"WARNING: weights_only load failed for {ck_path}; falling back", flush=True)
            ckpt = torch.load(ck_path, map_location="cpu", weights_only=False)
        if not isinstance(ckpt, dict) or "model" not in ckpt:
            raise RuntimeError(f"unexpected checkpoint schema: {ck_path}")
        # Freeze rule: US train-only stats from checkpoint, never crypto OOS/IS.
        mean = float(ckpt["mean"])
        std = float(ckpt["std"])
        if std <= 0:
            raise RuntimeError(f"invalid std in {ck_path}")
        model = build_model(image_window)
        model.load_state_dict(ckpt["model"], strict=True)
        model.to(device)
        model.eval()
        for parameter in model.parameters():
            parameter.requires_grad_(False)

        probs = np.empty(len(meta), dtype=np.float64)
        with torch.inference_mode():
            for start in range(0, len(meta), batch):
                stop = min(start + batch, len(meta))
                chunk = np.asarray(mm[start:stop], dtype=np.float32) / 255.0
                chunk = (chunk - mean) / std
                tensor = torch.from_numpy(chunk[:, None, :, :]).to(device)
                logits = model(tensor)
                probs[start:stop] = torch.softmax(logits, dim=1)[:, 1].detach().cpu().numpy()
        seed_probs.append(probs)
        seed_records.append(
            {
                "seed": seed,
                "checkpoint": str(ck_path),
                "checkpoint_sha256": sha256_file(ck_path),
                "us_normalization_mean": mean,
                "us_normalization_std": std,
                "us_normalization_refit_on_crypto": False,
                "gradient_updates": 0,
                "optimizer_steps": 0,
                "model_train_mode": False,
                "parameters_requires_grad": False,
            }
        )
        del model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    ens = np.mean(np.stack(seed_probs, axis=0), axis=0)
    rets = [float(row["future_return"]) for row in meta]
    labels = np.asarray([int(row["label"]) for row in meta], dtype=np.int64)
    dates = [row["chart_date"] for row in meta]
    summary = summarise_rank_ic_by_date(ens.tolist(), rets, dates, horizon, min_names=min_names)

    try:
        from sklearn.metrics import roc_auc_score

        auc = float(roc_auc_score(labels, ens))
    except Exception:
        auc = float("nan")

    crypto_image_geometry = "raw_author_exact_ohlc"
    representation_match = arm_dir_name == "raw"

    return {
        "arm": ARM_DISPLAY[arm_dir_name],
        "arm_dir": arm_dir_name,
        "cell": cell,
        "image_window": image_window,
        "horizon": horizon,
        "transfer_mode": TRANSFER_MODE,
        "retrain": False,
        "fine_tune": False,
        "gradient_updates": 0,
        "us_weights_updated_on_crypto": False,
        "us_normalization_refit_on_crypto": False,
        "crypto_image_geometry": crypto_image_geometry,
        "us_training_representation": ARM_DISPLAY[arm_dir_name],
        "representation_geometry_matched": representation_match,
        "representation_note": (
            "matched_raw_on_raw"
            if representation_match
            else "cross_representation_us_expand_or_clip_weights_on_crypto_raw_images"
        ),
        "n_pred_rows": int(len(meta)),
        "min_names_per_formation_date": int(min_names),
        "n_ic_dates": int(summary["n_ic_dates"]),
        "n_ic_dates_skipped_nan": int(summary.get("n_ic_dates_skipped_nan", 0)),
        "rank_ic_mean": float(summary["rank_ic_mean"]),
        "rank_ic_std": float(summary["rank_ic_std"]),
        "icir": float(summary["icir"]),
        "auc": auc,
        "ls_mean": float(summary["ls_mean"]),
        "ls_std": float(summary["ls_std"]),
        "ls_sharpe_ann_proxy": float(summary["ls_sharpe_ann_proxy"]),
        "return_definition": "close_to_close_future_return_from_metadata",
        "cost_bps_applied": 0,
        "formation_step_days": horizon,
        "crypto_dataset_dir": str(crypto_ds),
        "crypto_dataset_manifest_sha256": sha256_file(crypto_ds / "dataset_manifest.json"),
        "crypto_images_sha256": sha256_file(crypto_ds / "images.uint8.bin"),
        "us_cell_dir": str(cell_dir),
        "seeds": seed_records,
        "device": str(device),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--us-root",
        type=Path,
        default=Path("/share/home/user/snliu/price_trends_workspace/outputs/hfdata/purged_primary"),
    )
    parser.add_argument(
        "--shared-root",
        type=Path,
        default=Path("/share/home/user/snliu/price_trends_workspace"),
    )
    parser.add_argument(
        "--crypto-root",
        type=Path,
        default=Path("/share/home/user/snliu/crypto_reimaging_workspace"),
    )
    parser.add_argument("--cells", nargs="+", default=["i20_r20"])
    parser.add_argument("--arms", nargs="+", default=["raw", "expand", "clip"])
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2, 3, 4])
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--batch-size", type=int, default=512)
    parser.add_argument(
        "--min-names",
        type=int,
        default=50,
        help=(
            "minimum cross-section size per formation date for Rank IC / decile "
            "sorts; protocol value is 50 (configs/crypto_daily_reimaging_v1.yaml "
            "minimum_names_for_deciles). NOTE: the 2026-07-24 published run used "
            "the previous library default of 10; the effective value is recorded "
            "in the output payload as min_names_per_formation_date."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/oos/us_to_crypto_direct_transfer_i20_r20.json"),
    )
    args = parser.parse_args()

    device = torch.device(args.device if torch.cuda.is_available() or not str(args.device).startswith("cuda") else "cpu")
    if str(args.device).startswith("cuda") and device.type != "cuda":
        print("WARNING: CUDA requested but unavailable; using CPU", flush=True)

    results: list[dict[str, Any]] = []
    for cell in args.cells:
        for arm_alias in args.arms:
            arm_dir = ARM_ALIASES[arm_alias]
            crypto_ds = args.crypto_root / "data" / "crypto" / f"{cell}_oos"
            print(f"=== transfer arm={arm_dir} cell={cell} ===", flush=True)
            rec = score_arm(
                us_root=args.us_root,
                shared_root=args.shared_root,
                arm_dir_name=arm_dir,
                cell=cell,
                crypto_ds=crypto_ds,
                device=device,
                batch=args.batch_size,
                seeds=list(args.seeds),
                min_names=int(args.min_names),
            )
            results.append(rec)
            print(
                json.dumps(
                    {
                        "arm": rec["arm"],
                        "cell": rec["cell"],
                        "n_pred_rows": rec["n_pred_rows"],
                        "rank_ic_mean": rec["rank_ic_mean"],
                        "icir": rec["icir"],
                        "auc": rec["auc"],
                        "transfer_mode": rec["transfer_mode"],
                        "retrain": rec["retrain"],
                    },
                    indent=2,
                ),
                flush=True,
            )

    payload = {
        "schema_version": 1,
        "status": "us_to_crypto_direct_frozen_transfer_complete",
        "experiment": "Study_C_zero_shot_us_representation_arms_to_crypto",
        "transfer_mode": TRANSFER_MODE,
        "retrain": False,
        "fine_tune": False,
        "us_weights_updated_on_crypto": False,
        "us_normalization_refit_on_crypto": False,
        "device": str(device),
        "gpu": torch.cuda.get_device_name(0) if device.type == "cuda" else None,
        "us_checkpoint_root": str(args.us_root),
        "crypto_workspace": str(args.crypto_root),
        "shared_model_root": str(args.shared_root),
        "cells": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("WROTE", args.output, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
