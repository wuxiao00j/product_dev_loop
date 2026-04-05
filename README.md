# product_dev_loop

## Overview

`product_dev_loop` is a merged public repository for a two-layer AI collaboration workflow:

- `tool/product_dev_loop_tool` is the analysis layer.
- `skill/product_dev_loop` is the orchestration layer.

The goal is to keep the repository cloneable, understandable, and directly reusable without turning it into a complex platform.

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
