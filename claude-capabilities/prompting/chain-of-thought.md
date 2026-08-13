---
title: 思维链
description: 引导逐步推理的 prompt 模式——4 种变体、5 个实战技巧、与 Extended Thinking 的边界
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  cotDocs: 'https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought'
  extendedThinking: 'https://platform.claude.com/docs/en/build-with-claude/extended-thinking'
  accessedAt: 2026-08-07
---

# 思维链

> **TL;DR**：思维链（Chain-of-Thought, CoT）让模型**写出推理步骤**——简单任务用 zero-shot CoT（一句话触发），复杂任务用 few-shot CoT（给示例推理）。与 [Extended Thinking](/claude-capabilities/core/extended-thinking) 的区别：CoT 是 prompt 层技巧，Extended Thinking 是 API 层机制。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 4 种 CoT 变体（zero-shot / few-shot / self-consistency / ToT）
- 何时该用 CoT、用了反而更糟的情况
- 5 个实战技巧（step 数 / 显式 vs 隐式 / 输出格式 / 错误处理 / 与系统提示结合）
- CoT 与 [推理能力](/claude-capabilities/core/reasoning) / [Extended Thinking](/claude-capabilities/core/extended-thinking) 的边界
- 4 个常见坑

## 一、CoT 的本质

**让模型把"思考过程"写出来**——而不是直接给答案。背后的简单逻辑：**显式推理 > 隐式跳跃**。

```text
# ❌ 不显式推理
"这段代码有什么问题？"
→ 答案：可能错或漏

# ✅ 显式 CoT
"请逐步检查这段代码：1. 边界条件 2. 错误处理 3. 性能 4. 安全"
→ 模型先 list 各维度问题，再综合给结论
```

**为什么有效**：
- 模型在每一步能"自我检查"
- 长推理被分解成多个短推理，**每步错率 < 整段错率**
- 思考过程**对用户可见**——可审查、可调试

详见 [推理能力 · 隐式 CoT vs 显式 thinking](/claude-capabilities/core/reasoning#一claude-推理的两层)。

## 二、4 种 CoT 变体

### 变体 1：Zero-shot CoT（一句话触发）

```text
请逐步思考，然后回答：
"为什么这个 API 设计是 anti-pattern？"
```

**触发短语**（任选其一）：
- "Let's think step by step"
- "请逐步思考"
- "请先想清楚再答"
- "Think before answering"

**适用**：简单任务（中等推理、debug、对比）。

### 变体 2：Few-shot CoT（给示例）

```text
Q: 这个数字 24 是偶数吗？
A: 24 = 2 × 12，所以是偶数。

Q: 35 是偶数吗？
A: 35 = 5 × 7，不是 2 的倍数，所以不是偶数。

Q: 89 是偶数吗？
A:
```

**适用**：复杂推理（数学、逻辑、特定领域）。

### 变体 3：Self-Consistency（多次采样投票）

```text
请用 5 种不同思路独立回答这道题，最后给出最一致的答案：
[复杂数学题]
```

**适用**：**高价值决策**（多步推理、关键方案选型）。成本 5x。

### 变体 4：Tree of Thought（探索多个分支）

```text
请列出 3 种可能的解决思路，评估每种的优劣，选最好的执行：
[复杂任务]
```

**适用**：方案选型、架构决策、debug 多根因。详见 [推理能力 · 模式 2：先想 3 个反例](/claude-capabilities/core/reasoning#模式-2先想-3-个反例)。

## 三、何时该用 CoT

| 任务 | 该用 CoT？ | 原因 |
| --- | :---: | --- |
| 简单 Q&A | ❌ | 加 CoT 拖时间、可能幻觉 |
| 文档总结 | ❌ | 总结任务不需要推理 |
| 短对话 | ❌ | 默认 CoT 够用 |
| **多步决策** | ✅ | 显式步骤大幅提升质量 |
| **复杂 debug** | ✅ | 避免 Claude 直接猜、漏读文件 |
| **架构设计** | ✅ | 先列约束、再给方案 |
| **数学 / 逻辑题** | ✅ | 显式步骤让 Claude 不跳步 |
| **长链 agent 规划** | ✅ | 每步先想清楚再动手 |
| **高价值决策**（1+ 选 1） | ✅ Self-Consistency | 多次采样取一致 |

详见 [推理能力 · 何时该让 Claude 想](/claude-capabilities/core/reasoning#二何时该让-claude-想--不该让它想)。

## 四、5 个实战技巧

### 技巧 1：明确 step 数

```text
# ❌ 模糊
"逐步分析"

# ✅ 明确
"分 3 步分析：1. 找 5 个可能原因 2. 排除不可能的 3. 验证剩下的"
```

**实战**：**3-5 步**最有效——太少不分解、太多变冗长。

### 技巧 2：显式 vs 隐式 CoT

| 模式 | 写法 | 适用 |
| --- | --- | --- |
| **显式** | "请先想 X，再想 Y" | 输出含推理 |
| **隐式** | "思考后给答案" | 输出**不含**推理（更快） |

```text
# 显式——推理嵌入 response
"先想 3 个反例，再给方案。最后给最终代码。"

# 隐式——思考但不输出
"想清楚后给最终答案，不要展示过程。"
```

### 技巧 3：规定 CoT 输出格式

```text
请按以下格式思考：
思考：[推理过程]
结论：[最终答案]
```

**实战**：用 XML 标签 / Markdown heading 结构化 CoT 输出——方便后续 extract 推理痕迹。

### 技巧 4：CoT 错误处理

```text
如果思考过程中发现矛盾，回头重新分析。最多 2 次重试。
```

**实战**：让 Claude **自我检查 + 修订**——Self-Correction。

### 技巧 5：CoT 与 system prompt 结合

```python
# system：长期规则
system = "你是严谨的工程师。任何结论必须有 3 个支撑依据。"

# user：当前任务 + CoT 触发
messages = [{"role": "user", "content": """
先想 3 个支撑依据再给结论：
[当前任务]
"""}]
```

详见 [System Prompt 设计](/claude-capabilities/prompting/system-prompts)。

## 五、CoT 与 Extended Thinking 的边界

| 维度 | CoT | Extended Thinking |
| --- | --- | --- |
| **触发方式** | prompt 写 "step by step" | API 参数 `thinking` |
| **思考可见** | 嵌入 response 文本 | 独立 `thinking` block |
| **Token 预算** | 受 max_tokens 限制 | 显式 `budget_tokens` |
| **模型支持** | 全部 | 仅 Haiku 4.5 legacy |
| **成本** | 计入 response token | 独立计费 |

**反例**：

```text
# 在 Opus 5 / Sonnet 5 / Fable 5 上加 Extended Thinking 想"控制思考深度"是错的
# → 这些模型走 adaptive thinking，CoT 已自动启用
# → Extended Thinking 仅 Haiku 4.5 有效
```

详见 [Extended Thinking 详解 · 4 模型 2 行为](/claude-capabilities/core/extended-thinking#二4-模型-2-行为api-形态对比)。

## 六、4 个常见坑

**1. 简单任务用 CoT**

"今天天气怎么样？" + "逐步思考" = 拖慢 + 幻觉。详见 [推理能力 · 反直觉](/claude-capabilities/core/reasoning#二何时该让-claude-想--不该让它想)。

**2. step 数过多**

```text
# ❌ 10 步 CoT
"分 10 步分析..."

# ✅ 3-5 步
"分 3 步分析..."
```

超过 7-8 步，模型开始"凑步骤"——质量反而下降。

**3. CoT 不规定输出格式**

```text
# ❌ 输出散装
"想清楚再答"

# ✅ 强制结构
"按 '思考' / '结论' 两段输出"
```

**4. CoT 后不验证**

```text
# ❌ CoT 完直接给代码
"想 3 个边界 → 给代码"

# ✅ CoT 完自检 + 跑测试
"想 3 个边界 → 给代码 → 自检 + 跑 [测试用例] 验证"
```

详见 [代码能力 · 4 类代码任务](/claude-capabilities/core/coding#三四类代码任务的模型选型)。

## 参考

- [Anthropic Docs · Chain of Thought](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought)（访问于 2026-08-07）
- [Anthropic Docs · Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)（访问于 2026-08-07）
- [推理能力 · 5 个模式](/claude-capabilities/core/reasoning#三5-个让-claude-想清楚再答的-prompt-模式)
- [Extended Thinking 详解](/claude-capabilities/core/extended-thinking)
- [最佳实践 · 原则 3](/claude-capabilities/prompting/best-practices#原则-3让模型想)
- [System Prompt 设计](/claude-capabilities/prompting/system-prompts)

## 下一步

- Few-shot 实战 → [Few-shot 示例](/claude-capabilities/prompting/few-shot)
- XML 标签结构化 → [Prefill 与 XML 标签](/claude-capabilities/prompting/prefill-and-xml)
- 速查模板 → [常用模板](/claude-capabilities/prompting/templates)

## 如果你想

- 推理深入 → [推理能力](/claude-capabilities/core/reasoning)
- Extended Thinking API → [Extended Thinking 详解](/claude-capabilities/core/extended-thinking)
- 切到 API 调用 → [Messages API](/claude-capabilities/api/messages)
