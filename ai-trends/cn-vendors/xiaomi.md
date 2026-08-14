---
title: 小米 MiMo
description: 新晋开源玩家——MiMo-V2-Pro（1T+ 参数、1M 上下文）、coding → claw 路线
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-14
verifiedWith:
  sources:
    - name: Xiaomi MiMo-V2-Pro 官方
      url: https://mimo.xiaomi.com/mimo-v2-pro
      accessedAt: 2026-08-14
    - name: 中国 LLM 现状观察（2026-03）
      url: https://merchmindai.net/blog/zh/post/china-llm-landscape-2026
      accessedAt: 2026-08-14
---

# 小米 MiMo

> **TL;DR**：新晋开源玩家——MiMo-V2-Pro 用 1T+ 参数 + 1M 上下文直接押注 agent 工作负载，路线是「从 coding 扩展到 claw（通用 agent）」。

## 一、定位

小米的 AI 策略是**从模型底座层押注 agent 工作流**：不只是编码，而是更广义的可执行 agent（claw）。官方页面直接写出「generalizing from coding to claw」。

## 二、模型线（截至 2026-08）

| 模型 | 说明 |
| --- | --- |
| **MiMo-V2-Pro** | 旗舰基座：1T+ 总参数 / 42B 激活、1M context、面向真实 agent 负载 |
| **MiMo-V2-Omni** | 统一图像 / 视频 / 音频 / 文本的多模态 agent 基座，原生结构化 tool calling |

## 三、关键事实

- **1M 上下文 + 1T+ 参数**：参数规模超过 1T，总激活参数 42B
- **基准**：PinchBench #3、ClawEval #3（官方口径，全球）
- **开源生态**：把 OpenClaw 称为「正在开源社区快速升温的通用 agent 框架」

## 四、特点

- **Agent 原生**：为 agent 工作负载设计，而非通用聊天
- **多模态 agent 化**：Omni 线把能力扩展到 UI grounding 与结构化 tool calling
- **新晋玩家**：不在传统 AI 创业公司名单里，但版本线推进很快

## 五、适合 / 不适合

**适合**：开源 agent 工作流、长上下文 + 工具调用场景、关注 claw / agent 框架生态的开发者。

**不适合**：需要成熟生态 / 企业服务（新晋玩家，生态与案例少）、中文知识深度要求极高的场景。

## 参考

- [MiMo-V2-Pro 官方页面](https://mimo.xiaomi.com/mimo-v2-pro)（访问于 2026-08-14）
- [中国 LLM 现状观察（2026-03）](https://merchmindai.net/blog/zh/post/china-llm-landscape-2026)（访问于 2026-08-14）

## 下一步

- 看总览 → [国内厂商](/ai-trends/cn-vendors/)
- 对比七家 → [7 厂商横向对比](/reference/model-comparison)

## 如果你想

- 看 DeepSeek → [DeepSeek](/ai-trends/cn-vendors/deepseek)
- 看开源生态 → [开源项目推荐](/ai-trends/research-highlights/open-source)
- 理解 agent 工作流 → [AI Coding 落地](/ai-coding/)
