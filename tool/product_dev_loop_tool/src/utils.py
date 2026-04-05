from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_json(path: str, payload: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: str, content: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def print_structured(payload: dict[str, Any]) -> None:
    for key, value in payload.items():
        if isinstance(value, list):
            joined = ", ".join(value) if value else "[]"
            print(f"{key}: {joined}")
        elif isinstance(value, dict):
            print(f"{key}:")
            for child_key, child_value in value.items():
                print(f"  {child_key}: {child_value}")
        else:
            print(f"{key}: {value}")


def compact_text(text: str, limit: int = 120) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3] + "..."


def contains_any(text: str, patterns: list[str]) -> bool:
    lowered = text.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def count_present(text: str, patterns: list[str]) -> int:
    lowered = text.lower()
    return sum(1 for pattern in patterns if pattern.lower() in lowered)


def extract_value(text: str, labels: list[str]) -> str | None:
    for label in labels:
        pattern = rf"(?:{label})\s*[：:]\s*`?([^`\n]+)`?"
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def extract_round(text: str) -> str | None:
    explicit = extract_value(text, ["当前轮次", "轮次"])
    if explicit:
        return explicit
    match = re.search(r"\bround[-_ ]?\d+\b", text, flags=re.IGNORECASE)
    if match:
        return match.group(0)
    return None


def now_timestamp() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def extract_focus_text(text: str) -> str:
    lines = text.splitlines()
    section: str | None = None
    boundary_mode: str | None = None
    captured: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("【"):
            boundary_mode = None
            if line == "【本轮目标】":
                section = "goal"
            elif line == "【本轮边界】":
                section = "boundary"
            elif line == "【验收标准】":
                section = "acceptance"
            elif line == "【PASS Evidence】":
                section = "pass_evidence"
            else:
                section = None
            continue

        if section == "boundary":
            if "必做" in line:
                boundary_mode = "must"
                continue
            if "不做" in line or "保持不动" in line:
                boundary_mode = "skip"
                continue
            if boundary_mode == "must":
                captured.append(line)
            continue

        if section in {"goal", "acceptance", "pass_evidence"}:
            captured.append(line)

    return "\n".join(captured) if captured else text


def extract_section_lines(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    active = False
    captured: list[str] = []

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped.startswith("【") and stripped.endswith("】"):
            if stripped == heading:
                active = True
                continue
            if active:
                break
        if active and stripped:
            captured.append(stripped)

    return captured
