# Round Prompt Skeleton

- status: `draft_not_ready_for_delegation`
- input_type: `raw_request`
- gate_result: `REWRITE_REQUIRED`
- ready_for_delegation: `false`

## Notes

- 这是 skeleton / draft，只用于 agent 二次收口，不是最终可直接派单文本。
- 当前输入仍未通过 Gate，不能直接进入 Build Delegation。
- contract missing fields: project_round_stage_prd, task_type, round_goal, out_of_scope, acceptance, dependency_fallback_blocker, structured_return, test_requirement, prd_alignment

Recommended next step: `rewrite_more`

## Missing Strengthening Items

- acceptance
- fallback_blocker_rule
- out_of_scope
- pass_evidence
- prd_alignment
- project_round_stage_prd
- round_goal
- round_main_closure
- structured_return
- task_type
- test_requirement
- why_not_split

## Contract-to-Skeleton Gap View

- acceptance -> affects: [验收标准] -> action: 把验收改成外部可判断的结果句子，而不是愿景描述。
- fallback_blocker_rule -> affects: [依赖与降级规则, PASS Evidence] -> action: 补一句依赖失败时如何降级，哪些情况必须直接阻塞。
- out_of_scope -> affects: [本轮边界] -> action: 补清本轮不做和保持不动，防止顺手扩做。
- pass_evidence -> affects: [PASS Evidence] -> action: 补完整 PASS evidence，证明当前输入不是伪合格 prompt。
- prd_alignment -> affects: [完成后必须结构化回传] -> action: 补 PRD 对照要求，说明对应条目、已满足项和未满足项。
- project_round_stage_prd -> affects: [当前项目信息] -> action: 补齐项目名、轮次、阶段和 PRD 状态，再重新判断是否可进入 delegation。
- round_goal -> affects: [本轮目标] -> action: 把目标压成一个单轮最小闭环，并补一句用户可见结果。
- round_main_closure -> affects: [本轮目标, PASS Evidence] -> action: 补一句 Round main closure，写清本轮唯一主闭环。
- structured_return -> affects: [完成后必须结构化回传] -> action: 补固定结构化回传字段，方便主 agent 收口。
- task_type -> affects: [任务类型] -> action: 补稳定任务类型，避免 build / fix / polish / unblock 混用。
- test_requirement -> affects: [测试要求] -> action: 补测试入口、步骤、数据、预期结果和失败判定。
- why_not_split -> affects: [本轮目标, PASS Evidence] -> action: 补一句 why-not-split，或把当前输入拆成多轮。

## First Fix Order

1. 当前项目信息 [critical]
   - suggested_action: 补齐项目名、轮次、阶段和 PRD 状态
   - expected_outcome: 后续 section 的约束会更稳定。
   - stop_condition: 出现明确项目名、轮次、阶段和 PRD 状态即可。
   - next_check: 检查项目名、轮次、阶段和 PRD 状态是否都已明确出现。
   - check_signal: 已出现项目名 / 轮次 / 阶段 / PRD 状态。
   - reason: 当前 section 主要还是骨架占位，agent 需要补真实内容。
2. 任务类型 [critical]
   - suggested_action: 补齐稳定任务类型，明确 build / fix / polish / unblock
   - expected_outcome: 后续目标、边界和验收会更容易按同一类型收口。
   - stop_condition: 任务类型能稳定落到 build / fix / polish / unblock 之一即可。
   - next_check: 检查任务类型是否已稳定且不再混用。
   - check_signal: 已出现稳定任务类型，且不再混用。
   - reason: 当前 section 有内容，但仍受这些缺口影响：task_type。
3. 本轮目标 [critical]
   - suggested_action: 把本轮目标压成一个单轮主闭环，并补一句用户可见结果
   - expected_outcome: 边界、验收和拆轮判断会更容易对齐。
   - stop_condition: 目标收敛成一个单轮主闭环，并包含用户可见结果即可。
   - next_check: 检查本轮目标是否只剩一个主闭环，且有用户可见结果。
   - check_signal: 目标段只剩一个主闭环，且带用户可见结果。
   - reason: 当前 section 主要还是骨架占位，agent 需要补真实内容。
4. 依赖与降级规则 [critical]
   - suggested_action: 补一句依赖失败时的 fallback / blocker 处理
   - expected_outcome: 依赖失败时仍会有清晰的降级或阻塞路径。
   - stop_condition: 补出依赖失败时的 fallback / blocker 处理即可。
   - next_check: 检查是否已经写出依赖失败时的 fallback / blocker 路径。
   - check_signal: 已写出 fallback / blocker 处理。
   - reason: 当前 section 主要还是骨架占位，agent 需要补真实内容。
5. PASS Evidence [critical]
   - suggested_action: 补一句 PASS evidence，说明为什么当前可直接进入 Build Delegation
   - expected_outcome: 继续往下修时会更容易判断何时接近可放行状态。
   - stop_condition: 补出 why-not-split、round main closure 或 fallback/blocker 关键证据即可。
   - next_check: 检查是否已经写出 why-not-split、round main closure 或 fallback/blocker 关键证据。
   - check_signal: 已出现 why-not-split / round main closure / fallback-blocker 关键证据。
   - reason: 当前 section 有内容，但仍受这些缺口影响：pass_evidence, round_main_closure, why_not_split, fallback_blocker_rule。

## 任务类型 [weak]

- reason: 当前 section 有内容，但仍受这些缺口影响：task_type。
- source_type: inferred
- related_contract_items: task_type
- repair_hints:
  - [critical][lock_context] 补齐稳定任务类型，明确 build / fix / polish / unblock
- 本轮类型：`无法稳定判断`
- 选择原因：`待 agent 根据 PRD 与反馈再确认`

## 当前项目信息 [placeholder]

- reason: 当前 section 主要还是骨架占位，agent 需要补真实内容。
- source_type: placeholder
- related_contract_items: project_round_stage_prd
- repair_hints:
  - [critical][lock_context] 补齐项目名、轮次、阶段和 PRD 状态
  - [critical][lock_context] 补齐最小项目信息后再继续后面的 skeleton 收口
- 项目名：`待补`
- 当前轮次：`待补`
- 当前阶段：`Build Delegation`
- 当前 PRD 状态：`待补`
- 当前 Gate 状态：`REWRITE_REQUIRED`

## 执行前必读上下文 [filled]

- reason: 当前 section 已有可用内容，可作为 agent 二次收口底稿。
- source_type: inferred
- 必读：`PROJECT_STATE.md`
- 必读：`PRD.md`
- 必读：最近一轮 `PROGRESS.md`
- 必读：最近一轮 `IMPLEMENTATION_NOTES.md`
- 按需补读：`ARCHITECTURE.md` / `CHANGE_PROPOSALS.md` / `TEST_RESULTS.md`

## 本轮目标 [placeholder]

- reason: 当前 section 主要还是骨架占位，agent 需要补真实内容。
- source_type: placeholder
- related_contract_items: round_goal, round_main_closure, why_not_split
- repair_hints:
  - [critical][tighten_scope] 把本轮目标压成一个单轮主闭环，并补一句用户可见结果
  - [critical][add_pass_evidence] 补一句 Round main closure，写清本轮唯一主闭环
- 本轮只解决：`待 agent 收敛成一个单轮最小闭环`
- 这轮完成后，用户能直接看到的结果：`待补`
- 本轮目标来源：`PRD 条目 / 测试反馈 / 上轮未完成项 / 外部阻塞`

## 本轮边界 [placeholder]

- reason: 当前 section 主要还是骨架占位，agent 需要补真实内容。
- source_type: placeholder
- related_contract_items: out_of_scope
- repair_hints:
  - [important][add_constraint] 补齐本轮不做和保持不动，防止顺手扩做
  - [important][add_constraint] 补一句强边界，明确排除顺手扩做内容
- 必做：`待补`
- 不做：`待补，需写清禁止扩散内容`
- 保持不动：`待补`
- 重点文件 / 模块：`待补`

## 验收标准 [placeholder]

- reason: 当前 section 主要还是骨架占位，agent 需要补真实内容。
- source_type: placeholder
- related_contract_items: acceptance
- repair_hints:
  - [important][add_acceptance] 补一句围绕单轮主闭环的验收标准
- 验收项 1：`待补`
- 验收项 2：`待补`
- 验收项 3：`待补`

## 依赖与降级规则 [placeholder]

- reason: 当前 section 主要还是骨架占位，agent 需要补真实内容。
- source_type: placeholder
- related_contract_items: fallback_blocker_rule
- repair_hints:
  - [critical][add_fallback] 补一句依赖失败时的 fallback / blocker 处理
  - [critical][add_fallback] 补一句依赖失败时如何降级，以及哪些情况必须直接阻塞
- 关键依赖：`待补`
- 依赖满足时：`待补`
- 依赖不满足时允许的降级方案：`待补`
- 哪些情况应直接标记阻塞，不继续扩做：`待补`

## 测试要求 [weak]

- reason: 当前 section 有内容，但仍受这些缺口影响：test_requirement。
- source_type: inferred
- related_contract_items: test_requirement
- repair_hints:
  - [important][add_test_requirement] 补一句可执行测试方式和失败判定
- 请返回测试入口
- 请返回操作步骤
- 请返回测试数据
- 请返回预期结果
- 请返回失败判定

## 完成后必须结构化回传 [weak]

- reason: 当前 section 有内容，但仍受这些缺口影响：structured_return, prd_alignment。
- source_type: inferred
- related_contract_items: structured_return, prd_alignment
- repair_hints:
  - [important][add_constraint] 补齐固定结构化回传字段
  - [important][add_alignment] 补一句完成后按 PRD 条目逐项对照回传
1. 已完成
2. 未完成
3. 关键代码信息
4. `stub / mock / 假数据 / 隐藏入口 / 未接线`
5. 风险与需确认点
6. 测试建议
7. PRD 对照

## PASS Evidence [weak]

- reason: 当前 section 有内容，但仍受这些缺口影响：pass_evidence, round_main_closure, why_not_split, fallback_blocker_rule。
- source_type: inferred
- related_contract_items: pass_evidence, round_main_closure, why_not_split, fallback_blocker_rule
- repair_hints:
  - [critical][add_pass_evidence] 补一句 PASS evidence，说明为什么当前可直接进入 Build Delegation
  - [critical][add_pass_evidence] 补一句 Round main closure，写清本轮唯一主闭环
- Prompt Gate：`尚未 PASS`
- Delegation contract：`not yet`
- 说明：`当前仍是 skeleton / draft，不应直接派单`
- Round main closure：`待补，需用一句话写清本轮唯一主闭环`
- Why not split：`待补，需说明为什么本轮不拆轮`
- Fallback / blocker rule：`待补，需写清降级边界和直接阻塞条件`
