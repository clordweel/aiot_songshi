## 2026-05-08 — REST 创建「江苏松石智能科技有限公司」并套用科目默认值

- 时间：2026-05-08（会话执行）
- 环境：`http://10.0.0.40`，站点 **10-0-0-40.sslip.io**，REST **Administrator** Key
- 类型：`api_write`（Company 插入与更新）
- 摘要：
  - **Company**：`company_name` **江苏松石智能科技有限公司**，`abbr` **SSZS**，`tax_id` **91320321MA203BEF9X**，`country` China，`currency` CNY，`valuation_method` Moving Average；科目模板 **`整合会计准则`**（对应 **`cn_integrated_chart_of_accounts.json`**）。
  - **`company_defaults.json`**（参考 ai_cos_ops vendor cos）：将其中 **标准 Company 字段 + 与 DocType 匹配的 scalar** 映射为 Account Link 后 **`PUT /api/resource/Company/<name>`**；含收发类库存、折旧、暂估等字段。**不含** cos 专有 **custom_*** 字段（当前站点 Company 上无对应自定义字段）。
  - 本地一次性脚本：`tmp/create_company_sszs.py`（不入库）。
- 结果：`ok`
- 备注：建议在 Desk 核对 **默认银行账户**等是否与业务一致；人事/报销相关科目若 Company 无字段需在站点二次扩展 DocType 后再补。
