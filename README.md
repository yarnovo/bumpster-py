# bump-version-py

专为 Python 项目设计的智能语义化版本管理命令行工具。

## 安装

### 使用 pip 全局安装（类似 npm install -g）

```bash
# 使用 pip
pip install bump-version

# 或使用 pipx（推荐，自动隔离环境）
pipx install bump-version

# 或使用 uv
uv tool install bump-version
```

### 开发安装（本地测试）

```bash
# 克隆仓库
git clone https://github.com/ai-app-base/bump-version-py.git
cd bump-version-py

# 使用 uv 安装依赖
uv sync  # 会自动安装所有依赖（包括开发依赖）并使用 uv.lock 确保版本一致

# 开发模式安装（类似 npm link）
uv pip install -e .  # 在当前虚拟环境中安装

# 或者全局安装用于测试（推荐）
uv tool install -e .  # 全局安装开发版本，类似 npm link 的效果
```

#### uv 开发安装说明

- `uv pip install -e .`：在当前虚拟环境中以可编辑模式安装
  - 只在当前虚拟环境中可用
  - 适合项目内部开发测试

- `uv tool install -e .`：全局安装开发版本（推荐）
  - 在任何地方都可以使用 `bump-version-py` 或 `bvp` 命令
  - 代码修改会立即生效，无需重新安装
  - 完全等同于 npm link 的效果
  - 工具会被安装到独立的虚拟环境中，避免依赖冲突

## 使用方式

安装后，你可以在任何 Python 项目目录中使用：

```bash
# 完整命令
bump-version-py

# 简短别名
bvp
```

## Python 全局命令说明

Python 支持多种全局安装 CLI 工具的方式：

### 1. **pip install（传统方式）**
```bash
pip install bump-version
```
- 安装到系统 Python 或虚拟环境
- 命令会添加到 `~/.local/bin`（Linux/Mac）或 `Scripts`（Windows）
- 需要确保路径在 PATH 环境变量中

### 2. **pipx（推荐）**
```bash
# 安装 pipx
python -m pip install --user pipx
python -m pipx ensurepath

# 使用 pipx 安装
pipx install bump-version
```
- 每个工具自动隔离在独立虚拟环境
- 自动管理 PATH
- 避免依赖冲突

### 3. **uv tool（现代方式）**
```bash
# 使用 uv 安装全局工具
uv tool install bump-version
```
- uv 的 `tool install` 命令类似 pipx
- 自动创建隔离环境
- 性能更快

## 功能特性

- ✅ 专为 Python 项目设计
- ✅ 支持 pyproject.toml（现代 Python 项目）
- ✅ 支持 setup.py（传统 Python 项目）
- ✅ 遵循 PEP 440 版本规范
- ✅ 支持预发布版本（alpha、beta、rc、dev）
- ✅ Git 集成（自动提交、打标签、推送）
- ✅ 交互式命令行界面
- ✅ 安全检查（分支、工作区状态）

## 版本格式

遵循 PEP 440 规范：

```
1.0.0       # 正式版本
1.0.0a0     # Alpha 版本
1.0.0b0     # Beta 版本  
1.0.0rc0    # Release Candidate
1.0.0.dev0  # 开发版本（Python 特有）
```

## 配置文件支持

自动检测并更新以下 Python 项目配置文件：

1. **pyproject.toml**（推荐，现代 Python 项目标准）
   ```toml
   [project]
   version = "1.0.0"
   
   # 或 Poetry 项目
   [tool.poetry]
   version = "1.0.0"
   ```

2. **setup.py**（传统 Python 项目）
   ```python
   setup(
       name="my-package",
       version="1.0.0",
       ...
   )
   ```

## 开发

```bash
# 安装所有依赖（包括开发依赖）
uv sync

# 运行测试
uv run pytest

# 代码格式化
uv run black bump_version/
uv run ruff check bump_version/

# 类型检查
uv run mypy bump_version/
```

## 构建和发布

```bash
# 构建包
uv build

# 发布到 PyPI
uv publish
```

## 使用示例

### 基本使用

假设你有一个 Python 项目，`pyproject.toml` 内容如下：

```toml
[project]
name = "my-python-library"
version = "1.0.0"
description = "My awesome Python library"
```

运行 `bvp` 后：

1. 选择 "正式版本 (Production)"
2. 选择 "Patch (修订号)"
3. 确认执行

结果：
- `pyproject.toml` 中的版本更新为 `1.0.1`
- Git 提交信息：`chore: release 1.0.1`
- Git 标签：`v1.0.1`

### 预发布版本

创建 Alpha 版本：
```bash
bvp
# 选择 "Alpha 版本"
# 选择 "Minor (次版本号)"
# 版本：1.0.0 → 1.1.0a0（注意是 a0，不是 -alpha.0）
```

### 完整工作流程

```bash
# 1. 在 Python 项目根目录（包含 pyproject.toml）
cd my-python-project

# 2. 运行版本管理工具
bvp

# 3. 交互式选择版本类型和升级方式

# 4. 工具自动完成：
#    - 更新 pyproject.toml 中的版本号
#    - git add pyproject.toml
#    - git commit -m "chore: release X.Y.Z"
#    - git tag -a vX.Y.Z -m "Release X.Y.Z"
#    - git push --follow-tags（如果没有设置 BUMP_VERSION_SKIP_PUSH）

# 5. 发布到 PyPI（需要手动执行）
uv build
uv publish
```

## 版本号格式对比

| 类型 | JavaScript (npm) | Python (PEP 440) |
|------|------------------|------------------|
| 正式版 | 1.0.0 | 1.0.0 |
| Alpha | 1.0.0-alpha.0 | 1.0.0a0 |
| Beta | 1.0.0-beta.0 | 1.0.0b0 |
| RC | 1.0.0-rc.0 | 1.0.0rc0 |
| Dev | - | 1.0.0.dev0 |

## 命令说明

Python 版本提供两个命令：

- `bump-version-py`：完整命令名
- `bvp`：简短别名（bump version python 的缩写）

## 许可证

ISC