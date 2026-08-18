---
title: Zhipu · 智谱 GLM 全系
description: GLM-5.2 / GLM-5 / GLM-Z1——清华系、Agentic Coding、全尺寸开源
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: 智谱开放平台定价
      url: https://docs.bigmodel.cn
      accessedAt: 2026-08-14
    - name: GLM-5 官方文档
      url: https://docs.bigmodel.cn/cn/guide/models/text/glm-5
      accessedAt: 2026-08-14
---

# Zhipu · 智谱 GLM 全系

> 7 家厂商里**清华学术背景最深 + Agent 工具链最完整 + 全尺寸开源最彻底**。

## 一、公司背景

智谱 AI 由清华大学唐杰教授团队 2019 年孵化，总部北京。核心定位是**"学术 + 开源 + Agent"**——从 GLM-130B 开源起步，逐步商业化。商业模式：BigModel API + 企业 MaaS + 开源权重。是国内最早做大模型商业化的公司之一。

## 二、模型矩阵

| 模型 | 定位 | 上下文 | 思考模式 | 主要场景 |
|------|------|--------|----------|----------|
| **GLM-5.2** | 旗舰 | 200K+ | — | Agentic Engineering / 通用 |
| **GLM-5** | 上一代旗舰 | 200K | — | 已由 5.2 取代（744B / 40B） |
| **GLM-Z1** | 推理增强 | — | RLVR | 数学 / 代码 / 逻辑 |
| **GLM-4-Air** | 轻量 | — | — | 高并发 / 低成本 |

> **产品线逻辑**：GLM-5.2 做旗舰（2026 官方定价在售）、GLM-5 是上一代（744B / 40B 激活，主打 Agentic Coding）、GLM-Z1 做推理、GLM-4-Air 做轻量。

## 三、技术架构

**MoE 路径** —— GLM-5 系列采用 MoE 架构（GLM-5 为 744B 总参数 / 40B 激活），从 GLM-4 的 dense 演进，与行业趋势一致。

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

**CodeGeeX 开源** —— 智谱开源的 IDE 编程助手（VS Code / JetBrains），底层用 GLM 系列，是国内最早的 AI 编程工具之一。

## 五、部署形态

| 部署 | 平台 | 适合 |
|------|------|------|
| **BigModel API** | `open.bigmodel.cn` | 直接 API 调用 |
| **GLM-4 开源** | HuggingFace / ModelScope | 私有部署 / 微调 |
| **GLM-4-Air** | 端侧部署 | 低成本 / 隐私 |
| **MaaS 企业版** | 智谱云 | 企业私有化 |

**全尺寸开源是智谱优势** —— GLM-4 / GLM-4-Vision 完全开源（Apache 2.0），从 1.5B 到 130B 全尺寸覆盖。是国内开源最彻底的大模型厂商。

## 六、价格（截至 2026-08，官方定价）

| 模型 | Input | Output | 缓存命中 | 备注 |
|------|-------|--------|---------|------|
| GLM-5.2 | $1.4 / MTok | $4.4 / MTok | $0.26 | 旗舰 |
| GLM-5.1 | $1.4 / MTok | $4.4 / MTok | $0.26 | 同价位在售 |

**GLM-5.2 / 5.1 官方定价（2026-08）** —— 智谱旗舰 API 定价，大幅低于 Claude / GPT 同档；另有 Coding Plan（Max / Pro 套餐）支持 Claude Code 接入。

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
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- [Anthropic Claude 对比](/ai-trends/vendors/anthropic/)

## 下一步

- 看另一家开源路线 → [Qwen · 阿里通义千问全系](../qwen/)
- 看横向对比表 → [5 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)
