# Pseudo-Qualified Prompt Analysis Example

这个例子演示：一个输入已经长得像标准 round prompt，但 `Prompt Gate` 仍然不应该给 `PASS`。

## 1. 伪合格 prompt

见：

- `examples/pseudo_qualified_prompt_bad_example.txt`

## 2. 为什么它不是 PASS

这份输入的问题不在于字段缺失，而在于它只是“形式完整”，不是“闭环完整”。

它已经写了：

- 任务类型
- 项目 / 轮次 / 阶段 / PRD 状态
- 本轮目标
- 本轮边界
- 验收标准
- 测试要求
- 结构化回传

但它仍然不能通过 Gate，因为：

- 目标里同时塞了导出 EPUB、续写半章、风格引导、CLI、API、Web UI 六个主能力 / 主入口
- `必做` 直接把六项都列成必做，说明没有收成单轮主闭环
- 验收项不是围绕一个主闭环，而是围绕多个并列目标展开
- `fallback / blocker` 规则是空壳，只写“请说明”“视情况判断”，没有真实降级边界
- 完全没有 `why-not-split`
- 没有明确 `PASS evidence`

## 3. 它命中了哪些拆轮条件

按 `docs/round_split_decision_guide.md`，它至少命中了：

- 多个核心能力主题同时出现
- 依赖接入 + 功能实现 + 界面改造混合
- CLI / API / Web UI 多入口改造
- 同一轮验收项无法收成一个主闭环

所以即使格式看起来像标准 prompt，默认动作仍应是：

- `Prompt Gate = REWRITE_REQUIRED`

## 4. 它缺少哪些真正的 PASS 证据

真正缺少的是这些：

- `Round main closure`
  - 它没有一句话说明“本轮唯一主闭环是什么”
- `Why not split`
  - 它没有说明为什么这六项不是独立闭环
- `Fallback / blocker rule`
  - 它没有写清关键依赖失败时如何处理
- `Delegation contract: satisfied`
  - 它虽然字段很多，但没有证明自己满足的只是必要条件之外的充分条件

## 5. Prompt Gate 应如何给结论

推荐 Gate 结果应类似：

```md
# Prompt Gate Result

【输入概况】
- 输入来源：已收口 round prompt
- 输入类型判断：pseudo-qualified prompt
- 当前项目：novel-studio
- 当前轮次：round-09
- 当前阶段：Build Delegation
- 当前 PRD 状态：locked

【Gate 核心判断】
- 任务类型判断：build
- 是否单轮最小闭环：否
- 是否存在多主闭环混合：是
- 是否属于 pseudo-qualified prompt：是
- 是否建议拆轮：是

【一票否决项】
- 命中的一票否决项：
  - 目标没有收成一个可控 round
  - 存在多主闭环混合
  - fallback / blocker 规则无效

【可修正项】
- 当前仍需补齐的可修正项：
  - 明确唯一主闭环
  - 明确 why-not-split
  - 明确真实 fallback / blocker 规则

【推荐动作】
- 推荐动作：REWRITE_REQUIRED -> rewrite
- 禁止动作：禁止因为字段看起来齐全就直接进入 Build Delegation

【拆轮建议】
- 是否建议拆轮：是
- 若拆轮，建议拆分方向：
  - Round A：先收“续写半章 + 风格引导”的生成主闭环
  - Round B：补 API
  - Round C：补 Web UI
  - Round D：视优先级决定 CLI 或 EPUB

【PASS Evidence】
- `Prompt Gate: PASS` 是否成立：否
- `Round main closure`：缺失
- `Why not split`：缺失
- `Fallback / blocker rule`：缺失
- `Delegation contract: satisfied / not yet`：not yet

【最小补问】
- 如果必须先问一个问题：当前 round-09 最优先要闭环的是“生成主路径”还是“多入口交付”？

【Gate 最终结论】
- Gate 状态：REWRITE_REQUIRED
- 结论说明：当前输入属于 pseudo-qualified prompt，字段齐全但闭环未收，不能判 PASS
- 下一步动作：先 rewrite，并补齐 PASS evidence，再重新过 Gate
```

## 6. 为什么下一步必须是 REWRITE_REQUIRED

不是因为它写得差，而是因为：

- 它还没有成为单轮主闭环
- 它命中了默认拆轮条件
- 它没有真实 PASS 证据

所以正确动作不是直接派单，而是：

- `REWRITE_REQUIRED`
- 先重写，再决定是否拆轮
- 只有补齐 `PASS evidence` 后，才有资格重新争取 `PASS`
