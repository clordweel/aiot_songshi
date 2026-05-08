# AGENTS.md — 本仓库 AI 代理导读

1. **首先**阅读 [docs/aiot/INDEX.md](docs/aiot/INDEX.md)（渐进披露入口）。
2. **规则**：`.cursor/rules/*.mdc` 中间 `aiot-core` 与 `frappe-bench-erpnext` 为常驻上下文摘要；自定义 app **`ssi_app`** 默认「本地 `apps/ssi_app` → push GitHub → 服务器单向 pull」见 **`aiot-ssi-app-workflow`**。对用户可见的品牌字样默认 **AIOT**（包名仍为 `ssi_app`，详见 `aiot-core`）。
3. **技能**：按需阅读 `.cursor/skills/<name>/SKILL.md`，不要默认加载全部；三条连通路径（MCP / REST / SSH bench）见 **`frappe-agent-connectivity`**；**本地 push → 服务器 pull → bench 部署** 见 **`aiot-deliver-push-pull-deploy`**。命令面板快捷：**`/deliver-ssi-app`**、**`/deliver-aiot-repo`**、**`/deliver-stack`**（定义见 `.cursor/commands/`）；人类口令表见 [docs/aiot/prompts/deliver-push-pull.md](docs/aiot/prompts/deliver-push-pull.md)。
4. **环境事实**：先读 **[docs/aiot/env/server-baseline.md](docs/aiot/env/server-baseline.md)**（可提交）；站点线 [frappe-site-baseline.md](docs/aiot/env/frappe-site-baseline.md)。密钥等：`docs/aiot/env/*.local.md` 或 **`config/local.env`**（均 gitignore，模板见 `config/agent-connect.env.example`）。
5. **临时目录**：根目录 `tmp/` 放本地脚本与临时输出（见 `tmp/README.md`）；默认不提交。
6. **培训** `docs/aiot/training/`：HumanPrimary；仅当用户显式要求教学/改稿等时**单文件**读取，勿通读全树。
7. **真实执行**后：在仓库根目录 **`audits/`** 追加简报（约定见 [docs/aiot/AUDITS.md](docs/aiot/AUDITS.md)；该目录不入库）。
8. **长上下文 / 换阶段**时：可考虑新开 Agent 会话或使用子代理（见 `aiot-core` 规则）。
