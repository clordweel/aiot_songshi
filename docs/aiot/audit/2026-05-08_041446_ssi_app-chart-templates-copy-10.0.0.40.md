## 2026-05-08 16:55:00 — ssi_app 科目表模板复制至 ERPNext verified（10.0.0.40）

- 时间：2026-05-08 16:55:00 CST (UTC+8)（会话执行；补录，同日排序）
- 环境：VM **10.0.0.40**，Linux 用户 **frappe**，bench **`~/frappe-bench`**，站点 **`10-0-0-40.sslip.io`**
- 类型：`bench` / shell（写 ERPNext 源码树下 `verified/`）
- 摘要：
  - 远端 **`ssi_app`** 尚未包含仓库内的 **`copy_chart_templates.py`**：通过 **SCP** 写入 **`apps/ssi_app/ssi_app/ssi_accounts/copy_chart_templates.py`**。
  - **`mkdir`** **`apps/ssi_app/ssi_app/chart_of_accounts/custom`**；从 **`https://raw.githubusercontent.com/clordweel/cos/version-16-beta/cos/chart_of_accounts/custom/cn_custom_chart_of_accounts.json`** 拉取 **`cn_custom_chart_of_accounts.json`**（临时/bootstrap；可按策略替换为自有模板并删除远端副本）。
  - **`bench --site 10-0-0-40.sslip.io execute ssi_app.ssi_accounts.copy_chart_templates.copy_chart_templates`**：返回 **`errors`** 为空，已将同名 JSON 复制到 **`erpnext/.../chart_of_accounts/verified/`**。
  - 说明：交互式 SSH 下需 **`bash -lc`** 以保证 **`bench`** 在 **`PATH`**（本机为 **`~/.local/bin/bench`**）。
- 结果：`ok`
- 审批（可选）：
- 审批时间（可选）：
