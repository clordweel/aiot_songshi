# 服务器基线（可提交）

本文件记录**目标 VM 的非机密基础信息**，供人类与 Agent **跨会话**引用；**允许提交 Git**。  
**禁止**在此写入数据库口令、API Secret、私钥等；这类内容仅用 `docs/aiot/env/*.local.md`（已 gitignore）或 **`config/local.env`**（已 gitignore）。

| 字段 | 值 |
|------|-----|
| 主机名 | `aiot-songshi-frappe` |
| 管理 / SSH（当前阶段） | `root@10.0.0.40`；日常 bench 操作用 **`frappe@10.0.0.40`** |
| PVE VMID | （待填） |
| 环境性质 | 安装/预生产（**非生产**定稿前勿标生产） |
| ERPNext / Frappe 目标 | 官方 **`develop`**（**v17 开发线**，例 `17.0.0-dev`）；版本以上游 `erpnext/__init__.py` 的 `__version__`、本机 `bench version` 为准；`get-app` 使用 `--branch develop` |
| bench Linux 用户 | **`frappe`**（已创建） |
| frappe-bench 路径 | **`/home/frappe/frappe-bench`** |

## 硬件与系统（调查快照）

| 项 | 值 |
|----|-----|
| OS | Ubuntu 22.04.5 LTS (jammy)，内核 5.15.x |
| 虚拟化 | KVM / QEMU（guest） |
| vCPU | 4 |
| 内存 | 15 GiB |
| Swap | **无**（建议按规范评估 swapfile） |
| 根盘 | ext4，约 46G 总容量（量级以现场为准） |

## 运行时栈（随安装维护）

> **当前**：本机已部署 **bench + ERPNext develop + `ssi_app` + `frappe_assistant_core`（FAC）**；浏览器/API 基线见 **[frappe-site-baseline.md](frappe-site-baseline.md)**。组件版本以 **`bench version`** 与现场为准，勿在此写死小版本。

| 组件 | 状态（摘要） |
|------|----------------|
| `bench` / frappe-bench | 已初始化 |
| Web / DB / Redis / Node | 站点已可访问（当前内网 HTTP）；详见装机审计 |
| Unix 用户 `frappe` | 已创建 |

## 部署就绪摘要

- **当前**：VM **10.0.0.40** 上 bench 已运行；站点名与 URL 见 **frappe-site-baseline**。  
- **重大变更**前快照：[pre-change-snapshot.md](../runbooks/pre-change-snapshot.md)。  
- 装机检查清单（新主机）：[frappe-erpnext-install-prep.md](../runbooks/frappe-erpnext-install-prep.md)。

## 维护约定

1. **装机或重大变更后**：更新本页表格与 **frappe-site-baseline.md**。  
2. **与 `pve-vm.local.md` 分工**：`*.local.md` 只放**不宜入库**的补充；与 baseline **不重复**粘贴长表。  
3. **审计**：执行留痕见 `docs/aiot/audit/`。
