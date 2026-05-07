# Frappe / ERPNext 站点基线（可提交）

与 **bench 站点**相关的 **非机密、跨会话** 约定；**允许提交 Git**。  
站点口令、API Key、TLS 私钥等**不得**写在本文件，请用 `frappe-site.local.md`（gitignore）。

| 字段 | 值 |
|------|-----|
| site 名称 | `10-0-0-40.sslip.io`（浏览器可达 **`http://10.0.0.40`**） |
| 主域名 / base URL | `http://10.0.0.40`（内网 HTTP；TLS/域名变更后请同步） |
| 已规划应用 | `frappe`、`erpnext`、`ssi_app`、`frappe_assistant_core`（**FAC / MCP**）@ **`develop`** / v17 开发线；以 `bench version` 为准 |
| 本机 Node / Python（期望） | 以 **develop** 官方文档与 `bench version` 输出为准 |

**维护**：建站、`install-app`、升级后更新上表；详细检出分支以 `git -C apps/<app> status` 为准。
