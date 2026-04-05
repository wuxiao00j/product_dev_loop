CONTRACT_FIELD_PATTERNS: dict[str, list[str]] = {
    "project_round_stage_prd": ["项目名", "当前项目", "当前轮次", "当前阶段", "PRD 状态"],
    "task_type": ["任务类型", "本轮类型"],
    "round_goal": ["本轮目标", "本轮只解决", "这轮完成后"],
    "out_of_scope": ["不做", "保持不动", "out of scope"],
    "acceptance": ["验收标准", "验收项", "acceptance"],
    "dependency_fallback_blocker": ["关键依赖", "降级方案", "直接阻塞", "fallback", "blocker"],
    "structured_return": ["结构化回传", "已完成", "未完成", "关键代码信息", "风险与需确认点"],
    "test_requirement": ["测试要求", "测试入口", "操作步骤", "测试数据", "预期结果", "失败判定"],
    "prd_alignment": ["PRD 对照", "对应条目", "已满足", "未满足"],
}

WEAK_FALLBACK_PATTERNS = [
    "请说明",
    "视情况判断",
    "按需处理",
    "自行判断",
]

WHY_NOT_SPLIT_PATTERNS = [
    "Why not split",
    "为什么本轮不需要拆轮",
    "本轮不需要拆轮",
    "只是必要接线",
    "不是独立轮次",
]
