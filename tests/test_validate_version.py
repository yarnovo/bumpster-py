"""测试版本验证功能"""

import subprocess
import sys

import pytest

from bump_version.validate_version import validate_version


class TestValidateVersion:
    """测试版本验证功能"""

    def test_valid_versions(self):
        """测试有效的版本号"""
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

    def test_invalid_versions(self):
        """测试无效的版本号"""
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

    def test_command_line_valid_version(self):
        """测试命令行接口 - 有效版本"""
        result = subprocess.run(
            [sys.executable, "-m", "bump_version.validate_version", "1.0.0"], capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "✅" in result.stdout
        assert "PEP 440 compliant" in result.stdout

    def test_command_line_invalid_version(self):
        """测试命令行接口 - 无效版本"""
        result = subprocess.run(
            [sys.executable, "-m", "bump_version.validate_version", "invalid-version"], capture_output=True, text=True
        )
        assert result.returncode == 1
        assert "❌" in result.stdout
        assert "not PEP 440 compliant" in result.stdout

    def test_command_line_no_args(self):
        """测试命令行接口 - 无参数"""
        result = subprocess.run([sys.executable, "-m", "bump_version.validate_version"], capture_output=True, text=True)
        assert result.returncode == 1
        assert "Usage:" in result.stdout

    def test_installed_command(self):
        """测试通过 pip 安装后的命令"""
        # 这个测试在包安装后才能运行
        # 可以通过 pytest -m installed 来运行
        pytest.skip("需要先安装包才能测试 validate-version 命令")
