# Product Dev Loop 工作流

这份文档把 5 阶段写成可直接执行的流程。每个阶段都明确输入、动作、输出和进入下一阶段条件。

## 0. 总原则

- 先探索上下文，再执行
- 每一步都记录，但只记录关键
- 主 agent 负责调度、判断、收口
- 外部执行器负责执行并结构化回传
- `PRD.md` 一旦 `locked`，范围变化只能先走 `CHANGE_PROPOSALS.md`
- 不把执行器长回执直接当项目记录
- 不把执行器自我评价直接当事实
- 用户草稿需求不等于合格派单 prompt
- 需求写得很长，也不等于 prompt 已经收口
- 所有准备进入 `Build Delegation` 的输入，都必须先经过 `Prompt Gate`
- 只有 `Prompt Gate = PASS`，才允许进入正式派单
- `REWRITE_REQUIRED` 和 `CLARIFICATION_REQUIRED` 都禁止直接进入 `Build Delegation`
- 字段齐全，不等于 `Prompt Gate = PASS`
- Gate 后还要检查 `PASS evidence`
- Gate 后先记录，再决定 clarify / rewrite / pass

## 0.1 接手已有项目时先做什么

第一次接手已有项目时，不要先看最新 prompt，也不要先全量扫所有 docs。

先看 `docs/agent_handoff_quickstart.md`，再按下面顺序建立最小上下文：

1. `PROJECT_STATE.md`
2. `PRD.md`
3. `PROGRESS.md`
4. `IMPLEMENTATION_NOTES.md`
5. `ROUND_INDEX.md`
6. `TEST_RESULTS.md`

再根据当前任务目标，进入对应规则文档。

## 0.2 用户只说“继续项目”时先做什么

当用户输入属于“继续项目 / 接手项目 / 跟进项目”这类意图时，不要直接进入 `Build Delegation`。

先进入默认接管协议：

1. 识别项目名 / 项目标识 / 项目目录
2. 如果项目、范围或记录存在关键歧义，先用 `templates/takeover_clarification_template.md` 做最小补问
3. 读取 `docs/agent_handoff_quickstart.md`
4. 读取该项目的：
   - `PROJECT_STATE.md`
   - `PRD.md`
   - `PROGRESS.md`
5. 再按状态补读：
   - `IMPLEMENTATION_NOTES.md`
   - `TEST_RESULTS.md`
   - `TEST_GUIDANCE.md`
   - `ROUND_INDEX.md`
6. 先形成接管摘要
7. 再分流到具体动作：
   - 写 prompt
   - 审回执并更新记录
   - 生成测试说明
   - 判断下一步
   - 进入 `CHANGE_PROPOSALS.md`

原则：

- 先建立最小上下文，再进入具体动作
- 接管优先于直接行动
- 有歧义时先向用户补问，不默认推进
- 一次只补问最影响推进的那个问题

## 0.3 最小接管完成后如何分流

接管摘要出来后，不要靠感觉选下一步。优先看最直接的信号。

### 更适合先写 prompt

当同时满足这些信号时，优先进入 `Build Delegation`：

- 当前项目和范围已明确
- 最近反馈已被判断为继续派单的问题
- 当前最关键未闭环点清楚
- 下一轮能收敛成一个小目标

### 更适合先审回执并更新记录

当同时满足这些信号时，优先进入 `Feedback Capture`：

- 手头已有新的执行器回执
- 项目记录明显滞后
- 当前最缺的是“这轮到底做到了什么”的判断
- 还不能直接写下一轮 prompt

### 更适合先写测试说明

当同时满足这些信号时，优先进入 `Test Guidance`：

- 本轮结果看起来已基本达到目标
- 有可操作测试入口
- 执行器声称已完成，但仍需用户验证
- 当前最缺的是用户可读测试步骤

### 更适合先做下一步判断

当同时满足这些信号时，优先进入阶段判断：

- 最近已有测试结果或用户反馈
- 当前分歧在“接下来该做什么”，而不是“做了什么”
- 需要先决定继续派单、先测试、等确认还是阻塞等待

### 不应直接分流，应该先补问

出现以下任一情况时，先补问：

- 项目不唯一
- 当前范围是否仍沿用不明确
- 当前具体任务目标仍模糊
- 关键记录冲突已经影响下一步判断

## 1. 阶段一：Discovery

### 输入

- 用户的当前想法
- 现有代码或现有项目背景
- 已知约束、参考产品、技术偏好

### 动作

1. 建立项目目录 `projects/<project-name>/`
2. 新建或更新 `DISCOVERY.md`
3. 记录用户目标、核心场景、非目标、风险、待确认问题
4. 识别隐性要求，但先标记为待确认
5. 如果项目是新建项目，同时新建 `PROJECT_STATE.md`

### 输出

- `DISCOVERY.md`
- 初版 `PROJECT_STATE.md`
- 必要时初版 `IMPLICIT_REQUIREMENTS.md`

### 进入下一阶段条件

- 问题定义清楚
- 第一阶段范围清楚
- 暂不做什么清楚
- 影响范围的隐性要求已至少被识别

## 2. 阶段二：PRD

### 输入

- `DISCOVERY.md`
- 当前确认过的用户目标
- 相关约束与已有实现背景

### 动作

1. 生成 `PRD.md`
2. 需要时生成 `ARCHITECTURE.md`
3. 在 `PRD.md` 中写清目标、非目标、验收标准、风险和依赖
4. 在 `PROJECT_STATE.md` 写入当前 `PRD 状态`
5. 用户确认前，PRD 状态保持 `draft`
6. 用户确认后，PRD 状态改为 `locked`

### 输出

- `PRD.md`
- 可选 `ARCHITECTURE.md`
- 更新后的 `PROJECT_STATE.md`

### 进入下一阶段条件

- PRD 已经可执行，不只是方向讨论
- 用户已确认当前轮开发目标
- 当前目标可以拆成一个小步开发任务

## 2.5 Build Delegation 强制入口门：Prompt Gate

这一步不是第六阶段，而是 `Build Delegation` 的强制入口门。

标准分叉必须是：

`Input Intake -> Prompt Gate -> 记录 Gate Result -> PASS / REWRITE_REQUIRED / CLARIFICATION_REQUIRED`

然后再继续：

- `PASS -> scoring -> Build Delegation`
- `REWRITE_REQUIRED -> rewrite -> re-gate`
- `CLARIFICATION_REQUIRED -> 最小补问 -> re-gate`

硬规则：

- 未经 `Prompt Gate PASS`，不得把用户原始任务块视为可直接派给执行器的 round prompt
- `Build Delegation` 只接受已通过 Gate 的 round prompt
- Gate 结果必须结构化输出，不允许只凭脑内判断
- 即使字段齐全，只要仍属于 `pseudo-qualified prompt`，也不得放行
- `Gate Result` 必须落档

### 输入 Intake

- 用户原始任务块
- 已整理输入
- 已收口 round prompt
- 接手后从项目记录中提炼的候选 prompt

### Gate 输入分类

- `qualified round prompt`
- `raw request`
- `ambiguous input`
- `pseudo-qualified prompt`

### 输入

- Input Intake 的候选输入
- `PROJECT_STATE.md`
- `PRD.md`
- 最近一轮 `PROGRESS.md`
- 最近一轮 `IMPLEMENTATION_NOTES.md`

### 动作

1. 先用 `docs/prompt_gate_protocol.md` 判断当前输入属于 `qualified round prompt / raw request / ambiguous input / pseudo-qualified prompt`
2. 用 `templates/prompt_gate_result_template.md` 输出结构化 Gate 结果
3. Gate 至少检查：
   - 项目 / 轮次 / 阶段 / PRD 状态
   - 任务类型是否可稳定归类
   - 是否为单轮最小闭环
   - 是否明确本轮不做
   - 是否有验收标准
   - 是否有依赖 / fallback / blocker 规则
   - 是否有结构化回传
   - 是否有测试要求
   - 是否有 PRD 对照
   - 是否属于 `pseudo-qualified prompt`
   - 是否具备 `PASS evidence`
4. 如果项目不唯一、当前轮次不清楚、PRD 状态不清楚或关键冲突未解，给 `CLARIFICATION_REQUIRED`
5. 如果输入仍是 raw request、命中一票否决项、多主闭环混合，或属于 `pseudo-qualified prompt`，给 `REWRITE_REQUIRED`
6. 如果同时出现多个核心能力主题、多个交付入口、依赖接入与实现混合、功能与优化混合，默认按 `docs/round_split_decision_guide.md` 建议拆轮
7. 如果 `PRD.md` 已 `locked` 且当前输入包含范围变化，禁止直接进入 `Build Delegation`；应进入 `CHANGE_PROPOSALS.md`，或先收缩目标
8. 即使 Gate 初判为 `PASS`，仍要检查 `PASS evidence`
9. 只有 Gate 结果为 `PASS`、`PASS evidence` 成立，且满足 `docs/build_delegation_input_contract.md`，才允许进入正式 `Build Delegation`
10. Gate 结果统一记录到 `projects/<project>/PROMPTS/GATE_RESULTS.md`

### Gate 输出状态

- `PASS`
- `REWRITE_REQUIRED`
- `CLARIFICATION_REQUIRED`

### 输出

- 一份结构化 `Prompt Gate Result`
- 更新后的 `projects/<project>/PROMPTS/GATE_RESULTS.md`
- 一次 Gate 落档记录
- 或 rewrite 任务
- 或最小补问
- 或拆轮建议
- 或进入 `CHANGE_PROPOSALS.md` / `阻塞等待` 的判断

### 进入下一阶段条件

- Gate 结果为 `PASS`
- `PASS evidence` 成立
- 输入满足 `Build Delegation` 输入契约
- prompt 已具备可派发条件

### 非 PASS 时的后续动作

#### `REWRITE_REQUIRED`

- 先落档
- 进入 `prompt rewrite`
- rewrite 后重新过 Gate
- re-gate 后再次落档
- 未重新拿到 `PASS` 前，不进入 `Build Delegation`

#### `CLARIFICATION_REQUIRED`

- 先落档
- 只允许最小补问
- 补问只针对当前最阻塞推进的那个问题
- 只问一个问题，不连环追问
- 记录这个最小补问
- 用户给出最短回复后先记录回复
- 拿到澄清后重新过 Gate
- re-gate 后再次落档
- 未重新拿到 `PASS` 前，不进入 `Build Delegation`

## 3. 阶段三：Build Delegation

### 输入

- `PROJECT_STATE.md`
- `PRD.md`
- 最近一轮 `PROGRESS.md`
- 最近一轮 `IMPLEMENTATION_NOTES.md`
- `Prompt Gate Result = PASS`
- 明确 `PASS evidence`
- 满足 `docs/build_delegation_input_contract.md` 的 round prompt
- 按需补读 `ARCHITECTURE.md`、`CHANGE_PROPOSALS.md`、`IMPLICIT_REQUIREMENTS.md`、`DECISIONS.md`

### 动作

1. 主 agent 先检查上下文是否完整、是否冲突
2. 先确认输入已经拿到 `Prompt Gate = PASS`
3. 再确认 `PASS evidence` 成立，而不是只长得像标准 prompt
4. 再确认输入满足 `docs/build_delegation_input_contract.md`
5. 如果 Gate 结果不是 `PASS`，或 `PASS evidence` 不成立，立即停止，不继续派单
6. 判断当前轮最适合推进什么，优先处理最影响闭环的一件事
7. 先判断本轮任务类型是 `build`、`fix`、`polish` 还是 `unblock`
8. 把本轮目标收敛成一个清楚的小任务
9. 生成的是“合格的收口型 prompt”，不是普通需求描述
10. 生成 `PROMPTS/round-xx-build.txt`
11. 在提示词里明确：
   - 任务类型
   - 当前项目信息
   - 当前轮次
   - 当前阶段
   - 当前 PRD 状态
   - 执行前必读上下文
   - 当前目标
   - 本轮边界
   - 验收标准
   - 依赖 / 降级规则
   - 不要扩散
   - 测试要求
   - PRD 对照要求
   - 新需求与隐性要求处理规则
   - `PASS evidence`
12. 根据任务类型补强重点：
   - `build`：写最小闭环、关键数据流和验收边界
   - `fix`：写复现现象、修复目标、回归风险和修后验证
   - `polish`：写可动范围和不可动范围，防止借机重构
   - `unblock`：写阻塞点、解阻目标、临时方案与正式方案
13. 明确要求外部执行器返回结构化结果：
   - 已完成
   - 未完成
   - 关键文件
   - 关键逻辑
   - `stub / mock / 假数据 / 隐藏入口 / 未接线`
   - 测试建议
   - 与 PRD 不一致处
14. 在输出前先确认 Gate 结果没有失效，`PASS evidence` 仍成立，输入仍满足 `Build Delegation` 输入契约
15. 再用 `templates/prompt_quality_checklist.md` 自检，确认它不是“只有功能描述的普通需求文案”
16. 再按评分规约判断：
   - 是否低于最低标准
   - 是否只是“仅及格”
   - 是否已达到“可直接发”

这里的判断标准是：

- 普通需求描述只是在说“想做什么”
- 合格的收口型 prompt 必须把“这轮做什么、这轮不做什么、怎样算完成、做完必须怎么回传”一起写清楚
- 更稳的收口型 prompt 还会写清任务类型、类型特有风险、依赖 / 降级规则，以及收到什么反馈时应该停下来而不是继续扩功能
- 如果输入仍像功能清单、issue 池或 TODO 打包，就说明 Gate 不应给 `PASS`
- 如果输入只是字段齐全、格式正规，但仍是多主闭环或没有有效 `PASS evidence`，也不应给 `PASS`
- 只有 `PASS` 输入才有资格被当成 `Build Delegation` 输入

### 输出

- `PROMPTS/round-xx-build.txt`
- 本轮派单记录

### 进入下一阶段条件

- 已拿到开发结果或清楚的实现回执
- 回执能够被压缩为结构化记录

## 4. 阶段四：Test Guidance

### 输入

- 本轮开发回执
- 当前 PRD 验收标准
- 当前可测试入口

### 动作

1. 生成或更新 `TEST_GUIDANCE.md`
2. 写明：
   - 本轮重点验证项
   - 测试入口
   - 测试前提
   - 操作步骤
   - 测试数据
   - 预期结果
   - 失败判定
3. 如果执行器只是声称“已完成”，但证据不足，要明确标为“需重点验证”
4. 如果有已知限制、环境要求、隐藏入口、`stub / mock / 假数据 / 未接线`，也要明确写出
5. 测试描述必须让用户可以直接按步骤执行，而不是看代码说明

### 输出

- `TEST_GUIDANCE.md`

### 进入下一阶段条件

- 已拿到测试结果
- 或已拿到用户体验反馈
- 或已明确当前阻塞点

## 5. 阶段五：Feedback Capture

### 输入

- 开发回执
- `TEST_GUIDANCE.md`
- 用户测试结果或反馈
- `PRD.md`

### 动作

1. 先把执行器长回执压缩成关键事实，不直接照抄原文
2. 把实现事实、关键文件、风险和特殊状态写入 `IMPLEMENTATION_NOTES.md`
3. 在 `PROGRESS.md` 写一段 1 到 2 句短摘要
4. 对照 PRD 判断：
   - 已完成什么
   - 未完成什么
   - 是否闭环
   - 是否存在 `stub / mock / 假数据 / 隐藏入口 / 未接线`
5. 从回执里提炼用户现在最需要验证的测试点，生成或更新 `TEST_GUIDANCE.md`
6. 再判断当前更适合：
   - 继续派单
   - 进入用户测试
   - 等待用户确认
   - 阻塞等待外部条件
   - 进入 `CHANGE_PROPOSALS.md`
   - 进入下一阶段
7. 在 `PROJECT_STATE.md` 更新当前阶段、当前结论、阻塞和下一步
8. 如果出现范围变化，先写 `CHANGE_PROPOSALS.md`
9. 如果确认了新的隐性要求，写 `IMPLICIT_REQUIREMENTS.md`
10. 只有在反馈被判断为可继续执行的实现问题后，才生成下一轮提示词

补充判断：

- 如果当前最缺的是“这轮到底做到了什么”，先不要写 prompt，先压缩回执
- 如果当前最缺的是“用户怎么测”，先不要继续派单，先写测试说明
- 如果当前最缺的是“现在该不该继续”，先做阶段判断，再决定是否派单

### 输出

- `IMPLEMENTATION_NOTES.md`
- `PROGRESS.md`
- `TEST_GUIDANCE.md`
- `PROJECT_STATE.md`
- 按需更新 `CHANGE_PROPOSALS.md`
- 按需更新 `IMPLICIT_REQUIREMENTS.md`
- 按需生成下一轮 `PROMPTS/`

### 进入下一轮条件

- 下一轮目标已经清楚
- 已知当前是 `通过`、`继续修改` 还是 `阻塞等待`

## 6. 结论判断方式

每轮反馈后必须在 `PROJECT_STATE.md` 或 `PROGRESS.md` 明确写出以下三种结论之一：

- `通过`
  - 当前轮目标达到 PRD 验收标准
  - 没有阻断当前轮闭环的未完成项
- `继续修改`
  - 当前轮有价值产出，但还未达到 PRD 验收标准
  - 仍有未完成项、stub、mock、假数据、隐藏入口或未接线问题
- `阻塞等待`
  - 当前无法继续推进
  - 原因可能是需求不清、依赖缺失、环境问题、用户待决策

## 7. 测试反馈如何进入下一轮

测试完成后，不要只写“测过了”。

必须把测试反馈转成下一轮输入：

1. 把用户反馈写进 `IMPLEMENTATION_NOTES.md`
2. 判断它属于哪一类：
   - 实现缺陷
   - 验收未达标
   - 新需求
   - 隐性偏好
   - 环境阻塞
3. 如果是实现缺陷或验收未达标，进入下一轮 `Build Delegation`
4. 如果是新需求，先进 `CHANGE_PROPOSALS.md`
5. 如果是隐性偏好，先确认，再进 `IMPLICIT_REQUIREMENTS.md`
6. 如果是外部阻塞，优先判断是否写成 `unblock`，还是直接 `阻塞等待`
7. 如果当前已经达到本轮目标，不继续扩功能，先进入测试或下一阶段
8. 更新 `PROJECT_STATE.md` 的下一步建议

## 8. 执行器回执如何压缩成不同文件

主 agent 收到回执后，应按用途拆写：

- `PROGRESS.md`：只写 1 到 2 句最关键进展
- `IMPLEMENTATION_NOTES.md`：写实现事实、关键文件、风险、特殊状态
- `TEST_GUIDANCE.md`：写用户可读测试说明
- `TEST_RESULTS.md`：写实际测到的问题和通过情况
- `PROJECT_STATE.md`：写当前阶段、当前结论、阻塞和下一步

不要把任何单个文件写成“全量收容器”。

## 9. 隐性要求的识别、确认、落档

隐性要求常见信号：

- 用户多次重复某个判断标准
- 用户强调“默认应该这样”
- 用户对交互、视觉、路径、风格有稳定偏好，但没有写进 PRD

处理方式：

1. 先标记为“待确认”
2. 向用户确认是否作为稳定要求
3. 确认后写入 `IMPLICIT_REQUIREMENTS.md`
4. 如果它会改变范围或验收标准，同时写进 `CHANGE_PROPOSALS.md`
5. 只有在用户明确同意需求变更后，才允许回写 `PRD.md`

## 10. PRD locked 后如何处理变更建议

当 `PRD.md` 已经 `locked` 时：

1. 不直接改 `PRD.md`
2. 在 `CHANGE_PROPOSALS.md` 新增一条变更提议
3. 写清：
   - 变更内容
   - 变更原因
   - 影响范围
   - 风险
   - 是否影响验收标准
4. 等用户明确同意
5. 同意后再修改 `PRD.md`，并在 `DECISIONS.md` 记录这次决策

## 11. 最小项目文件建议

一个可运行的项目最少维护这些文件：

- `PRD.md`
- `PROJECT_STATE.md`
- `PROGRESS.md`
- `IMPLEMENTATION_NOTES.md`
- `CHANGE_PROPOSALS.md`
- `IMPLICIT_REQUIREMENTS.md`
- `DECISIONS.md`
- `TEST_GUIDANCE.md`
- `TEST_RESULTS.md`
- `PROMPTS/`
