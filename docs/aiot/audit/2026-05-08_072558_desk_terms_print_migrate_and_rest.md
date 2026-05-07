## 2026-05-08 07:25:58 — desk_terms_print：migrate 未落库原因与 REST 补导入

- 时间：2026-05-08 07:25:58 CST (UTC+8)（本机记录）
- 环境：`10.0.0.40`，站点 `10-0-0-40.sslip.io`；REST 凭据来自 `config/local.env`（本文不复述）。
- 类型：`api_write` / `deploy`（说明）
- 摘要：
  1. **历史**：`hooks.fixtures` 已包含 `desk_terms_print/*.json`，此前 **`bench migrate` 已执行**，但 fixture 中 **`Print Format.module` 指向 COS 应用模块**（`COS Stock` / `COS Share` 等），目标站 **未安装 COS**，**`Module Def` 不存在**，导入阶段无法合法写入 **`Print Format`**（站点侧核实：`库存调账 - 标准` 等不存在）。
  2. **代码**：已将 **`print_format.json`** 内 **`module`** 映射为 **`ssi_stock` / `ssi_app` / `ssi_accounts`**（提交 **`ssi_app` `aeb08cb`**），并在服务器 **`git pull` + `bench migrate`**；migrate 日志仅有笼统 **`Syncing fixtures...`**，**仍未自动出现全部打印格式**（可能与 fixture 同步策略/静默失败有关；未在本次深挖源码）。
  3. **补救**：本地脚本 **`tmp/import_ssi_desk_fixtures.py`** 通过 REST **幂等**导入 `desk_terms_print` 四类：**`Print Format`** 新建 21、更新 1；**`Print Style`**、`**Letter Head**`、**`Terms and Conditions`** 全部新建成功（失败 0）。事后 **`Print Format` 且 `module in (ssi_stock, ssi_app, ssi_accounts)`** 共 **22** 条。
- 结果：`ok`
- 审批（可选）：—
