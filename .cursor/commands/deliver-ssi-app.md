---
description: ssi_app 全链路 — 本地 push + 服务器 git pull + bench（migrate/build/restart）
---

按仓库 **AIOT 交付约定**执行 **ssi_app** 推送—拉取—部署：

1. 读取 `.cursor/skills/aiot-deliver-push-pull-deploy/SKILL.md` 与 `.cursor/rules/aiot-ssi-app-workflow.mdc`。  
2. 在 **`apps/ssi_app`** 确认变更：`git status`；必要时补充 **`git commit`**，推 **`origin develop`**（或当前约定分支）。  
3. 在目标 bench 机 **`~/frappe-bench/apps/ssi_app`** **`git pull`**（与远端单向对齐）；于 bench 根按需 **`bench migrate`** / **`bench build --app ssi_app`** / **`bench restart`**（站点名以 **server-baseline / frappe-site-baseline** 为准）。  
4. **优先**在本机执行：`python scripts/deploy_ssi_app.py --dry-run`，确认无误后 **`python scripts/deploy_ssi_app.py --push`**（需已配置 **`config/local.env`** 等）。若环境不允许跑脚本，再用等价 SSH 命令手工完成。  
5. 服务器产生写影响后，在仓库根目录 **`audits/`** 按 **`docs/aiot/AUDITS.md`** 追加简报（勿写密钥）。重大变更前提醒快照。
