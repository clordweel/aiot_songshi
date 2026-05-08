# 口令备忘：推送 → 远端 → 服务器拉取部署

与 **`.cursor/skills/aiot-deliver-push-pull-deploy/SKILL.md`**、**`.cursor/commands/`** 下 **`deliver-*`** 指令一致；对人类与代理通用。

## 常用口令（说什么）

| 说法 | 期望行为 |
|------|-----------|
| 「**交付 ssi_app**」「**推送部署**」「**推到服务器**」 | `apps/ssi_app` → `push` → 目标机 `apps/ssi_app` **`pull`** → **`bench migrate/build/restart`** |
| 「**服务器拉一下**」「**同步 bench**」 | 仅 SSH：app 目录 **`pull`** + bench 收口（默认先有远端新提交） |
| 「**只推父仓库**」「**文档入库**」 | 仅在 **`aiot_songshi` 根目录** `commit`/`push`，不上 bench |
| 「**全栈交付**」 | 父仓库 push + **`ssi_app`** 推送部署（先后顺序见下） |

## Cursor 快捷指令（命令面板）

- **`deliver-ssi-app`** — 二开 app 全链路（可用 **`scripts/deploy_ssi_app.py --push`**）。  
- **`deliver-aiot-repo`** — 仅父仓库 Git。  
- **`deliver-stack`** — 父仓库与 **ssi_app** 依次处理。

## 顺序口诀

1. **ssi_app**：单一真相在 **`apps/ssi_app`**；服务器 **只 pull**。  
2. **bench**：在 **`~/frappe-bench`** 根跑 **`migrate`** / **`build`** / **`restart`**（站点名见 **frappe-site-baseline**）。  
3. **审计**：SSH/bench **写库或改进程** 后 → 仓库根目录 **`audits/`**（见 **AUDITS.md**）。  
4. **脚本**：`python scripts/deploy_ssi_app.py --dry-run` → `--push`。
