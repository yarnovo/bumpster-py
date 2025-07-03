#!/usr/bin/env python
"""验证版本号是否符合 PEP 440 规范"""

import sys

from packaging.version import InvalidVersion, Version


def validate_version(version_string):
    """验证版本号是否符合 PEP 440 规范"""
    try:
        Version(version_string)
        print(f"✅ Version {version_string} is PEP 440 compliant")
        return True
    except InvalidVersion:
        print(f"❌ Version '{version_string}' is not PEP 440 compliant")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: validate_version.py <version>")
        sys.exit(1)

    version = sys.argv[1]
    if validate_version(version):
        sys.exit(0)
    else:
        sys.exit(1)
