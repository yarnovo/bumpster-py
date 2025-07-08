## 项目开发规则约定

### 包名变更历史
- 原包名：`ai-app-base-bump-version`
- 新包名：`bumpster` (2025-07-08)

### 命令行工具
- 主命令：`bump`
- 别名：`bump-py`

## 开发注意事项

### 依赖管理
- 使用 `uv sync` 同步所有依赖（包括开发依赖）
- pyright 是 Python 包，通过 uv 管理，不需要 npm 安装

### 类型检查
- 运行命令：`make type-check` 或 `uv run pyright bump_version/`

<!-- 最后检查时间: 2025-07-08T05:29:00Z -->