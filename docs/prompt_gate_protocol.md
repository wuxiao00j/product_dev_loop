# Prompt Gate Protocol

这份文档定义 `Prompt Gate` 的正式协议。

目标不是补一层说明，而是提供一个真正的入口门，判断当前输入能不能直接进入 `Build Delegation`。

硬规则先写在前面：

- 未经 `Prompt Gate` 判定为 `PASS`，不得把用户原始任务块视为可直接派给执行器的 round prompt
- `REWRITE_REQUIRED` 和 `CLARIFICATION_REQUIRED` 都禁止直接进入 `Build Delegation`
- `Build Delegation` 只接受已经通过 `Prompt Gate` 的 round prompt
- 字段齐全，不等于 `Prompt Gate` 已通过

## 1. Gate 的职责

`Prompt Gate` 的职责只有一个：

- 判断当前输入是否具备直接进入 `Build Delegation` 的资格

它不负责直接实现代码，也不负责偷偷替用户扩范围。

它负责做三件事：

1. 识别输入类型
2. 给出 `PASS / REWRITE_REQUIRED / CLARIFICATION_REQUIRED`
3. 指定后续动作

补充职责：

4. 识别 `pseudo-qualified prompt`
5. 在 `PASS` 前检查 `PASS evidence`
6. 把每次 `Prompt Gate Result` 落档
7. 在 `CLARIFICATION_REQUIRED` 时只提出一个最小阻塞问题

## 2. Gate 处理的三类输入

### 1. Qualified Round Prompt

特征：

- 已锁定项目 / 轮次 / 阶段 / PRD 状态
- 已判断任务类型
- 已收成单轮最小闭环
- 已写本轮不做、验收、依赖规则、结构化回传、测试要求、PRD 对照

默认 Gate 结果：

- `PASS`

注意：

- 只有真正满足 `PASS evidence` 的 qualified round prompt，才应得到 `PASS`

### 2. Raw Request

特征：

- 更像功能清单、issue 池、TODO 打包、需求块或多模块开发单
- 缺少 round prompt 的关键字段

默认 Gate 结果：

- `REWRITE_REQUIRED`

### 3. Ambiguous Input

特征：

- 项目不唯一
- 当前轮次或 PRD 状态不清楚
- 输入里包含关键冲突，导致无法稳定归类或无法安全 rewrite

默认 Gate 结果：

- `CLARIFICATION_REQUIRED`

## 2.1 什么是 pseudo-qualified prompt

`pseudo-qualified prompt` 不是第四种 Gate 状态，而是一种高风险输入形态。

它的典型特点是：

- 看起来像标准 round prompt
- 字段已经写得比较齐
- 但实质上仍然没有通过 Gate

典型信号：

- 已写 round / stage / PRD status / test / structured return
- 但仍然同时包含多个主闭环
- 或验收项无法收成一个主闭环
- 或 fallback / blocker 规则只是空壳
- 或没有明确 `why not split`
- 或没有明确 `PASS evidence`

遇到 `pseudo-qualified prompt` 时，默认动作不是因为“格式像合格 prompt”就放行，而是：

- 继续判 `REWRITE_REQUIRED`

## 3. Gate 的三种输出状态

### 1. PASS

表示：

- 当前输入已经满足进入 `Build Delegation` 的最低输入契约
- 并且已经具备明确的 `PASS evidence`

后续动作：

1. 记录 `Prompt Gate` 结果
2. 进入 round prompt 自检与评分
3. 只有评分也过线后，才进入正式 `Build Delegation`

### 2. REWRITE_REQUIRED

表示：

- 当前输入不是可直接派单的 round prompt
- 但上下文足够，可以先 rewrite

后续动作：

1. 先输出 Gate 结果
2. 先落档
3. 进入 `prompt rewrite`
4. 必要时建议拆轮
5. rewrite 完成后，重新过 `Prompt Gate`
6. re-gate 后继续落档
7. 未重新拿到 `PASS` 前，不得进入 `Build Delegation`

### 3. CLARIFICATION_REQUIRED

表示：

- 当前阻塞不是“文案不够好”，而是存在关键不确定项
- 此时不能安全 rewrite，也不能安全派单

后续动作：

1. 先输出 Gate 结果
2. 先落档
3. 只允许提出最小补问
4. 补问只针对当前最影响推进的那个阻塞点
5. 拿到澄清后，先记录用户最短回复
6. 再重新过 `Prompt Gate`
7. re-gate 后继续落档
8. 未拿到 `PASS` 前，不得进入 `Build Delegation`

## 4. Gate 的判定维度

`Prompt Gate` 至少检查以下九个维度：

### 1. 项目 / 轮次 / 阶段 / PRD 状态是否锁定

要检查：

- 是否明确项目
- 是否明确当前轮次
- 是否明确当前阶段
- 是否明确 `PRD.md` 是 `draft` 还是 `locked`

### 2. 任务类型是否能稳定归类

要检查：

- 是否能明确判断为 `build / fix / polish / unblock`
- 是否不存在多个主类型并列争夺本轮主目标

### 3. 是否为单轮最小闭环

要检查：

- 是否只收敛一个主目标
- 是否能明确用户本轮能看到什么变化
- 是否不存在多主闭环混合

### 4. 是否明确本轮不做

要检查：

- 是否有强边界
- 是否禁止顺手扩功能、顺手重构、顺手补依赖链

### 5. 是否有验收标准

要检查：

- 验收是否外部可判断
- 验收是否能覆盖本轮目标

### 6. 是否有依赖 / fallback / blocker 规则

要检查：

- 关键依赖是否明确
- 依赖不满足时是否写明降级边界
- 哪些情况应直接阻塞，是否明确

### 7. 是否有结构化回传

要检查：

- 是否明确要求 `已完成 / 未完成 / 关键代码信息 / 特殊状态 / 风险`

### 8. 是否有测试要求

要检查：

- 是否要求测试入口、步骤、数据、预期结果、失败判定

### 9. 是否有 PRD 对照

要检查：

- 是否要求说明对应哪些 PRD 条目
- 是否要求区分已满足和未满足项
- 是否要求判断是否达成本轮验收

## 4.1 Gate 还必须防止“被格式欺骗”

以下情况即使字段齐全，也仍然不能给 `PASS`：

### 1. 多主闭环混合

- 目标区和必做区同时塞入多个核心能力主题

### 2. 多入口并行新做

- CLI / API / Web UI 同时作为本轮新主目标

### 3. 验收项不是围绕一个主闭环

- 验收项之间是并列闭环，不是同一主路径的不同环节

### 4. fallback / blocker 规则无效

- 只写“请说明”“视情况判断”
- 没写清降级边界和直接阻塞条件

### 5. 没有 why-not-split

- 输入命中默认拆轮条件
- 却没有解释为什么本轮不拆

### 6. 没有 PASS evidence

- 没有明确证明为什么这是 `PASS`

这些都说明：

- 字段齐全只是形式完整
- 不是闭环完整

## 5. Gate 判定逻辑

建议按下面顺序判：

1. 先看是不是项目不明、轮次不明、PRD 状态不明或关键冲突
2. 如果是，给 `CLARIFICATION_REQUIRED`
3. 再看当前输入是不是 `pseudo-qualified prompt`
4. 如果是，默认不给 `PASS`
5. 再看是否命中一票否决项
6. 如果命中，但上下文足够 rewrite，给 `REWRITE_REQUIRED`
7. 再看是否属于多主闭环混合
8. 如果是，默认 `REWRITE_REQUIRED`，并建议拆轮
9. 再检查是否具备 `PASS evidence`
10. 只有全部关键维度都过线，且 `PASS evidence` 成立时，才给 `PASS`

## 5.1 PASS evidence 要求

真正的 `PASS` 必须同时满足：

1. 输入契约字段齐
2. 已收成单轮主闭环
3. `out of scope` 有效抑制扩散
4. `acceptance` 与 `round goal` 一一对应
5. `dependency / fallback / blocker` 规则清楚
6. 不命中默认拆轮条件，或已明确说明为什么本轮不拆
7. 已提供明确 `PASS evidence`

推荐最少证据：

- `Prompt Gate: PASS`
- `Round main closure`
- `Why not split`
- `Fallback / blocker rule`
- `Delegation contract: satisfied`

## 6. Gate 与 Rewrite / Clarify / Delegation 的关系

顺序必须是：

`Input Intake -> Prompt Gate -> PASS / REWRITE_REQUIRED / CLARIFICATION_REQUIRED`

然后再分流：

- `PASS -> 落档 -> scoring -> Build Delegation`
- `REWRITE_REQUIRED -> 落档 -> rewrite -> re-gate -> 再落档`
- `CLARIFICATION_REQUIRED -> 落档 -> 最小补问 -> 记录最短回复 -> re-gate -> 再落档`

禁止的动作：

- 不经过 Gate，直接把 raw request 发给执行器
- Gate 结果是 `REWRITE_REQUIRED`，却跳过 rewrite 直接派单
- Gate 结果是 `CLARIFICATION_REQUIRED`，却靠猜测继续收口

## 7. Gate 输出必须结构化

`Prompt Gate` 的结果不能只写一句“这个不太行”。

每次 Gate 都应尽量输出结构化结果，至少包括：

- 输入类型判断
- 任务类型判断
- 是否单轮最小闭环
- 是否属于 `pseudo-qualified prompt`
- 一票否决项
- 可修正项
- 推荐动作
- 是否建议拆轮
- `PASS evidence` 是否成立
- 若拆轮，建议拆分方向
- 若需补问，只允许问的最小阻塞问题
- Gate 最终结论

建议使用：

- `templates/prompt_gate_result_template.md`

## 7.1 Gate Result 落档要求

`Prompt Gate Result` 不是只在聊天里说过就算。

canonical 落档位置固定为：

- `projects/<project>/PROMPTS/GATE_RESULTS.md`

记录要求：

- 首次 Gate 后必须记录
- rewrite 后 re-gate 必须更新
- clarification 后 re-gate 必须更新
- `PASS` 结果也必须记录

每条记录至少包括：

- 输入类型
- Gate 结论
- 是否 `pseudo-qualified`
- 一票否决项
- 可修正项
- 是否建议拆轮
- 下一步动作
- 若为 `PASS`，`PASS evidence` 摘要

建议搭配：

- `docs/prompt_gate_result_logging_guide.md`
- `templates/prompt_gate_result_log_entry_template.md`

## 7.2 CLARIFICATION_REQUIRED 的最小补问原则

`CLARIFICATION_REQUIRED` 不是让 agent 自由发挥连环追问。

硬规则：

- 只问当前最阻塞推进的那一个问题
- 不连环追问
- 不把多个问题打包一起问
- 不在问题里顺带长篇方案
- 用户给出最短回复后，应能重新进入 Gate

适用情形：

- 项目不唯一
- 当前轮次 / 阶段不清
- PRD 状态不清
- 输入存在关键冲突，导致无法安全收口
- 缺少会直接影响拆轮 / 主闭环判断的关键信息

建议搭配：

- `templates/clarification_min_question_template.md`
- `examples/clarification_required_example.md`

## 8. 与现有长期原则的关系

`Prompt Gate` 不改变现有 skill 的核心定位，只负责把入口门做硬：

- 不改变 `PRD locked` 后不得擅改的原则
- 不改变多项目隔离原则
- 不取消每轮测试要求
- 不取消 PRD 对照要求
- 不把 skill 变成代码执行器

它只是把“用户草稿需求不等于合格派单 prompt”从说明性规则升级成协议层入口门。
