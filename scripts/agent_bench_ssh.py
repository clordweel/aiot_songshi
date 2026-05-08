#!/usr/bin/env python3
"""
通过 SSH 在远端 frappe-bench 执行一条 ``bench`` 命令（默认 ``bench version``），用于 Agent 链路基线自检。

用法::

	python scripts/agent_bench_ssh.py --dry-run
	python scripts/agent_bench_ssh.py
	python scripts/agent_bench_ssh.py --remote-command "bench --site SITE migrate"

环境变量::

	AIOT_SSH_TARGET / AIOT_BENCH_ROOT（推荐）；兼容 AGENT_BENCH_*；可选 ``config/local.env``

服务器真实写入结束后请在仓库根目录 ``audits/`` 追加简报（字段见 ``docs/aiot/AUDITS.md``）。
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_lib = _SCRIPT_DIR / "lib"
if str(_lib) not in sys.path:
	sys.path.insert(0, str(_lib))

from env_loader import load_optional_repo_env


def _posix_single_quote(s: str) -> str:
	return "'" + s.replace("'", "'\"'\"'") + "'"


def _ssh_target() -> str:
	return (
		os.environ.get("DEPLOY_SSI_SSH_TARGET", "").strip()
		or os.environ.get("AIOT_SSH_TARGET", "").strip()
		or os.environ.get("AGENT_BENCH_SSH_TARGET", "").strip()
		or "frappe@10.0.0.40"
	)


def _bench_root() -> str:
	return (
		os.environ.get("AIOT_BENCH_ROOT", "").strip()
		or os.environ.get("AGENT_BENCH_ROOT", "").strip()
		or "~/frappe-bench"
	)


def main() -> int:
	ap = argparse.ArgumentParser(description="SSH 至 bench 主机执行 bench 单行自检")
	ap.add_argument("--ssh-target", default=None)
	ap.add_argument("--bench-root", default=None)
	ap.add_argument(
		"--remote-command",
		default="bench version",
		help="在 bench 根目录下执行的命令（默认 bench version）",
	)
	ap.add_argument("--dry-run", action="store_true")
	ap.add_argument("--no-env-file", action="store_true")
	args = ap.parse_args()

	if not args.no_env_file:
		for p in load_optional_repo_env(no_env_file=False):
			print(f"Loaded env file: {p}")

	if args.ssh_target is None:
		args.ssh_target = _ssh_target()
	if args.bench_root is None:
		args.bench_root = _bench_root()

	remote_cmd = f"cd {args.bench_root} && {args.remote_command}"
	remote_argv = "bash -lc " + _posix_single_quote(remote_cmd)
	cmd = ["ssh", "-o", "BatchMode=yes", args.ssh_target, remote_argv]

	print("SSH:", args.ssh_target)
	print("远端:", remote_cmd)
	print("等价:", " ".join(cmd))
	print("")

	if args.dry_run:
		return 0

	r = subprocess.run(cmd)
	return 0 if r.returncode == 0 else 2


if __name__ == "__main__":
	sys.exit(main())
