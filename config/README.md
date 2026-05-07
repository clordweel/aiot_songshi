# 本地与脚本配置（`config/`）

| 文件 | 是否入库 | 说明 |
|------|----------|------|
| [agent-connect.env.example](agent-connect.env.example) | 是 | REST / MCP / SSH bench / 部署脚本的**变量名与示例占位**，可复制为 `local.env` |
| **`local.env`** | **否**（gitignore） | 本机密钥与非机密默认值；由 Python 脚本自动加载 |

## 与文档的关系

- **跨会话事实（非密钥）**：仍以 [docs/aiot/env/frappe-site-baseline.md](../docs/aiot/env/frappe-site-baseline.md)、[server-baseline.md](../docs/aiot/env/server-baseline.md) 为准。
- **`docs/aiot/env/frappe-site.local.md`**：人类可读补充（gitignore）；与 `local.env` **勿重复粘贴密钥**，任选其一为主即可。

## 迁移说明

若仍在使用根目录 `scripts/agent_connect.local.env`，脚本会继续读取（优先级低于 `config/local.env` 中的同名键）。新布置建议只维护 **`config/local.env`**。
