---
title: OpenAI · GPT 全系
description: GPT-5.6 系列（Sol / Terra / Luna / Cyber）——技术架构、推理模型路线、部署与价格
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-14
verifiedWith:
  sources:
    - name: OpenAI 官方定价
      url: https://developers.openai.com/api/docs/pricing
      accessedAt: 2026-08-14
    - name: GPT-5.6 Sol 模型页
      url: https://developers.openai.com/api/docs/models/gpt-5.6-sol
      accessedAt: 2026-08-14
---

# OpenAI · GPT 全系

> 7 家厂商里**最早商业化 + 最激进推理模型路线（o-series）+ 2026 年首次开源（GPT-OSS）**。

## 一、公司背景

OpenAI 2015 年成立，从非营利转型为"利润上限"结构。核心投资方 Microsoft（累计 $130 亿+）。商业模式：闭源 API + ChatGPT 订阅 + Azure OpenAI 企业部署。2026 年首次开源 GPT-OSS 20B/120B，标志策略转向。

## 二、模型矩阵（截至 2026-08）

| 模型 | 定位 | 价格（input / output） | 主要场景 |
|------|------|--------|----------|
| **GPT-5.6 Sol** | 旗舰推理 | $5 / $30 | 编码 / 研究 / 科学 / 网络安全 |
| **GPT-5.6 Terra** | 主力 | $2 / $12 | 通用对话 / 工具调用 |
| **GPT-5.6 Luna** | 轻量 | $0.20 / $1.20 | 高并发 / 成本敏感 |
| **GPT-5.6 Cyber** | 安全专精（Daybreak） | $12.50 / $75 | 网络安全（受限场景） |
| **o 系列（o1 / o3 → o4-mini）** | 推理模型线 | 视型号而定 | 数学 / 代码 / 逻辑 |

> **产品线逻辑**：GPT-5.6 系列做通用（Sol 旗舰 → Terra 主力 → Luna 轻量），Cyber 走 Daybreak 安全线，o 系列做深度推理。2026-07-09 起 GPT-5.6 Sol 在 ChatGPT 推出，目前为旗舰。

## 三、技术架构

**MoE 路径（推测）** —— GPT-5 系列采用 MoE 架构，具体专家数未公开。相比 Anthropic 的 dense 路线，MoE 让 OpenAI 在相同推理成本下堆更大参数量。

**o-series 推理模型** —— OpenAI 的核心差异化。o1/o3 用 RLVR（Reinforcement Learning with Verifiable Rewards）训练：数学题答案对错、代码题单测通过率，完全可程序验证。**"多花时间想 = 准确率提升"** 是 o-series 的核心理念。o4-mini 等后续型号仍在定价表中。

**开源动态（GPT-OSS）** —— OpenAI 已进入"闭源 + 开源"双轨，开源型号以官方发布为准（具体尺寸与许可请查 OpenAI 官方开源仓库）。

## 四、核心能力

| 能力 | 描述 | 落地 |
|------|------|------|
| **Function Calling** | JSON Schema 函数调用 | Chat Completions API |
| **Structured Outputs** | 强制 JSON 输出格式 | 响应格式参数 |
| **Vision** | 图片理解 + OCR | GPT-4o / GPT-5 原生 |
| **Realtime API** | 语音实时交互 | WebSocket 流式 |
| **Code Interpreter** | 沙箱内执行代码 | Assistants API |
| **File Search** | RAG 检索增强 | Assistants API |

**Function Calling 是 OpenAI 首创** —— 2023 年 6 月推出，现已成为行业标准。Claude 的 Tool Use、Kimi 的 Tool Use 都是跟进。

## 五、部署形态

| 部署 | 平台 | 适合 |
|------|------|------|
| **OpenAI API** | `platform.openai.com` | 直接 API 调用 |
| **Azure OpenAI** | Azure 云 | 企业合规 / 私有 VPC |
| **GPT-OSS** | HuggingFace / 自部署 | 私有化 / 微调 |
| **ChatGPT** | Web/Desktop/Mobile | 终端用户产品 |

**Azure OpenAI 是企业入口** —— 大客户走 Azure marketplace 计费，与 Microsoft 365 深度集成。

## 六、价格（截至 2026-08，官方定价）

| 模型 | Input | Output | 缓存读 | 备注 |
|------|-------|--------|--------|------|
| GPT-5.6 Sol | $5 / MTok | $30 / MTok | $0.50 | 旗舰；长上下文档 $10 / $45 |
| GPT-5.6 Terra | $2 / MTok | $12 / MTok | $0.20 | 主力 |
| GPT-5.6 Luna | $0.20 / MTok | $1.20 / MTok | $0.02 | 轻量 |
| GPT-5.6 Cyber | $12.50 / MTok | $75 / MTok | $1.25 | Daybreak 安全线 |

**价格梯度**：Luna < Terra < Sol < Cyber。**Cyber 最贵**（安全专精），Sol 是通用旗舰。

**定价另有档位**：长上下文（long context）约 2x；Fast 模式、Realtime / 图像 / 视频模型各有独立定价——见 OpenAI 官方 [pricing](https://developers.openai.com/api/docs/pricing)。

## 七、适合场景 / 不适合场景

**适合**：
- 通用对话（GPT-5.6 Terra / Luna 性价比高）
- 数学 / 代码 / 逻辑推理（o 系列业界标杆）
- 多模态（Vision + Realtime API）
- 企业合规（Azure OpenAI 深度集成）

**不适合**：
- 超低成本边缘场景（Luna 之外仍偏贵）
- 极简单轮问答（杀鸡用牛刀）
- 国内直接使用（需走 Azure 或代理）

## 八、最新动态（2026-08）

**三层产品线跟踪**：

- **产品层 — ChatGPT**：面向终端用户的对话产品，功能更新频繁（工具调用、多模态、Agent 能力）
- **模型层 — GPT 系列 / o 系列**：
  - **GPT 系列**：通用对话与生成，主打综合能力（GPT-4、GPT-4o 等）
  - **o 系列**：推理模型，回答前「思考」更久，擅长数学、编程、逻辑（o1、o3 等）
- **开发者层 — Platform API**：模型 API、助手 API、微调、批处理端点。价格与限额变化对工程师最直接

> 关键认知：2024 年起 OpenAI 把「快速应答」与「慢速推理」分成两条模型线，o 系列确立了**推理时计算（inference-time compute）**路线——这也影响了后来的整个行业，包括 [DeepSeek-R1](/ai-trends/cn-vendors/)。

**已核实的历史锚点**：

| 时间 | 事件 | 意义 |
| --- | --- | --- |
| 2022-11 | ChatGPT 发布 | 对话式 AI 进入大众视野 |
| 2023-03 | GPT-4 发布 | 多模态（图像输入）与更强推理 |
| 2024-05 | GPT-4o 发布 | 实时语音对话；免费开放 |
| 2024-09 | o1 发布 | 推理时计算路线确立，推理模型品类诞生 |
| 2026-07 | GPT-5.6 Sol 推出 | 旗舰推理模型，主打编码 / 研究 / 科学 / 网络安全 |

> ⚠️ 锚点截至 2026-08 已核实；更新的动态以 [OpenAI Blog](https://openai.com/blog) 为准。注意：GPT-5 系列 2026 年已迭代到 5.6，引用旧版本数字时需注明版本号。

**如何跟踪**：

1. **官方源**：[OpenAI Blog](https://openai.com/blog)（产品与模型）、[Platform docs](https://platform.openai.com/docs)（API 变化）、[Status](https://status.openai.com)（服务可用性）
2. **关注信号**：模型降价 / 提价、上下文长度变化、新端点、功能从「实验室」转「正式」
3. **中文二手**：机器之心、量子位聚合快，但价格等数字以官方为准

## 关键洞察

- **o 系列是推理标杆** —— RLVR 训练让"想得更久 = 答得更准"成为现实
- **GPT-5.6 Sol 是性价比旗舰** —— 比 GPT-4o 时代大幅降价，编码与知识工作接近前沿
- **Function Calling 是行业标准** —— Claude / Kimi / Qwen 都兼容 OpenAI 格式
- **Azure 是企业护城河** —— 与 Microsoft 365 / Copilot 深度绑定

## 参考

- [OpenAI 平台文档](https://platform.openai.com/docs)
- [OpenAI 定价](https://openai.com/pricing)
- [Anthropic Claude 对比](../anthropic/)
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 下一步

- 看国内厂商路线 → [Moonshot · Kimi 全系](/ai-trends/cn-vendors/moonshot/)
- 看横向对比表 → [5 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)
