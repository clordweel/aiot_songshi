# AGENTS.md — 本仓库 AI 代理导读

1. **首先**阅读 [docs/aiot/INDEX.md](docs/aiot/INDEX.md)（渐进披露入口）。
2. **规则**：`.cursor/rules/*.mdc` 中间 `aiot-core` 与 `frappe-bench-erpnext` 为常驻上下文摘要。
3. **技能**：按需阅读 `.cursor/skills/<name>/SKILL.md`，不要默认加载全部。
4. **环境事实**：`docs/aiot/env/*.template.md`；填入的 `*.local.md` 已 gitignore。
5. **培训** `docs/aiot/training/`：HumanPrimary；仅当用户显式要求教学/改稿等时**单文件**读取，勿通读全树。
6. **真实执行**后：按 [docs/aiot/audit/README.md](docs/aiot/audit/README.md) 追加简报。
