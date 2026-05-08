# AIOT 文档索引（渐进披露入口）

本文是代理与人类查阅长文的**目录**，优先读本文件再下钻；勿一次性加载 `training/` 全文。

## 仓库本地（不入库或部分入库）

- [tmp/README.md](../../tmp/README.md) — 根目录 `tmp/` 临时文件区（除本说明外默认 gitignore）
- 仓库根目录 **`audits/`** — 真实执行简报 Markdown（**gitignore**；字段与模板见 [AUDITS.md](AUDITS.md)）

## 术语

- [glossary.md](glossary.md) — AIOT、bench、site、DocType、PVE 等名词

## 环境事实（L2）

- **[env/server-baseline.md](env/server-baseline.md)** — **服务器基线（可提交）**：SSH、OS、资源、目标分支、运行时栈摘要；跨会话 / Agent 优先读此文件。
- **[env/frappe-site-baseline.md](env/frappe-site-baseline.md)** — **站点基线（可提交）**：site 名、URL、应用线等非机密约定。
- [config/README.md](../../config/README.md) — **脚本/Agent 本地变量**：可提交的示例 `agent-connect.env.example` 与 gitignore 的 `local.env`。
- [env/pve-vm.template.md](env/pve-vm.template.md) — PVE 空白表（复制为 `pve-vm.local.md` 仅供本地补充）。
- [env/frappe-site.template.md](env/frappe-site.template.md) — 站点空白表（复制为 `frappe-site.local.md` 存密钥等）。

## 运行与排错（L3）

- [scripts/deploy_ssi_app.py](../../scripts/deploy_ssi_app.py) — **`ssi_app`**：SSH 至 bench，远端 `git pull` + `migrate` / `build` / `restart`（可选 `--push`、`--copy-chart-templates`）
- [scripts/pack_audits.py](../../scripts/pack_audits.py) — 按 **`--since` / `--until`**（日期或日期时间）筛选仓库根目录 **`audits/`** 并打成 zip（默认输出 `tmp/`）
- [scripts/agent_rest_smoke.py](../../scripts/agent_rest_smoke.py)、[scripts/agent_mcp_ping.py](../../scripts/agent_mcp_ping.py)、[scripts/agent_bench_ssh.py](../../scripts/agent_bench_ssh.py) — Agent **REST / MCP / bench SSH** 自检（凭证 **`config/local.env`**，模板见 [config/agent-connect.env.example](../../config/agent-connect.env.example)）
- [runbooks/](runbooks/) — 快照、回滚、升级等长步骤
- [runbooks/frappe-erpnext-install-prep.md](runbooks/frappe-erpnext-install-prep.md) — Frappe / ERPNext（bench）安装前检查清单
- [runbooks/frappe-assistant-core-fac.md](runbooks/frappe-assistant-core-fac.md) — Frappe_Assistant_Core（FAC）安装与 MCP Endpoint
- [runbooks/pre-change-snapshot.md](runbooks/pre-change-snapshot.md) — 变更前快照占位

## 执行留痕（Audit）

- [AUDITS.md](AUDITS.md) — 简报字段与策略（简报正文落在仓库根目录 **`audits/`**，不入库）；**重大变更详述进 runbook，日常可核查进 `audits/`**

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
| L2 | **已提交**：`server-baseline.md`、`frappe-site-baseline.md`；模板与 `*.local.md`（涉密、gitignore） |
| L3 | `docs/aiot/runbooks/` |
| Audit | 仓库根目录 `audits/`（不入库；约定见 [AUDITS.md](AUDITS.md)） |
| Training | `docs/aiot/training/`（默认不进入模型上下文；按需单文件读取） |

**代理默认顺序**：本 INDEX → **[env/server-baseline.md](env/server-baseline.md)**（及按需 `frappe-site-baseline.md`）→ 模板 / `*.local.md`（仅涉密）→ 相关 skill。

**真实执行**（SSH、bench 写操作、API 写、PVE 变更等）结束后：在仓库根目录 **`audits/`** 追加一条简报（约定见 [AUDITS.md](AUDITS.md)）。
