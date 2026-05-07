#!/usr/bin/env python3
"""
Frappe REST 连通性与鉴权探测：`frappe.ping`、`frappe.auth.get_logged_user`。

用法::

	python scripts/agent_rest_smoke.py
	python scripts/agent_rest_smoke.py --base-url https://site.example

凭证优先级::

	命令行 ``--api-key`` / ``--api-secret`` >
	环境变量 ``FRAPPE_API_KEY`` / ``FRAPPE_API_SECRET`` >
	可选仓库 ``config/local.env``（或旧路径 ``scripts/agent_connect.local.env``），见 ``config/agent-connect.env.example``

依赖：Python 标准库 ``urllib``。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_lib = _SCRIPT_DIR / "lib"
if str(_lib) not in sys.path:
	sys.path.insert(0, str(_lib))

from env_loader import load_optional_repo_env


def _get(
	url: str,
	*,
	timeout: int,
	auth_header: str | None,
) -> tuple[int, str]:
	req = urllib.request.Request(url, method="GET")
	req.add_header("Accept", "application/json")
	if auth_header:
		req.add_header("Authorization", auth_header)
	try:
		with urllib.request.urlopen(req, timeout=timeout) as resp:
			raw = resp.read(8192)
			return resp.status, raw.decode("utf-8", errors="replace")
	except urllib.error.HTTPError as e:
		raw = e.read(8192)
		return int(e.code), raw.decode("utf-8", errors="replace")


def main() -> int:
	ap = argparse.ArgumentParser(description="Frappe REST 自检（ping + get_logged_user）")
	ap.add_argument(
		"--base-url",
		default=os.environ.get("FRAPPE_SITE_URL", "").rstrip("/"),
		help="站点根 URL（可与 REST API 同源），默认 FRAPPE_SITE_URL",
	)
	ap.add_argument("--api-key", default=os.environ.get("FRAPPE_API_KEY", ""))
	ap.add_argument("--api-secret", default=os.environ.get("FRAPPE_API_SECRET", ""))
	ap.add_argument(
		"--auth-header",
		default=os.environ.get("FRAPPE_AUTH_HEADER", ""),
		help="若已拼好完整 Authorization 值可直传（覆盖 key/secret）",
	)
	ap.add_argument("--timeout", type=int, default=20)
	ap.add_argument(
		"--no-env-file",
		action="store_true",
		help="不读取 config/local.env 与 scripts/agent_connect.local.env",
	)
	args = ap.parse_args()

	if not args.no_env_file:
		for p in load_optional_repo_env(no_env_file=False):
			print(f"Loaded env file: {p}")
		# reload defaults from env after file
		if not args.base_url:
			args.base_url = os.environ.get("FRAPPE_SITE_URL", "").rstrip("/")
		if not args.api_key:
			args.api_key = os.environ.get("FRAPPE_API_KEY", "")
		if not args.api_secret:
			args.api_secret = os.environ.get("FRAPPE_API_SECRET", "")
		if not args.auth_header:
			args.auth_header = os.environ.get("FRAPPE_AUTH_HEADER", "")

	if not args.base_url:
		print("ERROR: 缺少 base URL（--base-url 或 FRAPPE_SITE_URL）", file=sys.stderr)
		return 2

	if args.auth_header:
		auth_header = args.auth_header
	elif args.api_key and args.api_secret:
		auth_header = f"token {args.api_key}:{args.api_secret}"
	else:
		print(
			"ERROR: 缺少认证（--api-key/--api-secret、FRAPPE_* 或 FRAPPE_AUTH_HEADER）",
			file=sys.stderr,
		)
		return 2

	ok = True
	for label, path in (
		("frappe.ping", "/api/method/frappe.ping"),
		("get_logged_user", "/api/method/frappe.auth.get_logged_user"),
	):
		url = args.base_url + path
		status, body = _get(url, timeout=args.timeout, auth_header=auth_header)
		print(f"{label} GET {url}")
		print(f"  STATUS={status}")
		if body:
			try:
				parsed = json.loads(body)
				print("  BODY:", json.dumps(parsed, ensure_ascii=False)[:500])
			except json.JSONDecodeError:
				print("  BODY:", body[:500])
		if not (200 <= status < 300):
			ok = False
		print("")

	return 0 if ok else 1


if __name__ == "__main__":
	sys.exit(main())
