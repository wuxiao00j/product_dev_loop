# Prompt Gate Result Logging Guide

这份文档定义：`Prompt Gate Result` 应记录到哪里、何时记录、记录什么。

目标不是增加文书负担，而是让 Gate 不再停留在聊天里说过就算。

## 1. Canonical 落档位置

`Prompt Gate Result` 的 canonical 记录位置固定为：

- `projects/<project>/PROMPTS/GATE_RESULTS.md`

如果文件不存在，应在第一次 Gate 时创建。

原因：

- 它和派单 prompt 同属执行入口记录
- 便于接手 agent 回看“这条输入为什么没直接进 Build Delegation”
- 便于串联 `raw input -> gate -> rewrite or clarify -> re-gate -> delegation`

硬规则：

- Gate 结果只在一个 canonical 文件里完整落档
- 不要把完整 Gate 结果散落复制到多个长期文件

补充说明：

- `PROJECT_STATE.md` 可以保留一句当前结论或下一步摘要
- 但完整 Gate 结果以 `PROMPTS/GATE_RESULTS.md` 为准

## 2. 记录时机

### 1. 首次 Gate 后必须记录

适用于：

- 初次判断 raw request
- 初次判断 pseudo-qualified prompt
- 初次判断 ambiguous input
- 初次判断 qualified round prompt

### 2. rewrite 后 re-gate 必须更新

适用于：

- 输入先被判 `REWRITE_REQUIRED`
- rewrite 完成后重新过 Gate

要求：

- 不覆盖旧记录
- 追加一条新的 Gate 结果
- 明确这次是 `re-gate after rewrite`

### 3. clarification 后 re-gate 必须更新

适用于：

- 输入先被判 `CLARIFICATION_REQUIRED`
- 用户给出最短澄清后重新过 Gate

要求：

- 先记录原始 `CLARIFICATION_REQUIRED`
- 再记录用户最短回复
- 再记录新的 re-gate 结果

### 4. Gate 初判 PASS 后也必须记录

原因：

- 需要留下通过证据
- 让后续 agent 知道这轮为什么能合法进入 `Build Delegation`

## 3. 每条 Gate Result 至少记录什么

每条记录至少包括：

- 输入类型
- Gate 结论
- 是否 `pseudo-qualified`
- 一票否决项
- 可修正项
- 是否建议拆轮
- 下一步动作
- 若为 `PASS`，`PASS evidence` 摘要

建议再补：

- `Gate run`
- 来源输入摘要
- 当前项目 / 轮次 / 阶段 / PRD 状态
- 如果是 clarify，记录“本轮只问的最小阻塞问题”
- 如果是 re-gate，写清是 `after rewrite` 还是 `after clarification`

## 4. 记录目的

记录 Gate Result 的目的至少有三个：

### 1. 便于后续 agent 接手

- 后来的 agent 不用重新猜这条输入为什么被拦下

### 2. 避免重复判定

- 不会每次都重新从头判断同一个输入

### 3. 形成完整链路记录

- 从原始输入到最终 delegation 的入口链路可追溯

## 5. 推荐记录结构

建议按追加日志写法记录，每次 Gate 都新增一个小节。

推荐格式：

- `Gate Run`
- 输入概况
- Gate 核心判断
- 一票否决项
- 可修正项
- Clarification
- `PASS evidence`
- 下一步动作

建议使用：

- `templates/prompt_gate_result_log_entry_template.md`

## 6. 与主流程的关系

主流程顺序应是：

`Input Intake -> Prompt Gate -> 记录 Gate Result -> clarify or rewrite or pass -> re-gate -> 再记录 -> Build Delegation`

不是：

- 先在脑内判断
- 直接 rewrite 或直接补问
- 最后想起来再补记录

## 7. 不要这样做

- 不要只在聊天里说“这轮是 REWRITE_REQUIRED”，却不落档
- 不要把完整 Gate 结果同时复制进 `PROJECT_STATE.md`、`PROGRESS.md`、`IMPLEMENTATION_NOTES.md`
- 不要在 rewrite 或 clarification 后覆盖掉上一条 Gate 结果
- 不要省略 `PASS` 记录，默认“反正最后过了就行”
