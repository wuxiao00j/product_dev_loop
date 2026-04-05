from __future__ import annotations

from contract_checker import analyze_contract
from models import GateResult
from rules.gate_rules import AMBIGUOUS_PATTERNS, PASS_EVIDENCE_PATTERNS
from utils import compact_text, contains_any, extract_focus_text, extract_round, extract_value


def pass_evidence_present(text: str) -> bool:
    lowered = text.lower()
    return all(any(pattern.lower() in lowered for pattern in patterns) for patterns in PASS_EVIDENCE_PATTERNS.values())


def task_type_guess(text: str) -> str:
    explicit = extract_value(text, ["本轮类型", "任务类型"])
    if explicit in {"build", "fix", "polish", "unblock"}:
        return explicit
    return "无法稳定判断"


def detect_theme_hits(text: str) -> list[str]:
    lowered = extract_focus_text(text).lower()
    theme_map = {
        "generation": ["续写", "生成", "写作"],
        "style": ["风格", "语气"],
        "export": ["导出", "epub"],
        "cli": ["cli", "命令行", "命令"],
        "api": ["api 接口", "`api`", "后端接口", "endpoint", "接口"],
        "web_ui": ["web ui", "webui", "前端页面", "网页界面", "页面交互", "web 页面"],
        "dependency": ["第三方接入", "sdk", "权限系统", "接口契约", "外部服务接入"],
        "polish": ["优化", "体验", "文案", "交互"],
    }
    hits = []
    for theme, patterns in theme_map.items():
        if any(pattern.lower() in lowered for pattern in patterns):
            hits.append(theme)
    return sorted(set(hits))


def ambiguous_input(text: str, project: str | None, round_id: str | None, stage: str | None, prd_status: str | None) -> bool:
    lowered = text.lower()
    if contains_any(text, AMBIGUOUS_PATTERNS):
        return True
    if sum(1 for value in [project, round_id, stage, prd_status] if value) in {1, 2, 3} and any(
        token in lowered for token in ["继续", "接手", "上一轮", "当前轮", "这个项目"]
    ):
        return True
    return False


def build_split_recommendation(theme_hits: list[str], contract_result) -> str:
    if contract_result.multi_closure_risk == "high":
        if any(theme in theme_hits for theme in ["cli", "api", "web_ui"]):
            return "建议拆轮：先保留一个最小主路径闭环，再把 CLI / API / Web UI 分成后续轮次。"
        return "建议拆轮：先保留最小可验收主闭环，把并列主题拆到后续轮次。"
    if contract_result.multi_closure_risk == "medium":
        return "可考虑拆轮；至少要补 why-not-split，并解释其余子项为什么只是必要接线。"
    return "当前输入更接近单轮闭环，不需要默认拆轮。"


def determine_clarification(
    text: str,
    project: str | None,
    round_id: str | None,
    stage: str | None,
    prd_status: str | None,
) -> tuple[str, str, str]:
    lowered = text.lower()

    if not project:
        return (
            "你这次要继续的是哪个项目？",
            "项目未锁定，当前无法稳定判断这是哪个项目的 Gate 输入。",
            "拿到项目名后，先用这条最短回复重新过 Gate，再判断是 rewrite 还是继续 clarify。",
        )
    if not round_id:
        return (
            "这次对应的是哪个 round？",
            "当前轮次未锁定，无法安全判断本轮边界和是否需要拆轮。",
            "拿到 round 后，先重新过 Gate，再判断是否进入 rewrite。",
        )
    if not stage:
        return (
            "当前这轮处于哪个阶段？",
            "阶段未锁定，当前无法判断这段输入是否已经具备进入 Build Delegation 的资格。",
            "拿到阶段后，先重新过 Gate，再决定下一步动作。",
        )
    if not prd_status:
        return (
            "当前 PRD 状态是 draft 还是 locked？",
            "PRD 状态未锁定，会直接影响本轮能否安全 rewrite 或进入 delegation。",
            "拿到 PRD 状态后，先重新过 Gate，再决定是否 rewrite。",
        )
    if "还是" in lowered and any(token in lowered for token in ["优先", "先做", "先闭环"]):
        return (
            "这轮优先闭环的是哪一个主目标？",
            "输入里存在主目标冲突，当前不能稳定归类为单轮闭环。",
            "拿到唯一主目标后，先重新过 Gate，再判断是否需要拆轮 rewrite。",
        )
    return (
        "请只补充当前最关键的缺失上下文是什么？",
        "当前输入仍有关键不确定项，不能安全 rewrite。",
        "拿到最短澄清回复后，重新过 Gate。",
    )


def derive_missing_strengthening_items(
    input_type: str,
    contract_result,
    pass_evidence_present_flag: bool,
) -> list[str]:
    items: list[str] = []
    field_to_item = {
        "project_round_stage_prd": "project_round_stage_prd",
        "task_type": "task_type",
        "round_goal": "round_goal",
        "out_of_scope": "out_of_scope",
        "acceptance": "acceptance",
        "dependency_fallback_blocker": "fallback_blocker_rule",
        "structured_return": "structured_return",
        "test_requirement": "test_requirement",
        "prd_alignment": "prd_alignment",
    }

    for field in contract_result.missing_fields:
        mapped = field_to_item.get(field)
        if mapped:
            items.append(mapped)

    for field in contract_result.weak_fields:
        if field == "dependency_fallback_blocker":
            items.append("fallback_blocker_rule")
        elif field == "out_of_scope":
            items.append("tighter_out_of_scope")

    if input_type in {"raw_request", "pseudo_qualified_prompt"} and not contract_result.why_not_split_present:
        items.append("why_not_split")
    if not pass_evidence_present_flag:
        items.extend(["round_main_closure", "pass_evidence"])

    return sorted(set(items))


def build_split_plan(round_id: str | None, theme_hits: list[str], contract_result) -> list[str]:
    if contract_result.multi_closure_risk not in {"medium", "high"}:
        return []

    prefix = round_id or "round"
    plan: list[str] = []
    index = 0

    def add_plan(label: str, goal: str) -> None:
        nonlocal index
        index += 1
        suffix = chr(ord("A") + index - 1)
        plan.append(f"{prefix}{suffix}: {goal}")

    if "generation" in theme_hits:
        if "style" in theme_hits:
            add_plan("generation_style", "先闭环生成主路径，并把风格控制限定为该主路径的必要接线")
        else:
            add_plan("generation", "先闭环生成主路径")
    if "export" in theme_hits:
        add_plan("export", "单独补导出能力闭环")
    if "api" in theme_hits:
        add_plan("api", "补 API 主入口接线")
    if "web_ui" in theme_hits:
        add_plan("web_ui", "补 Web UI 主入口接线")
    if "cli" in theme_hits:
        add_plan("cli", "补 CLI 主入口接线")
    if not plan:
        add_plan("closure", "先压成一个最小可验收主闭环，再把次要主题后移")
    return plan


def build_rewrite_suggestions(
    input_type: str,
    contract_result,
    theme_hits: list[str],
    evidence_present: bool,
    round_id: str | None,
) -> tuple[list[str], list[str], list[str]]:
    if input_type == "qualified_round_prompt" and contract_result.contract_pass:
        return [], [], []
    if input_type == "ambiguous_input":
        return [], [], []

    rewrite_actions: list[str] = []

    if input_type == "raw_request":
        rewrite_actions.extend(["tighten_scope", "add_contract_fields"])
    if input_type == "pseudo_qualified_prompt":
        rewrite_actions.append("tighten_scope")
    if contract_result.multi_closure_risk == "high" or len(theme_hits) >= 2:
        rewrite_actions.append("split")
    if not contract_result.fallback_blocker_present:
        rewrite_actions.append("add_fallback")
    if not evidence_present:
        rewrite_actions.append("add_pass_evidence")
    if contract_result.missing_fields:
        rewrite_actions.append("add_contract_fields")

    split_plan = build_split_plan(round_id, theme_hits, contract_result) if "split" in rewrite_actions else []
    missing_strengthening_items = derive_missing_strengthening_items(input_type, contract_result, evidence_present)
    return sorted(set(rewrite_actions)), split_plan, missing_strengthening_items


def analyze_gate(text: str) -> GateResult:
    project = extract_value(text, ["项目名", "当前项目", "项目"])
    round_id = extract_round(text)
    stage = extract_value(text, ["当前阶段", "阶段"])
    prd_status = extract_value(text, ["当前 PRD 状态", "PRD 状态"])
    task_type = task_type_guess(text)
    evidence_present = pass_evidence_present(text)
    contract_result = analyze_contract(text)
    theme_hits = detect_theme_hits(text)

    blockers: list[str] = []
    missing_or_weak_items = list(contract_result.missing_fields) + list(contract_result.weak_fields)
    minimal_clarification_question = ""
    clarification_reason = ""
    next_action_after_answer = ""

    is_ambiguous = ambiguous_input(text, project, round_id, stage, prd_status)
    structured_shape = sum(1 for present in contract_result.field_presence.values() if present) >= 6
    pseudo_like = structured_shape and (
        contract_result.multi_closure_risk in {"medium", "high"}
        or not contract_result.why_not_split_present
        or not contract_result.fallback_blocker_present
        or not evidence_present
    )

    if is_ambiguous:
        input_type = "ambiguous_input"
        gate_result = "CLARIFICATION_REQUIRED"
        blockers.append("项目 / 轮次 / 阶段 / PRD 状态存在缺口或引用关系不清")
        short_reason = "当前输入带有接手或续做语义，但上下文锚点不足，不能安全 rewrite。"
        next_action = "只问一个最小阻塞问题，再重新过 Gate。"
        (
            minimal_clarification_question,
            clarification_reason,
            next_action_after_answer,
        ) = determine_clarification(text, project, round_id, stage, prd_status)
    elif structured_shape and not pseudo_like and contract_result.contract_pass:
        input_type = "qualified_round_prompt"
        gate_result = "PASS"
        short_reason = "输入已收成单轮主闭环，契约字段与 PASS evidence 基本齐全。"
        next_action = "记录 Gate 结果，然后进入 scoring / Build Delegation。"
    elif structured_shape:
        input_type = "pseudo_qualified_prompt"
        gate_result = "REWRITE_REQUIRED"
        short_reason = "输入看起来像 round prompt，但仍未证明自己是单轮最小闭环。"
        next_action = "先 rewrite，必要时拆轮；补齐 why-not-split、fallback/blocker 和 PASS evidence 后再 re-gate。"
        if contract_result.multi_closure_risk in {"medium", "high"}:
            blockers.append("存在多主闭环或多入口并行改造风险")
        if not contract_result.why_not_split_present:
            blockers.append("缺少 why-not-split")
        if not contract_result.fallback_blocker_present:
            blockers.append("fallback / blocker 规则无效或缺失")
        if not evidence_present:
            blockers.append("缺少完整 PASS evidence")
    else:
        input_type = "raw_request"
        gate_result = "REWRITE_REQUIRED"
        short_reason = "当前更像原始需求块，还没有收成可直接派单的 round prompt。"
        next_action = "先 rewrite 成单轮 round prompt，再重新过 Gate。"
        if not project:
            missing_or_weak_items.append("project_round_stage_prd")
        if task_type == "无法稳定判断":
            missing_or_weak_items.append("task_type")

    if contract_result.multi_closure_risk == "high" and "存在多主闭环或多入口并行改造风险" not in blockers:
        blockers.append("存在多主闭环或多入口并行改造风险")

    split_recommendation = build_split_recommendation(theme_hits, contract_result)
    rewrite_actions, split_plan, missing_strengthening_items = build_rewrite_suggestions(
        input_type,
        contract_result,
        theme_hits,
        evidence_present,
        round_id,
    )

    return GateResult(
        input_type=input_type,
        gate_result=gate_result,
        task_type_guess=task_type,
        blockers=sorted(set(blockers)),
        missing_or_weak_items=sorted(set(missing_or_weak_items)),
        split_recommendation=split_recommendation,
        pass_evidence_present=evidence_present,
        short_reason=short_reason,
        project=project,
        round_id=round_id,
        stage=stage,
        prd_status=prd_status,
        is_pseudo_qualified=input_type == "pseudo_qualified_prompt",
        single_round_closure=gate_result == "PASS",
        next_action=next_action,
        minimal_clarification_question=minimal_clarification_question,
        clarification_reason=clarification_reason,
        next_action_after_answer=next_action_after_answer,
        rewrite_actions=rewrite_actions,
        split_plan=split_plan,
        missing_strengthening_items=missing_strengthening_items,
        source_summary=compact_text(text),
    )
