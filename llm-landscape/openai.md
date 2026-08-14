---
title: OpenAI · GPT 全系
description: GPT-5 / GPT-5 mini / o1 / o3 / GPT-OSS——技术架构、推理模型路线、部署与价格
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: OpenAI 平台文档
      url: https://platform.openai.com/docs
      accessedAt: 2026-08-13
    - name: OpenAI 定价
      url: https://openai.com/pricing
      accessedAt: 2026-08-13
---

# OpenAI · GPT 全系

> 5 家厂商里**最早商业化 + 最激进推理模型路线（o-series）+ 2026 年首次开源（GPT-OSS）**。

## 一、公司背景

OpenAI 2015 年成立，从非营利转型为"利润上限"结构。核心投资方 Microsoft（累计 $130 亿+）。商业模式：闭源 API + ChatGPT 订阅 + Azure OpenAI 企业部署。2026 年首次开源 GPT-OSS 20B/120B，标志策略转向。

## 二、模型矩阵

| 模型 | 定位 | 上下文 | 思考模式 | 主要场景 |
|------|------|--------|----------|----------|
| **GPT-5** | 旗舰 | 128K | adaptive thinking | 复杂推理 / 多模态 / Agent |
| **GPT-5 mini** | 主力 | 128K | 快速 | 通用对话 / 编码 / 成本敏感 |
| **o1** | 推理 | 200K | 长思考 | 数学 / 代码 / 逻辑 |
| **o3** | 推理增强 | 200K | 长思考 | 竞赛级推理 / 复杂分析 |
| **GPT-OSS 120B** | 开源旗舰 | 128K | — | 私有部署 / 微调 |
| **GPT-OSS 20B** | 开源轻量 | 128K | — | 端侧 / 低成本 |

> **产品线逻辑**：GPT-5 系列做通用，o-series 做推理，GPT-OSS 做开源——三条线覆盖不同需求。

## 三、技术架构

**MoE 路径（推测）** —— GPT-5 系列采用 MoE 架构，具体专家数未公开。相比 Anthropic 的 dense 路线，MoE 让 OpenAI 在相同推理成本下堆更大参数量。

**o-series 推理模型** —— OpenAI 的核心差异化。o1/o3 用 RLVR（Reinforcement Learning with Verifiable Rewards）训练：数学题答案对错、代码题单测通过率，完全可程序验证。**"多花时间想 = 准确率提升"** 是 o-series 的核心理念。

**GPT-OSS 开源** —— 2026 年首次开源，20B/120B 两个尺寸。基于 GPT-5 架构裁剪，Apache 2.0 许可。标志 OpenAI 从"纯闭源"转向"闭源 + 开源"双轨。

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

## 六、价格 / 性能基准（截至 2026-08）

| 模型 | Input | Output | SWE-bench | MMLU | GPQA |
|------|-------|--------|-----------|------|------|
| GPT-5 | $10 / MTok | $30 / MTok | 75.2% | 89.3% | 72.1% |
| GPT-5 mini | $1.50 / MTok | $6 / MTok | 68.5% | 85.7% | 65.3% |
| o1 | $15 / MTok | $60 / MTok | 71.8% | 87.5% | 78.9% |
| o3 | $20 / MTok | $80 / MTok | 未公开 | 未公开 | 85.2% |
| GPT-OSS 120B | 免费（自部署） | — | 62.3% | 83.1% | 58.7% |

**价格梯度**：GPT-OSS（免费）< GPT-5 mini < GPT-5 < o1 < o3。**o-series 最贵**，但推理准确率最高。

## 七、适合场景 / 不适合场景

**适合**：
- 通用对话（GPT-5 mini 性价比高）
- 数学 / 代码 / 逻辑推理（o-series 业界最强）
- 多模态（Vision + Realtime API）
- 企业合规（Azure OpenAI 深度集成）

**不适合**：
- 超长上下文（128K，不如 Kimi 2M / Claude 200K + Fable 1M）
- 极低成本场景（GPT-OSS 免费但需自部署）
- 国内直接使用（需走 Azure 或代理）

## 关键洞察

- **o-series 是推理标杆** —— RLVR 训练让"想得更久 = 答得更准"成为现实
- **GPT-OSS 改变格局** —— 2026 年首次开源，直接与 Qwen / GLM 竞争
- **Function Calling 是行业标准** —— Claude / Kimi / Qwen 都兼容 OpenAI 格式
- **Azure 是企业护城河** —— 与 Microsoft 365 / Copilot 深度绑定

## 参考

- [OpenAI 平台文档](https://platform.openai.com/docs)
- [OpenAI 定价](https://openai.com/pricing)
- [Anthropic Claude 对比](./anthropic)
- [技术架构总览](./architecture)

## 下一步

- 看国内厂商路线 → [Moonshot · Kimi 全系](./moonshot)
- 看横向对比表 → [5 厂商横向对比](./comparison)
- 选型决策 → [选型决策树](./selection-guide)
