---
title: 预训练与微调
description: 预训练目标、SFT、LoRA、全量微调的技术路线
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: LoRA 论文
      url: https://arxiv.org/abs/2106.09685
      accessedAt: 2026-09-30
    - name: QLoRA 论文
      url: https://arxiv.org/abs/2305.14314
      accessedAt: 2026-09-30
    - name: Training Compute-Optimal Large Language Models
      url: https://arxiv.org/abs/2203.15556
      accessedAt: 2026-09-30
    - name: Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?
      url: https://arxiv.org/abs/2405.05904
      accessedAt: 2026-09-30
    - name: InstructGPT
      url: https://arxiv.org/abs/2203.02155
      accessedAt: 2026-09-30
    - name: DeepSeek-R1
      url: https://arxiv.org/abs/2501.12948
      accessedAt: 2026-09-30
---

# 预训练与微调

> **TL;DR**：预训练建立通用基础，后训练继续塑造能力与行为；SFT 是训练方法，LoRA 与全量微调是参数更新方式，可以组合使用。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 预训练的目标与数据
- SFT（监督微调）的作用
- LoRA vs 全量微调的选择
- 微调的常见坑

## 预训练：建立通用基础

**目标**：从大量数据中学习语言规律、知识与任务模式。这里以自回归语言模型的下一 token 预测为例。

**数据**：可包含代码、论文、书籍、网页等，规模与配比因模型而异。

**训练方式**：自回归（Decoder-only）——给定前文，预测下一个 token。

以下是训练目标示意，不是可运行的训练程序：

```text
输入：The cat sat on the
目标：mat
损失：-log P(mat | The cat sat on the)
```

**Scaling Law（缩放定律）**：在一定条件下，预测损失随参数、数据和计算投入的扩展呈现可拟合的规律。三者需要匹配，不能理解成增加任一项都必然变强。[Chinchilla 研究](https://arxiv.org/abs/2203.15556)展示了固定预算下平衡模型规模与训练数据的重要性。

## SFT：适配任务与行为

预训练模型可能已有问答能力，但未必稳定遵循指令。监督微调（SFT）用输入与期望输出示例训练模型，改善任务表现、格式和行为。

**数据示意**（实际字段取决于训练框架）：

```json
{
  "instruction": "解释什么是 Transformer",
  "output": "Transformer 是一种基于自注意力机制的..."
}
```

**SFT 的作用**：

- 学会指令格式（问答、对话、任务）
- 学会拒绝不当请求
- 学会输出结构化内容（JSON、Markdown）

**SFT 也可能学习新知识**，但不等于可靠地更新知识库。[一项闭卷问答研究](https://arxiv.org/abs/2405.05904)发现，新事实学得较慢，学会后还可能增加幻觉。这个实验结论不能推广为所有微调的必然结果。

后训练也包含强化学习等方法。[DeepSeek-R1](https://arxiv.org/abs/2501.12948)展示了强化学习对推理表现的提升，因此不能把后训练概括成“只改表达”。

## LoRA：低成本适配

LoRA 冻结原模型权重，训练选定层中的低秩更新矩阵，减少可训练参数及相关显存开销。节省比例取决于模型、序列长度、优化器和实现。

**原理示意**（省略缩放系数）：把权重更新写成 `ΔW = BA`，用较小的中间维度限制更新矩阵的秩。

```text
原始：y = Wx
LoRA：y = Wx + BAx
```

**参数效率**：

| 方法 | 更新范围 | 主要取舍 |
|------|----------|----------|
| 全量微调 | 全部模型参数 | 调整空间大，训练资源需求通常更高 |
| LoRA | 低秩更新矩阵 | 减少训练与存储开销，效果需按任务评估 |
| QLoRA | 量化底座上的 LoRA 参数 | 进一步压缩底座显存，需评估量化与实现影响 |

LoRA 与 QLoRA 论文均在部分实验中获得接近或匹配全量微调的效果，不能据此排出固定的效果顺序。

**适用场景**：

- 领域适配（医疗、法律、金融）
- 风格调整（语气、格式）
- 多任务适配（每个任务一个 LoRA adapter）

## 全量微调：深度定制

更新所有参数，适合需要更广泛调整模型、且资源预算允许的情况；不保证优于 LoRA。

**适用场景**：

- 需要深度改变模型行为
- 有足够覆盖目标任务的高质量数据
- 有充足计算资源

**常见坑**：

- **过拟合**：数据量小时容易过拟合
- **灾难性遗忘**：原有任务表现可能退化，需要保留回归评估
- **资源不足**：显存与训练时长还取决于精度、序列长度和训练配置

## 微调 vs 提示工程

| 维度 | 微调 | 提示工程 |
|------|------|----------|
| 成本 | 增加训练与模型维护成本 | 无训练成本，长提示可能增加推理成本 |
| 调整对象 | 模型参数 | 本次输入与上下文 |
| 灵活性 | 需要重新训练 | 随时改提示 |
| 适用 | 有训练样本的重复任务 | 快速尝试指令、示例与上下文 |

**经验法则**：先试提示工程，不够再微调。

## 参考

- [LoRA](https://arxiv.org/abs/2106.09685)（访问于 2026-09-30）
- [QLoRA](https://arxiv.org/abs/2305.14314)（访问于 2026-09-30）
- [Chinchilla：计算预算下的规模分配](https://arxiv.org/abs/2203.15556)（访问于 2026-09-30）
- [微调与新知识研究](https://arxiv.org/abs/2405.05904)（访问于 2026-09-30）
- [InstructGPT](https://arxiv.org/abs/2203.02155)（访问于 2026-09-30）
- [DeepSeek-R1](https://arxiv.org/abs/2501.12948)（访问于 2026-09-30）
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 下一步

- 了解对齐训练 → [RLHF 与对齐](./alignment)
- 了解数据工程 → [数据工程](../training/data-engineering)

## 如果你想

- 看各家模型的微调方案 → [模型选型决策树](/ai-trends/model-selection/model-selection-guide)
- 动手微调 → [Cookbook](/cookbook/)
