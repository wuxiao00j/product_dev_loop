# product_dev_loop

## Overview

`product_dev_loop` 是一个把 AI 协作开发流程拆成“编排层 + 分析层”的公开仓库，用来帮助团队把零散的想法、原始需求、执行回执和测试反馈，稳定推进成可持续的产品开发闭环。

`product_dev_loop` is a public repository that separates AI-assisted product development into two layers, an orchestration layer and an analysis layer, so teams can turn scattered ideas, raw requests, executor feedback, and testing results into a stable and repeatable development loop.

这个仓库由两部分组成：

- `skill/product_dev_loop`：编排层，负责默认协作规则、输入分流、项目接管、项目记录维护，以及最终输出收敛。
- `tool/product_dev_loop_tool`：分析层，负责 `gate`、`contract`、`skeleton`、section 级 `action-card` 和 `recommended_next_step` 等结构化诊断。

The repository is built from two parts:

- `skill/product_dev_loop`: the orchestration layer, responsible for default collaboration rules, input routing, project takeover, project record maintenance, and final output convergence.
- `tool/product_dev_loop_tool`: the analysis layer, responsible for structured diagnostics such as `gate`, `contract`, `skeleton`, section-level `action-card` guidance, and `recommended_next_step`.

这个仓库的目标不是替你自动写完所有 prompt，也不是把方法做成复杂平台，而是提供一套清晰、克制、可测试、可复用的协作结构，让不同 agent 或不同协作者在接手项目时仍然能沿着同一套规则推进。

This repository is not meant to automatically write every final prompt for you, and it is not intended to become a complex platform. Its goal is to provide a clear, disciplined, testable, and reusable collaboration structure so different agents or collaborators can continue moving a project forward under the same operating rules.

它特别适合这些场景：

- 你手上只有一段原始需求，还没有稳定的开发派单 prompt
- 你已经有项目在推进，但会话中断或换 agent 后容易丢上下文
- 你希望把 `Discovery -> PRD -> Build Delegation -> Feedback Capture -> Test Guidance -> Next-step Decision` 变成稳定闭环
- 你希望在进入正式 Build Delegation 前，先用明确规则检查 prompt 是否真的合格

It is especially useful when:

- you only have a raw request and not yet a qualified delegation prompt
- you already have a project in progress, but continuity is easily lost across sessions or agents
- you want to turn `Discovery -> PRD -> Build Delegation -> Feedback Capture -> Test Guidance -> Next-step Decision` into a stable loop
- you want formal prompt-quality checks before entering Build Delegation

这个仓库默认公开的是规则、模板、文档、示例和分析工具本身。真实项目内容应由使用者在本地 `projects/` 目录中维护，而不是直接上传到公开仓库。

What this repository publishes by default is the rules, templates, documentation, examples, and the analysis tool itself. Real project runtime content should be maintained locally in `projects/` folders instead of being uploaded into the public repository.

## Repository Structure

```text
repo-root/
├── README.md
├── docs/
│   └── getting_started.md
├── skill/
│   └── product_dev_loop/
│       ├── SKILL.md
│       ├── README.md
│       ├── docs/
│       ├── examples/
│       └── templates/
└── tool/
    └── product_dev_loop_tool/
        ├── README.md
        ├── examples/
        ├── output/
        ├── src/
        └── tests/
```

## Tool vs Skill

| Layer | Path | Role |
| --- | --- | --- |
| Analysis layer | `tool/product_dev_loop_tool` | Gate, contract, skeleton, action-card, and `recommended_next_step` analysis |
| Orchestration layer | `skill/product_dev_loop` | Default collaboration rules, input routing, project records, and final output convergence |

## What The Tool Does

`tool/product_dev_loop_tool` focuses on structured analysis, not freeform orchestration.

- `gate`: classify input and decide `PASS / REWRITE_REQUIRED / CLARIFICATION_REQUIRED`
- `contract`: check Build Delegation input contract quality
- `skeleton`: generate a safe round-prompt skeleton with section diagnostics
- `action-card`: expose repair hints and first-fix order through section-level guidance
- `recommended_next_step`: suggest whether to `rewrite_more`, `re_gate`, stay stable, or clarify first

It does not replace the main agent, does not call any LLM API, and does not automatically write the final delegation prompt for you.

## What The Skill Does

`skill/product_dev_loop` is the control layer that decides how the work should move forward.

- Applies the default collaboration rules
- Routes incoming input into the right handling path
- Decides whether to clarify, rewrite, test, record, or block
- Maintains project records and takeover continuity
- Converges output into the most useful next artifact for the user

## Recommended Usage

Use the skill as the main controller and the tool as selective support.

1. Read the skill rules first so you know the default flow.
2. Use the skill to decide the current stage and the right next output.
3. Call the tool only when you need structured prompt analysis or delegation-readiness checks.
4. Keep real project state in local `projects/` folders, not in the public repository.

## Quick Start

First read these files:

- `skill/product_dev_loop/SKILL.md`
- `skill/product_dev_loop/docs/default_collaboration_rules.md`
- `tool/product_dev_loop_tool/README.md`

Then run the tool examples from its own directory:

```bash
cd tool/product_dev_loop_tool
python3 -m unittest discover -s tests -v
python3 src/main.py gate --input examples/sample_raw_request.txt
python3 src/main.py skeleton --input examples/sample_raw_request.txt --json
```

For a first-pass workflow:

1. Start from the skill rules.
2. Use `skeleton` on a raw request.
3. Rewrite only as much as needed.
4. Re-run `gate` and `contract` when preparing formal Build Delegation.

## Default Collaboration Flow

1. Identify the input type: raw request, executor feedback, user test feedback, or external blocker.
2. If this is an ongoing project, take over the project context before acting.
3. Use `skeleton` first when the input is still rough.
4. Use `gate` and `contract` only when delegation quality needs to be checked formally.
5. Let the skill converge the output into one of four primary outputs: a prompt, test guidance, blocker reminder, or a minimal clarification question.
6. Update local project records as the collaboration progresses.

## Project File Conventions

This public repository keeps templates, docs, examples, and rules. Real project runtime files should live in local `projects/<project>/` folders created by the user.

Common local project files include:

- `PROJECT_STATE.md`
- `PRD.md`
- `PROGRESS.md`
- `ROUND_INDEX.md`
- `PROMPTS/GATE_RESULTS.md`
- `IMPLEMENTATION_NOTES.md`
- `TEST_GUIDANCE.md`
- `TEST_RESULTS.md`

The repository intentionally does not need to ship real private project data to be usable.

## Boundaries

This repository does not try to be:

- a hosted platform
- an agent runtime
- an automatic full-prompt rewriter
- an auto-approval system for Build Delegation
- a place to publish secrets, tokens, or private project history

If you need deeper instructions, start with `docs/getting_started.md`.
