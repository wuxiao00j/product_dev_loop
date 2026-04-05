from __future__ import annotations

import json
from pathlib import Path

from utils import now_timestamp


def load_result(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def append_gate_log(project_root: str, project: str, result: dict) -> str:
    target_dir = Path(project_root) / "projects" / project / "PROMPTS"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / "GATE_RESULTS.md"

    blockers = result.get("blockers") or ["无"]
    missing_items = result.get("missing_or_weak_items") or ["无"]
    pass_evidence_summary = "存在" if result.get("pass_evidence_present") else "缺失"
    clarification_question = result.get("minimal_clarification_question") or "无"
    rewrite_actions = result.get("rewrite_actions") or ["无"]
    split_plan = result.get("split_plan") or ["无"]

    entry = f"""## Gate Run | {now_timestamp()}

- input_type: `{result.get("input_type", "unknown")}`
- gate_result: `{result.get("gate_result", "unknown")}`
- pseudo_qualified: `{"yes" if result.get("is_pseudo_qualified") else "no"}`
- project: `{result.get("project") or project}`
- round: `{result.get("round_id") or "unknown"}`
- stage: `{result.get("stage") or "unknown"}`
- PRD status: `{result.get("prd_status") or "unknown"}`
- blockers: {", ".join(blockers)}
- missing_or_weak_items: {", ".join(missing_items)}
- split recommendation: {result.get("split_recommendation", "无")}
- minimal clarification question: {clarification_question}
- rewrite actions: {", ".join(rewrite_actions)}
- split plan: {" | ".join(split_plan)}
- next action: {result.get("next_action", "无")}
- PASS evidence summary: {pass_evidence_summary}
- short reason: {result.get("short_reason", "无")}

"""

    if not target_file.exists():
        header = "# GATE_RESULTS\n\n"
        target_file.write_text(header + entry, encoding="utf-8")
    else:
        with target_file.open("a", encoding="utf-8") as file:
            file.write(entry)

    return str(target_file)
