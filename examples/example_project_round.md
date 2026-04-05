# 示例：单项目一轮闭环记录

项目目录示例：

```text
projects/todo-lite/
  PRD.md
  IMPLICIT_REQUIREMENTS.md
  ROUND_RECORD.md
  PROMPTS/
    round-01-build.txt
```

本轮关键点示例：

- 当前阶段：`Feedback Capture`
- 当前 PRD 状态：`locked`
- 本轮目标：完成待办创建和列表展示
- 本轮非目标：不做登录、不做分享
- 关键文件：`src/pages/todos.tsx`、`src/components/todo-form.tsx`
- 关键逻辑：提交表单后创建待办，并刷新当前列表
- 未完成项：删除功能仍未接线
- 风险：当前列表仍使用本地假数据

测试指引示例：

- 测试入口：打开 `/todos`
- 操作步骤：输入标题并提交，再刷新页面
- 测试数据：标题 `买牛奶`
- 预期结果：页面立即显示新待办
- 失败判定：提交后无新增，或刷新后数据丢失

PRD 对照示例：

- 已完成：新增待办、展示待办列表
- 未完成：删除待办、真实后端持久化
- 是否闭环：未完全闭环
- 当前结论：`继续修改`

隐性要求示例：

- 用户强调“默认页面必须一眼看懂，不要隐藏主入口”
- 已确认后，应写入项目自己的 `IMPLICIT_REQUIREMENTS.md`
