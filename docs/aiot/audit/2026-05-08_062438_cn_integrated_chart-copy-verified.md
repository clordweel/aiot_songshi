## 2026-05-08 — cn_integrated_chart_of_accounts.json 复制至 ERPNext verified

- 时间：2026-05-08（会话执行）
- 环境：VM **10.0.0.40**，用户 **frappe**，bench **`/home/frappe/frappe-bench`**，站点 **`10-0-0-40.sslip.io`**
- 类型：`scp` / `bench execute`（写 `ssi_app/custom` 与 `erpnext/.../verified/`）
- 摘要：
  - **`scp`** 本地 **`apps/ssi_app/.../cn_integrated_chart_of_accounts.json`** → 远端 **`.../chart_of_accounts/custom/`**。
  - **`bench --site 10-0-0-40.sslip.io execute`** **`ssi_app.ssi_accounts.copy_chart_templates.copy_chart_templates`**：**`errors`** 为空；**`cn_integrated_chart_of_accounts.json`**（及目录内既有 **`cn_custom_chart_of_accounts.json`**）已写入 **`erpnext/accounts/doctype/account/chart_of_accounts/verified/`**。
- 结果：`ok`
- 后续：建议在 **`apps/ssi_app`** 仓库 **`git commit`** / **`git push`** 纳入该 JSON，避免下次 **`git pull`** 覆盖远端手工文件。
