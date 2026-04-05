from __future__ import annotations

from models import ContractResult
from rules.contract_rules import CONTRACT_FIELD_PATTERNS, WEAK_FALLBACK_PATTERNS, WHY_NOT_SPLIT_PATTERNS
from utils import contains_any, count_present, extract_focus_text, extract_round, extract_value


def detect_task_type(text: str) -> str:
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


def build_field_presence(text: str) -> dict[str, bool]:
    presence: dict[str, bool] = {}
    for field_name, patterns in CONTRACT_FIELD_PATTERNS.items():
        if field_name == "project_round_stage_prd":
            project = extract_value(text, ["项目名", "当前项目", "项目"])
            round_id = extract_round(text)
            stage = extract_value(text, ["当前阶段", "阶段"])
            prd_status = extract_value(text, ["当前 PRD 状态", "PRD 状态"])
            presence[field_name] = all([project, round_id, stage, prd_status])
        else:
            threshold = 1
            if field_name == "structured_return":
                threshold = 3
            elif field_name == "test_requirement":
                threshold = 3
            elif field_name == "prd_alignment":
                threshold = 2
            presence[field_name] = count_present(text, patterns) >= threshold
    return presence


def fallback_blocker_present(text: str) -> bool:
    lowered = text.lower()
    has_dependency = any(token in lowered for token in ["关键依赖", "dependency", "依赖"])
    has_fallback = any(token in lowered for token in ["降级方案", "fallback", "依赖不满足"])
    has_blocker = any(token in lowered for token in ["直接阻塞", "blocker", "阻塞"])
    if not (has_dependency and has_fallback and has_blocker):
        return False
    if any(pattern.lower() in lowered for pattern in WEAK_FALLBACK_PATTERNS):
        return False
    return True


def pass_evidence_present(text: str) -> bool:
    lowered = text.lower()
    return all(
        token.lower() in lowered
        for token in [
            "prompt gate",
            "pass",
            "round main closure",
            "why not split",
            "fallback / blocker rule",
            "delegation contract",
            "satisfied",
        ]
    )


def analyze_contract(text: str) -> ContractResult:
    field_presence = build_field_presence(text)
    missing_fields = [field for field, present in field_presence.items() if not present]
    weak_fields: list[str] = []
    risk_flags: list[str] = []

    project = extract_value(text, ["项目名", "当前项目", "项目"])
    round_id = extract_round(text)
    stage = extract_value(text, ["当前阶段", "阶段"])
    prd_status = extract_value(text, ["当前 PRD 状态", "PRD 状态"])
    task_type = detect_task_type(text)
    theme_hits = detect_theme_hits(text)

    why_not_split_present = contains_any(text, WHY_NOT_SPLIT_PATTERNS)
    fallback_ok = fallback_blocker_present(text)
    pass_evidence_ok = pass_evidence_present(text)

    if not fallback_ok and count_present(text, CONTRACT_FIELD_PATTERNS["dependency_fallback_blocker"]) > 0:
        weak_fields.append("dependency_fallback_blocker")
        risk_flags.append("fallback / blocker 规则为空壳或缺少明确降级边界")

    if len(theme_hits) >= 3:
        risk_flags.append("多个核心能力主题同时出现")
    if len([theme for theme in theme_hits if theme in {"cli", "api", "web_ui"}]) >= 2:
        risk_flags.append("CLI / API / Web UI 多入口改造")
    if "polish" in theme_hits and any(theme in theme_hits for theme in {"generation", "export", "api", "web_ui", "cli"}):
        risk_flags.append("新能力实现与优化目标混合")
    if "dependency" in theme_hits and any(theme in theme_hits for theme in {"generation", "export", "api", "web_ui", "cli"}):
        risk_flags.append("依赖接入与主功能实现混合")
    if not why_not_split_present and len(theme_hits) >= 2:
        risk_flags.append("命中拆轮信号但缺少 why-not-split")
    if not pass_evidence_ok:
        risk_flags.append("缺少完整 PASS evidence")

    required_for_single_closure = {"generation", "style", "export", "cli", "api", "web_ui"}
    focused_hits = [theme for theme in theme_hits if theme in required_for_single_closure]
    if len(focused_hits) >= 4 or len(risk_flags) >= 3:
        multi_closure_risk = "high"
    elif len(focused_hits) >= 2 or len(risk_flags) >= 1:
        multi_closure_risk = "medium"
    else:
        multi_closure_risk = "low"

    if field_presence.get("out_of_scope") and multi_closure_risk in {"medium", "high"}:
        weak_fields.append("out_of_scope")
        risk_flags.append("虽然写了不做，但没有真正削掉并列主目标")

    contract_pass = (
        not missing_fields
        and not weak_fields
        and multi_closure_risk != "high"
        and why_not_split_present
        and fallback_ok
        and pass_evidence_ok
    )

    if contract_pass:
        summary = "输入契约字段齐全，PASS evidence 完整，未发现高风险多主闭环信号。"
    else:
        summary = "输入仍未满足 Build Delegation 输入契约；需要先补齐缺字段、削减多主闭环风险或补 PASS evidence。"

    return ContractResult(
        contract_pass=contract_pass,
        missing_fields=missing_fields,
        weak_fields=sorted(set(weak_fields)),
        risk_flags=sorted(set(risk_flags)),
        multi_closure_risk=multi_closure_risk,
        pass_evidence_present=pass_evidence_ok,
        why_not_split_present=why_not_split_present,
        fallback_blocker_present=fallback_ok,
        summary=summary,
        field_presence=field_presence,
        task_type_guess=task_type,
        project=project,
        round_id=round_id,
        stage=stage,
        prd_status=prd_status,
    )
