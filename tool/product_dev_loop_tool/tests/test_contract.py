from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from contract_checker import analyze_contract
from utils import read_text


def load_snapshot(name: str) -> dict:
    return json.loads((ROOT / "tests" / "snapshots" / name).read_text(encoding="utf-8"))


class ContractSnapshotTests(unittest.TestCase):
    def test_sample_pass_prompt_contract_snapshot(self) -> None:
        result = analyze_contract(read_text(str(ROOT / "examples" / "sample_pass_prompt.txt"))).to_dict()
        expected = load_snapshot("contract_pass_prompt.json")
        subset = {key: result[key] for key in expected}
        self.assertEqual(subset, expected)
        self.assertTrue(result["contract_pass"])


if __name__ == "__main__":
    unittest.main()
