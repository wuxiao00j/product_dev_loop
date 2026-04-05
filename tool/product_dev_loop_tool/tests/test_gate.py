from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from gate_checker import analyze_gate
from utils import read_text


def load_snapshot(name: str) -> dict:
    return json.loads((ROOT / "tests" / "snapshots" / name).read_text(encoding="utf-8"))


class GateSnapshotTests(unittest.TestCase):
    def test_sample_raw_request_snapshot(self) -> None:
        result = analyze_gate(read_text(str(ROOT / "examples" / "sample_raw_request.txt"))).to_dict()
        expected = load_snapshot("gate_raw_request.json")
        subset = {key: result[key] for key in expected}
        self.assertEqual(subset, expected)

    def test_sample_pseudo_prompt_snapshot(self) -> None:
        result = analyze_gate(read_text(str(ROOT / "examples" / "sample_pseudo_prompt.txt"))).to_dict()
        expected = load_snapshot("gate_pseudo_prompt.json")
        subset = {key: result[key] for key in expected}
        self.assertEqual(subset, expected)
        self.assertIn("pseudo_qualified_prompt", result["input_type"])
        self.assertTrue(
            "split" in result["rewrite_actions"] or "add_pass_evidence" in result["rewrite_actions"]
        )


if __name__ == "__main__":
    unittest.main()
