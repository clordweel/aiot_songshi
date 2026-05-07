## 2026-05-09 — 科目表模板标题仍为「君海…」：根因与修复

- 时间：2026-05-09（会话执行）
- 环境：**10.0.0.40**，**frappe**，bench **`~/frappe-bench`**，站点 **`10-0-0-40.sslip.io`**
- 类型：`bench` / `git`（服务器）
- 摘要：
  - **现象**：Desk 新建公司「科目表模板」仍为 **君海定制企业会计准则**。
  - **根因**：① 服务器 **`apps/ssi_app`** 停在旧提交（未 **`git pull`**）；② 早前 **curl/SCP** 在 **`chart_of_accounts/custom/`**、**`ssi_accounts/copy_chart_templates.py`** 留下 **未跟踪文件**，**`git pull`** 报 *untracked would be overwritten*，合并中止；③ 复制脚本只是把磁盘上的旧 JSON 拷进 **`verified/`**，故界面不变。
  - **处理**：在 **`~/frappe-bench/apps/ssi_app`** 删除冲突未跟踪文件后 **`git pull origin develop`**（含 **`name`: 定制企业会计准则** 的 JSON），再执行 **`copy_chart_templates`**；校验 **`verified/cn_custom_chart_of_accounts.json`** 前几行已为 **`定制企业会计准则`**。
- 结果：`ok`
- **后续**：部署脚本 **`scripts/deploy_ssi_app.py`** 应以 **`git pull`** 为主线；若遇同类冲突，先清理 **`custom/*.json`** / 孤立 **`copy_chart_templates.py`**（已由仓库跟踪时可 **`git checkout --`** 恢复），再拉取。
