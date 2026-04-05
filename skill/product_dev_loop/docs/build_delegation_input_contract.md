# Build Delegation Input Contract

这份文档定义 `Build Delegation` 的输入契约。

它解决的问题不是“如何写好 prompt”，而是：

- 什么输入有资格进入 `Build Delegation`
- 什么输入必须被卡在入口外

硬规则先写在前面：

- `Build Delegation` 只接受已经通过 `Prompt Gate` 的 round prompt
- 任何未通过 `Prompt Gate PASS` 的输入，禁止进入 `Build Delegation`
- 用户原始任务块、功能清单、issue 列表、TODO 打包，默认都不属于合法输入
- 输入契约满足只是必要条件，不是充分条件
- 字段齐全，不等于已经通过 Gate

## 1. 合法输入的定义

一个合法的 `Build Delegation` 输入，必须同时满足两层条件：

### 第一层：Gate 条件

- 已拿到 `Prompt Gate = PASS`

### 第二层：字段条件

输入里必须同时具备：

- `project / round / stage / PRD status`
- `task type`
- `round goal`
- `out of scope`
- `acceptance`
- `dependency + fallback / blocker`
- `structured return`
- `test requirement`
- `PRD alignment`

缺任一项，都不应视为合法输入。

注意：

- 就算以上字段都齐，也仍然可能是 `pseudo-qualified prompt`
- 所以输入契约满足，只代表“形式上可检查”
- 不代表“已经证明本轮是单轮主闭环”

## 2. Build Delegation 必收字段

### 1. project / round / stage / PRD status

必须明确：

- 当前项目
- 当前轮次
- 当前阶段
- 当前 PRD 状态

缺失后果：

- 容易串项目、串轮次、串边界

### 2. task type

必须明确：

- `build / fix / polish / unblock`

缺失后果：

- 执行器无法稳定判断本轮优先级和边界

### 3. round goal

必须明确：

- 本轮只解决什么
- 本轮完成后用户能直接看到什么变化

缺失后果：

- 输入会退化成愿景列表或任务池

### 4. out of scope

必须明确：

- 本轮不做
- 保持不动

缺失后果：

- 执行器默认可以顺手扩做

### 5. acceptance

必须明确：

- 外部可判断的验收标准

缺失后果：

- 主 agent 无法判断本轮是否真正完成

### 6. dependency + fallback / blocker

必须明确：

- 关键依赖
- 依赖满足时怎么做
- 依赖不满足时允许的降级方案
- 哪些情况直接阻塞

缺失后果：

- 执行器会自行编方案，或把阻塞误当实现任务

### 7. structured return

必须明确：

- 已完成
- 未完成
- 关键代码信息
- 特殊状态
- 风险与需确认点

缺失后果：

- 回执无法稳定进入收口流程

### 8. test requirement

必须明确：

- 测试入口
- 操作步骤
- 测试数据
- 预期结果
- 失败判定

缺失后果：

- 结果不可验证

### 9. PRD alignment

必须明确：

- 本轮对应哪些 PRD 条目
- 已满足哪些
- 未满足哪些
- 当前是否达成本轮验收

缺失后果：

- 实现结果可能偏离 PRD 却被误判为通过

## 2.1 为什么字段齐全仍然可能不够

下面这种输入，字段可能都在，但仍然不能进 `Build Delegation`：

- 已写 `task type`
- 已写 `project / round / stage / PRD status`
- 已写 `test requirement`
- 已写 `structured return`
- 但目标里同时塞了导出、续写、风格引导、CLI、API、UI 六项

原因：

- 输入契约字段齐，只证明形式完整
- 不证明已经收成单轮主闭环
- 不证明 `why-not-split` 成立
- 不证明 fallback / blocker 规则有效

所以这类输入仍应被视为：

- `pseudo-qualified prompt`

正确动作：

- 不放行
- 回到 Gate
- 继续判 `REWRITE_REQUIRED`

## 3. Build Delegation 必须拒收的输入

出现下列任一情况，`Build Delegation` 应拒绝接收：

### 1. Gate 结果不是 PASS

包括：

- `REWRITE_REQUIRED`
- `CLARIFICATION_REQUIRED`

### 2. 输入仍像 raw request

包括：

- 功能清单
- issue 列表
- 多模块打包需求
- 含多个主闭环的大包任务

### 3. 缺少输入契约关键字段

即使其他内容很多，只要缺以下任一项，也应拒收：

- `project / round / stage / PRD status`
- `task type`
- `round goal`
- `out of scope`
- `acceptance`
- `dependency + fallback / blocker`
- `structured return`
- `test requirement`
- `PRD alignment`

### 4. 字段齐全但仍未提供 PASS evidence

包括：

- 没有 `Round main closure`
- 没有 `Why not split`
- 没有明确 `Fallback / blocker rule`
- 没有 `Delegation contract: satisfied`

### 5. 字段齐全但仍属于 pseudo-qualified prompt

包括：

- 多主闭环混合
- 多个核心能力主题并列必做
- 验收项无法收成一个主闭环
- fallback / blocker 规则无效

### 6. PRD locked 后夹带范围变化

包括：

- 新能力
- 验收变化
- 方向偏移

正确动作：

- 先转入 `CHANGE_PROPOSALS.md`
- 或将本轮目标收缩回不改 PRD 的范围

## 4. 合法输入的最小形态

一个最小合法输入，至少应具备：

1. 一份 `Prompt Gate` 结果，且结论为 `PASS`
2. 一份合格 round prompt
3. 一份明确 `PASS evidence`

如果只有其一，也不算完整合法输入。

## 5. 这个输入契约真正卡住了什么

它卡住的是这些常见坏输入：

- “帮我把这些都做了，做完告诉我”
- “页面、接口、导出、权限一起补一下”
- “看情况你自己判断怎么拆”
- “先把 CLI / API / Web UI 全铺上”
- “先都做出来，验收后面再补”

这些输入即使很长，也不得绕过 Gate 直接进入 `Build Delegation`。
