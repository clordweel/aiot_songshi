# Prompt：自定义 App 变更前自检

在改代码或加 DocType 前快速扫一遍影响面。

1. **变更落在自定义 app**：优先extend / hooks，避免直接改 `frappe` / `erpnext` 核心。
2. **DocType**：是否新 DocType、是否改 schema、是否需要 `migrate` 与 fixtures。
3. **权限**：Role、Permission、Workspace；是否需导出权限到 fixtures。
4. **报表/打印格式/客户端脚本**：联动查询与导出。
5. **定时任务**：`hooks.py` 中 scheduled jobs。
6. **真实执行**：bench 命令或部署后在仓库根目录 `audits/` 写简报（约定见 `docs/aiot/AUDITS.md`）；大变更前见 `runbooks/pre-change-snapshot.md`。
