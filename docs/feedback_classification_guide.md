# 反馈分类与流转指南

这份指南解决的是：用户反馈、Cursor 回执和测试结果拿到后，应该怎么分流。

## 1. 最小分类

最少分成 5 类：

- `实现缺陷`
- `PRD 未达标`
- `新需求`
- `隐性偏好`
- `环境阻塞`

## 2. 每类分别写入哪里

### 实现缺陷

定义：

- 需求没变，但实现有 bug、未接线、假数据、错误状态、入口异常

优先写入：

- `IMPLEMENTATION_NOTES.md`
- `PROJECT_STATE.md`

常见结论：

- `继续修改`

### PRD 未达标

定义：

- 功能方向没错，但还没达到 PRD 验收标准

优先写入：

- `IMPLEMENTATION_NOTES.md`
- `PROJECT_STATE.md`
- `PROGRESS.md`

常见结论：

- `继续修改`

### 新需求

定义：

- 用户提出了原 PRD 没写的新功能、新范围或新的验收要求

优先写入：

- `CHANGE_PROPOSALS.md`
- `PROJECT_STATE.md`

注意：

- `PRD.md` 如果已 `locked`，不能直接改

### 隐性偏好

定义：

- 用户没直接写进 PRD，但反复体现稳定偏好或判断标准

优先写入：

- `IMPLICIT_REQUIREMENTS.md`
- `PROJECT_STATE.md`

如果会改变范围或验收：

- 同时写入 `CHANGE_PROPOSALS.md`

### 环境阻塞

定义：

- 不是需求问题，也不是实现本身，而是环境、依赖、权限、数据源等阻断推进

优先写入：

- `PROJECT_STATE.md`
- `PROGRESS.md`

常见结论：

- `阻塞等待`

## 3. 如何判断本轮结论

### `通过`

满足以下条件：

- 本轮目标已达到 PRD 验收标准
- 没有阻断闭环的未完成项
- 没有关键 `stub / mock / 假数据 / 隐藏入口 / 未接线`

### `继续修改`

出现以下任一情况：

- 有实现缺陷
- 仍未达到 PRD 验收标准
- 仍存在关键 `stub / mock / 假数据 / 隐藏入口 / 未接线`

### `阻塞等待`

出现以下任一情况：

- 环境问题导致无法验证
- 用户尚未确认关键变更
- 依赖条件不足，无法进入下一轮

## 4. 推荐流转顺序

1. 先用 `feedback_triage_template.md` 给反馈分类
2. 按分类落到对应文档
3. 在 `PROJECT_STATE.md` 写当前结论
4. 如果需要修复，再生成下一轮 `PROMPTS/round-xx-fix.txt`
