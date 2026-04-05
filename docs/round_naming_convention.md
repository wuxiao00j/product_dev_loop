# 轮次命名规范

这份规范只做一件事：让多轮推进时不混乱。

## 1. 基本命名规则

统一使用两位数字轮次：

- `round-01`
- `round-02`
- `round-03`

不要混用这些写法：

- `r1`
- `first-round`
- `第二轮修复`

## 2. Prompt 文件命名

推荐格式：

- `PROMPTS/round-01-build.txt`
- `PROMPTS/round-02-fix.txt`
- `PROMPTS/round-02-fix-layout.txt`
- `PROMPTS/round-03-polish.txt`

规则：

- `build` 用于首轮实现
- `fix` 用于修复缺陷或补未达标项
- `polish` 用于小范围体验优化
- 如果同一轮有明确主题，可以在后面补短标签

## 3. 测试结果与实现记录如何对应

推荐对应关系：

- `PROMPTS/round-01-build.txt` 对应 `TEST_RESULTS.md` 中的 `Round 01`
- `PROMPTS/round-02-fix.txt` 对应 `TEST_RESULTS.md` 中的 `Round 02`
- `IMPLEMENTATION_NOTES.md` 中按轮次记录关键实现摘要
- `PROGRESS.md` 中按轮次记录结论和下一步

## 4. PROGRESS.md 如何引用轮次

推荐写法：

```md
### Round 01
- 目标：
- 结果：
- 当前结论：

### Round 02
- 目标：
- 结果：
- 当前结论：
```

## 5. 如何避免多轮混乱

- 每一轮只保留一个主 prompt
- 每一轮都在 `TEST_RESULTS.md` 留测试结果
- 每一轮都在 `PROGRESS.md` 留短摘要
- 每一轮如果有新需求，先写入 `CHANGE_PROPOSALS.md`
- 每一轮如果确认了新偏好，写入 `IMPLICIT_REQUIREMENTS.md`
- 使用 `ROUND_INDEX.md` 做总览，快速看到“这一轮做了什么、测了什么、结论是什么”
