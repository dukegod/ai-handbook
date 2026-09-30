---
title: RLHF 与对齐
description: 从人类反馈中学习——RLHF / DPO / Constitutional AI / RLVR
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: InstructGPT
      url: https://arxiv.org/abs/2203.02155
      accessedAt: 2026-09-30
    - name: DPO 论文
      url: https://arxiv.org/abs/2305.18290
      accessedAt: 2026-09-30
    - name: Constitutional AI
      url: https://arxiv.org/abs/2212.08073
      accessedAt: 2026-09-30
    - name: DeepSeekMath
      url: https://arxiv.org/html/2402.03300v3
      accessedAt: 2026-09-30
    - name: DeepSeek-R1
      url: https://arxiv.org/html/2501.12948v1
      accessedAt: 2026-09-30
---

# RLHF 与对齐

> **TL;DR**：对齐训练改善模型与人类意图的一致性。RLHF、DPO、RLVR 等描述的维度不同，并非依次替代的三代技术；后训练也能提升特定任务的推理表现。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- RLHF 的典型流程
- DPO 如何简化 RLHF
- Constitutional AI 的独特思路
- RLVR 与 GRPO 如何配合

## 为什么需要对齐

预训练模型的问题：

- **指令遵循不稳定**：可能已有问答能力，但也可能把问题续写成更多问题
- **可能有害**：互联网数据包含有害内容
- **可控性有限**：输出格式、长度或风格可能不符合要求

**对齐的目标**：让模型有用（helpful）、无害（harmless）、诚实（honest）——简称 HHH。

## 反馈来源与优化方法

### RLHF：从人类反馈中学习

以 [InstructGPT](https://arxiv.org/abs/2203.02155) 为例：

1. **SFT**：用期望回答的示例微调预训练模型
2. **训练 Reward Model**：人类对比两个回答，标注哪个更好
3. **PPO 优化**：用 reward model 的分数作为奖励，用 PPO 算法优化策略

PPO（近端策略优化）是强化学习算法。训练成本和稳定性取决于具体配置，不能用固定模型数量概括所有 RLHF 实现。

### DPO：直接优化偏好

**核心思想**：用“更偏好／较不偏好”的回答对直接训练模型，原始方法无需单独训练奖励模型，也无需在微调期间反复在线采样。

这简化了训练流程，但效果仍取决于偏好数据与配置；[原论文](https://arxiv.org/abs/2305.18290)中的结果不是对所有任务的保证。

### RLVR：用可验证结果作为奖励

**核心思想**：通过规则、答案校验或程序测试获得奖励，适合能自动验证结果的任务。

- 数学题：有标准答案时，检查最终答案
- 代码题：执行预设测试，检查是否通过

[DeepSeek-R1-Zero](https://arxiv.org/html/2501.12948v1)采用规则奖励与 GRPO 训练，展示了推理表现的提升。奖励答案正确不代表每步推理都正确，也不意味着输出越长越准。

### GRPO：一种强化学习优化算法

[DeepSeekMath](https://arxiv.org/html/2402.03300v3)提出 GRPO：对同一问题采样多个回答，以组内奖励估计基线，省去单独训练价值模型。GRPO 回答“如何更新模型”，RLVR 回答“奖励从哪里来”，二者可以组合。

## Constitutional AI：Anthropic 的独特路线

Anthropic 的 Constitutional AI 用一组人类制定的原则指导 AI 反馈，减少对有害输出的人类标注需求。

**流程**：

1. 模型根据原则批评并修改回答，再用修改后的示例做监督微调
2. 模型比较回答，生成偏好数据并训练偏好模型
3. 以偏好模型提供的奖励进行强化学习，即 RLAIF（AI 反馈强化学习）

**原则示意**：

- 回答应该有用、诚实、无害
- 不应该帮助非法活动
- 不应该生成有害内容

人类仍需制定原则、设计评估并检查效果，AI 反馈也可能带有偏差。

## 对齐方法对比

| 方法 | 主要维度 | 阅读时关注 |
|------|----------|------------|
| RLHF | 人类反馈 | 人类偏好如何收集并转为训练信号 |
| RLAIF | AI 反馈 | 评判模型与原则是否可靠 |
| DPO | 偏好优化方法 | 回答对的质量与覆盖范围 |
| GRPO | 强化学习优化算法 | 组内比较与奖励设计 |
| RLVR | 可验证奖励 | 验证器能检查什么、会漏掉什么 |

这些方法覆盖不同维度，不能仅凭名称推断某款产品的完整训练流程。

## 常见坑

**对齐 ≠ 安全**

对齐训练让模型"倾向于"遵循规则，但不是"保证"。Jailbreak 仍然可能。

**过度对齐**

过度对齐会导致模型过于保守，拒绝合理请求。

**偏好数据质量**

RLHF/DPO 依赖偏好数据质量；RLVR 也受限于验证器。应同时评估目标任务与原有能力，避免只追逐训练奖励。

## 参考

- [InstructGPT](https://arxiv.org/abs/2203.02155)（访问于 2026-09-30）
- [DPO](https://arxiv.org/abs/2305.18290)（访问于 2026-09-30）
- [Constitutional AI](https://arxiv.org/abs/2212.08073)（访问于 2026-09-30）
- [DeepSeekMath](https://arxiv.org/html/2402.03300v3)（访问于 2026-09-30）
- [DeepSeek-R1](https://arxiv.org/html/2501.12948v1)（访问于 2026-09-30）
- [跨厂商架构路线](/ai-core/model-arch/architecture-landscape)

## 下一步

- 了解模型架构选择 → [Dense vs MoE](../model-arch/dense-vs-moe)
- 了解推理优化 → [推理优化](../training/inference-optimization)

## 如果你想

- 看各家模型的对齐方法 → [厂商档案 · Anthropic](/ai-trends/vendors/anthropic/)
- 了解提示工程 → [Claude 能力 · 提示工程](/claude-capabilities/prompting/best-practices)
