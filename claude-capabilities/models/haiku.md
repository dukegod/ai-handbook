---
title: Haiku 5.5
description: '高并发 / 延迟敏感档；Model ID `claude-haiku-5-5`；1M context；按 prompt 长度分档计价 $0.10 / $0.50 起'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-08
verifiedWith:
  claudeCode: 2.1.293
  model: claude-haiku-5-5
  modelOverview: 'https://platform.claude.com/docs/en/about-claude/models/overview'
  modelPage: 'https://platform.claude.com/docs/en/models/haiku-5-5/overview'
  pricing: 'https://platform.claude.com/docs/en/about-claude/pricing'
  deprecations: 'https://platform.claude.com/docs/en/about-claude/model-deprecations'
  releaseNotes: 'https://platform.claude.com/docs/en/release-notes/overview'
  accessedAt: 2026-10-08
---

# Haiku 5.5

> **TL;DR**：Haiku 5.5 = 高并发、延迟敏感档——`claude-haiku-5-5`，**1M context / 128k output**，**from $0.10 / $0.50 per 1M token**（全系最便宜），2026-10-07 发布。分类、提取、路由、subagent 的默认选择。**它是唯一按 prompt 长度分档计费的型号**：prompt 超过 10 万 token，输入输出价各跳 5 倍。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 最小调用示例（与同代 API 协议，仅 model 字段换 ID）
- **分档计价**：为什么同一模型两个价，以及怎么在预算里体现
- Haiku 4.5 → 5.5 的三个 breaking change（`budget_tokens` 失效 / 新分词器 / thinking 默认开）
- 批量任务实战（[Message Batches API](/claude-capabilities/api/message-batches)）
- Sub-agent 编排中做 sub 的角色
- 何时不该用 Haiku

## 一、最小调用示例

```python
import anthropic

client = anthropic.Anthropic()

msg = client.messages.create(
    model="claude-haiku-5-5",        # ← 唯一区别
    max_tokens=1024,
    messages=[{"role": "user", "content": "把这段日志归类为 ERROR / WARN / INFO"}],
)
```

**官方规格**（[Claude Haiku 5.5 模型页](https://platform.claude.com/docs/en/models/haiku-5-5/overview)，访问于 2026-10-08）：

| 项 | 值 |
| --- | --- |
| Context window | 1M tokens |
| Max output | 128K tokens（Batch API 下配 `output-300k-2026-03-24` beta header 可到 300K） |
| Thinking | Adaptive（默认开启，用 `effort` 控深度，默认 `medium`） |
| 相对延迟 | **Fastest**（当前阵容中最快） |
| 知识截止 | Jun 2026 |
| 发布 | 2026-10-07 |
| 退役承诺 | 不早于 2027-10-07 |

其他平台 ID：Bedrock `anthropic.claude-haiku-5-5`；Google Cloud / Microsoft Foundry / Claude Platform on AWS 均用 `claude-haiku-5-5`。

## 二、定价：唯一按 prompt 长度分档的型号

官方价目表把 Haiku 5.5 拆成两行：

| 特征 | prompt ≤ 100,000 tokens | prompt > 100,000 tokens |
| --- | :---: | :---: |
| Input | **$0.10 / MTok** | $0.50 / MTok |
| Output | **$0.50 / MTok** | $2.50 / MTok |
| 5 分钟缓存写 | $0.125 / MTok | $0.625 / MTok |
| 1 小时缓存写 | $0.20 / MTok | $1 / MTok |
| 缓存读（命中） | $0.01 / MTok | $0.05 / MTok |
| Batch 输入 / 输出 | $0.05 / $0.25 | $0.25 / $1.25 |

**分档看的是「单次请求的 prompt 长度」，不是会话累计。** 一条 50 token 的日志分类走便宜档；一份 30 万 token 的长文档摘要走贵档——哪怕它也是"分类任务"。

> 这一点值得单独记住：**Haiku 5.5 不在官方「1M 上下文按标准价计费」的豁免名单里**（其他 4.6 及之后模型都在，唯一的例外就是它）。做超长上下文任务前，先量 prompt 长度再定预算。

**成本量级对照**（每条评论 50 输入 + 20 输出 token，共 100 万条 = 输入 5000 万 + 输出 2000 万 token）：

| 模式 | 输入成本 | 输出成本 | 合计 |
| --- | :---: | :---: | :---: |
| **全 Haiku 5.5**（每次请求都是单条短评论，走便宜档） | $5 | $10 | **$15** |
| 全 Haiku 5.5 + Batch API | $2.50 | $5 | $7.50 |
| 全 Sonnet 5.5 | $100 | $200 | $300 |

对比上一代 Haiku 4.5（$1 / $5），Haiku 5.5 的单 token 价格又降了 10 倍——但它换来了新分词器，同样文本约多 30% token，两者部分抵消。

## 三、Haiku 4.5 → 5.5：三个 breaking change

官方 release notes（2026-10-07）明确点名："Code written for Claude Haiku 4.5 can break on Claude Haiku 5.5."

| 变更 | 后果 |
| --- | --- |
| **手动 extended thinking（`budget_tokens`）返回 400** | `thinking={"type": "enabled", "budget_tokens": 2048}` 直接报错 |
| **adaptive thinking 默认开启** | 响应可能以 `thinking` 块开头，解析代码要能吃这个形态 |
| **换用新分词器** | 同样文本比 Haiku 4.5 多约 **30%** token，预算与 cache 命中率计算都要重算 |

**Haiku 4.5 现在什么状态**（[Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)，访问于 2026-10-08）：仍是 **Active**——**没有**被标 Deprecated，退役承诺仍是「不早于 2026-10-15」。Haiku 5.5 的发布**没有**顺延或提前这个日期。

```python
# ❌ Haiku 4.5 的写法，在 5.5 上 400
thinking={"type": "enabled", "budget_tokens": 2048}

# ✅ 5.5：省略 thinking，用 effort 控深度
msg = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=1024,
    output_config={"effort": "medium"},   # 默认就是 medium
    messages=[{"role": "user", "content": "..."}],
)
```

> 另外注意：`temperature` / `top_p` / `top_k` 传非默认值一律 400（4.7 及之后模型的通用规则）。

## 四、批量任务实战

Haiku 5.5 是 [Message Batches API](/claude-capabilities/api/message-batches) 的甜区——50% 折扣换 24h 内处理：

```python
# 提交 batch
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"comment-{i}",
            "params": {
                "model": "claude-haiku-5-5",
                "max_tokens": 64,
                "messages": [{"role": "user", "content": f"分类：{comment}"}],
            },
        }
        for i, comment in enumerate(comments)
    ]
)

# 24h 内查结果
result = client.messages.batches.retrieve(batch.id)
```

**batch vs online 决策**：

| 场景 | 推荐 |
| --- | --- |
| 实时对话（< 1s 响应） | **Online**（streaming） |
| 用户提交后等结果（5-30s） | Online |
| 离线批处理（万条以上、可等 24h） | **Batch**（50% off） |
| 跨小时 ETL 流水线 | Batch |

## 五、Sub-agent 编排：Haiku 5.5 做 sub

[Subagent 编排](/claude-code/subagents-and-workflows/workflow-orchestration) 中 Haiku 是最常用的 sub-agent 模型——主 agent 用 Sonnet 5.5 / Opus 5.5，sub-agent 全部用 Haiku 5.5。

```
主 agent（Sonnet 5.5）
  ├─ sub: 文章分批（Haiku 5.5，摘要）
  ├─ sub: 情感分析（Haiku 5.5，评论）
  └─ sub: 实体提取（Haiku 5.5，段落）
→ 主 agent 综合
```

> Claude Code 里 `haiku` alias 在 Anthropic API 上已解析到 **Haiku 5.5**，但需要 **v2.1.293+**；其他 provider（Bedrock / Google Cloud / Foundry / Claude Platform on AWS）仍解析到 **Haiku 4.5**。跨云部署记得显式 pin。

## 六、何时不该用 Haiku

1. **复杂多步 agent 规划**——主 agent 别用它
2. **架构决策 / 根因分析**——深度推理不够，走 [Opus 5.5](./opus) 或 [Fable 5.1](./fable)
3. **超长文档摘要**——1M context 够用，但要按第三节确认 prompt 落在哪一档，否则成本可能翻 5 倍
4. **需要 Fable 5.1 那种长程自主能力**——Haiku 做不了长链专家活

## 七、常见坑

**把 Haiku 5.5 当成"便宜版 Sonnet"估超长上下文预算**

先量 prompt 是否超过 100k token，再决定用哪档价。这是最容易低估的一项。

**从 Haiku 4.5 直接改 model 字段就上线**

`budget_tokens` 会 400，thinking 块形态变了，token 数也涨了 30%。三项都要改。

**Max output 设 300k 却没带 beta header**

300k 输出只在 Message Batches API + `output-300k-2026-03-24` beta header 下可用，同步接口上限就是 128k。

**以为 `haiku` alias 在哪都指向最新**

只有 Anthropic API 指向 Haiku 5.5；Bedrock / Google Cloud / Foundry 仍是 Haiku 4.5。

**分类 / 提取这类活全塞给一个超长 prompt**

分档是按单次请求算的。把 1 万条评论拼成一个请求会直接跳到贵档；拆成短请求反而更便宜。

## 参考

- [Anthropic Docs · Claude Haiku 5.5](https://platform.claude.com/docs/en/models/haiku-5-5/overview)（访问于 2026-10-08）
- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-10-08）
- [Anthropic Docs · Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)（访问于 2026-10-08）
- [Anthropic Docs · Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（访问于 2026-10-08）
- [Anthropic Docs · Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview)（访问于 2026-10-08）
- [Anthropic Docs · Message Batches API](https://platform.claude.com/docs/en/api/messages/batches)（访问于 2026-08-06）
- [模型家族总览](/claude-capabilities/models/overview)
- [Sonnet 5.5 对照](./sonnet)
- [Opus 5.5 对照](./opus)

## 下一步

- 长链 agent 专家 → [Fable 5.1](./fable)
- API 视角选型决策 → [模型概览 · 选型决策指南](./overview#五选型决策指南)
- Batch API 详解 → [Message Batches API](/claude-capabilities/api/message-batches)

## 如果你想

- 思考模式详解 → [Extended Thinking 详解](/claude-capabilities/core/extended-thinking)
- Sub-agent 编排模式 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)
