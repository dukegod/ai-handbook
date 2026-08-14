---
title: 重要论文速递
description: 论文追踪方法论——arXiv 怎么追、筛选标准、已收录论文清单
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-14
verifiedWith:
  sources:
    - name: arXiv
      url: https://arxiv.org
      accessedAt: 2026-08-14
    - name: Attention Is All You Need
      url: https://arxiv.org/abs/1706.03762
      accessedAt: 2026-08-14
    - name: DeepSeek-R1
      url: https://arxiv.org/abs/2501.12948
      accessedAt: 2026-08-14
---

# 重要论文速递

> **TL;DR**：论文速递不是「读所有热门论文」，是「从几百篇里捞出值得花时间的 2-3 篇」。本文给筛选漏斗与已收录锚点。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 用筛选漏斗在 arXiv 噪音里捞论文
- 判断一篇论文值不值得深读的 4 个问题
- 已收录论文清单（可作入门路径）

## 一、筛选漏斗（三层）

**第一层 — 自动过滤**：只看高引 / 热门榜单（Hugging Face Papers、arXiv 热度榜），排除「重复工作型」论文。

**第二层 — 5 分钟判读**：读摘要 + 图表，回答：

1. 它解决了什么问题？
2. 相对已知方案的新点是什么？
3. 结果有没有公开代码 / 权重？
4. 与我的工作有没有关系？

**第三层 — 深读**：只有第 2、3、4 问都通过才完整读。

## 二、值得关注的论文类型

| 类型 | 信号 | 例子 |
| --- | --- | --- |
| 架构新范式 | 后续被大量引用、复现 | Transformer |
| 训练方法突破 | 成本 / 效果显著改善 | InstructGPT |
| 开源权重 + 强效果 | 社区立刻下载复现 | DeepSeek-R1 |
| 效率技术 | 推理 / 微调变便宜 | LoRA |

> 与架构原理的对应讲解见 [AI 核心技术](/ai-core/)。

## 三、已收录论文锚点

| 论文 | 时间 | 意义 | 对应本站 |
| --- | --- | --- | --- |
| Attention Is All You Need | 2017 | Transformer 奠基 | [Transformer](/ai-core/fundamentals/transformer) |
| BERT | 2018 | 预训练 + 微调范式 | [预训练](/ai-core/fundamentals/pretraining) |
| LoRA | 2021 | 高效微调，成本大降 | [训练与推理](/ai-core/) |
| InstructGPT | 2022 | RLHF 落地，对齐成为标配 | [对齐](/ai-core/fundamentals/alignment) |
| Mixtral | 2024 | MoE 架构开源化 | [稠密 vs MoE](/ai-core/model-arch/dense-vs-moe) |
| DeepSeek-R1 | 2025-01 | 开源推理模型追平闭源 | [推理模型](/ai-trends/product-updates/china) |

> ⚠️ 锚点用于学习路径，非「最新速递」。每周更新部分请自行按第一节漏斗筛。

## 四、如何跟踪

1. **工具**：arXiv 订阅（关键词：LLM、RLHF、MoE、Agent、MCP）、Hugging Face Papers 每日榜单
2. **节奏**：双周一次筛选，一次 30 分钟足够
3. **记录**：按上面 4 个问题写两行笔记，比收藏链接有用

## 参考

- [arXiv](https://arxiv.org)（访问于 2026-08-14）
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)（访问于 2026-08-14）
- [DeepSeek-R1 论文](https://arxiv.org/abs/2501.12948)（访问于 2026-08-14）

## 下一步

- 看能直接上手的开源项目 → [开源项目推荐](/ai-trends/research-highlights/open-source)
- 理解论文背后的原理 → [AI 核心技术](/ai-core/)

## 如果你想

- 补架构基础 → [Transformer 原理](/ai-core/fundamentals/transformer)
- 看训练方法 → [预训练与对齐](/ai-core/fundamentals/pretraining)
- 追踪行业大势 → [行业趋势](/ai-trends/industry/trends)
