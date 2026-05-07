---
name: erpnext-api-ops
description: 通过 Frappe/ERPNext REST API 查 meta、读 DocType、谨慎写入；用户提到 API、集成、DocType 写操作时使用。API 写操作执行后须写 audit。
---

# ERPNext / Frappe HTTP API

## 前置

- `docs/aiot/env/frappe-site.local.md`（或模板）：base URL、site 名；认证方式以站点为准（API Key / Secret、Token 等），**不在**对话或文档中泄露 Secret。

## 推荐流程

1. **确认 DocType 与字段**：必要时先读 meta（或文档化字段列表），避免猜字段名。
2. **读再写**：`GET` 或 `GET list` 确认状态；`POST` / `PUT` / `PATCH` 时注意必填与选项。
3. **权限与错误**：区分认证失败、权限拒绝、校验错误；避免用管理员密钥绕过业务规则除非明确要求。
4. **幂等**：重复提交是否安全；是否需先查询再更新。

## 辅助材料

- 任务拆解提示：[docs/aiot/prompts/api-task-decompose.md](docs/aiot/prompts/api-task-decompose.md)

## 留痕

- 对**真实环境**的 API **写操作**完成后：按 `docs/aiot/audit/README.md` 记一条简报（DocType、动作摘要、结果；**勿**贴 Secret）。
