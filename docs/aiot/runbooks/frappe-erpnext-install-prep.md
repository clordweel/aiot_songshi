# Frappe / ERPNext（原生 bench）安装前准备 — Ubuntu 22.04



面向已通过 SSH 可达的宿主机（见 `docs/aiot/env/pve-vm.local.md` 调查快照）。**以下为检查清单与顺序建议，具体命令以官方 `develop` 分支文档为准。**



## 0. 版本线（本仓库约定）



- **Frappe / ERPNext**：使用 GitHub **官方仓库的 `develop` 分支**（当前上游为 **v17 开发线**，例 `17.0.0-dev`；以 [frappe/erpnext `develop`：`erpnext/__init__.py` 的 `__version__`](https://raw.githubusercontent.com/frappe/erpnext/develop/erpnext/__init__.py) 与本机 `bench version` 为准）。`bench get-app` / clone 时指定 `--branch develop`（或以官方当前推荐方式检出 develop）。

- **依赖版本**：`develop` 对 **Python / Node / MariaDB** 的要求常高于 LTS 稳定版；务必核对当期 **`erpnext` / `frappe` 仓库的 `pyproject.toml`**（例如上游 `erpnext` develop 曾声明 `requires-python >= 3.14`）。勿照搬旧版 v14/v15/v16 数字；精确版本以官方仓库与 `bench` 输出为准。



## 1. 锁定文档



- 打开 Frappe / ERPNext **develop** 的安装或贡献者文档中「生产/手动安装」章节。

- 记录 **Node 主版本、MariaDB 主版本、Python 最低版本**；`develop` 常与 **Python 3.14+** 等新要求对齐（以官方 `pyproject.toml` 为准）。若高于 Ubuntu 22.04 自带的 Python 3.10，需规划 **受支持的 Python 安装方式、pyenv、升级基础 OS 等**，勿假设系统 `python3` 即可用于当前 `develop`。

- 记录对应的 **Redis**、**wkhtmltopdf**（若仍文档要求）等组件。



## 2. 系统资源与安全基线



- [ ] CPU / 内存 / 磁盘满足官方最低与团队预期（当前 VM：4C / 15G / ~43G 可用，见本地 env）。

- [ ] **Swap**：若内存余量紧张或需大构建，建议按规范添加 swapfile。

- [ ] **专用 Unix 用户（推荐）**：按 Frappe 实践创建（常见 `frappe`），`useradd -m -s /bin/bash`，home 下放 `frappe-bench`；日常 **`bench` 不以 root 运行**；root 仅用于系统包与权限初始化。

- [ ] `apt update` 后仅安装文档列出的依赖（build-essential、lib 系列等依官方列表）。

- [ ] 时区、NTP、hostname、hosts（站点 FQDN 若已确定可先写 hosts 预演）。



## 3. 数据库与缓存



- [ ] 安装文档要求的 **MariaDB**（或指定 MySQL），配置字符集/排序规则按官方（常见 `utf8mb4`）。

- [ ] 设置 **Redis**（Frappe 缓存与队列依赖）。

- [ ] root DB 密码策略：仅存密钥管理 / 本地安全备忘录，**不入库** Git 与培训正文。



## 4. Node / 前端构建



- [ ] 安装文档指定 **Node**（常用 nvm 或 NodeSource；版本错会导致 `yarn`/`esbuild` 失败）。

- [ ] 全局 **yarn**（若文档要求）。



## 5. Bench



- [ ] 按官方方式安装 **bench CLI**（常见为 `pip` 安装到**专用用户**虚拟环境或用户级 pip）。

- [ ] 在该用户下 `bench init` 创建 **frappe-bench**；`get-app frappe`、`get-app erpnext` 等使用 **`--branch develop`**（以官方说明为准）。

- [ ] 后续 `new-site` / `install-app erpnext` 依文档顺序执行。



## 6. 网络与 TLS



- [ ] 规划 **站点域名**、内网/公网反向代理（Nginx/Caddy 等）。

- [ ] TLS 证书策略（Let’s Encrypt / 内网 CA）。



## 7. 安装后立刻要做



- [ ] `bench version`、各 app 分支、站点列表记入 `docs/aiot/env/frappe-site.local.md`。

- [ ] 对**真实改配置的命令**、`migrate`、开放端口等：按仓库根目录 `audits/` 留痕（约定见 `docs/aiot/AUDITS.md`）。



## 8. 重大步骤前的快照



安装过程中若包含**大段迁移或生产切库**等高风险步骤：**先**按 [pre-change-snapshot.md](pre-change-snapshot.md) 做 **PVE 快照**或（若可用且允许）**LVM 快照**。



## 9. 与快照的差异跟踪



当前调查：**无 Node / 无 MariaDB / 无 Redis / 无 bench**。完成每一大块安装后，可复用下列只读命令复核：



```bash

python3 --version

node -v 2>/dev/null || true

mariadb --version 2>/dev/null || mysql --version 2>/dev/null || true

redis-server --version 2>/dev/null || true

command -v bench && bench version

```


