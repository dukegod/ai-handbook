---
title: RLHF 与对齐
description: 从人类反馈中学习——RLHF / DPO / Constitutional AI / RLVR
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  sources:
    - name: InstructGPT
      url: https://arxiv.org/abs/2203.02155
      accessedAt: 2026-08-13
    - name: DPO 论文
      url: https://arxiv.org/abs/2305.18290
      accessedAt: 2026-08-13
    - name: Constitutional AI
      url: https://www.anthropic.com/research/constitutional-ai
      accessedAt: 2026-08-13
---

# RLHF 与对齐

> **TL;DR**：预训练模型只会"续写"，对齐训练教它"有用、无害、诚实"。RLHF → DPO → RLVR 是三代演进。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- RLHF 的完整流程
- DPO 如何简化 RLHF
- Constitutional AI 的独特思路
- RLVR 为什么成为推理模型核心

## 为什么需要对齐

预训练模型的问题：

- **会续写，不会回答**：给一个问题，它可能续写成更多问题
- **可能有害**：互联网数据包含有害内容
- **不可控**：输出格式、长度、风格都不稳定

**对齐的目标**：让模型有用（helpful）、无害（harmless）、诚实（honest）——简称 HHH。

## RLHF：三代演进

### 第一代：RLHF（2022）

**流程**：

1. **SFT**：用指令数据微调预训练模型
2. **训练 Reward Model**：人类对比两个回答，标注哪个更好
3. **PPO 优化**：用 reward model 的分数作为奖励，用 PPO 算法优化策略

**问题**：需要 4 个模型（policy / ref / reward / value），训练不稳定。

### 第二代：DPO（2023）

**核心思想**：去掉 reward model，直接用偏好数据优化策略。

```
损失 = -log σ(β · log(π(y_w)/π_ref(y_w)) - β · log(π(y_l)/π_ref(y_l)))
```

**优势**：只需 2 个模型（policy / ref），训练更稳定。

**DPO 是 2023-2025 年主流**——LLaMA 3、Mistral 都用 DPO。

### 第三代：RLVR（2024-2026）

**核心思想**：用可验证奖励替代人类偏好。

- 数学题：答案对错 → 奖励 1/0
- 代码题：单测通过率 → 奖励 0-1
- 逻辑题：推理步骤正确性 → 奖励

**RLVR 是 o-series / K2 Thinking 的核心**——"想得更久 = 答得更准"的基础。

## Constitutional AI：Anthropic 的独特路线

Anthropic 的 Constitutional AI 用"宪法"原则替代人类标注：

**流程**：

1. 让模型自评回答是否符合"宪法"原则
2. 用自评结果训练 reward model
3. 用 RLAIF（AI 反馈）优化策略

**宪法原则示例**：

- 回答应该有用、诚实、无害
- 不应该帮助非法活动
- 不应该生成有害内容

**优势**：不需要大量人类标注，可扩展性更强。

## 对齐方法对比

| 方法 | 奖励来源 | 模型数量 | 训练稳定性 | 代表 |
|------|----------|----------|-----------|------|
| RLHF | 人类偏好 | 4 | 不稳定 | InstructGPT |
| DPO | 人类偏好 | 2 | 稳定 | LLaMA 3 / Mistral |
| RLAIF | AI 反馈 | 2 | 稳定 | Claude 全系 |
| GRPO | 组内相对 | 1 | 稳定 | DeepSeek |
| RLVR | 可验证 | 2 | 稳定 | o-series / K2 Thinking |

## 常见坑

**对齐 ≠ 安全**

对齐训练让模型"倾向于"遵循规则，但不是"保证"。Jailbreak 仍然可能。

**过度对齐**

过度对齐会导致模型过于保守，拒绝合理请求。

**偏好数据质量**

RLHF/DPO 的效果取决于偏好数据质量。垃圾数据 → 垃圾模型。

## 参考

- [InstructGPT](https://arxiv.org/abs/2203.02155)（2022）
- [DPO: Direct Preference Optimization](https://arxiv.org/abs/2305.18290)（2023）
- [Constitutional AI](https://www.anthropic.com/research/constitutional-ai)
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 下一步

- 了解模型架构选择 → [Dense vs MoE](../model-arch/dense-vs-moe)
- 了解推理优化 → [推理优化](../training/inference-optimization)

## 如果你想

- 看各家模型的对齐方法 → [厂商档案 · Anthropic](/ai-trends/vendors/anthropic/)
- 了解提示工程 → [Claude 能力 · 提示工程](/claude-capabilities/prompting/best-practices)
