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

## Repository Structure / 仓库结构

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

## Tool vs Skill / Tool 与 Skill 的分工

| Layer | Path | Role |
| --- | --- | --- |
| Analysis layer / 分析层 | `tool/product_dev_loop_tool` | Gate, contract, skeleton, action-card, and `recommended_next_step` analysis |
| Orchestration layer / 编排层 | `skill/product_dev_loop` | Default collaboration rules, input routing, project records, and final output convergence |

## What The Tool Does / Tool 做什么

`tool/product_dev_loop_tool` focuses on structured analysis, not freeform orchestration.

`tool/product_dev_loop_tool` 聚焦结构化分析，而不是自由发挥式编排。

- `gate`: classify input and decide `PASS / REWRITE_REQUIRED / CLARIFICATION_REQUIRED`
- `contract`: check Build Delegation input contract quality
- `skeleton`: generate a safe round-prompt skeleton with section diagnostics
- `action-card`: expose repair hints and first-fix order through section-level guidance
- `recommended_next_step`: suggest whether to `rewrite_more`, `re_gate`, stay stable, or clarify first

- `gate`：识别输入类型，并判断 `PASS / REWRITE_REQUIRED / CLARIFICATION_REQUIRED`
- `contract`：检查 Build Delegation 输入契约是否达标
- `skeleton`：生成安全、克制的 round prompt skeleton，并附带 section 级诊断
- `action-card`：以 section 级修复提示卡的形式给出修补方向
- `recommended_next_step`：建议下一步更适合 `rewrite_more`、`re_gate`、保持稳定还是先澄清

It does not replace the main agent, does not call any LLM API, and does not automatically write the final delegation prompt for you.

它不会替代主 agent，不调用任何 LLM API，也不会自动替你写出最终可直接发出的 delegation prompt。

## What The Skill Does / Skill 做什么

`skill/product_dev_loop` is the control layer that decides how the work should move forward.

`skill/product_dev_loop` 是决定工作如何推进的控制层。

- Applies the default collaboration rules
- Routes incoming input into the right handling path
- Decides whether to clarify, rewrite, test, record, or block
- Maintains project records and takeover continuity
- Converges output into the most useful next artifact for the user

- 应用默认协作规则
- 将输入分流到合适的处理路径
- 判断当前更适合澄清、rewrite、测试、记录还是阻塞等待
- 维护项目记录和接管连续性
- 把输出收敛成对用户最有用的下一份交付物

## Recommended Usage / 推荐用法

Use the skill as the main controller and the tool as selective support.

建议把 skill 作为主控层，把 tool 作为按需调用的分析支持层。

1. Read the skill rules first so you know the default flow.
2. Use the skill to decide the current stage and the right next output.
3. Call the tool only when you need structured prompt analysis or delegation-readiness checks.
4. Keep real project state in local `projects/` folders, not in the public repository.

1. 先读 skill 规则，先建立默认流程感。
2. 由 skill 判断当前阶段和最合适的下一步输出。
3. 只有在需要结构化分析或 delegation 就绪检查时才调用 tool。
4. 真实项目状态保留在本地 `projects/` 目录，而不是公开仓库里。

## Quick Start / 快速开始

First read these files:

第一次使用时，建议先读这些文件：

- `skill/product_dev_loop/SKILL.md`
- `skill/product_dev_loop/docs/default_collaboration_rules.md`
- `tool/product_dev_loop_tool/README.md`

Then run the tool examples from its own directory:

然后进入 tool 目录运行示例命令：

```bash
cd tool/product_dev_loop_tool
python3 -m unittest discover -s tests -v
python3 src/main.py gate --input examples/sample_raw_request.txt
python3 src/main.py skeleton --input examples/sample_raw_request.txt --json
```

For a first-pass workflow:

一个建议的首次上手流程是：

1. Start from the skill rules.
2. Use `skeleton` on a raw request.
3. Rewrite only as much as needed.
4. Re-run `gate` and `contract` when preparing formal Build Delegation.

1. 先从 skill 规则开始。
2. 先对原始需求运行 `skeleton`。
3. 只 rewrite 到足够清晰为止。
4. 在准备进入正式 Build Delegation 时，再重新运行 `gate` 和 `contract`。

## Default Collaboration Flow / 默认协作流

1. Identify the input type: raw request, executor feedback, user test feedback, or external blocker.
2. If this is an ongoing project, take over the project context before acting.
3. Use `skeleton` first when the input is still rough.
4. Use `gate` and `contract` only when delegation quality needs to be checked formally.
5. Let the skill converge the output into one of four primary outputs: a prompt, test guidance, blocker reminder, or a minimal clarification question.
6. Update local project records as the collaboration progresses.

1. 先识别输入类型：原始需求、执行器回执、用户测试反馈，还是外部阻塞。
2. 如果这是一个持续中的项目，先接管项目上下文，再采取动作。
3. 当输入仍然粗糙时，优先先跑 `skeleton`。
4. 只有在需要正式检查 delegation 质量时，才运行 `gate` 和 `contract`。
5. 让 skill 把输出收敛成四类之一：下一段 prompt、测试说明、阻塞提醒或最小澄清问题。
6. 随着协作推进，持续更新本地项目记录。

## Project File Conventions / 项目文件约定

This public repository keeps templates, docs, examples, and rules. Real project runtime files should live in local `projects/<project>/` folders created by the user.

这个公开仓库保留的是模板、文档、示例和规则。真实项目运行中的文件应由使用者保存在本地 `projects/<project>/` 目录中。

Common local project files include:

常见的本地项目文件包括：

- `PROJECT_STATE.md`
- `PRD.md`
- `PROGRESS.md`
- `ROUND_INDEX.md`
- `PROMPTS/GATE_RESULTS.md`
- `IMPLEMENTATION_NOTES.md`
- `TEST_GUIDANCE.md`
- `TEST_RESULTS.md`

The repository intentionally does not need to ship real private project data to be usable.

为了保证可公开 clone 与复用，这个仓库不需要附带任何真实私有项目数据也能正常使用。

## Boundaries / 边界说明

This repository does not try to be:

这个仓库刻意不试图变成下面这些东西：

- a hosted platform
- an agent runtime
- an automatic full-prompt rewriter
- an auto-approval system for Build Delegation
- a place to publish secrets, tokens, or private project history

- 托管平台
- agent 运行时
- 自动全文 prompt 重写器
- Build Delegation 的自动放行系统
- 发布 secrets、token 或私有项目历史的地方

If you need deeper instructions, start with `docs/getting_started.md`.

如果你想继续看更细的第一次使用说明，请从 `docs/getting_started.md` 开始。
