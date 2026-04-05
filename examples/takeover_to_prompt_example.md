# 示例：接管后进入“写下一轮开发 prompt”

## 用户最初怎么说

`继续项目 demo，并准备下一轮开发 prompt。`

## agent 如何触发最小接管

先读：

1. `docs/agent_handoff_quickstart.md`
2. `projects/demo/PROJECT_STATE.md`
3. `projects/demo/PRD.md`
4. `projects/demo/PROGRESS.md`
5. `projects/demo/TEST_RESULTS.md`

## 接管摘要里识别出的关键结论

- 当前阶段：`Build Delegation`
- `PRD.md`：`locked`
- 最近测试已确认：主路径可用，但刷新后数据丢失
- 当前最关键未闭环点：数据仍未持久化

## 为什么下一步该进入这个分流

- 当前项目和范围都明确
- 最近反馈已经能稳定归类为继续派单的问题
- 下一轮目标可以收敛成“补持久化闭环”

这时不该先走测试说明，因为主问题还没修完。

## 第一条正式动作输出应该长什么样

`下一轮建议继续派单，任务类型倾向于 build。目标只聚焦把待办数据从临时内存改成可保留的数据链路；本轮不扩删除功能，不改列表交互。接下来按 prompt 收口规则生成 round prompt。`
