## 2026-05-08 14:00:00 — bench 生产：ERPNext/Frappe develop（10.0.0.40）

- 时间：2026-05-08 14:00:00 CST (UTC+8)（会话执行；补录，同日排序）
- 环境：VM **10.0.0.40**，Unix 用户 **frappe**（sudo NOPASSWD）；SSH 主机密钥曾变更，客户端已更新 `known_hosts`
- 类型：`deploy`（bench / nginx / supervisor / MariaDB）
- 摘要：
  - **Ubuntu 24.04**，MariaDB **11.8.x**，系统 Redis 仍在主机上；bench 使用 **supervisor** 管理的 bench 内 **redis-cache / redis-queue**（端口与 `common_site_config.json` 一致）。
  - 依赖：`uv` + **Python 3.14**，`uv tool install frappe-bench`（bench **5.29.1**）；**Node 24** / Yarn **1.22.x**；`/usr/local/bin` 下符号链接 **node/npm/yarn**（避免 bench 子进程找不到 `yarn`）。
  - MariaDB `root@localhost` 已轮换口令并写入 **`/home/frappe/bench_secrets.txt`**（**600**，不入库密码）；站点 Administrator 口令同文件内 **`ADMIN_PASSWORD`**（多次尝试安装会导致重复键名行，建议在服务器上手工整理该文件并轮转口令）。
  - **bench**：`~/frappe-bench`，**frappe / erpnext** 均为 **develop**（`bench version` 显示 **17.x.x-develop**）。
  - **站点**：`10-0-0-40.sslip.io`（DNS 指向 **10.0.0.40**），`bench setup production --yes frappe` 已跑通 nginx；**supervisor**：`bench setup production` 未在 **`/etc/supervisor/conf.d/`** 生成指向 `~/frappe-bench/config/supervisor.conf` 的符号链接，已手工执行  
    `ln -sf /home/frappe/frappe-bench/config/supervisor.conf /etc/supervisor/conf.d/frappe-bench.conf`  
    后 **`supervisorctl reread/update`**，进程组 **RUNNING**。
  - **Ansible**：`bench setup production` 依赖 `ansible-playbook`；已对 uv 工具内 Python 执行 **ensurepip + pip install ansible**，并将 **`ansible-playbook`/`ansible`** 链到 **`/usr/local/bin`**。
  - **内核参数**：`/etc/sysctl.d/99-frappe-overcommit.conf` 设置 **`vm.overcommit_memory=1`**（消除 Redis 后台保存告警）。
  - **验收**：本机 `curl -I -H "Host: 10-0-0-40.sslip.io" http://127.0.0.1/` 返回 **HTTP 200**（登录页）。
- 结果：`ok`
- 后续建议（未自动执行）：HTTPS/Let’s Encrypt；将 **`live_reload`** 在生产关闭；复核 **`redis_socketio`** 是否与当前 bench 设计一致；整理 **`bench_secrets.txt`** 重复键名。
- 审批（可选）：
- 审批时间（可选）：
