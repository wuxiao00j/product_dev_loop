from __future__ import annotations

from contract_checker import analyze_contract
from gate_checker import analyze_gate
from models import SkeletonResult
from utils import extract_section_lines


DEFAULT_CONTEXT_LINES = [
    "- 必读：`PROJECT_STATE.md`",
    "- 必读：`PRD.md`",
    "- 必读：最近一轮 `PROGRESS.md`",
    "- 必读：最近一轮 `IMPLEMENTATION_NOTES.md`",
    "- 按需补读：`ARCHITECTURE.md` / `CHANGE_PROPOSALS.md` / `TEST_RESULTS.md`",
]

DEFAULT_RETURN_LINES = [
    "1. 已完成",
    "2. 未完成",
    "3. 关键代码信息",
    "4. `stub / mock / 假数据 / 隐藏入口 / 未接线`",
    "5. 风险与需确认点",
    "6. 测试建议",
    "7. PRD 对照",
]

DEFAULT_TEST_LINES = [
    "- 请返回测试入口",
    "- 请返回操作步骤",
    "- 请返回测试数据",
    "- 请返回预期结果",
    "- 请返回失败判定",
]

SECTION_CONTRACT_MAP = {
    "task_type": ["task_type"],
    "project_info": ["project_round_stage_prd"],
    "required_context": [],
    "round_goal": ["round_goal", "round_main_closure", "why_not_split"],
    "round_boundary": ["out_of_scope", "tighter_out_of_scope"],
    "acceptance": ["acceptance"],
    "dependency_rules": ["fallback_blocker_rule", "dependency_fallback_blocker"],
    "test_requirement": ["test_requirement"],
    "structured_return": ["structured_return", "prd_alignment"],
    "pass_evidence": ["pass_evidence", "round_main_closure", "why_not_split", "fallback_blocker_rule"],
}

SECTION_TITLES = {
    "task_type": "任务类型",
    "project_info": "当前项目信息",
    "required_context": "执行前必读上下文",
    "round_goal": "本轮目标",
    "round_boundary": "本轮边界",
    "acceptance": "验收标准",
    "dependency_rules": "依赖与降级规则",
    "test_requirement": "测试要求",
    "structured_return": "完成后必须结构化回传",
    "pass_evidence": "PASS Evidence",
}

GAP_ACTIONS = {
    "project_round_stage_prd": "补齐项目名、轮次、阶段和 PRD 状态，再重新判断是否可进入 delegation。",
    "task_type": "补稳定任务类型，避免 build / fix / polish / unblock 混用。",
    "round_goal": "把目标压成一个单轮最小闭环，并补一句用户可见结果。",
    "out_of_scope": "补清本轮不做和保持不动，防止顺手扩做。",
    "tighter_out_of_scope": "已有边界但仍偏松，需要明确削掉并列主目标。",
    "acceptance": "把验收改成外部可判断的结果句子，而不是愿景描述。",
    "dependency_fallback_blocker": "补清关键依赖、降级方案和直接阻塞条件。",
    "fallback_blocker_rule": "补一句依赖失败时如何降级，哪些情况必须直接阻塞。",
    "structured_return": "补固定结构化回传字段，方便主 agent 收口。",
    "test_requirement": "补测试入口、步骤、数据、预期结果和失败判定。",
    "prd_alignment": "补 PRD 对照要求，说明对应条目、已满足项和未满足项。",
    "round_main_closure": "补一句 Round main closure，写清本轮唯一主闭环。",
    "why_not_split": "补一句 why-not-split，或把当前输入拆成多轮。",
    "pass_evidence": "补完整 PASS evidence，证明当前输入不是伪合格 prompt。",
}

CONTRACT_PRIORITIES = {
    "project_round_stage_prd": "critical",
    "task_type": "critical",
    "round_goal": "critical",
    "round_main_closure": "critical",
    "why_not_split": "critical",
    "fallback_blocker_rule": "critical",
    "dependency_fallback_blocker": "critical",
    "pass_evidence": "critical",
    "out_of_scope": "important",
    "tighter_out_of_scope": "important",
    "acceptance": "important",
    "structured_return": "important",
    "test_requirement": "important",
    "prd_alignment": "important",
}

CONTRACT_HINT_SPECS = {
    "project_round_stage_prd": {
        "text": "补齐项目名、轮次、阶段和 PRD 状态",
        "type": "lock_context",
    },
    "task_type": {
        "text": "补齐稳定任务类型，明确 build / fix / polish / unblock",
        "type": "lock_context",
    },
    "round_goal": {
        "text": "把本轮目标压成一个单轮主闭环，并补一句用户可见结果",
        "type": "tighten_scope",
    },
    "out_of_scope": {
        "text": "补齐本轮不做和保持不动，防止顺手扩做",
        "type": "add_constraint",
    },
    "tighter_out_of_scope": {
        "text": "把本轮边界收紧到一个主闭环，删掉并列主目标",
        "type": "tighten_scope",
    },
    "acceptance": {
        "text": "补一句围绕单轮主闭环的验收标准",
        "type": "add_acceptance",
    },
    "dependency_fallback_blocker": {
        "text": "补清关键依赖、降级方案和直接阻塞条件",
        "type": "add_fallback",
    },
    "fallback_blocker_rule": {
        "text": "补一句依赖失败时的 fallback / blocker 处理",
        "type": "add_fallback",
    },
    "structured_return": {
        "text": "补齐固定结构化回传字段",
        "type": "add_constraint",
    },
    "test_requirement": {
        "text": "补一句可执行测试方式和失败判定",
        "type": "add_test_requirement",
    },
    "prd_alignment": {
        "text": "补一句完成后按 PRD 条目逐项对照回传",
        "type": "add_alignment",
    },
    "round_main_closure": {
        "text": "补一句 Round main closure，写清本轮唯一主闭环",
        "type": "add_pass_evidence",
    },
    "why_not_split": {
        "text": "补一句 why-not-split，说明为什么本轮不拆轮",
        "type": "tighten_scope",
    },
    "pass_evidence": {
        "text": "补一句 PASS evidence，说明为什么当前可直接进入 Build Delegation",
        "type": "add_pass_evidence",
    },
}

SECTION_PRIORITY_WEIGHT = {
    "project_info": 0,
    "task_type": 1,
    "round_goal": 2,
    "round_boundary": 3,
    "dependency_rules": 4,
    "acceptance": 5,
    "test_requirement": 6,
    "structured_return": 7,
    "pass_evidence": 8,
    "required_context": 9,
}


def _section_or_placeholder(lines: list[str], placeholders: list[str]) -> list[str]:
    return lines if lines else placeholders


def _build_pass_evidence_lines(gate_result, contract_result, missing_items: list[str]) -> list[str]:
    if gate_result.gate_result == "PASS" and gate_result.pass_evidence_present:
        return [
            "- Prompt Gate：`PASS`",
            "- Round main closure：`已具备，但 agent 应再确认一句话主闭环表述`",
            "- Why not split：`已具备，但 agent 应再确认为什么其余子项只是必要接线`",
            "- Fallback / blocker rule：`已具备，但 agent 应确认降级边界和直接阻塞条件保持清晰`",
            "- Delegation contract：`satisfied`",
            "- 说明：`这是 skeleton / draft，不是最终放行文本`",
        ]

    lines = [
        "- Prompt Gate：`尚未 PASS`",
        f"- Delegation contract：`{'satisfied' if contract_result.contract_pass else 'not yet'}`",
        "- 说明：`当前仍是 skeleton / draft，不应直接派单`",
    ]
    if "round_main_closure" in missing_items or "pass_evidence" in missing_items:
        lines.append("- Round main closure：`待补，需用一句话写清本轮唯一主闭环`")
    if "why_not_split" in missing_items:
        lines.append("- Why not split：`待补，需说明为什么本轮不拆轮`")
    if "fallback_blocker_rule" in missing_items:
        lines.append("- Fallback / blocker rule：`待补，需写清降级边界和直接阻塞条件`")
    return lines


def _build_section(
    key: str,
    content: list[str],
    source_type: str,
    gate_result,
    contract_result,
    missing_items: list[str],
) -> dict:
    title = SECTION_TITLES[key]
    related_items = [item for item in SECTION_CONTRACT_MAP.get(key, []) if item in missing_items]
    placeholder = source_type == "placeholder" or all("待补" in line for line in content)

    if placeholder:
        status = "placeholder"
        reason = "当前 section 主要还是骨架占位，agent 需要补真实内容。"
    elif related_items:
        status = "weak"
        reason = f"当前 section 有内容，但仍受这些缺口影响：{', '.join(related_items)}。"
    elif key == "round_goal" and gate_result.gate_result == "REWRITE_REQUIRED":
        status = "weak"
        reason = "目标已有内容，但当前还没有稳定收成单轮最小闭环。"
    elif key == "pass_evidence" and gate_result.gate_result != "PASS":
        status = "weak"
        reason = "PASS evidence 仍未成立，当前不能直接进入 Build Delegation。"
    elif key == "dependency_rules" and not contract_result.fallback_blocker_present:
        status = "weak"
        reason = "依赖段落存在，但 fallback / blocker 规则仍然不够可执行。"
    else:
        status = "filled"
        reason = "当前 section 已有可用内容，可作为 agent 二次收口底稿。"

    repair_hints = _build_repair_hints(
        key,
        status,
        related_items,
        gate_result.rewrite_actions,
        gate_result.task_type_guess,
    )

    return {
        "title": title,
        "content": content,
        "status": status,
        "reason": reason,
        "source_type": source_type,
        "related_contract_items": related_items,
        "repair_hints": repair_hints,
    }


def _build_repair_hints(
    key: str,
    status: str,
    related_items: list[str],
    rewrite_actions: list[str],
    task_type: str,
) -> list[dict]:
    if status == "filled":
        return []

    hints: list[dict] = []

    def add_hint(text: str, priority: str, hint_type: str) -> None:
        if not any(existing["text"] == text for existing in hints):
            hints.append({"text": text, "priority": priority, "type": hint_type})

    for item in related_items:
        hint_spec = CONTRACT_HINT_SPECS.get(item)
        if hint_spec:
            add_hint(hint_spec["text"], CONTRACT_PRIORITIES.get(item, "important"), hint_spec["type"])

    if key == "round_goal" and "tighten_scope" in rewrite_actions:
        add_hint("把目标中的并列独立能力收回到一个最小主闭环", "critical", "tighten_scope")
    if key == "round_goal" and "split" in rewrite_actions:
        add_hint("先转成 split plan，再保留当前轮唯一目标", "critical", "tighten_scope")
    if key == "round_boundary" and "tighten_scope" in rewrite_actions:
        add_hint("补一句强边界，明确排除顺手扩做内容", "important", "add_constraint")
    if key == "dependency_rules" and "add_fallback" in rewrite_actions:
        add_hint("补一句依赖失败时如何降级，以及哪些情况必须直接阻塞", "critical", "add_fallback")
    if key == "pass_evidence" and "add_pass_evidence" in rewrite_actions:
        add_hint("补一句 why-not-split 或 round main closure，但不要直接假装已经 PASS", "critical", "add_pass_evidence")
    if key == "project_info" and status == "placeholder":
        add_hint("补齐最小项目信息后再继续后面的 skeleton 收口", "critical", "lock_context")

    if status == "placeholder" and not hints:
        add_hint("补到可判断、可执行，不要只保留占位", "important", "add_constraint")

    return _apply_task_type_hint_templates(key, hints[:2], task_type)


def _apply_task_type_hint_templates(key: str, hints: list[dict], task_type: str) -> list[dict]:
    if task_type not in {"build", "fix", "polish", "unblock"}:
        return hints

    overrides = {
        ("build", "round_goal", "tighten_scope"): "把本轮目标收成一个新增主闭环，并补一句用户可见结果",
        ("build", "acceptance", "add_acceptance"): "补一句围绕新增主闭环的验收标准",
        ("build", "test_requirement", "add_test_requirement"): "补一句验证新增主路径已走通的测试方式和失败判定",
        ("build", "pass_evidence", "add_pass_evidence"): "补一句 PASS evidence，说明新增主闭环为什么已接近可放行",
        ("fix", "round_goal", "tighten_scope"): "把本轮目标收成一个明确问题修复闭环，并写清修复结果",
        ("fix", "round_boundary", "add_constraint"): "补一句只修问题范围、不要顺手重构的边界",
        ("fix", "acceptance", "add_acceptance"): "补一句问题消失且无明显回归的验收标准",
        ("fix", "test_requirement", "add_test_requirement"): "补一句复现步骤、修复后验证和失败判定",
        ("polish", "round_boundary", "tighten_scope"): "把本轮边界收成局部优化范围，不改主流程和结构定义",
        ("polish", "round_boundary", "add_constraint"): "补一句只做局部优化、不改主流程的边界",
        ("polish", "acceptance", "add_acceptance"): "补一句优化可感知且不改变主闭环的验收标准",
        ("unblock", "round_goal", "tighten_scope"): "把本轮目标收成阻塞解除闭环，并写清解除后可继续推进的结果",
        ("unblock", "dependency_rules", "add_fallback"): "补一句阻塞解除失败时的 fallback / blocker 处理",
        ("unblock", "pass_evidence", "add_pass_evidence"): "补一句阻塞已解除到可继续推进的 PASS evidence",
    }

    adjusted: list[dict] = []
    for hint in hints:
        updated = dict(hint)
        override = overrides.get((task_type, key, hint["type"]))
        if override:
            updated["text"] = override
        if not any(existing["text"] == updated["text"] and existing["type"] == updated["type"] for existing in adjusted):
            adjusted.append(updated)
    return adjusted


def _build_expected_outcome(section_key: str, suggested_action: str, section: dict) -> str:
    related_items = set(section.get("related_contract_items", []))
    if section_key == "project_info":
        return "后续 section 的约束会更稳定。"
    if section_key == "task_type":
        return "后续目标、边界和验收会更容易按同一类型收口。"
    if section_key == "round_goal":
        return "边界、验收和拆轮判断会更容易对齐。"
    if section_key == "dependency_rules":
        return "依赖失败时仍会有清晰的降级或阻塞路径。"
    if section_key == "acceptance":
        return "这一轮是否完成会更容易外部判断。"
    if section_key == "test_requirement":
        return "后续验证路径会更可执行。"
    if section_key == "structured_return":
        return "主 agent 收口时会更容易对照结果与 PRD。"
    if section_key == "pass_evidence":
        return "继续往下修时会更容易判断何时接近可放行状态。"
    if "prd_alignment" in related_items:
        return "回传和 PRD 对照会更稳定。"
    return "这一节继续往下修时会更容易判断是否够用。"


def _build_stop_condition(section_key: str, section: dict) -> str:
    related_items = set(section.get("related_contract_items", []))
    if section_key == "project_info":
        return "出现明确项目名、轮次、阶段和 PRD 状态即可。"
    if section_key == "task_type":
        return "任务类型能稳定落到 build / fix / polish / unblock 之一即可。"
    if section_key == "round_goal":
        return "目标收敛成一个单轮主闭环，并包含用户可见结果即可。"
    if section_key == "dependency_rules":
        return "补出依赖失败时的 fallback / blocker 处理即可。"
    if section_key == "acceptance":
        return "补出围绕单轮主闭环的可判断验收标准即可。"
    if section_key == "test_requirement":
        return "补出可执行测试方式和失败判定即可。"
    if section_key == "structured_return":
        return "补出固定回传结构，并说明如何按 PRD 对照即可。"
    if section_key == "pass_evidence":
        return "补出 why-not-split、round main closure 或 fallback/blocker 关键证据即可。"
    if "out_of_scope" in related_items or "tighter_out_of_scope" in related_items:
        return "出现明确不做边界，并能挡住顺手扩做即可。"
    return "这一节从占位或偏弱变成可判断、可执行即可。"


def _build_next_check(section_key: str, section: dict, stop_condition: str, task_type: str) -> str:
    if section_key == "project_info":
        return "检查项目名、轮次、阶段和 PRD 状态是否都已明确出现。"
    if section_key == "task_type":
        return "检查任务类型是否已稳定且不再混用。"
    if section_key == "round_goal":
        if task_type == "fix":
            return "检查本轮目标是否明确原问题和修复后的结果。"
        if task_type == "unblock":
            return "检查本轮目标是否明确阻塞点和解除后的继续推进结果。"
        return "检查本轮目标是否只剩一个主闭环，且有用户可见结果。"
    if section_key == "dependency_rules":
        if task_type == "unblock":
            return "检查是否已经写出阻塞解除失败时的 fallback / blocker 路径。"
        return "检查是否已经写出依赖失败时的 fallback / blocker 路径。"
    if section_key == "acceptance":
        if task_type == "fix":
            return "检查验收是否说明问题消失且无明显回归。"
        if task_type == "polish":
            return "检查验收是否说明优化可感知且不改主流程。"
        return "检查验收是否围绕单轮主闭环，而不是多个能力并列。"
    if section_key == "test_requirement":
        if task_type == "fix":
            return "检查是否已有复现步骤、修复后验证和失败判定。"
        return "检查测试要求是否包含操作步骤、预期结果和失败判定。"
    if section_key == "structured_return":
        return "检查回传是否包含固定结构，并且有 PRD 对照。"
    if section_key == "pass_evidence":
        return "检查是否已经写出 why-not-split、round main closure 或 fallback/blocker 关键证据。"
    return f"检查这一节是否已达到：{stop_condition}"


def _build_check_signal(section_key: str, section: dict, task_type: str) -> str:
    if section_key == "project_info":
        return "已出现项目名 / 轮次 / 阶段 / PRD 状态。"
    if section_key == "task_type":
        return "已出现稳定任务类型，且不再混用。"
    if section_key == "round_goal":
        if task_type == "fix":
            return "目标段已写出原问题与修复结果。"
        if task_type == "unblock":
            return "目标段已写出阻塞点与解除后可继续推进结果。"
        return "目标段只剩一个主闭环，且带用户可见结果。"
    if section_key == "dependency_rules":
        if task_type == "unblock":
            return "已写出阻塞解除失败时的 fallback / blocker 处理。"
        return "已写出 fallback / blocker 处理。"
    if section_key == "acceptance":
        if task_type == "fix":
            return "验收段已写出问题消失且无明显回归。"
        if task_type == "polish":
            return "验收段已写出优化可感知且不改主流程。"
        return "验收段已围绕单轮主闭环。"
    if section_key == "test_requirement":
        if task_type == "fix":
            return "测试段已包含复现步骤 / 修复后验证 / 失败判定。"
        return "测试段已包含步骤 / 预期 / 失败判定。"
    if section_key == "structured_return":
        return "回传段已包含固定结构与 PRD 对照。"
    if section_key == "pass_evidence":
        return "已出现 why-not-split / round main closure / fallback-blocker 关键证据。"
    return "该段已出现可判断的过线信号。"


def _section_priority(section: dict) -> str:
    if not section["repair_hints"]:
        return "optional"
    priorities = [hint["priority"] for hint in section["repair_hints"]]
    if "critical" in priorities:
        return "critical"
    if "important" in priorities:
        return "important"
    return "optional"


def _build_first_fix_order(sections: dict[str, dict], gate_result) -> list[dict]:
    if gate_result.gate_result == "PASS":
        return []

    candidates: list[tuple[int, int, str, dict]] = []
    priority_rank = {"critical": 0, "important": 1, "optional": 2}

    for key, section in sections.items():
        if section["status"] not in {"weak", "placeholder"}:
            continue
        section_priority = _section_priority(section)
        suggested_action = section["repair_hints"][0]["text"] if section["repair_hints"] else "先补这一节的关键缺口。"
        reason = section["reason"]
        candidates.append(
            (
                priority_rank.get(section_priority, 2),
                SECTION_PRIORITY_WEIGHT.get(key, 99),
                key,
                {
                    "section_key": key,
                    "section": section["title"],
                    "priority": section_priority,
                    "reason": reason,
                    "suggested_action": suggested_action,
                    "expected_outcome": _build_expected_outcome(key, suggested_action, section),
                    "stop_condition": _build_stop_condition(key, section),
                    "next_check": _build_next_check(key, section, _build_stop_condition(key, section), gate_result.task_type_guess),
                    "check_signal": _build_check_signal(key, section, gate_result.task_type_guess),
                },
            )
        )

    candidates.sort(key=lambda item: (item[0], item[1]))
    return [item[3] for item in candidates[:5]]


def _build_recommended_next_step(
    gate_result,
    sections: dict[str, dict],
    first_fix_order: list[dict],
) -> str:
    if gate_result.gate_result == "CLARIFICATION_REQUIRED":
        return "clarify_first"
    if gate_result.gate_result == "PASS":
        return "stable"

    placeholder_sections = [
        key
        for key, section in sections.items()
        if section["status"] == "placeholder" and key in {"project_info", "round_goal", "round_boundary", "dependency_rules", "acceptance"}
    ]
    critical_fix_count = sum(1 for item in first_fix_order if item["priority"] == "critical")

    if gate_result.input_type == "raw_request":
        return "rewrite_more"
    if placeholder_sections:
        return "rewrite_more"
    if critical_fix_count >= 3:
        return "rewrite_more"
    return "re_gate"


def _build_gap_view(missing_items: list[str]) -> list[dict]:
    gap_view: list[dict] = []
    for contract_item in missing_items:
        affects = [SECTION_TITLES[key] for key, items in SECTION_CONTRACT_MAP.items() if contract_item in items]
        gap_view.append(
            {
                "contract_item": contract_item,
                "affects": affects,
                "action": GAP_ACTIONS.get(contract_item, "补足该 contract 缺口后再重新检查 skeleton。"),
            }
        )
    return gap_view


def _render_markdown(result: SkeletonResult) -> str:
    lines = [
        "# Round Prompt Skeleton",
        "",
        f"- status: `{result.status}`",
        f"- input_type: `{result.input_type}`",
        f"- gate_result: `{result.gate_result}`",
        f"- ready_for_delegation: `{str(result.ready_for_delegation).lower()}`",
    ]

    if result.deferred:
        lines.extend(
            [
                "- skeleton_generation: `deferred_until_clarification`",
                "- recommended_next_step: `clarify_first`",
                "",
                "## Clarification Block",
                "",
                f"- clarification_reason: {result.clarification_reason}",
                f"- minimal_clarification_question: {result.minimal_clarification_question}",
                f"- next_action_after_answer: {result.next_action_after_answer}",
            ]
        )
        return "\n".join(lines) + "\n"

    if result.notes:
        lines.extend(["", "## Notes", ""])
        lines.extend(f"- {note}" for note in result.notes)

    if result.recommended_next_step:
        lines.extend(["", f"Recommended next step: `{result.recommended_next_step}`"])

    if result.split_plan:
        lines.extend(["", "## Split Suggestion", ""])
        lines.extend(f"- {item}" for item in result.split_plan)

    if result.missing_items:
        lines.extend(["", "## Missing Strengthening Items", ""])
        lines.extend(f"- {item}" for item in result.missing_items)

    if result.gap_view:
        lines.extend(["", "## Contract-to-Skeleton Gap View", ""])
        for gap in result.gap_view:
            affects = ", ".join(gap["affects"]) if gap["affects"] else "未直接映射到具体 section"
            lines.append(f"- {gap['contract_item']} -> affects: [{affects}] -> action: {gap['action']}")

    if result.first_fix_order:
        lines.extend(["", "## First Fix Order", ""])
        for index, item in enumerate(result.first_fix_order, start=1):
            lines.append(f"{index}. {item['section']} [{item['priority']}]")
            lines.append(f"   - suggested_action: {item['suggested_action']}")
            lines.append(f"   - expected_outcome: {item['expected_outcome']}")
            lines.append(f"   - stop_condition: {item['stop_condition']}")
            lines.append(f"   - next_check: {item['next_check']}")
            lines.append(f"   - check_signal: {item['check_signal']}")
            lines.append(f"   - reason: {item['reason']}")

    for key in [
        "task_type",
        "project_info",
        "required_context",
        "round_goal",
        "round_boundary",
        "acceptance",
        "dependency_rules",
        "test_requirement",
        "structured_return",
        "pass_evidence",
    ]:
        section = result.sections.get(key)
        if not section:
            lines.extend(["", f"## {SECTION_TITLES[key]} [placeholder]", "", "- 待补"])
            continue
        lines.extend(["", f"## {section['title']} [{section['status']}]", ""])
        lines.append(f"- reason: {section['reason']}")
        lines.append(f"- source_type: {section['source_type']}")
        if section["related_contract_items"]:
            lines.append(f"- related_contract_items: {', '.join(section['related_contract_items'])}")
        if section["repair_hints"]:
            lines.append("- repair_hints:")
            for hint in section["repair_hints"]:
                lines.append(f"  - [{hint['priority']}][{hint['type']}] {hint['text']}")
        lines.extend(section["content"])

    return "\n".join(lines) + "\n"


def build_skeleton(text: str) -> SkeletonResult:
    gate_result = analyze_gate(text)
    contract_result = analyze_contract(text)

    if gate_result.gate_result == "CLARIFICATION_REQUIRED":
        result = SkeletonResult(
            input_type=gate_result.input_type,
            gate_result=gate_result.gate_result,
            task_type_guess=gate_result.task_type_guess,
            status="deferred_until_clarification",
            ready_for_delegation=False,
            deferred=True,
            project=gate_result.project,
            round_id=gate_result.round_id,
            stage=gate_result.stage,
            prd_status=gate_result.prd_status,
            minimal_clarification_question=gate_result.minimal_clarification_question,
            clarification_reason=gate_result.clarification_reason,
            next_action_after_answer=gate_result.next_action_after_answer,
            notes=["需先澄清后再生成 skeleton，不应强行铺满 round prompt 段落。"],
            sections={},
            gap_view=[],
            first_fix_order=[],
            recommended_next_step="clarify_first",
        )
        result.skeleton_markdown = _render_markdown(result)
        return result

    goal_source = extract_section_lines(text, "【本轮目标】")
    goal_lines = _section_or_placeholder(
        goal_source,
        [
            "- 本轮只解决：`待 agent 收敛成一个单轮最小闭环`",
            "- 这轮完成后，用户能直接看到的结果：`待补`",
            "- 本轮目标来源：`PRD 条目 / 测试反馈 / 上轮未完成项 / 外部阻塞`",
        ],
    )
    boundary_source = extract_section_lines(text, "【本轮边界】")
    boundary_lines = _section_or_placeholder(
        boundary_source,
        [
            "- 必做：`待补`",
            "- 不做：`待补，需写清禁止扩散内容`",
            "- 保持不动：`待补`",
            "- 重点文件 / 模块：`待补`",
        ],
    )
    acceptance_source = extract_section_lines(text, "【验收标准】")
    acceptance_lines = _section_or_placeholder(
        acceptance_source,
        [
            "- 验收项 1：`待补`",
            "- 验收项 2：`待补`",
            "- 验收项 3：`待补`",
        ],
    )
    dependency_source = extract_section_lines(text, "【依赖与降级规则】")
    dependency_lines = _section_or_placeholder(
        dependency_source,
        [
            "- 关键依赖：`待补`",
            "- 依赖满足时：`待补`",
            "- 依赖不满足时允许的降级方案：`待补`",
            "- 哪些情况应直接标记阻塞，不继续扩做：`待补`",
        ],
    )
    test_source = extract_section_lines(text, "【测试要求】")
    test_lines = _section_or_placeholder(test_source, DEFAULT_TEST_LINES)
    return_source = extract_section_lines(text, "【完成后必须结构化回传】")
    return_lines = _section_or_placeholder(return_source, DEFAULT_RETURN_LINES)
    project_info_lines = [
        f"- 项目名：`{gate_result.project or '待补'}`",
        f"- 当前轮次：`{gate_result.round_id or '待补'}`",
        f"- 当前阶段：`{gate_result.stage or 'Build Delegation'}`",
        f"- 当前 PRD 状态：`{gate_result.prd_status or '待补'}`",
        f"- 当前 Gate 状态：`{gate_result.gate_result}`",
    ]
    task_type_lines = [
        f"- 本轮类型：`{gate_result.task_type_guess}`",
        "- 选择原因：`待 agent 根据 PRD 与反馈再确认`",
    ]

    notes = ["这是 skeleton / draft，只用于 agent 二次收口，不是最终可直接派单文本。"]
    if gate_result.gate_result != "PASS":
        notes.append("当前输入仍未通过 Gate，不能直接进入 Build Delegation。")
    if gate_result.input_type == "pseudo_qualified_prompt":
        notes.append("当前输入属于 pseudo-qualified prompt：形式较完整，但闭环仍未收口。")
    if contract_result.missing_fields:
        notes.append(f"contract missing fields: {', '.join(contract_result.missing_fields)}")
    if contract_result.weak_fields:
        notes.append(f"weak fields: {', '.join(contract_result.weak_fields)}")

    pass_evidence_lines = _build_pass_evidence_lines(gate_result, contract_result, gate_result.missing_strengthening_items)

    sections = {
        "task_type": _build_section(
            "task_type",
            task_type_lines,
            "source" if gate_result.task_type_guess != "无法稳定判断" else "inferred",
            gate_result,
            contract_result,
            gate_result.missing_strengthening_items,
        ),
        "project_info": _build_section(
            "project_info",
            project_info_lines,
            "source" if gate_result.project and gate_result.round_id and gate_result.stage and gate_result.prd_status else "placeholder",
            gate_result,
            contract_result,
            gate_result.missing_strengthening_items,
        ),
        "required_context": _build_section(
            "required_context",
            DEFAULT_CONTEXT_LINES,
            "inferred",
            gate_result,
            contract_result,
            gate_result.missing_strengthening_items,
        ),
        "round_goal": _build_section(
            "round_goal",
            goal_lines,
            "source" if goal_source else "placeholder",
            gate_result,
            contract_result,
            gate_result.missing_strengthening_items,
        ),
        "round_boundary": _build_section(
            "round_boundary",
            boundary_lines,
            "source" if boundary_source else "placeholder",
            gate_result,
            contract_result,
            gate_result.missing_strengthening_items,
        ),
        "acceptance": _build_section(
            "acceptance",
            acceptance_lines,
            "source" if acceptance_source else "placeholder",
            gate_result,
            contract_result,
            gate_result.missing_strengthening_items,
        ),
        "dependency_rules": _build_section(
            "dependency_rules",
            dependency_lines,
            "source" if dependency_source else "placeholder",
            gate_result,
            contract_result,
            gate_result.missing_strengthening_items,
        ),
        "test_requirement": _build_section(
            "test_requirement",
            test_lines,
            "source" if test_source else "inferred",
            gate_result,
            contract_result,
            gate_result.missing_strengthening_items,
        ),
        "structured_return": _build_section(
            "structured_return",
            return_lines,
            "source" if return_source else "inferred",
            gate_result,
            contract_result,
            gate_result.missing_strengthening_items,
        ),
        "pass_evidence": _build_section(
            "pass_evidence",
            pass_evidence_lines,
            "source" if gate_result.gate_result == "PASS" and gate_result.pass_evidence_present else "inferred",
            gate_result,
            contract_result,
            gate_result.missing_strengthening_items,
        ),
    }

    gap_view = _build_gap_view(gate_result.missing_strengthening_items)
    first_fix_order = _build_first_fix_order(sections, gate_result)
    recommended_next_step = _build_recommended_next_step(gate_result, sections, first_fix_order)

    result = SkeletonResult(
        input_type=gate_result.input_type,
        gate_result=gate_result.gate_result,
        task_type_guess=gate_result.task_type_guess,
        status="draft_not_ready_for_delegation" if gate_result.gate_result != "PASS" else "skeleton_ready_for_agent_refinement",
        ready_for_delegation=False,
        deferred=False,
        project=gate_result.project,
        round_id=gate_result.round_id,
        stage=gate_result.stage,
        prd_status=gate_result.prd_status,
        missing_items=gate_result.missing_strengthening_items,
        rewrite_actions=gate_result.rewrite_actions,
        split_plan=gate_result.split_plan,
        notes=notes,
        sections=sections,
        gap_view=gap_view,
        first_fix_order=first_fix_order,
        recommended_next_step=recommended_next_step,
    )
    result.skeleton_markdown = _render_markdown(result)
    return result
