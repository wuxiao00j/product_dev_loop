# Agent Handoff Quickstart

这是一张给“第一次接手 `product_dev_loop` 的 agent”用的接管导航卡。

目标只有一个：

- 用尽量短的时间接上当前上下文
- 不重新摸索整套文档结构
- 不犯串项目、串范围、误判闭环的低级错误

## 一句话定位

`product_dev_loop` 用来把一个项目从需求、PRD、开发派单、测试说明、反馈收口一路推进成可判断、可继续迭代的闭环。

默认动作不是“直接干活”，而是“先接管，再判断，再推进”。

如果接管时出现项目歧义、范围歧义或关键记录冲突，先用 `templates/takeover_clarification_template.md` 做最小补问。

## 默认接管触发

如果用户只说：

- 继续项目 X
- 接手项目 X
- 跟进项目 X
- 看看项目 X 现在到哪了

默认先走 `docs/default_takeover_protocol.md`，不要直接开始写下一轮 prompt。

## 先记住的 5 条硬规则

1. `PRD.md` 已 `locked` 后不得擅改；范围变化先走 `CHANGE_PROPOSALS.md`
2. 多项目必须隔离；任何判断都只基于当前项目目录
3. 每轮都要有测试指引和 PRD 对照
4. 不把执行器“已完成”“理论上可用”直接当事实
5. 记录只记关键，不照抄长回执，不把项目未完成误判成本轮未完成

## 当前 skill 的核心能力模块

- `Prompt 收口`：把开发 prompt 写成可执行、可验收、可回传的版本
- `任务类型判断`：区分 `build / fix / polish / unblock`
- `反馈映射`：把测试反馈或回执转成下一轮动作判断
- `回执压缩`：把长回执拆写进 `PROGRESS / IMPLEMENTATION_NOTES / TEST_GUIDANCE / TEST_RESULTS / PROJECT_STATE`
- `测试说明生成`：把开发结果翻成用户可直接照着测的说明
- `阶段切换判断`：决定继续派单、先测试、先确认、阻塞等待还是进入下一阶段

## 第一次接手时的推荐阅读顺序

如果你是第一次进入这个 skill，推荐只按下面顺序读：

1. 当前文档 `agent_handoff_quickstart.md`
2. `SKILL.md`
3. `docs/workflow.md`
4. 再按当前任务目标，进入下面对应的阅读路径

不要一上来把所有 docs 全读完。先定位任务，再补读相关规则。

## 不同任务目标下的阅读路径

### A. 想继续写开发 prompt

按这个顺序读：

1. `projects/<project>/PROJECT_STATE.md`
2. `projects/<project>/PRD.md`
3. `projects/<project>/PROGRESS.md`
4. `projects/<project>/IMPLEMENTATION_NOTES.md`
5. `projects/<project>/TEST_RESULTS.md`
6. `docs/prompt_generation_guide.md`
7. `docs/prompt_generation_flow.md`
8. `docs/task_type_prompt_guide.md`
9. `docs/prompt_scoring_rubric.md`
10. `templates/round_prompt_by_type_template.txt`

为什么这样读：

- 前 5 个先告诉你当前项目状态和上一轮遗留
- 后 5 个才决定 prompt 怎么收口

### B. 想审执行器回执并更新记录

按这个顺序读：

1. `projects/<project>/PROJECT_STATE.md`
2. `projects/<project>/PRD.md`
3. `projects/<project>/IMPLEMENTATION_NOTES.md`
4. `projects/<project>/PROGRESS.md`
5. 当前轮 prompt 或 `ROUND_INDEX.md`
6. `docs/implementation_feedback_compression_guide.md`
7. `docs/feedback_to_prompt_mapping.md`
8. `templates/implementation_capture_template.md`
9. `templates/progress_template.md`

为什么这样读：

- 先知道这轮本来要做什么，再判断回执到底值不值得写进长期记录

### C. 想给用户写测试说明

按这个顺序读：

1. `projects/<project>/PROJECT_STATE.md`
2. `projects/<project>/PRD.md`
3. `projects/<project>/IMPLEMENTATION_NOTES.md`
4. `projects/<project>/TEST_RESULTS.md`
5. `docs/test_guidance_generation_guide.md`
6. `templates/test_guidance_template.md`

为什么这样读：

- 测试说明优先服务本轮目标和当前风险，不是复述实现过程

### D. 想判断下一步该继续派单 / 先测试 / 阻塞等待

按这个顺序读：

1. `projects/<project>/PROJECT_STATE.md`
2. `projects/<project>/PRD.md`
3. `projects/<project>/IMPLEMENTATION_NOTES.md`
4. `projects/<project>/TEST_RESULTS.md`
5. `docs/stage_transition_decision_card.md`
6. `docs/feedback_to_prompt_mapping.md`
7. `templates/next_step_template.md`

为什么这样读：

- 阶段判断依赖“当前事实 + 最近测试/反馈”，不是只看最新 prompt

### E. 想接一个已有项目

按这个顺序读：

1. `docs/agent_handoff_quickstart.md`
2. `projects/<project>/PROJECT_STATE.md`
3. `projects/<project>/PRD.md`
4. `projects/<project>/PROGRESS.md`
5. `projects/<project>/IMPLEMENTATION_NOTES.md`
6. `projects/<project>/ROUND_INDEX.md`
7. `projects/<project>/TEST_RESULTS.md`
8. `projects/<project>/TEST_GUIDANCE.md`

为什么不是先读别的：

- `PROJECT_STATE.md` 先给你当前阶段和下一步
- `PRD.md` 先告诉你边界
- `PROGRESS.md` 先给 1 到 2 分钟内可用的短摘要
- 其余文件再补细节

## 最小接管完成后怎么选分流

接管摘要形成后，优先这样选：

- 要补下一轮开发动作：走开发 prompt 路径
- 手头已经有新回执：先走回执压缩和记录更新
- 当前结果看起来已可测：先走测试说明
- 当前分歧是“现在该做什么”：先走下一步判断

如果这四条都还不能稳定判断，先补问，不要硬分流。

## 接某个具体项目时，项目文件应该按什么顺序看

默认顺序：

1. `PROJECT_STATE.md`
2. `PRD.md`
3. `PROGRESS.md`
4. `IMPLEMENTATION_NOTES.md`
5. `ROUND_INDEX.md`
6. `TEST_RESULTS.md`
7. `TEST_GUIDANCE.md`

补充判断：

- 必须先看 `PROJECT_STATE.md`，不要先看 prompt
- 如果最近一轮发生过测试、用户反馈或失败，必须优先补看 `TEST_RESULTS.md`
- 如果你要判断“实际做到了什么”，必须看 `IMPLEMENTATION_NOTES.md`
- 如果只是快速接概况，`PROJECT_STATE.md + PRD.md + PROGRESS.md` 可以先建立最小上下文

## 如何判断当前项目处于什么状态

先看 `PROJECT_STATE.md` 的 `当前阶段`，再用其他文件交叉确认。

- `Discovery`：没有可执行 PRD，或当前阶段就是 `Discovery`
- `PRD locked 后开发中`：`PRD.md` 已 `locked`，且当前阶段是 `Build Delegation`
- `测试中`：当前阶段是 `Test Guidance`，或 `TEST_GUIDANCE.md / TEST_RESULTS.md` 是最近主要动作
- `阻塞中`：当前结论是 `阻塞等待`，或当前阻塞依赖外部条件 / 用户决策
- `收尾中`：本轮目标已基本通过，当前主要是测试验证、记录补齐或下一轮规划

不要只靠一个文件单点判断。

## 第一轮输出前，最低限度必须确认的信息

在你第一次输出前，至少确认这 8 件事：

1. 当前项目名
2. 当前阶段
3. `PRD.md` 是否 `locked`
4. 当前轮 / 最近一轮在做什么
5. 当前轮结论是 `通过 / 继续修改 / 阻塞等待`
6. 当前最关键未闭环点是什么
7. 最近是否已有测试结果或用户反馈
8. 当前是否存在 `stub / mock / 假数据 / 未接线 / 外部阻塞`

如果这 8 件事里有明显空白，不要急着写 prompt 或下结论。

默认接管时，第一轮输出优先用 `templates/takeover_summary_template.md` 的结构来汇报。

## 常见误接手错误

### 1. 只看最新 prompt，不看 `PRD.md / PROJECT_STATE.md`

为什么危险：

- 很容易串范围，或把旧 prompt 当成当前真实状态

正确替代动作：

- 先看 `PROJECT_STATE.md` 和 `PRD.md`，再决定 prompt 是否仍有效

### 2. 看到执行器说“已完成”就默认闭环

为什么危险：

- 执行器自评不等于可验证事实

正确替代动作：

- 优先找 `IMPLEMENTATION_NOTES.md`、`TEST_RESULTS.md` 和待验证点

### 3. 没区分新增需求和实现偏差

为什么危险：

- 会把应该走变更提议的问题，误写成修复派单

正确替代动作：

- 先读 `docs/feedback_to_prompt_mapping.md`

### 4. 没区分本轮完成和项目完成

为什么危险：

- 会把“项目还有后续条目”误判为“本轮没过”

正确替代动作：

- 先判断当前轮目标是否达标，再看 PRD 是否还有后续轮次

### 5. 没看 `locked` PRD 状态就直接改范围

为什么危险：

- 会破坏整个 skill 最重要的边界约束

正确替代动作：

- 先确认 `PRD.md` 状态；如已 `locked`，新范围先进 `CHANGE_PROPOSALS.md`

### 6. 把长回执大段照抄进项目记录

为什么危险：

- 记录会失焦，后续 agent 更难接手

正确替代动作：

- 先用 `docs/implementation_feedback_compression_guide.md` 按用途拆写

### 7. 没看测试结果就直接继续派单

为什么危险：

- 容易漏掉用户已经反馈的问题，或在本该先测试时继续扩功能

正确替代动作：

- 如果最近一轮已有测试或用户反馈，先看 `TEST_RESULTS.md`

## 30 秒接管版摘要

- 先看：`PROJECT_STATE.md -> PRD.md -> PROGRESS.md`
- 再看：`IMPLEMENTATION_NOTES.md -> ROUND_INDEX.md -> TEST_RESULTS.md`
- 写 prompt 前：补读 `prompt_generation_*`、`task_type_prompt_guide.md`、`prompt_scoring_rubric.md`
- 审回执前：补读 `implementation_feedback_compression_guide.md`
- 写测试说明前：补读 `test_guidance_generation_guide.md`
- 判断下一步前：补读 `stage_transition_decision_card.md`
- 永远记住：`locked PRD 不擅改，执行器自评不等于事实，多项目不串，记录不照抄`
