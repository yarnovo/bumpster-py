# 开发文档

本文档包含 `bump-version-py` 项目的开发相关信息。

## 项目结构

```
bump-version-py/
├── bump_version/               # 源代码
│   ├── __init__.py
│   ├── cli.py                 # 命令行接口（包含版本验证功能）
│   ├── version_manager.py     # 版本管理核心逻辑
│   ├── _version.py           # 版本信息管理
│   └── py.typed              # PEP 561 类型标记
├── tests/                     # 测试代码
│   ├── test_cli.py           # CLI 测试（包含版本验证测试）
│   ├── test_version_manager.py
│   └── test_integration.py
├── .github/                   # GitHub 配置
│   └── workflows/
│       └── ci-cd.yml         # CI/CD 流程
├── pyproject.toml            # 项目配置
├── pytest.ini                # 测试配置
├── Makefile                  # 开发任务
└── uv.lock                   # 依赖锁定文件
```

## 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/ai-app-base/bump-version-py.git
cd bumpster-py
```

### 2. 安装依赖

```bash
# 使用 uv 安装所有依赖（包括开发依赖）
uv sync
```

### 3. 开发模式安装

```bash
# 全局工具安装（推荐，类似 npm link）
uv tool install -e .

# 在当前虚拟环境中安装（仅用于测试）
uv pip install -e .
```

## 开发任务

### 使用 Makefile

```bash
# 格式化代码
make format

# 代码检查
make lint

# 类型检查
make type-check

# 运行测试
make test

# 运行所有检查
make all

# 构建包
make build

# 清理构建文件
make clean
```

### 手动命令

```bash
# 代码格式化
uv run ruff format bump_version/

# 代码检查
uv run ruff check bump_version/

# 类型检查
uv run pyright bump_version/

# 运行测试
uv run pytest

# 测试覆盖率
uv run pytest --cov=bump_version

# 构建
uv build

# 发布到 PyPI
uv publish
```

## 代码规范

### Python 版本

项目使用 Python 3.12+，配置在 `pyproject.toml` 中：

```toml
requires-python = ">=3.12"
```

### 代码风格

- 使用 `ruff` 进行代码格式化和检查
- 使用 `pyright` 进行类型检查
- 遵循 PEP 8 规范
- 所有函数和类需要类型注解

### 类型检查配置

`pyproject.toml` 中的 pyright 配置：

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "standard"
reportMissingImports = true
reportMissingTypeStubs = false
```

### Ruff 配置

```toml
[tool.ruff]
target-version = "py312"
line-length = 120

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "RUF"]
ignore = ["E501", "RUF001", "RUF002", "RUF003"]
```

## 测试

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_version_manager.py

# 运行特定测试
uv run pytest tests/test_version_manager.py::TestVersionParsing::test_parse_simple_version

# 详细输出
uv run pytest -v

# 显示打印输出
uv run pytest -s
```

### 测试覆盖率

```bash
# 生成覆盖率报告
uv run pytest --cov=bump_version --cov-report=html

# 查看报告
open htmlcov/index.html
```

### 编写测试

测试文件命名规则：`test_*.py`

```python
import pytest
from bump_version.version_manager import VersionManager

class TestVersionManager:
    def test_parse_version(self):
        vm = VersionManager()
        parts = vm.parse_version("1.0.0")
        assert parts.major == 1
        assert parts.minor == 0
        assert parts.patch == 0
```

## CI/CD

### GitHub Actions

项目使用 GitHub Actions 进行 CI/CD，配置文件：`.github/workflows/ci-cd.yml`

CI 流程：
1. 代码检查（ruff）
2. 类型检查（pyright）
3. 运行测试（pytest）
4. 版本标签验证（使用 validate_version）
5. 构建包（仅在标签推送时）
6. 发布到 PyPI（仅在标签推送时）

### 发布流程

1. 使用工具更新版本：
   ```bash
   bump
   ```

2. 工具自动完成：
   - 更新 pyproject.toml 版本号
   - 创建 Git 提交
   - 创建版本标签
   - 推送到 GitHub

3. GitHub Actions 自动：
   - 运行所有测试
   - 验证版本号格式
   - 构建包
   - 发布到 PyPI

## 版本管理

### 版本号规范

遵循 PEP 440：

- 正式版本：`X.Y.Z`
- 预发布版本：`X.Y.Za0`、`X.Y.Zb0`、`X.Y.Zrc0`
- 开发版本：`X.Y.Z.dev0`
- 后发布版本：`X.Y.Z.post0`

### Git 标签规范

- 格式：`vX.Y.Z`（自动添加 v 前缀）
- 示例：`v1.0.0`、`v1.0.0a0`

## 依赖管理

### 运行时依赖

在 `pyproject.toml` 的 `dependencies` 中定义：

```toml
dependencies = [
    "click>=8.1.0",
    "rich>=13.0.0",
    "inquirer>=3.1.0",
    "toml>=0.10.2",
    "packaging>=23.0",
]
```

### 开发依赖

在 `pyproject.toml` 的 `[dependency-groups.dev]` 中定义：

```toml
[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pyright>=1.1.0",
    "ruff>=0.1.0",
    "pre-commit>=3.5.0",
]
```

### 更新依赖

```bash
# 更新所有依赖
uv sync --upgrade

# 添加新依赖
uv add package-name

# 添加开发依赖
uv add --dev package-name

# 更新特定依赖到最新版本
uv add package-name@latest
```

## 调试

### 本地测试命令

```bash
# 直接运行模块
uv run python -m bump_version.cli

# 验证版本
uv run python -m bump_version.cli validate 1.0.0

# 使用 pdb 调试
uv run python -m pdb -m bump_version.cli
```

### VS Code 配置

创建 `.vscode/launch.json`：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug CLI",
            "type": "python",
            "request": "launch",
            "module": "bump_version.cli",
            "justMyCode": true
        }
    ]
}
```

## 贡献指南

1. Fork 项目
2. 创建功能分支：`git checkout -b feature/my-feature`
3. 提交更改：`git commit -m "feat: add new feature"`
4. 推送分支：`git push origin feature/my-feature`
5. 创建 Pull Request

### 提交信息规范

使用约定式提交：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式化
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建或辅助工具的变动

## 常见问题

### 1. 如何添加新的命令行参数？

在 `bump_version/cli.py` 中修改，使用 `click` 装饰器。

### 2. 如何支持新的配置文件格式？

在 `get_current_version()` 和 `update_version_in_file()` 函数中添加支持。

### 3. 如何添加新的预发布类型？

修改 `bump_version/version_manager.py` 中的 `PrereleaseType` 定义。

## 相关链接

- [PEP 440 - 版本标识和依赖规范](https://www.python.org/dev/peps/pep-0440/)
- [PEP 517 - Python 构建系统](https://www.python.org/dev/peps/pep-0517/)
- [PEP 621 - pyproject.toml 规范](https://www.python.org/dev/peps/pep-0621/)
- [Packaging 文档](https://packaging.python.org/)