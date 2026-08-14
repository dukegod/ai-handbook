---
title: 国内厂商动态
description: 阿里 Qwen、DeepSeek、Kimi、GLM 等国内大模型厂商跟踪——开源主线与闭源主线
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

# 国内厂商动态

> **TL;DR**：国内大模型市场分「开源」（Qwen、DeepSeek 为代表）与「闭源」（豆包、Kimi、GLM 为代表）两条主线。开源线对开发者价值最大。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 国内主要玩家地图与各自强项
- 「开源 vs 闭源」两条主线的判断框架
- DeepSeek 现象对行业的影响
- 跟踪信息源

## 一、玩家地图（截至 2026-08）

| 阵营 | 厂商 | 代表模型（2026 年） | 特点 |
| --- | --- | --- | --- |
| 开源 | 阿里 | Qwen3.5 / Qwen3.8-Max | 开源生态最完整，开发者生态全球影响力最大 |
| 开源 | DeepSeek | V4（V4-Flash / V4-Pro） | 降本标杆，技术品牌最强 |
| 开源 | 月之暗面 | Kimi K2.5 / K3 | 2.8T 参数旗舰，7 月开源 |
| 开源 | 智谱 | GLM-5 | 主打 Agentic Coding，744B / 40B |
| 开源 | 小米 | MiMo-V2-Pro / Omni | 1T+ 参数，通用 agent 基座，新晋玩家 |
| 闭源 | 字节 | 豆包 / Seed 2.0 | 消费端入口第一（2025-08 起反超 DeepSeek） |
| 闭源 | 百度 | 文心 5.0 | 原生全模态，云 + 搜索生态 |
| 闭源 | 腾讯 | 混元 2.0 | 微信生态场景，Anthropic 兼容接口 |

> 格局要点：**豆包是消费入口的赢家，Qwen / DeepSeek 是开源生态的赢家**——两者不是同一批公司。另有 MiniMax（M2.7）、StepFun（Step-3.5-Flash）等持续迭代。

## 二、两条主线

**开源线**（Qwen、DeepSeek）：

- 权重可下载，可私有化部署，可控成本
- 适合：企业私有化、数据敏感场景、二次开发
- 部署选型见 [AI Coding · 企业部署](/ai-coding/enterprise/deployment)

**闭源线**（豆包、Kimi、GLM、文心、混元）：

- API 调用，免运维，迭代由厂商推进
- 适合：快速上线、无强数据约束、成本敏感（部分低价）

> **判断框架**：先问「数据能不能出域、要不要私有化」。能出域且团队小 → 闭源 API 最快；要私有化 → 看开源线。

## 三、开源降本 → 军备竞赛（2024-12 ~ 2026）

- **DeepSeek-V3**（2024-12）：训练成本约为同代闭源模型的十分之一量级——「降本」信号
- **DeepSeek-R1**（2025-01）：开源推理模型，效果对标 o1 系列——「推理能力平民化」信号
- **2026 年夏**：三款国产旗舰密集发布——Kimi K3（7 月）、Qwen3.8-Max（8 月）、DeepSeek V4（7 月）——开源与闭源的能力差被进一步压缩

**影响**：开源 / 闭源能力差大幅缩小；推理成本快速下降；API 价格战加剧。**竞争焦点从「谁能训练出更强模型」转向「谁能成为 Claude Code / Cline 等编码工作流的默认后端」**——各家都在做 Anthropic 兼容接口。对开发者是红利期。

## 四、如何跟踪

1. **官方源**：[Qwen 官方](https://qwenlm.github.io)、[DeepSeek 官方](https://api-docs.deepseek.com)、各家开放平台文档（百炼 / 火山引擎 / 千帆）
2. **社区源**：机器之心、量子位、Hugging Face 趋势榜（开源模型下载量）
3. **关键信号**：开源新版本发布（权重是否开放）、API 价格调整、Anthropic / OpenAI 兼容接口的接入情况、备案与合规动态（截至 2025 年底累计 748 款生成式 AI 服务完成备案）

## 参考

- [Qwen 官方](https://qwenlm.github.io)（访问于 2026-08-14）
- [DeepSeek 官方](https://www.deepseek.com)（访问于 2026-08-14）
- [机器之心](https://www.jiqizhixin.com)（访问于 2026-08-14）

## 下一步

- 看海外巨头 → [ChatGPT 动态](/ai-trends/product-updates/chatgpt) / [Claude 动态](/ai-trends/product-updates/claude)
- 按月汇总 → [月度产品速报](/ai-trends/product-updates/monthly)

## 如果你想

- 私有化部署 → [AI Coding · 企业部署](/ai-coding/enterprise/deployment)
- 对比五大厂商 → [LLM 全景](/llm-landscape/)
- 评估开源模型 → [开源项目推荐](/ai-trends/research-highlights/open-source)
