---
name: frappe-bench-site-ops
description: 在原生 bench 环境下运维站点、migrate、缓存与进程；用户提到 bench、站点、PVE 上 Frappe 运维时使用。真实执行命令后须写 audit。
---

# Frappe bench 站点运维

## 前置

- 确认目标 VM 与路径：查阅 `docs/aiot/env/`（`pve-vm.local.md` 或模板）。
- 大变更前：提醒按 `docs/aiot/runbooks/pre-change-snapshot.md` 做快照（若适用）。

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
