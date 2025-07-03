# 部署文档

本文档介绍 `bump-version-py` 项目的 CI/CD 配置和自动化部署流程。

## GitHub Actions 概述

项目使用 GitHub Actions 实现自动化的持续集成和部署。配置文件位于 `.github/workflows/ci-cd.yml`。

## CI/CD 工作流程

### 触发条件

```yaml
on:
  push:
    branches: [ main ]
    tags:
      - '*'
  pull_request:
    branches: [ main ]
```

工作流程在以下情况触发：
- 推送到 main 分支
- 推送任何标签
- 针对 main 分支的 Pull Request

### 完整流程

1. **代码质量检查**
   - Ruff 格式检查
   - Ruff 代码检查
   - Pyright 类型检查

2. **测试**
   - 运行所有单元测试
   - 生成测试报告

3. **版本验证**（仅标签触发）
   - 验证标签是否为有效的 PEP 440 版本

4. **构建**（仅标签触发）
   - 构建 Python 包

5. **发布**（仅标签触发）
   - 发布到 PyPI

## 详细配置说明

### 环境设置

```yaml
jobs:
  CI-CD:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
```

### uv 工具安装

```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v3
  with:
    enable-cache: true
    cache-dependency-glob: |
      **/uv.lock
      **/requirements*.txt
      **/pyproject.toml
```

特点：
- 启用缓存以加速构建
- 缓存基于依赖文件的哈希值

### 依赖安装

```yaml
- name: Install dependencies
  run: |
    uv sync
```

使用 `uv sync` 确保依赖版本与 `uv.lock` 完全一致。

### 代码质量检查

```yaml
- name: Run linting
  run: |
    uv run ruff check bump_version/

- name: Run type checking
  run: |
    uv run pyright bump_version/
```

### 测试运行

```yaml
- name: Run tests
  run: |
    uv run pytest
```

### 版本标签处理

```yaml
- name: Check if this is a version tag
  id: check_tag
  run: |
    if [[ "$GITHUB_REF" == refs/tags/* ]]; then
      TAG="${GITHUB_REF#refs/tags/}"
      echo "tag=$TAG" >> $GITHUB_OUTPUT
      echo "is_tag=true" >> $GITHUB_OUTPUT
      
      # 移除可能的 'v' 前缀
      if [[ "$TAG" =~ ^v(.*)$ ]]; then
        TAG="${BASH_REMATCH[1]}"
      fi
      
      # 使用包内的验证功能验证 PEP 440 版本号格式
      if uv run python -m bump_version.cli validate "$TAG"; then
        echo "version=$TAG" >> $GITHUB_OUTPUT
      else
        exit 1
      fi
    else
      echo "is_tag=false" >> $GITHUB_OUTPUT
    fi
```

这个步骤：
1. 检查是否为标签推送
2. 提取标签名称
3. 移除 'v' 前缀（如果有）
4. 使用项目内的验证工具验证版本号
5. 将结果输出供后续步骤使用

### 构建包

```yaml
- name: Build package
  if: steps.check_tag.outputs.is_tag == 'true'
  run: |
    uv build
```

仅在标签推送时执行构建。

### 发布到 PyPI

```yaml
- name: Publish to PyPI
  if: steps.check_tag.outputs.is_tag == 'true'
  env:
    UV_PUBLISH_USERNAME: __token__
    UV_PUBLISH_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
  run: |
    uv publish
```

使用 PyPI API Token 进行身份验证。

## 设置 PyPI 发布

### 1. 获取 PyPI API Token

1. 登录 [PyPI](https://pypi.org/)
2. 进入账户设置 -> API tokens
3. 创建新的 API token
   - Token 名称：`bump-version-py`
   - 范围：选择特定项目或整个账户

### 2. 配置 GitHub Secrets

1. 在 GitHub 仓库页面，进入 Settings -> Secrets and variables -> Actions
2. 点击 "New repository secret"
3. 创建密钥：
   - Name: `PYPI_API_TOKEN`
   - Value: 粘贴从 PyPI 获取的 token

## 发布流程

### 自动发布（推荐）

1. 使用工具更新版本：
   ```bash
   bvp
   # 选择版本类型和升级方式
   ```

2. 工具自动完成：
   - 更新 pyproject.toml 版本号
   - 创建 Git 提交：`chore: release X.Y.Z`
   - 创建 Git 标签：`vX.Y.Z`
   - 推送到 GitHub（包括标签）

3. GitHub Actions 自动触发：
   - 运行所有检查和测试
   - 验证版本号格式
   - 构建 Python 包
   - 发布到 PyPI

### 手动发布

如果需要手动创建版本：

```bash
# 1. 更新版本号
# 编辑 pyproject.toml 中的 version 字段

# 2. 提交更改
git add pyproject.toml
git commit -m "chore: release X.Y.Z"

# 3. 创建标签
git tag -a vX.Y.Z -m "Release X.Y.Z"

# 4. 推送
git push origin main --follow-tags
```

## 工作流程状态

### 查看构建状态

1. 在 GitHub 仓库页面点击 "Actions" 标签
2. 查看最近的工作流程运行
3. 点击具体运行查看详细日志

### 状态徽章

在 README 中添加构建状态徽章：

```markdown
[![CI/CD](https://github.com/ai-app-base/bump-version-py/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/ai-app-base/bump-version-py/actions/workflows/ci-cd.yml)
```

## 故障排查

### 常见问题

1. **版本号验证失败**
   - 确保标签格式正确（如 `v1.0.0`）
   - 版本号必须符合 PEP 440 规范

2. **PyPI 发布失败**
   - 检查 `PYPI_API_TOKEN` 是否正确配置
   - 确认 token 有发布权限
   - 检查包名是否已被占用

3. **测试失败**
   - 查看具体的测试输出
   - 在本地运行 `uv run pytest` 复现问题

### 调试技巧

1. **本地测试 GitHub Actions**
   ```bash
   # 安装 act
   # https://github.com/nektos/act
   
   # 运行工作流程
   act push
   ```

2. **查看环境变量**
   在工作流程中添加调试步骤：
   ```yaml
   - name: Debug
     run: |
       echo "GitHub Ref: $GITHUB_REF"
       echo "Tag: ${{ steps.check_tag.outputs.tag }}"
       echo "Version: ${{ steps.check_tag.outputs.version }}"
   ```

## 最佳实践

1. **版本管理**
   - 始终使用 `bvp` 工具管理版本
   - 遵循语义化版本规范
   - 在发布前充分测试

2. **分支保护**
   - 设置 main 分支保护规则
   - 要求 PR 通过所有检查
   - 禁止直接推送到 main

3. **发布检查清单**
   - [ ] 所有测试通过
   - [ ] 更新 CHANGELOG（如有）
   - [ ] 代码审查完成
   - [ ] 文档已更新

## 扩展配置

### 添加更多 Python 版本测试

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']

steps:
- name: Set up Python ${{ matrix.python-version }}
  uses: actions/setup-python@v5
  with:
    python-version: ${{ matrix.python-version }}
```

### 添加测试覆盖率报告

```yaml
- name: Run tests with coverage
  run: |
    uv run pytest --cov=bump_version --cov-report=xml

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

### 添加发布通知

```yaml
- name: Notify release
  if: steps.check_tag.outputs.is_tag == 'true'
  run: |
    # 发送通知到 Slack、Discord 等
```

## 相关资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [uv 文档](https://github.com/astral-sh/uv)
- [PyPI 发布指南](https://packaging.python.org/tutorials/packaging-projects/)
- [PEP 440 - 版本标识规范](https://www.python.org/dev/peps/pep-0440/)