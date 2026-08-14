---
title: 多模态架构
description: 视觉-语言模型、跨模态对齐、多模态训练策略
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: LLaVA 论文
      url: https://arxiv.org/abs/2304.08485
      accessedAt: 2026-08-13
    - name: Qwen-VL 论文
      url: https://arxiv.org/abs/2308.12966
      accessedAt: 2026-08-13
---

# 多模态架构

> **TL;DR**：三种路径——原生多模态（GPT-4o）、适配器（LLaVA/Qwen-VL）、混合专家。2026 年适配器是开放权重标配。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 三种多模态架构的区别
- 视觉编码器的选择
- 跨模态对齐的训练策略
- 各家模型的多模态能力

## 三种架构路径

### 1. 原生多模态

视觉/音频在预训练阶段 token 化统一——所有模态共享同一个 Transformer。

**优势**：模态间交互最自然，端到端训练。

**劣势**：需要大量多模态预训练数据，成本高。

**代表**：GPT-4o / Claude 3.5+ / Gemini

### 2. 适配器

文本主干冻结，视觉/音频通过 adapter 微调接入。

```
图片 → 视觉编码器 → adapter → 文本 Transformer
```

**优势**：复用已有文本模型，成本低。

**劣势**：模态间交互受限于 adapter 容量。

**代表**：LLaVA / Qwen-VL / CogVLM

### 3. 混合专家

不同模态走不同 expert 路由。

**优势**：模态特化，效率高。

**劣势**：路由复杂，训练不稳定。

**代表**：GLM-4V（推测）

## 视觉编码器

| 编码器 | 原理 | 代表 |
|--------|------|------|
| **ViT** | 图片切 patch，当 token 处理 | LLaVA / Qwen-VL |
| **CLIP** | 图文对比学习 | DALL-E / Stable Diffusion |
| **SigLIP** | CLIP 改进版 | Gemini |

**ViT + CLIP 是主流**：先用 CLIP 预训练对齐图文表示，再用 ViT 提取视觉特征。

## 跨模态对齐

**问题**：视觉 token 和文本 token 的表示空间不同，需要对齐。

**方法**：

1. **线性投影**：最简单，视觉 token 通过线性层映射到文本空间
2. **Q-Former**：用可学习的 query token 从视觉特征中提取信息（BLIP-2）
3. **Cross-Attention**：文本 token 通过交叉注意力看视觉特征

**2026 年主流是线性投影**——简单有效，Q-Former 和 Cross-Attention 的额外复杂度收益不大。

## 训练策略

**阶段 1：预训练视觉编码器**

用 CLIP 目标（图文对比学习）训练视觉编码器。

**阶段 2：对齐训练**

冻结视觉编码器，训练 adapter 让视觉 token 与文本 token 对齐。

**阶段 3：指令微调**

用多模态指令数据微调整个模型。

## 各家多模态能力

| 厂商 | 文本 | 图片 | 音频 | 视频 | 全模态 |
|------|------|------|------|------|--------|
| Anthropic | ✅ | ✅ | ❌ | ❌ | ❌ |
| OpenAI | ✅ | ✅ | ✅ | ❌ | ❌ |
| Moonshot | ✅ | ✅ | ❌ | ✅ | ❌ |
| Zhipu | ✅ | ✅ | ❌ | ❌ | ❌ |
| Qwen | ✅ | ✅ | ✅ | ✅ | ✅（Omni） |

**Qwen 全模态最完整**——文本、图片、音频、视频全覆盖。

## 常见坑

**多模态 ≠ 理解**

模型能"看"图片，但不一定"理解"。复杂图表推理仍是挑战。

**视觉 token 成本**

一张图片 ≈ 100-1000 个 token，多图场景成本高。

## 参考

- [LLaVA: Visual Instruction Tuning](https://arxiv.org/abs/2304.08485)（2023）
- [Qwen-VL: A Versatile Vision-Language Model](https://arxiv.org/abs/2308.12966)（2023）
- [LLM 全景 · 技术架构总览](/llm-landscape/architecture)

## 下一步

- 了解数据工程 → [数据工程](../training/data-engineering)
- 了解推理优化 → [推理优化](../training/inference-optimization)

## 如果你想

- 看各家模型的多模态能力 → [LLM 全景 · 5 厂商横向对比](/llm-landscape/comparison)
- 用 Claude 处理图片 → [Claude 能力 · 视觉能力](/claude-capabilities/core/vision)
