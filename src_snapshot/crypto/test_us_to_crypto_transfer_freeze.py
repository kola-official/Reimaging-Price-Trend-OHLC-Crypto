"""Freeze invariants for US→crypto direct transfer.

Exercises shipped crypto_reimaging.transfer_metrics and the published metrics
JSON. Does not hard-code expected Rank IC values.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from crypto_reimaging.transfer_metrics import (
    ARM_ALIASES,
    TRANSFER_MODE,
    assert_freeze_payload,
    spearman_ic,
)

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "transfer_us_arms_to_crypto_frozen.py"
METRICS = ROOT / "outputs" / "oos" / "us_to_crypto_direct_transfer_i20_r20.json"


class TransferFreezeTests(unittest.TestCase):
    def test_shipped_entry_point_exists(self) -> None:
        self.assertTrue(SCRIPT.is_file())
        text = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("direct_frozen", text)
        self.assertIn("us_normalization_refit_on_crypto", text)
        self.assertIn("requires_grad_(False)", text)

    def test_arm_aliases(self) -> None:
        self.assertEqual(ARM_ALIASES["raw"], "raw")
        self.assertEqual(ARM_ALIASES["expand"], "vwpq")
        self.assertEqual(ARM_ALIASES["clip"], "vwpq_clip")
        self.assertEqual(TRANSFER_MODE, "direct_frozen_us_weights")

    def test_spearman_ic_perfect_rank(self) -> None:
        ic = spearman_ic([0.1, 0.2, 0.3, 0.4, 0.5], [1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertGreater(ic, 0.99)

    def test_spearman_ic_inverse_rank(self) -> None:
        ic = spearman_ic([0.5, 0.4, 0.3, 0.2, 0.1], [1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertLess(ic, -0.99)

    def test_published_metrics_freeze_schema(self) -> None:
        self.assertTrue(METRICS.is_file(), f"missing {METRICS}")
        payload = json.loads(METRICS.read_text(encoding="utf-8"))
        errors = assert_freeze_payload(payload)
        self.assertEqual(errors, [], msg=str(errors))
        # All three arms share identical OOS row counts on primary cell.
        i20 = [c for c in payload["cells"] if c["cell"] == "i20_r20"]
        self.assertEqual(len(i20), 3)
        rows = {c["n_pred_rows"] for c in i20}
        self.assertEqual(len(rows), 1)
        self.assertGreater(next(iter(rows)), 1000)


if __name__ == "__main__":
    unittest.main()
