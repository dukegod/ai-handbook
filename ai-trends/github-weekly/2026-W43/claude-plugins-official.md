---
title: anthropics/claude-plugins-official：插件目录与结构规范
description: Claude Code 官方插件目录深度解读——插件的标准结构、不可变命名约束、skill-bundle 插件，以及它作为 Agent 资产分发标准的意义
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-10-21
---

# anthropics/claude-plugins-official：插件目录与结构规范

> **TL;DR**：这是 Anthropic 维护的 Claude Code 官方插件目录。与其说它是「插件市场」，不如说它是**插件结构的规范发布点**——本周 +5,650，但更值得看的是它定下的那几个约束。

📅 数据窗口：2026-10-15 ~ 2026-10-21 ｜ 🏷️ 分发规范 ｜ 总 star 43,442

## 是什么

仓库本身很小（README 仅约 3.8 KB），因为它的价值不在代码，而在**它公布的结构约定**。

**插件的标准结构：**

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # 插件元数据（必需）
├── .mcp.json            # MCP server 配置（可选）
├── commands/            # 斜杠命令（可选）
├── agents/              # Agent 定义（可选）
├── skills/              # Skill 定义（可选）
└── README.md            # 文档
```

**安装方式：** `/plugin install {plugin-name}@claude-plugins-official`，或在 `/plugin > Discover` 里浏览。

目录分两类：**内部插件**（Anthropic 团队开发，参考实现在 `plugins/example-plugin`）和**外部插件**（第三方伙伴与社区提交，需通过质量与安全标准审核，提交入口是官方表单）。

## 技术亮点

**两个约束条款，是这个仓库真正的「规范」部分：**

1. **插件名不可变。** marketplace 条目里的 `name` 是**不可变的 slug**。发布后不能改——用户是按这个 slug 安装的，改名会导致他们安装失效并报 `plugin-not-found`。要改 UI 上的显示名应该改 `displayName`；确实必须改名时，在 `.claude-plugin/marketplace.json` 顶层加一条 `renames` 映射，加载器会在用户下次 sync 时透明地重写旧 slug。

2. **支持 skill-bundle 插件。** 当插件源仓库只带了 `SKILL.md` 而没有 `.claude-plugin/plugin.json` 清单时，marketplace 条目可以声明这些技能并被正常加载。

**这两条看起来琐碎，实际上是分发层最重要的问题：版本演化不能破坏已安装状态。** 第三方作者想改名、想改结构、想升级到新的清单格式——这些都会破坏存量用户的安装。规范提前把「不可变的东西」和「可演化的东西」分开，是让生态能长期演化的前提。

## 后续发展建议

**这个仓库的信号意义大于它的内容意义：厂商开始为 Agent 资产的分发层定规范了。** 本周同时上榜的还有 `cursor/plugins`（Cursor 的插件规范与官方插件）、`android/skills`（Android 官方用 Kotlin 下场做 Skills）、`wshobson/agents`（跨 harness 市场）、`K-Dense-AI/scientific-agent-skills`、`cathrynlavery/diagram-design`（跨 6 个 harness 的图表 Skill）——**四个不同来源的插件规范同时出现，说明「Agent 资产」正在从各家私产变成一种通用商品**。

三个判断：

- **最终的赢家会是「能力声明」而不是「插件格式」。** 现在每个 harness 的插件结构都略有不同（Claude Code 要 `.claude-plugin/plugin.json`，Codex 用 TOML，Cursor 又是另一套）。格式会继续分化，**但底层会收敛出「这个资产需要什么能力」的标准描述**（需要 hooks？需要 MCP？支持哪些模型别名？），由各家适配器消费。这套描述格式才是长期资产——参考 [wshobson/agents 深读](./wshobson-agents.md) 里的适配器矩阵。
- **「skill-bundle」这种宽松入口会继续放宽。** 允许「只有 SKILL.md、没有清单」也能上架，说明规范在往**降低发布门槛**的方向走。这对生态是好事，但代价是**质量下限下移**——官方目录靠「外部插件需通过质量与安全标准审核」来兜底。**未来审核机制本身会被 AI 化**（自动静态检查 + 抽样人工），这是必然的。
- **对内部团队的直接启示**：如果内部也在维护 Skill / Agent 目录，**「不可变 slug + 显示名可变 + 改名映射」这套约束值得直接照抄**。资产一旦分发给多个团队，改名导致的静默失效是最难排查的一类问题。相关规范可参考 [AI Native 三层架构](../../../ai-harness/three-layer-architecture.md) 里的模块模板。

## 下一步

- 看跨 harness 怎么分发同一套资产 → [wshobson/agents 深读](./wshobson-agents.md)
- 看生态里 Skill 怎么被组织成领域能力 → [scientific-agent-skills 深读](./scientific-agent-skills.md)

## 如果你想

- 想理解 MCP 在插件体系里的位置 → [工具调用](../../../getting-started/tool-calling.md)
- 想看插件生态的整体图景 → [开源项目推荐](../../research-highlights/open-source.md)
