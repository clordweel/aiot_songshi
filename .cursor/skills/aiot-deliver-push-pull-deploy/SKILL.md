---
name: aiot-deliver-push-pull-deploy
description: 本地提交并推送 Git 远端后，在目标 bench 服务器单向 git pull 并完成 migrate/build/restart；用户提到交付、推送部署、pull 部署、同步服务器、deploy ssi_app 时使用。
---

# AIOT：推送—拉取—部署（Git → 服务器）

## 何时读取本技能

用户自然语言若命中下列 **口令或同义说法**，优先按本流程执行（并与 **`aiot-ssi-app-workflow`**、**`frappe-bench-site-ops`** 一致）：

| 口令示例 | 含义 |
|----------|------|
| **交付 / 推到服务器 / 推送部署** | `ssi_app`：`commit` → `push` → 服务器 `pull` → `bench` 收口 |
| **同步 bench / 服务器拉一下** | 仅服务器侧：远端目录 `git pull` + 按需 `migrate`/`build`/`restart` |
| **全链路部署（ssi_app）** | 本地 push + SSH 拉取 + bench（可与脚本等价） |
| **只推仓库（父仓库）** | 仅 **`aiot_songshi` 根目录** Git：不涉及 `~/frappe-bench/apps/ssi_app` |

## 两条源码线（不要混）

1. **`apps/ssi_app/`**（独立 Git，父仓库已 ignore）  
   - **单一真相**：在此目录 `commit` + `push` → 远端 **`develop`**（或团队约定分支）。  
   - **服务器**：`~/frappe-bench/apps/ssi_app` 仅 **`fetch`/`pull`**，不把服务器当主线写回 GitHub（除非用户明确要求反向迁移）。

2. **`aiot_songshi` 父仓库**（文档、规则、脚本、`pack_audits` 等）  
   - 在**仓库根目录** `git commit` / `push`。  
   - **默认不**因此自动登录 bench；若用户同时要部署二开，再走下方「ssi_app」步骤。

## 推荐自动化（ssi_app）

在已配置 **`config/local.env`**（或等价环境变量）的前提下，优先：

```bash
python scripts/deploy_ssi_app.py --dry-run
python scripts/deploy_ssi_app.py --push
```

- `--push`：在本地 `apps/ssi_app` 执行 `git push`（默认会检查脏工作区；慎用 `--no-check-dirty`）。  
- 脚本随后在 SSH 目标上执行：**app 目录 `git pull`** + **`bench migrate` / `build` / `restart`**（具体以脚本参数与现场为准）。  
- 详见脚本内说明：`scripts/deploy_ssi_app.py`。

代理若无法执行脚本，则用等价手工命令（保持 **`bash -lc`**、`bench` 在 bench 根目录执行等现有惯例）。

## 手工顺序备忘（ssi_app）

1. 本地：`cd apps/ssi_app` → `git status` → `git commit` → `git push origin develop`  
2. SSH：`cd ~/frappe-bench/apps/ssi_app` → `git fetch` + `git pull`（**ff-only** 优先）  
3. bench 根：`bench --site <site> migrate`；涉及前端时 `bench build --app ssi_app`；按需 `bench restart`  
4. **留痕**：服务器产生写影响后，在仓库根目录 **`audits/`** 按 [docs/aiot/AUDITS.md](../../../docs/aiot/AUDITS.md) 记一条（勿写密钥）。  
5. **高风险**（大 `migrate`、结构性变更）：事先提醒 **PVE 快照** 等，见 `pre-change-snapshot` runbook。

## 父仓库-only（文档/规则/脚本）

- 根目录：`git add` → `git commit` → `git push`。  
- **无需** bench；除非用户明确要求顺带部署 `ssi_app`。

## 与子代理 / 会话

变更面大或 SSH 长跑与编码并行时，可按 **`aiot-core`** 提示评估 **新开会话** 或 **子代理** 分担。
