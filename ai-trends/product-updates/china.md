---
title: 国内厂商动态
description: 阿里 Qwen、DeepSeek、Kimi、GLM 等国内大模型厂商跟踪——开源主线与闭源主线
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-14
verifiedWith:
  sources:
    - name: Qwen 官方
      url: https://qwenlm.github.io
      accessedAt: 2026-08-14
    - name: DeepSeek 官方
      url: https://www.deepseek.com
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

## 一、玩家地图

| 阵营 | 厂商 | 代表模型 | 特点 |
| --- | --- | --- | --- |
| 开源 | 阿里 | Qwen（通义千问） | 开源生态最完整，中英文均衡 |
| 开源 | DeepSeek | V3 / R1 | 训练成本低，推理能力追平闭源 |
| 闭源 | 字节 | 豆包 | 消费端入口 + 低价 API |
| 闭源 | 月之暗面 | Kimi | 长上下文起步早 |
| 闭源 | 智谱 | GLM | 企业服务成熟，学术基因 |
| 闭源 | 百度 | 文心 | 云 + 搜索生态绑定 |
| 闭源 | 腾讯 | 混元 | 微信生态场景 |

## 二、两条主线

**开源线**（Qwen、DeepSeek）：

- 权重可下载，可私有化部署，可控成本
- 适合：企业私有化、数据敏感场景、二次开发
- 部署选型见 [AI Coding · 企业部署](/ai-coding/enterprise/deployment)

**闭源线**（豆包、Kimi、GLM、文心、混元）：

- API 调用，免运维，迭代由厂商推进
- 适合：快速上线、无强数据约束、成本敏感（部分低价）

> **判断框架**：先问「数据能不能出域、要不要私有化」。能出域且团队小 → 闭源 API 最快；要私有化 → 看开源线。

## 三、DeepSeek 现象（2024-12 ~ 2025-01）

- **DeepSeek-V3**（2024-12）：开源模型，训练成本约为同代闭源模型的十分之一量级——「降本」信号
- **DeepSeek-R1**（2025-01）：开源推理模型，效果对标 o1 系列——「推理能力平民化」信号

**影响**：开源与闭源的能力差被大幅压缩；推理成本快速下降；国内 API 价格战加剧。对开发者是红利期——模型成本从「预算大头」变成「可以忽略」。

## 四、如何跟踪

1. **官方源**：[Qwen 官方](https://qwenlm.github.io)、[DeepSeek 官方](https://www.deepseek.com)、各家开放平台文档
2. **社区源**：机器之心、量子位、Hugging Face 趋势榜（开源模型下载量）
3. **关键信号**：开源新版本发布（权重是否开放）、API 价格调整、上下文长度、备案与合规动态

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
