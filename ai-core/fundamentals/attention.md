---
title: 注意力机制
description: Self-Attention / Multi-Head / Flash Attention 的原理与演进
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: FlashAttention
      url: https://arxiv.org/abs/2205.14135
      accessedAt: 2026-08-13
    - name: FlashAttention-2
      url: https://arxiv.org/abs/2307.08691
      accessedAt: 2026-08-13
---

# 注意力机制

> **TL;DR**：注意力让每个 token 看所有其他 token。Multi-Head 增加表达力，Flash Attention 优化显存和速度。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- Self-Attention 的数学原理
- Multi-Head Attention 的设计动机
- Flash Attention 的显存优化
- 注意力的 O(n²) 复杂度问题与解法

## Self-Attention 数学

每个 token 生成三个向量：

- **Q（Query）**：我在找什么
- **K（Key）**：我有什么特征
- **V（Value）**：我的实际内容

```
Attention(Q, K, V) = softmax(QK^T / √d_k) × V
```

**步骤**：

1. Q 和 K 做点积，得到相关性分数矩阵（n×n）
2. 除以 √d_k 防止分数过大
3. Softmax 归一化为概率分布
4. 用概率分布加权求和 V

**复杂度**：O(n²d)，n 是序列长度，d 是维度。**n² 是长上下文的瓶颈**。

## Multi-Head Attention

把 Q/K/V 拆成 h 个头，每个头独立算注意力，最后拼接：

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) × W_o
head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

**为什么需要多头？**

- 不同头关注不同类型的关系（语法、语义、位置）
- 增加模型表达能力
- 不增加计算量（每个头维度是 d/h）

## Flash Attention

传统注意力的 O(n²) 显存是瓶颈。Flash Attention 通过**分块计算**优化：

**核心思想**：不把完整的 n×n 注意力矩阵存到显存，而是分块计算，利用 SRAM 的高速缓存。

**优化效果**：

| 指标 | 传统注意力 | Flash Attention |
|------|-----------|-----------------|
| 显存 | O(n²) | O(n) |
| 速度 | 基准 | 2-4x 加速 |
| 精度 | 基准 | 完全一致 |

**Flash Attention 2**（2023）进一步优化：更好的并行度、更少的非矩阵乘法操作。**2026 年所有主流模型都用 Flash Attention**。

## 注意力变体

| 变体 | 复杂度 | 原理 | 适用 |
|------|--------|------|------|
| **Full Attention** | O(n²) | 每个 token 看所有 | 标准 |
| **Sliding Window** | O(n×w) | 只看局部窗口 w | Mistral / Qwen |
| **Sparse Attention** | O(n√n) | 稀疏采样 | 长序列 |
| **Linear Attention** | O(n) | 核近似替代 softmax | 实验中 |

**Sliding Window + Full Attention 混合**是 2026 年主流：大部分层用滑动窗口（4K-8K），少数层用全 attention，**节省 KV cache 又保留长程依赖**。

## KV Cache

推理时，之前 token 的 K/V 可以缓存，避免重复计算：

```
新 token 只需计算自己的 Q，与缓存的 K/V 做注意力
```

**KV Cache 问题**：长上下文时 KV Cache 占用大量显存（200K context ≈ 几 GB）。**PagedAttention（vLLM）** 通过分页管理解决碎片化问题。

## 常见坑

**O(n²) 不可避免**

Full Attention 的 O(n²) 是数学限制，无法绕过。只能用 Sliding Window / Sparse 等近似方案。

**Flash Attention 不改变结果**

Flash Attention 只是优化显存和速度，注意力计算结果与传统方法完全一致。

## 参考

- [FlashAttention: Fast and Memory-Efficient Exact Attention](https://arxiv.org/abs/2205.14135)（2022）
- [FlashAttention-2](https://arxiv.org/abs/2307.08691)（2023）
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)（2017）

## 下一步

- 了解预训练流程 → [预训练与微调](./pretraining)
- 了解长上下文技术 → [长上下文技术](../model-arch/long-context)

## 如果你想

- 看各家模型的注意力选择 → [LLM 全景 · 技术架构总览](/llm-landscape/architecture)
- 了解推理优化 → [推理优化](../training/inference-optimization)
