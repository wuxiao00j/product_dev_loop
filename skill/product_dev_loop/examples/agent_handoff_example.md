# 示例：新 agent 如何接手一个已有项目

## 当前场景

- 项目：`demo`
- 当前 `PROJECT_STATE.md` 显示：
  - 当前阶段：`Build Delegation`
  - PRD 状态：`locked`
  - 当前结论：`继续修改`
  - 下一步：执行 `PROMPTS/round-02-fix.txt`

## 如果用户只说“继续项目 demo”

这句话默认应触发接管协议，而不是直接开始写 `round-02-fix` 的下一版 prompt。

## 新 agent 应先读哪些文件

推荐顺序：

1. `projects/demo/PROJECT_STATE.md`
2. `projects/demo/PRD.md`
3. `projects/demo/PROGRESS.md`
4. `projects/demo/IMPLEMENTATION_NOTES.md`
5. `projects/demo/ROUND_INDEX.md`
6. `projects/demo/TEST_RESULTS.md`

## 为什么不是先读别的

- 不是先读最新 prompt：
  - 因为先要确认当前状态和当前边界，避免拿旧 prompt 当最新事实
- 不是先读所有 docs：
  - 因为先接项目状态，再补相关规则，速度更快
- 不是先读 `TEST_GUIDANCE.md`：
  - 因为当前阶段是 `Build Delegation`，先确认实现缺口比先看测试步骤更重要

## 接手后第一轮应该确认什么

最少确认：

- 当前在修什么：Round 01 测试确认存在假数据问题
- 当前不该改什么：PRD 范围不变，不扩“删除待办”
- 当前阻塞什么：真实持久化尚未接入；删除功能是否纳入 v1 待用户决策
- 最近测试说明了什么：`TEST_RESULTS.md` 已把问题分成实现缺陷 / 新需求 / 隐性偏好

## 接手后第一轮应该输出什么

如果目标是继续写开发 prompt：

- 第一轮输出不应直接开始写代码
- 应先确认当前下一轮仍应聚焦“去掉假数据初始化并再次验证闭环”
- 然后再进入 `prompt_generation_guide.md -> prompt_generation_flow.md -> task_type_prompt_guide.md`

如果目标是判断现在该不该继续派单：

- 第一轮输出应先给出阶段判断：
  - 当前仍属于 `继续派单`
  - 原因：存在明确实现缺陷，且测试已确认问题，不是新增需求

## 这个示例要表达的重点

- 新 agent 接手时，先接项目状态，再选规则路径
- 先弄清“当前最关键未闭环点”，再决定读哪类规则文档
