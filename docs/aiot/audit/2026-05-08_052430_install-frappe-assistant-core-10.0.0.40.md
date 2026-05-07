## 2026-05-08 — 安装 Frappe_Assistant_Core（FAC）于 10.0.0.40

- 时间：2026-05-08（会话执行）
- 环境：VM **10.0.0.40**，Linux 用户 **frappe**，bench **`/home/frappe/frappe-bench`**，站点 **`10-0-0-40.sslip.io`**
- 类型：`bench` / SSH（写 apps、站点安装应用、migrate、restart）
- 摘要：
  - **`bench get-app https://github.com/buildswithpaul/Frappe_Assistant_Core`**（克隆为 `apps/frappe_assistant_core`）；上游依赖声明与 **Frappe 17 dev** 不完全一致时有告警，现场按 develop 继续。
  - **`bench --site 10-0-0-40.sslip.io install-app frappe_assistant_core`**（DocType 同步完成；可选 PaddleOCR 依赖未装则跳过预下载）。
  - **`bench --site 10-0-0-40.sslip.io migrate`**；**`bench restart`**。
  - 开发机自检：**`python scripts/agent_mcp_ping.py`** 对 **`http://10.0.0.40/.../handle_mcp`** JSON-RPC `initialize` 返回 **HTTP 200**（凭据来自本地 gitignore env，未写入本文）。
- 结果：`ok`
- 审批（可选）：
