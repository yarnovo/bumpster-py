"""命令行工具测试。"""

import subprocess
from pathlib import Path

from tests.conftest import (
    get_version_from_pyproject,
    get_version_from_setup_py,
)


def run_bump_version(cwd: Path, env_vars: dict | None = None) -> subprocess.CompletedProcess:
    """运行 bump-version 命令。"""
    import os
    import sys

    env = {
        **os.environ,  # 保留当前环境变量
        "BUMP_VERSION_SKIP_PUSH": "true",  # 测试时跳过推送
        **(env_vars or {}),
    }

    # 使用当前 Python 解释器
    result = subprocess.run(
        [sys.executable, "-m", "bump_version.cli"], cwd=cwd, env=env, capture_output=True, text=True
    )
    return result


class TestCLI:
    """测试命令行工具的基本功能。"""

    def test_show_help_without_config(self, temp_dir):
        """测试在没有配置文件的目录中运行。"""
        result = run_bump_version(temp_dir)

        # 应该报错并退出
        assert result.returncode == 1
        assert "未找到 Python 项目配置文件" in result.stdout

    def test_show_version_info(self, project_with_pyproject):
        """测试显示版本信息。"""
        project_path = project_with_pyproject["path"]

        # 创建一个会立即退出的环境（模拟用户取消）
        result = run_bump_version(project_path, {"BUMP_VERSION_AUTO_EXIT": "1"})

        # 检查输出包含版本信息
        assert "当前版本: 1.0.0" in result.stdout
        assert "配置文件: pyproject.toml" in result.stdout
        assert "当前分支: main" in result.stdout


class TestVersionManager:
    """测试版本管理功能（不依赖交互式输入）。"""

    def test_version_parsing_and_bumping(self):
        """测试版本解析和升级逻辑。"""
        from bump_version.version_manager import VersionManager

        manager = VersionManager()

        # 测试简单版本升级
        assert manager.get_next_version("1.0.0", "patch", False, None) == "1.0.1"
        assert manager.get_next_version("1.0.0", "minor", False, None) == "1.1.0"
        assert manager.get_next_version("1.0.0", "major", False, None) == "2.0.0"

        # 测试预发布版本
        assert manager.get_next_version("1.0.0", "patch", True, "a") == "1.0.1a0"
        assert manager.get_next_version("1.0.0a0", "patch", True, "a") == "1.0.0a1"
        assert manager.get_next_version("1.0.0a1", "patch", True, "b") == "1.0.0b0"


class TestGitIntegration:
    """测试 Git 集成功能。"""

    def test_check_clean_working_tree(self, project_with_pyproject):
        """测试工作区检查。"""
        from bump_version.cli import check_git_status

        project_path = project_with_pyproject["path"]

        # 切换到项目目录
        import os

        old_cwd = os.getcwd()
        os.chdir(project_path)

        try:
            # 干净的工作区应该返回 True
            assert check_git_status() is True

            # 创建未提交的文件
            (project_path / "test.txt").write_text("test")

            # 应该返回 False
            assert check_git_status() is False
        finally:
            os.chdir(old_cwd)

    def test_get_current_branch(self, project_with_pyproject):
        """测试获取当前分支。"""
        from bump_version.cli import get_current_branch

        project_path = project_with_pyproject["path"]

        import os

        old_cwd = os.getcwd()
        os.chdir(project_path)

        try:
            branch = get_current_branch()
            assert branch == "main"
        finally:
            os.chdir(old_cwd)


class TestConfigFileSupport:
    """测试不同配置文件的支持。"""

    def test_pyproject_toml_support(self, project_with_pyproject):
        """测试 pyproject.toml 支持。"""
        from bump_version.cli import get_current_version, update_version_file

        project_path = project_with_pyproject["path"]

        import os

        old_cwd = os.getcwd()
        os.chdir(project_path)

        try:
            # 获取当前版本
            version, config_type = get_current_version()
            assert version == "1.0.0"
            assert config_type == "pyproject.toml"

            # 更新版本
            update_version_file("1.1.0", config_type)

            # 验证更新
            new_version = get_version_from_pyproject(project_path)
            assert new_version == "1.1.0"
        finally:
            os.chdir(old_cwd)

    def test_setup_py_support(self, project_with_setup_py):
        """测试 setup.py 支持。"""
        from bump_version.cli import get_current_version, update_version_file

        project_path = project_with_setup_py["path"]

        import os

        old_cwd = os.getcwd()
        os.chdir(project_path)

        try:
            # 获取当前版本
            version, config_type = get_current_version()
            assert version == "1.0.0"
            assert config_type == "setup.py"

            # 更新版本
            update_version_file("2.0.0", config_type)

            # 验证更新
            new_version = get_version_from_setup_py(project_path)
            assert new_version == "2.0.0"
        finally:
            os.chdir(old_cwd)


class TestVersionValidation:
    """测试版本验证功能。"""

    def test_validate_valid_versions(self):
        """测试有效版本号的验证。"""
        from bump_version.cli import validate_version

        # 这些版本应该都是有效的
        valid_versions = [
            "1.0.0",
            "0.1.0",
            "2.5.3",
            "1.0.0a1",
            "1.0.0b2",
            "1.0.0rc1",
            "1.0.0.dev1",
            "1.0.0+build.123",
            "1.0.0-alpha.1",
            "2021.4.0",
            "1!1.0.0",  # epoch version
            "v1.0.0",  # v prefix is valid
            "1.a.0",  # letters in version parts are valid
            "1.0",  # two-part version is valid
            "1.0.0.0.0",  # multi-part version is valid
        ]

        for version in valid_versions:
            assert validate_version(version) is True, f"Version {version} should be valid"

    def test_validate_invalid_versions(self):
        """测试无效版本号的验证。"""
        from bump_version.cli import validate_version

        # 这些版本应该都是无效的
        invalid_versions = [
            "1.0.0-",  # 无效的预发布版本
            "abc",  # 非版本字符串
            "",  # 空字符串
            "1.0.0..dev1",  # 双点
            "1.0.0.invalid",  # 无效的后缀
            "1_0_0",  # 使用下划线
        ]

        for version in invalid_versions:
            assert validate_version(version) is False, f"Version {version} should be invalid"

    def test_validate_command_line_valid_version(self, temp_dir):
        """测试命令行验证有效版本。"""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "-m", "bump_version.cli", "validate", "1.0.0"], capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "✅" in result.stdout
        assert "PEP 440 compliant" in result.stdout

    def test_validate_command_line_invalid_version(self, temp_dir):
        """测试命令行验证无效版本。"""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "-m", "bump_version.cli", "validate", "invalid-version"], capture_output=True, text=True
        )
        assert result.returncode == 1
        assert "❌" in result.stdout
        assert "not PEP 440 compliant" in result.stdout

    def test_validate_command_line_help(self, temp_dir):
        """测试命令行验证的帮助信息。"""
        import subprocess
        import sys

        result = subprocess.run([sys.executable, "-m", "bump_version.cli", "--help"], capture_output=True, text=True)
        assert result.returncode == 0
        assert "Commands:" in result.stdout
        assert "validate" in result.stdout
        assert "验证版本号是否符合 PEP 440 规范" in result.stdout

    def test_validate_subcommand_help(self, temp_dir):
        """测试 validate 子命令的帮助信息。"""
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "-m", "bump_version.cli", "validate", "--help"], capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "验证版本号是否符合 PEP 440 规范" in result.stdout
        assert "示例:" in result.stdout
        assert "退出码:" in result.stdout
