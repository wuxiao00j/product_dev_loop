from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class GateResult:
    input_type: str
    gate_result: str
    task_type_guess: str
    blockers: list[str] = field(default_factory=list)
    missing_or_weak_items: list[str] = field(default_factory=list)
    split_recommendation: str = ""
    pass_evidence_present: bool = False
    short_reason: str = ""
    project: str | None = None
    round_id: str | None = None
    stage: str | None = None
    prd_status: str | None = None
    is_pseudo_qualified: bool = False
    single_round_closure: bool = False
    next_action: str = ""
    minimal_clarification_question: str = ""
    clarification_reason: str = ""
    next_action_after_answer: str = ""
    rewrite_actions: list[str] = field(default_factory=list)
    split_plan: list[str] = field(default_factory=list)
    missing_strengthening_items: list[str] = field(default_factory=list)
    source_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ContractResult:
    contract_pass: bool
    missing_fields: list[str] = field(default_factory=list)
    weak_fields: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)
    multi_closure_risk: str = "low"
    pass_evidence_present: bool = False
    why_not_split_present: bool = False
    fallback_blocker_present: bool = False
    summary: str = ""
    field_presence: dict[str, bool] = field(default_factory=dict)
    task_type_guess: str = "无法稳定判断"
    project: str | None = None
    round_id: str | None = None
    stage: str | None = None
    prd_status: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SkeletonResult:
    input_type: str
    gate_result: str
    task_type_guess: str
    status: str
    ready_for_delegation: bool = False
    deferred: bool = False
    project: str | None = None
    round_id: str | None = None
    stage: str | None = None
    prd_status: str | None = None
    missing_items: list[str] = field(default_factory=list)
    rewrite_actions: list[str] = field(default_factory=list)
    split_plan: list[str] = field(default_factory=list)
    minimal_clarification_question: str = ""
    clarification_reason: str = ""
    next_action_after_answer: str = ""
    notes: list[str] = field(default_factory=list)
    sections: dict[str, dict[str, Any]] = field(default_factory=dict)
    gap_view: list[dict[str, Any]] = field(default_factory=list)
    first_fix_order: list[dict[str, Any]] = field(default_factory=list)
    recommended_next_step: str = ""
    skeleton_markdown: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
