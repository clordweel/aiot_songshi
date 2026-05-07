"""
从仓库内 env 文件合并默认值（不覆盖操作系统已 export 的变量）。

优先级（同一键 latter wins，仅当键尚未在 os.environ 中设置时写入）：
1. ``scripts/agent_connect.local.env``（旧路径，deprecated）
2. ``config/local.env``（推荐）

加载顺序实现为：先解析 legacy，再解析 config，最后用合并结果逐项 ``setdefault`` 语义 —
等价于：config 覆盖 legacy 中定义的键（对脚本进程内首次导入时生效）。
"""

from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
	"""仓库根目录（含 ``config/``、``scripts/``）。"""
	return Path(__file__).resolve().parents[2]


def _parse_env_file(path: Path) -> dict[str, str]:
	out: dict[str, str] = {}
	try:
		raw = path.read_text(encoding="utf-8")
	except OSError:
		return out
	for line in raw.splitlines():
		line = line.strip()
		if not line or line.startswith("#"):
			continue
		if "=" not in line:
			continue
		key, _, val = line.partition("=")
		key = key.strip()
		val = val.strip().strip('"').strip("'")
		if key:
			out[key] = val
	return out


def merge_repo_env_files() -> dict[str, str]:
	legacy = repo_root() / "scripts" / "agent_connect.local.env"
	preferred = repo_root() / "config" / "local.env"
	merged: dict[str, str] = {}
	if legacy.is_file():
		merged.update(_parse_env_file(legacy))
	if preferred.is_file():
		merged.update(_parse_env_file(preferred))
	return merged


def apply_repo_env(merged: dict[str, str]) -> None:
	for key, val in merged.items():
		if key and key not in os.environ:
			os.environ[key] = val


def load_optional_repo_env(*, no_env_file: bool = False) -> list[Path]:
	"""
	将仓库 env 合并结果应用到 ``os.environ``。
	返回实际存在的 env 文件路径列表（用于打印提示）。
	"""
	if no_env_file:
		return []
	r = repo_root()
	candidates = [r / "scripts" / "agent_connect.local.env", r / "config" / "local.env"]
	paths_exist = [p for p in candidates if p.is_file()]
	if not paths_exist:
		return []
	merged = merge_repo_env_files()
	apply_repo_env(merged)
	return paths_exist
