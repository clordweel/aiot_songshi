# PVE 虚拟机环境（模板）

复制本文件为 `pve-vm.local.md` 后，仅填写**不宜入库**的补充；**可提交**的主事实请维护 **[server-baseline.md](server-baseline.md)**（跨会话/Agent 优先读该文件）。

| 字段 | 示例 / 说明 |
|------|-------------|
| 显示名 | |
| VMID | |
| 管理网 IP | |
| SSH 别名或 `user@host` | |
| 是否生产 | 是 / 否 |
| bench Linux 用户 | |
| bench 家目录 / frappe-bench 路径 | 如 `~/frappe-bench` |
| Frappe / ERPNext 分支目标 | 如官方 `develop`（**v17 开发线**）；精确版本以上游 `erpnext/__init__.py` 的 `__version__` 为准 |
| 备注 | HA、快照策略、维护窗口 |
