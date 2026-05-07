#!/usr/bin/env python3
"""
部署自定义 App ``ssi_app`` 到 bench 服务器：**远端仓库单向 git pull**，再在 bench 根目录执行 ``migrate`` / ``build`` / ``restart``。

约定与本仓库 ``.cursor/rules/aiot-ssi-app-workflow.mdc`` 一致：**Git 同步为主线**，仅特殊情况使用 SCP。

用法::

	python scripts/deploy_ssi_app.py
	python scripts/deploy_ssi_app.py --dry-run
	python scripts/deploy_ssi_app.py --push
	python scripts/deploy_ssi_app.py --push --copy-chart-templates

环境变量（可选）::

	set DEPLOY_SSI_SSH_TARGET=frappe@10.0.0.40

服务器真实写入结束后请按 ``docs/aiot/audit/README.md`` 追加简报。
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_SSH_TARGET = os.environ.get("DEPLOY_SSI_SSH_TARGET", "frappe@10.0.0.40")
DEFAULT_SERVER_APP_PATH = "~/frappe-bench/apps/ssi_app"
DEFAULT_BENCH_ROOT = "~/frappe-bench"
DEFAULT_BRANCH = "develop"
DEFAULT_SITE = os.environ.get("DEPLOY_SSI_SITE", "10-0-0-40.sslip.io")


def _posix_single_quote(s: str) -> str:
	"""SSH 远端走 POSIX shell，勿使用 Windows 版 shlex.quote。"""
	return "'" + s.replace("'", "'\"'\"'") + "'"


def repo_root() -> Path:
	return Path(__file__).resolve().parents[1]


def local_ssi_app_dir() -> Path:
	return repo_root() / "apps" / "ssi_app"


def is_repo_dirty(app_dir: Path) -> tuple[bool, str]:
	r = subprocess.run(
		["git", "-C", str(app_dir), "status", "--porcelain"],
		capture_output=True,
		text=True,
	)
	if r.returncode != 0:
		return True, "无法获取 git 状态"
	out = (r.stdout or "").strip()
	return bool(out), out or "(无未提交变更)"


def print_audit_hint(*, server_app_path: str, dry_run: bool) -> None:
	print("")
	print("审计提示（简报见 docs/aiot/audit/README.md）：")
	print(f"  - Git：远端路径 {server_app_path}（仅 ssi_app 仓库），不写 frappe/erpnext 源码仓库内的手写补丁。")
	print("  - bench：migrate / build / restart 在 ~/frappe-bench 根目录执行。")
	if dry_run:
		print("  - [dry-run] 未执行 push / SSH。")
	print("")


def main() -> int:
	ap = argparse.ArgumentParser(description="部署 ssi_app：远端 git pull + bench migrate/build/restart")
	ap.add_argument("--dry-run", action="store_true", help="仅打印将要执行的命令，不写远端")
	ap.add_argument(
		"--push",
		action="store_true",
		help="部署前在本地 apps/ssi_app 执行 git push origin <branch>",
	)
	ap.add_argument(
		"--no-check-dirty",
		action="store_true",
		help="与 --push 联用时跳过本地脏目录检查（慎用）",
	)
	ap.add_argument("--ssh-target", default=DEFAULT_SSH_TARGET, help=f"SSH 目标，默认 {DEFAULT_SSH_TARGET}")
	ap.add_argument(
		"--server-path",
		default=DEFAULT_SERVER_APP_PATH,
		help=f"服务器上 ssi_app 路径，默认 {DEFAULT_SERVER_APP_PATH}",
	)
	ap.add_argument(
		"--bench-root",
		default=DEFAULT_BENCH_ROOT,
		help=f"bench 根目录，默认 {DEFAULT_BENCH_ROOT}",
	)
	ap.add_argument("--branch", default=DEFAULT_BRANCH, help=f"拉取分支，默认 {DEFAULT_BRANCH}")
	ap.add_argument("--site", default=DEFAULT_SITE, help=f"bench --site，默认 {DEFAULT_SITE}")
	ap.add_argument("--no-migrate", action="store_true", help="跳过 bench migrate")
	ap.add_argument("--no-build", action="store_true", help="跳过 bench build --app ssi_app")
	ap.add_argument("--no-restart", action="store_true", help="跳过 bench restart")
	ap.add_argument(
		"--copy-chart-templates",
		action="store_true",
		help="migrate 之后执行 copy_chart_templates（写入 erpnext verified 目录）",
	)
	args = ap.parse_args()

	local_app = local_ssi_app_dir()
	if args.push:
		if not local_app.is_dir():
			print(f"ERROR: 本地目录不存在：{local_app}")
			return 2
		if not (local_app / ".git").is_dir():
			print(f"ERROR: 非 git 仓库：{local_app}")
			return 2
		if not args.no_check_dirty:
			dirty, status = is_repo_dirty(local_app)
			if dirty:
				print("ERROR: ssi_app 存在未提交变更，push 不会带上工作区修改。")
				print("请先 commit，或使用 --no-check-dirty（不推荐）。")
				for line in status.splitlines():
					print(f"  {line}")
				return 2
		push_cmd = ["git", "-C", str(local_app), "push", "origin", args.branch]
		print("步骤 0: 本地 git push")
		print("  ", " ".join(push_cmd))
		if not args.dry_run:
			if subprocess.run(push_cmd).returncode != 0:
				print("ERROR: git push 失败")
				return 2
		print("")

	fetch_pull = (
		f"cd {args.server_path} && "
		f"git fetch origin && git checkout {args.branch} && git pull origin {args.branch}"
	)
	post: list[str] = []
	if not args.no_migrate:
		post.append(f"bench --site {args.site} migrate")
	if args.copy_chart_templates:
		post.append(
			f"bench --site {args.site} execute "
			f"ssi_app.ssi_accounts.copy_chart_templates.copy_chart_templates"
		)
	if not args.no_build:
		post.append("bench build --app ssi_app")
	if not args.no_restart:
		post.append("bench restart")

	post_str = " && ".join(post) if post else "true"
	remote_cmd = f"{fetch_pull} && cd {args.bench_root} && {post_str}"

	remote_argv = "bash -lc " + _posix_single_quote(remote_cmd)
	cmd = ["ssh", "-o", "BatchMode=yes", args.ssh_target, remote_argv]

	print("目标 SSH:", args.ssh_target)
	print("站点:", args.site)
	print_audit_hint(server_app_path=args.server_path, dry_run=args.dry_run)
	print("远端将要执行的 shell:")
	print(remote_cmd)
	print("")
	print("等价 SSH:")
	print(" ", "ssh", "-o", "BatchMode=yes", args.ssh_target, remote_argv)
	print("")

	if args.dry_run:
		return 0

	r = subprocess.run(cmd)
	if r.returncode != 0:
		print("ERROR: SSH / 远端命令失败")
		return 2
	print("部署流程已触发完成（请以远端日志与站点验收为准）。")
	return 0


if __name__ == "__main__":
	sys.exit(main())
