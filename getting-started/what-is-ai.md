---
title: 什么是 AI
description: 从符号 AI 到生成式 AI——一次 60 年的快速历史散步，理解当前这波浪潮为什么不同
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: Generative Adversarial Networks
      url: https://arxiv.org/abs/1406.2661
      accessedAt: 2026-09-30
    - name: Attention Is All You Need
      url: https://arxiv.org/abs/1706.03762
      accessedAt: 2026-09-30
    - name: Training Compute-Optimal Large Language Models
      url: https://arxiv.org/abs/2203.15556
      accessedAt: 2026-09-30
    - name: Are Emergent Abilities of Large Language Models a Mirage?
      url: https://arxiv.org/abs/2304.15004
      accessedAt: 2026-09-30
---

# 什么是 AI

> **一句话**：AI（Artificial Intelligence，人工智能）是让机器完成"需要智能才能做"的任务的科学。当前这波浪潮的主角是**生成式 AI**。

## 一、三次浪潮，一次看懂

| 应用重心 | 大致活跃时期 | 代表技术 | 能做什么 | 局限 |
| --- | --- | --- | --- | --- |
| **符号 AI** | 1950s–1980s | 专家系统、规则引擎 | 下棋、证明定理 | 规则写不完，遇到"常识"就崩 |
| **数据驱动学习** | 1990s 起持续发展 | 机器学习、深度学习 | 分类、预测，也可生成内容 | 依赖训练数据，跨场景表现可能下降 |
| **生成式 AI 广泛应用** | 2020s 起加速普及 | 大语言模型（LLM）、扩散模型 | 对话、写代码、画图、生成视频 | 会生成看似可信但错误的内容 |

> 这是按应用重心整理的地图，各条技术路线长期并存。**生成式模型早已存在**，例如 2014 年的 GAN；当前变化在于生成质量、通用性和交互体验的提升。AI 也仍广泛用于预测、推荐和控制。

## 二、理解生成式 AI 的三个视角

**大语言模型（LLM）** —— 从语言数据中学习，可用于对话、写作、总结、编程。GPT、Claude 是模型系列；ChatGPT 是使用模型并集成工具的产品。**公司、模型、产品不是同一层概念**。

**多模态模型** —— 能处理文本、图片、音频、视频中的多种类型，不要求四种都支持。**多模态输入 ≠ 多模态生成**：能看懂图片的模型不一定能画图。

**生成式媒体模型** —— 面向图像、视频、音频等内容生成，例如根据描述画图或合成语音。它与前两类可以重叠，不是互斥分类。

## 三、为什么是现在

大语言模型并不是 2022 年才出现的新物种，而是三条曲线的交汇：

1. **算力**：GPU 集群支持更大规模的训练与推理
2. **数据**：互联网积累了海量文本语料
3. **算法**：Transformer 架构（2017）提高了序列任务的训练并行性；后续训练与工程方法持续改进

**参数更多不保证模型更强**。Chinchilla 研究表明，参数量与训练数据量需要在给定计算预算下匹配。某些评测中的能力跃升被称为“涌现”，但其表现也受评测指标影响，不能仅凭规模认定因果。

## 关键洞察

- **AI 的范围比生成式 AI 更广**——识别、预测、推荐等能力仍有价值
- **模型与产品分开理解**——产品还可能集成搜索、文件处理和外部工具
- **用任务结果判断能力**——不要只看参数、版本号或演示效果；产品变化见 [产品动向](/ai-trends/)

## 参考

- [Generative Adversarial Networks](https://arxiv.org/abs/1406.2661)（生成模型历史；访问于 2026-09-30）
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)（Transformer；访问于 2026-09-30）
- [Chinchilla](https://arxiv.org/abs/2203.15556)（规模与数据配比；访问于 2026-09-30）
- [Are Emergent Abilities of Large Language Models a Mirage?](https://arxiv.org/abs/2304.15004)（涌现与评测指标；访问于 2026-09-30）
- [AI 核心技术 · 基础原理](/ai-core/fundamentals/transformer)

## 下一步

- 接着读 → [什么是大语言模型](./what-is-llm)
- 深入原理 → [Transformer 架构](/ai-core/fundamentals/transformer)

## 如果你想

- 直接看工具 → [主流 AI 产品全景](./ai-tools-landscape)
- 看行业趋势 → [行业观察](/ai-trends/industry/trends)
