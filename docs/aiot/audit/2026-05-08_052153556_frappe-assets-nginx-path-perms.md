## 2026-05-08 17:25:00 — nginx 无法读取 bench assets（权限）

- 时间：2026-05-08 17:25:00 CST (UTC+8)（补录，同日排序）
- 环境：VM **10.0.0.40**，bench `~/frappe-bench`，站点 `10-0-0-40.sslip.io`
- 类型：`bench` / 配置与权限
- 摘要：登录页 `/assets/*` **404** / 无样式；`namei` 显示 **`/home/frappe` 为 750**，**`www-data` 无法穿越**。执行 **`sudo chmod o+x /home/frappe`**（751，`others` 仅有目录执行位以便路径遍历），并以 **`sudo -u www-data`** 验证可读 `sites/assets/...`。
- 结果：`ok`
- 审批（可选）：
- 审批时间（可选）：
