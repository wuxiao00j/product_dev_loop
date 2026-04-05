# Prompt Gate Result

【输入概况】
- 输入来源：`用户原始任务块 / 已收口 round prompt / 接手后整理输入 / 其他`
- 输入类型判断：`qualified round prompt / raw request / ambiguous input / pseudo-qualified prompt`
- 当前项目：
- 当前轮次：
- 当前阶段：
- 当前 PRD 状态：

【Gate 核心判断】
- 任务类型判断：`build / fix / polish / unblock / 无法稳定判断`
- 是否单轮最小闭环：`是 / 否`
- 是否存在多主闭环混合：`是 / 否`
- 是否属于 `pseudo-qualified prompt`：`是 / 否`
- 是否建议拆轮：`是 / 否`

【一票否决项】
- 命中的一票否决项：
- 如果没有，写：`无`

【可修正项】
- 当前仍需补齐的可修正项：
- 如果没有，写：`无`

【推荐动作】
- 推荐动作：`PASS -> scoring / Build Delegation` 或 `REWRITE_REQUIRED -> rewrite` 或 `CLARIFICATION_REQUIRED -> 最小补问`
- 禁止动作：`写明当前不允许直接做什么`

【拆轮建议】
- 是否建议拆轮：`是 / 否`
- 若拆轮，建议拆分方向：
- 若不拆轮，说明为什么仍可压成单轮：

【PASS Evidence】
- `Prompt Gate: PASS` 是否成立：`是 / 否`
- `Round main closure`：
- `Why not split`：
- `Fallback / blocker rule`：
- `Delegation contract: satisfied / not yet`

【最小补问】
- 如果是 `CLARIFICATION_REQUIRED`，只允许问的最小阻塞问题：
- 如果不是，写：`无`

【Gate 最终结论】
- Gate 状态：`PASS / REWRITE_REQUIRED / CLARIFICATION_REQUIRED`
- 结论说明：
- 下一步动作：
