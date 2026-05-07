# Frappe / ERPNext 站点（模板）

复制为 `frappe-site.local.md` 填写；**勿提交**含密钥的 local 文件。

| 字段 | 说明 |
|------|------|
| site 名称 | `bench use` 所针对的 site |
| 主域名 / base URL | HTTPS 访问根，API 亦基于此 |
| 已安装应用 | frappe、erpnext、hrms、自定义 app 列表 |
| Python / Node（若已知） | 以目标机 `bench version` 为准 |
| API 认证方式 | API Key / 其他（不在本文写 Secret） |

**版本以目标机为准**：执行前用 `bench version`、站点详情等确认，勿在规则中写死小版本。
