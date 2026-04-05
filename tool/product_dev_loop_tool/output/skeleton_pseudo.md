# Round Prompt Skeleton

- status: `draft_not_ready_for_delegation`
- input_type: `pseudo_qualified_prompt`
- gate_result: `REWRITE_REQUIRED`
- ready_for_delegation: `false`

## Notes

- 这是 skeleton / draft，只用于 agent 二次收口，不是最终可直接派单文本。
- 当前输入仍未通过 Gate，不能直接进入 Build Delegation。
- 当前输入属于 pseudo-qualified prompt：形式较完整，但闭环仍未收口。
- contract missing fields: prd_alignment
- weak fields: dependency_fallback_blocker, out_of_scope

Recommended next step: `rewrite_more`

## Split Suggestion

- round-09A: 先闭环生成主路径，并把风格控制限定为该主路径的必要接线
- round-09B: 单独补导出能力闭环
- round-09C: 补 API 主入口接线
- round-09D: 补 Web UI 主入口接线
- round-09E: 补 CLI 主入口接线

## Missing Strengthening Items

- fallback_blocker_rule
- pass_evidence
- prd_alignment
- round_main_closure
- tighter_out_of_scope
- why_not_split

## Contract-to-Skeleton Gap View

- fallback_blocker_rule -> affects: [依赖与降级规则, PASS Evidence] -> action: 补一句依赖失败时如何降级，哪些情况必须直接阻塞。
- pass_evidence -> affects: [PASS Evidence] -> action: 补完整 PASS evidence，证明当前输入不是伪合格 prompt。
- prd_alignment -> affects: [完成后必须结构化回传] -> action: 补 PRD 对照要求，说明对应条目、已满足项和未满足项。
- round_main_closure -> affects: [本轮目标, PASS Evidence] -> action: 补一句 Round main closure，写清本轮唯一主闭环。
- tighter_out_of_scope -> affects: [本轮边界] -> action: 已有边界但仍偏松，需要明确削掉并列主目标。
- why_not_split -> affects: [本轮目标, PASS Evidence] -> action: 补一句 why-not-split，或把当前输入拆成多轮。

## First Fix Order

1. 本轮目标 [critical]
   - suggested_action: 补一句 Round main closure，写清本轮唯一主闭环
   - expected_outcome: 边界、验收和拆轮判断会更容易对齐。
   - stop_condition: 目标收敛成一个单轮主闭环，并包含用户可见结果即可。
   - next_check: 检查本轮目标是否只剩一个主闭环，且有用户可见结果。
   - check_signal: 目标段只剩一个主闭环，且带用户可见结果。
   - reason: 当前 section 有内容，但仍受这些缺口影响：round_main_closure, why_not_split。
2. 依赖与降级规则 [critical]
   - suggested_action: 补一句依赖失败时的 fallback / blocker 处理
   - expected_outcome: 依赖失败时仍会有清晰的降级或阻塞路径。
   - stop_condition: 补出依赖失败时的 fallback / blocker 处理即可。
   - next_check: 检查是否已经写出依赖失败时的 fallback / blocker 路径。
   - check_signal: 已写出 fallback / blocker 处理。
   - reason: 当前 section 有内容，但仍受这些缺口影响：fallback_blocker_rule。
3. PASS Evidence [critical]
   - suggested_action: 补一句 PASS evidence，说明新增主闭环为什么已接近可放行
   - expected_outcome: 继续往下修时会更容易判断何时接近可放行状态。
   - stop_condition: 补出 why-not-split、round main closure 或 fallback/blocker 关键证据即可。
   - next_check: 检查是否已经写出 why-not-split、round main closure 或 fallback/blocker 关键证据。
   - check_signal: 已出现 why-not-split / round main closure / fallback-blocker 关键证据。
   - reason: 当前 section 有内容，但仍受这些缺口影响：pass_evidence, round_main_closure, why_not_split, fallback_blocker_rule。
4. 本轮边界 [important]
   - suggested_action: 把本轮边界收紧到一个主闭环，删掉并列主目标
   - expected_outcome: 这一节继续往下修时会更容易判断是否够用。
   - stop_condition: 出现明确不做边界，并能挡住顺手扩做即可。
   - next_check: 检查这一节是否已达到：出现明确不做边界，并能挡住顺手扩做即可。
   - check_signal: 该段已出现可判断的过线信号。
   - reason: 当前 section 有内容，但仍受这些缺口影响：tighter_out_of_scope。
5. 完成后必须结构化回传 [important]
   - suggested_action: 补一句完成后按 PRD 条目逐项对照回传
   - expected_outcome: 主 agent 收口时会更容易对照结果与 PRD。
   - stop_condition: 补出固定回传结构，并说明如何按 PRD 对照即可。
   - next_check: 检查回传是否包含固定结构，并且有 PRD 对照。
   - check_signal: 回传段已包含固定结构与 PRD 对照。
   - reason: 当前 section 有内容，但仍受这些缺口影响：prd_alignment。

## 任务类型 [filled]

- reason: 当前 section 已有可用内容，可作为 agent 二次收口底稿。
- source_type: source
- 本轮类型：`build`
- 选择原因：`待 agent 根据 PRD 与反馈再确认`

## 当前项目信息 [filled]

- reason: 当前 section 已有可用内容，可作为 agent 二次收口底稿。
- source_type: source
- 项目名：`novel-studio`
- 当前轮次：`round-09`
- 当前阶段：`Build Delegation`
- 当前 PRD 状态：`locked`
- 当前 Gate 状态：`REWRITE_REQUIRED`

## 执行前必读上下文 [filled]

- reason: 当前 section 已有可用内容，可作为 agent 二次收口底稿。
- source_type: inferred
- 必读：`PROJECT_STATE.md`
- 必读：`PRD.md`
- 必读：最近一轮 `PROGRESS.md`
- 必读：最近一轮 `IMPLEMENTATION_NOTES.md`
- 按需补读：`ARCHITECTURE.md` / `CHANGE_PROPOSALS.md` / `TEST_RESULTS.md`

## 本轮目标 [weak]

- reason: 当前 section 有内容，但仍受这些缺口影响：round_main_closure, why_not_split。
- source_type: source
- related_contract_items: round_main_closure, why_not_split
- repair_hints:
  - [critical][add_pass_evidence] 补一句 Round main closure，写清本轮唯一主闭环
  - [critical][tighten_scope] 把本轮目标收成一个新增主闭环，并补一句用户可见结果
- 本轮只解决：把导出 EPUB、续写半章、风格引导、CLI 命令、API 接口和 Web UI 一起补齐
- 这轮完成后，用户可以直接从 CLI、API 和 Web UI 发起续写，并带风格引导，还能导出 EPUB
- 本轮目标来源：`PRD.md` 当前能力建设目标

## 本轮边界 [weak]

- reason: 当前 section 有内容，但仍受这些缺口影响：tighter_out_of_scope。
- source_type: source
- related_contract_items: tighter_out_of_scope
- repair_hints:
  - [important][tighten_scope] 把本轮边界收紧到一个主闭环，删掉并列主目标
  - [important][add_constraint] 补一句强边界，明确排除顺手扩做内容
- 必做：
- 导出 EPUB
- 续写半章
- 风格引导
- CLI 命令
- API 接口
- Web UI
- 不做：
- 无关目录重构
- 文案微调
- 保持不动：
- 现有账户体系

## 验收标准 [filled]

- reason: 当前 section 已有可用内容，可作为 agent 二次收口底稿。
- source_type: source
- 验收项 1：CLI 可以发起续写
- 验收项 2：API 可以发起续写
- 验收项 3：Web UI 可以发起续写
- 验收项 4：支持风格引导
- 验收项 5：支持导出 EPUB

## 依赖与降级规则 [weak]

- reason: 当前 section 有内容，但仍受这些缺口影响：fallback_blocker_rule。
- source_type: source
- related_contract_items: fallback_blocker_rule
- repair_hints:
  - [critical][add_fallback] 补一句依赖失败时的 fallback / blocker 处理
  - [critical][add_fallback] 补一句依赖失败时如何降级，以及哪些情况必须直接阻塞
- 关键依赖：模型接口、导出服务、API 层、前端页面
- 依赖满足时：全部接好
- 依赖不满足时允许的降级方案：请说明
- 哪些情况应直接标记阻塞，不继续扩做：视情况判断

## 测试要求 [filled]

- reason: 当前 section 已有可用内容，可作为 agent 二次收口底稿。
- source_type: source
- 请返回测试入口、操作步骤、测试数据、预期结果、失败判定

## 完成后必须结构化回传 [weak]

- reason: 当前 section 有内容，但仍受这些缺口影响：prd_alignment。
- source_type: source
- related_contract_items: prd_alignment
- repair_hints:
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
  - [critical][add_pass_evidence] 补一句 PASS evidence，说明新增主闭环为什么已接近可放行
- Prompt Gate：`尚未 PASS`
- Delegation contract：`not yet`
- 说明：`当前仍是 skeleton / draft，不应直接派单`
- Round main closure：`待补，需用一句话写清本轮唯一主闭环`
- Why not split：`待补，需说明为什么本轮不拆轮`
- Fallback / blocker rule：`待补，需写清降级边界和直接阻塞条件`
