---
name: erpnext-api-ops
description: 通过 Frappe/ERPNext REST API 查 meta、读 DocType、谨慎写入；用户提到 API、集成、DocType 写操作时使用。API 写操作执行后须写 audit。
---

# ERPNext / Frappe HTTP API

## 前置

- 环境与站点：先读 [server-baseline.md](../../../docs/aiot/env/server-baseline.md)、[frappe-site-baseline.md](../../../docs/aiot/env/frappe-site-baseline.md)（site、base URL 约定）；认证与密钥仅用 `frappe-site.local.md`（gitignore），**不在**对话或可追溯文档中泄露 Secret。
- 栈目标：官方 **`develop`**（**v17 开发线**，如 `17.0.0-dev`）；精确版本以 `apps/erpnext/erpnext/__init__.py` 的 `__version__`、`bench version` 为准。API 行为与字段以现场 meta 与版本为准。

## 推荐流程

1. **确认 DocType 与字段**：必要时先读 meta（或文档化字段列表），避免猜字段名。
2. **读再写**：`GET` 或 `GET list` 确认状态；`POST` / `PUT` / `PATCH` 时注意必填与选项。
3. **权限与错误**：区分认证失败、权限拒绝、校验错误；避免用管理员密钥绕过业务规则除非明确要求。
4. **幂等**：重复提交是否安全；是否需先查询再更新。

## 辅助材料

- 任务拆解提示：[api-task-decompose.md](../../../docs/aiot/prompts/api-task-decompose.md)

## 留痕

- 对**真实环境**的 API **写操作**完成后：在仓库根目录 **`audits/`** 记一条简报（字段见 `docs/aiot/AUDITS.md`；DocType、动作摘要、结果；**勿**贴 Secret）。
