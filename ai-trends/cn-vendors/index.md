---
title: 国内厂商
description: DeepSeek / 豆包 / 文心 / 混元 / 小米 MiMo 等国内大模型厂商——开源主线与闭源主线
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-14
verifiedWith:
  sources:
    - name: 中国 LLM 现状观察（2026-03）
      url: https://merchmindai.net/blog/zh/post/china-llm-landscape-2026
      accessedAt: 2026-08-14
    - name: DeepSeek 官方
      url: https://api-docs.deepseek.com
      accessedAt: 2026-08-14
    - name: 机器之心
      url: https://www.jiqizhixin.com
      accessedAt: 2026-08-14
---

# 国内厂商

> **TL;DR**：国内大模型市场分「开源」（Qwen、DeepSeek 为代表）与「闭源」（豆包、文心、混元为代表）两条主线。开源线对开发者价值最大。

⏱ 预计阅读时间：5 分钟

## 玩家地图（截至 2026-08）

| 阵营 | 厂商 | 代表模型（2026 年） | 档案 |
| --- | --- | --- | --- |
| 开源 | DeepSeek | V4（V4-Flash / V4-Pro） | [DeepSeek](./deepseek) |
| 开源 | 小米 | MiMo-V2-Pro / Omni | [小米 MiMo](./xiaomi) |
| 开源 | 阿里 | Qwen3.5 / Qwen3.8-Max | [厂商档案 · Qwen](/ai-trends/vendors/qwen) |
| 开源 | 月之暗面 | Kimi K2.5 / K3 | [厂商档案 · Kimi](/ai-trends/vendors/moonshot) |
| 开源 | 智谱 | GLM-5.2 | [厂商档案 · GLM](/ai-trends/vendors/zhipu) |
| 闭源 | 字节 | 豆包 / Seed 2.0 | [字节豆包](./doubao) |
| 闭源 | 百度 | 文心 5.0 | [百度文心](./baidu) |
| 闭源 | 腾讯 | 混元 2.0 | [腾讯混元](./tencent) |

> 格局要点：**豆包是消费入口的赢家（2025-08 起反超 DeepSeek），Qwen / DeepSeek 是开源生态的赢家**——两者不是同一批公司。另有 MiniMax（M2.7，[厂商档案](/ai-trends/vendors/minimax)）、StepFun（Step-3.5-Flash）等持续迭代。

## 两条主线

**开源线**（DeepSeek、Qwen、Kimi、GLM、MiMo）：

- 权重可下载，可私有化部署，可控成本
- 适合：企业私有化、数据敏感场景、二次开发
- 部署选型见 [AI Coding · 企业部署](/ai-coding/enterprise/deployment)

**闭源线**（豆包、文心、混元）：

- API 调用，免运维，迭代由厂商推进
- 适合：快速上线、无强数据约束、成本敏感（部分低价）

> **判断框架**：先问「数据能不能出域、要不要私有化」。能出域且团队小 → 闭源 API 最快；要私有化 → 看开源线。

## 开源降本 → 军备竞赛（2024-12 ~ 2026）

- **DeepSeek-V3**（2024-12）：训练成本约为同代闭源模型的十分之一量级——「降本」信号
- **DeepSeek-R1**（2025-01）：开源推理模型，效果对标 o1 系列——「推理能力平民化」信号
- **2026 年夏**：三款国产旗舰密集发布——Kimi K3（7 月）、Qwen3.8-Max（8 月）、DeepSeek V4（7 月）——开源与闭源的能力差被进一步压缩

**影响**：开源 / 闭源能力差大幅缩小；推理成本快速下降；API 价格战加剧。**竞争焦点从「谁能训练出更强模型」转向「谁能成为 Claude Code / Cline 等编码工作流的默认后端」**——各家都在做 Anthropic 兼容接口。对开发者是红利期。

## 如何跟踪

1. **官方源**：[DeepSeek 官方](https://api-docs.deepseek.com)、各家开放平台文档（火山引擎 / 千帆 / 混元）
2. **社区源**：机器之心、量子位、Hugging Face 趋势榜（开源模型下载量）
3. **关键信号**：开源新版本发布（权重是否开放）、API 价格调整、Anthropic / OpenAI 兼容接口的接入情况、备案与合规动态（截至 2025 年底累计 748 款生成式 AI 服务完成备案）

## 参考

- [中国 LLM 现状观察（2026-03）](https://merchmindai.net/blog/zh/post/china-llm-landscape-2026)（访问于 2026-08-14）
- [DeepSeek 官方](https://api-docs.deepseek.com)（访问于 2026-08-14）
- [机器之心](https://www.jiqizhixin.com)（访问于 2026-08-14）

## 下一步

- 逐家深入 → [DeepSeek](./deepseek) / [字节豆包](./doubao) / [百度文心](./baidu) / [腾讯混元](./tencent) / [小米 MiMo](./xiaomi)
- 看海外巨头 → [ChatGPT 动态](/ai-trends/product-updates/chatgpt) / [Claude 动态](/ai-trends/product-updates/claude)
- 按月汇总 → [月度产品速报](/ai-trends/product-updates/monthly)

## 如果你想

- 私有化部署 → [AI Coding · 企业部署](/ai-coding/enterprise/deployment)
- 对比七家厂商 → [7 厂商横向对比](/reference/model-comparison)
- 评估开源模型 → [开源项目推荐](/ai-trends/research-highlights/open-source)
