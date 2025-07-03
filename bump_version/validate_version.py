#!/usr/bin/env python
"""验证版本号是否符合 PEP 440 规范"""

import sys

from packaging.version import InvalidVersion, Version


def validate_version(version_string: str) -> bool:
    """验证版本号是否符合 PEP 440 规范

    Args:
        version_string: 要验证的版本号字符串

    Returns:
        bool: 如果版本号符合 PEP 440 规范返回 True，否则返回 False
    """
    try:
        Version(version_string)
        print(f"✅ Version {version_string} is PEP 440 compliant")
        return True
    except InvalidVersion:
        print(f"❌ Version '{version_string}' is not PEP 440 compliant")
        return False


def main() -> None:
    """命令行入口点"""
    if len(sys.argv) != 2:
        print("Usage: validate-version <version>")
        sys.exit(1)

    version = sys.argv[1]
    if validate_version(version):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
