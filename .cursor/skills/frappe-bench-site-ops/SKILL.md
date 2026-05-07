---
name: frappe-bench-site-ops
description: 在原生 bench 环境下运维站点、migrate、缓存与进程；用户提到 bench、站点、PVE 上 Frappe 运维时使用。真实执行命令后须写 audit。
---

# Frappe bench 站点运维

## 前置

- 确认目标 VM 与路径：先读 [server-baseline.md](../../../docs/aiot/env/server-baseline.md)；涉密补充见 `docs/aiot/env/pve-vm.local.md`。
- **重大变更 / 高风险**（大版本升级、大规模 `migrate`、危险数据导入、生产切换、存储/内核类操作）：**先提醒** 操作者取得 **可恢复快照** — **PVE VM 快照**（首选）或宿主若使用 **LVM** 且策略允许则评估 **LVM 快照**；见 [pre-change-snapshot.md](../../../docs/aiot/runbooks/pre-change-snapshot.md)。
- **ERPNext 线**：目标为官方 **`develop`**（v17 开发线，如 `17.0.0-dev`）；以目标机 `apps/erpnext`、`bench version` 与官方文档为准。
- **运行用户**：`bench` 应在 **专用 Unix 用户**（如 `frappe`）下执行；避免长期 root 跑 `bench`。

## 概念

- **bench 根目录**：通常含 `apps/`、`sites/`、`env/`；当前 site 由 `sites/currentsite.txt` 或 `bench use` 指定。
- **常用命令**（顺序与必要性依场景而定，勿机械套用）：
  - `bench use <site>` — 切换上下文
  - `bench migrate` — 应用 schema 变更后
  - `bench clear-cache` — 清缓存
  - `bench restart` — 重启进程（依 bench 版本可能对应 supervisor/systemd）

## 代理注意

- 执行任何在目标机上产生**实际效果**的 `bench`/shell 命令后：按 `docs/aiot/audit/README.md` 写一条简报（环境、命令摘要、结果；**勿**贴密钥）。
- 不在技能中重复官方长文档；不确定时引导查 Context7 / Frappe 官方文档或现场 `bench --help`。
