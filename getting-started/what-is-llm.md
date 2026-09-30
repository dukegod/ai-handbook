---
title: 什么是大语言模型
description: 非技术视角——LLM 是怎么练出来的、为什么会"思考"、为什么有时会胡说八道
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-09-30
verifiedWith:
  sources:
    - name: InstructGPT
      url: https://arxiv.org/abs/2203.02155
      accessedAt: 2026-09-30
    - name: DeepSeek-R1
      url: https://arxiv.org/abs/2501.12948
      accessedAt: 2026-09-30
    - name: Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations?
      url: https://arxiv.org/abs/2405.05904
      accessedAt: 2026-09-30
    - name: When More is Less
      url: https://arxiv.org/abs/2502.07266
      accessedAt: 2026-09-30
    - name: Training Compute-Optimal Large Language Models
      url: https://arxiv.org/abs/2203.15556
      accessedAt: 2026-09-30
---

# 什么是大语言模型

> **一句话**：大语言模型（Large Language Model，LLM）从大量语言数据中学习规律与知识。常见的生成式 LLM 通过“预测下一个 Token（词元）”预训练，再经后训练适配任务；生成得流畅不等于事实正确。

## 一、从预训练到后训练（直觉版）

**预训练：建立基础** —— 用书籍、网页、代码等数据学习语言规律、知识与部分推理能力。预测单位是 token，可能是字、词的一部分或符号，不固定等于一个单词。

**监督微调（SFT）：学习示范** —— 用高质量任务与回答示例训练模型，改善指令遵循、输出格式和任务表现。它也可能学习新知识，但不等于可靠地更新知识库；研究发现，新事实可能学得更慢并增加幻觉风险。

**偏好优化与强化学习：按反馈改进** —— 人类或 AI 的偏好可帮助改善回答行为；答案校验、代码测试等反馈可用于提升特定任务的推理表现。DeepSeek-R1 的研究展示了强化学习对推理能力的作用。

> SFT、偏好优化和强化学习都可以属于**后训练**，具体流程不一定按固定三步执行。预训练打基础，后训练也能改变能力；对齐强调行为符合目标，不是“只调整语气”。

## 二、为什么它会"思考"

常见的自回归模型逐个生成 token，已生成的内容会进入后续上下文。**思维链（Chain of Thought）**通过中间步骤分解问题，可以为复杂任务提供更多计算过程。

但**步骤更长不保证更准确**，也可能引入错误并增加成本。推理表现取决于训练方法、任务难度和推理预算，不能把推理模型理解成“普通模型多写一点草稿”。

## 三、三个重要事实

**1. 上下文不等于修改权重** —— 普通对话通常不会直接更新模型参数。模型可利用本次输入的历史信息；跨会话保存与取回资料，通常由产品的记忆机制实现。

**2. 生成与检索是两种机制** —— 单靠模型参数不能保证掌握最新事实。联网搜索依赖外部工具提供资料，模型再利用结果回答；它也可以被训练为选择何时调用工具。

**3. 流畅不代表正确** —— 训练、推理或检索中的问题都可能导致错误回答。引用、数字、新闻等应核对来源；联网也不保证无误。相关讨论见 [能力与边界](./capabilities-and-limits)。

## 四、为什么有的模型强有的弱

| 因素 | 影响 |
| --- | --- |
| 参数与数据 | 参数量、数据质量与数量、计算预算需要匹配 |
| 后训练 | 示范、偏好和奖励设计影响行为与任务能力 |
| 推理时计算 | 更多计算可能改善复杂任务，但收益并非无限或必然 |
| 产品层能力 | 联网、文件、工具调用——模型外挂，可叠加 |

选模型的方法论见 [模型选型决策树](/ai-trends/model-selection/model-selection-guide)。

## 关键洞察

- **预测机制不等于能力边界**——模型可学习知识和推理模式，输出仍需验证
- **预训练与后训练共同影响表现**——不能简单分成“学知识”和“学格式”
- **模型、上下文、工具分开看**——用相同任务比较，才能判断差异来自哪里

## 参考

- [InstructGPT](https://arxiv.org/abs/2203.02155)（指令遵循与反馈；访问于 2026-09-30）
- [DeepSeek-R1](https://arxiv.org/abs/2501.12948)（强化学习与推理；访问于 2026-09-30）
- [微调与新知识研究](https://arxiv.org/abs/2405.05904)（学习新事实的实验边界；访问于 2026-09-30）
- [When More is Less](https://arxiv.org/abs/2502.07266)（思维链长度；访问于 2026-09-30）
- [Chinchilla](https://arxiv.org/abs/2203.15556)（参数与数据配比；访问于 2026-09-30）
- [预训练与微调（技术版）](/ai-core/fundamentals/pretraining)
- [RLHF 与对齐（技术版）](/ai-core/fundamentals/alignment)

## 下一步

- 接着读 → [能力与边界](./capabilities-and-limits)
- 深入原理 → [AI 核心技术](/ai-core/)

## 如果你想

- 了解各家模型差异 → [厂商档案](/ai-trends/vendors/)
- 直接开始用 → [主流 AI 产品全景](./ai-tools-landscape)
