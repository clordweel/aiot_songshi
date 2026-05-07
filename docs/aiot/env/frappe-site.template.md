# Frappe / ERPNext 站点（模板）

复制为 `frappe-site.local.md` 填写**密钥等涉密项**。非机密的 site / URL / 应用线请维护 **[frappe-site-baseline.md](frappe-site-baseline.md)**（可提交）。

| 字段 | 说明 |
|------|------|
| site 名称 | `bench use` 所针对的 site |
| 主域名 / base URL | HTTPS 访问根，API 亦基于此 |
| 已安装应用 | frappe、erpnext（目标 **`develop` / v17 开发线**）、hrms、自定义 app 列表 |
| 检出分支 | 如 `erpnext@develop`、`frappe@develop`（以 `git -C apps/<app> status` 为准） |
| Python / Node（若已知） | 以 **develop** 官方要求与目标机 `bench version` 为准 |
| API 认证方式 | API Key / API Secret（Desk → 用户 → API Access Keys；不在本文写明文） |
| FAC MCP Endpoint URL | 安装 **Frappe_Assistant_Core** 后填写：`https://<站点>/api/method/frappe_assistant_core.api.fac_endpoint.handle_mcp` |
| MCP OAuth / Bearer | FAC 侧 OAuth / Bearer（与 REST Key **通常不是同一套**；仅存本地） |
| SSH bench 目标 | 与 [server-baseline.md](server-baseline.md) 对齐；变量集中于 **`config/local.env`**（gitignore） |
| 本地变量模板 | 复制 [config/agent-connect.env.example](../../../config/agent-connect.env.example) → **`config/local.env`**（勿提交）；说明见 [config/README.md](../../../config/README.md) |

**版本以目标机为准**：执行前用 `bench version`、站点详情等确认，勿在规则中写死小版本。
