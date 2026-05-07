## 2026-05-08 — 删除江苏松石公司并以「整合会计准则」重建

- 时间：2026-05-08（会话执行）
- 环境：`http://10.0.0.40`，站点 **10-0-0-40.sslip.io**，REST
- 类型：`api_write`；远端 **`bench execute`** 同步科目模板至 **`verified/`**
- 摘要：
  - **`bench execute`** **`ssi_app.ssi_accounts.copy_chart_templates.copy_chart_templates`**：已刷新 **`cn_integrated_chart_of_accounts.json`** / **`cn_custom_chart_of_accounts.json`** 至 **ERPNext `verified/`**。
  - **`DELETE /api/resource/Company/<Doc.name>`**：移除错误科目的既有「江苏松石智能科技有限公司」记录。
  - **`POST Company`**：`chart_of_accounts` **整合会计准则**（对应 **`cn_integrated_chart_of_accounts.json`**），`abbr` **SSZS**，税号等沿用先前设定。
  - **补救**：科目默认值 PATCH 须按 **`Account.company` = 公司 Doc 全称**（中文），不可用缩写 **`SSZS`** 过滤；已运行 **`tmp/patch_company_defaults_sszs.py`**，**256** 条科目，成功写入 **37** 项 PATCH（含 Account Link + scalar）。
  - 脚本修正：**`tmp/recreate_company_sszs.py`**、**`tmp/create_company_sszs.py`** 中 Account 列表改为 **`company_doc_name`**。
- 结果：`ok`
