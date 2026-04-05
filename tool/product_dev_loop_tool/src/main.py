from __future__ import annotations

import argparse
import json
import sys

from contract_checker import analyze_contract
from gate_checker import analyze_gate
from gate_logger import append_gate_log
from skeleton_builder import build_skeleton
from utils import print_structured, read_text, write_json, write_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="product_dev_loop_tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gate_parser = subparsers.add_parser("gate", help="Run Prompt Gate checks")
    gate_parser.add_argument("--input", required=True, help="Path to raw request or round prompt text")
    gate_parser.add_argument("--json", action="store_true", help="Print JSON only")
    gate_parser.add_argument("--output", help="Optional path to save JSON result")

    contract_parser = subparsers.add_parser("contract", help="Run Build Delegation contract checks")
    contract_parser.add_argument("--input", required=True, help="Path to round prompt text")
    contract_parser.add_argument("--json", action="store_true", help="Print JSON only")
    contract_parser.add_argument("--output", help="Optional path to save JSON result")

    skeleton_parser = subparsers.add_parser("skeleton", help="Build a safe round prompt skeleton")
    skeleton_parser.add_argument("--input", required=True, help="Path to raw request or round prompt text")
    skeleton_parser.add_argument("--json", action="store_true", help="Print JSON instead of markdown skeleton")
    skeleton_parser.add_argument("--output", help="Optional path to save skeleton output")

    logger_parser = subparsers.add_parser("log-gate", help="Append a gate result to markdown log")
    logger_parser.add_argument("--project", required=True, help="Project name")
    logger_parser.add_argument("--result-file", required=True, help="Path to gate result JSON")
    logger_parser.add_argument(
        "--project-root",
        default=".",
        help="Root folder containing the projects directory. Defaults to current working directory.",
    )

    return parser


def handle_gate(args: argparse.Namespace) -> int:
    result = analyze_gate(read_text(args.input)).to_dict()
    if args.output:
        write_json(args.output, result)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_structured(result)
    return 0


def handle_contract(args: argparse.Namespace) -> int:
    result = analyze_contract(read_text(args.input)).to_dict()
    if args.output:
        write_json(args.output, result)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_structured(result)
    return 0


def handle_skeleton(args: argparse.Namespace) -> int:
    result = build_skeleton(read_text(args.input))
    if args.output:
        if args.json:
            write_json(args.output, result.to_dict())
        else:
            write_text(args.output, result.skeleton_markdown)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.skeleton_markdown, end="")
    return 0


def handle_log_gate(args: argparse.Namespace) -> int:
    with open(args.result_file, "r", encoding="utf-8") as file:
        payload = json.load(file)
    path = append_gate_log(args.project_root, args.project, payload)
    print(json.dumps({"logged": True, "path": path}, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "gate":
        return handle_gate(args)
    if args.command == "contract":
        return handle_contract(args)
    if args.command == "skeleton":
        return handle_skeleton(args)
    if args.command == "log-gate":
        return handle_log_gate(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
