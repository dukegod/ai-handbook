---
title: Anthropic · Claude 全系
description: Opus 5 / Sonnet 5 / Haiku 4.5 / Fable 5——技术架构、Constitutional AI 训练、能力与部署
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-11
verifiedWith:
  sources:
    - name: Anthropic 模型总览
      url: https://platform.claude.com/docs/en/about-claude/models/overview
      accessedAt: 2026-08-14
    - name: Claude 定价文档
      url: https://platform.claude.com/docs/en/about-claude/pricing
      accessedAt: 2026-08-14
    - name: Opus 5 发布博客
      url: https://www.anthropic.com/news/claude-opus-5
      accessedAt: 2026-08-14
---

# Anthropic · Claude 全系

> 7 家厂商里**最坚持 dense 架构** + 唯一公开推 RLAIF 训练方法 + 把 Agent / Computer Use 当一等公民。

## 一、公司背景

Anthropic 是 2021 年由前 OpenAI 核心成员 Dario Amodei 与 Daniela Amodei 兄妹创办的 AI 安全公司，总部旧金山。核心定位是**"安全 + 可解释 + 可控"**——研发路径上不卷规模上限，专注**可调度的工程化 AI**。商业模式 100% 闭源、按 token 计费 API + 订阅制产品（Claude.ai）+ Claude Code 终端 + 企业部署（AWS Bedrock / GCP Vertex）。

## 二、模型矩阵（截至 2026-08）

| 模型 | 定位 | 上下文 | 思考模式 | 主要场景 |
| --- | --- | --- | --- | --- |
| **Opus 5** | 旗舰推理 | 1M | adaptive thinking | 复杂推理 / 编码 / Agent |
| **Sonnet 5** | 主力 | 1M | adaptive thinking | 编码 / 通用对话 / 工具调用 |
| **Haiku 4.5** | 轻量 | 200K | 快速 | 高并发 / 实时 / 成本敏感 |
| **Fable 5** | 长 Agent 专精 | 1M | adaptive thinking（强制） | 长任务 / 长 Agent / 大仓库 |
| **Mythos 5** | 安全专精 | 1M | — | 网络安全 / 生物（limited availability） |

> **产品线逻辑**：4 个主流型号覆盖“质量/速度/成本”三角 + Fable 5 是“长 Agent”专属赛道，**Fable 5 不是 Opus 的替代**，是补位；Mythos 5 未 GA，仅限安全与基础设施供应商。

## 三、技术架构

**dense 模型路径**（推测）—— 在 7 家厂商里 Anthropic 是少数仍坚持 dense 的（其他多数厂商走 MoE）。代价是训练成本更高、参数总量受限；收益是**推理行为更稳定、不需要路由调优**。

**Constitutional AI（RLAIF）** —— Anthropic 主推的训练方法：用 AI 而非人类做偏好标注，先用"宪法"原则（helpful / harmless / honest）让模型自评，再用 RLAIF 训练。**核心差异**：和 OpenAI 的 RLHF / DeepSeek 的 GRPO 路线不同，Constitutional AI 把"价值观"显式编码进训练流程——更适合做安全可控的助手。

**长上下文实现** —— Opus 5 / Sonnet 5 / Fable 5 均为 1M 上下文（官方默认），Haiku 4.5 为 200K。技术细节未完全公开，1M 的“needle in haystack”检索准确率领先业界。底层用 RoPE 位置插值 + 滑动窗口混合。

## 四、核心能力

| 能力 | 描述 | 落地 |
| --- | --- | --- |
| **Tool Use** | 函数调用 / JSON Schema 校验 | Messages API 原生 |
| **Prompt Caching** | 5 分钟缓存（命中后 90% 折扣） | 1.4x 写入 / 0.1x 读取 |
| **Computer Use** | 截图 + 操作 GUI（鼠标键盘） | Beta API / Claude Code 内置 |
| **Agent SDK** | 多 agent 编排 / Subagent 派生 | Claude Code / SDK 同源 |
| **Files API** | 客户端文件直传 | 替代 base64 上传 |
| **Message Batches** | 24h 异步批处理（50% 折扣） | Messages API |

**Agent 能力是 Anthropic 的核心壁垒**——Computer Use 让你"操作电脑"，Agent SDK 让你"派生 subagent"，组合起来能做**长任务自动化**（v0.3.1 hooks + skills + subagents 那一整套就是这套能力的工程化封装）。

## 五、部署形态

| 部署 | 平台 | 适合 |
| --- | --- | --- |
| **Claude API** | `platform.claude.com` | 直接 API 调用 |
| **Claude Code** | CLI / VS Code / JetBrains | 本地 CLI 工作流 |
| **AWS Bedrock** | `aws.amazon.com/bedrock` | AWS 集成 / 私有化 |
| **GCP Vertex AI** | `cloud.google.com/vertex-ai` | GCP 集成 / 私有化 |
| **Claude.ai** | Web/Desktop/Mobile | 终端用户产品 |

**Bedrock + Vertex 是企业部署两条腿**——大客户不直接接 Anthropic，走云厂商 marketplace 计费 + 私有 VPC。

## 六、价格（截至 2026-08，官方定价）

| 模型 | Input | Output | 缓存读 | 备注 |
| --- | --- | --- | --- | --- |
| Opus 5 | $5 / MTok | $25 / MTok | $0.50 / MTok | 接近 Fable 5 智能，半价 |
| Sonnet 5 | $2 / MTok | $10 / MTok | $0.20 / MTok | 2026-08 起保持 intro 价为标准价 |
| Haiku 4.5 | $1 / MTok | $5 / MTok | $0.10 / MTok | 轻量档 |
| Fable 5 | $10 / MTok | $50 / MTok | $1 / MTok | 全系最贵 |
| Mythos 5 | $10 / MTok | $50 / MTok | $1 / MTok | limited availability |

**价格梯度**：Haiku 4.5 < Sonnet 5 < Opus 5 < Fable 5 = Mythos 5。**Fable 5 是全系最贵**（是 Opus 5 的两倍价），定位“长 Agent 专家”；Opus 5 是“接近 Fable 智能的半价平替”。

**Prompt Caching 是 Anthropic 的差异化**——缓存写入 1.25x、读取 0.1x，长 prompt + 多轮对话场景可省可观成本（具体折扣以官方定价页为准）。

## 七、适合场景 / 不适合场景

**适合**：
- 编码 + 工具调用（Sonnet 5 + Tool Use 是业界标杆）
- 长文档处理（1M 默认 + Fable 5 1M）
- Agent 任务（Computer Use + Agent SDK + Subagent 组合）
- 重视安全可控（Constitutional AI 路线）

**不适合**：
- 超低成本场景（Haiku 4.5 仍比 Qwen / GLM 同尺寸贵）
- 国内合规（需走 Bedrock / Vertex 海外，或等国内合作）
- 极简单轮问答（杀鸡用牛刀，Haiku 也贵）

## 关键洞察

- **dense 路径在 2026 是少数派**——但 Anthropic 靠“行为稳定 + 安全可控”差异化
- **Agent 是核心壁垒**——Computer Use / Agent SDK / Skills / Hooks 是别的厂商没整合好的
- **Prompt Caching 是价格利器**——长 prompt 场景必开
- **Fable 5 是补位不是替代**——专门做“长 Agent”赛道；Opus 5 是性价比首选

## 参考

- [Anthropic 平台文档](https://platform.claude.com/docs/en/intro)
- [Claude 定价](https://platform.claude.com/docs/en/about-claude/pricing)
- [Claude 产品总览](https://claude.com/product/overview)
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- [Claude 模型 · claude-capabilities](/claude-capabilities/models/overview)
- [Claude Code 精通](/claude-code/)
- [architecture review](/contributing/architecture-review-2026-08-10)

## 下一步

- 看 OpenAI 路线对比 → [OpenAI · GPT 全系](./openai)
- 看技术架构对比 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- 选型决策 → [模型选型决策树](/reference/model-selection-guide)
