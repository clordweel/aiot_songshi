# Frappe_Assistant_Core（FAC）安装与 MCP Endpoint

本文面向 bench 站点：**安装 FAC（GitHub `buildswithpaul/Frappe_Assistant_Core`）**、启用 MCP HTTP Endpoint，并与 Cursor Agent **REST / MCP / SSH bench** 自检脚本对齐。

- **上游源码**：https://github.com/buildswithpaul/Frappe_Assistant_Core  
- bench **目录与应用名**：克隆后为 `apps/frappe_assistant_core`，`hooks.py` 中 **`app_name = "frappe_assistant_core"`** —— `bench install-app`、`bench migrate` 均使用该 Python 包名。

**重大变更前**：按 [pre-change-snapshot.md](pre-change-snapshot.md) 取得可恢复快照；装机栈不熟见 [frappe-erpnext-install-prep.md](frappe-erpnext-install-prep.md)。

---

## 1. 前置

- bench 已初始化，`frappe`（或专用 Unix 用户）持有 bench。
- 目标站点已创建并可 `bench --site <site>`。
- Node/Python/MariaDB/Redis 等满足上游 **Frappe develop** 与 FAC README 要求（以现场为准）。

---

## 2. 获取并安装应用

在 bench **根目录**，以 bench 用户执行（示例；分支以上游默认分支为准）：

```bash
cd ~/frappe-bench
bench get-app https://github.com/buildswithpaul/Frappe_Assistant_Core
bench --site <site_name> install-app frappe_assistant_core
bench migrate
bench restart
```

若 `get-app` 需指定分支：

```bash
bench get-app --branch main https://github.com/buildswithpaul/Frappe_Assistant_Core
```

**DocType / OAuth**：FAC 会扩展 OAuth 与 MCP 相关设置；首次安装后登录 Desk，按上游文档完成 **Assistant Core Settings**（或等价 DocType）与 OAuth 客户端配置。**细则以上游 README / Wiki 为准**，此处不写死字段名。

---

## 3. MCP Endpoint URL（Cursor / Agent）

典型 StreamableHTTP MCP URL：

```text
https://<你的站点域名>/api/method/frappe_assistant_core.api.fac_endpoint.handle_mcp
```

本地自检（可选 FAC 变量，见 ``config/local.env``）：

```bash
python scripts/agent_mcp_ping.py --url "https://<site>/api/method/frappe_assistant_core.api.fac_endpoint.handle_mcp"
```

未配置 URL 时脚本 **SKIP**，不影响 REST/bench 流程。

---

## 4. 鉴权分工（勿混用）

| 用途 | 常见凭证 |
|------|-----------|
| **REST**（标准 DocType API） | 用户在 Desk 生成的 **API Key + API Secret**，Header：`Authorization: token <key>:<secret>` |
| **FAC MCP** | 多为 **OAuth 2.0 Bearer**（FAC / Assistant Core Settings 中发放的访问令牌）；部分现场也可用策略允许的 token 形态 |

自检脚本环境变量见 [config/agent-connect.env.example](../../../config/agent-connect.env.example)（复制为 `config/local.env`）。**勿将密钥写入仓库 JSON**。

---

## 5. Cursor MCP（仅限本地 IDE）

在 Cursor **Settings → MCP** 中为远端 FAC 添加 HTTP MCP：**Server URL** 为上节 Endpoint；**Headers** 中配置 `Authorization`（Bearer 或其他现场要求）。

占位说明见 [.cursor/skills/frappe-agent-connectivity/SKILL.md](../../../.cursor/skills/frappe-agent-connectivity/SKILL.md)。

---

## 6. 验证清单

1. **bench**：`python scripts/agent_bench_ssh.py`（默认远端 `bench version`）。
2. **REST**：`python scripts/agent_rest_smoke.py`（需 `FRAPPE_SITE_URL` + Key/Secret）。
3. **MCP**：安装 FAC 并拿到 Bearer/token 后 `python scripts/agent_mcp_ping.py`。

写入完成后：按 [audit/README.md](../audit/README.md) 简报。

---

## 7. 卸载（慎用）

如需移除安装的应用：

```bash
bench --site <site_name> uninstall-app frappe_assistant_core
```

删除前先备份站点与数据库；确认对其他自定义应用的依赖。
