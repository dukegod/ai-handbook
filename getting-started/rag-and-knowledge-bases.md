---
title: RAG 与知识库
description: 用团队文档助手理解检索增强生成、向量检索及它与微调的区别
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
      url: https://arxiv.org/abs/2005.11401
      accessedAt: 2026-09-30
    - name: Sentence-BERT
      url: https://arxiv.org/abs/1908.10084
      accessedAt: 2026-09-30
    - name: 'Sentence Transformers Retrieve & Re-Rank'
      url: https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html
      accessedAt: 2026-09-30
    - name: Azure AI Search RAG overview
      url: https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview
      accessedAt: 2026-09-30
    - name: Azure AI Search security filters
      url: https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search
      accessedAt: 2026-09-30
---

# RAG 与知识库

> **一句话**：RAG 先找资料，再让模型根据资料回答；可靠性取决于检索与证据。

## 你能在这里学到

- 知识库怎样为模型提供资料
- 嵌入、分块、向量检索与重排各做什么
- 什么时候用 RAG，什么时候考虑微调

## 前置知识

- [Token、上下文与记忆](./tokens-context-memory)
- [工具调用](./tool-calling)

## 一、先查资料，再组织回答

**RAG（检索增强生成）**把检索到的资料交给生成模型，帮助它回答依赖外部知识的问题。“知识库”通常包含原始资料、可检索的索引，以及来源、版本和权限等信息；它不等于模型已经记住了所有文档。

以下为**虚构的团队文档助手示例，未运行实测**。用户问：“项目发布前要做什么？”资料中有《项目发布流程》v2：“完成回归检查，由发布负责人确认后上线。”助手应找到当前适用版本，再说明步骤并标出文档与段落出处。

```mermaid
flowchart LR
  A[用户问题] --> B[检索有权访问的资料]
  B --> C[选取适用版本并按需重排]
  C --> D[把相关片段放入上下文]
  D --> E[依据资料回答并标出处]
```

如果资料不够，应说明缺少什么，不能补造发布规则。这个流程体现了 [RAG](https://arxiv.org/abs/2005.11401)结合模型能力与外部资料的思路。

## 二、几个检索术语分别做什么

1. **分块（Chunking）**：把长文档拆成可检索片段。例如保留“发布前检查”这一节，并带上标题、版本与来源；切得太碎可能丢掉适用条件。
2. **Embedding（嵌入）**：把文本转换为一组数字，便于比较语义。[Sentence-BERT](https://arxiv.org/abs/1908.10084)是学习句子嵌入的一种方法。
3. **向量检索**：比较问题与片段的嵌入，找到语义接近的候选资料。“上线检查”可能匹配“发布前检查”，但相近不代表事实正确，也不代表版本适用。
4. **重排（Reranking）**：对候选片段再按与问题的相关程度排序，挑出更有用的内容。它是可选步骤，不能找回第一轮漏掉的资料。[官方示例](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)展示了这种先检索再重排的分工。

RAG 不要求一定用向量数据库，也能用关键词、数据库查询或多种检索方式组合。最终提供给模型的通常是可阅读的资料片段，而不只是相似度分数。

## 三、Prompt、RAG、微调怎么选

| 方法 | 主要改什么 | 何时考虑 |
| --- | --- | --- |
| Prompt（提示词） | 本次指令、示例与上下文 | 先明确任务；短资料可直接附在问题里 |
| RAG | 可检索资料及送入上下文的证据 | 文档多、经常更新，或需要逐条追溯来源 |
| 微调 | 模型参数 | 有高质量训练样本，希望稳定适配任务或输出行为 |

三者可以组合：用微调适配回答风格，用 RAG 查发布流程，再用提示词要求列出处。**查询时检索不会自动更新模型权重**；检索器或生成模型可以另行训练，但这不是每次查询的必需步骤。

## 四、怎样判断它真的有用

先用几条已知答案的问题检查整个过程，而不只看回答是否流畅：

- **漏检**：发布审批条件没有找到，就可能漏掉必要步骤。
- **过期**：新版原文已更新，索引还停在旧版，需要同步更新和失效处理。
- **权限**：系统应根据用户身份限制可检索内容，在资料进入模型前执行权限检查，不能只写一句“不要泄露”。[权限过滤示例](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search)
- **引用不支持结论**：有出处仍可能曲解原文，应检查对应段落是否真的支持每项要求。

**资料找对、版本适用、回答有依据**，才能说明知识库帮助解决了问题。

## 参考

- [RAG 原论文](https://arxiv.org/abs/2005.11401)（访问于 2026-09-30）
- [Sentence-BERT 原论文](https://arxiv.org/abs/1908.10084)（访问于 2026-09-30）
- [Sentence Transformers：检索与重排](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)（访问于 2026-09-30）
- [Microsoft：RAG 的检索、资料准备与边界](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview)（访问于 2026-09-30）
- [Microsoft：按用户身份过滤检索结果](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search)（访问于 2026-09-30）

## 下一步

- 继续读 → [Agent 与 Workflow](./agents-and-workflows)

## 如果你想

- 理解训练如何改变模型 → [预训练与微调](/ai-core/fundamentals/pretraining)
- 学习验证效果 → [评估方法论](/ai-core/eval/methodology)
