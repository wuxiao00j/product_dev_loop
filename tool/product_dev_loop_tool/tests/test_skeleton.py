from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from skeleton_builder import build_skeleton
from utils import read_text


def load_snapshot(name: str) -> dict:
    return json.loads((ROOT / "tests" / "snapshots" / name).read_text(encoding="utf-8"))


class SkeletonTests(unittest.TestCase):
    def test_pseudo_prompt_skeleton_is_draft(self) -> None:
        result = build_skeleton(read_text(str(ROOT / "examples" / "sample_pseudo_prompt.txt"))).to_dict()
        expected = load_snapshot("skeleton_pseudo_prompt.json")
        for key in [
            "input_type",
            "gate_result",
            "status",
            "ready_for_delegation",
            "deferred",
            "missing_items",
            "rewrite_actions",
            "recommended_next_step",
        ]:
            self.assertEqual(result[key], expected[key])
        for section_key, section_expected in expected["sections"].items():
            self.assertEqual(result["sections"][section_key]["status"], section_expected["status"])
        self.assertIn("draft", result["status"])
        self.assertIn("why_not_split", result["missing_items"])
        self.assertEqual(result["sections"]["round_goal"]["status"], "weak")
        self.assertTrue(result["sections"]["round_goal"]["repair_hints"])
        self.assertEqual(result["sections"]["round_goal"]["repair_hints"][0]["priority"], "critical")
        self.assertEqual(result["sections"]["round_goal"]["repair_hints"][0]["type"], "add_pass_evidence")
        self.assertTrue(result["gap_view"])
        self.assertTrue(result["first_fix_order"])
        self.assertIn(result["recommended_next_step"], {"rewrite_more", "re_gate"})
        self.assertIn("expected_outcome", result["first_fix_order"][0])
        self.assertIn("stop_condition", result["first_fix_order"][0])
        self.assertIn("next_check", result["first_fix_order"][0])
        self.assertIn("check_signal", result["first_fix_order"][0])
        self.assertNotEqual(result["first_fix_order"][0]["next_check"], result["first_fix_order"][0]["check_signal"])
        contract_items = {gap["contract_item"] for gap in result["gap_view"]}
        self.assertTrue("why_not_split" in contract_items or "fallback_blocker_rule" in contract_items)
        self.assertIn("## 本轮目标 [weak]", result["skeleton_markdown"])
        self.assertIn("- repair_hints:", result["skeleton_markdown"])
        self.assertIn("[critical]", result["skeleton_markdown"])
        self.assertIn("[add_pass_evidence]", result["skeleton_markdown"])
        self.assertIn("## First Fix Order", result["skeleton_markdown"])
        self.assertIn("stop_condition:", result["skeleton_markdown"])
        self.assertIn("next_check:", result["skeleton_markdown"])
        self.assertIn("check_signal:", result["skeleton_markdown"])

    def test_pass_prompt_skeleton_contains_core_sections(self) -> None:
        result = build_skeleton(read_text(str(ROOT / "examples" / "sample_pass_prompt.txt"))).to_dict()
        expected = load_snapshot("skeleton_pass_prompt.json")
        for key in ["input_type", "gate_result", "status", "ready_for_delegation", "deferred", "gap_view", "first_fix_order"]:
            self.assertEqual(result[key], expected[key])
        self.assertEqual(result["recommended_next_step"], "stable")
        for section_key, section_expected in expected["sections"].items():
            self.assertEqual(result["sections"][section_key]["status"], section_expected["status"])
        markdown = result["skeleton_markdown"]
        for title in [
            "## 任务类型 [filled]",
            "## 当前项目信息 [filled]",
            "## 执行前必读上下文 [filled]",
            "## 本轮目标 [filled]",
            "## 本轮边界 [filled]",
            "## 验收标准 [filled]",
            "## 测试要求 [filled]",
            "## 完成后必须结构化回传 [filled]",
            "## PASS Evidence [filled]",
        ]:
            self.assertIn(title, markdown)
        filled_count = sum(1 for section in result["sections"].values() if section["status"] == "filled")
        self.assertGreaterEqual(filled_count, 8)
        hint_count = sum(len(section["repair_hints"]) for section in result["sections"].values())
        self.assertLessEqual(hint_count, 1)
        self.assertNotIn("## First Fix Order", markdown)

    def test_ambiguous_input_skeleton_is_deferred(self) -> None:
        result = build_skeleton(read_text(str(ROOT / "examples" / "sample_ambiguous_input.txt"))).to_dict()
        expected = load_snapshot("skeleton_ambiguous_input.json")
        subset = {key: result[key] for key in expected}
        self.assertEqual(subset, expected)
        self.assertIn("minimal_clarification_question", result)
        self.assertNotIn("## 本轮目标", result["skeleton_markdown"])
        self.assertEqual(result["gap_view"], [])
        self.assertEqual(result["first_fix_order"], [])
        self.assertEqual(result["recommended_next_step"], "clarify_first")

    def test_raw_request_skeleton_has_placeholders_and_hints(self) -> None:
        result = build_skeleton(read_text(str(ROOT / "examples" / "sample_raw_request.txt"))).to_dict()
        expected = load_snapshot("skeleton_raw_request.json")
        for key in ["input_type", "gate_result", "status", "ready_for_delegation", "deferred", "rewrite_actions", "recommended_next_step"]:
            self.assertEqual(result[key], expected[key])
        self.assertEqual(result["sections"]["project_info"]["status"], "placeholder")
        self.assertEqual(result["sections"]["round_goal"]["status"], "placeholder")
        self.assertTrue(result["sections"]["round_goal"]["repair_hints"])
        self.assertTrue(result["sections"]["project_info"]["repair_hints"])
        self.assertEqual(result["sections"]["project_info"]["repair_hints"][0]["priority"], "critical")
        self.assertEqual(result["sections"]["project_info"]["repair_hints"][0]["type"], "lock_context")
        self.assertTrue(result["first_fix_order"])
        self.assertEqual(result["first_fix_order"][0]["section"], "当前项目信息")
        self.assertIn("expected_outcome", result["first_fix_order"][0])
        self.assertIn("stop_condition", result["first_fix_order"][0])
        self.assertIn("next_check", result["first_fix_order"][0])
        self.assertIn("check_signal", result["first_fix_order"][0])
        self.assertNotEqual(result["first_fix_order"][0]["next_check"], result["first_fix_order"][0]["check_signal"])
        self.assertEqual(result["recommended_next_step"], "rewrite_more")
        self.assertIn("## 当前项目信息 [placeholder]", result["skeleton_markdown"])
        self.assertIn("## 本轮目标 [placeholder]", result["skeleton_markdown"])
        self.assertIn("## First Fix Order", result["skeleton_markdown"])
        self.assertIn("[critical]", result["skeleton_markdown"])
        self.assertIn("[lock_context]", result["skeleton_markdown"])
        self.assertIn("stop_condition:", result["skeleton_markdown"])
        self.assertIn("next_check:", result["skeleton_markdown"])
        self.assertIn("check_signal:", result["skeleton_markdown"])
        self.assertIn("Recommended next step:", result["skeleton_markdown"])

    def test_task_type_aware_hint_templates_vary_for_fix_and_unblock(self) -> None:
        fix_text = """
【任务类型】
- 本轮类型：`fix`

这是一个修复导出按钮失败的原始需求块。
"""
        unblock_text = """
【任务类型】
- 本轮类型：`unblock`

这是一个解除接口权限阻塞的原始需求块。
"""
        fix_result = build_skeleton(fix_text).to_dict()
        unblock_result = build_skeleton(unblock_text).to_dict()

        fix_goal_hint = fix_result["sections"]["round_goal"]["repair_hints"][0]["text"]
        fix_test_hint = fix_result["sections"]["test_requirement"]["repair_hints"][0]["text"]
        unblock_goal_hint = unblock_result["sections"]["round_goal"]["repair_hints"][0]["text"]
        unblock_dependency_hint = unblock_result["sections"]["dependency_rules"]["repair_hints"][0]["text"]

        self.assertIn("修复", fix_goal_hint)
        self.assertIn("复现步骤", fix_test_hint)
        self.assertIn("阻塞解除", unblock_goal_hint)
        self.assertIn("阻塞解除失败", unblock_dependency_hint)


if __name__ == "__main__":
    unittest.main()
