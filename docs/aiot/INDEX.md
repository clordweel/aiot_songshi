# AIOT 文档索引（渐进披露入口）

本文是代理与人类查阅长文的**目录**，优先读本文件再下钻；勿一次性加载 `training/` 全文。

## 术语

- [glossary.md](glossary.md) — AIOT、bench、site、DocType、PVE 等名词

## 环境事实（L2）

- [env/pve-vm.template.md](env/pve-vm.template.md) — PVE 虚拟机占位表（复制为 `pve-vm.local.md` 后填写）
- [env/frappe-site.template.md](env/frappe-site.template.md) — Frappe / ERPNext 站点占位表（复制为 `frappe-site.local.md`）

## 运行与排错（L3）

- [runbooks/](runbooks/) — 快照、回滚、升级等长步骤

## 执行留痕（Audit）

- [audit/README.md](audit/README.md) — 真实执行后简报模板与策略；**重大变更详述进 runbook，日常可核查进 audit**

## 培训（HumanPrimary）

- [training/README.md](training/README.md) — 学习路径（**人类主读**、可详尽；代理非必要勿批量载入）
- [training/levels/L0-cursor-models.md](training/levels/L0-cursor-models.md) — 新手：按任务选 Cursor 模型**档位**（非写死具体型号）

## 提示模板

- [prompts/api-task-decompose.md](prompts/api-task-decompose.md) — API 任务拆解
- [prompts/custom-app-change.md](prompts/custom-app-change.md) — 自定义 app 变更前自检

## 披露层级（约定）

| 层级 | 位置 |
|------|------|
| L0 | `.cursor/rules/*.mdc` |
| L1 | `.cursor/skills/*/SKILL.md` |
| L2 | `docs/aiot/env/*.md` |
| L3 | `docs/aiot/runbooks/` |
| Audit | `docs/aiot/audit/` |
| Training | `docs/aiot/training/`（默认不进入模型上下文；按需单文件读取） |

**代理默认顺序**：本 INDEX → env（模板或 local）→ 相关 skill。

**真实执行**（SSH、bench 写操作、API 写、PVE 变更等）结束后：按 [audit/README.md](audit/README.md) 追加一条简报。
