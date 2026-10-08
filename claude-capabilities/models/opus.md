---
title: Opus 5
description: '上一代旗舰推理模型；Model ID `claude-opus-5`；1M context；当前旗舰已换代为 Opus 5.5'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-08
verifiedWith:
  claudeCode: 2.1.280
  model: claude-opus-5-5
  modelOverview: 'https://platform.claude.com/docs/en/about-claude/models/overview'
  modelConfig: 'https://code.claude.com/docs/en/model-config'
  pricing: 'https://platform.claude.com/docs/en/about-claude/pricing'
  deprecations: 'https://platform.claude.com/docs/en/about-claude/model-deprecations'
  accessedAt: 2026-10-08
---

# Opus 5

> ⚠️ **本页讲的是上一代 Opus 5**。当前旗舰已换代为 **Opus 5.5**（`claude-opus-5-5`，2026-09-22 发布），官方选型指引是「绝大多数负载从 Opus 5.5 起步」。Opus 5 仍可调用，状态 Active，退役承诺不早于 2027-07-24。

> **TL;DR**：Opus 5 = 「the expert」——`claude-opus-5`，1M context / 128k output，**$5 / $25 per 1M token**。复杂 agentic 编程、陌生代码、架构决策的稳妥选择；新项目请直接上 Opus 5.5（$4 / $20，**便宜 20%**）。

**Opus 5.5 与 Opus 5 的关键差异**（[Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)，访问于 2026-10-08）：

| | Opus 5.5（当前） | Opus 5（上一代） |
| --- | --- | --- |
| Model ID | `claude-opus-5-5` | `claude-opus-5` |
| 输入 / 输出 | $4 / $20 | $5 / $25 |
| 缓存读 | $0.20（0.05x） | $0.50（0.1x） |
| Context / Max output | 1M / 128k | 1M / 128k |
| 思考 | Adaptive，**总是开、不可关** | Adaptive，不可关 |
| 默认 effort | `medium` | — |
| `tool_choice: any / tool` | ❌ 400 | 支持 |
| Fast mode（research preview） | ✅ $8 / $40 | ✅ $10 / $50 |

其余按「一、最小调用示例」到「七、常见坑」的内容适用于两者——把 `model` 换成 `claude-opus-5-5` 即可，唯一要额外处理的是 Opus 5.5 上 `thinking` 与 `tool_choice` 的限制。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 最小调用示例（Python + TypeScript）
- 关键参数速查（adaptive thinking / max_tokens / system / tool use）
- Adaptive Thinking 在 Opus 5 上的行为（与 Fable 5 / Haiku 4.5 的差异）
- 与 Sonnet 5 的实测选型（不是「更聪明」而是「少 X 步」）
- 何时**不该**用 Opus 5（成本反直觉 + 批量场景）

## 一、最小调用示例

**Python**（[anthropic-sdk-python](https://github.com/anthropics/anthropic-sdk-python)）：

```python
import anthropic

client = anthropic.Anthropic()

msg = client.messages.create(
    model="claude-opus-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "解释这段 Python 代码为什么慢：..."}
    ],
)
print(msg.content[0].text)
```

**TypeScript**（[@anthropic-ai/sdk](https://github.com/anthropics/anthropic-sdk-typescript)）：

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const msg = await client.messages.create({
  model: "claude-opus-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "解释这段 Python 代码为什么慢：..." }],
});
console.log(msg.content[0].text);
```

**Streaming**（长输出场景必备）：

```python
with client.messages.stream(
    model="claude-opus-5",
    max_tokens=4096,
    messages=[{"role": "user", "content": "..."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## 二、关键参数速查

| 参数 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `model` | `str` | — | `claude-opus-5`（当前旗舰 `claude-opus-5-5`） |
| `max_tokens` | `int` | — | 必填；上限 **128000** |
| `system` | `str` \| list | — | System prompt；可用缓存（见 [Prompt Caching](/claude-capabilities/api/prompt-caching)） |
| `temperature` / `top_p` / `top_k` | — | — | **Opus 4.7 及之后模型传非默认值返回 400**，别设 |
| `thinking` | `dict` | 省略 | Opus 上是 always-on adaptive thinking，显式传 `disabled` / `enabled` 都会 400 |
| `output_config.effort` | `str` | `medium`（Opus 5.5） | 控思考深度，见 [Effort level](/claude-code/basics/model-selection#四effort-levels-与-effort) |
| `tools` | `list[dict]` | — | 工具定义（[Tool Use API 协议](/claude-capabilities/core/tool-use)） |
| `metadata` | `dict` | — | 自定义追踪字段（user_id / session_id） |

> 完整字段以 [Anthropic Docs · Messages API](https://platform.claude.com/docs/en/api/messages) 为准。

## 三、Adaptive Thinking：Opus 5 的"思考"行为

Opus 5（与 Fable 5 / Sonnet 5 同代）走 **adaptive thinking**——模型自动决定每次请求"想多深"，**不需要**也不支持 `thinking={"type": "enabled", "budget_tokens": N}` 这种 legacy extended thinking 显式传 budget。

**与其他模型的差异**：

| 模型 | thinking 行为 |
| --- | --- |
| **Fable 5.1** | Adaptive thinking **总是开**，且**不能关**（specialist 设计） |
| **Opus 5.5 / Opus 5** | Adaptive thinking 总是开（不能显式关） |
| **Sonnet 5.5** | Adaptive；`high` 及以下 effort 可用 `between_tools` 关掉前置思考 |
| **Haiku 5.5** | Adaptive，默认开，默认 effort `medium` |
| **Haiku 4.5** | **不支持** adaptive；用 legacy extended thinking + `budget_tokens` |

> 想显式控制"想多深"——走 [Effort level](/claude-code/basics/model-selection#四effort-levels-与-effort)。当前 API 上的默认 effort：Opus 5.5 与 Haiku 5.5 是 `medium`，Sonnet 5.5 与 Fable 5.1 是 `high`。

## 四、Opus 5 vs Sonnet 5：实测选型

**不是"Opus 更聪明"，而是"Opus 少步数"**。

按 Anthropic 官方数据与社区实测（参考 [Anthropic Blog · Choosing a Claude model](https://claude.com/blog/claude-model-and-effort-level-in-claude-code)，访问于 2026-08-06）：

| 任务 | Sonnet 5 表现 | Opus 5 表现 | 何时该升 Opus |
| --- | --- | --- | --- |
| 日常 80% 编程 | 表现良好 | 同样能完成 | 不该升——成本翻倍 |
| 大型陌生代码库 debug | 多次循环 + 漏读文件 | 一次定位根因 | 该升 |
| 多文件架构重构 | 给出方向但要反复 prompt | 直接给可执行方案 | 该升 |
| 长链多步 agent（10+ tool call） | 走 15-20 步 + 中途验证丢失 | 走 8-12 步且自查 | 该升 |
| 简单 Q&A / 文档总结 | 表现良好 | 表现良好 | **不该升** |

**成本反直觉**：

```
Sonnet 5:  $3/M input  × 20 步 × 50k input  =  $3.00
Opus 5:    $5/M input  × 10 步 × 30k input  =  $1.50
                              → Opus 总成本反而更低
```

详见 [成本与 Token 管理](/claude-code/basics/cost-and-tokens) 的「少步数大模型」段落。

## 五、何时**不该**用 Opus 5

1. **简单批处理 / 分类 / 提取**——用 [Haiku 5.5](./haiku)（$0.10 / $0.50 起，比 Opus 5 便宜 50 倍）
2. **日常 80% 编程与对话**——[Sonnet 5.5](./sonnet) 够用
3. **超长链 agent**（50+ tool call 跨小时）——直接上 [Fable 5.1](./fable)
4. **Function calling 大量并发**——Opus 延迟比 Haiku 高一个量级，subagent 编排时混搭用
5. **Prompt caching 命中率 < 30%**——缓存不命中时 Opus 的高单价不划算

## 六、常见坑

**Model ID 写成 `claude-opus-4-8`**

历史版本 ID，新代码会 404。Opus 5 必须用 `claude-opus-5`；想 pin 老版本显式 `claude-opus-4-8`（见 [概览 · Legacy 模型索引](/claude-capabilities/models/overview#六legacy-模型索引)）。

**max_tokens 设了 128000 但实际只输出几千 token**

Opus 5 max_tokens 上限 128k 是 **output** 限制，不是目标；设 128k 不会让模型"努力写更多"，反而增加首 token 延迟。按场景给合理值（短回答 256-1024，长文 4096-8192）。

**Temperature 设 0 期望 100% 复现**

即使是 0，跨 provider / 跨 region 也可能有微小浮点差。要严格复现 prompt + `model` + `temperature=0` + 相同 cache_control。

**在 Subagent 里强制全用 Opus 5**

[Subagent 编排](/claude-code/subagents-and-workflows/workflow-orchestration) 时主 agent 用 Opus 5 + subagent 用 Haiku 4.5 是常见省钱模式；全用 Opus 5 反而拖慢整体。

## 参考

- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-10-08）
- [Anthropic Docs · Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)（访问于 2026-10-08）
- [Anthropic Docs · Messages API](https://platform.claude.com/docs/en/api/messages)（访问于 2026-08-06）
- [Anthropic Docs · Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（访问于 2026-10-08）
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
- 长链 agent 场景 → [Fable 5.1](./fable)
