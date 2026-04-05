# Clarification Required Example

这个例子演示：某条输入为什么不能直接 rewrite 或 delegation，而应该先进入 `CLARIFICATION_REQUIRED`，只问一个最小阻塞问题；用户给出最短回复后，如何重新进入 Gate。

## 1. 输入

```text
继续把小说项目的文风系统补一下。
```

## 2. 为什么当前不能直接 rewrite 或 delegation

这条输入现在还不能直接 rewrite，不是因为它太短，而是因为当前最阻塞推进的问题还没解决：

- “小说项目” 不唯一
- 如果当前并行存在多个小说相关项目，主 agent 无法安全锁定项目上下文
- 项目不锁定，就无法安全判断当前轮次、当前 PRD 状态、当前文风系统到底指哪一段能力

所以这里应先给：

- `Prompt Gate = CLARIFICATION_REQUIRED`

而不是：

- 直接 rewrite
- 或直接 delegation

## 3. 最小补问应该怎么问

这里最小补问只能针对当前最阻塞的那个问题：

```text
请只回答这一个问题：你说的“小说项目”是 `novel-studio` 还是 `novel-mobile`？
```

为什么只问这一句：

- 项目不唯一是当前最上游阻塞
- 只要项目锁定，主 agent 才能继续看该项目的 PRD、轮次和当前缺口
- 现在不应该顺带问“优先续写还是导出”“要不要顺便补 API”，因为那已经超出本轮最小补问范围

## 4. 用户给出的最短回复

```text
novel-studio
```

## 5. 重新进入 Gate

拿到这条最短回复后，动作不是直接派单，而是：

1. 先记录原始 `CLARIFICATION_REQUIRED`
2. 记录这条用户最短回复
3. 重新过 `Prompt Gate`

此时 re-gate 结果可以变成：

- 不再是 `CLARIFICATION_REQUIRED`
- 进入 `REWRITE_REQUIRED`

原因：

- 项目已经明确
- 但“文风系统补一下” 仍然太宽，仍需 rewrite 才能收成单轮主闭环

## 6. 示例 Gate 结果链路

```md
## Gate Run: gate-01
- 记录类型：initial gate

### 输入概况
- 输入来源：用户原始任务块
- 输入类型判断：ambiguous input
- 项目名：未锁定
- 当前轮次：未锁定
- 当前阶段：Build Delegation
- 当前 PRD 状态：未知
- 来源输入摘要：继续把小说项目的文风系统补一下

### Gate 核心判断
- 任务类型判断：无法稳定判断
- 是否单轮最小闭环：无法判断
- 是否存在多主闭环混合：暂不判断
- 是否属于 pseudo-qualified prompt：否
- 是否建议拆轮：暂不判断

### Clarification
- 只问的最小阻塞问题：你说的“小说项目”是 `novel-studio` 还是 `novel-mobile`？
- 用户最短回复：novel-studio

### 下一步动作
- Gate 状态：CLARIFICATION_REQUIRED
- 下一步动作：拿到回复后重新过 Gate
```

```md
## Gate Run: gate-02
- 记录类型：re-gate after clarification

### 输入概况
- 输入来源：用户原始任务块 + clarification
- 输入类型判断：raw request
- 项目名：novel-studio
- 当前轮次：待从项目记录判断
- 当前阶段：Build Delegation
- 当前 PRD 状态：待从项目记录判断
- 来源输入摘要：继续把 novel-studio 的文风系统补一下

### Gate 核心判断
- 任务类型判断：polish 或 build，需结合项目记录收口
- 是否单轮最小闭环：否
- 是否存在多主闭环混合：当前仍未收口
- 是否属于 pseudo-qualified prompt：否
- 是否建议拆轮：视项目记录判断

### 下一步动作
- Gate 状态：REWRITE_REQUIRED
- 下一步动作：读取项目上下文后进入 rewrite
```

## 7. 这个例子证明了什么

它证明的不是“会补问”，而是：

- `CLARIFICATION_REQUIRED` 不是随便追问
- 只问当前最阻塞推进的那一个问题
- 用户给最短回复后，先 re-gate
- re-gate 之后才决定进入 rewrite、继续 clarify，还是最终 PASS
