---
title: Extended Thinking
description: API 层的显式 thinking 机制；当前 4 型号全走 adaptive，深度用 effort 控，legacy budget_tokens 只对上一代有效
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 订正 thinking 取值矩阵与 effort 口径（官方 thinking / effort / extended-thinking 文档同日复核）：当前 4 型号全部走 adaptive，thinking.enabled / budget_tokens 一律 400，深度改用 output_config.effort；章节 H2 沿用旧措辞以保住站内锚点，CLI 相关断言沿用 2026-08 的记录（当时基于 Claude Code 2.1.220），示例未在本机重跑'
  claudeCode: 2.1.220
  model: claude-opus-5-5
  extendedThinking: 'https://platform.claude.com/docs/en/build-with-claude/extended-thinking'
  thinking: 'https://platform.claude.com/docs/en/build-with-claude/thinking'
  effort: 'https://platform.claude.com/docs/en/build-with-claude/effort'
  modelOverview: 'https://platform.claude.com/docs/en/about-claude/models/overview'
  accessedAt: 2026-08-06
---

# Extended Thinking

> **TL;DR**：Extended Thinking 是 API 层的**显式 thinking 参数**——给模型一块独立于 response 的思考空间。**当前 4 个型号（Fable 5.2 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5）全部走 adaptive**：模型自己决定想多深，你能控深度的是 **effort**，不是 `thinking` 参数。legacy `budget_tokens` 只对 4.6 之前的上一代型号有效，在当前型号上一律 **400**。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- Extended Thinking 的本质（独立 `thinking` block + 可关闭返回）
- 当前 4 型号的 `thinking` 取值矩阵（哪些写法直接 400）
- Adaptive thinking 的实际行为（"模型自动决定"到底是怎样的）
- Legacy `budget_tokens` 实战（只对上一代有效）与官方迁移映射
- effort 与 thinking 的分工（深度归 effort）
- 与 prompt 里"think step by step"的本质区别

## 一、Extended Thinking 的本质

**普通 prompt 的"thinking"**：模型在生成 response 的同时内部推理，**思考内容嵌入在 response 正文**——你看到的就是"含推理痕迹的最终答案"。

**Extended Thinking**：模型在生成 response **之前**先做一段**独立的思考**（独立 `thinking` block），然后基于这个思考再写 response：

```python
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=4096,
    output_config={"effort": "high"},   # 想多深靠 effort，不靠 thinking 参数
    messages=[{"role": "user", "content": "..."}],
)

# response.content 可能以 thinking block 开头：
#   [
#     ThinkingBlock(signature=..., thinking=""),   # Claude 5+ 默认 display="omitted"，摘要不回传
#     TextBlock(text="基于以上分析，答案是..."),
#   ]
```

**关键差异**：

| 维度 | 普通 prompt thinking | Extended Thinking |
| --- | --- | --- |
| **触发** | prompt 写 "think step by step" | API 参数 `thinking` / `output_config.effort` |
| **思考位置** | 嵌入 response 正文 | **独立 `thinking` block** |
| **是否可见** | 必可见（写进 response 文本） | **默认不可见**（`display` 默认 `omitted`） |
| **Token 预算** | 受 `max_tokens` 限制 | effort 控深度（上一代是显式 `budget_tokens`） |
| **模型支持** | 全部 | 当前 4 型号全走 adaptive；`budget_tokens` 只在 4.6 之前有效 |

**生产意义**：Extended Thinking 的 `thinking` block 是独立可隐藏的——你可以让用户只看"最终答案"，把"思考痕迹"藏在服务端日志里。

## 二、4 模型 2 行为：API 形态对比

> ⚠️ 本章 H2 沿用 2026-08 的旧措辞（"4 模型 2 行为"）以保住站内锚点。**截至 2026-11-13，当前 4 型号实际只有 1 种行为（adaptive）**，深度控制交给了 effort。

官方按型号给出的 `thinking` 取值矩阵（`400` = 直接拒绝请求）：

| 型号 | 省略 `thinking` | `{"type": "adaptive"}` | `{"type": "enabled", "budget_tokens"}` | `{"type": "between_tools"}` | `{"type": "disabled"}` |
| --- | --- | --- | --- | --- | --- |
| **Fable 5.2** | adaptive | adaptive | 400 | 400 | 400 |
| **Opus 5.5** | adaptive | adaptive | 400 | 400 | 400 |
| **Sonnet 5.5** | adaptive | adaptive | 400 | 关掉前置思考（high 及以下 effort） | 400 |
| **Haiku 5.5** | adaptive | adaptive | 400 | 400 | 关掉思考（high 及以下 effort） |

**所以当前只有两个旋钮**：

- **想多深** → `output_config: {"effort": "low|medium|high|xhigh|max"}`
- **要不要看思考摘要** → `thinking: {"type": "adaptive", "display": "summarized"}`

**为什么不让用户显式控 thinking？**

按 Anthropic 官方解释（同代 5 系模型）：

- 模型已被训练为**自动判断"该想多深"**——显式预算会破坏它的判断
- 实验室数据显示，adaptive thinking 的"自动判断"在大多数任务上**优于**用户手动设的预算
- Fable 5.2 的"specialist"定位更是如此——你不需要告诉专家"想多深"

**用户还能控什么**：

- **Haiku 5.5**：当前唯一还能显式关掉思考的型号（`disabled`，仅 high 及以下 effort）
- **Sonnet 5.5**：用 `between_tools` 关掉前置思考（仅 high 及以下 effort，xhigh / max 会 400）
- 其余情况：**只调 effort**

## 三、Legacy `budget_tokens` 实战（仅 Haiku 4.5）

> ⚠️ 本章是**上一代写法**。官方已把 extended thinking 标为 legacy：Opus 4.6 / Sonnet 4.6 上废弃，**4.7 及之后一律 400**——当前 4 型号（Fable 5.2 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5）全在 400 那一侧。

**上一代怎么写**（只对 4.6 之前的型号有效，如 `claude-haiku-4-5`）：

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

**`budget_tokens` 怎么选**（上一代口径）：

```
简单分类 / 格式化:       1024
中等推理:               2048-4096
复杂多步:               8192
> 8192                上一代 Haiku 已不够——升 Opus（今天是 Opus 5.5）
```

**迁到当前型号**（官方给的映射）：

```python
# ❌ 旧写法，当前型号 400
thinking={"type": "enabled", "budget_tokens": 10000}

# ✅ 现在的写法
thinking={"type": "adaptive"},
output_config={"effort": "high"},
```

官方预算规则还有两条硬约束：`budget_tokens` **最小 1024**，且必须 **小于 `max_tokens`**（思考 token 计入 `max_tokens`）。

## 四、Adaptive Thinking 的实际行为

虽然当前 4 型号都不让用户显式设 budget，**但思考仍然发生**——只是模型**自己决定**该想多深：

- **简单 Q&A**：模型可能"想"几十 token 就答
- **复杂编程**：模型可能"想" 1000+ token 再写 code
- **长链 agent**：模型可能"想" 2000+ token 规划路径

**`thinking` block 仍然会返回**，但**默认看不到思考文本**——Claude 5 及之后的型号 `display` 默认是 `omitted`，回传的 thinking block 里 `thinking` 字段是空的：

```python
# 省略 thinking 即可（adaptive 默认开）
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": "..."}],
)

# 想看思考摘要——显式要
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=4096,
    thinking={"type": "adaptive", "display": "summarized"},
    messages=[{"role": "user", "content": "..."}],
)

# 不让用户看到思考痕迹
final_text = "\n".join(
    block.text for block in response.content if block.type == "text"
)
```

**生产建议**：**默认就别开 `display: "summarized"`**——用户看"答案"，不"看"模型怎么想。要留审计日志就自己开 `summarized` 再写进服务端日志。

## 五、何时用 Extended Thinking

| 场景 | 用？ | 理由 |
| --- | :---: | --- |
| 简单 Q&A / 文档总结 | ❌ | 浪费 token、无质量提升 |
| **Haiku 5.5 上做中等复杂任务** | ✅ | 默认 `medium` effort；省成本降到 `low` |
| **Opus 5.5 / Fable 5.2 上做复杂任务** | ✅ | adaptive 自动判断，深度用 effort 调 |
| **Sonnet 5.5 不想有前置思考** | ✅ | `thinking: {"type": "between_tools"}`（high 及以下 effort） |
| **生产环境需要隐藏思考** | ✅ | `display` 默认 `omitted`，默认就看不到思考文本 |
| **需要 thinking 审计日志** | ✅ | 显式 `display: "summarized"` |

**反直觉**：**在 Opus 5.5 / Fable 5.2 上传 `thinking` 参数不是"多余"而是会 400**——`{"type": "enabled"}` 和 `{"type": "disabled"}` 都被拒；Sonnet 5.5 上 `disabled` 也 400，只有 `between_tools` 可用。当前型号的默认写法就是**省略 `thinking` 字段**。

## 六、与 prompt "think step by step" 的区别

详见 [推理能力 · 关系 Extended Thinking](/claude-capabilities/core/reasoning#四、与-extended-thinking-的关系)。核心差异：

- **prompt "think step by step"**：思考嵌入 response 文本、用户必看见、不能控制预算
- **Extended Thinking**：思考独立 block、可隐藏（`display` 控制）、深度由 effort 控

**何时用 prompt 模式**：

- 简单任务、不在意 token 浪费
- 思考本身对用户有价值（教育性、可解释性）

**何时用 Extended Thinking**：

- 生产环境（要隐藏思考）
- 需要 thinking 审计
- 需要精确控制思考深度（调 effort）

## 七、常见坑

**给当前型号传 `budget_tokens` 或 `thinking: {"type": "enabled"}`**

```python
# ❌ 错——当前 4 型号一律 400
client.messages.create(
    model="claude-opus-5-5",
    thinking={"type": "enabled", "budget_tokens": 4096},
    ...
)

# ✅ 对——省略 thinking，用 effort 控深度
client.messages.create(
    model="claude-opus-5-5",
    max_tokens=4096,
    output_config={"effort": "high"},
    ...
)
```

**把 `adaptive` 当成 effort 值传**

`adaptive` 是 thinking 模式，不是 effort 档位——`output_config: {"effort": "adaptive"}` 是错的。effort 只有 `low` / `medium` / `high` / `xhigh` / `max` 五档。

**把 Extended Thinking 的 `thinking` block 直接返回给用户**

泄露模型"思考细节"——可能包含内部 prompt 重述、模型自检、无关思考。**生产必 filter**；而且 Claude 5+ 默认 `display: "omitted"`，最省事的做法是压根不开 `summarized`。

**上一代 `budget_tokens` 设过大**

`budget_tokens` 太大 → thinking 占用过多 token → 实际 `max_tokens` 不够 response。**预留比例**：`budget_tokens` ≤ `max_tokens` 的 50%（官方硬规则：最小 1024、必须小于 `max_tokens`）。

**混淆"extended thinking"和"extended context"**

- Extended Thinking：API 层的 thinking 参数
- Extended Context：1M context（当前 4 型号都是 1M context）

**完全两件事**——别混。

**用 Extended Thinking 替代 Sub-agent 拆解**

复杂任务更该拆 sub-agent（成本更可控、并行更快）——Extended Thinking 是**单次**深度推理工具，不是**任务分解**工具。

## 参考

- [Anthropic Docs · Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)（访问于 2026-11-13）
- [Anthropic Docs · Effort](https://platform.claude.com/docs/en/build-with-claude/effort)（访问于 2026-11-13）
- [Anthropic Docs · Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)（访问于 2026-11-13）
- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-11-13）
- [模型 ID 与定价](/claude-capabilities/models/model-ids)
- [推理能力 · 何时让 Claude 想](/claude-capabilities/core/reasoning)
- [Haiku 5.5 · 4.5→5.5 三个 breaking change](/claude-capabilities/models/haiku#三、haiku-4-5-→-5-5-三个-breaking-change)
- [Fable 5.2 详解 · Adaptive Thinking 强制开启](/claude-capabilities/models/fable#二、adaptive-thinking-强制开启)
- [Opus 5.5 详解 · Adaptive Thinking 行为](/claude-capabilities/models/opus#三、adaptive-thinking)

## 下一步

- 视觉推理 → [Vision 能力](/claude-capabilities/core/vision)
- 代码生成能力 → [代码能力](/claude-capabilities/core/coding)
- 长文档处理 → [长上下文](/claude-capabilities/core/long-context)

## 如果你想

- 思考 vs effort level 关系 → [CLI 视角 · Effort levels](/claude-code/basics/model-selection#四、effort-levels-与-effort)
- 隐藏 thinking 的生产模式 → [代码能力 · 实战模式](/claude-capabilities/core/coding)
- 提示工程系统化 → [深度提示工程](/claude-capabilities/prompting/chain-of-thought)
