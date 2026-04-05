# Pseudo-Qualified Prompt Detection Guide

这份文档专门解决一个更隐蔽的误判：

- 输入已经长得像标准 round prompt
- 甚至已经写了项目、轮次、阶段、PRD 状态、测试要求、结构化回传
- 但它本质上仍然没有通过 `Prompt Gate`

结论先写在前面：

- 字段齐全，不等于 Gate 已通过
- 结构看起来正规，不等于已经收成单轮主闭环
- 只长得像标准 prompt 的输入，仍然可能是 `pseudo-qualified prompt`
- `pseudo-qualified prompt` 默认不能直接进入 `Build Delegation`

## 1. 什么是 pseudo-qualified prompt

`pseudo-qualified prompt` 指的是：

- 它在形式上已经像 round prompt
- 但在实质上仍然没有完成闭环收口

典型特征：

- 有字段
- 有格式
- 有标题
- 有测试要求
- 有结构化回传

但仍然存在以下任一问题：

- 多主闭环混合
- 多个核心能力主题同时争夺本轮主目标
- 验收项无法收成一个主闭环
- `out of scope` 没有真正抑制扩散
- `fallback / blocker` 规则缺失或无效
- 没有明确 `why not split`
- 没有真正的 `PASS` 证据

## 2. 为什么 pseudo-qualified prompt 更危险

raw request 很容易被看出来。

`pseudo-qualified prompt` 更危险，是因为它会制造一种假象：

- “字段都在，应该能发了”
- “结构挺标准，应该够了”
- “测试和回传也写了，不像草稿了”

真正的问题在于：

- 它只是形式完整
- 不是闭环完整

所以它最容易绕过低质量判断，直接滑进 `Build Delegation`。

## 3. pseudo-qualified prompt 的典型识别信号

### 1. 字段齐了，但本轮目标仍然塞了多个主闭环

典型信号：

- 目标区里同时写导出、续写、风格引导、CLI、API、Web UI
- 并把它们都列为本轮必做

判定：

- 默认 `REWRITE_REQUIRED`

### 2. 任务类型写了，但不足以稳定解释本轮真实工作

典型信号：

- 写了 `本轮类型：build`
- 但目标里同时混着 build、polish、unblock

判定：

- 默认 `REWRITE_REQUIRED`

### 3. out of scope 存在，但没有真正削掉并列主目标

典型信号：

- 形式上写了 `不做`
- 但 `必做` 里仍然有多个核心能力主题

判定：

- `不做` 无效
- 默认 `REWRITE_REQUIRED`

### 4. acceptance 写了很多条，但不是围绕一个主闭环

典型信号：

- 验收项彼此独立
- 验收完无法用一句话说明“本轮唯一主闭环是什么”

判定：

- 默认 `REWRITE_REQUIRED`

### 5. fallback / blocker 规则只是空壳

典型信号：

- 只写“如果依赖不满足请说明”
- 没写允许降级到哪里
- 没写哪些情况必须直接阻塞

判定：

- 依赖规则无效
- 不能算 Gate `PASS`

### 6. 结构化回传很完整，但没有 why-not-split

典型信号：

- 写了已完成、未完成、测试建议、PRD 对照
- 但没有解释为什么当前这一轮不需要拆

判定：

- 如果输入命中默认拆轮条件，仍应 `REWRITE_REQUIRED`

## 4. 真正 PASS 与 pseudo-qualified 的区别

真正 PASS 需要同时满足：

1. 输入契约字段齐
2. 已收成单轮主闭环
3. `out of scope` 有效抑制扩散
4. `acceptance` 与 `round goal` 一一对应
5. `dependency / fallback / blocker` 规则清楚
6. 不命中默认拆轮条件，或已明确说明为什么本轮不拆
7. 已提供明确 `PASS evidence`

只满足第 1 条，不足以通过 Gate。

## 5. 遇到 pseudo-qualified prompt 时该怎么判

默认动作不是“因为它格式比较完整，所以先发出去试试”。

默认动作应是：

- 识别为 `pseudo-qualified prompt`
- Gate 结果给 `REWRITE_REQUIRED`
- 明确指出它为什么仍未通过 Gate
- 如果命中拆轮条件，建议拆轮

只有在 rewrite 后补齐真正的单轮闭环与 `PASS evidence`，才允许重新争取 `PASS`。

## 6. 最容易误判 PASS 的场景

最典型的误判场景就是：

- `本轮类型：build`
- `当前项目 / 轮次 / 阶段 / PRD 状态` 都写了
- `测试要求 / 结构化回传` 也都写了
- 但目标里同时塞了导出、续写、风格引导、CLI、API、UI 六项

这种输入看起来正规，但仍然应该被 Gate 拦下。

原因：

- 它不是单轮主闭环
- `必做` 已经失控
- 拆轮条件被命中
- 没有 why-not-split
- 没有真实 `PASS evidence`

## 7. 与其他文档的关系

建议搭配使用：

- `docs/prompt_gate_protocol.md`
- `docs/round_split_decision_guide.md`
- `docs/build_delegation_input_contract.md`
- `templates/prompt_gate_result_template.md`

这份文档的角色不是替代它们，而是防止主 agent 被“格式像标准 prompt”这件事欺骗。
