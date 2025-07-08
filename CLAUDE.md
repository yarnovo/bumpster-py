# Bumpster - Python 语义化版本管理工具

## 项目概述

Bumpster 是一个专为 Python 项目设计的智能语义化版本管理命令行工具，遵循 PEP 440 规范，支持自动更新项目版本号、创建 Git 提交和标签，简化版本发布流程。

### 项目元信息
- **包名**: `bumpster` (原名: `ai-app-base-bump-version`)
- **版本**: 0.1.1
- **Python 版本要求**: >=3.12
- **许可证**: ISC
- **命令行工具**: `bump` (主命令), `bump-py` (别名)
- **仓库地址**: https://github.com/yarnovo/bumpster-py
- **包名变更日期**: 2025-07-08

## 技术栈

### 核心技术
- **语言**: Python 3.12+
- **包管理器**: uv (现代 Python 包管理工具)
- **构建系统**: Hatchling (基于 PEP 517/621)

### 运行时依赖
- **click** (>=8.1.0): 命令行接口框架
- **rich** (>=13.0.0): 终端美化和格式化输出
- **inquirer** (>=3.1.0): 交互式命令行提示
- **tomlkit** (>=0.12.0): TOML 文件解析和修改（保留格式）
- **packaging** (>=23.0): PEP 440 版本号解析和验证

### 开发依赖
- **pytest** (>=7.0.0): 测试框架
- **pytest-cov** (>=4.0.0): 测试覆盖率
- **pyright** (>=1.1.0): 静态类型检查器
- **ruff** (>=0.1.0): 快速的 Python linter 和格式化工具
- **pre-commit** (>=3.5.0): Git 钩子管理

## 项目结构

```
bump_version/               # 源代码目录
├── __init__.py            # 包初始化文件
├── _version.py            # 版本信息管理模块
├── cli.py                 # 命令行接口主模块（入口点）
├── version_manager.py     # 版本管理核心逻辑
└── py.typed               # PEP 561 类型标记
```

### 核心模块说明
- **cli.py**: Click 基础的 CLI 实现，提供 `main()` 入口和 `validate` 子命令
- **version_manager.py**: 版本号解析、验证和升级的核心业务逻辑
- **_version.py**: 动态读取 pyproject.toml 中的版本信息

## 开发工作流

### 环境设置
```bash
# 删除虚拟环境后需要重新设置
rm -rf .venv
uv sync                    # 同步所有依赖
make pre-commit           # 重新安装 pre-commit 钩子（重要！）
```

### 常用命令
- `make sync`: 同步依赖
- `make format`: 使用 ruff 格式化代码
- `make lint`: 运行代码检查
- `make type-check`: 运行 pyright 类型检查
- `make test`: 运行所有测试
- `make check`: 运行 lint + type-check
- `make all`: 运行所有检查和测试
- `make build`: 构建发布包
- `make dev-install-global`: 全局安装开发版本

### 代码质量标准
- **Ruff 配置**:
  - 目标版本: Python 3.12
  - 行长限制: 120 字符
  - 启用规则: E, W, F, I, B, UP, RUF
  - 忽略规则: E501 (行长), RUF001-003 (Unicode 相关)

- **Pyright 配置**:
  - 类型检查模式: standard
  - 报告缺失的导入
  - 允许未知类型（部分情况）

## Git 工作流

### Pre-commit 钩子
- 自动运行 ruff 格式化和检查
- 在提交前确保代码质量
- 支持 pre-commit 和 pre-push 钩子

### 版本发布流程
1. 使用 `bump` 命令交互式选择版本升级
2. 工具自动更新 pyproject.toml 中的版本号
3. 创建符合规范的 Git 提交（如: "chore: release 0.1.2"）
4. 创建 Git 标签（如: "v0.1.2"）
5. 可选：推送到远程仓库

## CI/CD 流程

### GitHub Actions 工作流
- **触发条件**: main 分支推送、标签推送、Pull Request
- **流程步骤**:
  1. 代码检查 (ruff)
  2. 类型检查 (pyright)
  3. 测试运行 (pytest)
  4. 版本验证
  5. 构建包
  6. 发布到 PyPI（仅标签触发）

## 注意事项

### 依赖管理
- 使用 `uv sync` 同步所有依赖（包括开发依赖）
- pyright 是 Python 包，通过 uv 管理，不需要 npm 安装
- 删除 .venv 后必须重新运行 `make pre-commit` 安装钩子

### 版本管理
- 完全遵循 PEP 440 规范
- 支持正式版、预发布版（alpha/beta/rc）、开发版、后发布版
- 使用 packaging 库进行版本解析和验证

### 测试策略
- 测试标记: @pytest.mark.slow, @pytest.mark.integration, @pytest.mark.unit
- 使用 pytest-cov 生成覆盖率报告
- 集成测试包括 Git 操作和文件系统操作

## 开发提示

1. **修改代码前**：确保 pre-commit 钩子已安装
2. **提交代码前**：运行 `make check` 确保通过所有检查
3. **发布新版本**：使用 `bump` 命令，不要手动修改版本号
4. **类型检查失败**：确保已运行 `uv sync` 安装 pyright
5. **更新代码后**：检查并更新相关文档
   - README.md - 项目说明和使用指南
   - TESTING.md - 测试指南和本地安装
   - DEVELOPMENT.md - 开发环境和流程
   - DEPLOYMENT.md - 部署和发布流程

## 项目迁移记录

### 2025-07-08 项目重要变更
1. **包名变更**: `ai-app-base-bump-version` → `bumpster`
2. **命令变更**: `bump-version-py`/`bvp` → `bump`/`bump-py`
3. **仓库迁移**: `github.com/ai-app-base/bump-version-py` → `github.com/yarnovo/bumpster-py`
4. **新增文档**: TESTING.md - 详细的测试指南和本地安装说明

### 重要操作记录
- 删除 .venv 后必须执行 `make pre-commit` 重新安装 Git 钩子
- pyright 是 Python 包，通过 `uv sync` 安装，不是通过 npm

<!-- 最后检查时间: 2025-07-08T06:22:36.352Z -->