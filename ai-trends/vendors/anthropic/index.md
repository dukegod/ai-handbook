---
title: Anthropic · Claude 全系
description: Opus 5.5 / Sonnet 5.5 / Haiku 4.5 / Fable 5.1——技术架构、Constitutional AI 训练、能力与部署
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: Anthropic 模型总览
      url: https://platform.claude.com/docs/en/about-claude/models/overview
      accessedAt: 2026-09-30
    - name: Claude 定价文档
      url: https://platform.claude.com/docs/en/about-claude/pricing
      accessedAt: 2026-09-30
    - name: Claude Platform release notes
      url: https://platform.claude.com/docs/en/release-notes/overview
      accessedAt: 2026-09-30
---

# Anthropic · Claude 全系

> 7 家厂商里**最坚持 dense 架构** + 唯一公开推 RLAIF 训练方法 + 把 Agent / Computer Use 当一等公民。

## 一、公司背景

Anthropic 是 2021 年由前 OpenAI 核心成员 Dario Amodei 与 Daniela Amodei 兄妹创办的 AI 安全公司，总部旧金山。核心定位是**"安全 + 可解释 + 可控"**——研发路径上不卷规模上限，专注**可调度的工程化 AI**。商业模式 100% 闭源、按 token 计费 API + 订阅制产品（Claude.ai）+ Claude Code 终端 + 企业部署（AWS Bedrock / GCP Vertex）。

## 二、模型矩阵（截至 2026-09）

| 模型 | 定位 | 上下文 | 思考模式 | 发布 | 主要场景 |
| --- | --- | --- | --- | --- | --- |
| **Fable 5.1** | 长 Agent 专精 | 1M | adaptive thinking（始终开启） | 2026-09-01 | 长任务 / 长 Agent / 大仓库 |
| **Opus 5.5** | 旗舰推理 | 1M | adaptive thinking（始终开启） | 2026-09-22 | 复杂推理 / 编码 / Agent |
| **Sonnet 5.5** | 主力 | 1M | adaptive thinking | 2026-09-28 | 编码 / 通用对话 / 工具调用 |
| **Haiku 4.5** | 轻量 | 200K | extended thinking | 2025-10-15 | 高并发 / 实时 / 成本敏感 |
| **Mythos 5.1** | 安全专精 | 1M | — | 2026-09-01 | 网络安全 / 生物（limited availability） |

> **产品线逻辑**：4 个主流型号覆盖"质量/速度/成本"三角 + Fable 5.1 是"长 Agent"专属赛道，**Fable 5.1 不是 Opus 的替代**，是补位。官方选型指引是：绝大多数负载从 **Opus 5.5** 起步；当 Opus 5.5 提高 effort 后仍不够，再上 **Fable 5.1**。Mythos 5.1 未 GA，仅限 Project Glasswing 邀请制。

> ⚠️ **2026-09 换代提醒**：Opus 5 / Sonnet 5 / Fable 5 已全部退居 legacy 档（仍可调用），主力位由 5.5 / 5.1 系列接替。Haiku 4.5 是**当前唯一未换代的型号**。

## 三、技术架构

**dense 模型路径**（推测）—— 在 7 家厂商里 Anthropic 是少数仍坚持 dense 的（其他多数厂商走 MoE）。代价是训练成本更高、参数总量受限；收益是**推理行为更稳定、不需要路由调优**。

**Constitutional AI（RLAIF）** —— Anthropic 主推的训练方法：用 AI 而非人类做偏好标注，先用"宪法"原则（helpful / harmless / honest）让模型自评，再用 RLAIF 训练。**核心差异**：和 OpenAI 的 RLHF / DeepSeek 的 GRPO 路线不同，Constitutional AI 把"价值观"显式编码进训练流程——更适合做安全可控的助手。

**长上下文实现** —— Fable 5.1 / Opus 5.5 / Sonnet 5.5 均为 1M 上下文（官方默认），Haiku 4.5 为 200K。1M 上下文在 4.6 及之后的模型上**按标准价计费**（官方举例：90 万 token 的请求与 9 千 token 的请求单价相同）。具体位置编码方案未公开；官方唯一披露的工程细节是**分词器换代**——Claude 4.7 及之后的模型与 Mythos Preview 换用新分词器，同样文本约多出 30% token（Sonnet 4.6 及更早沿用旧分词器）。

## 四、核心能力

| 能力 | 描述 | 落地 |
| --- | --- | --- |
| **Tool Use** | 函数调用 / JSON Schema 校验 | Messages API 原生 |
| **Prompt Caching** | 5 分钟 + 1 小时双档缓存 | 读 0.1x（Fable 5.1 / Mythos 5.1 为 0.025x、Opus 5.5 为 0.05x） |
| **Computer Use** | 截图 + 操作 GUI（鼠标键盘） | `computer_toolset_20260801` 已 GA（2026-08-19） |
| **Browser Use** | 应用自托管浏览器内驱动 | `browser_toolset_20260801`（2026-08-19 新增） |
| **Agent SDK** | 多 agent 编排 / Subagent 派生 | Claude Code / SDK 同源 |
| **Files API** | 客户端文件直传 | 已 GA（2026-08-19） |
| **Agent Skills** | Skills 打包进容器 | Skills API 已 GA（2026-08-19） |
| **Managed Agents** | 托管会话 + 预算 / 审批 / 记忆 | $0.08 / 会话小时 |
| **Message Batches** | 24h 异步批处理（50% 折扣） | Messages API |

**Agent 能力是 Anthropic 的核心壁垒**——Computer Use 让你"操作电脑"，Browser Use 让你"操作浏览器"，Agent SDK 让你"派生 subagent"，组合起来能做**长任务自动化**（hooks + skills + subagents 那一整套就是这套能力的工程化封装）。

## 五、部署形态

| 部署 | 平台 | 适合 |
| --- | --- | --- |
| **Claude API** | `platform.claude.com` | 直接 API 调用 |
| **Claude Code** | CLI / VS Code / JetBrains | 本地 CLI 工作流 |
| **AWS Bedrock** | `aws.amazon.com/bedrock` | AWS 集成 / 私有化 |
| **GCP Vertex AI** | `cloud.google.com/vertex-ai` | GCP 集成 / 私有化 |
| **Claude Platform on AWS** | AWS Marketplace（CCU 计费） | Anthropic 官方运维 + AWS 采购 |
| **Claude in Microsoft Foundry** | Azure Marketplace（CCU 计费） | Azure 企业采购路径 |
| **Claude.ai** | Web/Desktop/Mobile | 终端用户产品 |

**云厂商是企业部署的多条腿**——大客户不直接接 Anthropic，走云厂商 marketplace 计费 + 私有 VPC。两条计费口径要分清：**Bedrock / Vertex 是云厂商自己开票**；**Claude Platform on AWS / Claude in Microsoft Foundry 是 Anthropic 定价后折算成 CCU（$0.01 / CCU）由云厂商转收**。

## 六、价格（截至 2026-09，官方定价）

| 模型 | Input | Output | 缓存读 | 备注 |
| --- | --- | --- | --- | --- |
| Haiku 4.5 | $1 / MTok | $5 / MTok | $0.10 / MTok | 轻量档；2026-10-15 起最早退役 |
| Sonnet 5.5 | $2 / MTok | $10 / MTok | $0.20 / MTok | 速度与智能的最佳组合 |
| Opus 5.5 | $4 / MTok | $20 / MTok | $0.20 / MTok | 比 Opus 5 降 20% |
| Fable 5.1 | $10 / MTok | $50 / MTok | $0.25 / MTok | 全系最贵；缓存读 0.025x |
| Mythos 5.1 | $10 / MTok | $50 / MTok | $0.25 / MTok | limited availability（Project Glasswing） |

**价格梯度**：Haiku 4.5 < Sonnet 5.5 < Opus 5.5 < Fable 5.1 = Mythos 5.1。**Fable 5.1 是全系最贵**（是 Opus 5.5 的 2.5 倍价），定位"长 Agent 专家"；Opus 5.5 是"性价比旗舰"。

**缓存折扣已不再统一**——读取命中价按模型分档：一般模型 0.1x、Opus 5.5 为 0.05x、Fable 5.1 与 Mythos 5.1 为 **0.025x**（读一次只要基准 input 的 2.5%）。写入侧是 5 分钟档 1.25x、1 小时档 2x。**长 prompt + 多轮对话场景必开缓存**（具体折扣以官方定价页为准）。

**其他计价维度**：Batch API 一律 5 折；`inference_geo: "us"` 数据驻留为 1.1x；Fast mode（research preview）Opus 5.5 为 $8 / $40、Opus 5 与 Opus 4.8 为 $10 / $50，且不与 Batch 叠加。

## 七、适合场景 / 不适合场景

**适合**：
- 编码 + 工具调用（Sonnet 5.5 + Tool Use 是业界标杆）
- 长文档处理（1M 默认 + Fable 5.1 1M）
- Agent 任务（Computer Use + Browser Use + Agent SDK + Subagent 组合）
- 重视安全可控（Constitutional AI 路线）

**不适合**：
- 超低成本场景（Haiku 4.5 仍比 Qwen / GLM 同尺寸贵）
- 国内合规（需走 Bedrock / Vertex 等海外渠道，或等国内合作）
- 极简单轮问答（杀鸡用牛刀，Haiku 也贵）

## 八、最新动态（2026-09）

**三条跟踪线**：

- **模型线**：Claude 家族发布与定价。核心看「哪个模型在哪个价位，能力定位是什么」
- **工具线**：Claude Code（CLI）、Claude Agent SDK、Claude.ai 产品功能。对开发者，这条线比模型线更常变化
- **协议线**：MCP（Model Context Protocol）的演进。MCP 已开源为开放标准，生态变化影响所有工具

**本轮核实的 2026-09 事件**（均见 [Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview)）：

| 日期 | 事件 | 影响 |
| --- | --- | --- |
| 2026-09-28 | 发布 **Claude Sonnet 5.5**（`claude-sonnet-5-5`），$2 / $10 | 主力位换代；`thinking: "disabled"` 失效，强制 `tool_choice` 返回 400 |
| 2026-09-22 | 发布 **Claude Opus 5.5**（`claude-opus-5-5`），$4 / $20 | 旗舰降价 20%；思考不可关闭，深度改由 `effort` 控制（默认 `medium`） |
| 2026-09-22 | Fast mode（research preview）开放给 Opus 5.5 | $8 / $40 |
| 2026-09-14 | 会话按需压缩（compaction on demand）进 beta | 长会话可主动折叠，保留近期轮次原文 |
| 2026-09-10 | `ant` CLI 1.32.0 可直连 Managed Agents 会话 | 终端里审批 / 跟踪 agent |
| 2026-09-01 | 发布 **Fable 5.1** + **Mythos 5.1** | 缓存读砍到 0.025x（$0.25 / MTok）；Fable 5.1 文本带水印，且强制 30 天数据留存 |
| 2026-08-19 | Computer Use 转正、新增 Browser Use、Files API / Skills 转正 | 一批 beta header 可以摘掉了 |
| 2026-08-10 | Sonnet 5 的 $2 / $10 转正价，原定 9-01 涨到 $3 / $15 **不执行** | 主力价长期锁定 |

> ⚠️ **2026-09 最值得注意的迁移风险**：新一代 5.5 / 5.1 都是**思考不可关闭**的，`thinking: {"type": "disabled"}` 与 `"enabled"` 一律返回 400，`tool_choice` 的 `any` / `tool` 也返回 400。从 Opus 5 / Sonnet 5 升上来的代码需要按迁移指南改写。

**如何跟踪**：

1. **官方源**：[Anthropic News](https://www.anthropic.com/news)、[Claude 模型总览](https://platform.claude.com/docs/en/about-claude/models/overview)、[Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview)、[Claude Code docs](https://code.claude.com/docs)
2. **更新节奏**：模型大版本约半年一更，但 2026-09 一个月内连发三个（5.1 / 5.5 / 5.5）——换代节奏在加快；Claude Code 几乎每周迭代
3. **判断原则**：模型更新看「价格 / 能力 / 上下文」三要素；工具更新看「对现有工作流的破坏性」——破坏性变更（如思考不可关闭）优先跟进

## 关键洞察

- **dense 路径在 2026 是少数派**——但 Anthropic 靠"行为稳定 + 安全可控"差异化
- **Agent 是核心壁垒**——Computer Use / Browser Use / Agent SDK / Skills / Hooks 是别的厂商没整合好的
- **缓存折扣是价格利器**——长 prompt 场景必开，且新一代把读取打到 0.025x
- **Fable 5.1 是补位不是替代**——专门做"长 Agent"赛道；Opus 5.5 是性价比首选
- **换代在加速，破坏性变更在变多**——2026-09 一个月发三个型号，思考不可关闭是新的迁移门槛

## 参考

- [Anthropic 平台文档](https://platform.claude.com/docs/en/intro)
- [Claude 定价](https://platform.claude.com/docs/en/about-claude/pricing)
- [Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview)（访问于 2026-09-30）
- [Claude 产品总览](https://claude.com/product/overview)
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- [Claude 模型 · claude-capabilities](/claude-capabilities/models/overview)
- [Claude Code 精通](/claude-code/)
- [architecture review](/contributing/architecture-review-2026-08-10)

## 下一步

- 看 OpenAI 路线对比 → [OpenAI · GPT 全系](../openai/)
- 看技术架构对比 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)

## 如果你想

- 选模型 → [模型选择](/claude-code/basics/model-selection)
- 了解 Fable 5 → [Fable 5 深度解读](/claude-capabilities/models/fable)
- 对比七家厂商 → [7 厂商横向对比](/ai-trends/model-selection/model-comparison)
