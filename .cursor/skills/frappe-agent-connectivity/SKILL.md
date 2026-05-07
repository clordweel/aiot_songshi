---
name: frappe-agent-connectivity
description: 为 Agent 串联 MCP（FAC）、Frappe REST、bench SSH 三条路径；自检脚本与凭证约定；FAC 未安装时降级 REST/bench。涉及远端连通/API/MCP 时读取。
---

# Frappe Agent 三条连通路径（MCP / REST / bench）

## 何时用哪条路（摘要）

| 场景 | 优先 |
|------|------|
| 运维脚本、大批量迁移、需任意站点 Python 上下文 | **bench**（SSH 至 frappe-bench） |
| 远程集成、免 SSH、标准 DocType CRUD | **REST**（API Key + Secret → `Authorization: token …`） |
| Cursor / Agent 需统一工具发现、FAC 已启用 | **MCP**（FAC endpoint） |

FAC **工具列表即能力上限**；REST **受 whitelist / 权限约束**；bench **能力最全**，须有 SSH 与正确 `--site`。

## 相关技能（按需打开）

- 站点/migrate/进程：[frappe-bench-site-ops](../frappe-bench-site-ops/SKILL.md)
- REST DocType 读写：[erpnext-api-ops](../erpnext-api-ops/SKILL.md)

## 凭证与环境事实（只读本仓库）

1. **[docs/aiot/env/server-baseline.md](../../../docs/aiot/env/server-baseline.md)** — SSH、bench 路径摘要。
2. **[docs/aiot/env/frappe-site-baseline.md](../../../docs/aiot/env/frappe-site-baseline.md)** — site / URL（非机密）。
3. **`docs/aiot/env/frappe-site.local.md`**（gitignore）— API Key、MCP Bearer/token、SSH 补充说明。
4. 可选：复制 [config/agent-connect.env.example](../../../config/agent-connect.env.example) 为 **`config/local.env`**（gitignore），说明见 [config/README.md](../../../config/README.md)。

**切勿**把密钥写入可提交的 JSON（例如 Cursor MCP UI 以外的仓库文件）；REST Key 与 **FAC MCP OAuth/Bearer** 常为两套凭证，勿混填。

## FAC / MCP

- **上游仓库**：https://github.com/buildswithpaul/Frappe_Assistant_Core  
- bench **Python app 名**：`frappe_assistant_core`（见上游 `hooks.py` → `app_name`）。
- **典型 MCP HTTP Endpoint**：  
  `https://<站点域名>/api/method/frappe_assistant_core.api.fac_endpoint.handle_mcp`
- **安装与 Cursor**：见 **[docs/aiot/runbooks/frappe-assistant-core-fac.md](../../../docs/aiot/runbooks/frappe-assistant-core-fac.md)**。
- FAC **未安装**时：`agent_mcp_ping.py` 在未配置 URL 时会跳过；Agent 使用 REST + bench 即可。

## 自检脚本（仓库根目录执行）

依赖：`urllib`（标准库）。若在极简环境遇到 HTTPS，使用系统 Python 3.10+。

```bash
# REST（需 FRAPPE_SITE_URL + FRAPPE_API_KEY + FRAPPE_API_SECRET，或 env 文件导出）
python scripts/agent_rest_smoke.py

# MCP — FAC（未设置 FAC_MCP_URL 则跳过）
python scripts/agent_mcp_ping.py

# bench — SSH（默认 frappe 用户与 ~/frappe-bench）
python scripts/agent_bench_ssh.py --dry-run
python scripts/agent_bench_ssh.py
```

脚本支持的 CLI 参数见各文件 `--help`。

## 留痕

对站点产生真实写入（REST PUT、bench migrate、`bench execute` 写库等）后：按 [docs/aiot/audit/README.md](../../../docs/aiot/audit/README.md) 简报；**勿**贴 Secret。
