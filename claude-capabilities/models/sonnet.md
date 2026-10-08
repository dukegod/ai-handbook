---
title: Sonnet 5
description: '上一代主力日常模型；Model ID `claude-sonnet-5`；1M context；$2 / $10 已是标准价，当前主力已换代为 Sonnet 5.5'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-08
verifiedWith:
  claudeCode: 2.1.284
  model: claude-sonnet-5-5
  modelOverview: 'https://platform.claude.com/docs/en/about-claude/models/overview'
  pricing: 'https://platform.claude.com/docs/en/about-claude/pricing'
  deprecations: 'https://platform.claude.com/docs/en/about-claude/model-deprecations'
  accessedAt: 2026-10-08
---

# Sonnet 5

> ⚠️ **本页讲的是上一代 Sonnet 5**。当前主力已换代为 **Sonnet 5.5**（`claude-sonnet-5-5`，2026-09-28 发布）。Sonnet 5 仍可调用，状态 Active，退役承诺不早于 2027-06-30。

> **TL;DR**：Sonnet 5 = 「really good generalist」——`claude-sonnet-5`，1M context，**$2 / $10 per 1M token**。日常 80% 编程与对话的首选，把 cache_control 用对、用 Haiku 混搭是省钱关键。

**Sonnet 5.5 与 Sonnet 5 的关键差异**（[Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) 与 [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)，访问于 2026-10-08）：

| | Sonnet 5.5（当前） | Sonnet 5（上一代） |
| --- | --- | --- |
| Model ID | `claude-sonnet-5-5` | `claude-sonnet-5` |
| 输入 / 输出 | $2 / $10 | $2 / $10（**已是标准价**） |
| 缓存读 | **$0.10（0.05x）** | $0.20（0.1x） |
| Context / Max output | 1M / 128k | 1M / 128k |
| 相对延迟 | Fast | Fast |
| 默认 effort | `high` | — |
| 关掉前置思考 | `thinking: {"type": "between_tools"}`（`high` 及以下 effort） | — |
| `tool_choice: any / tool` | ❌ 400 | 支持 |

> ⚠️ **价格陷阱已解除**：Sonnet 5 上线时的 $2 / $10 原是「introductory pricing，截至 2026-08-31」。官方定价页脚注明确写着——**该价格已转为标准价**，原定 2026-09-01 上调到 $3 / $15 **不会发生**。仓库此前把「9 月起实际多花 50%」写成常见坑，**该结论现已作废**。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 最小调用示例（与 Opus 5 同 API，model 字段换 ID）
- 1M context 是默认行为——不需要 `[1m]` 后缀
- Introductory pricing 时间窗与怎么算
- Prompt caching 命中率优化（5 个常见错误）
- Sub-agent 编排：Sonnet 5 主 + Haiku 4.5 sub 的混搭模式
- 何时该升 Opus 5 / 何时该降 Haiku 4.5

## 一、最小调用示例

API 调用结构与 [Opus 5](./opus#一最小调用示例) **完全相同**——只是 `model` 字段换 ID：

```python
import anthropic

client = anthropic.Anthropic()

msg = client.messages.create(
    model="claude-sonnet-5",       # ← 唯一区别
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
)
```

**关键认知**：Sonnet 5 / Opus 5 / Fable 5 / Haiku 4.5 是同代 API 协议——切换模型不换代码。详见 [Messages API](/claude-capabilities/api/messages)。

## 二、1M Context 是默认

Sonnet 5 在 Anthropic API 上**永远 1M context**（200k 基础 + prompt caching 扩到 1M）。**不要写** `claude-sonnet-5[1m]`：

```python
# ✅ 正确
client.messages.create(model="claude-sonnet-5", ...)

# ❌ 错——[1m] 后缀是 Sonnet 4.5 时代的写法，Sonnet 5 上是冗余
client.messages.create(model="claude-sonnet-5[1m]", ...)
```

`[1m]` 后缀在 Bedrock / Vertex 等 provider 上可能仍需保留（视 provider 文档），但**Anthropic API 直接调可以省**。

**Auto-compact 触发点**：约 **967k token** 处。可用环境变量调：

```bash
export CLAUDE_CODE_AUTO_COMPACT_WINDOW=800000   # 提前到 800k 触发
```

## 三、Introductory Pricing（限时折扣）

> ⚠️ **本节内容已过时，结论反转**：Sonnet 5 上线时的 **introductory pricing $2 / $10** 截至 **2026-08-31** 到期，但官方定价页明确说明该价格**已转为标准价**，原定 2026-09-01 上调到 $3 / $15 **不会发生**。所以「回到 $3 / $15」这一步**不存在**。

| 阶段 | 输入 $/1M | 输出 $/1M |
| --- | :---: | :---: |
| Introductory（截至 2026-08-31） | $2 | $10 |
| **标准价（当前）** | **$2** | **$10** |
| ~~原计划 2026-09-01 上调~~ | ~~$3~~ | ~~$15~~ **不执行** |

**缓存读另有一处变化**：Sonnet 5.5 的 prompt cache 读取价在 **2026-10-07 从 $0.20 降到 $0.10 / MTok**（0.05x 取代 0.1x），写侧与其他价格不变。Sonnet 5 本身仍是 $0.20。

**生产环境用法**：

```python
# 用环境变量 / settings 集中管 model id，方便后续批量调价
# settings.json
{ "model": "claude-sonnet-5" }

# CI / 评测脚本里读 env
import os
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")
```

**注意**：定价在 Bedrock / Vertex 等第三方 provider 上**不一定同步**——跨云部署前看各 provider 自己的 pricing 页。

## 四、Prompt Caching 命中率优化

Sonnet 5 默认对每个请求都做 prompt caching（[官方自动开启](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)）。命中 cache 读价格是基础价的 **10%**——命中率从 30% 升到 80% 可能让单次成本腰斩。

**5 个常见错误**（按影响排序）：

1. **System prompt 放消息末尾而不是 `system` 字段**——cache_control 默认对 system 字段前 4 块生效，system 放 messages 里不享受
2. **长 system 块之间不分区**——把"角色设定"和"few-shot 示例"拆成两个 block，独立的 cache_control TTL 单独刷
3. **消息体里加时间戳**——`messages[0].content` 包含 `datetime.now()` 会让每请求 cache miss
4. **Tool 定义顺序每次不一样**——Python dict 顺序保留但 JSON 序列化可能乱，固定 schema
5. **Image / PDF 跟在 system 后面**——把可变内容放 messages 末尾，不可变放 system 头部

**典型 Sonnet 5 + cache 实战**：

```python
import anthropic
client = anthropic.Anthropic()

SYSTEM = [
    {
        "type": "text",
        "text": "你是代码审查助手...",
        "cache_control": {"type": "ephemeral"},   # 5 分钟 TTL
    },
    {
        "type": "text",
        "text": "以下是项目代码风格约定...",     # 另一块，单独 cache
        "cache_control": {"type": "ephemeral"},
    },
]

msg = client.messages.create(
    model="claude-sonnet-5",
    system=SYSTEM,                  # ← 放 system 字段（不放在 messages 里）
    max_tokens=2048,
    messages=[{"role": "user", "content": "审查 PR #1234"}],
)
```

详见 [Prompt Caching API 详解](/claude-capabilities/api/prompt-caching)。

## 五、Sub-agent 编排：Sonnet 5 + Haiku 4.5 混搭

Sonnet 5 在 sub-agent 编排中**做主 agent**最划算——Opus 5 太贵、Haiku 4.5 智能不够。典型模式：

```python
import anthropic
client = anthropic.Anthropic()

# 主 agent：Sonnet 5（编排放行决策、最终综合）
# sub-agent：Haiku 4.5（批量小任务：分类、提取、初审）
tools = [
    {"name": "haiku_classify", "description": "对 100 条评论做情感分类（用 Haiku 4.5）", ...},
    {"name": "haiku_summarize", "description": "对 10 篇文章生成 200 字摘要（用 Haiku 4.5）", ...},
    {"name": "opus_plan", "description": "对架构问题调 Opus 5（用 Opus 5）", ...},
]

# 主对话用 Sonnet 5
msg = client.messages.create(
    model="claude-sonnet-5",
    tools=tools,
    messages=[{"role": "user", "content": "分析这 100 条评论的情感分布并给报告"}],
)
```

**成本对比**（同样 100 条评论任务）：

| 模式 | 总成本估算 |
| --- | --- |
| 全 Sonnet 5 | $0.45 |
| 全 Opus 5 | $0.75 |
| **Sonnet 5 主 + Haiku 4.5 sub** | **$0.15** |
| 全 Haiku 4.5 | $0.08（但质量塌方） |

> ⚠️ 上表是 **Sonnet 5 + Haiku 4.5** 组合的成本（页面主题是上一代）。新项目请按 **Sonnet 5.5 + Haiku 5.5** 配比——Haiku 5.5 的单 token 输入价是 Haiku 4.5 的 1/10，sub-agent 这条线的账单结构已经完全不同。见 [Haiku 5.5](./haiku)。

详见 [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)。

## 六、何时该升 / 降

**该升 Opus 5**（[Opus 5 详解](./opus#四opus-5-vs-sonnet-5实测选型)）：
- 大型陌生代码 debug
- 多文件架构重构
- 长链多步 agent（10+ tool call）

**该降 Haiku 4.5**（[Haiku 4.5 详解](./haiku)）：
- 简单批处理（分类、提取、格式化）
- 延迟敏感场景（< 200ms 响应）
- 大量并发 sub-agent

**保持 Sonnet 5**：
- 日常编程、对话、文档总结（80% 场景）
- 中等复杂度的多步任务（5-10 tool call）

## 七、常见坑

**Sonnet 5 上还写 `sonnet[1m]`**

见 [第二节](#二1m-context-是默认)。Anthropic API 上 1M 是默认；`[1m]` 后缀是 Sonnet 4.5 时代产物。

**Introductory pricing 涨价（该坑已不存在）**

原以为 2026-09-01 起从 $2 / $10 涨到 $3 / $15。官方定价页脚注确认**涨价不执行**，$2 / $10 已是标准价。代码里的成本估算不需要按 50% 上调。

**Sub-agent 全用 Sonnet 5 拼成本**

100 个 sub-agent 任务全用 Sonnet 5 比 Sonnet 5 主 + Haiku 4.5 sub 贵 3 倍。混搭是默认模式。

**System prompt 跟 messages 混在一起**

导致 cache miss。**永远**把 system 内容放 `system` 字段、不可变部分加 `cache_control`。

**Alias 在 Bedrock 上解析成 Sonnet 4.5**

跨云部署要显式 pin：`ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5`。

## 参考

- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-10-08）
- [Anthropic Docs · Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)（访问于 2026-10-08）
- [Anthropic Docs · Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)（访问于 2026-08-06）
- [Anthropic Docs · Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（访问于 2026-10-08）
- [Opus 5.5 对照](./opus)
- [Haiku 5.5 对照](./haiku)
- [模型家族总览](/claude-capabilities/models/overview)

## 下一步

- 批量 / 延迟敏感 → [Haiku 5.5](./haiku)
- 长链 agent 专家 → [Fable 5.1](./fable)
- Prompt caching 详解 → [Prompt Caching API](/claude-capabilities/api/prompt-caching)

## 如果你想

- sub-agent 编排省钱模式 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)
- 详细成本与 token 优化 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)
- 选型决策树 → [模型概览 · 选型决策指南](./overview#五选型决策指南)
