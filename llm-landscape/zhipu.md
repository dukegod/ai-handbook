---
title: Zhipu · 智谱 GLM 全系
description: GLM-5 / GLM-4.6 / GLM-Z1 / CogVLM——清华系、Agent 能力、全尺寸开源
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: 智谱 BigModel 开放平台
      url: https://open.bigmodel.cn/
      accessedAt: 2026-08-13
    - name: GLM-4 技术报告
      url: https://github.com/THUDM/GLM-4
      accessedAt: 2026-08-13
---

# Zhipu · 智谱 GLM 全系

> 5 家厂商里**清华学术背景最深 + Agent 工具链最完整 + 全尺寸开源最彻底**。

## 一、公司背景

智谱 AI 由清华大学唐杰教授团队 2019 年孵化，总部北京。核心定位是**"学术 + 开源 + Agent"**——从 GLM-130B 开源起步，逐步商业化。商业模式：BigModel API + 企业 MaaS + 开源权重。是国内最早做大模型商业化的公司之一。

## 二、模型矩阵

| 模型 | 定位 | 上下文 | 思考模式 | 主要场景 |
|------|------|--------|----------|----------|
| **GLM-5** | 旗舰 | 128K | — | 通用 / 复杂推理 / Agent |
| **GLM-4.6** | 主力 | 128K | — | 编码 / 通用对话 |
| **GLM-Z1** | 推理增强 | 128K | RLVR | 数学 / 代码 / 逻辑 |
| **GLM-4-Vision** | 多模态 | 128K | — | 图片理解 / OCR |
| **GLM-4-Air** | 轻量 | 128K | — | 高并发 / 低成本 |

> **产品线逻辑**：GLM-5 做旗舰、GLM-4.6 做主力、GLM-Z1 做推理、GLM-4-Air 做轻量——四层覆盖。

## 三、技术架构

**MoE 路径（推测）** —— GLM-5 采用 MoE 架构，具体专家数未公开。从 GLM-4 的 dense 演进到 GLM-5 的 MoE，与行业趋势一致。

**GLM 双向注意力** —— GLM 系列的独特设计：早期版本用双向注意力（Encoder-Decoder 风格），GLM-4 起转为自回归（Decoder-only）。**双向注意力在理解任务上有优势，但生成任务不如自回归**。

**GLM-Z1 推理** —— 和 OpenAI o-series / Kimi K2 Thinking 同路线：RLVR 训练。在中文数学/代码基准上表现优异。

**CogVLM 多模态** —— 智谱自研的视觉语言模型，GLM-4-Vision 底层用 CogVLM 架构。支持图片理解、OCR、图表分析。

## 四、核心能力

| 能力 | 描述 | 落地 |
|------|------|------|
| **Tool Use** | 函数调用 / AllTools | BigModel API |
| **Agent** | GLM-Z1 推理 + 工具调用 | AllTools 组合 |
| **CogVLM** | 视觉理解 + OCR | GLM-4-Vision |
| **代码能力** | 代码生成 / 审查 | CodeGeeX（开源 IDE 插件） |
| **AllTools** | 搜索 + 计算 + 绘图组合 | BigModel 内置 |

**AllTools 是智谱的差异化** —— 一个 API 调用同时支持搜索、计算、绘图、代码执行，类似 ChatGPT 的 Code Interpreter + Web Browsing 组合。

**CodeGeeX 开源** —— 智谱开源的 IDE 编程助手（VS Code / JetBrains），底层用 GLM-4.6，是国内最早的 AI 编程工具之一。

## 五、部署形态

| 部署 | 平台 | 适合 |
|------|------|------|
| **BigModel API** | `open.bigmodel.cn` | 直接 API 调用 |
| **GLM-4 开源** | HuggingFace / ModelScope | 私有部署 / 微调 |
| **GLM-4-Air** | 端侧部署 | 低成本 / 隐私 |
| **MaaS 企业版** | 智谱云 | 企业私有化 |

**全尺寸开源是智谱优势** —— GLM-4 / GLM-4-Vision 完全开源（Apache 2.0），从 1.5B 到 130B 全尺寸覆盖。是国内开源最彻底的大模型厂商。

## 六、价格 / 性能基准（截至 2026-08）

| 模型 | Input | Output | C-Eval | CMMLU | SuperCLUE |
|------|-------|--------|--------|-------|-----------|
| GLM-5 | ¥15 / MTok | ¥45 / MTok | 88.7% | 87.9% | 85.3% |
| GLM-4.6 | ¥5 / MTok | ¥15 / MTok | 85.2% | 84.6% | 82.1% |
| GLM-Z1 | ¥10 / MTok | ¥30 / MTok | 90.1% | 89.3% | 86.7% |
| GLM-4-Air | ¥0.5 / MTok | ¥1.5 / MTok | 78.3% | 77.1% | 74.5% |

**GLM-Z1 在中文推理基准上最强** —— C-Eval 90.1%、CMMLU 89.3%，超过 GPT-5 和 Claude Opus 4.8。

## 七、适合场景 / 不适合场景

**适合**：
- 中文场景（中文基准领先，中文原生训练）
- 国产化替代（全尺寸开源，可完全私有部署）
- Agent 部署（AllTools + GLM-Z1 推理）
- 学术研究（清华背景，开源最彻底）

**不适合**：
- 英文为主的场景（Claude / GPT 英文更强）
- 超长上下文（128K，不如 Kimi 2M / Claude 200K + Fable 1M）
- 极简单轮问答（GLM-4-Air 也比 Qwen 同尺寸贵）

## 关键洞察

- **全尺寸开源是最大优势** —— 1.5B 到 130B 全覆盖，私有部署最灵活
- **GLM-Z1 中文推理最强** —— C-Eval / CMMLU 基准领先
- **AllTools 是差异化** —— 搜索 + 计算 + 绘图组合，类似 ChatGPT 体验
- **CodeGeeX 是编程入口** —— 国内最早的 AI 编程助手之一

## 参考

- [智谱 BigModel 开放平台](https://open.bigmodel.cn/)
- [GLM-4 技术报告](https://github.com/THUDM/GLM-4)
- [技术架构总览](./architecture)
- [Anthropic Claude 对比](./anthropic)

## 下一步

- 看另一家开源路线 → [Qwen · 阿里通义千问全系](./qwen)
- 看横向对比表 → [5 厂商横向对比](./comparison)
- 选型决策 → [选型决策树](./selection-guide)
