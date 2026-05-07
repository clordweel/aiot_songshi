#!/usr/bin/env python3
"""
FAC MCP HTTP Endpoint 连通性探测：发送 JSON-RPC ``initialize``（只读）。

若未配置 ``FAC_MCP_URL``（或 ``FRAPPE_MCP_URL``），打印 skip 并以状态码 0 退出。

用法::

	python scripts/agent_mcp_ping.py
	python scripts/agent_mcp_ping.py --url https://site/api/method/frappe_assistant_core.api.fac_endpoint.handle_mcp

鉴权 ``--auth``::

	auto — 优先 ``FAC_MCP_TOKEN``：若为 ``key:secret`` 且无空格则用 ``token key:secret``，否则 ``Bearer``；
	       否则退回 ``FRAPPE_API_KEY`` + ``FRAPPE_API_SECRET`` 组成 ``token …``
	bearer / token / none — 固定策略

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


def _post_json(url: str, *, auth_header: str | None, body: dict, timeout: int) -> tuple[int, str]:
	headers = {"Content-Type": "application/json", "Accept": "application/json"}
	if auth_header:
		headers["Authorization"] = auth_header
	data = json.dumps(body, ensure_ascii=False).encode("utf-8")
	req = urllib.request.Request(url, data=data, headers=headers, method="POST")
	try:
		with urllib.request.urlopen(req, timeout=timeout) as resp:
			raw = resp.read(8192)
			return resp.status, raw.decode("utf-8", errors="replace")
	except urllib.error.HTTPError as e:
		raw = e.read(8192)
		return int(e.code), raw.decode("utf-8", errors="replace")


def _build_auth_header(mode: str) -> str | None:
	key = os.environ.get("FRAPPE_API_KEY", "")
	sec = os.environ.get("FRAPPE_API_SECRET", "")
	token = os.environ.get("FAC_MCP_TOKEN", "").strip()

	if mode == "none":
		return None
	if mode == "bearer":
		return f"Bearer {token}" if token else None
	if mode == "token":
		if key and sec:
			return f"token {key}:{sec}"
		return None

	# auto
	if token:
		if ":" in token and " " not in token:
			return f"token {token}"
		return f"Bearer {token}"
	if key and sec:
		return f"token {key}:{sec}"
	return None


def main() -> int:
	ap = argparse.ArgumentParser(description="FAC MCP initialize 探测（可选跳过）")
	ap.add_argument(
		"--url",
		default=os.environ.get("FAC_MCP_URL") or os.environ.get("FRAPPE_MCP_URL") or "",
		help="MCP endpoint；默认 FAC_MCP_URL / FRAPPE_MCP_URL",
	)
	ap.add_argument(
		"--auth",
		choices=("auto", "bearer", "token", "none"),
		default="auto",
	)
	ap.add_argument("--timeout", type=int, default=20)
	ap.add_argument(
		"--no-env-file",
		action="store_true",
	)
	args = ap.parse_args()

	if not args.no_env_file:
		for p in load_optional_repo_env(no_env_file=False):
			print(f"Loaded env file: {p}")
		if not args.url:
			args.url = os.environ.get("FAC_MCP_URL") or os.environ.get("FRAPPE_MCP_URL") or ""

	args.url = args.url.strip()
	if not args.url:
		print("SKIP: FAC_MCP_URL / FRAPPE_MCP_URL 未配置（FAC 未装或未填写时可忽略）")
		return 0

	auth_header = _build_auth_header(args.auth)

	payload = {
		"jsonrpc": "2.0",
		"method": "initialize",
		"params": {"protocolVersion": "2025-03-26", "capabilities": {}},
		"id": 1,
	}

	status, text = _post_json(args.url, auth_header=auth_header, body=payload, timeout=args.timeout)
	print(f"MCP_ENDPOINT={args.url}")
	print(f"STATUS={status}")
	if auth_header:
		scheme = auth_header.split()[0]
		print(f"Authorization=present ({scheme} …)")
	else:
		print("Authorization=(none)")
	print("BODY:")
	print(text[:4000])

	return 0 if (200 <= status < 300) else 1


if __name__ == "__main__":
	sys.exit(main())
