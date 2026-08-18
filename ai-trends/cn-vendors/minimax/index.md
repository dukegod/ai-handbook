---
title: MiniMax 全系
description: MiniMax M2.7——Agentic 旗舰、205K 上下文、极致性价比、全模态
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-14
verifiedWith:
  sources:
    - name: MiniMax 官方定价
      url: https://platform.minimax.io/docs/guides/pricing-paygo
      accessedAt: 2026-08-14
    - name: MiniMax M2.7 发布
      url: https://www.minimax.io/news/minimax-m27-en
      accessedAt: 2026-08-14
---

# MiniMax 全系

> 7 家厂商里**性价比最激进（$0.3/M input）+ Agentic 定位最明确 + 全模态覆盖最广**。

## 一、公司背景

MiniMax 由前商汤科技副总裁闫俊杰创立，2021 年成立，总部上海。核心策略是 **「Agentic + 全模态 + 低价」**——不只做文本，语音 / 视频 / 图像 / 音乐全线自研。商业模式：API 计费 + 消费端产品（海螺 / Talkie）+ 企业方案。海外用 `platform.minimax.io`，国内用 MiniMax 开放平台。

## 二、模型矩阵（截至 2026-08）

| 模型 | 定位 | 上下文 | 主要场景 |
| --- | --- | --- | --- |
| **MiniMax-M2.7** | Agentic 旗舰 | 205K | Agent 工作流 / 编码 / 办公 |
| **MiniMax-M2.5 / M2.1** | 前代 | — | 已由 M2.7 取代 |
| **MiniMax-VL / 语音 / 视频线** | 全模态 | — | 视觉 / 音频 / 视频生成 |

> **产品线逻辑**：M2.7 是官方定位的 **agentic flagship**（文本，2026-03 发布），主打复杂 agent harness、Agent Teams、动态工具搜索、软件工程与办公任务；多模态走独立模型线。

## 三、技术架构

**Agentic 原生** —— M2.7 的基准全部围绕 agent 任务设计：SWE-Pro 56.22%、VIBE-Pro 55.6%、Terminal Bench 2 57.0%（官方发布数据）——官方明确把「复杂 agent 工作负载」作为第一目标，而非通用聊天。

**全模态自研** —— 与多数厂商「文本为核、多模态为插件」不同，MiniMax 的语音 / 视频 / 图像 / 音乐是独立自研产品线，走「全模态矩阵」路线。

## 四、核心能力

| 能力 | 描述 |
| --- | --- |
| **Agent Teams** | 多 agent 协作编排 |
| **动态工具搜索** | 按需发现 / 加载工具 |
| **MCP 支持** | 开放协议接入 |
| **全模态** | 文本 + 语音 + 视频 + 图像 + 音乐 |

## 五、部署形态

| 部署 | 平台 |
| --- | --- |
| **MiniMax API** | `platform.minimax.io`（海外）/ 国内开放平台 |
| **消费端** | 海螺 / Talkie 等产品 |
| **企业** | 云厂商 + 私有化方案 |

## 六、价格（截至 2026-08，官方定价）

| 模型 | Input | Output | 缓存读 |
| --- | --- | --- | --- |
| MiniMax-M2.7 | $0.30 / MTok | $1.20 / MTok | $0.06 |

**MiniMax M2.7 是 7 家厂商里 input 价最低的旗舰之一**（$0.3/M，仅为 Claude Sonnet 5 的约 1/7）——走「极致性价比 + agentic 能力」的错位竞争路线。

## 七、适合场景 / 不适合场景

**适合**：
- Agent 工作流 / 工具调用（Agentic 原生设计）
- 成本敏感的大规模调用
- 多模态需求（语音 / 视频 / 图像全套自研）

**不适合**：
- 需要顶级推理质量的场景（基准仍落后 Claude / GPT 旗舰）
- 中文知识深度要求高的场景（中文生态弱于 Qwen / GLM / Kimi）
- 需要长链条稳定性的生产环境（年轻模型，生态成熟度待验证）

## 关键洞察

- **价格是最大的武器**——$0.3/M input 直接打穿成本线
- **Agentic 是明确路线**——不是「通用模型 + Agent 能力」，是「为 Agent 而生的模型」
- **全模态矩阵**——少数全线自研多模态的中国厂商

## 参考

- [MiniMax 官方定价](https://platform.minimax.io/docs/guides/pricing-paygo)（访问于 2026-08-14）
- [MiniMax M2.7 发布](https://www.minimax.io/news/minimax-m27-en)（访问于 2026-08-14）
- [中国 LLM 现状观察（2026-03）](https://merchmindai.net/blog/zh/post/china-llm-landscape-2026)（访问于 2026-08-14）

## 下一步

- 横向对比 7 家 → [5 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 按场景选型 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)
- 看技术路线 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 如果你想

- 看 Kimi 档案 → [Moonshot · Kimi 全系](/ai-trends/cn-vendors/moonshot/)
- 看 GLM 档案 → [Zhipu · 智谱 GLM 全系](/ai-trends/cn-vendors/zhipu/)
- 看国内厂商动态 → [国内厂商](/ai-trends/cn-vendors/)
