"""版本信息管理模块。"""

from pathlib import Path

import toml


def get_package_version() -> str:
    """获取当前包的版本号。"""
    try:
        # 尝试从包的根目录读取 pyproject.toml
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"

        if pyproject_path.exists():
            with open(pyproject_path) as f:
                data = toml.load(f)
            return data.get("project", {}).get("version", "unknown")

        # 如果找不到，返回默认值
        return "unknown"
    except Exception:
        return "unknown"
