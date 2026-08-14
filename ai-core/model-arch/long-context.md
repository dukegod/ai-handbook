---
title: 长上下文技术
description: RoPE / YaRN / Ring Attention / 上下文窗口扩展
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: RoPE 论文
      url: https://arxiv.org/abs/2104.09864
      accessedAt: 2026-08-13
    - name: YaRN 论文
      url: https://arxiv.org/abs/2309.00071
      accessedAt: 2026-08-13
---

# 长上下文技术

> **TL;DR**：RoPE 位置插值是主流方案，YaRN / LongRoPE 是进阶优化。2026 年最长到 2M token（Kimi）。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- RoPE 位置编码的原理与扩展
- YaRN / LongRoPE 的优化思路
- KV Cache 优化（PagedAttention）
- 各家模型的上下文长度

## RoPE：旋转位置编码

**原理**：把位置编码成"复数相位的旋转"。Q 和 K 的内积天然带相对位置信息。

```
q_m^T R(m-n) k_n
```

其中 R(m-n) 是旋转矩阵，m 和 n 是两个 token 的位置。

**优势**：

- 天然支持相对位置
- 无需额外参数
- 扩展性好

## 位置插值扩展

RoPE 的频率是为训练长度设计的。扩展到更长上下文需要**位置插值**。

### PI（Position Interpolation）

最简单：线性缩放频率 θ → θ/scale。

```
θ'_i = θ_i / scale
```

**问题**：高频位置精度损失。

### YaRN（2023）

结合 NTK-aware 插值 + 注意力缩放：

- 低频维度：线性插值
- 高频维度：NTK-aware 缩放
- 注意力分数：加温度缩放

**YaRN 是 Claude 200K 的推测方案**。

### LongRoPE（2024）

搜索每个维度的最优缩放因子：

```
θ'_i = θ_i / scale_i  （每个维度不同 scale）
```

**LongRoPE 是 Kimi 2M 的推测方案**。

## 各家上下文长度

| 厂商 | 模型 | 上下文 | 技术 |
|------|------|--------|------|
| Anthropic | Claude | 1M（Opus 5 / Sonnet 5） | RoPE + YaRN（推测） |
| Anthropic | Fable 5 | 1M | RoPE 扩展 |
| OpenAI | GPT-5.6 | 短/长上下文双档 | RoPE 扩展 |
| Moonshot | Kimi K3 | 1M | LongRoPE 风格 |
| Qwen | Qwen3.5 / Qwen3.8-Max | 1M | RoPE + 滑动窗口 |

## KV Cache 优化

长上下文时，KV Cache 占用大量显存：

```
KV Cache 大小 = 2 × 层数 × 头数 × 头维度 × 序列长度 × batch_size
```

**200K context ≈ 几 GB KV Cache**。

### PagedAttention（vLLM）

把 KV Cache 分成固定大小的"页"，按需分配，避免碎片化。

**效果**：显存利用率提升 2-4x，支持更大 batch。

### 滑动窗口注意力

大部分层只看局部窗口（4K-8K），少数层看全 attention。

**效果**：KV Cache 减少 80%+，保留长程依赖。

## 常见坑

**长上下文 ≠ 全部有效**

模型在 200K context 下，中间位置的信息检索准确率会下降（"lost in the middle"问题）。

**KV Cache 成本**

长上下文的推理成本主要是 KV Cache，不是计算。优化 KV Cache 比优化计算更有效。

## 参考

- [RoPE: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864)（2021）
- [YaRN: Efficient Context Window Extension](https://arxiv.org/abs/2309.00071)（2023）
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 下一步

- 了解多模态架构 → [多模态架构](./multimodal)
- 了解推理优化 → [推理优化](../training/inference-optimization)

## 如果你想

- 看各家模型的上下文选择 → [5 厂商横向对比](/reference/model-comparison)
- 了解注意力机制 → [注意力机制](../fundamentals/attention)
