---
title: 预训练与微调
description: 预训练目标、SFT、LoRA、全量微调的技术路线
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: LoRA 论文
      url: https://arxiv.org/abs/2106.09685
      accessedAt: 2026-08-13
---

# 预训练与微调

> **TL;DR**：预训练学通用知识，SFT 学指令格式，LoRA 低成本适配，全量微调深度定制。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 预训练的目标与数据
- SFT（监督微调）的作用
- LoRA vs 全量微调的选择
- 微调的常见坑

## 预训练：学通用知识

**目标**：让模型学会语言的统计规律——预测下一个 token。

**数据**：互联网文本（万亿 token 级别），涵盖代码、论文、书籍、网页等。

**训练方式**：自回归（Decoder-only）——给定前文，预测下一个 token。

```
输入：The cat sat on the
目标：mat
损失：-log P(mat | The cat sat on the)
```

**Scaling Law**：模型性能与参数量、数据量、计算量呈幂律关系。**增加任意一个都能提升性能**，但有边际递减。

## SFT：学指令格式

预训练模型只会"续写"，不会"回答问题"。SFT（Supervised Fine-Tuning）教模型按指令格式回答。

**数据格式**：

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

**SFT 不改变模型的知识**，只是教模型"怎么表达"。

## LoRA：低成本适配

全量微调需要更新所有参数（几十 GB 显存）。LoRA 只训练低秩矩阵，**显存需求降低 10-100 倍**。

**原理**：在每层添加低秩矩阵 `ΔW = BA`，其中 B 和 A 的秩远小于原始权重。

```
原始：y = Wx
LoRA：y = Wx + BAx
```

**参数效率**：

| 方法 | 可训练参数 | 显存需求 | 效果 |
|------|-----------|----------|------|
| 全量微调 | 100% | 100% | 最好 |
| LoRA | 0.1-1% | 5-10% | 接近全量 |
| QLoRA | 0.1-1% | 2-5% | 略低于 LoRA |

**适用场景**：

- 领域适配（医疗、法律、金融）
- 风格调整（语气、格式）
- 多任务适配（每个任务一个 LoRA adapter）

## 全量微调：深度定制

更新所有参数，效果最好但成本最高。

**适用场景**：

- 需要深度改变模型行为
- 数据量大（百万级样本）
- 有充足计算资源

**常见坑**：

- **过拟合**：数据量小时容易过拟合
- **灾难性遗忘**：微调后丢失预训练知识
- **成本高**：70B 模型全量微调需要数百 GPU

## 微调 vs 提示工程

| 维度 | 微调 | 提示工程 |
|------|------|----------|
| 成本 | 高（训练 + 推理） | 低（只影响推理） |
| 效果 | 深度定制 | 浅层调整 |
| 灵活性 | 需要重新训练 | 随时改提示 |
| 适用 | 大量数据 + 特定任务 | 少量示例 + 通用任务 |

**经验法则**：先试提示工程，不够再微调。

## 参考

- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)（2021）
- [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)（2020）
- [LLM 全景 · 技术架构总览](/llm-landscape/architecture)

## 下一步

- 了解对齐训练 → [RLHF 与对齐](./alignment)
- 了解数据工程 → [数据工程](../training/data-engineering)

## 如果你想

- 看各家模型的微调方案 → [LLM 全景 · 选型决策树](/llm-landscape/selection-guide)
- 动手微调 → [Cookbook](/cookbook/)
