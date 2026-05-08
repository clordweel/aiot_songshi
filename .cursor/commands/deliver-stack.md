---
description: 父仓库 + ssi_app 双仓库依次推送（先文档/规则，再二开 app 部署）
---

用户同时改了 **父仓库** 与 **`apps/ssi_app`** 时，按顺序：

1. **父仓库**：根目录 `git add` / `commit` / `push`（见命令 **`deliver-aiot-repo`** 的意图）。  
2. **ssi_app**：`apps/ssi_app` 内 `commit` / `push`，再在服务器 **pull + bench**（见命令 **`deliver-ssi-app`**）。  
3. 只对 **步骤 2 的服务器写操作** 记 **`audits/`**（若步骤 1 无环境写入则不强制）。
