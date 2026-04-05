# 示例：接管后进入“判断下一步该怎么走”

## 用户最初怎么说

`继续项目 demo，先帮我判断现在该继续改、先测试，还是先停一下。`

## agent 如何触发最小接管

先读：

1. `docs/agent_handoff_quickstart.md`
2. `projects/demo/PROJECT_STATE.md`
3. `projects/demo/PRD.md`
4. `projects/demo/IMPLEMENTATION_NOTES.md`
5. `projects/demo/TEST_RESULTS.md`

## 接管摘要里识别出的关键结论

- 当前 `PRD.md` 已 `locked`
- 主路径已经能走通
- 最近用户反馈提到“顺手加删除功能”
- 但当前测试失败点只集中在边界提示

## 为什么下一步该进入这个分流

- 当前分歧不是“做了什么”，而是“接下来该怎么处理”
- 用户反馈里同时混有新增需求和现有问题
- 这时先做阶段判断，比直接写 prompt 更稳

## 第一条正式动作输出应该长什么样

`当前更适合先做下一步判断：边界提示问题属于可继续修复的实现问题，但“删除功能”是新增需求，不建议直接混进下一轮。下一步建议先确认是否把删除功能写入 change proposal，再决定要不要继续派单修边界。`
