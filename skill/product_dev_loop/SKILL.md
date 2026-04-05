---
name: product_dev_loop
description: 用于把产品想法推进成真实项目闭环。先做需求共创，再沉淀 PRD 与架构，再派单给 Cursor、Claude Code 或 Codex 开发，并在每轮开发后留下测试指引、反馈判断、变更提议和下一步建议。支持多项目并行，要求 PRD locked 后不得擅改，每一步都记录，但只记录关键。
---

# Product Dev Loop

这个 skill 用于把“想法讨论”推进成“可执行项目闭环”。

第一次接手这个 skill 时，先读 `docs/agent_handoff_quickstart.md`。

如果用户只说“继续项目 X / 接手项目 X / 跟进项目 X”，默认先执行 `docs/default_takeover_protocol.md`，而不是直接开始写 prompt 或改文档。

如果用户只说：
- `继续`
- `继续某项目`
- `给我某项目下一步`
- `继续喂 Cursor`

默认不要靠感觉自由发挥。先读 `docs/default_collaboration_rules.md`，按其中的默认触发语句、输入分流规则、tool 调用规则、记录策略和最终输出协议执行。

核心目标不是写漂亮文档，而是稳定推进以下链路：

`Discovery -> PRD -> Build Delegation -> Test Guidance -> Feedback Capture`

这个 skill 不只是管理文档，也负责把“开发派单 prompt”收口成真正可执行、可验收、可回传的版本。

这里新增一个正式强制入口门：

- 所有准备进入 `Build Delegation` 的输入，都必须先过 `Prompt Gate`
- 只有 `Prompt Gate = PASS`，才允许进入正式 `Build Delegation`
- `REWRITE_REQUIRED` 和 `CLARIFICATION_REQUIRED` 都禁止直接派单
- 未经 `Prompt Gate PASS`，不得把用户原始任务块视为可直接派给执行器的 round prompt
- 字段齐全，不等于 `Prompt Gate PASS`
- 最终 delegation prompt 需要明确 `PASS evidence`
- `Prompt Gate Result` 不是只在脑内判断，应有落档动作
- `CLARIFICATION_REQUIRED` 默认只问一个最小阻塞问题
- `Prompt Gate Result` 的 canonical 落档位置是 `projects/<project>/PROMPTS/GATE_RESULTS.md`

同样重要的是：当外部执行器已经返回一大段实现说明后，这个 skill 还要负责把回执压缩成关键记录、判断当前阶段、生成用户可读测试说明，并给出下一步建议。

## 适用场景

- 用户只有模糊想法，需要一起把范围说清楚
- 用户需要先锁定 PRD，再把任务派给开发工具
- 用户需要每轮开发后都能拿到测试指引和 PRD 对照判断
- 用户同时推进多个项目，需要独立目录和独立文档

## 首次接手入口

如果你是第一次进入这个 skill，不要先把所有 docs 从头读到尾。

推荐入口：

1. 先读 `docs/agent_handoff_quickstart.md`
2. 再读 `SKILL.md`
3. 再读 `docs/workflow.md`
4. 再读 `docs/default_collaboration_rules.md`
5. 然后按任务目标选择阅读路径

这样能最快接上当前上下文，而不是重新摸索文档结构。

## 默认接管协议

这个 skill 的默认姿势不是“直接干活”，而是“先判断再推进”。

具体来说：

- 当用户只表达“继续某个项目”时，默认先触发接管协议
- 接管协议优先于直接行动
- 如果用户已经指定更细任务，也要先做最小接管，再进入该任务
- 如果项目或范围存在歧义，先用 `templates/takeover_clarification_template.md` 做最小补问，再继续接管

默认最小接管至少包括：

1. `docs/agent_handoff_quickstart.md`
2. `projects/<project>/PROJECT_STATE.md`
3. `projects/<project>/PRD.md`
4. `projects/<project>/PROGRESS.md`

必要时再补读：

- `IMPLEMENTATION_NOTES.md`
- `TEST_RESULTS.md`
- `TEST_GUIDANCE.md`
- `ROUND_INDEX.md`

接管后第一轮默认先输出结构化接管摘要，而不是直接写下一轮开发 prompt。

最小接管完成后，再按信号分流：

- 当前目标和缺口明确，进入具体动作
- 当前项目或范围仍不清楚，先补问
- 当前记录存在关键冲突，先说明冲突再判断下一步

默认分流优先看这几个问题：

1. 现在缺的是开发 prompt，还是缺对已有回执的判断
2. 现在更需要用户测试说明，还是更需要下一步决策
3. 有没有信息不足到不能安全推进

默认输入分流的正式规则固定为 4 类：
- 新需求 / 原始需求
- Cursor / Codex 回执
- 用户测试反馈
- 外部阻塞说明

每类输入默认动作、是否调用 `product_dev_loop_tool`、最终输出如何收敛，都以 `docs/default_collaboration_rules.md` 为准。

## 三层视角

这个 skill 固定用 5 个阶段推进，同时要用三层视角理解流程：

- `计划层`：`Discovery` + `PRD`
- `执行层`：`Build Delegation`
- `反馈层`：`Test Guidance` + `Feedback Capture`

约束：

- 计划层没有收敛，不进入执行层
- 执行层没有明确结果，不进入反馈层
- 反馈层没有形成判断，不直接开始下一轮

补充约束：

- `Prompt Gate` 不是新阶段
- 它是 `Build Delegation` 的正式强制入口门
- `Prompt Gate` 先判断输入属于 `qualified round prompt / raw request / ambiguous input / pseudo-qualified prompt`
- 只有 `Prompt Gate = PASS`，才允许进入 `Build Delegation`
- 用户草稿需求和含糊输入都不能绕过这层
- `pseudo-qualified prompt` 也不能绕过这层

## 固定 5 阶段

1. `Discovery`
2. `PRD`
3. `Build Delegation`
4. `Test Guidance`
5. `Feedback Capture`

没有上一步产物时，不跳阶段。

## 提示词收口职责

`product_dev_loop` 不只是提供静态模板，也负责引导生成高质量开发 prompt。

在 `Build Delegation` 阶段，目标不是写一段“功能需求描述”，而是生成合格的收口型派单 prompt。

进入 `Build Delegation` 前，先按这四类输入分流：

- `qualified round prompt`：进入 `Prompt Gate`，争取直接 `PASS`
- `raw request`：进入 `Prompt Gate`，通常得到 `REWRITE_REQUIRED`
- `ambiguous input`：进入 `Prompt Gate`，通常得到 `CLARIFICATION_REQUIRED`
- `pseudo-qualified prompt`：进入 `Prompt Gate`，通常继续判 `REWRITE_REQUIRED`

先做 Gate，再决定：

- 是否可以直接进入 prompt scoring
- 是否必须先 rewrite
- 是否只能先做最小补问
- 是否只是 `pseudo-qualified prompt`
- 是否已经具备 `PASS evidence`
- Gate 结果应该如何落档

如果当前输入还只是：

- 功能清单
- issue 列表
- 用户口述的一段需求块
- 多模块打包需求
- 带文件路径但缺边界的任务说明
- 带命令 / API / UI 要求但没有验收和回传的开发单

先不要把它当合格 prompt，也不要默认它能进入 `Build Delegation`。

先读：

- `docs/prompt_gate_protocol.md`
- `docs/prompt_gate_result_logging_guide.md`
- `docs/pseudo_qualified_prompt_detection_guide.md`
- `docs/raw_request_to_round_prompt_guide.md`
- `docs/raw_prompt_defect_checklist.md`
- `docs/round_split_decision_guide.md`
- `docs/build_delegation_input_contract.md`

再用：

- `templates/prompt_gate_result_template.md`
- `templates/prompt_gate_result_log_entry_template.md`
- `templates/clarification_min_question_template.md`
- `templates/prompt_pass_evidence_block.txt`
- `templates/round_prompt_rewrite_template.txt`

先产出 Gate 结果，再决定 rewrite / clarify / prompt generation。

生成 prompt 时必须走这个过程：

1. 先做 `Prompt Gate`
2. 先产出结构化 Gate 结果
3. 先把 Gate 结果落档
4. 如果是 `CLARIFICATION_REQUIRED`，只做一个最小补问
5. 如果是 `REWRITE_REQUIRED`，先 rewrite，必要时默认建议拆轮
6. clarification 或 rewrite 后重新过 Gate
7. re-gate 后继续落档
8. Gate 初判为 `PASS` 后，还要检查 `PASS evidence`
9. 只有 Gate `PASS` 且 `PASS evidence` 成立后，才进入 prompt scoring
10. 先读上下文
11. 先判断任务类型
12. 收敛目标
13. 划边界
14. 写验收
15. 写依赖与降级规则
16. 写回传
17. 写测试
18. 写 PRD 对照
19. 写 `PASS evidence`
20. 做发出前打分

如果做不到以上 20 步，即使已经写了功能描述，也不算合格 prompt。

## 从 Claude Code 吸收并固化的机制

这里吸收的是机制，不是原文照搬。重点参考了 `projectOnboardingState.ts`、`toolUseSummaryGenerator.ts`、`agentSummary.ts` 这类思路：先确认项目已具备最小上下文，再要求短而结构化的进度摘要，最后由主控统一收口。

### 1. 派单前必须先探索上下文

进入 `Build Delegation` 前，主 agent 必须至少先读这些文件：

- `PROJECT_STATE.md`
- `PRD.md`
- 最近一轮 `PROGRESS.md`
- 最近一轮 `IMPLEMENTATION_NOTES.md`

按需补读这些文件：

- `ARCHITECTURE.md`
- `CHANGE_PROPOSALS.md`
- `IMPLICIT_REQUIREMENTS.md`
- `DECISIONS.md`

如果这些基础上下文不存在或互相冲突，不要直接派单，先回到 `Discovery` 或补文档。

### 2. 主 agent 负责调度、判断、收口

主 agent 负责：

- 判断当前项目处于哪一阶段
- 检查是否具备进入下一阶段的输入
- 把 PRD 拆成当前轮的小目标
- 生成给外部执行器的收口型提示词
- 把外部执行器回执压缩成关键记录
- 对照 PRD 做结果判断
- 决定本轮结论是 `通过`、`继续修改` 还是 `阻塞等待`

外部执行器不负责最终判断，只负责执行与结构化回传。

这里特别强调：

- 普通需求描述不等于可执行 prompt
- 用户草稿需求不等于合格派单 prompt
- 需求写得很长，不等于 prompt 已经合格
- 字段齐全，不等于 prompt 已经通过 Gate
- `Prompt Gate` 的职责是判断输入能否直接进入 `Build Delegation`
- 未 `PASS` 的输入禁止进入 `Build Delegation`
- 合格 prompt 必须同时包含目标、边界、验收、结构化回传、测试建议和 PRD 对照要求
- 如果原始草稿过大，还必须先拆分或定义本轮最低闭环
- 如果需求中存在依赖不确定项，还必须显式补降级规则
- 如果多主闭环混合，默认 `REWRITE_REQUIRED` 并建议拆轮
- 如果输入只是“像标准 prompt”，但仍是多主闭环或没有 `PASS evidence`，也应继续判 `REWRITE_REQUIRED`
- 最终可派单 prompt 必须能明确说明 `Round main closure / Why not split / Fallback or blocker / Delegation contract`
- 合格 prompt 还必须先判断任务类型，并在发出前确认质量分数达到最低标准

### 3. 外部执行器返回必须结构化

外部执行器返回中必须至少包含：

- 已完成
- 未完成
- 关键文件路径
- 关键文件职责
- 关键函数、组件、接口或逻辑点
- `stub / mock / 假数据 / 隐藏入口 / 未接线`
- 测试建议
- 与 PRD 不一致处

不要把整段原始过程原样存入长期文档。

### 3.1 回执不是直接存档，而是按用途压缩

主 agent 看到执行器长回执后，必须先拆成不同用途：

- `PROGRESS.md`：只保留 1 到 2 句最关键进展
- `IMPLEMENTATION_NOTES.md`：保留实现事实、关键文件、风险和特殊状态
- `TEST_GUIDANCE.md`：转成用户可读测试说明
- `TEST_RESULTS.md`：记录实际测试结果与问题分类
- `PROJECT_STATE.md`：只更新当前阶段、当前结论、阻塞和下一步

不要把长回执整段复制到任何长期文档。

### 3.2 不把执行器自我评价直接当事实

执行器常会说：

- “应该已经完成”
- “理论上可用”
- “大体没问题”

这些话不能直接当结论写入项目记录。

主 agent 要尽量改写成：

- 已确认事实
- 待验证点
- 待确认推测

如果证据不足，应明确标记 `待验证`，而不是假装闭环。

### 4. 每轮都要有短摘要，但只保留关键

每轮在 `PROGRESS.md` 里都要写 1 到 2 句短摘要，像工具摘要一样，快速回答：

- 这轮主要做了什么
- 当前最重要的未完成点是什么

长期文档只保留：

- 关键结论
- 关键文件
- 关键逻辑
- 风险
- 未完成项
- PRD 对照判断

不保留大段聊天全文、完整工具日志或冗长过程复述。

### 4.1 用户可读测试说明必须单独生成

测试说明的目标读者不是开发者，而是产品、老板或测试者。

所以 `TEST_GUIDANCE.md` 必须优先写：

- 测试入口
- 测试前提
- 操作步骤
- 测试数据
- 预期结果
- 失败判定
- 已知限制
- 本轮重点验证项

不要把测试说明写成代码说明或 debug 清单。

### 5. 范围变化只能走变更提议

如果开发过程中发现范围变化：

- 不得直接修改已锁定的 `PRD.md`
- 先写入 `CHANGE_PROPOSALS.md`
- 写清原因、影响、建议方案
- 等用户明确同意后，才能回写 PRD

### 6. 反馈必须能转成下一轮 prompt 判断

测试反馈、执行器回执和用户反馈，不应直接堆进下一轮 prompt。

主 agent 必须先判断它属于哪一类：

- 功能未完成
- 功能已实现但未接线
- 只有 UI 壳子，没有真实逻辑
- 逻辑已接但数据未落地
- 主路径可用，但边界条件失败
- 实现与 PRD 不一致
- 新增需求
- 隐性偏好
- 外部阻塞
- 已满足本轮目标

只有判断清楚，下一轮 prompt 才不会写散。

### 7. 反馈收口后，还要判断阶段切换

`Feedback Capture` 不等于“继续派单”。

主 agent 在压缩回执后，还必须判断当前更适合：

- 继续派单
- 进入用户测试
- 等待用户确认
- 阻塞等待外部条件
- 进入 `CHANGE_PROPOSALS.md`
- 进入下一阶段

这个判断要写进 `PROJECT_STATE.md` 和下一步建议里，而不是只留在脑内。

## PRD 锁定规则

- `PRD.md` 初始状态是 `draft`
- 用户确认后改为 `locked`
- `locked` 后不得擅改
- 新需求、需求偏移、验收标准变化都先进入 `CHANGE_PROPOSALS.md`

## 隐性要求规则

如果发现用户存在隐性要求、重复出现的偏好或没明说但反复强调的判断标准：

- 先确认
- 确认后单独写进 `IMPLICIT_REQUIREMENTS.md`
- 不直接混入已锁定 PRD
- 如果它会改变范围或验收标准，先进入 `CHANGE_PROPOSALS.md`

## 多项目支持规则

这个 skill 明确支持多个项目并行，但每个项目必须完全隔离：

- 每个项目独立目录
- 每个项目独立 `PRD.md`
- 每个项目独立 `PROJECT_STATE.md`
- 每个项目独立 `PROGRESS.md`
- 每个项目独立 `IMPLEMENTATION_NOTES.md`
- 每个项目独立 `TEST_GUIDANCE.md`
- 每个项目独立 `TEST_RESULTS.md`
- 每个项目独立 `CHANGE_PROPOSALS.md`
- 每个项目独立 `IMPLICIT_REQUIREMENTS.md`
- 每个项目独立 `DECISIONS.md`
- 每个项目独立 `PROMPTS/`

默认记录的最小粒度：

- `ROUND_INDEX.md`：只更新轮次、类型、目标、状态
- `PROGRESS.md`：只写本轮关键进展和最重要未完成点
- `PROJECT_STATE.md`：只写当前阶段、当前结论、阻塞和下一步
- `PROMPTS/GATE_RESULTS.md`：只记每次 Gate / re-gate 的结果摘要

推荐结构：

```text
projects/
  project-a/
    PRD.md
    PROJECT_STATE.md
    PROGRESS.md
    IMPLEMENTATION_NOTES.md
    CHANGE_PROPOSALS.md
    IMPLICIT_REQUIREMENTS.md
    DECISIONS.md
    TEST_GUIDANCE.md
    TEST_RESULTS.md
    PROMPTS/
  project-b/
    ...
```

## 每一步都记录，但只记录关键

每一步都要记，但只记关键，不堆全文：

- 当前阶段
- 本轮目标
- 关键结论
- 关键文件
- 关键逻辑
- 未完成项
- 风险
- 测试方式
- 是否符合 PRD
- 下一步建议

## 推荐执行顺序

1. 先在 `projects/<project-name>/` 建目录
2. 用 `discovery_template.md` 记录需求与疑问
3. 用 `prd_template.md` 写第一版 PRD
4. 用户确认后把 PRD 状态改为 `locked`
5. 先读 `docs/prompt_gate_protocol.md`
6. 读 `docs/pseudo_qualified_prompt_detection_guide.md`，确认当前输入是不是“字段齐全但仍未通过 Gate”的伪合格 prompt
7. 用 `templates/prompt_gate_result_template.md` 产出 Gate 结果
8. 如果 Gate = `CLARIFICATION_REQUIRED`，只做最小补问，拿到信息后重新过 Gate
9. 如果 Gate = `REWRITE_REQUIRED`，先读 `docs/raw_request_to_round_prompt_guide.md`
10. 用 `docs/raw_prompt_defect_checklist.md` 判断它为什么不能直接派单
11. 用 `docs/round_split_decision_guide.md` 判断是否默认建议拆轮
12. 用 `templates/round_prompt_rewrite_template.txt` 先做 rewrite
13. rewrite 完成后重新过 Gate
14. 如果 Gate 初判为 `PASS`，再用 `templates/prompt_pass_evidence_block.txt` 检查 `PASS evidence`
15. 只有 Gate = `PASS` 且 `PASS evidence` 成立，才读取 `docs/build_delegation_input_contract.md` 并进入 `Build Delegation`
16. 再用 `docs/task_type_prompt_guide.md` 判断本轮属于 `build / fix / polish / unblock`
17. 再按 `docs/prompt_generation_flow.md` 收敛 prompt，并用 `prompt_quality_checklist.md` 自检
18. 按 `docs/prompt_scoring_rubric.md` 打分，低于最低标准时不要直接发
19. 用 `cursor_prompt_template.txt` 或 round prompt 模板派发当前轮开发任务
20. 外部执行器回执回来后，先按 `docs/implementation_feedback_compression_guide.md` 压缩记录
21. 用 `test_guidance_template.md` 和 `docs/test_guidance_generation_guide.md` 生成用户可读测试说明
22. 用 `implementation_capture_template.md` 和 `progress_template.md` 收口
23. 用 `docs/stage_transition_decision_card.md` 判断当前该继续派单、先测试、先确认还是阻塞等待
24. 用 `docs/feedback_to_prompt_mapping.md` 把反馈转成下一轮判断
25. 如果有范围变化，用 `change_proposal_template.md`
26. 如果有新确认的隐性要求，用 `implicit_requirements_template.md`

## 模板清单

- `docs/agent_handoff_quickstart.md`
- `docs/default_takeover_protocol.md`
- `docs/workflow.md`
- `docs/prompt_gate_protocol.md`
- `docs/prompt_gate_result_logging_guide.md`
- `docs/pseudo_qualified_prompt_detection_guide.md`
- `docs/prompt_generation_guide.md`
- `docs/prompt_generation_flow.md`
- `docs/raw_request_to_round_prompt_guide.md`
- `docs/raw_prompt_defect_checklist.md`
- `docs/round_split_decision_guide.md`
- `docs/build_delegation_input_contract.md`
- `docs/task_type_prompt_guide.md`
- `docs/feedback_to_prompt_mapping.md`
- `docs/prompt_scoring_rubric.md`
- `docs/implementation_feedback_compression_guide.md`
- `docs/stage_transition_decision_card.md`
- `docs/test_guidance_generation_guide.md`
- `templates/discovery_template.md`
- `templates/prd_template.md`
- `templates/architecture_template.md`
- `templates/test_guidance_template.md`
- `templates/implementation_capture_template.md`
- `templates/change_proposal_template.md`
- `templates/project_state_template.md`
- `templates/progress_template.md`
- `templates/next_step_template.md`
- `templates/implicit_requirements_template.md`
- `templates/decisions_template.md`
- `templates/cursor_prompt_template.txt`
- `templates/takeover_summary_template.md`
- `templates/round_prompt_template.txt`
- `templates/round_prompt_guided_template.txt`
- `templates/round_prompt_by_type_template.txt`
- `templates/prompt_gate_result_template.md`
- `templates/prompt_gate_result_log_entry_template.md`
- `templates/clarification_min_question_template.md`
- `templates/prompt_pass_evidence_block.txt`
- `templates/round_prompt_rewrite_template.txt`
- `templates/prompt_quality_checklist.md`
- `templates/round_record_template.md`
- `examples/prompt_bad_example.txt`
- `examples/prompt_good_example.txt`
- `examples/raw_request_bad_example.txt`
- `examples/raw_request_fixed_example.txt`
- `examples/raw_request_to_round_prompt_example.md`
- `examples/prompt_gate_split_example.md`
- `examples/pseudo_qualified_prompt_bad_example.txt`
- `examples/pseudo_qualified_prompt_analysis_example.md`
- `examples/clarification_required_example.md`
- `examples/prompt_build_example.txt`
- `examples/prompt_fix_example.txt`
- `examples/prompt_polish_example.txt`
- `examples/prompt_unblock_example.txt`
- `examples/feedback_to_next_round_prompt_example.md`
- `examples/feedback_compression_example.md`
- `examples/test_guidance_from_feedback_example.md`
- `examples/next_step_decision_example.md`
- `examples/agent_handoff_example.md`
- `examples/default_takeover_example.md`

## 不要这样做

- 不要跳过上下文检查直接派单
- 不要把普通功能描述当成合格 prompt 发出去
- 不要把用户草稿需求原样发给执行器
- 不要把需求写得很长误判成“已经是合格 prompt”
- 不要跳过 `Prompt Gate`
- 不要在 Gate 结果是 `REWRITE_REQUIRED` 或 `CLARIFICATION_REQUIRED` 时继续派单
- 不要因为字段看起来齐全，就把伪合格 prompt 误判成 `PASS`
- 不要让多个项目共用一份 PRD
- 不要把未确认偏好直接写进 PRD
- 不要在 `locked` 后直接改 PRD
- 不要只写“做了什么”，不判断“是否符合 PRD”
- 不要让用户在没有测试入口和预期结果时盲测
- 不要把执行器原话大段抄进 `PROGRESS.md`、`IMPLEMENTATION_NOTES.md` 或 `PROJECT_STATE.md`
- 不要把执行器的“应该完成了”直接当成事实
- 不要把工具长输出整段塞进长期文档
