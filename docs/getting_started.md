# Getting Started

## 先读什么文件

第一次使用这个合并仓库时，先按这个顺序阅读：

1. `README.md`
2. `skill/product_dev_loop/SKILL.md`
3. `skill/product_dev_loop/docs/default_collaboration_rules.md`
4. `tool/product_dev_loop_tool/README.md`

如果你的目标是继续某个已有项目，再补读：

1. `skill/product_dev_loop/docs/agent_handoff_quickstart.md`
2. `skill/product_dev_loop/docs/default_takeover_protocol.md`

## 典型用法一：只有原始需求

当你手上只有一段原始需求、功能清单、TODO 或 issue 打包时，默认不要直接把它当成可发给 Cursor 或 Codex 的正式 prompt。

建议顺序：

1. 先按 `skill/product_dev_loop` 的规则判断当前处于 `Discovery` 或 `Build Delegation` 前置阶段。
2. 进入 `tool/product_dev_loop_tool/`，先运行 `skeleton`。
3. 根据 `recommended_next_step` 判断是继续 rewrite、补最小澄清，还是值得 re-gate。
4. 只有在输入已接近正式 round prompt 时，再运行 `gate` 和必要的 `contract`。
5. 最后由 skill 把输出收敛成一段真正可派单的下一轮 prompt。

最常用命令：

```bash
cd tool/product_dev_loop_tool
python3 src/main.py skeleton --input examples/sample_raw_request.txt --json
python3 src/main.py gate --input examples/sample_raw_request.txt --json
```

## 典型用法二：已有项目推进中

当你已经有项目记录，或者用户只说“继续某项目”“给我某项目下一步”“继续喂 Cursor”，默认不要直接开写新 prompt。

建议顺序：

1. 先按 skill 的接管规则读取最小上下文。
2. 先判断当前输入更像：
   - 新需求
   - 执行器回执
   - 用户测试反馈
   - 外部阻塞
3. 如果当前最缺的是测试说明、记录更新或阻塞判断，就先做这些，不要强行调用 tool。
4. 只有当目标明确是“继续收口下一轮 prompt”时，再调用 `skeleton`、`gate` 或 `contract`。
5. 继续把最终输出收敛成一个最重要的交付物：下一段 prompt、测试说明、阻塞提醒或最小澄清问题。

## 默认短口令怎么理解

`skill/product_dev_loop/docs/default_collaboration_rules.md` 已经把这些短口令的默认行为写死了。第一次使用时，建议直接照那份规则执行。

常见短口令的默认含义：

- `继续`：先识别输入类型和当前阶段，再输出最合适的下一步动作。
- `继续某项目`：先做最小接管，再决定下一步。
- `给我某项目下一步`：优先收敛成一个默认下一步，而不是展开长分析。
- `继续喂 Cursor`：只有在当前状态适合继续派单时，才输出下一段 prompt。

## 什么时候调用 tool，什么时候不调用

应调用 `tool/product_dev_loop_tool` 的情况：

- 原始需求还没有收成稳定 round prompt，需要先跑 `skeleton`
- 怀疑当前只是伪合格 prompt，需要跑 `gate`
- 准备进入正式 Build Delegation，需要跑 `gate` 和 `contract`
- 已有一轮执行结果，准备收口下一轮 prompt，需要再次判断 `rewrite_more` 还是 `re_gate`

不必调用 tool 的情况：

- 当前只是生成用户可读测试说明
- 当前只是压缩记录或更新项目状态
- 当前明确是外部阻塞，问题不在 prompt 本身

## 一个最小闭环示例

下面是一个最小可复用闭环：

1. 读根 `README.md` 和 skill 规则。
2. 在 `tool/product_dev_loop_tool/` 运行：

```bash
cd tool/product_dev_loop_tool
python3 -m unittest discover -s tests -v
python3 src/main.py skeleton --input examples/sample_raw_request.txt --json
python3 src/main.py gate --input examples/sample_raw_request.txt
```

3. 根据 `skeleton` 和 `gate` 的结果，把原始需求 rewrite 成更稳定的一轮 prompt。
4. 在接近正式 Build Delegation 时，再补：

```bash
python3 src/main.py contract --input examples/sample_pass_prompt.txt --json
```

5. 由 skill 决定最终输出给执行器的 prompt 应该长什么样。
6. 执行器回执回来后，先更新项目记录或测试说明，再决定是否进入下一轮 prompt 收口。

## 公开仓库边界

这个仓库默认公开的是：

- 通用模板
- 文档
- 规则
- 示例
- 分析工具代码和测试

这个仓库默认不应该公开的是：

- API key
- 个人账号信息
- 私有项目上下文
- 真实业务数据

如果你要在本地维护真实项目，请把内容放在本地 `projects/` 目录，并保持忽略提交。
