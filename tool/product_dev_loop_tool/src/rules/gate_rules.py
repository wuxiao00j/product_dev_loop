TASK_TYPE_PATTERNS: dict[str, list[str]] = {
    "build": ["本轮类型：`build`", "任务类型：`build`", " task type", " build", "开发", "实现", "新增"],
    "fix": ["本轮类型：`fix`", "任务类型：`fix`", "修复", "修 bug", "bugfix", "fix"],
    "polish": ["本轮类型：`polish`", "任务类型：`polish`", "优化", "体验优化", "polish"],
    "unblock": ["本轮类型：`unblock`", "任务类型：`unblock`", "解阻", "阻塞解除", "unblock"],
}

AMBIGUOUS_PATTERNS = [
    "继续这个项目",
    "继续上个项目",
    "接手这个项目",
    "继续上一轮",
    "按之前那个来",
    "那个项目",
    "这个需求",
]

PASS_EVIDENCE_PATTERNS = {
    "prompt_gate_pass": ["Prompt Gate：`PASS`", "Prompt Gate:`PASS`", "Prompt Gate: `PASS`"],
    "round_main_closure": ["Round main closure", "唯一主闭环", "本轮唯一主闭环"],
    "why_not_split": ["Why not split", "为什么本轮不需要拆轮", "本轮不需要拆轮"],
    "fallback_blocker_rule": ["Fallback / blocker rule", "降级方案", "直接阻塞", "blocker"],
    "delegation_contract": ["Delegation contract：`satisfied`", "Delegation contract: `satisfied`", "Delegation contract：`satisfied`"],
}

SECTION_PATTERNS = {
    "goal": ["本轮目标", "本轮只解决", "round goal", "这轮完成后"],
    "out_of_scope": ["本轮边界", "不做", "out of scope", "保持不动"],
    "acceptance": ["验收标准", "验收项", "acceptance"],
    "dependency": ["依赖与降级规则", "关键依赖", "fallback", "blocker", "降级方案", "直接阻塞"],
    "structured_return": ["结构化回传", "已完成", "未完成", "关键代码信息", "风险与需确认点"],
    "test": ["测试要求", "测试入口", "操作步骤", "测试数据", "预期结果", "失败判定"],
    "prd_alignment": ["PRD 对照", "PRD alignment", "对应条目", "已满足", "未满足"],
}
