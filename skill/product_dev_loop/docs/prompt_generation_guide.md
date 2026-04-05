# Prompt Generation Guide

这份文档专门约束 `Build Delegation` 阶段如何生成高质量开发派单 prompt。

结论先写在前面：

- 只有功能描述，不算合格 prompt。
- “帮我做一个 xx 功能” 只是需求描述，不是可派发、可验收、可收口的开发 prompt。
- 合格 prompt 的目标不是把任务说得更长，而是把本轮范围、完成标准、回传结构和 PRD 边界说清楚。
- 合格 prompt 还要先判断任务类型，并在发出前判断质量分数是否够稳。
- 在任何 rewrite 或 prompt generation 前，先做 `Prompt Gate`。
- 如果 Gate 不是 `PASS`，不要把输入原样发出去。
- 字段齐全，不等于 `Prompt Gate = PASS`。
- 最终可派单 prompt 需要明确 `PASS evidence`，不能只长得像标准 prompt。
- `Gate Result` 需要落档，不能只停留在聊天里。

## 先产出 Gate 判断，再决定下一步

进入 prompt 生成前，不要先靠感觉决定“这是不是能发的 prompt”。

先做：

1. 读 `docs/prompt_gate_protocol.md`
2. 用 `templates/prompt_gate_result_template.md` 产出 Gate 结果
3. 根据 Gate 状态决定后续动作

Gate 状态与动作映射：

- `PASS`：进入 prompt scoring / `Build Delegation`
- `REWRITE_REQUIRED`：先 rewrite，禁止直接派单
- `CLARIFICATION_REQUIRED`：只允许最小补问，禁止直接派单

Gate 后先做：

- 把本次 `Prompt Gate Result` 落到 canonical 位置
- 再决定进入 clarify / rewrite / pass

补充提醒：

- 如果一个输入已经很像标准 round prompt，也要防止它只是 `pseudo-qualified prompt`
- 不能因为它写了 round / stage / PRD / test / return structure，就默认给 `PASS`

这时再按需要读：

- `docs/prompt_gate_result_logging_guide.md`
- `docs/raw_request_to_round_prompt_guide.md`
- `docs/raw_prompt_defect_checklist.md`
- `docs/round_split_decision_guide.md`
- `docs/build_delegation_input_contract.md`

如果 Gate 结果是 `REWRITE_REQUIRED`，再用：

- `templates/round_prompt_rewrite_template.txt`

把草稿收成合格 round prompt。

如果 Gate 结果是 `CLARIFICATION_REQUIRED`，不要先 rewrite；应先解决最小阻塞问题。

建议使用：

- `templates/clarification_min_question_template.md`

什么时候该问，什么时候不该问：

- 如果缺的是项目锁定、当前轮次、PRD 状态、关键冲突或会直接影响拆轮判断的信息，应先问
- 如果上下文已经足够，只是目标太散、边界太松、验收太空，应直接 `REWRITE_REQUIRED`，不要先问

怎么避免多问：

- 每次 Gate cycle 只问一个当前最阻塞的问题
- 用户答完后先 re-gate
- 如果仍未通过，再决定是进入 rewrite，还是下一次新的单问题 clarify

## 如何识别 pseudo-qualified prompt，不被格式欺骗

建议再读：

- `docs/pseudo_qualified_prompt_detection_guide.md`

高风险信号：

- 目标区同时塞多个核心能力主题
- `必做` 同时列多个主闭环
- 验收项无法围绕一个主闭环解释
- fallback / blocker 规则只是空壳
- 没有 `why-not-split`
- 没有 `PASS evidence`

判断原则：

- 字段齐全，只是形式完整
- 闭环收口，才是实质完整

所以：

- 看起来正规，不等于真的能派
- 真正的 `PASS` 必须拿得出 `PASS evidence`

## 什么叫合格的开发派单 prompt

一个合格 prompt，至少要让执行者在开始前就能回答下面这些问题：

- 我现在在做哪个项目？
- 这是第几轮？
- 当前处于哪个阶段？
- PRD 现在是 `draft` 还是 `locked`？
- 开始前必须先读哪些上下文？
- 这一轮只解决什么？
- 这一轮明确不做什么？
- 什么结果才算本轮完成？
- 做完后必须按什么结构回报？
- 需要怎么建议测试？
- 回报时如何对照 PRD 判断？
- 如果中途发现新需求、隐性要求或 PRD 缺口，该怎么处理？

如果这些问题答不出来，这个 prompt 就还没收口，不应该直接派单。

如果这些问题答不出来，Gate 也不应给 `PASS`。

## 先选任务类型，再写 prompt

在开始写字段之前，先判断这轮属于哪一类：

- `build`
- `fix`
- `polish`
- `unblock`

这一步不能省。因为不同类型的 prompt，最容易失控的点不同：

- `build` 容易只写功能，不写最小闭环和数据流
- `fix` 容易只写“修一下”，不写复现、回归风险和修后验证
- `polish` 容易借优化名义扩重构
- `unblock` 容易把解除阻塞写成整套改造

如果类型没选清楚，后面的目标、边界和验收通常也不会稳。

## 合格 prompt 的最小组成

下面这些部分缺一项，prompt 质量就会明显下降。

### 1. 当前项目信息

必须包含：

- 项目名
- 当前轮次
- 当前阶段
- 当前 PRD 状态

作用：

- 防止多项目并行时串项目
- 防止执行者不知道自己是在补缺陷、推进新开发，还是在收尾
- 防止在 `PRD locked` 后还把需求当成可以随便改的草稿

### 2. 执行前必读上下文

至少明确：

- 必读文件
- 按需补读文件
- 上下文冲突时的处理规则

作用：

- 防止执行者脱离项目真实状态直接开做
- 防止重复实现、错改方案、忽略上轮遗留

建议最少要求先读：

- `PROJECT_STATE.md`
- `PRD.md`
- 最近一轮 `PROGRESS.md`
- 最近一轮 `IMPLEMENTATION_NOTES.md`

按需补读：

- `ARCHITECTURE.md`
- `CHANGE_PROPOSALS.md`
- `IMPLICIT_REQUIREMENTS.md`
- `DECISIONS.md`
- `TEST_RESULTS.md`

### 3. 本轮目标

必须写成“这一轮只收敛一个可完成小目标”，而不是功能愿景列表。

合格写法特征：

- 来自 PRD 条目、测试反馈或上轮遗留
- 是这一轮能完成、能验证的小任务
- 能直接说明用户这轮能看到什么变化

不合格写法特征：

- 一次塞入多个未收敛目标
- 只有“把 xx 做完整”这种泛描述
- 没写这轮目标和 PRD 哪部分有关

补充要求：

- `build` 要写最小闭环
- `fix` 要写复现现象和修复目标
- `polish` 要写优化对象和不可动范围
- `unblock` 要写阻塞点和解阻目标

### 4. 本轮边界

必须明确：

- 本轮必做
- 本轮不做
- 重点修改范围

作用：

- 防止顺手扩需求
- 防止把下一轮问题提前混进来
- 防止执行者为了“更完整”而破坏当前节奏

这里要写清楚：`必做` 是本轮闭环底线，`不做` 是强制禁止扩散。

对于不同任务类型，这里的侧重点也不同：

- `build`：边界要防止顺手补更多功能
- `fix`：边界要防止顺手重构
- `polish`：边界要防止借机改结构
- `unblock`：边界要防止把临时解阻扩成正式大改

### 5. 验收标准

必须写成可判断的结果，不要写成空泛目标。

合格的验收标准应该：

- 与本轮目标一一对应
- 可从界面、接口、逻辑结果中直接判断
- 能回答“做到什么程度才算这轮完成”

不合格示例：

- “体验更好”
- “逻辑更完整”
- “尽量优化一下”

### 6. 完成后必须返回的结构化信息

这是收口关键，必须明确写出来。

至少要求返回：

1. 已完成
2. 未完成
3. 关键代码信息
4. `stub / mock / 假数据 / 隐藏入口 / 未接线`
5. 测试建议
6. PRD 对照
7. 需要确认的点或变更建议

作用：

- 让主 agent 能快速判断本轮结论
- 方便压缩到 `PROGRESS.md` 和 `IMPLEMENTATION_NOTES.md`
- 防止执行者只给“已做好”这类无用回执

### 7. 测试建议要求

必须明确要求执行者返回测试建议，而不是默认测试环节自己想。

至少应覆盖：

- 测试入口
- 操作步骤
- 测试数据
- 预期结果
- 失败判定

作用：

- 保证本轮结果可验证
- 方便直接转入 `Test Guidance`

不同任务类型下，测试要求也应补强：

- `build`：验证主路径闭环和关键数据流
- `fix`：验证原问题消失且没有明显回归
- `polish`：验证优化结果可感知且主路径不变
- `unblock`：验证阻塞已解除到可继续推进的程度

### 8. PRD 对照要求

必须要求执行者对照 PRD 输出判断，而不是只报告代码改动。

至少要说明：

- 满足了哪些 PRD 条目
- 还没满足哪些 PRD 条目
- 当前是否达到本轮验收标准

作用：

- 防止“代码做了很多，但不一定做对”
- 防止把偏离 PRD 的结果误判为完成

### 9. 变更建议与隐性要求处理规则

必须明确：

- 发现新需求时，不得直接扩做
- 发现 PRD 缺口时，不得直接擅改 PRD
- 发现隐性要求时，先标记，再确认
- 如果 `PRD.md` 已 `locked`，范围变化先进入 `CHANGE_PROPOSALS.md`

作用：

- 把“执行”与“改范围”拆开
- 保住 PRD 作为项目边界的约束力

## 发出前还要判断“够不够强”

一个 prompt 通过 checklist，只代表“主要字段存在”。

但在真实多轮开发里，prompt 还会因为以下原因继续退化：

- 目标虽然写了，但仍然太散
- `不做` 虽然写了，但没有约束力
- 测试建议虽然写了，但执行不了
- 回传虽然结构化，但没有抓到关键风险

所以发出前还要再做一层判断：

- 先过 checklist
- 再按评分规约打分
- 低于最低标准时，不建议直接发出

## 普通需求 prompt 与收口型派单 prompt 的区别

普通需求 prompt 常见样子：

- 只说要做什么功能
- 没有轮次、阶段、PRD 状态
- 没有上下文阅读要求
- 没有本轮边界
- 没有验收标准
- 没有结构化回传
- 没有测试要求
- 没有 PRD 对照

收口型派单 prompt 则必须做到：

- 能锁定当前项目、当前轮和当前阶段
- 能把目标压缩成一个可完成的小步
- 能明确阻止范围扩散
- 能定义这轮怎样算完成
- 能约束执行后必须回传什么
- 能把结果直接接入测试和 PRD 判断

## 一句话判断法

如果一个 prompt 发出去以后，执行者仍然需要追问“我这轮到底只做什么、什么不做、做完怎么汇报、是否允许改 PRD”，那它就还不是合格 prompt。
