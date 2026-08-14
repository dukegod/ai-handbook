---
title: 推理优化
description: KV Cache / Speculative Decoding / Continuous Batching / FlashAttention
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: vLLM
      url: https://github.com/vllm-project/vllm
      accessedAt: 2026-08-13
    - name: Speculative Decoding
      url: https://arxiv.org/abs/2211.17192
      accessedAt: 2026-08-13
---

# 推理优化

> **TL;DR**：推理优化是叠加而非替代——FlashAttention + PagedAttention + Speculative Decoding + Continuous Batching 同时使用。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- KV Cache 的原理与优化
- Speculative Decoding 的加速思路
- Continuous Batching 的吞吐提升
- 各层优化技术的组合

## 推理优化全景

| 层 | 技术 | 优化目标 |
|------|------|----------|
| 注意力 | FlashAttention | 显存 + 速度 |
| KV Cache | PagedAttention | 显存利用率 |
| 解码 | Speculative Decoding | 延迟 |
| 批处理 | Continuous Batching | 吞吐 |
| 量化 | INT8/INT4 | 显存 + 速度 |

## KV Cache

**问题**：自回归推理时，每个新 token 都要和所有历史 token 做注意力。重复计算 K/V 浪费。

**解法**：缓存之前 token 的 K/V，新 token 只算自己的 Q。

```
第 1 步：计算所有 token 的 K/V，缓存
第 2 步：新 token 只算 Q，与缓存的 K/V 做注意力
```

**KV Cache 大小**：

```
2 × 层数 × 头数 × 头维度 × 序列长度 × batch_size × 精度
```

**200K context ≈ 4-8 GB KV Cache**（FP16，70B 模型）。

### PagedAttention（vLLM）

传统 KV Cache 连续分配，导致碎片化。PagedAttention 把 KV Cache 分成固定大小的"页"：

- 按需分配，不预留
- 页可以不连续
- 支持跨请求共享（相同 prefix）

**效果**：显存利用率提升 2-4x，吞吐提升 2-3x。

## Speculative Decoding

**问题**：大模型自回归解码，每步只能生成 1 个 token，延迟高。

**解法**：用小模型快速生成多个候选 token，大模型一次性验证。

```
小模型生成 5 个候选 token → 大模型一次性验证 → 接受正确的，拒绝错误的
```

**效果**：延迟降低 2-3x，输出质量不变（数学上等价）。

**适用场景**：延迟敏感的交互式场景。

## Continuous Batching

**问题**：传统批处理等所有请求完成才处理下一批。短请求等长请求，浪费。

**解法**：请求完成就立即释放，新请求立即加入。

```
传统：[请求1, 请求2, 请求3] → 全部完成 → [请求4, 请求5, 请求6]
连续：[请求1, 请求2, 请求3] → 请求2 完成 → [请求1, 请求4, 请求3]
```

**效果**：吞吐提升 2-10x。

## FlashAttention

（详见 [注意力机制](../fundamentals/attention)）

分块计算注意力，利用 SRAM 高速缓存。显存 O(n²) → O(n)，速度 2-4x 加速。

## 优化组合

**2026 年主流推理栈**：

```
FlashAttention（注意力层）
    ↓
PagedAttention（KV Cache 层）
    ↓
Speculative Decoding（解码层）
    ↓
Continuous Batching（批处理层）
    ↓
INT8 量化（精度层）
```

**所有优化叠加使用**，不是互斥选择。

## 推理框架

| 框架 | 特点 | 适用 |
|------|------|------|
| **vLLM** | PagedAttention + Continuous Batching | 通用推理 |
| **TensorRT-LLM** | NVIDIA 优化 | NVIDIA GPU |
| **llama.cpp** | CPU/端侧推理 | 端侧部署 |
| **MLX** | Apple Silicon 优化 | Mac 部署 |

## 常见坑

**优化有上限**

推理优化只能做到硬件极限，无法突破。最终瓶颈是内存带宽。

**精度损失**

量化（INT8/INT4）会损失精度。需要在速度和质量间权衡。

## 参考

- [vLLM](https://github.com/vllm-project/vllm)
- [Speculative Decoding](https://arxiv.org/abs/2211.17192)（2022）
- [LLM 全景 · 技术架构总览](/llm-landscape/architecture)

## 下一步

- 了解量化与蒸馏 → [量化与蒸馏](./quantization)
- 了解基准测试 → [基准测试](../eval/benchmarks)

## 如果你想

- 看各家模型的推理优化 → [LLM 全景 · 技术架构总览](/llm-landscape/architecture)
- 了解注意力机制 → [注意力机制](../fundamentals/attention)
