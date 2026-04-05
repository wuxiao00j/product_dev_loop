# 示例：接管后进入“审执行器回执并更新记录”

## 用户最初怎么说

`继续项目 demo，这里是 Codex 刚回的实现说明，帮我收一下记录。`

## agent 如何触发最小接管

先读：

1. `docs/agent_handoff_quickstart.md`
2. `projects/demo/PROJECT_STATE.md`
3. `projects/demo/PRD.md`
4. `projects/demo/PROGRESS.md`
5. `projects/demo/IMPLEMENTATION_NOTES.md`

然后再读用户刚给的执行器回执。

## 接管摘要里识别出的关键结论

- 项目仍在 `Feedback Capture`
- `PRD.md` 已 `locked`
- 当前记录还停留在上一轮
- 手头已经有一份新的长回执，但尚未压缩进项目记录

## 为什么下一步该进入这个分流

- 当前最缺的是“这轮实际做到了什么”的判断
- 还不能直接写下一轮 prompt
- 也不适合先给用户测试，因为记录还没压缩成可用事实

## 第一条正式动作输出应该长什么样

`我先按回执压缩规则收这轮实现信息：把可确认事实写进 IMPLEMENTATION_NOTES，把 1 到 2 句结论写进 PROGRESS，再根据待验证点补 TEST_GUIDANCE 和 PROJECT_STATE。`
