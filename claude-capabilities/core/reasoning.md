---
title: 推理能力
description: Claude 的推理特性与提示技巧；何时该显式让 Claude "想"、何时直接答
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 订正 Extended Thinking / effort 口径（官方 thinking / effort / extended-thinking 文档同日复核）：当前 4 型号全部走 adaptive，thinking.enabled / budget_tokens 一律 400，思考深度由 output_config.effort 控；CLI 相关断言沿用 2026-08 的记录（当时基于 Claude Code 2.1.220），示例未在本机重跑'
  claudeCode: 2.1.220
  model: claude-opus-5-5
  promptEngineering: 'https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-prompts'
  extendedThinking: 'https://platform.claude.com/docs/en/build-with-claude/extended-thinking'
  thinking: 'https://platform.claude.com/docs/en/build-with-claude/thinking'
  effort: 'https://platform.claude.com/docs/en/build-with-claude/effort'
  accessedAt: 2026-08-06
---

# 推理能力

> **TL;DR**：Claude 默认会做"内部推理"（chain-of-thought），**不需要**显式 prompt 也能给好答案；但**复杂任务**（多步决策、规划、debug）显式让 Claude "think step by step" 能让准确率提升 10-30%。本文讲**何时**该显式触发 + 提示技巧，机制本身见 [Extended Thinking](/claude-capabilities/core/extended-thinking)。
>
> **当前 4 型号的 thinking 都是 adaptive**——想让 Claude 多想一点，先升 effort，别急着加 `thinking` 参数。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- Claude "推理"的两层含义（隐式 CoT vs 显式 thinking）
- 何时**该**让 Claude 想、**不该**让它想
- 4 类任务的推理策略对比
- 提示技巧：5 个让 Claude "想清楚再答"的 prompt 模式
- 常见坑（过度推理、推理幻觉、推理拖时间）

## 一、Claude "推理"的两层

**第 1 层：隐式 CoT（永远在跑）**

Claude 在生成每个 token 前都会做"内部推理"——这是模型架构本身的特性，与 prompt 无关。**所以**：

```text
# 即便 prompt 不要求 "think step by step"
# Claude 也会内部"想"再答
```

**第 2 层：显式 thinking（按需触发）**

对**复杂任务**，prompt 里显式让 Claude 写出推理步骤，能大幅提升质量：

```text
请先想清楚 3 件事再给方案：
1. 这个 bug 的可能根因有哪几个
2. 哪个最值得先验证
3. 验证失败如何回退

想清楚后给一个 30 分钟内能修好的方案。
```

这两层**不冲突**——隐式 CoT 永远在跑；显式 thinking 把它"外化"为可读步骤，方便你 review、方便模型自身一致化。

## 二、何时该让 Claude 想 / 不让它想

| 任务类型 | 该显式让 Claude 想？ | 原因 |
| --- | :---: | --- |
| 简单 Q&A（"X 是什么"） | ❌ | 加 "think step by step" 反而拖时间、可能幻觉 |
| 文档总结 / 改写 | ❌ | 总结任务不需要推理 |
| 短对话 / 日常编程 | ❌ | 默认 CoT 够用 |
| **多步决策**（"选哪个方案"） | ✅ | 列前提条件、对比 trade-off 显著提高决策质量 |
| **复杂 debug** | ✅ | 避免 Claude 直接猜、漏读文件 |
| **架构设计** | ✅ | 让 Claude 先列约束、再给方案 |
| **数学 / 逻辑题** | ✅ | 显式步骤让 Claude 不跳步 |
| **长链 agent 规划** | ✅ | 每步先想清楚再动手 |

**反直觉**：**简单任务加 "think step by step" 反而掉质量**——模型在简单任务上"过度推理"会产生幻觉、绕远路、给过度复杂的答案。

## 三、5 个让 Claude 想清楚再答的 prompt 模式

### 模式 1：列前提条件再答

```text
在回答前，先列出 3 个你对这个问题的前提假设。如果任一假设不成立，告诉我哪个、并换答案。
```

**适用**：开放问题、方案选型、决策。

### 模式 2：先想 3 个反例

```text
在给方案前，先想 3 个它会失败的反例。如果你能找到任何一个，就修订方案直到无法证伪。
```

**适用**：架构决策、SLA 承诺、安全性 claim。

### 模式 3：先拆步骤再执行

```text
这是一个 5 步任务：...
请先列出你的执行计划（每步预期 30 秒内），我确认后再开始。
```

**适用**：长链 agent 任务、批量数据处理。

### 模式 4：先自我审查

```text
给出答案后，再回头审一遍——有没有不严谨的地方、是否漏了边界条件。审出任何问题立刻修订。
```

**适用**：代码生成、文档草稿、SQL 写完后自检。

### 模式 5：双视角对比

```text
请从 2 个不同视角分别思考这个问题：
1. 资深工程师视角
2. 产品经理视角

然后告诉我两个视角的共识和分歧。
```

**适用**：跨职能决策、trade-off 不明确的任务。

## 四、与 Extended Thinking 的关系

**Extended Thinking 是显式 thinking 的"重型版"**——模型在响应前先做一段独立思考。当前 4 型号（Fable 5.2 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5）**全部走 adaptive**：模型自己决定想多深，你用 `output_config: {"effort": ...}` 控深度。legacy 的 `thinking={"type": "enabled", "budget_tokens": N}` 只对 4.6 之前的上一代型号有效，在当前型号上一律 **400**。

| 维度 | 普通 prompt thinking | Extended Thinking |
| --- | --- | --- |
| **触发方式** | prompt 里写 "think step by step" | API 参数 `thinking` / `output_config.effort` |
| **思考可见性** | 写在响应正文里 | 单独 `thinking` block，可关闭返回 |
| **Token 预算** | 受 max_tokens 限制 | effort 控深度（上一代是显式 `budget_tokens`） |
| **模型支持** | 全部 | 当前 4 型号全走 adaptive；`budget_tokens` 只在 4.6 之前有效 |
| **适用场景** | 中等复杂 | 长链推理、需要精确控制思考深度 |

详见 [Extended Thinking 详解](/claude-capabilities/core/extended-thinking)。

## 五、与 Effort Level 的关系

**Effort 是请求级的"努力程度"**——控制模型在一次请求上做**多少总工作**（读多少文件、用多少工具、检查前推进多少步骤），不只是"思考多少"。当前 4 型号的 thinking 都是 adaptive，**effort 就是控制思考深度的旋钮**。

**API 侧**用 `output_config: {"effort": "..."}`（5 档），**CLI 侧**走 `/effort`：

| Level | 含义 |
| --- | --- |
| `low` | 最短、最省、延迟敏感 |
| `medium` | 成本敏感（**Opus 5.5 / Haiku 5.5 的默认档**） |
| `high` | 平衡，多数编程任务最优（**Fable 5.2 / Sonnet 5.5 的默认档**） |
| `xhigh` | 更深推理，token 更贵 |
| `max` | 极难任务；有 overthinking 风险 |

> 省略 `effort` 就等于用该型号的默认档——**不同型号默认不同**（Fable 5.2 / Sonnet 5.5 是 `high`，Opus 5.5 / Haiku 5.5 是 `medium`），换型号后别照抄旧参数。

详见 [CLI 视角 · Effort levels](/claude-code/basics/model-selection#四、effort-levels-与-effort)。

## 六、常见坑

**给简单 Q&A 加 "think step by step"**

拖慢响应、模型过度推理、给"看起来严谨但没必要的复杂答案"。

**长链 agent 每步都让 Claude 重新想一遍全任务**

每 turn 的 thinking 都受 max_tokens 限制。**长任务靠 effort level / Extended Thinking / Sub-agent 拆解**——不要每步都让 Claude 重新做规划。

**显式 thinking 输出到用户面前**

当前型号 `display` 默认是 `omitted`——思考摘要**根本不会回传**；一旦你显式开 `display: "summarized"`，就得自己负责过滤：

```python
# 显式隐藏 thinking
response = client.messages.create(...)
for block in response.content:
    if block.type == "thinking":
        continue     # 不展示给用户
    if block.type == "text":
        print(block.text)
```

**在 prompt 里写"先想 100 个可能"**

模型不会"真"做 100 个枚举——它会假装做了 100 个但其实只做了 3 个。**显式 thinking 的有效性跟具体性成正比**：3 个清晰的问题 > 100 个模糊的列举。

**混淆"推理"和"知识"**

- **知识不够** → 升 tier（Sonnet 5.5 → Opus 5.5）—— 详见 [模型选型 · 缺知识 vs 没努力](/claude-code/basics/model-selection#五、决策规则-缺知识-vs-没努力)
- **努力不够** → 升 effort 或加显式 thinking

加 thinking 解决不了"知识不够"——比如"2024 年欧冠冠军是谁"，加再多的 "think step by step" 也不知道答案。

## 参考

- [Anthropic Docs · Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)（访问于 2026-11-13）
- [Anthropic Docs · Effort](https://platform.claude.com/docs/en/build-with-claude/effort)（访问于 2026-11-13）
- [Anthropic Docs · Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)（访问于 2026-11-13）
- [Anthropic Docs · Chain prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-prompts)（访问于 2026-08-06）
- [Anthropic Docs · Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)（访问于 2026-08-06）
- [Extended Thinking 详解](/claude-capabilities/core/extended-thinking)
- [模型 ID 与定价](/claude-capabilities/models/model-ids)
- [模型选型 · 缺知识 vs 没努力](/claude-code/basics/model-selection#五、决策规则-缺知识-vs-没努力)
- [Opus 5.5 详解](/claude-capabilities/models/opus)

## 下一步

- Extended Thinking 机制深入 → [Extended Thinking 详解](/claude-capabilities/core/extended-thinking)
- 长链 agent 推理 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)
- 视觉推理 → [Vision 能力](/claude-capabilities/core/vision)

## 如果你想

- 提示工程更系统 → [深度提示工程 · 思维链](/claude-capabilities/prompting/chain-of-thought)
- 成本与推理深度权衡 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)
- 模型族选型 → [模型概览 · 选型决策指南](/claude-capabilities/models/overview#五、选型决策指南)
