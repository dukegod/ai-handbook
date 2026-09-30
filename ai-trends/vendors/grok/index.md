---
title: xAI · Grok 全系
description: Grok 4.7 / Grok 4.20-reasoning——X 生态整合、500K+ 上下文、实时搜索
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: xAI 模型文档
      url: https://docs.x.ai/developers/models
      accessedAt: 2026-09-30
    - name: xAI 定价
      url: https://docs.x.ai/developers/pricing
      accessedAt: 2026-09-30
    - name: xAI release notes
      url: https://docs.x.ai/developers/release-notes
      accessedAt: 2026-09-30
---

# xAI · Grok 全系

> 7 家厂商里**与社交平台整合最深（X 生态）+ 实时信息获取最强 + 长上下文激进**。

## 一、公司背景

xAI 由 Elon Musk 于 2023 年创立，总部旧金山湾区。核心差异化是 **X（原 Twitter）生态整合**——Grok 原生接入 X 的实时信息，支持 Web Search / X Search 工具，训练与推理依赖自建 Colossus 超算集群。商业模式：闭源 API + X 订阅（Premium 用户内置 Grok）+ 企业部署。

## 二、模型矩阵（截至 2026-09）

| 模型 | 定位 | 上下文 | 主要场景 |
| --- | --- | --- | --- |
| **Grok 4.7** | 主力（当前前沿） | 500K | 编码 / Agent 任务 / 知识工作 |
| **Grok 4.6** | 上一代前沿 | 500K | 编码 / 通用 / 工具调用 |
| **Grok 4.20-reasoning** | 推理增强 | 1M | 复杂推理 / 多步任务 |
| **Grok 4.20-non-reasoning** | 推理线非思考版 | 1M | 低延迟 / 不需要思考 |
| **Grok 4.20-multi-agent** | 多 agent 编排 | 1M | 委派型长任务（限流最紧） |
| **Grok 4.5** | 前代 | 500K | 已被 4.6 / 4.7 取代 |
| **Grok 4.3** | 前代 | 1M | 已被 4.6 / 4.20 取代 |
| **Grok Build 0.1**（别名 `grok-code-fast-1`） | 编码专精 | 256K | agentic coding 工作流 |

> **产品线逻辑**：**Grok 4.7 是 2026-09 的前沿主力**（与 4.6 同价、同 500K 上下文），4.20 三兄弟走深度推理 / 多 agent 线（1M 上下文但单价更低），另有图像 / 视频 / 语音专用模型（`grok-imagine-*` / `grok-voice-*`）。4.7 仍**没有文本输出长度上限**。
>
> ⚠️ **版本号容易看错**：4.20 排在 4.7 之后，但它是**不同产品线**（深度推理 / 1M 上下文），不是"更新的 4.7"。日常主力选 4.7，要 1M 上下文 + 深度推理才选 4.20。

## 三、技术架构

**长上下文激进派** —— Grok 4.7 与 4.6 提供 500K 上下文，4.20 线（含 reasoning / non-reasoning / multi-agent）扩到 1M。与 Kimi / Qwen 一样走「上下文即能力」路线，但 xAI 的差异点是**实时信息**：静态知识之外，靠 server-side 搜索工具补足。（具体知识截止日期以官方模型页为准，本轮未逐个复核。）

**推理模式** —— 4.7 / 4.6 / 4.5 支持 `reasoning_effort` 四档（`low` / `medium` / `high` / `xhigh`，默认 `high`），4.20 线提供 thinking / non-thinking / multi-agent 三个显式变体。4.20 与 4.20 multi-agent 于 2026-03 上线。

**成本可观测性** —— 每个 API 响应的 `usage` 里带 `cost_in_usd_ticks`，能直接拿到本次请求花了多少钱。

## 四、核心能力

| 能力 | 描述 |
| --- | --- |
| **Web Search / X Search** | 服务端搜索工具，实时数据补足知识截止；Web $5 / 1k 次，X 按 post / profile 计费 |
| **X 生态整合** | 与 X 平台内容、订阅体系深度绑定 |
| **多模态** | 文本 + 图像输入；图像 / 视频 / 语音各有专用模型 |
| **长上下文** | 500K（4.7 / 4.6）/ 1M（4.20 线） |
| **Remote MCP** | 连接自建 MCP 工具服务器，按 token 计费 |
| **Context Compaction** | 长会话压缩成更短上下文，降低长 agent 循环成本 |
| **safety_identifier** | 把策略违规归因到终端用户而非 API key（2026-09 新增） |

**工具调用的账要单独算**——xAI 的服务端工具是"token 费用 + 工具调用费"两段计费，而 agent 自主决定调用几次，**成本随查询复杂度放大**。X Search 尤其要留意：它按**取回的条目数**计费（每条 post、每个 profile 都算），不是按调用次数。

## 五、部署形态

| 部署 | 平台 |
| --- | --- |
| **xAI API** | `docs.x.ai`，标准 REST + 流式 |
| **X 订阅** | Premium / Premium+ 用户内置 Grok |
| **Grok Build** | 独立编码 CLI / TUI（2026-05 进 beta），与 Claude Code 同类定位 |
| **Grok Bot** | 常驻云端电脑的 agent 队友（2026-08 上线），带消息、审批、连接器、routines |
| **区域端点** | `api.x.ai`（全球）/ `us.api.x.ai`（美国，1.1x）/ `eu-west-1` 集群 |
| **企业** | 私有部署方案（按需） |

**xAI 现在有三条产品面**——API 给开发者，**Grok Build** 对标 Claude Code 打编码工作流，**Grok Bot** 做常驻型 agent。这三条是 2026 年新增的，"xAI 只是聊天 API 厂商"的印象已经过时。

## 六、价格（截至 2026-09，官方定价）

短上下文 = prompt < 200K；长上下文 = prompt ≥ 200K（达阈值后**整个请求**按高档计费）。

| 模型 | 上下文 | Input | 缓存读 | Output |
| --- | --- | --- | --- | --- |
| Grok 4.7（< 200K prompt） | 500K | $2.00 / MTok | $0.50 | $6.00 / MTok |
| Grok 4.7（≥ 200K prompt） | 500K | $4.00 / MTok | $1.00 | $12.00 / MTok |
| Grok 4.6（< 200K prompt） | 500K | $2.00 / MTok | $0.50 | $6.00 / MTok |
| Grok 4.6（≥ 200K prompt） | 500K | $4.00 / MTok | $1.00 | $12.00 / MTok |
| Grok 4.20-reasoning（< 200K prompt） | 1M | $1.25 / MTok | $0.20 | $2.50 / MTok |
| Grok 4.20-reasoning（≥ 200K prompt） | 1M | $2.50 / MTok | $0.40 | $5.00 / MTok |
| Grok 4.5（< 200K prompt） | 500K | $2.00 / MTok | $0.30 | $6.00 / MTok |
| Grok Build 0.1（< 200K prompt） | 256K | $1.00 / MTok | $0.20 | $2.00 / MTok |

**两个反直觉点**：

- **1M 上下文反而更便宜**——4.20 线（1M）单价只有 4.7（500K）的 6 折。要长上下文 + 省钱，4.20 比 4.7 更划算。
- **4.7 和 4.6 同价**——新旗舰没涨价，升级是纯能力收益。

**其他计价维度**：Batch API 对 4.3 / 4.20 三个变体给 8 折（4.7 / 4.6 / 4.5 **无折扣**）；Priority Processing 为 2x；**美国区域端点 `us.api.x.ai` 为 1.1x**（Grok 4.7 因此是 $2.20 / $0.55 / $6.60）。图像 $0.02–$0.05 / 张，视频 $0.05–$0.08 / 秒。

**Grok 4.7 Fast 不在公共 API 上**——它是同一个 4.7 模型跑更快的基础设施，价格 2x（长上下文档 1.5x），**仅在 Cursor 与 Grok Build 内可用**，通过那边的套餐计费。

## 七、适合场景 / 不适合场景

**适合**：
- 需要实时 / 社交信息的应用（X 生态强绑定）
- 长上下文 + 编码（500K 档位，或 4.20 线的 1M）
- 深度推理（4.20-reasoning / multi-agent）
- 想要常驻型 agent（Grok Bot）或独立编码 CLI（Grok Build）

**不适合**：
- 中文优先场景（中文生态弱于国内厂商）
- 极致低成本（同档比 MiniMax / GLM 贵一个量级）
- 数据敏感企业（实时搜索会外发上下文）
- 严格预算控制（工具按条目计费，agent 自主决定调用次数）

## 八、最新动态（2026-09）

**三条跟踪线**：

- **模型线**：Grok 4.x 旗舰的迭代。核心看「哪个版本是当前主力、上下文与定价怎么变」
- **工具线**：Grok Build（编码 CLI）、Grok Bot（常驻 agent）、Imagine（图像 / 视频）。这条线 2026 年变化最大
- **生态线**：X 平台整合与服务端工具计费规则。X Search 按条目计费这一条直接影响成本模型

**本轮核实的 2026-08 / 09 事件**（均见 [xAI release notes](https://docs.x.ai/developers/release-notes)）：

| 时间 | 事件 | 影响 |
| --- | --- | --- |
| 2026-09 | **Grok 4.7 上线** | 500K 上下文，$2 / $0.50 / $6，无输出长度上限 |
| 2026-09 | `safety_identifier` 请求字段 | 违规可归因到终端用户而非 API key |
| 2026-09 | Grok Voice Transcribe 2.0 可用 | 语音转写换代 |
| 2026-09 | 公告 `grok-imagine-image-quality` 将于 2026-11-02 退役 | 请求会转由 `grok-imagine-image-2.0`（`quality=low`）承接，价格更低 |
| 2026-08 | 图像 API 更新 | `quality` 支持 `auto` 且成为默认；多图编辑 3 → **5** 张；新增 21:9 与 5:2 比例 |
| 2026-08 | **Grok 4.6 上线** | 500K 上下文，与 4.7 同价 |
| 2026-08 | **Grok Bot 上线** | 常驻云端电脑的 agent 队友，带审批与连接器 |

> ⚠️ **版本号是最容易出错的地方**：`Grok 4.20` 排在 `Grok 4.7` 之后，但**版本号不代表新旧**——4.20 是 2026-03 上线的深度推理产品线，与 4.x 旗舰不是同一条线。官方 release notes 里 4.7 和 4.6 都写作 "frontier model for coding, agentic tasks, and knowledge work"。

**如何跟踪**：

1. **官方源**：[xAI release notes](https://docs.x.ai/developers/release-notes)（开发者侧最准）、[模型文档](https://docs.x.ai/developers/models)、[定价](https://docs.x.ai/developers/pricing)、[Grok Build 文档](https://docs.x.ai/build/overview)
2. **更新节奏**：旗舰模型 2026 年基本月更（4.5 → 4.6 → 4.7），工具线（Build / Bot / Imagine）变化更频繁
3. **判断原则**：模型更新看「上下文 / 定价 / 是否退役」；工具更新看「是否影响成本模型」——xAI 的工具是按调用条目计费的，能力增强往往同时抬高账单

> 📌 一个观察项：xAI 文档站现以 **SpaceXAI** 名义发布，自述为 "Official SpaceXAI (xAI) developer documentation"（见 [llms.txt](https://docs.x.ai/llms.txt)）。API 域名与 slug 仍是 `api.x.ai` / `grok-*`，但品牌表述已变，引用文档时注意区分。

## 关键洞察

- **实时信息是核心差异化**——X 生态是 Grok 独有护城河
- **长上下文激进**——500K / 1M 档位与 Kimi、Qwen 同一梯队
- **1M 上下文更便宜**——4.20 线单价低于 4.7 旗舰，长文档场景是隐藏优选
- **工具按条目计费**——X Search 等工具的成本随 agent 自主调用次数放大，预算模型要单独建
- **产品面从 API 扩到 CLI 与 agent**——Grok Build + Grok Bot 让 xAI 直接参与编码与常驻 agent 竞争

## 参考

- [xAI 模型文档](https://docs.x.ai/developers/models)（访问于 2026-09-30）
- [xAI 定价](https://docs.x.ai/developers/pricing)（访问于 2026-09-30）
- [xAI release notes](https://docs.x.ai/developers/release-notes)（访问于 2026-09-30）
- [Grok 4.7 发布公告](https://x.ai/news/grok-4-7)
- [Grok 4.20 model card](https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf)

## 下一步

- 横向对比 7 家 → [7 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 按场景选型 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)
- 看技术路线 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 如果你想

- 看 Claude 档案 → [Anthropic · Claude 全系](/ai-trends/vendors/anthropic/)
- 看 OpenAI 档案 → [OpenAI · GPT 全系](/ai-trends/vendors/openai/)
- 看国内厂商 → [国内厂商](/ai-trends/cn-vendors/)
