# product_dev_loop_tool

## Overview

`product_dev_loop_tool` 是一个面向 `product_dev_loop` 规则的轻量 CLI 工具。它的目标不是替 agent 自动写最终 prompt，而是把 Prompt Gate、Build Delegation 输入契约、以及 round prompt skeleton 的诊断和收口辅助规则，整理成稳定、可复用、可测试的后台工具链。

它更像：

- 一个规则化 Gate / Contract 检查器
- 一个安全、克制的 skeleton 生成器
- 一个 section 级 action-card 提示器

它不是：

- 自动全文 rewrite 器
- 最终可直接发送给 Cursor / Codex 的成品 prompt 生成器
- 自动修复器
- 自动 re-gate 执行器
- 通用项目上下文读取系统

## What This Tool Is For

这个工具主要解决 3 类问题：

1. 原始输入看起来很多，但主 agent 很难快速判断它到底是 `raw_request`、`pseudo_qualified_prompt` 还是已经接近 `PASS`。
2. 就算已经生成了 skeleton，agent 仍然需要自己判断：哪里弱、先修哪里、修到什么程度算够、下一步更适合继续 rewrite 还是值得重新跑 gate。
3. 规则已经很多，纯靠聊天口述容易漂移，所以需要稳定字段、样例输出和测试把行为口径固定下来。

## What This Tool Does Not Do

本工具明确不做这些事：

- 不接 LLM API
- 不自动全文 rewrite
- 不自动生成最终 delegation prompt
- 不自动执行 re-gate / re-contract
- 不替主 agent 做最终放行判断
- 不读完整项目上下文来做深层语义规划

## Commands

### `gate`

```bash
python3 src/main.py gate --input examples/sample_raw_request.txt
python3 src/main.py gate --input examples/sample_pseudo_prompt.txt --json
python3 src/main.py gate --input examples/sample_ambiguous_input.txt --json
```

用途：

- 识别输入类型
- 给出 `PASS / REWRITE_REQUIRED / CLARIFICATION_REQUIRED`
- 输出最小补问、rewrite suggestions、split plan

### `contract`

```bash
python3 src/main.py contract --input examples/sample_pseudo_prompt.txt
python3 src/main.py contract --input examples/sample_pass_prompt.txt --json
```

用途：

- 检查 Build Delegation 输入契约
- 输出缺字段、弱字段、风险项、多主闭环风险

### `skeleton`

```bash
python3 src/main.py skeleton --input examples/sample_raw_request.txt --json
python3 src/main.py skeleton --input examples/sample_pseudo_prompt.txt
python3 src/main.py skeleton --input examples/sample_pass_prompt.txt --output output/skeleton_pass.md
python3 src/main.py skeleton --input examples/sample_ambiguous_input.txt --json
```

用途：

- 生成一个安全、克制的 round prompt skeleton
- 输出 section 级诊断和 action-card
- 给出 first-fix-order 与轻量下一步建议

### `log-gate`

```bash
python3 src/main.py log-gate --project demo-project --result-file output/gate_raw_result.json
```

用途：

- 把 Gate 结果追加写入 `projects/<project>/PROMPTS/GATE_RESULTS.md`

## Input Categories

本工具当前默认处理 4 类输入：

- `raw_request`
  - 更像原始需求块、功能清单、TODO 打包
  - 通常需要先 rewrite
- `pseudo_qualified_prompt`
  - 字段看起来比较齐，但实质上仍未收成单轮主闭环
  - 常见问题是 why-not-split、fallback/blocker、PASS evidence 不成立
- `qualified_round_prompt`
  - 已具备较稳定的 round prompt 结构
  - 仍然只输出 skeleton / draft，不直接替你放行
- `ambiguous_input`
  - 先 clarify，不应强行生成完整 skeleton

## Skeleton Output Model

### Top-Level Fields

当前 skeleton 的顶层字段主要包括：

- `input_type`
  - 输入类型判断
- `gate_result`
  - 当前 Gate 结论
- `status`
  - 当前 skeleton 状态，例如 `draft_not_ready_for_delegation`
- `ready_for_delegation`
  - 当前始终保持克制，不把 skeleton 当成最终可发文本
- `missing_items`
  - 仍需补强的 contract / gate 缺口
- `rewrite_actions`
  - 建议继续做的 rewrite 动作
- `split_plan`
  - 若有必要拆轮，给出轻量拆轮建议
- `notes`
  - 当前 skeleton 的总体说明
- `sections`
  - 每个 section 的结构化内容与诊断
- `gap_view`
  - contract 缺口如何映射到 skeleton section
- `first_fix_order`
  - 先修哪里、为什么、修到什么程度
- `recommended_next_step`
  - 当前更适合 `rewrite_more / re_gate / stable / clarify_first`
- `skeleton_markdown`
  - 便于直接阅读的 markdown 版本

### Section Structure

`sections` 下的每个 section 当前常见字段包括：

- `title`
- `content`
- `status`
  - `filled / weak / placeholder`
- `reason`
- `source_type`
  - `source / inferred / placeholder`
- `related_contract_items`
- `repair_hints`

### Repair Hint Structure

每条 `repair_hint` 当前是一个小动作卡片：

- `text`
- `priority`
  - `critical / important / optional`
- `type`
  - 例如 `lock_context / tighten_scope / add_fallback / add_alignment`

### First Fix Order Structure

`first_fix_order` 当前每项包括：

- `section_key`
- `section`
- `priority`
- `reason`
- `suggested_action`
- `expected_outcome`
- `stop_condition`
- `next_check`
- `check_signal`

## Section-Level Diagnostics

Skeleton 的核心不是“把内容凑满”，而是先告诉 agent：

- 哪些 section 已经可用
- 哪些 section 仍然偏弱
- 哪些 section 还只是占位
- 这些弱点分别由哪些 contract / gate 缺口导致

当前状态语义：

- `filled`
  - 当前 section 有可用内容，可作为二次收口底稿
- `weak`
  - 有内容，但仍被 contract / gate 缺口命中
- `placeholder`
  - 主要还是骨架占位，agent 需要补真实内容

## Repair Hints And Action Cards

Repair hints 负责告诉 agent：

- 这块要补哪种动作
- 这块补的优先级大概多高

它们是 section 级提示，不是全文代写。

当前高频 `type` 包括：

- `lock_context`
- `tighten_scope`
- `add_constraint`
- `add_fallback`
- `add_acceptance`
- `add_alignment`
- `add_pass_evidence`
- `add_test_requirement`

## First Fix Order Semantics

`first_fix_order` 负责告诉 agent：

- 当前最该先修哪个 section
- 为什么先修它
- 修完后理论上会带来什么改善
- 修到什么程度先够
- 修完后立刻检查什么
- 看到什么现象可初步认为它过线

这不是自动修复计划，只是修补顺序建议。

### Field Semantics

- `suggested_action`
  - 现在先去补什么
  - 更像动作起点
- `expected_outcome`
  - 补完这一块后，整体收口会有什么改善
- `stop_condition`
  - 这块修到什么程度先够继续往下走
- `next_check`
  - 现在去检查什么
  - 是动作式表达
- `check_signal`
  - 看到什么说明这块基本过线
  - 是结果式表达

可以把它们理解成：

- `suggested_action`：先做什么
- `expected_outcome`：做完会改善什么
- `stop_condition`：做到哪儿先够
- `next_check`：现在去检查什么
- `check_signal`：看到什么说明基本过线

## Recommended Next Step Semantics

`recommended_next_step` 是轻量建议，不是流程控制器。

当前可能值：

- `clarify_first`
  - 输入仍然模糊，应先澄清
- `rewrite_more`
  - 关键 placeholder / 上游缺口仍明显，继续 rewrite 更有价值
- `re_gate`
  - 上游关键项基本成形，再继续局部修补收益下降，值得重新跑 gate / contract
- `stable`
  - 当前已是 `PASS` 型 skeleton，保持克制，不再过度建议下一步

## Scenario Behavior

### `raw_request`

典型行为：

- `draft_not_ready_for_delegation`
- `recommended_next_step = rewrite_more`
- `project_info / round_goal / round_boundary / acceptance / dependency_rules` 常常是 `placeholder`
- first-fix-order 往往从 `当前项目信息 -> 任务类型 -> 本轮目标` 开始

原因：

- 它本质上还是原始需求块，还没形成可派单的 round prompt 结构

### `pseudo_qualified_prompt`

典型行为：

- 仍然是 draft
- 常见 top issues 是：
  - `round_main_closure`
  - `why_not_split`
  - `fallback_blocker_rule`
  - `prd_alignment`
  - `pass_evidence`
- `recommended_next_step` 通常偏 `rewrite_more`
- 当关键项已基本成形时，理论上可进入 `re_gate`，但当前实现仍保持保守

原因：

- 形式完整不等于闭环完整

### `qualified_round_prompt` / `PASS`

典型行为：

- section 多为 `filled`
- repair hints 为空或极少
- `first_fix_order = []`
- `recommended_next_step = stable`

原因：

- 这时 skeleton 更像一个稳定底稿，而不是修补清单

### `ambiguous_input`

典型行为：

- `deferred_until_clarification`
- 不铺满完整 skeleton
- 直接输出 clarification block
- `recommended_next_step = clarify_first`

原因：

- 这个阶段不该 rewrite，更不该伪装成可派单 prompt

## Task-Type-Aware Hint Templates

当前只做了轻量、少量的 task-type 差异化。

重点覆盖：

- `build`
  - 强调新增主闭环、依赖接线、验证新增主路径
- `fix`
  - 强调问题修复、复现步骤、回归验证、不要顺手重构
- `polish`
  - 强调局部优化、影响面受控、不改主流程
- `unblock`
  - 强调阻塞解除、降级路径、继续推进条件

边界：

- 不是所有 section 都会做 task-type 差异化
- 只覆盖高频且明显有帮助的 section
- 不做复杂模板系统

## What This Tool Does Not Do

本工具当前明确不做：

- 自动全文 rewrite
- 自动修复
- 自动 re-gate / re-contract
- 自动最终放行
- LLM 接入
- 复杂动态规划
- 全项目上下文推理器

## Testing And Snapshots

运行测试：

```bash
cd /Users/barry/Desktop/cursor/tool/product_dev_loop_tool
python3 -m unittest discover -s tests -v
```

当前样例输出：

- [output/skeleton_raw.json](/Users/barry/Desktop/cursor/tool/product_dev_loop_tool/output/skeleton_raw.json)
- [output/skeleton_pseudo.json](/Users/barry/Desktop/cursor/tool/product_dev_loop_tool/output/skeleton_pseudo.json)
- [output/skeleton_pass.json](/Users/barry/Desktop/cursor/tool/product_dev_loop_tool/output/skeleton_pass.json)
- [output/skeleton_ambiguous.json](/Users/barry/Desktop/cursor/tool/product_dev_loop_tool/output/skeleton_ambiguous.json)

当前快照：

- [tests/snapshots/skeleton_raw_request.json](/Users/barry/Desktop/cursor/tool/product_dev_loop_tool/tests/snapshots/skeleton_raw_request.json)
- [tests/snapshots/skeleton_pseudo_prompt.json](/Users/barry/Desktop/cursor/tool/product_dev_loop_tool/tests/snapshots/skeleton_pseudo_prompt.json)
- [tests/snapshots/skeleton_pass_prompt.json](/Users/barry/Desktop/cursor/tool/product_dev_loop_tool/tests/snapshots/skeleton_pass_prompt.json)

如果 README 重组但核心逻辑未变，快照和输出应保持一致；本轮仍建议真实跑一次测试确认没有意外漂移。numerusformеиԥш to=functions.exec_command  天天中彩票怎么买json
