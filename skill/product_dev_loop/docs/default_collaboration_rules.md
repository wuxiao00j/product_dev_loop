# 默认协作规则

这份文档把“用户只说一句短话，agent 也能继续推进项目”的默认规则写死。

目标不是做自动系统，而是把默认判断顺序、何时调用 `product_dev_loop_tool`、何时记录项目文件、最终如何收敛输出，固定成陌生 agent 也能照着执行的规则。

---

## 1. 默认触发语句

下面这些说法，默认都视为“请按当前项目状态给出下一步动作”：

- `继续`
- `继续某项目`
- `给我某项目下一步`
- `继续喂 Cursor`

这些短句的默认含义不是“马上写一条新 prompt”，而是：

1. 先识别当前输入类型
2. 先判断当前阶段
3. 先判断最合适的下一步动作
4. 再把输出收敛成用户可直接执行的内容

---

## 2. 默认输入分流规则

收到内容后，先分成 4 类，不要混着处理。

### A. 新需求 / 原始需求

特征：
- 更像需求块、功能清单、TODO、issue 打包
- 还不是稳定 round prompt

默认动作：
1. 读取最小项目上下文（`PROJECT_STATE.md` / `PRD.md` / `PROGRESS.md`）
2. 必要时补读 `IMPLEMENTATION_NOTES.md`
3. 调用 `product_dev_loop_tool skeleton`
4. 如果 skeleton 显示 `rewrite_more`，先产出“收口版下一段 prompt”
5. 如果已接近 `re_gate`，再补 Gate / contract 判断
6. 输出优先收敛成：**给 Cursor / Codex 的下一段提示词**

### B. Cursor / Codex 回执

特征：
- 包含“已完成 / 未完成 / 改了哪些文件 / 测试建议 / 风险”等回执口吻
- 或明显是在描述一轮实现结果

默认动作：
1. 先压缩回执，不直接写下一轮 prompt
2. 更新项目记录（至少 `PROGRESS.md` / `PROJECT_STATE.md` / `IMPLEMENTATION_NOTES.md`）
3. 判断当前更适合：
   - 先给用户测试说明
   - 继续下一轮开发
   - 外部阻塞等待
4. 如果判断“当前更适合先测试”，默认先更新或生成项目内的 `TEST_GUIDANCE.md`
5. 再把其中最关键的测试步骤直接输出给用户，而不是只口头说“你去测一下”
6. 只有当“当前最关键未闭环点”已经明确时，才进入下一轮 prompt 收口
7. 如需继续收口下一轮 prompt，可再调用 `product_dev_loop_tool skeleton / gate / contract`
8. 输出优先收敛成：**测试说明** 或 **下一段 Cursor 提示词**

### C. 用户测试反馈

特征：
- 包含“我测了”“这里不对”“这个没接上”“这个通过了”之类测试结果
- 重点是用户验证后的现象，而不是实现过程

默认动作：
1. 先分类：
   - 实现缺陷
   - PRD 未达标
   - 新需求
   - 隐性偏好
   - 外部阻塞
   - 本轮通过
2. 更新 `TEST_RESULTS.md`（如项目维护该文件）
3. 同步更新 `PROJECT_STATE.md`
4. 如果是实现缺陷 / 未达标，收敛成下一轮 prompt
5. 如果是新需求 / 隐性偏好，先进入变更提议或确认流程
6. 如果是通过，优先进入下一阶段或下一轮目标判断
7. 输出优先收敛成：**下一段 Cursor 提示词**、**阻塞提醒** 或 **澄清问题**

### D. 外部阻塞说明

特征：
- 缺 API key / 账号权限 / 第三方服务 / 环境依赖 / 安装失败
- 当前阻塞不在 prompt 文案，而在外部条件

默认动作：
1. 不默认继续 rewrite prompt
2. 不默认继续派单
3. 直接判断：当前哪些事还能做，哪些事必须停
4. 在 `PROJECT_STATE.md` 标记为 `阻塞等待`
5. 输出优先收敛成：**给用户的阻塞提醒**

---

## 3. “继续某项目”的默认流程

用户只说：`继续某项目`

默认按下面顺序执行：

1. 识别项目
2. 读取最小上下文：
   - `PROJECT_STATE.md`
   - `PRD.md`
   - `PROGRESS.md`
3. 按需补读：
   - `IMPLEMENTATION_NOTES.md`
   - `TEST_RESULTS.md`
   - `TEST_GUIDANCE.md`
   - `ROUND_INDEX.md`
4. 判断当前更接近哪一种：
   - 缺下一轮 prompt
   - 缺对回执的判断
   - 缺测试说明
   - 缺外部条件
5. 输出一个默认下一步，不展开内部长分析

默认输出只能优先收敛成 4 类之一：
- 给 Cursor / Codex 的下一段提示词
- 给用户的测试说明
- 给用户的阻塞提醒
- 给用户的最小澄清问题

---

## 4. “继续喂 Cursor”的默认流程

用户只说：`继续喂 Cursor`

默认理解为：
- 当前需要产出一段新的、可直接继续发给 Cursor / Codex 的 prompt
- 但前提是当前状态确实适合继续派单

执行顺序：
1. 先确认当前不是 `阻塞等待`
2. 先确认最近输入不是“应该先测试”
3. 如果最近输入更像新需求 / 回执 / 测试反馈，先做分流判断
4. 如果需要 prompt 收口：
   - 优先调用 `product_dev_loop_tool skeleton`
   - 若 skeleton 仍显示 `rewrite_more`，继续写收口版 prompt
   - 若 skeleton 已接近 `re_gate`，再补 Gate / contract
5. 最终只输出：**下一段给 Cursor / Codex 的提示词**

---

## 5. 何时调用 `product_dev_loop_tool`

`product_dev_loop_tool` 是分析层，不是默认每次都调用。

### 应调用的情况

#### 1. 新需求 / 需要收口 prompt
- 优先调用 `skeleton`
- 目的：判断当前是 `rewrite_more / re_gate / stable / clarify_first`

#### 2. 伪合格 prompt 风险高
- 调用 `gate`
- 目的：确认是不是 `pseudo-qualified prompt`

#### 3. 准备进入正式 Build Delegation
- 调用 `gate` + `contract`
- 目的：确认是否已具备 `PASS` 和输入契约

#### 4. Cursor 回执后准备继续下一轮 prompt
- 可再次调用 `skeleton`
- 目的：判断当前更适合继续 rewrite 还是值得 re-gate

### 不应调用的情况

#### 1. 纯外部阻塞
- 缺 API key / 权限 / 环境依赖
- 这时先输出阻塞提醒，不要硬跑 tool

#### 2. 纯测试说明生成
- 当前明确是“给用户怎么测”
- 不需要先跑 Gate / skeleton

#### 3. 纯记录归档
- 当前只是把回执压缩进项目记录
- 不需要为记录动作单独跑 tool

---

## 6. rewrite / re-gate / user_test / blocked_external 默认判断

### 继续 rewrite prompt
满足任一情况时，默认优先 rewrite：
- `skeleton.recommended_next_step = rewrite_more`
- 关键 section 仍是 `placeholder`
- `first_fix_order` 前几项仍是 `critical`
- 当前输入更像 raw request 或 pseudo-qualified prompt

### 进入 re-gate
满足这些信号时，默认值得 re-gate：
- skeleton 关键 placeholder 已消失
- 主闭环、边界、fallback、结构化回传、PRD 对照都已补齐
- 继续局部润色的收益已经明显下降

### 让用户先测试
满足这些信号时，默认先给测试说明：
- 执行器回执显示主路径已实现
- 当前最缺的是“用户如何验证”
- 是否通过，要靠真实运行或点击验证

### 停下来补外部条件
满足这些信号时，默认不要继续扩做：
- 缺账号、权限、token、服务可用性
- 缺第三方库且不存在合理 fallback
- 当前问题不是 prompt 不够好，而是外部条件不成立

---

## 7. 默认记录策略

默认至少维护这些文件：

- `ROUND_INDEX.md`
- `PROGRESS.md`
- `PROJECT_STATE.md`
- `PROMPTS/GATE_RESULTS.md`

按需维护：

- `IMPLEMENTATION_NOTES.md`
- `TEST_GUIDANCE.md`
- `TEST_RESULTS.md`
- `CHANGE_PROPOSALS.md`
- `IMPLICIT_REQUIREMENTS.md`
- `DECISIONS.md`

#### `TEST_GUIDANCE.md`
- 阶段角色：`user_test / Test Guidance`
- 记录：用户现在该怎么测、优先测什么、预期结果是什么、出现什么算失败
- 与 `TEST_RESULTS.md` 的区别：`TEST_GUIDANCE.md` 记录“怎么测”；`TEST_RESULTS.md` 记录“实际测到了什么”
- 默认更新时间：当收到执行器回执，且判断当前更适合先测试时，应优先更新或生成

### 最小记录粒度

#### `ROUND_INDEX.md`
- 记录：当前轮次、类型、目标、状态
- 粒度：一行即可，不写长回执

#### `PROGRESS.md`
- 记录：本轮做了什么、当前最重要未完成点
- 粒度：1~2 句关键结论 + 必要交付物

#### `PROJECT_STATE.md`
- 记录：当前阶段、当前结论、当前阻塞、下一步建议
- 粒度：站在主控视角写，不抄执行器原文

#### `PROMPTS/GATE_RESULTS.md`
- 记录：每次 Gate / re-gate 的结果摘要
- 粒度：输入类型、Gate 结论、下一步动作、PASS evidence 摘要

---

## 8. 最终输出协议

无论内部做了多少分析，给用户的最终输出优先只收敛成以下 4 类：

1. **下一段给 Cursor / Codex 的提示词**
2. **给用户的测试说明**
3. **给用户的阻塞提醒**
4. **给用户的最小澄清问题**

如果输出的是测试说明，默认先把 `TEST_GUIDANCE.md` 落好，再把其中最关键的测试入口、步骤、预期结果和失败判定直接发给用户。

不要默认给用户一大段内部流程解释。

如果用户明确要看内部判断，可以再附：
- 当前阶段
- 当前结论
- 为什么是这个下一步

但默认输出应以“可直接执行”为优先。

---

## 9. 陌生 agent 的最小阅读路径

下载 skill + tool 后，陌生 agent 至少读这 5 个文件就能开始：

1. `SKILL.md`
2. `docs/workflow.md`
3. `docs/default_collaboration_rules.md`
4. `docs/prompt_gate_protocol.md`
5. `product_dev_loop_tool/README.md`

如果当前任务是继续某个已有项目，再补读项目的：
- `PROJECT_STATE.md`
- `PRD.md`
- `PROGRESS.md`

这样就能知道：
- 默认口令怎么响应
- 什么情况该先 rewrite
- 什么情况该 re-gate
- 什么情况该先测试或先阻塞等待
- 什么情况该调用 tool，什么情况不该调用
