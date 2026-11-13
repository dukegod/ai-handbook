---
title: Opus 5.5
description: '当前旗舰 agentic 编码模型；Model ID `claude-opus-5-5`；1M context；$4 / $20 per MTok；上一代 Opus 5 档案见文末'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 复核了 Opus 5.5 与上一代 Opus 5 的 Model ID、定价与缓存价、context / max output、thinking 与 tool_choice 行为、Batch 300k 支持型号、退役承诺与 Claude Code 最低版本；Fast mode 价格、Opus 5 vs Sonnet 5 实测数据，以及 Messages API 与 Anthropic Blog 两条外链沿用 2026-10-08 / 2026-08-06 的旧记录；本页示例未在本机重跑'
  claudeCode: 2.1.319
  model: claude-opus-5-5
  modelOverview: 'https://platform.claude.com/docs/en/about-claude/models/overview'
  modelConfig: 'https://code.claude.com/docs/en/model-config'
  pricing: 'https://platform.claude.com/docs/en/about-claude/pricing'
  deprecations: 'https://platform.claude.com/docs/en/about-claude/model-deprecations'
  modelIds: 'https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions'
  effort: 'https://platform.claude.com/docs/en/build-with-claude/effort'
  thinking: 'https://platform.claude.com/docs/en/build-with-claude/thinking'
  accessedAt: 2026-11-13
---

# Opus 5.5

> ⚠️ **上一代 Opus 5（`claude-opus-5`）的档案保留在文末**——它仍可调用（状态 Active，退役承诺不早于 2027-07-24），但新代码请直接写 `claude-opus-5-5`。

> **TL;DR**：Opus 5.5 = 「the expert」——`claude-opus-5-5`，**1M context / 128k output**，**$4 / $20 per MTok**（比上一代 Opus 5 便宜 20%）。官方定位是 "For long-running agentic coding and knowledge work"——**绝大多数负载从它起步**。

**官方规格**（[Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)，访问于 2026-11-13）：

| 项 | 值 |
| --- | --- |
| Context window | 1M tokens |
| Max output | 128K（Batch API 下配 `output-300k-2026-03-24` beta header 可到 300K） |
| 思考 | Adaptive，**总是开、不能显式关**；默认 effort `medium` |
| 相对延迟 | Moderate |
| 知识截止 | 2026-06 |
| Fast mode（research preview） | $8 / $40 † |
| 退役承诺 | 不早于 2027-09-22 |
| Claude Code 最低版本 | v2.1.280 |

† Fast mode 价格沿用仓库 2026-10-08 的记录（[Anthropic 厂商档案 · 价格](/ai-trends/vendors/anthropic/#六、价格-截至-2026-11-官方定价)），本轮未在官方定价页重新核对；**不与 Batch 叠加**。

**同代横向对照**（完整表见 [模型 ID 与定价](./model-ids)）：

| 模型 | Model ID | 输入 / 输出（$/MTok） | 缓存读 | 默认 effort | 相对延迟 |
| --- | --- | --- | --- | --- | --- |
| **Opus 5.5** | `claude-opus-5-5` | **$4 / $20** | $0.20（5%） | `medium` | Moderate |
| Sonnet 5.5 | `claude-sonnet-5-5` | $2 / $10 | $0.10（5%） | `high` | Fast |
| Haiku 5.5 | `claude-haiku-5-5` | $0.10 / $0.50 † | $0.01 | `medium` | Fastest |
| Fable 5.2 | `claude-fable-5-2` | $8 / $40 | $0.20（2.5%） | `high` | Slower |

† Haiku 5.5 是全系唯一按 prompt 长度分档计费的型号（> 100k token 时输入 $0.50 / 输出 $2.50）。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 最小调用示例（Python + TypeScript + streaming）
- 关键参数速查（adaptive thinking / effort / max_tokens / strict tool use）
- Adaptive Thinking 在 Opus 5.5 上的行为与两个 400 陷阱
- 与 Sonnet 5.5 的实测选型（不是「更聪明」而是「少 X 步」）
- 何时**不该**用 Opus 5.5
- 上一代 Opus 5 的规格与迁移差异

## 一、最小调用示例

**Python**（[anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)）：

```python
import anthropic

client = anthropic.Anthropic()

msg = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "解释这段 Python 代码为什么慢：..."}],
)
print(msg.content[0].text)
```

**TypeScript**（[@anthropic-ai/sdk](https://github.com/anthropics/anthropic-sdk-typescript)）：

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const msg = await client.messages.create({
  model: "claude-opus-5-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "解释这段 Python 代码为什么慢：..." }],
});
console.log(msg.content[0].text);
```

**Streaming**（长输出场景必备）：

```python
with client.messages.stream(
    model="claude-opus-5-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": "..."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

> **Tokenizer 变了**：Opus 5.5 用 4.7 世代引入的新 tokenizer——当前 tokenizer 下 1M token ≈ 555k 词 ≈ 250 万字符，旧 tokenizer 下 1M token ≈ 750k 词。同样文本在 Opus 5.5 上约多 30~35% token，预算与 cache 命中率都要重算。

## 二、关键参数速查

| 参数 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `model` | `str` | — | `claude-opus-5-5`（4.6 世代起 dateless ID 本身就是 pinned 快照） |
| `max_tokens` | `int` | — | 必填；同步接口上限 **128000** |
| `system` | `str` \| list | — | System prompt；加 `cache_control` 走缓存（见 [Prompt Caching](/claude-capabilities/api/prompt-caching)） |
| `thinking` | `dict` | 省略 | **不要传**：`disabled` / `enabled` 一律 400 |
| `output_config.effort` | `str` | `medium` | 控思考深度，见 [Effort level](/claude-code/basics/model-selection#四、effort-levels-与-effort) |
| `tools` | `list[dict]` | — | 工具定义（[Tool Use API 协议](/claude-capabilities/core/tool-use)） |
| `tool_choice` | `str` | `auto` | `any` / `tool` **返回 400**，只能用 `auto` / `none` / 指定工具名 |
| `metadata` | `dict` | — | 自定义追踪字段（user_id / session_id） |

> **不要传 `temperature` / `top_p` / `top_k`**：API version `2026-10-21` 起这三个参数已被移除，传了返回 400（连默认值也报错）。
>
> **Batch API 一律 5 折**：输入输出同时打对折，Opus 5.5 → **$2 / $10**（见 [Message Batches API](/claude-capabilities/api/message-batches)）。
>
> 完整字段以 [Anthropic Docs · Messages API](https://platform.claude.com/docs/en/api/messages) 为准。

## 三、Adaptive Thinking

Opus 5.5 走 **adaptive thinking**——模型自己决定每次请求「想多深」。它**总是开、不能关**，也不接受 legacy 的 `budget_tokens`：

```python
# ❌ 一律 400
thinking={"type": "disabled"}
thinking={"type": "enabled", "budget_tokens": 4096}

# ✅ 省略 thinking，用 effort 控深度
msg = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=4096,
    output_config={"effort": "high"},   # 默认 medium，可选 low / medium / high
    messages=[{"role": "user", "content": "..."}],
)
```

**同代 thinking 行为对照**：

| 模型 | thinking 行为 |
| --- | --- |
| **Opus 5.5** | Adaptive，**总是开、不能显式关**；默认 effort `medium` |
| Fable 5.2 | Adaptive，总是开、不能关；默认 effort `high` |
| Sonnet 5.5 | Adaptive，默认 effort `high`；`high` 及以下 effort 可用 `between_tools` 关掉前置思考 |
| Haiku 5.5 | Adaptive，默认开，默认 effort `medium` |
| Haiku 4.5 | **不支持** adaptive；用 legacy extended thinking + `budget_tokens` |

> legacy `thinking.type: "enabled"` + `budget_tokens` 自 **Opus 4.6 起已废弃**，在更晚的模型上一律不接受。

**第二个 400 陷阱是 `tool_choice`**：`any` / `tool` 在 Opus 5.5、Sonnet 5.5、Fable 5.2 上一律返回 400。要保证工具入参符合 schema，用 **strict tool use**（`strict: true`）或 structured outputs。

详见 [Extended Thinking 详解](/claude-capabilities/core/extended-thinking)。

## 四、Opus 5.5 vs Sonnet 5.5 实测选型

**不是「Opus 更聪明」，而是「Opus 少步数」**。

| 任务 | Sonnet 5.5 表现 | Opus 5.5 表现 | 何时该升 Opus |
| --- | --- | --- | --- |
| 日常 80% 编程 | 表现良好 | 同样能完成 | 不该升——成本翻倍 |
| 大型陌生代码库 debug | 多次循环 + 漏读文件 | 一次定位根因 | 该升 |
| 多文件架构重构 | 给出方向但要反复 prompt | 直接给可执行方案 | 该升 |
| 长链多步 agent（10+ tool call） | 走 15-20 步 + 中途验证丢失 | 走 8-12 步且自查 | 该升 |
| 简单 Q&A / 文档总结 | 表现良好 | 表现良好 | **不该升** |

**成本反直觉**：

```
Sonnet 5.5:  $2/M input  × 20 步 × 50k input  =  $2.00
Opus 5.5:    $4/M input  × 10 步 × 30k input  =  $1.20
                              → Opus 总成本反而更低
```

「少步数」原则的完整讨论见 [选型决策指南](./overview#五、选型决策指南)；降本手段清单见 [成本与 Token 管理](/claude-code/basics/cost-and-tokens)。

## 五、何时不该用

1. **简单批处理 / 分类 / 提取**——用 [Haiku 5.5](./haiku)（$0.10 / $0.50 起，比 Opus 5.5 便宜 40 倍）
2. **日常 80% 编程与对话**——[Sonnet 5.5](./sonnet) 够用，价格只有一半
3. **超长链 agent**（50+ tool call 跨小时）——直接上 [Fable 5.2](./fable)
4. **大量并发 function calling**——Opus 5.5 的相对延迟是 Moderate，subagent 编排时混搭用 Haiku
5. **Prompt caching 命中率 < 30%**——缓存不命中时 Opus 的高单价不划算

## 六、常见坑

**Model ID 写成 `claude-opus-5`**

这是上一代，仍能调用（Active，退役不早于 2027-07-24），但**不会 404**——你会静默地按上一代的价格和参数行为跑。Opus 5.5 必须写 `claude-opus-5-5`。

**传 `temperature` / `top_p` / `top_k`**

API version `2026-10-21` 起这三个参数被移除，传了返回 400——**连默认值也报错**。想控制输出风格只能写进 prompt。

**`thinking` 显式传 `disabled` 或 `enabled`**

一律 400。只能省略字段、改用 `output_config.effort`。

**`tool_choice: "any"`**

Opus 5.5 / Sonnet 5.5 / Fable 5.2 上返回 400。要强制工具调用，用 strict tool use 或 structured outputs。

**max_tokens 设了 128000 但实际只输出几千 token**

128k 是 **output 上限**，不是目标；设 128k 不会让模型「努力写更多」，反而增加首 token 延迟。按场景给合理值（短回答 256-1024，长文 4096-8192）。

**Batch 里想输出 300k 却没带 beta header**

300k 输出只在 [Message Batches API](/claude-capabilities/api/message-batches) + `anthropic-beta: output-300k-2026-03-24` 下可用；同步 Messages API 上限就是 128K。Opus 5.5 在官方点名支持的名单内（Fable 5.2 不在）。

## 七、Opus 5（上一代）档案

> 以下是**上一代 Opus 5** 的记录，保留作参考与迁移对照。新代码请用 `claude-opus-5-5`。

**Opus 5.5 与 Opus 5 的差异**（[Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) 与 [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)，访问于 2026-11-13）：

| | Opus 5.5（当前） | Opus 5（上一代） |
| --- | --- | --- |
| Model ID | `claude-opus-5-5` | `claude-opus-5` |
| 输入 / 输出 | $4 / $20 | $5 / $25 |
| 缓存写 5m / 1h | $5 / $8 | $6.25 / $10 |
| 缓存读 | $0.20（0.05x） | $0.50（0.1x） |
| Context / Max output | 1M / 128k | 1M / 128k |
| 思考 | Adaptive，总是开、不可关 | Adaptive，不可关 |
| 默认 effort | `medium` | — |
| `tool_choice: any / tool` | ❌ 400 | 支持 |
| Fast mode（research preview） | $8 / $40 † | $10 / $50 † |
| 退役承诺 | 不早于 2027-09-22 | 不早于 2027-07-24 |

**最值得注意的两处**：一是**缓存读便宜了 60%**（$0.50 → $0.20），长 prompt 高度重复的 agent 场景直接受益；二是 **Opus 5 仍支持 `tool_choice: any / tool`，Opus 5.5 上会 400**——从 Opus 5 迁上来的代码要改用 strict tool use。

**Opus 5 时代的实测选型**（Opus 5 vs Sonnet 5，参考 [Anthropic Blog · Choosing a Claude model](https://claude.com/blog/claude-model-and-effort-level-in-claude-code)，访问于 2026-08-06）：

| 任务 | Sonnet 5 表现 | Opus 5 表现 |
| --- | --- | --- |
| 大型陌生代码库 debug | 多次循环 + 漏读文件 | 一次定位根因 |
| 多文件架构重构 | 给出方向但要反复 prompt | 直接给可执行方案 |
| 长链多步 agent（10+ tool call） | 走 15-20 步 + 中途验证丢失 | 走 8-12 步且自查 |
| 简单 Q&A / 文档总结 | 表现良好 | 表现良好（**不该升**） |

**再上一代**：Opus 4.8 / 4.7 / 4.6 的 Model ID 是 `claude-opus-4-8` / `-4-7` / `-4-6`，同为 1M / 128k、$5 / $25、缓存读 $0.50，退役承诺分别不早于 2027-05-28 / 04-16 / 02-05。完整生命周期表见 [模型 ID 与定价](./model-ids)。

## 参考

- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-11-13）
- [Anthropic Docs · Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)（访问于 2026-11-13）
- [Anthropic Docs · Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（访问于 2026-11-13）
- [Anthropic Docs · Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)（访问于 2026-11-13）
- [Anthropic Docs · Effort](https://platform.claude.com/docs/en/build-with-claude/effort)（访问于 2026-11-13）
- [Anthropic Docs · Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)（访问于 2026-11-13）
- [Claude Code · Model configuration](https://code.claude.com/docs/en/model-config)（访问于 2026-11-13）
- [Anthropic Docs · Messages API](https://platform.claude.com/docs/en/api/messages)（访问于 2026-08-06）
- [模型 ID 与定价](./model-ids)
- [模型家族总览](/claude-capabilities/models/overview)
- [Sonnet 5.5 对照](./sonnet)
- [CLI 视角选型](/claude-code/basics/model-selection)

## 下一步

- 日常主力选型 → [Sonnet 5.5](./sonnet)
- 批量 / 延迟敏感 → [Haiku 5.5](./haiku)
- API 调用细节 → [Messages API](/claude-capabilities/api/messages)

## 如果你想

- 详细成本计算 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)
- Prompt caching 怎么搭 → [Prompt Caching](/claude-capabilities/api/prompt-caching)
- 长链 agent 场景 → [Fable 5.2](./fable)
