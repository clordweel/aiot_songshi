#!/usr/bin/env python3
"""
将仓库根目录 ``audits/`` 下的简报 Markdown 按**文件名中的日期/时间**筛选后打成 zip。

简报命名约定见 ``docs/aiot/AUDITS.md``::

	YYYY-MM-DD_HHmmss_slug.md   → 视为该秒的时刻点
	YYYY-MM-DD_slug.md          → 视为当日全天（00:00:00～23:59:59.999999）

未匹配上述模式的文件（如 ``README.md``）默认跳过；可用 ``--include-extra`` 一并打入。

用法::

	python scripts/pack_audits.py --dry-run
	python scripts/pack_audits.py --since 2026-05-08 --until 2026-05-09
	python scripts/pack_audits.py --since "2026-05-08 09:00:00" --until "2026-05-08T18:30:00"
	python scripts/pack_audits.py --since-date 2026-05-08 --until-date 2026-05-08 -o tmp/my-audits.zip

默认输出：``tmp/audits-pack_<UTC时间戳>.zip``（``tmp/`` 在仓库根目录）。
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from datetime import date, datetime, time, timezone
from pathlib import Path


_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent


def _parse_bound(raw: str, *, is_until: bool) -> datetime:
	s = raw.strip()
	if len(s) == 10 and s[4] == "-" and s[7] == "-":
		d = date.fromisoformat(s)
		if is_until:
			return datetime.combine(d, time.max)
		return datetime.combine(d, time.min)
	normalized = s.replace(" ", "T", 1)
	try:
		dt = datetime.fromisoformat(normalized)
	except ValueError as e:
		raise argparse.ArgumentTypeError(f"无法解析日期时间: {raw!r} ({e})") from e
	return dt


def _filename_window(name: str) -> tuple[datetime, datetime] | None:
	"""若可解析则返回 (window_start, window_end) 闭区间，否则 None。"""
	if not name.endswith(".md"):
		return None
	stem = name[:-3]
	m = re.match(r"^(\d{4}-\d{2}-\d{2})_(.+)$", stem)
	if not m:
		return None
	d_str, rest = m.group(1), m.group(2)
	try:
		d = date.fromisoformat(d_str)
	except ValueError:
		return None
	# rest: either "HHmmss_slug" or "slug"
	if len(rest) >= 7 and rest[:6].isdigit() and rest[6] == "_":
		hhmmss = rest[:6]
		h, mi, s = int(hhmmss[:2]), int(hhmmss[2:4]), int(hhmmss[4:6])
		try:
			t = time(h, mi, s)
		except ValueError:
			return None
		point = datetime.combine(d, t)
		return (point, point)
	start = datetime.combine(d, time.min)
	end = datetime.combine(d, time.max)
	return (start, end)


def _ranges_overlap(
	a0: datetime, a1: datetime, b0: datetime | None, b1: datetime | None
) -> bool:
	if b0 is not None and a1 < b0:
		return False
	if b1 is not None and a0 > b1:
		return False
	return True


def _collect_files(
	audits_dir: Path,
	since: datetime | None,
	until: datetime | None,
	*,
	include_extra: bool,
) -> list[Path]:
	out: list[Path] = []
	for p in sorted(audits_dir.iterdir()):
		if not p.is_file():
			continue
		win = _filename_window(p.name)
		if win is None:
			if include_extra:
				out.append(p)
			continue
		a0, a1 = win
		if _ranges_overlap(a0, a1, since, until):
			out.append(p)
	return out


def main(argv: list[str] | None = None) -> int:
	parser = argparse.ArgumentParser(description="按日期时间范围打包 audits/ 简报为 zip")
	parser.add_argument(
		"--audits-dir",
		type=Path,
		default=_REPO_ROOT / "audits",
		help="简报目录（默认：仓库根目录 audits/）",
	)
	parser.add_argument(
		"--since",
		type=lambda s: _parse_bound(s, is_until=False),
		default=None,
		help="起始（含）。纯日期 YYYY-MM-DD 视为当日 00:00:00",
	)
	parser.add_argument(
		"--until",
		type=lambda s: _parse_bound(s, is_until=True),
		default=None,
		help="结束（含）。纯日期 YYYY-MM-DD 视为当日 23:59:59.999999",
	)
	parser.add_argument(
		"--since-date",
		type=lambda s: _parse_bound(s, is_until=False),
		default=None,
		help="与 --since 相同，便于只写日期",
	)
	parser.add_argument(
		"--until-date",
		type=lambda s: _parse_bound(s, is_until=True),
		default=None,
		help="与 --until 相同，便于只写日期",
	)
	parser.add_argument(
		"-o",
		"--output",
		type=Path,
		default=None,
		help="输出 zip 路径（默认 tmp/audits-pack_<timestamp>.zip）",
	)
	parser.add_argument(
		"--include-extra",
		action="store_true",
		help="纳入无法按文件名解析日期的文件（如 README.md）",
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="只列出将打入的文件，不写 zip",
	)
	parser.add_argument(
		"--list",
		action="store_true",
		help="同 --dry-run",
	)
	parser.add_argument(
		"-v",
		"--verbose",
		action="store_true",
		help="写入 zip 时仍将匹配文件名列 stdout（默认静默仅 stderr 汇总）",
	)
	args = parser.parse_args(argv)

	since = args.since or args.since_date
	until = args.until or args.until_date

	audits_dir: Path = args.audits_dir.resolve()
	if not audits_dir.is_dir():
		print(f"错误：目录不存在：{audits_dir}", file=sys.stderr)
		return 2

	matched = _collect_files(
		audits_dir, since, until, include_extra=args.include_extra
	)
	if not matched:
		print("没有匹配的文件（检查范围参数与 audits/ 内容）。", file=sys.stderr)
		return 1

	show_names = args.dry_run or args.list or args.verbose
	for p in matched:
		if show_names:
			print(p.relative_to(audits_dir))
	if args.dry_run or args.list:
		print(f"共 {len(matched)} 个文件", file=sys.stderr)
		return 0

	out_path = args.output
	if out_path is None:
		tmp_dir = _REPO_ROOT / "tmp"
		tmp_dir.mkdir(parents=True, exist_ok=True)
		tag = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
		out_path = tmp_dir / f"audits-pack_{tag}.zip"
	else:
		out_path = out_path.resolve()
		out_path.parent.mkdir(parents=True, exist_ok=True)

	prefix = audits_dir.name + "/"
	with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
		for p in matched:
			arc = prefix + p.name
			zf.write(p, arcname=arc)

	print(f"已写入：{out_path}（{len(matched)} 个文件）", file=sys.stderr)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
