## 2026-05-08 07:31:15 — 服务器 migrate（fixtures 缺 name 修复后）

- 时间：2026-05-08 07:31:15 CST (UTC+8)（本机记录）；bench 日志内时间为服务器时钟。
- 环境：`frappe@10.0.0.40`，`/home/frappe/frappe-bench`，站点 `10-0-0-40.sslip.io`
- 类型：`bench`
- 摘要：
  1. 首次 **`git pull`**（含扁平 fixtures）后 **`bench migrate`** 在 **`sync_fixtures`/`import_doc`** 处失败：**`KeyError: 'name'`**——**`import_file.import_file_by_path`** 对 fixture 每条顶层记录要求存在 **`name`**（先于插入即可比对 DB）；**`account_category_china.json`、`financial_report_template_china_balance_sheet.json`** 原缺失 **`name`**。
  2. 源码修正：**Account Category** 每条 **`name` = `account_category_name`**；**Financial Report Template** 顶层 **`name` = `template_name`**（`ssi_app` **`22f71d5`**），**push** 后再 **`git pull`**。
  3. 第二次 **`bench --site 10-0-0-40.sslip.io migrate`**：**exit 0**；含 **`Syncing fixtures...`**、`after_migrate`、搜索索引队列更新。
- 结果：`ok`（第二次）；首次：`failed`（已修复）
- 审批（可选）：—
