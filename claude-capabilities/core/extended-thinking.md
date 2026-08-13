---
title: Extended Thinking
description: API 层的显式 thinking 机制；adaptive vs legacy budget_tokens 两种行为，4 模型 4 行为
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-06
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  extendedThinking: 'https://platform.claude.com/docs/en/build-with-claude/extended-thinking'
  modelOverview: 'https://platform.claude.com/docs/en/about-claude/models/overview'
  accessedAt: 2026-08-06
---

# Extended Thinking

> **TL;DR**：Extended Thinking 是 API 层的**显式 thinking 参数**——给模型"独立于 response 的思考空间"。**4 个模型走 2 种行为**：Fable 5 / Opus 5 / Sonnet 5 走 **adaptive**（模型自动决定思考深度，用户不能控）；**仅 Haiku 4.5 走 legacy `budget_tokens`**（用户显式控制思考预算）。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- Extended Thinking 的本质（独立 `thinking` block + 可关闭返回）
- 4 模型 2 行为的 API 形态对比
- Adaptive thinking 的实际行为（"模型自动决定"到底是怎样的）
- Legacy `budget_tokens` 实战（仅 Haiku 4.5）
- 何时用 / 不用 Extended Thinking
- 与 prompt 里"think step by step"的本质区别

## 一、Extended Thinking 的本质

**普通 prompt 的"thinking"**：模型在生成 response 的同时内部推理，**思考内容嵌入在 response 正文**——你看到的就是"含推理痕迹的最终答案"。

**Extended Thinking**：模型在生成 response **之前**先做一段**独立的思考**（独立 `thinking` block），然后基于这个思考再写 response：

```python
response = client.messages.create(
    model="claude-haiku-4-5",       # 仅 Haiku 4.5 支持 legacy budget_tokens
    max_tokens=4096,
    thinking={
        "type": "enabled",
        "budget_tokens": 2048,       # 思考的 token 预算
    },
    messages=[{"role": "user", "content": "..."}],
)

# response.content 现在是：
#   [
#     ThinkingBlock(signature=..., thinking="让我先分析..."),
#     TextBlock(text="基于以上分析，答案是..."),
#   ]
```

**关键差异**：

| 维度 | 普通 prompt thinking | Extended Thinking |
| --- | --- | --- |
| **触发** | prompt 写 "think step by step" | API 参数 `thinking` |
| **思考位置** | 嵌入 response 正文 | **独立 `thinking` block** |
| **是否可见** | 必可见（写进 response 文本） | **可关闭返回**（filter 掉） |
| **Token 预算** | 受 `max_tokens` 限制 | 显式 `budget_tokens` |
| **模型支持** | 全部 | **仅 Haiku 4.5**（走 legacy） |

**生产意义**：Extended Thinking 的 `thinking` block 是独立可隐藏的——你可以让用户只看"最终答案"，把"思考痕迹"藏在服务端日志里。

## 二、4 模型 2 行为：API 形态对比

| 模型 | thinking 行为 | API 形式 |
| --- | --- | --- |
| **Fable 5** | Adaptive，**强制开**，不能关，不能显式调 | `thinking` 字段只读，**不能传 `type: "enabled"`** |
| **Opus 5** | Adaptive，**总开**，不能显式关 | 同上 |
| **Sonnet 5** | Adaptive，**总开** | 同上 |
| **Haiku 4.5** | **Legacy `budget_tokens`** 显式控制 | `thinking={"type": "enabled", "budget_tokens": N}` |

**为什么 Fable 5 / Opus 5 / Sonnet 5 不让用户显式控 thinking？**

按 Anthropic 官方解释（同代 5 系模型）：
- 模型已被训练为**自动判断"该想多深"**——显式预算会破坏它的判断
- 实验室数据显示，adaptive thinking 的"自动判断"在大多数任务上**优于**用户手动设的预算
- Fable 5 的"specialist"定位更是如此——你不需要告诉专家"想多深"

**用户能控的只有 Haiku 4.5**——因为：
- Haiku 4.5 是上代模型，**不支持** adaptive
- legacy extended thinking 是它唯一能"被显式调度思考深度"的方式

## 三、Legacy `budget_tokens` 实战（仅 Haiku 4.5）

```python
import anthropic

client = anthropic.Anthropic()

# 简单分类任务：思考预算 1024
msg1 = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=2048,
    thinking={"type": "enabled", "budget_tokens": 1024},
    messages=[{"role": "user", "content": "把这段评论归类：'真的很差'"}],
)

# 中等推理：思考预算 2048-4096
msg2 = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=4096,
    thinking={"type": "enabled", "budget_tokens": 2048},
    messages=[{"role": "user", "content": "为什么这个 API 设计是 anti-pattern？"}],
)

# 复杂多步：思考预算 8192
msg3 = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=8192,
    thinking={"type": "enabled", "budget_tokens": 8192},
    messages=[{"role": "user", "content": "..."}],
)
```

**`budget_tokens` 怎么选**：

```
简单分类 / 格式化:       1024
中等推理:               2048-4096
复杂多步（仍在 Haiku 范畴）:  8192
> 8192                Haiku 4.5 已不够——升 Opus 5
```

## 四、Adaptive Thinking 的实际行为

虽然 Opus 5 / Sonnet 5 / Fable 5 不让用户显式设 budget，**但思考仍然发生**——只是模型**自己决定**该想多深：

- **简单 Q&A**：模型可能"想" 50 token 就答
- **复杂编程**：模型可能"想" 1000+ token 再写 code
- **长链 agent**：模型可能"想" 2000+ token 规划路径

**`thinking` block 仍然会返回**（结构与 Haiku 4.5 一致），但：
- 你**不能**在请求里设 budget
- 你**可以**在响应里 filter 掉（不让用户看到）

```python
# Opus 5 也返回 thinking block
response = client.messages.create(
    model="claude-opus-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": "..."}],
)

# 想隐藏思考痕迹
final_text = "\n".join(
    block.text for block in response.content if block.type == "text"
)
```

**生产建议**：API 端**永远** filter `thinking` block——用户看"答案"，不"看"模型怎么想。

## 五、何时用 Extended Thinking

| 场景 | 用？ | 理由 |
| --- | :---: | --- |
| 简单 Q&A / 文档总结 | ❌ | 浪费 token、无质量提升 |
| **Haiku 4.5 上做中等复杂任务** | ✅ | legacy 唯一可控方式 |
| **Opus 5 / Sonnet 5 / Fable 5 上做复杂任务** | ❌ 不需要显式 | adaptive 已自动判断 |
| **生产环境需要隐藏思考** | ✅ | Extended Thinking 的 `thinking` block 可 filter |
| **需要 thinking 审计日志** | ✅ | 独立 block 方便服务端记录 |

**反直觉**：**Opus 5 / Sonnet 5 / Fable 5 上加 `thinking` 参数是多余的**——模型已经在自适应"想"。传 `thinking` 反而会**破坏** adaptive 行为（部分 SDK 会报错，部分会忽略）。

## 六、与 prompt "think step by step" 的区别

详见 [推理能力 · 关系 Extended Thinking](/claude-capabilities/core/reasoning#四与-extended-thinking-的关系)。核心差异：

- **prompt "think step by step"**：思考嵌入 response 文本、用户必看见、不能控制预算
- **Extended Thinking**：思考独立 block、可隐藏、可控预算（仅 Haiku 4.5）

**何时用 prompt 模式**：
- 简单任务、不在意 token 浪费
- 思考本身对用户有价值（教育性、可解释性）

**何时用 Extended Thinking**：
- 生产环境（要隐藏思考）
- 需要 thinking 审计
- Haiku 4.5 上做需要思考深度的任务

## 七、常见坑

**给 Opus 5 / Sonnet 5 / Fable 5 传 `budget_tokens`**

```python
# ❌ 错
client.messages.create(
    model="claude-opus-5",
    thinking={"type": "enabled", "budget_tokens": 4096},   # 报 schema 错或忽略
    ...
)

# ✅ 对——Opus 5 不传 thinking，adaptive 自己决定
client.messages.create(model="claude-opus-5", ...)
```

**把 Extended Thinking 的 `thinking` block 直接返回给用户**

泄露模型"思考细节"——可能包含内部 prompt 重述、模型自检、unrelated 思考。**生产必 filter**。

**Haiku 4.5 `budget_tokens` 设过大**

`budget_tokens` 太大 → thinking 占用过多 token → 实际 `max_tokens` 不够 response。**预留比例**：`budget_tokens` ≤ `max_tokens` 的 50%。

**混淆"extended thinking"和"extended context"**

- Extended Thinking：API 层的 thinking 参数
- Extended Context：1M context（Opus 5 / Sonnet 5 / Fable 5 上 1M context 是默认）

**完全两件事**——别混。

**用 Extended Thinking 替代 Sub-agent 拆解**

复杂任务更该拆 sub-agent（成本更可控、并行更快）——Extended Thinking 是**单次**深度推理工具，不是**任务分解**工具。

## 参考

- [Anthropic Docs · Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)（访问于 2026-08-06）
- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-08-06）
- [推理能力 · 何时让 Claude 想](/claude-capabilities/core/reasoning)
- [Haiku 4.5 详解 · Legacy Extended Thinking](/claude-capabilities/models/haiku#三legacy-extended-thinkinghaiku-45-独有)
- [Fable 5 详解 · Adaptive Thinking 强制开启](/claude-capabilities/models/fable#二adaptive-thinking-强制开启)
- [Opus 5 详解 · Adaptive Thinking 行为](/claude-capabilities/models/opus#三adaptive-thinkingopus-5-的思考行为)

## 下一步

- 视觉推理 → [Vision 能力](/claude-capabilities/core/vision)
- 代码生成能力 → [代码能力](/claude-capabilities/core/coding)
- 长文档处理 → [长上下文](/claude-capabilities/core/long-context)

## 如果你想

- 思考 vs effort level 关系 → [CLI 视角 · Effort levels](/claude-code/basics/model-selection#四effort-levels-与-effort)
- 隐藏 thinking 的生产模式 → [代码能力 · 实战模式](/claude-capabilities/core/coding)
- 提示工程系统化 → [深度提示工程](/claude-capabilities/prompting/chain-of-thought)
