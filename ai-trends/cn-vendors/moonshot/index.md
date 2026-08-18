---
title: Moonshot · Kimi 全系
description: Kimi K3 / K2.5 / K2——MoE 架构、1M 长上下文、中文长文档分析
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: Kimi K3 官方定价
      url: https://platform.kimi.ai/docs/pricing/chat-k3
      accessedAt: 2026-08-14
    - name: Kimi K3 官方文档
      url: https://platform.kimi.ai/docs/guide/kimi-k3-quickstart
      accessedAt: 2026-08-14
---

# Moonshot · Kimi 全系

> 7 家厂商里**长上下文最激进（2M）+ MoE 专家数最多（384）+ 中文长文档分析标杆**。

## 一、公司背景

Moonshot AI（月之暗面）2023 年由清华系创业者杨植麟创办，总部北京。核心定位是**"长上下文 + 中文场景"**——从 128K 起步，一路扩到 2M token，是中文用户处理长文档/长视频的首选。商业模式：Kimi Web/App 免费 + API 付费 + 企业定制。

## 二、模型矩阵

| 模型 | 定位 | 上下文 | 思考模式 | 主要场景 |
|------|------|--------|----------|----------|
| **Kimi K3** | 旗舰 | 1M | 总是推理（reasoning_effort） | 长时编码 / 知识工作 |
| **Kimi K2.5** | 上一代 | 256K | 原生多模态 agentic | 视觉 + 文本 agent |
| **Kimi K2** | 历史 | 1M | — | 已由 K2.5 / K3 取代 |

> **产品线逻辑**：K3 做旗舰（2026-07 发布、7-27 开源，2.8T 参数）、K2.5 做多模态 agent、K2 已退居历史。

## 三、技术架构

**MoE 架构** —— K2 系列以 384 专家（激活 8）的激进 MoE 设计著称，路由用 shared expert + routed expert 双轨。K3 旗舰的具体架构参数未公开，但延续长上下文 + 编码专精路线。

**2M 长上下文（历史）** —— K2-0905 曾扩到 2M token，当时是 7 家厂商中最长。技术用 LongRoPE 风格的位置插值。**当前旗舰 K3 为 1M**——中文长文档分析仍是 Kimi 的核心场景。

**K2 Thinking（RLVR）** —— 和 OpenAI o-series 同路线：用可验证奖励（数学答案对错、代码单测通过率）训练推理能力。**K2 Thinking 在中文数学/代码基准上追平 o1**。

## 四、核心能力

| 能力 | 描述 | 落地 |
|------|------|------|
| **Tool Use** | 函数调用 / JSON Schema | Kimi API |
| **Deep Research** | 多步搜索 + 长文档分析 | Kimi Web 内置 |
| **文件解析** | PDF / Word / PPT 直接解析 | Kimi Web + API |
| **多模态** | 图片理解 + OCR | K2 原生 |
| **长视频** | 视频理解（历史 2M 上下文） | K2-0905（已被 K3 取代） |

**文件解析是 Kimi 差异化** —— 直接上传 PDF/Office 文件，Kimi 解析后在 1M context 内分析。Claude 需要先用 Files API 上传，GPT 需要 Code Interpreter。

## 五、部署形态

| 部署 | 平台 | 适合 |
|------|------|------|
| **Kimi API** | `platform.moonshot.cn` | 直接 API 调用 |
| **Kimi Web/App** | 网页 / 移动端 | 终端用户产品 |
| **K2 权重** | 部分开源 | 私有部署 / 微调 |

**K2 部分开源（历史）** —— K2 基础权重已开源（Apache 2.0），但 K2 Thinking 和 K2-0905 仍闭源。**K3 已开源（2026-07-27）**，是月之暗面最新开源旗舰。

## 六、价格（截至 2026-08，官方定价）

| 模型 | Input | Output | 缓存命中 | 备注 |
|------|-------|--------|---------|------|
| Kimi K3 | $3 / MTok | $15 / MTok | $0.30 | 旗舰，1M 上下文 |

**Kimi K3 官方定价（2026-07 发布）** —— 1M context、自动上下文缓存、ToolCall / JSON Mode / 结构化输出原生支持。

## 七、适合场景 / 不适合场景

**适合**：
- 长文档分析（PDF / 合同 / 论文，1M-2M 上下文）
- 中文场景（中文基准领先，中文文件解析原生支持）
- 办公自动化（Deep Research + 文件解析组合）
- 中文数学/代码推理（K2 Thinking）

**不适合**：
- 英文为主的场景（Claude / GPT 英文更强）
- 极低成本场景（K2 价格比 Qwen / GLM 贵 2-3x）
- 海外部署（Kimi API 主要面向国内）

## 关键洞察

- **2M 上下文是核心壁垒** —— 处理超长文档/视频，Kimi 是唯一选择
- **MoE 384 专家是最激进设计** —— 推理效率高，但路由调优难度大
- **文件解析是差异化** —— 直接上传 Office/PDF，无需预处理
- **中文长文档是护城河** —— 中文 OCR + 长上下文 + 文件解析的组合，Claude/GPT 都不如

## 参考

- [Kimi 开放平台](https://platform.moonshot.cn/docs)
- [Kimi K2 技术报告](https://moonshotai.github.io/Kimi-K2/)
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- [Anthropic Claude 对比](/ai-trends/vendors/anthropic/)

## 下一步

- 看国内另一家路线 → [Zhipu · 智谱 GLM 全系](../zhipu/)
- 看横向对比表 → [5 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)
