---
title: xAI · Grok 全系
description: Grok 4.6 / Grok 4.20-reasoning——X 生态整合、500K+ 上下文、实时搜索
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-14
verifiedWith:
  sources:
    - name: xAI 模型文档
      url: https://docs.x.ai/developers/models
      accessedAt: 2026-08-14
    - name: xAI 定价
      url: https://docs.x.ai/developers/pricing
      accessedAt: 2026-08-14
---

# xAI · Grok 全系

> 7 家厂商里**与社交平台整合最深（X 生态）+ 实时信息获取最强 + 长上下文激进**。

## 一、公司背景

xAI 由 Elon Musk 于 2023 年创立，总部旧金山湾区。核心差异化是 **X（原 Twitter）生态整合**——Grok 原生接入 X 的实时信息，支持 Web Search / X Search 工具，训练与推理依赖自建 Colossus 超算集群。商业模式：闭源 API + X 订阅（Premium 用户内置 Grok）+ 企业部署。

## 二、模型矩阵（截至 2026-08）

| 模型 | 定位 | 上下文 | 主要场景 |
| --- | --- | --- | --- |
| **Grok 4.6** | 主力（最智能 + 最快） | 500K | 编码 / 通用 / 工具调用 |
| **Grok 4.20-reasoning** | 推理增强 | 1M | 复杂推理 / 多步任务 |
| **Grok 4.3** | 前代 | — | 已由 4.6 / 4.20 取代 |

> **产品线逻辑**：Grok 4.6 是官方推荐的日常主力（docs 明确"For everything else, including code, use Grok 4.6"），4.20-reasoning 走深度推理线，另有音频 / 图像 / 视频专用模型。

## 三、技术架构

**长上下文激进派** —— Grok 4.6 提供 500K 上下文，reasoning 线扩到 1M。与 Kimi / Qwen 一样走「上下文即能力」路线，但 xAI 的差异点是**实时信息**：模型知识截止 2026-02-01，实时数据靠 server-side 搜索工具补足。

**推理模式** —— 4.20 系列支持 reasoning 模式，官方 model card 强调 advanced reasoning + multi-agent 能力（2026-04 发布）。

## 四、核心能力

| 能力 | 描述 |
| --- | --- |
| **Web Search / X Search** | 服务端搜索工具，实时数据补足知识截止 |
| **X 生态整合** | 与 X 平台内容、订阅体系深度绑定 |
| **多模态** | 文本 + 图像输入；音频 / 视频专用模型 |
| **长上下文** | 500K（4.6）/ 1M（reasoning） |

## 五、部署形态

| 部署 | 平台 |
| --- | --- |
| **xAI API** | `docs.x.ai`，标准 REST + 流式 |
| **X 订阅** | Premium / Premium+ 用户内置 Grok |
| **企业** | 私有部署方案（按需） |

## 六、价格（截至 2026-08，官方定价）

| 模型 | Input | Output | 缓存读 |
| --- | --- | --- | --- |
| Grok 4.6（< 200K prompt） | $2 / MTok | $6 / MTok | $0.50 |
| Grok 4.6（≥ 200K prompt） | $4 / MTok | $6 / MTok | — |

**Grok 4.6 定价是 7 家中档水平**——比 Claude / GPT 旗舰便宜，比 Qwen / GLM / MiniMax 贵。Grok 4.20-reasoning 定价以官方 [pricing](https://docs.x.ai/developers/pricing) 为准。

## 七、适合场景 / 不适合场景

**适合**：
- 需要实时 / 社交信息的应用（X 生态强绑定）
- 长上下文 + 编码（500K 档位）
- 深度推理（4.20-reasoning）

**不适合**：
- 中文优先场景（中文生态弱于国内厂商）
- 极致低成本（同档比 MiniMax / GLM 贵一个量级）
- 数据敏感企业（实时搜索会外发上下文）

## 关键洞察

- **实时信息是核心差异化**——X 生态是 Grok 独有护城河
- **长上下文激进**——500K / 1M 档位与 Kimi、Qwen 同一梯队
- **性价比中档**——比闭源旗舰便宜，比国产开源贵

## 参考

- [xAI 模型文档](https://docs.x.ai/developers/models)（访问于 2026-08-14）
- [xAI 定价](https://docs.x.ai/developers/pricing)（访问于 2026-08-14）
- [Grok 4.20 model card](https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf)（访问于 2026-08-14）

## 下一步

- 横向对比 7 家 → [5 厂商横向对比](/reference/model-comparison)
- 按场景选型 → [模型选型决策树](/reference/model-selection-guide)
- 看技术路线 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 如果你想

- 看 Claude 档案 → [Anthropic · Claude 全系](/ai-trends/vendors/anthropic)
- 看 OpenAI 档案 → [OpenAI · GPT 全系](/ai-trends/vendors/openai)
- 看国内厂商 → [国内厂商动态](/ai-trends/product-updates/china)
