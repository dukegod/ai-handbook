---
title: Haiku 4.5
description: '速度优先 + 接近前沿智能；Model ID `claude-haiku-4-5`；200k context；定位 "fastest near-frontier"'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-06
verifiedWith:
  claudeCode: 2.1.220
  model: claude-haiku-4-5
  modelOverview: 'https://platform.claude.com/docs/en/about-claude/models/overview'
  pricing: 'https://platform.claude.com/docs/en/about-claude/pricing'
  accessedAt: 2026-08-06
---

# Haiku 4.5

> **TL;DR**：Haiku 4.5 = 「fastest near-frontier」——`claude-haiku-4-5`，200k context，**$1 / $5 per 1M token**（最便宜）。批量任务、sub-agent 编排、延迟敏感场景首选；走 **legacy extended thinking**（与 Opus 5 / Sonnet 5 的 adaptive thinking 是不同 API 行为）。

⏱ 预计阅读时间：4 分钟

## 你能在这里学到

- 最小调用示例（与同代 API 协议，仅 model 字段换 ID）
- 200k context 限制场景与边界
- Legacy extended thinking 的 `budget_tokens` 实战（**这是 Haiku 4.5 独有的 API 形态**）
- 批量任务实战（[Message Batches API](/claude-capabilities/api/message-batches)）
- Sub-agent 编排中做 sub 的角色
- 何时不该用 Haiku（深度推理、多步规划、复杂代码生成）

## 一、最小调用示例

API 调用结构与 Opus 5 / Sonnet 5 完全相同——同代 API 协议：

```python
import anthropic

client = anthropic.Anthropic()

msg = client.messages.create(
    model="claude-haiku-4-5",       # ← 唯一区别
    max_tokens=1024,
    messages=[{"role": "user", "content": "把这段日志归类为 ERROR / WARN / INFO"}],
)
```

**注意两点差异**：
- **200k context**（不是 1M）—— 超出 200k 输入会 400 错误
- **64k max output**（不是 128k）—— 设超过 64k 会被 clamp

## 二、5 倍便宜的实战对比

| 模型 | 输入 $/1M | 输出 $/1M | Haiku 4.5 是其倍数 |
| --- | :---: | :---: | --- |
| **Haiku 4.5** | **$1** | **$5** | 1×（基准） |
| Sonnet 5 | $3 | $15 | 3× / 3× |
| Opus 5 | $5 | $25 | 5× / 5× |
| Fable 5 | $10 | $50 | 10× / 10× |

**典型场景**：100 万条评论做情感分类

| 模式 | 总成本估算 | 质量 |
| --- | --- | --- |
| 全 Sonnet 5 | $3.00 | 高（过头） |
| 全 Haiku 4.5 | **$1.00** | 良好（足够） |

**反直觉**：Haiku 4.5 在「分类、提取、格式化、简单 Q&A」上质量与 Sonnet 5 差距 < 5%，但价格是 1/3——**这类任务一律用 Haiku 4.5**。

## 三、Legacy Extended Thinking（Haiku 4.5 独有）

Haiku 4.5 **不支持** adaptive thinking——它走 legacy extended thinking，显式传 `thinking` 参数控制思考深度：

```python
msg = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=4096,
    thinking={
        "type": "enabled",
        "budget_tokens": 2048,       # ← 给思考的 token 预算
    },
    messages=[{"role": "user", "content": "..."}],
)
```

**关键参数**：

| 参数 | 含义 | 推荐范围 |
| --- | --- | --- |
| `type` | 固定 `"enabled"` | — |
| `budget_tokens` | 思考的 token 上限 | 1024-8192 |

**与 Opus 5 / Sonnet 5 的对比**：

| 模型 | thinking 行为 |
| --- | --- |
| **Fable 5** | Adaptive，总开，**不能关** |
| **Opus 5** | Adaptive，总开，不能显式关 |
| **Sonnet 5** | Adaptive，总开，不能显式关 |
| **Haiku 4.5** | **Legacy `budget_tokens` 显式控制**——更可控但要手动调 |

**`budget_tokens` 怎么选**：

```
简单分类 / 格式化:       1024
中等推理:               2048-4096
复杂多步（但仍在 Haiku 范畴）:  8192
```

详见 [Extended Thinking 详解](/claude-capabilities/core/extended-thinking)。

## 四、批量任务实战

Haiku 4.5 是 [Message Batches API](/claude-capabilities/api/message-batches) 的甜区——50% 价格折扣换 24h 内处理：

```python
# 提交 batch
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"comment-{i}",
            "params": {
                "model": "claude-haiku-4-5",
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

## 五、Sub-agent 编排：Haiku 4.5 做 sub

[Subagent 编排](/claude-code/subagents-and-workflows/workflow-orchestration) 中 Haiku 4.5 是最常用的 sub-agent 模型——主 agent 用 Sonnet 5 / Opus 5，sub-agent 全部用 Haiku 4.5。

**典型工作流**（研究 100 篇文章）：

```
主 agent（Sonnet 5）
  ├─ sub: 文章分批（Haiku 4.5，1000 篇文章 × 200 字摘要）
  ├─ sub: 情感分析（Haiku 4.5，1000 条评论）
  └─ sub: 实体提取（Haiku 4.5，1000 个段落）
→ 主 agent 综合
```

**成本对比**（同任务）：

| 模式 | 总成本 |
| --- | --- |
| 全 Sonnet 5 | $0.45 |
| Sonnet 主 + Haiku sub | **$0.15** |
| 全 Haiku 4.5 | $0.08（但综合质量塌方） |

详见 [Sonnet 5 · Sub-agent 混搭模式](./sonnet#五sub-agent-编排sonnet-5--haiku-45-混搭)。

## 六、何时不该用 Haiku 4.5

1. **复杂多步 agent 规划**——Haiku 在 5+ 步 tool call 上易"忘上下文"，主 agent 别用它
2. **陌生代码 debug**——模式识别弱，[Opus 5](./opus#四opus-5-vs-sonnet-5实测选型) 更稳
3. **架构决策 / 根因分析**——深度推理不够，走 [Opus 5](./opus) 或 [Fable 5](./fable)
4. **长文档（> 200k）摘要**——context 不够，先切片或用 Sonnet 5
5. **要 adaptive thinking 的智能调度**——Haiku 4.5 不支持，传 thinking 参数会报 schema 错

## 七、常见坑

**给 Haiku 4.5 加 adaptive thinking**

```python
# ❌ 错
thinking={"type": "adaptive"}

# ✅ 对
thinking={"type": "enabled", "budget_tokens": 2048}
```

**Input 超过 200k 不切片**

Sonnet 5 / Opus 5 上 1M context 让你忘了切——Haiku 4.5 仍然 200k 上限，**超出会 400**。

**Max output 设 128k**

Haiku 4.5 max output 是 **64k**。设 128k 会被静默 clamp 到 64k，且 billing 仍按你设的 128k 计（部分 SDK 行为），需注意。

**用 Haiku 4.5 做"研究 + 写作" 一体化任务**

研究 sub 可以是 Haiku 4.5，**但最终综合 / 写作必须是主 agent 模型**（Sonnet 5 或 Opus 5）—— Haiku 的"综合"质量塌方。

## 参考

- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-08-06）
- [Anthropic Docs · Message Batches API](https://platform.claude.com/docs/en/api/messages/batches)（访问于 2026-08-06）
- [Anthropic Docs · Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)（访问于 2026-08-06）
- [模型家族总览](/claude-capabilities/models/overview)
- [Sonnet 5 对照](./sonnet)
- [Opus 5 对照](./opus)

## 下一步

- 长链 agent 专家 → [Fable 5](./fable)
- API 视角选型决策 → [模型概览 · 选型决策指南](./overview#五选型决策指南)
- Batch API 详解 → [Message Batches API](/claude-capabilities/api/message-batches)

## 如果你想

- Extended Thinking 完整用法 → [Extended Thinking 详解](/claude-capabilities/core/extended-thinking)
- Sub-agent 编排模式 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)
