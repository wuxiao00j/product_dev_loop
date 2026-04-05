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


class ClarificationTests(unittest.TestCase):
    def test_ambiguous_input_requires_single_question(self) -> None:
        result = analyze_gate(read_text(str(ROOT / "examples" / "sample_ambiguous_input.txt"))).to_dict()
        expected = load_snapshot("gate_ambiguous_input.json")
        subset = {key: result[key] for key in expected}
        self.assertEqual(subset, expected)
        question = result["minimal_clarification_question"]
        punctuation_count = question.count("?") + question.count("？")
        self.assertEqual(punctuation_count, 1)
        self.assertEqual(result["gate_result"], "CLARIFICATION_REQUIRED")
        self.assertEqual(result["rewrite_actions"], [])


if __name__ == "__main__":
    unittest.main()
