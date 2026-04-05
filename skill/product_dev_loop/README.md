# product_dev_loop

在这个合并版仓库中，本 skill 位于 `skill/product_dev_loop/`。

`product_dev_loop` 是一套面向 AI 协作开发的主控型 workflow skill。  
`product_dev_loop` is a control-layer workflow skill for AI-assisted product development.

它的目标不是单纯生成 prompt，而是把原本容易散掉的开发协作过程沉淀成可复用闭环：  
It is designed not just to generate prompts, but to turn scattered AI collaboration into a reusable development loop:

**Discovery -> PRD Locking -> Build Delegation -> Feedback Capture -> Testing Guidance -> Next-step Decision**

它适合作为 Cursor、Claude Code、Codex 等编码执行器之上的“控制层 / 主控层”。  
It works as a **control layer** on top of coding agents such as Cursor, Claude Code, and Codex.

---

## 这是什么 / What is this

`product_dev_loop` 不是普通的 prompt 模板包，而是一套让 AI agent 更像“产品开发主控”的工作流 skill。  
`product_dev_loop` is not a simple prompt template pack. It is a workflow skill that helps an AI agent behave more like a **product/dev control layer**.

它帮助把以下过程串起来：  
It helps turn the following into a connected loop:

- 需求讨论 / discovery and requirement clarification
- PRD 起草与锁定 / PRD drafting and locking
- 派单给执行器开发 / implementation delegation to coding agents
- 执行器回执整理 / feedback capture from executors
- 用户可读测试说明 / user-readable testing guidance
- 下一步判断 / next-step recommendation
- 多项目接管与连续推进 / multi-project handoff and continuity

---

## 它解决什么问题 / What problem it solves

AI 协作开发最容易在这些地方失控：  
AI-assisted development often breaks down in the same places:

- 需求讨论完了，但没有沉淀成真正可用的 PRD  
  requirements are discussed, but never turned into a usable PRD
- prompt 退化成功能描述，没有边界、验收和回传要求  
  prompts drift into vague feature requests without scope, acceptance, or return structure
- 执行器只说“完成了”，但没有清晰的实现事实  
  coding agents say “done” without implementation truth
- 测试说明缺失，或者只有开发者看得懂  
  testing guidance is missing or too technical
- 用户反馈被直接抄成下一轮 prompt，越改越散  
  feedback gets copied straight into the next round and the project drifts
- 会话一断、新 agent 一接手，项目上下文就丢了  
  projects lose continuity when the session changes or a new agent takes over
- 多项目并行时，范围和记录容易串线  
  multiple projects get mixed together

`product_dev_loop` 就是为了解决这些问题。  
`product_dev_loop` exists to solve exactly these problems.

---

## 核心理念 / Core ideas

### 1. 普通需求描述不等于合格 prompt  
### 1. A feature description is not a qualified delegation prompt

一个可执行的 round prompt 至少要写清：  
A usable round prompt should define at least:

- 当前项目与轮次 / current project and round
- PRD 状态 / PRD status
- 本轮目标 / this round’s goal
- 本轮做什么 / what is in scope
- 本轮不做什么 / what is out of scope
- 验收标准 / acceptance criteria
- 结构化回传要求 / structured return format
- 测试要求 / testing expectations
- PRD 对照要求 / PRD comparison requirements

### 2. PRD locked 后不能随意改  
### 2. Locked PRDs should not be casually edited

PRD 一旦 locked，范围变化不应直接写回 PRD，而要先经过变更提议。  
Once a PRD is locked, scope changes should not be written directly into the PRD. They should go through change proposal handling first.

### 3. 执行器回执不是原样归档对象  
### 3. Executor feedback is not raw archive material

长回执应该被压缩成不同用途的项目记录：  
Long executor responses should be compressed into structured project records:

- `PROGRESS.md`
- `IMPLEMENTATION_NOTES.md`
- `TEST_GUIDANCE.md`
- `TEST_RESULTS.md`
- `PROJECT_STATE.md`

### 4. 测试说明必须用户可读  
### 4. Testing guidance must be user-readable

测试说明不是写给开发者自己看的，而是要让产品、老板或测试者能直接照着测。  
Testing guidance is not only for developers. It should tell a product owner, founder, or tester exactly how to validate the round.

### 5. 连续性优先  
### 5. Continuity matters

新 agent 应该能在最小摩擦下接手项目继续推进。  
A new agent should be able to resume a project with minimal friction.

---

## 核心能力 / Key capabilities

- 需求澄清与 Discovery 工作流 / discovery workflow for clarifying scope
- PRD 起草与锁定纪律 / PRD drafting and locking discipline
- 开发派单 prompt 引导 / delegation prompt guidance
- build / fix / polish / unblock 四类任务收口 / task-type-specific prompting
- prompt 自检与评分机制 / prompt checklist and scoring rubric
- 反馈分类与下一轮映射 / feedback classification and next-round mapping
- 执行器长回执压缩 / implementation feedback compression
- 用户可读测试说明生成 / user-readable testing guidance generation
- 阶段切换判断 / stage transition decisions
- 默认项目接管协议 / default project takeover protocol
- 多项目隔离与连续推进 / multi-project isolation and continuity

---

## 默认工作流 / Default workflow

这个 skill 围绕 5 个固定阶段工作：  
This skill is organized around five fixed stages:

1. **Discovery**
2. **PRD**
3. **Build Delegation**
4. **Test Guidance**
5. **Feedback Capture**

基本约束：  
Core operating rules:

- 计划没收敛，不进入执行  
  do not enter execution before planning is converged
- 没有执行结果，不进入反馈处理  
  do not enter feedback handling without execution results
- 没判断清楚反馈，不直接开下一轮  
  do not start a new round before feedback is interpreted
- 不把执行器自评直接当事实  
  do not treat executor self-evaluation as final truth
- 不在未确认情况下改 locked PRD  
  do not edit locked PRDs without explicit confirmation

---

## 默认接管行为 / Default takeover behavior

`product_dev_loop` 最重要的设计目标之一是连续性。  
One of the most important design goals of `product_dev_loop` is continuity.

当用户说：  
If a user says things like:

- 继续项目 X / continue project X
- 接手项目 X / take over project X
- 跟进项目 X / follow up on project X
- 看看项目 X 现在到哪了 / check where project X is now

这个 skill 的默认动作不是直接执行，而是：**先接管，再行动**。  
…the skill should not jump directly into action. Its default behavior is: **take over first, then act**.

默认接管逻辑：  
Default takeover logic:

1. 识别项目 / identify the project
2. 读取 handoff quickstart / read the handoff quickstart
3. 读取 `PROJECT_STATE.md`
4. 读取 `PRD.md`
5. 读取 `PROGRESS.md`
6. 按需补读 `IMPLEMENTATION_NOTES.md`、`TEST_RESULTS.md`、`TEST_GUIDANCE.md`、`ROUND_INDEX.md`  
   read additional files as needed
7. 输出结构化接管摘要 / output a structured takeover summary
8. 再判断下一步 / only then decide the next action

如果项目身份或范围有歧义，优先做最小补问，而不是猜。  
If the project identity or scope is ambiguous, the skill should use minimal clarification rather than guessing.

---

## 仓库结构 / Repository structure

```text
skill/product_dev_loop/
├── SKILL.md
├── README.md
├── .gitignore
├── docs/
│   ├── workflow.md
│   ├── agent_handoff_quickstart.md
│   ├── default_takeover_protocol.md
│   ├── prompt_generation_guide.md
│   ├── prompt_generation_flow.md
│   ├── task_type_prompt_guide.md
│   ├── feedback_to_prompt_mapping.md
│   ├── implementation_feedback_compression_guide.md
│   ├── test_guidance_generation_guide.md
│   ├── stage_transition_decision_card.md
│   └── ...
├── templates/
│   ├── round_prompt_template.txt
│   ├── round_prompt_by_type_template.txt
│   ├── takeover_summary_template.md
│   ├── takeover_clarification_template.md
│   ├── test_guidance_template.md
│   └── ...
├── examples/
│   ├── default_takeover_example.md
│   ├── agent_handoff_example.md
│   ├── prompt_build_example.txt
│   ├── prompt_fix_example.txt
│   ├── takeover_to_prompt_example.md
│   ├── takeover_to_feedback_capture_example.md
│   ├── takeover_to_test_guidance_example.md
│   └── takeover_to_next_step_example.md
└── projects/   # 本地项目目录，默认不上传 / ignored from GitHub upload
```

---

## 怎么使用 / How to use

### 基本使用 / Basic use
当你希望 AI agent 管的不只是“写一段代码”，而是整个项目推进闭环时，使用这个 skill。  
Use this skill when you want an AI agent to manage the full development loop, not just generate one-off coding output.

典型请求：  
Typical requests:

- "Use product_dev_loop to continue project X"
- "Use product_dev_loop to turn this idea into a PRD"
- "Use product_dev_loop to generate the next round prompt"
- "Use product_dev_loop to review this executor feedback and tell me what to test"

### 首次进入 / First-time entry
如果一个 agent 是第一次进入这个 skill，建议从这里开始：  
If an agent is entering the skill for the first time, start from:

1. `docs/agent_handoff_quickstart.md`
2. `SKILL.md`
3. `docs/workflow.md`

然后再按任务目标走对应阅读路径。  
Then follow the task-specific reading path.

### 与编码执行器的关系 / Working with coding agents
这个 skill 不取代 Cursor / Claude Code / Codex，而是与它们配合：  
This skill does not replace Cursor / Claude Code / Codex. It works with them.

- `product_dev_loop` = 控制层 / control layer
- Cursor / Claude Code / Codex = 执行层 / execution layer

---

## 适合谁 / Who this is for

如果你符合这些情况，这个 skill 会很有用：  
This skill is useful if you:

- 经常多轮使用 AI 编码工具 / work repeatedly with AI coding tools across multiple rounds
- 希望 PRD 和范围能被稳住 / want PRDs and scope to stay stable
- 需要比普通需求描述更强的派单 prompt / need better delegation prompts than plain feature requests
- 希望测试和反馈也是正式流程的一部分 / want feedback and testing to be part of the workflow
- 希望项目在换会话、换 agent 后还能接续 / want projects to survive session changes and agent handoff
- 想把 AI 协作开发做成可复用工作系统 / want a reusable operating system for AI-assisted product development

如果你只是想让 AI 临时写个小脚本，它可能有点重。  
It is probably overkill if you only want a one-off code snippet or a very short task.

---

## 当前状态 / Current status

`product_dev_loop` 当前仍是一套**文档驱动的 workflow skill**。  
`product_dev_loop` is currently a **document-driven workflow skill**.

它的重点在于：  
It focuses on:

- 协议 / protocol
- 结构 / structure
- 接管 / handoff
- 判断规则 / decision rules
- 模板 / templates
- 示例 / examples

它不是自动化 runtime，也不是完整编排引擎。  
It does not try to be a fully automated runtime or orchestration engine.

它的价值在于：让高质量 AI 协作开发变得**可复制、可控、可接力**。  
Its value is making high-quality AI collaboration **repeatable, controllable, and handoff-friendly**.

---

## 方法论 / Philosophy

`product_dev_loop` 提供秩序，我来提供判断。  
`product_dev_loop` provides the structure. A strong controlling agent provides the judgment.

最好的使用方式不是死板自动化，而是把：  
The best use of this skill is not rigid automation, but a combination of:

- 稳定的工作流纪律 / stable workflow discipline
- 清晰的项目记录 / clear project records
- 强主控判断 / strong control decisions

一句话总结：  
In short:

**它负责让项目不散。**  
**It keeps the project from falling apart.**

**强主控负责让项目不僵。**  
**A strong operator keeps it from becoming rigid.**
