## 2026-05-08 06:55:11 — 目标机拉取 ssi_app 并 migrate

- 时间：2026-05-08 06:55:11 CST (UTC+8)（以本机记录为准）
- 环境：`frappe@10.0.0.40`，bench `/home/frappe/frappe-bench`，站点 `10-0-0-40.sslip.io`
- 类型：`bench` / `deploy`
- 摘要：
  1. `git fetch` + `git pull --ff-only origin develop`（`apps/ssi_app`，fdc4398→667e1b5，含 desk_terms_print fixtures、hooks、chart JSON 等）。
  2. 裸 SSH 下 `bench` 不在 PATH（exit 127）；改用 `bash -lc` 执行 `bench --site 10-0-0-40.sslip.io migrate`，退出码 0；收尾含 `after_migrate`、`Queued rebuilding of search index`。
- 结果：`ok`
- 审批（可选）：—
