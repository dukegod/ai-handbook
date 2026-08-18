---
title: 量化与蒸馏
description: INT8/INT4 量化、知识蒸馏、模型压缩实践
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: GPTQ 论文
      url: https://arxiv.org/abs/2210.17323
      accessedAt: 2026-08-13
    - name: AWQ 论文
      url: https://arxiv.org/abs/2306.00978
      accessedAt: 2026-08-13
---

# 量化与蒸馏

> **TL;DR**：量化把 FP16 压到 INT8/INT4，显存减半/减四分之一。蒸馏把大模型知识转移到小模型。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 量化的原理与方法
- GPTQ / AWQ / GGUF 的区别
- 知识蒸馏的流程
- 端侧部署的量化策略

## 量化：精度换显存

**原理**：把模型权重从 FP16（16 位浮点）压缩到 INT8（8 位整数）或 INT4（4 位整数）。

**效果**：

| 精度 | 显存 | 速度 | 质量 |
|------|------|------|------|
| FP16 | 100% | 基准 | 最好 |
| INT8 | 50% | 1.5-2x | 接近 FP16 |
| INT4 | 25% | 2-3x | 略有损失 |

## 量化方法

### 训练后量化（PTQ）

模型训练完成后直接量化，无需重新训练。

**GPTQ**（2022）：

- 逐层量化，用 Hessian 矩阵补偿误差
- 支持 INT4/INT3
- 质量损失小

**AWQ**（2023）：

- 保护重要权重（1%），其余量化
- 比 GPTQ 更快，质量相当
- 2026 年主流

### 量化感知训练（QAT）

训练时就模拟量化效果，让模型适应低精度。

**优势**：质量损失最小。

**劣势**：需要重新训练，成本高。

## GGUF：端侧格式

**GGUF**（GPT-Generated Unified Format）是 llama.cpp 的量化格式：

- 支持多种量化级别（Q4_K_M / Q5_K_M / Q8_0 等）
- CPU/端侧推理优化
- 社区广泛支持

**常见量化级别**：

| 级别 | 大小（70B） | 质量 | 适用 |
|------|------------|------|------|
| Q4_K_M | ~40 GB | 好 | 端侧首选 |
| Q5_K_M | ~48 GB | 很好 | 质量优先 |
| Q8_0 | ~70 GB | 接近 FP16 | 显存充足 |

## 知识蒸馏

**原理**：用大模型（教师）的输出训练小模型（学生）。

**流程**：

1. 教师模型对训练数据生成软标签（概率分布）
2. 学生模型用软标签训练
3. 学生模型学习教师的"知识"，但参数量小得多

**效果**：7B 学生可以学到 70B 教师 80% 的能力。

**Qwen 的全尺寸蒸馏**：从 110B 蒸馏到 0.5B/1.5B/7B/14B/32B/72B，每个尺寸都经过专门优化。

## 端侧部署

**需求**：手机/PC 上运行大模型，显存有限。

**方案**：

| 方案 | 平台 | 模型 | 量化 |
|------|------|------|------|
| llama.cpp | CPU/通用 | LLaMA/Qwen | GGUF Q4 |
| MLX | Apple Silicon | LLaMA/Qwen | FP16/INT4 |
| Ollama | 通用 | 多种 | GGUF |
| MLC | 移动端 | 多种 | INT4 |

**Qwen 3-0.5B/1.5B 是端侧首选**——专为端侧优化，INT4 量化后可在手机运行。

## 常见坑

**量化 ≠ 免费**

INT4 量化会损失 1-3% 的基准分数。需要在显存和质量间权衡。

**量化不适用于所有层**

某些层（如注意力层）对量化敏感，需要特殊处理。

**蒸馏需要好的教师**

教师模型质量差，学生也学不好。

## 参考

- [GPTQ: Accurate Post-Training Quantization](https://arxiv.org/abs/2210.17323)（2022）
- [AWQ: Activation-aware Weight Quantization](https://arxiv.org/abs/2306.00978)（2023）
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 下一步

- 了解基准测试 → [基准测试](../eval/benchmarks)
- 了解评估方法论 → [评估方法论](../eval/methodology)

## 如果你想

- 看各家模型的量化方案 → [5 厂商横向对比](/ai-trends/model-selection/model-comparison)
- 端侧部署 Qwen → [Qwen · 阿里通义千问全系](/ai-trends/cn-vendors/qwen/)
