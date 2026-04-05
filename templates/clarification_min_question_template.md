你现在处于 `Prompt Gate = CLARIFICATION_REQUIRED`。

目标不是继续 rewrite，也不是提前派单，而是只问一个当前最阻塞推进的问题。用户给出最短回复后，应能重新进入 Gate。

【先确认为什么必须 clarify，而不是直接 rewrite】
- 当前阻塞类型：`项目不唯一 / 当前轮次不清 / 当前阶段不清 / PRD 状态不清 / 输入存在关键冲突 / 缺少直接影响主闭环或拆轮判断的关键信息`
- 为什么现在不能安全 rewrite：

【最小补问原则】
- 只问当前最阻塞的那一个问题
- 不连环追问
- 不把多个问题打包一起问
- 不在问题里顺带给长篇方案
- 问题必须让用户用最短回复也能继续推进

【输出格式】
- 当前 Gate 结论：`CLARIFICATION_REQUIRED`
- 最小阻塞点：
- 只问这一句：
- 为什么只问这一句：
- 当前禁止动作：`不要 rewrite / 不要 delegation / 不要多问`

【问题写法模板】
请只回答这一个问题：
`<single-blocking-question>`

【拿到用户回复后的动作】
1. 先把这次 Gate 结果记录到 `projects/<project>/PROMPTS/GATE_RESULTS.md`
2. 记录用户的最短澄清回复
3. 用这条回复重新过 `Prompt Gate`
4. 如果仍未 `PASS`，再判断是 `REWRITE_REQUIRED` 还是再次 `CLARIFICATION_REQUIRED`
5. 未重新拿到 `PASS` 前，不得进入 `Build Delegation`

【禁止示例】
- “你说的是哪个项目、哪一轮、优先做哪个、要不要顺便补 API？”
- “我建议你先做 A，再做 B，你看是否也一起做 C？”

【合格示例】
- “你说的‘小说项目’是 `novel-studio` 还是 `novel-mobile`？”
- “这轮优先闭环的是‘续写主路径’还是‘导出能力’？”
