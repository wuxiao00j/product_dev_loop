CORE_THEME_KEYWORDS: dict[str, list[str]] = {
    "generation": ["续写", "生成", "创作", "内容生成", "写作"],
    "style": ["风格引导", "风格", "语气", "风格控制"],
    "export": ["导出", "epub", "下载", "导出文件"],
    "cli": ["cli", "命令行", "命令"],
    "api": ["api", "接口", "endpoint"],
    "web_ui": ["web ui", "webui", "web", "ui", "前端", "页面", "网页"],
    "dependency": ["第三方", "依赖", "sdk", "权限", "环境", "接口契约"],
    "polish": ["优化", "体验", "文案", "交互", "风格优化", "引导优化"],
}

HIGH_RISK_COMBINATIONS = [
    {"generation", "style", "export"},
    {"cli", "api"},
    {"api", "web_ui"},
    {"cli", "web_ui"},
]
