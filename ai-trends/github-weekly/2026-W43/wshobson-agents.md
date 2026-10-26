---
title: wshobson/agents：跨 harness 分发同一套 Agent 资产
description: wshobson/agents 深度解读——「一份 Markdown 源 + 各家适配器」的跨 harness 分发模型，以及它对 A2A 协议落地的启示
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-21
---

# wshobson/agents：跨 harness 分发同一套 Agent 资产

> **TL;DR**：它让一份 Agent 插件同时跑在 Claude Code、Codex CLI、Cursor、OpenCode、GitHub Copilot、Antigravity、Pi 上——做法是「一份 Markdown 源 + 各家适配器生成」。本周只涨了 665 star，但**它是本周榜单里对 A2A 最有参考价值的一个**。

📅 数据窗口：2026-10-15 ~ 2026-10-21 ｜ 🏷️ 跨 harness 生态 / 分发模型 ｜ 总 star 41,317

## 是什么

[agents](https://github.com/wshobson/agents) 是一个**多 harness 的 Agent 插件市场**。核心机制在「How it works」一节说得很清楚：

- 一个插件把相关的 agents、skills、commands 归到 `plugins/` 下。例如 `python-development` 含 3 个 agent、16 个 skill、1 个脚手架命令。
- **贡献者只维护一份 Markdown 源**（Claude Code 插件格式）。支持原生注册表的 harness 直接指向这份源；其余 harness 由**适配器生成**所需格式。
- **不同 harness 的差异被抽象成映射问题**：command 可能降级成 skill 或 prompt 模板；agent 格式、模型选择、工具权限各家不同。源 agent 里写模型别名（`opus` / `sonnet` / `haiku` / `fable` / `inherit`），适配器负责把别名映射到各 harness 的模型设置——有些 harness 对 `inherit` 有固定默认值。

各 harness 的安装路径与能力边界在 README 里有对照表：Claude Code 走插件市场（可拿到插件级 hooks 与 MCP 配置），Codex CLI 走原生市场或生成产物（生成的 TOML agent 需另走 skill 路径），Cursor / OpenCode / Antigravity / Copilot / Pi 各自有 `make install-<harness>` 或生成式安装。

质量方面有 `make generate-all` / `make validate STRICT=1` / `make garden`，以及 `plugin-eval` 做静态 skill 校验。README 明确标注了 LLM judge 与 Monte Carlo 层**尚未对照人工标签验证**，只是模型自评——这个坦诚度值得肯定。

## 技术亮点

**它把「协议不统一」这件事从每个插件作者的负担，变成了平台层的适配问题。** 这是本周最重要的结构性变化。

对比一下：如果一个插件作者要支持 7 个 harness，他面对的是 7 套插件结构、7 套能力矩阵、7 套模型配置命名。wshobson/agents 把这个成本收敛到**适配器**里，插件作者只写一份源。插件生态的供给曲线因此从 O(1) 变成 O(1)，而不是 O(harness 数)。

这背后是一个更本质的观察：**Agent 资产（skill / agent 定义 / 命令）的可移植性，比 Agent 运行时的可移植性成熟得早得多。** 运行时协议还在 A2A 之类的事情上拉锯（见 [A2A 协议行业深度调研](../../industry/a2a-protocol.md)），而资产层已经默认「应该能跑在任何 harness 上」了。

## 后续发展建议

**这可能是本周对 A2A 落地最有参考价值的项目，因为它给出了 A2A 缺的那一半答案。** A2A 解决的是「Agent 之间怎么通信」，但企业落地的第一道门槛其实是「我写的 Agent 资产能不能在别人的平台上跑起来」。资产层的适配器模式，恰好是这条链路上可操作的部分。

三个具体判断：

- **「适配器」这个模式会沉淀成独立层，而不是每个市场各写一份。** 现在已经有至少三个项目在做同类的事（`wshobson/agents`、`cursor/plugins`、`anthropics/claude-plugins-official`），加上 `android/skills` 用 Kotlin 官方下场。**下一阶段的赢家会是「适配器注册表」**——描述每个 harness 的能力矩阵（支持 hooks？支持 MCP？模型别名怎么映射？），让适配器可插拔。现在这些映射是各家仓库里的 Python 代码，未来应该收敛成标准化的能力描述格式。
- **模型别名映射是当前最脏的一块，也是最先会出事的。** `opus` / `sonnet` / `haiku` / `fable` / `inherit` 这套别名本身是 Claude 侧的概念；映射到别的 harness 时要么翻译成本地模型名，要么退化成默认值。`inherit` 在部分 harness 有固定默认——**这意味着同一个资产在不同 harness 上跑出来的行为可能不一致**，而用户以为是同一份配置。对企业来说这是个真实的合规风险：跨 harness 的可复现性目前没有保证。建议关注是否有社区开始定义「能力声明 + 降级声明」的约定。
- **对内部平台团队的直接启示**：如果要做多 Agent 协作平台，**资产层和执行层应该解耦**。资产用一份源 + 能力描述，执行时由适配器决定落在哪个 harness 上跑。这样新增一个执行引擎时，不需要重写资产，也不需要让每个资产作者适配。这与多系统的边界划分逻辑是一样的——先定义接口契约，再谈实现。

**风险提示**：生态项目的成败高度依赖分发渠道而非技术质量。wshobson/agents 本周仅 +665 star（总 41,317），说明它**没赶上本轮爆发窗口**——爆发窗口被 `morluto/rea` 这类「单点能力惊艳」的项目拿走了。它的价值是结构性正确，但需要等市场从「尝鲜单个神技能」转向「建设自己的 Agent 资产库」时才会放量。

## 下一步

- 看官方如何定义插件结构与命名规范 → [官方插件目录深读](./claude-plugins-official.md)
- 看协议层（Agent 之间怎么通信）→ [A2A 协议行业深度调研](../../industry/a2a-protocol.md)

## 如果你想

- 想理解为什么模型别名会出问题 → [模型选型决策树](../../model-selection/model-selection-guide.md)
- 想看多 Agent 的运行时协作长什么样 → [ruflo 深读](./ruflo.md)
