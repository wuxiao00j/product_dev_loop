# 新项目初始化指南

这份指南只解决一个问题：如何从 0 建一个可长期复用的项目目录。

## 1. 从 0 创建新项目目录

推荐目录：

```text
skills/product_dev_loop/projects/<project-name>/
```

最少先创建这些文件：

- `PRD.md`
- `PROJECT_STATE.md`
- `PROGRESS.md`
- `IMPLEMENTATION_NOTES.md`
- `CHANGE_PROPOSALS.md`
- `IMPLICIT_REQUIREMENTS.md`
- `DECISIONS.md`
- `TEST_GUIDANCE.md`
- `PROMPTS/`

## 2. 哪些文件是必须的，哪些是按需

必须：

- `PRD.md`
- `PROJECT_STATE.md`
- `PROGRESS.md`
- `IMPLEMENTATION_NOTES.md`
- `CHANGE_PROPOSALS.md`
- `IMPLICIT_REQUIREMENTS.md`
- `DECISIONS.md`
- `TEST_GUIDANCE.md`
- `PROMPTS/`

按需：

- `DISCOVERY.md`
- `ARCHITECTURE.md`
- `ROUND_INDEX.md`
- `TEST_RESULTS.md`

如果项目会推进多轮，建议从一开始就加上 `ROUND_INDEX.md` 和 `TEST_RESULTS.md`。

## 3. PRD 什么时候从 draft 变成 locked

- 刚写出来时，`PRD.md` 状态是 `draft`
- 当用户明确确认当前范围、非目标和验收标准后，再改成 `locked`
- `locked` 之后不得直接改定义
- 新需求或范围变化先写进 `CHANGE_PROPOSALS.md`

## 4. 没有真实代码仓库时怎么推进

如果还没有真实代码仓库，也可以先按文档方式推进：

1. 先建项目目录和基础文档
2. 用 `DISCOVERY.md` 和 `PRD.md` 把范围写清楚
3. 用 `PROMPTS/round-01-build.txt` 先定义首轮开发目标
4. 用 `TEST_GUIDANCE.md` 和 `TEST_RESULTS.md` 先演练验收方式
5. 等真实仓库存在后，再把关键文件路径和实现记录接上

## 5. 第一次进入开发前的最小检查

- 项目目录已独立
- PRD 已存在
- PRD 状态已明确
- 当前轮目标已收敛
- 非目标已写清
- 测试入口至少可描述
