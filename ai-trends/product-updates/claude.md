---
title: Claude 动态
description: Anthropic 产品线跟踪——模型发布、Claude Code、API 与生态，附已核实里程碑
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-14
verifiedWith:
  sources:
    - name: Anthropic News
      url: https://www.anthropic.com/news
      accessedAt: 2026-08-14
    - name: Claude 模型总览
      url: https://platform.claude.com/docs/en/about-claude/models/overview
      accessedAt: 2026-08-14
    - name: Claude Code 文档
      url: https://code.claude.com/docs
      accessedAt: 2026-08-14
---

# Claude 动态

> **TL;DR**：Anthropic 产品线 = 模型（Claude 家族）+ 工具（Claude Code / Agent SDK）+ 协议（MCP）。跟踪三条线，就能抓住全部关键变化。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- Anthropic 产品线的三条跟踪线
- 模型家族当前的完整谱系
- 与 ChatGPT 动态的差异化（[ChatGPT 动态](/ai-trends/product-updates/chatgpt)）

## 一、三条跟踪线

**模型线**：Claude 家族发布与定价。核心看「哪个模型在哪个价位，能力定位是什么」。

**工具线**：Claude Code（CLI）、Claude Agent SDK、Claude.ai 产品功能。对开发者，这条线比模型线更常变化。

**协议线**：MCP（Model Context Protocol）的演进。MCP 已开源为开放标准，生态变化影响所有工具。

## 二、模型家族谱系（截至 2026-08）

| 模型 | 定位 | 关键事实 |
| --- | --- | --- |
| **Fable 5** | 顶级专家（specialist） | 2026-06-09 GA；$10 / $50 per MTok；长时运行 Agent 专用 |
| **Opus 5** | 最强推理（expert） | 接近 Fable 5 智能、半价（$5 / $25）；Claude Pro / Max 默认 |
| **Sonnet 5** | 均衡型（generalist） | 性价比主力；日常编码与工具调用 |
| **Haiku 4.5** | 快速轻量 | 延迟敏感场景；批量任务 |
| ~~Opus 4.8~~ | 上一代推理 | 已被 Opus 5 取代，仍可用 |
| **Mythos 5** | 网络安全 / 生物顶级 | Project Glasswing；limited availability，未 GA |

> 官方比喻：Fable = 顶级专家，Opus = 专家，Sonnet = 通才。选型对照见 [模型选择](/claude-code/basics/model-selection)。谱系核实自官方 [model overview](https://platform.claude.com/docs/en/about-claude/models/overview) 与 [Opus 5 发布博客](https://www.anthropic.com/news/claude-opus-5)（访问于 2026-08-14）。

## 三、工具线现状

- **Claude Code**：Anthropic 官方 CLI，与 IDE 插件、GitHub Actions 集成。详见 [Claude Code 章节](/claude-code/)
- **Claude Agent SDK**：从代码构建自定义 Agent，与 Anthropic SDK（HTTP 客户端）是两回事
- **Claude.ai**：网页 / 桌面 / 移动端产品，面向终端用户

## 四、如何跟踪

1. **官方源**：[Anthropic News](https://www.anthropic.com/news)、[Claude 模型总览](https://platform.claude.com/docs/en/about-claude/models/overview)、[Claude Code docs](https://code.claude.com/docs)
2. **更新节奏**：模型大版本约半年一更；Claude Code 几乎每周迭代
3. **判断原则**：模型更新看「价格 / 能力 / 上下文」三要素；工具更新看「对现有工作流的破坏性」——破坏性变更优先跟进

## 参考

- [Anthropic News](https://www.anthropic.com/news)（访问于 2026-08-14）
- [Claude 模型总览](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-08-14）
- [Fable 5 深度解读](/claude-capabilities/models/fable) — 本站已核实（2026-07-24）

## 下一步

- 看 ChatGPT 那边 → [ChatGPT 动态](/ai-trends/product-updates/chatgpt)
- 看国内厂商 → [国内厂商动态](/ai-trends/product-updates/china)
- 按月汇总所有动态 → [月度产品速报](/ai-trends/product-updates/monthly)

## 如果你想

- 选模型 → [模型选择](/claude-code/basics/model-selection)
- 了解 Fable 5 → [Fable 5 深度解读](/claude-capabilities/models/fable)
- 对比七家厂商 → [7 厂商横向对比](/reference/model-comparison)
