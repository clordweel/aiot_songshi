## 2026-05-08 07:40:14 — `aiot_songshi` 审计重整入库，`ssi_app` 服务器同步与 migrate

- 时间：2026-05-08 07:40:14 CST (UTC+8)（文件名前缀与正文同一约定）
- 环境：`frappe@10.0.0.40`，bench `~/frappe-bench`，站点 `10-0-0-40.sslip.io`
- 类型：`deploy` / `bench`
- 摘要：
  1. 父仓库 `aiot_songshi`：`develop` 提交 `7f7692f` —— `docs/aiot/audit/` 简报文件名重整（`_HHmmss_`）、README 微调、`git push`。
  2. `~/frappe-bench/apps/ssi_app`：`git fetch`/`checkout develop`/`git pull --ff-only origin develop`，`Updating 22f71d5..57f3e95`。
  3. `bench --site 10-0-0-40.sslip.io migrate` 完成（含 after_migrate、队列重建站点搜索索引）。
- 结果：`ok`
- 审批（可选）：—
