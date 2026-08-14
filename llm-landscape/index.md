---
title: LLM landscape 总览
description: 5 家主流大模型横向对比——Claude / GPT / Kimi / Zhipu / Qwen 的技术架构、能力与场景
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-11
---

# LLM landscape 总览

> v0.4.3 阶段骨架（9 篇 stub 已建）—— v0.5 阶段 1 起逐步填实。详见 [architecture review · v0.4.3](/contributing/architecture-review-2026-08-10)。

## 5 家厂商一览

| 厂商 | 模型 | 旗舰 | 开源策略 | 主力市场 |
| --- | --- | --- | --- | --- |
| [Anthropic](./anthropic) | Claude | Opus 5 / Sonnet 5 / Haiku 4.5 | 闭源 | 全球 + 中文 |
| [OpenAI](./openai) | GPT | GPT-5.6 Sol / Terra / Luna | 闭源 + 开源双轨 | 全球 |
| [Moonshot 月之暗面](./moonshot) | Kimi | K3 / K2.5 | 部分开源 | 中文 |
| [Zhipu 智谱](./zhipu) | GLM | GLM-5.2 / GLM-5 | 部分开源 | 中文 |
| [阿里 通义千问](./qwen) | Qwen | Qwen3.8-Max / Qwen3.5 | 开源 | 全球 + 中文 |

## 配套内容

- [技术架构总览](./architecture) — Transformer 演进 / MoE / 长上下文 / RL 训练方法
- [5 厂商横向对比](./comparison) — 基准 / 上下文 / 价格 / 部署
- [选型决策树](./selection-guide) — 什么任务选什么模型

## 你能在这里学到

- 5 家主流大模型的核心差异
- 各家技术路线选择（dense vs MoE / 长上下文实现 / RL 训练）
- 选型时该看哪些维度

## 前置知识

- 了解 Transformer 基础架构
- 接触过至少 1 个 LLM API（Claude / GPT / Kimi 任一）

## 下一步

- 深入某家厂商 → [Anthropic Claude 全系](./anthropic)
- 看技术架构对比 → [技术架构总览](./architecture)
- 选型决策 → [选型决策树](./selection-guide)
