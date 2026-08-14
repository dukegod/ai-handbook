---
title: Transformer 架构
description: 自注意力机制、编码器-解码器、位置编码——现代大模型的基石
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: Attention Is All You Need
      url: https://arxiv.org/abs/1706.03762
      accessedAt: 2026-08-13
---

# Transformer 架构

> **TL;DR**：Transformer 用自注意力替代 RNN 的序列依赖，实现并行计算。2017 年论文 "Attention Is All You Need" 是现代大模型的基石。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- Transformer 的核心思想与架构
- 编码器-解码器 vs 仅解码器的区别
- 位置编码的作用与实现
- 为什么 Transformer 能替代 RNN

## 核心思想

**RNN 的问题**：序列必须逐个处理，无法并行。长序列时早期信息被遗忘（梯度消失）。

**Transformer 的解法**：用**自注意力（Self-Attention）**让每个位置直接看所有其他位置，无需序列依赖。**并行计算 + 长程依赖**，一举两得。

## 架构演进

| 阶段 | 架构 | 代表模型 | 适用任务 |
|------|------|----------|----------|
| Encoder-Decoder | 编码+解码分离 | T5 / BART | 翻译 / 摘要 |
| Encoder-only | 仅编码 | BERT | 分类 / 理解 |
| Decoder-only | 仅解码 | GPT / Claude / LLaMA | 生成 / 对话 |

2026 年主流是**Decoder-only**——GPT-5.6、Claude、Kimi K3、Qwen3.5 都是。Encoder-only（BERT 系列）主要用于嵌入和分类。

## 三大核心组件

### 1. 自注意力（Self-Attention）

每个 token 生成三个向量：Query（Q）、Key（K）、Value（V）。

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```

**直觉**：Q 是"我在找什么"，K 是"我有什么"，V 是"我的内容"。Q 和 K 的点积算出相关性分数，加权求和 V 得到输出。

### 2. 多头注意力（Multi-Head Attention）

把 Q/K/V 拆成多个"头"，每个头独立算注意力，最后拼接。

**好处**：不同头可以关注不同类型的关系（语法、语义、位置等）。

### 3. 前馈网络（FFN）

每个位置独立的两层全连接网络：`FFN(x) = W₂ × ReLU(W₁ × x + b₁) + b₂`

**作用**：注意力负责"看其他位置"，FFN 负责"处理当前位置"。

## 位置编码

Transformer 没有内置的顺序信息，需要**位置编码**告诉模型每个 token 的位置。

| 方法 | 原理 | 代表 |
|------|------|------|
| **正弦位置编码** | 用 sin/cos 函数生成固定编码 | 原始 Transformer |
| **可学习位置编码** | 位置编码作为参数训练 | BERT / GPT-2 |
| **RoPE** | 旋转位置编码，天然支持相对位置 | LLaMA / Claude / Qwen |
| **ALiBi** | 线性偏置，无需训练 | BLOOM |

2026 年主流是 **RoPE**——旋转位置编码的内积天然带相对位置信息，扩展到长上下文时只需做位置插值。

## Decoder-only 为什么赢

| 特性 | Encoder-Decoder | Decoder-only |
|------|-----------------|--------------|
| 训练效率 | 需要配对数据 | 纯文本自回归 |
| 生成能力 | 需要解码器 | 原生生成 |
| 扩展性 | 受限于编码器 | 线性扩展 |
| In-context Learning | 弱 | 强 |

**Decoder-only 的核心优势**：自回归训练（预测下一个 token）天然适合生成任务，且 scaling law 表现最好——相同计算量下，Decoder-only 性能最高。

## 常见坑

**把 Transformer 当万能**

Transformer 不擅长精确数值计算、实时推理、超长序列（>1M）。这些场景需要专门的工具或架构。

**忽略位置编码**

位置编码决定了模型能处理的最大长度。RoPE 的扩展性好，但也有上限（通常 2M token）。

## 参考

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)（2017）
- [LLaMA: Open and Efficient Foundation Language Models](https://arxiv.org/abs/2302.13971)（2023）
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 下一步

- 深入注意力机制 → [注意力机制](./attention)
- 了解预训练流程 → [预训练与微调](./pretraining)

## 如果你想

- 看各家模型的架构选择 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- 了解 Dense vs MoE → [Dense vs MoE](../model-arch/dense-vs-moe)
- 动手实操 → [AI Coding 落地](/ai-coding/)
