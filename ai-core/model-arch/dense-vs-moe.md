---
title: Dense vs MoE
description: 稠密模型 vs 混合专家——路由策略、容量因子、训练差异
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: Switch Transformer
      url: https://arxiv.org/abs/2101.03961
      accessedAt: 2026-08-13
    - name: DeepSeek-V3
      url: https://arxiv.org/abs/2412.19437
      accessedAt: 2026-08-13
---

# Dense vs MoE

> **TL;DR**：Dense 每次激活全部参数，MoE 只激活 top-k 个专家。2026 年 MoE 成为主流——相同推理成本下性能更高。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- Dense 和 MoE 的核心区别
- MoE 的路由策略与负载均衡
- Shared Expert vs Routed Expert 双轨设计
- 各家厂商的架构选择

## Dense：全参数激活

**原理**：每次推理，所有参数都参与计算。

**优势**：

- 训练稳定，无路由问题
- 推理行为一致
- 实现简单

**劣势**：

- 推理成本与参数量线性增长
- 难以在低成本下堆大参数

**代表**：Claude（推测）、早期 GPT-3

## MoE：稀疏激活

**原理**：把 FFN 层拆成 N 个专家，每次只激活 top-k 个。

```
输入 token → Router 计算专家分数 → 选 top-k 专家 → 加权求和输出
```

**关键参数**：

| 参数 | 说明 | 典型值 |
|------|------|--------|
| 专家数 N | 总专家数量 | 8-384 |
| 激活数 k | 每次激活的专家数 | 1-8 |
| 容量因子 | 每个专家最多处理的 token 比例 | 1.0-1.5 |

**优势**：

- 相同推理成本下，总参数量可以做得更大
- 相同训练成本下，性能可以追平 dense 大模型

**劣势**：

- 路由不均衡（部分专家过载，部分空闲）
- 训练需要额外的负载均衡损失
- 实现复杂

**代表**：Kimi K3（K2 曾为 384 专家）、GPT-5.6（推测）、Qwen3.8-Max

## 路由策略

### Top-k 路由

最简单：对每个 token，选分数最高的 k 个专家。

```
scores = softmax(router(token))
top_k_scores = top_k(scores, k)
output = sum(top_k_scores[i] * expert[i] for i in top_k)
```

### Shared Expert + Routed Expert 双轨

**DeepSeek-V3 / Kimi K2 的设计**：

- **Shared Expert**：始终激活，学通用知识
- **Routed Expert**：参与 top-k 路由，学专业知识

**好处**：shared expert 保证基础能力，routed expert 学习差异化。

## 负载均衡

**问题**：router 可能倾向选少数专家，导致其他专家"饿死"。

**解法**：辅助损失（Load Balancing Loss）

```
L_balance = α * sum((f_i - 1/N)²)
```

其中 f_i 是专家 i 处理的 token 比例，N 是专家数。**惩罚偏离均匀分布**。

## 容量因子

每个专家最多处理的 token 数 = 总 token × (1/N) × capacity_factor。

**capacity_factor = 1.0**：每个专家处理相等份额
**capacity_factor = 1.5**：允许 50% 的弹性

超过容量的 token 会被丢弃（drop token）——这是 MoE 的一个潜在问题。

## 各家选择

| 厂商 | 模型 | 架构 | 专家数 | 激活数 |
|------|------|------|--------|--------|
| Anthropic | Claude | Dense（推测） | — | 全参 |
| OpenAI | GPT-5.6 | MoE（推测） | 未公开 | 未公开 |
| Moonshot | Kimi K3 | MoE | 未公开 | 未公开 |
| Zhipu | GLM-5.2 | MoE | 未公开 | 未公开 |
| Qwen | Qwen3.8-Max | MoE | 未公开 | 未公开 |

> Kimi K2（2025 年）曾以 384 专家 / 激活 8 的激进 MoE 设计著称，K3 具体参数未公开。

**趋势**：2026 年 MoE 成为主流，只剩 Anthropic 等少数厂商坚持 dense。

## 常见坑

**MoE ≠ 更好**

MoE 在推理效率上有优势，但路由调优复杂，训练不稳定。Dense 在小模型上仍然是好选择。

**专家数不是越多越好**

384 专家（Kimi K2）是极端设计，路由难度大。大多数模型用 8-64 专家。

## 参考

- [Switch Transformer](https://arxiv.org/abs/2101.03961)（2021）
- [DeepSeek-V3](https://arxiv.org/abs/2412.19437)（2024）
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 下一步

- 了解长上下文技术 → [长上下文技术](./long-context)
- 了解多模态架构 → [多模态架构](./multimodal)

## 如果你想

- 看各家模型的架构选择 → [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)
- 了解推理优化 → [推理优化](../training/inference-optimization)
