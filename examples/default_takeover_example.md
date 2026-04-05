# 示例：用户只说一句“继续项目 demo”时，默认如何接管

## 用户输入

`继续项目 demo`

## 默认触发的不是“直接写下一轮 prompt”

因为这句话表达的是：

- 先恢复项目上下文
- 再判断下一步该做什么

而不是：

- 已经明确要求立刻开始某个具体动作

## agent 默认应先读哪些文件

推荐顺序：

1. `docs/agent_handoff_quickstart.md`
2. `projects/demo/PROJECT_STATE.md`
3. `projects/demo/PRD.md`
4. `projects/demo/PROGRESS.md`
5. `projects/demo/IMPLEMENTATION_NOTES.md`
6. `projects/demo/TEST_RESULTS.md`
7. `projects/demo/ROUND_INDEX.md`

## agent 第一轮应输出什么

适合的首条接管摘要应类似：

```md
## 项目识别结果

- 项目名：`demo`
- 项目目录：`skills/product_dev_loop/projects/demo`
- 是否存在歧义：`无`

## 当前状态

- 当前阶段：`Build Delegation`
- PRD 状态：`locked`
- 当前轮次 / 最近轮次：`Round 02 / Round 01`

## 最近进展

- 最近一次关键进展：Round 01 已完成待办新增和列表展示，但测试确认存在假数据问题
- 最近一次测试 / 反馈结论：`未通过`，当前主要问题是列表初始化仍使用假数据

## 当前未闭环点

- 当前最关键未闭环点：去掉假数据初始化并再次验证闭环
- 当前主要风险或阻塞：真实持久化尚未接入；是否加入删除功能仍待用户决策

## 建议下一步

- 建议动作：`继续派单`
- 为什么是这个建议：当前存在明确实现缺陷，且测试已经给出问题分类；它不是新增需求，也不是纯外部阻塞
```

## 为什么这时不应直接开始写下一轮 prompt

- 因为还没先确认当前阶段和当前边界
- 还没先确认最近测试结果是否已经改变下一轮方向
- 还没先把“实现缺陷”和“新增需求 / 隐性偏好”分开

只有接管摘要先说清楚，下一轮 prompt 才不会写偏。
