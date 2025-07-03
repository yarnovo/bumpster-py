"""版本管理核心功能模块。"""

import re
from dataclasses import dataclass
from typing import Literal

ReleaseType = Literal["major", "minor", "patch"]
PrereleaseType = Literal["a", "b", "rc", "dev", "post"]  # Python 风格的预发布类型


@dataclass
class VersionParts:
    """版本号组成部分。"""

    major: int
    minor: int
    patch: int
    prerelease_type: PrereleaseType | None = None
    prerelease_num: int | None = None
    local: str | None = None  # Python 支持本地版本标识符


class VersionManager:
    """版本管理器。"""

    def parse_version(self, version: str) -> VersionParts | None:
        """解析版本号，支持 PEP 440 格式。"""
        # 支持多种格式：
        # 1.0.0
        # 1.0.0a0, 1.0.0.alpha0
        # 1.0.0b1, 1.0.0.beta1
        # 1.0.0rc2, 1.0.0.rc2
        # 1.0.0.dev3, 1.0.0dev3
        # 1.0.0.post4, 1.0.0post4
        # 1.0.0+local.version

        # 移除可能的 'v' 前缀
        version = version.lstrip("v")

        # 正则表达式匹配 PEP 440 格式
        pattern = r"^(\d+)\.(\d+)\.(\d+)"  # 主版本号
        pattern += r"(?:"  # 预发布版本（可选）
        pattern += r"(?:\.)?(a|alpha|b|beta|rc|dev|post)(?:\.)?(\d+)"
        pattern += r"|"
        pattern += r"(a|b|rc|dev|post)(\d+)"  # 紧凑格式
        pattern += r")?"
        pattern += r"(?:\+([a-zA-Z0-9.]+))?$"  # 本地版本（可选）

        match = re.match(pattern, version)
        if not match:
            return None

        groups = match.groups()
        major = int(groups[0])
        minor = int(groups[1])
        patch = int(groups[2])

        # 解析预发布类型
        prerelease_type = None
        prerelease_num = None

        if groups[3]:  # 格式如 1.0.0.alpha0
            type_map = {"alpha": "a", "beta": "b", "rc": "rc", "dev": "dev", "post": "post", "a": "a", "b": "b"}
            prerelease_type = type_map.get(groups[3])
            prerelease_num = int(groups[4]) if groups[4] else 0
        elif groups[5]:  # 格式如 1.0.0a0
            prerelease_type = groups[5]
            prerelease_num = int(groups[6]) if groups[6] else 0

        local = groups[7] if len(groups) > 7 else None

        return VersionParts(
            major=major,
            minor=minor,
            patch=patch,
            prerelease_type=prerelease_type if prerelease_type in {"a", "b", "rc", "dev", "post"} else None,  # type: ignore
            prerelease_num=prerelease_num,
            local=local,
        )

    def get_next_version(
        self,
        current_version: str,
        release_type: ReleaseType,
        is_prerelease: bool,
        prerelease_type: PrereleaseType | None,
    ) -> str:
        """计算下一个版本号。"""
        version_parts = self.parse_version(current_version)
        if not version_parts:
            raise ValueError(f"无效的版本号格式: {current_version}")

        major = version_parts.major
        minor = version_parts.minor
        patch = version_parts.patch

        # 如果当前是预发布版本
        if version_parts.prerelease_type:
            if is_prerelease and prerelease_type:
                if prerelease_type == version_parts.prerelease_type:
                    # 相同类型：递增版本号
                    new_num = (version_parts.prerelease_num or 0) + 1
                    if prerelease_type in ["dev", "post"]:
                        return f"{major}.{minor}.{patch}.{prerelease_type}{new_num}"
                    else:
                        return f"{major}.{minor}.{patch}{prerelease_type}{new_num}"
                else:
                    # 不同类型：检查升级路径
                    # PEP 440 顺序: dev < a < b < rc < 正式版 < post
                    prerelease_order = ["dev", "a", "b", "rc"]

                    # 处理 post 版本的特殊情况
                    if version_parts.prerelease_type == "post":
                        # 从 post 版本只能继续 post 或者升级到新的主/次/修订版本
                        if prerelease_type == "post":
                            new_num = (version_parts.prerelease_num or 0) + 1
                            return f"{major}.{minor}.{patch}.post{new_num}"
                        else:
                            # 不允许从 post 回到其他预发布版本
                            raise ValueError(f"不能从 post 版本回到 {prerelease_type} 版本")
                    elif prerelease_type == "post":
                        # 不能从预发布版本直接到 post 版本
                        raise ValueError("不能从预发布版本直接升级到 post 版本，请先发布正式版本")

                    current_idx = (
                        prerelease_order.index(version_parts.prerelease_type)
                        if version_parts.prerelease_type in prerelease_order
                        else -1
                    )
                    new_idx = prerelease_order.index(prerelease_type) if prerelease_type in prerelease_order else -1

                    if new_idx > current_idx:
                        # 升级预发布类型
                        if prerelease_type in ["dev", "post"]:
                            return f"{major}.{minor}.{patch}.{prerelease_type}0"
                        else:
                            return f"{major}.{minor}.{patch}{prerelease_type}0"
                    else:
                        # 降级警告，但仍然允许
                        if prerelease_type in ["dev", "post"]:
                            return f"{major}.{minor}.{patch}.{prerelease_type}0"
                        else:
                            return f"{major}.{minor}.{patch}{prerelease_type}0"
            else:
                # 预发布 -> 正式版：去掉预发布后缀
                return f"{major}.{minor}.{patch}"
        else:
            # 当前是正式版本
            if is_prerelease and prerelease_type == "post":
                # 正式版本可以直接升级到 post 版本
                return f"{major}.{minor}.{patch}.post0"

            if release_type == "major":
                major += 1
                minor = 0
                patch = 0
            elif release_type == "minor":
                minor += 1
                patch = 0
            elif release_type == "patch":
                patch += 1

            new_version = f"{major}.{minor}.{patch}"

            if is_prerelease and prerelease_type and prerelease_type != "post":
                if prerelease_type == "dev":
                    new_version += f".{prerelease_type}0"
                else:
                    new_version += f"{prerelease_type}0"

            return new_version
