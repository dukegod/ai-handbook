---
title: Token、上下文与记忆
description: '分清模型处理的单位、单次可见信息与跨会话保存机制'
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: Hugging Face Tokenization algorithms
      url: https://huggingface.co/docs/transformers/tokenizer_summary
      accessedAt: 2026-09-30
    - name: Context windows
      url: https://platform.claude.com/docs/en/build-with-claude/context-windows
      accessedAt: 2026-09-30
    - name: LangChain Memory overview
      url: https://docs.langchain.com/oss/python/concepts/memory
      accessedAt: 2026-09-30
    - name: Lost in the Middle
      url: https://arxiv.org/abs/2307.03172
      accessedAt: 2026-09-30
---

# Token、上下文与记忆

> **一句话**：Token 是计量单位，上下文是本次可用信息，应用记忆负责保存与取回。

## 你能在这里学到

- 为什么 token 不等于字数
- 为什么聊天记录还在，模型却可能没看到
- 模型知识、上下文与应用记忆的区别

## 前置知识

- [什么是大语言模型](./what-is-llm)

## 一、Token：模型处理文本的单位

分词器把文本转成 token 序列。一个 token 可能对应一个词、词的一部分或字符；不同分词器对同一文本的结果也可能不同。因此不能用固定的“一个汉字等于几个 token”推算所有模型。

想判断一份资料能否放进去，应使用目标模型对应的计数工具。图片、音频等输入的计量规则另看产品说明，不能直接按文本字数估算。

## 二、上下文：本次调用真正拿到什么

上下文可能包含系统要求、用户问题、选入的历史消息、文档片段与工具结果。**界面上能翻到的聊天记录，不一定全部进入本次调用。** 应用可能已经做了截断、筛选或摘要。

上下文窗口是模型单次处理长度的上限。很多生成接口由输入与生成输出共享总预算，还要留意思考内容等如何计入；具体口径按模型文档确认。

可以把它想成书桌：书库再大，一次放到桌上的资料也有限。窗口大代表“能放更多”，不保证“都用得好”。[Lost in the Middle](https://arxiv.org/abs/2307.03172) 在所测试的模型与任务上发现，信息所处位置会影响表现，不能把容量当成理解质量。

## 三、三种“记得”

| 层次 | 信息在哪里 | 如何变化 |
| --- | --- | --- |
| 模型知识 | 训练得到的参数 | 通常通过训练更新 |
| 当前上下文 | 本次提供的信息 | 每次调用可重新组织 |
| 应用记忆 | 保存的记录、摘要或资料库 | 应用写入、检索、更新或删除 |

普通对话通常不会直接改写模型参数。跨会话记忆需要应用保存并在合适时取回；**保存成功不等于每次都会被取回，更不保证保存的内容正确。**

## 四、贯穿例子：团队文档助手

以下是虚构场景，不代表实测结果。

你询问“项目 A 发布前要检查什么”：

1. 应用取出适用版本的发布规范与当前问题，组成上下文。
2. 助手根据本次拿到的资料起草检查清单。
3. 下次再问时，应用可以取回清单，但仍需检查规范版本是否变化。

把所有旧聊天都塞进去，可能引入过期要求；把聊天压成摘要，也可能丢掉例外条件。应优先保留当前目标、关键事实、来源与未解决问题，必要时回查原文。

## 五、怎么选

- 资料少且相关：直接提供上下文即可。
- 资料多、持续更新：考虑先检索再提供，见 [RAG 与知识库](./rag-and-knowledge-bases)。
- 需要跨会话延续任务：保存关键状态，并明确何时取回、更新与删除。
- 仅仅想让模型“记住新事实”：先区分资料管理需求与训练需求，别直接跳到微调。

## 参考

- [Hugging Face：分词算法](https://huggingface.co/docs/transformers/tokenizer_summary)（访问于 2026-09-30）
- [Claude：上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows)（接口示例；访问于 2026-09-30）
- [LangChain：记忆概览](https://docs.langchain.com/oss/python/concepts/memory)（应用记忆示例；访问于 2026-09-30）
- [Lost in the Middle](https://arxiv.org/abs/2307.03172)（访问于 2026-09-30）

## 下一步

- 看模型如何取得外部结果 → [工具调用](./tool-calling)

## 如果你想

- 深入长上下文技术 → [长上下文技术](/ai-core/model-arch/long-context)
- 了解训练如何改变参数 → [预训练与微调](/ai-core/fundamentals/pretraining)
