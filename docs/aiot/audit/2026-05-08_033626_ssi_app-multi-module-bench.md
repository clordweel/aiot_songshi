## 2026-05-08 15:45:00 — 二开 app `ssi_app`（多模块）安装

- 时间：2026-05-08 15:45:00 CST (UTC+8)（会话执行；补录，同日排序）
- 环境：VM **10.0.0.40**，用户 **frappe**，bench **`~/frappe-bench`**，站点 **`10-0-0-40.sslip.io`**
- 类型：`bench`
- 摘要：
  - `bench get-app https://github.com/clordweel/ssi_app.git`：**远端为空仓库**，clone 后无法安装；已删除半成品目录。
  - 改用 **`bench new-app ssi_app`**（交互项通过管道传入：`mit`、`workflow=n`、`branch=develop`）；生成 **`apps/ssi_app`** 并完成 **`bench build --app ssi_app`**。
  - **`ssi_app/ssi_app/modules.txt`** 设为三行：**`ssi_app`、`ssi_stock`、`ssi_accounts`**；对应子目录 **`ssi_app/`、`ssi_stock/`、`ssi_accounts/`** 均含 **`__init__.py`**。
  - App 内 **`git remote origin`** 指向 **`https://github.com/clordweel/ssi_app.git`**（bench 机仍遵循团队「不写推送凭据」策略；**推送首屏代码需在具备写权限的环境完成**）。
  - **`bench --site 10-0-0-40.sslip.io install-app ssi_app`**、`migrate`、`clear-cache`、**`bench restart`**：`migrate_EXIT` / `restart_EXIT` 均为 **0**；**`sites/apps.txt`** 含 **`ssi_app`**。
- 结果：`ok`
- 审批（可选）：
- 审批时间（可选）：
