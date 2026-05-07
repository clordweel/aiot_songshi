# AIOT 培训与学习路径（HumanPrimary）

本目录为人类自学与内训准备，内容可详尽。**Cursor 代理默认不应批量读取整棵 `training/`**；仅在用户明确要求讲解、改稿、出题等时，**按单文件**打开，避免撑爆上下文。

## 阅读顺序建议

1. [levels/L0-cursor-models.md](levels/L0-cursor-models.md) — 按任务选模型档位（新手优先）
2. [levels/L1-operator.md](levels/L1-operator.md) — 业务与日常操作认知
3. [levels/L2-ops-bench.md](levels/L2-ops-bench.md) — bench 与运维
4. [levels/L3-developer.md](levels/L3-developer.md) — 二开与 API 深入
5. [levels/L4-governance.md](levels/L4-governance.md) — 审批、留痕、合规

## AI 使用策略（摘要）

- 普通开发/运维任务：**不要**让模型通读全部培训稿。
- 内训场景：指定章节路径，单文件加载。

## 维护

- **.stack / 流程大改**后检查是否需同步更新对应章节。
- **Cursor 模型列表**变化时，主要维护 `L0-cursor-models.md` 中的**档位与场景**；具体型号名可放可替换附录并定期核对。

与项目事实对照：[../INDEX.md](../INDEX.md)、[../env/](../env/)。
