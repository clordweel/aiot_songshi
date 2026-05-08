---
description: 仅父仓库 aiot_songshi — commit + push（不涉及 bench）
---

执行 **本仓库根目录**（`aiot_songshi`）的 Git 交付，**不含** bench 部署：

1. 在仓库根目录查看 `git status`，仅纳入用户意图范围内的文件。  
2. 撰写恰当 **`git commit`** 说明并 **`git push`** 到约定远端分支。  
3. **不要**除非用户明确要求 — 登录 SSH 或执行 `bench`。  
4. 若本次仅为文档/规则变更且无环境写入，**无需**写 **`audits/`**（真实 SSH/bench/API 写后再记）。
