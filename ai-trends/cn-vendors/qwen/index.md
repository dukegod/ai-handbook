---
title: Qwen · 阿里通义千问全系
description: Qwen3.8-Max / Qwen3.5 / Qwen3——全尺寸开源、阿里达摩院、端侧部署
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: 阿里云百炼 Qwen3.8-Max 模型信息
      url: https://help.aliyun.com/zh/model-studio/qwen3-8-max
      accessedAt: 2026-08-14
    - name: Qwen 官方博客
      url: https://qwenlm.github.io/blog/
      accessedAt: 2026-08-14
    - name: Qwen GitHub
      url: https://github.com/QwenLM/Qwen
      accessedAt: 2026-08-13
---

# Qwen · 阿里通义千问全系

> 7 家厂商里**开源最彻底（全尺寸 + 全模态）+ 端侧部署最成熟 + 阿里云生态最完整**。

## 一、公司背景

Qwen（通义千问）由阿里达摩院 2023 年推出，现属阿里云通义实验室。核心定位是**"全尺寸开源 + 端侧部署 + 阿里云集成"**——从 0.5B 到 110B 全尺寸开源，覆盖从手机到数据中心的全场景。商业模式：DashScope API + 阿里云百炼 + 开源权重。

## 二、模型矩阵

| 模型 | 定位 | 上下文 | 思考模式 | 主要场景 |
|------|------|--------|----------|----------|
| **Qwen3.8-Max** | 旗舰（2026-08 正式版） | 1M | — | 复杂推理 / 长文档 / Agent |
| **Qwen3.5 系列** | 主力 | 1M | 原生多模态 + 思考 | 通用 / 视觉 / 工具调用 |
| **Qwen3** | 上一代 | 1M | adaptive thinking | 已由 3.5 / 3.8 取代 |
| **Qwen-VL** | 多模态专精 | 128K | — | 图片理解 / OCR / 视频 |
| **Qwen-Coder** | 编码专精 | 128K | — | 代码生成 / 审查 |

> **产品线逻辑**：Qwen3.8-Max 做旗舰（2.4T 参数）、Qwen3.5 做主力（plus / flash，原生多模态）、Qwen-VL/Coder 做专精——全尺寸 + 全模态覆盖，开源侧 `qwen3.5-397b-a17b` 等延续 Apache 2.0 路线。

## 三、技术架构

**MoE 路径** —— Qwen3.8-Max 采用 MoE 架构，具体专家数未公开。Qwen 3 系列从 dense 演进到 MoE，与行业趋势一致。

**全尺寸蒸馏** —— Qwen 的独特策略：从 110B 大模型蒸馏到 0.5B/1.5B/7B/14B/32B/72B 各尺寸，**每个尺寸都经过专门优化**。这让小模型也能保持高质量。

**1M 长上下文** —— Qwen 2.5 起已支持 1M token，Qwen 3 延续。技术用 RoPE 位置插值 + 滑动窗口混合。

**Qwen-Agent 框架** —— 阿里开源的 Agent 框架，底层用 Qwen 模型，支持 Tool Use / Code Interpreter / 搜索组合。

## 四、核心能力

| 能力 | 描述 | 落地 |
|------|------|------|
| **Tool Use** | 函数调用 / JSON Schema | DashScope API |
| **Qwen-Agent** | Agent 框架 / 多步推理 | 开源框架 |
| **Qwen-VL** | 图片 + 视频理解 | 原生多模态 |
| **Qwen-Audio** | 语音理解 + TTS | 原生音频 |
| **Qwen-Omni** | 全模态（文本+图+音+视） | 端到端 |
| **Qwen-Coder** | 代码生成 / 审查 | CodeQwen 插件 |

**全模态是 Qwen 差异化** —— 文本、图片、音频、视频全覆盖，Qwen-Omni 是国内首个全模态大模型。

**Qwen-Agent 开源** —— 类似 Claude Code 的 Agent 框架，支持 Tool Use / Code Interpreter / 搜索，但完全开源。

## 五、部署形态

| 部署 | 平台 | 适合 |
|------|------|------|
| **DashScope API** | `dashscope.aliyun.com` | 直接 API 调用 |
| **阿里云百炼** | 阿里云 | 企业 MaaS |
| **HuggingFace** | 开源权重 | 私有部署 / 微调 |
| **ModelScope** | 国内镜像 | 国内部署 |
| **端侧部署** | llama.cpp / MLX / Ollama | 手机 / PC / 嵌入式 |

**端侧部署是 Qwen 最大优势** —— 0.5B/1.5B/7B 小模型专为端侧优化，支持 llama.cpp / MLX / Ollama 等主流推理框架。是国内端侧部署最成熟的模型。

## 六、价格（截至 2026-08，阿里云百炼官方定价）

| 模型 | Input | Output | 缓存命中 | 备注 |
|------|-------|--------|---------|------|
| Qwen3.8-Max | ¥12 / MTok | ¥36 / MTok | ¥1.5 | 旗舰（原价，不含限时优惠） |

**价格梯度**：开源版自部署免费；API 端 Qwen3.8-Max 为旗舰价，开源尺寸（Qwen3.5 系列）自部署成本可控。

## 七、适合场景 / 不适合场景

**适合**：
- 本地部署 / 端侧部署（全尺寸开源 + 端侧优化）
- 国产化替代（阿里云生态 + 完全开源）
- 多尺寸选型（0.5B 到 110B 全覆盖）
- 多模态（文本+图+音+视频全覆盖）

**不适合**：
- 超长文档分析（1M 上下文，不如 Kimi 2M）
- 英文为主的场景（Claude / GPT 英文更强）
- 极端推理任务（o-series / GLM-Z1 推理更强）

## 关键洞察

- **全尺寸开源是最大优势** —— 0.5B 到 110B 全覆盖，端侧到云端无缝衔接
- **Qwen 3-7B 是性价比之王** —— 低成本 + 高性能，适合大部分场景
- **全模态是差异化** —— Qwen-Omni 是国内首个全模态大模型
- **阿里云生态是护城河** —— DashScope + 百炼 + 阿里云集成

## 参考

- [Qwen 官方博客](https://qwenlm.github.io/blog/)
- [DashScope 平台](https://dashscope.aliyun.com/)
- [Qwen GitHub](https://github.com/QwenLM/Qwen)
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- [Anthropic Claude 对比](/ai-trends/vendors/anthropic/)

## 下一步

- 看横向对比表 → [5 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 选型决策 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)
