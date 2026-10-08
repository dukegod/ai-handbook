---
title: 模型 ID 与定价
description: 全部 Claude 模型的 ID、context 长度、$/1M token、生命周期状态（截至 2026-10-08）
audience: beginner
difficulty: 🟢
status: planned
lastUpdated: 2026-10-08
verifiedWith:
  sources:
    - name: Anthropic 模型总览
      url: https://platform.claude.com/docs/en/about-claude/models/overview
      accessedAt: 2026-10-08
    - name: Claude 模型退役与生命周期
      url: https://platform.claude.com/docs/en/about-claude/model-deprecations
      accessedAt: 2026-10-08
    - name: Claude 定价文档
      url: https://platform.claude.com/docs/en/about-claude/pricing
      accessedAt: 2026-10-08
    - name: Claude Haiku 5.5 模型页
      url: https://platform.claude.com/docs/en/models/haiku-5-5/overview
      accessedAt: 2026-10-08
---

# 模型 ID 与定价

> 🚧 本页规划中，属于 Claude Handbook v0.1 路线图。下方只放**已核实**的速查表，完整版待补。详见 [roadmap](/contributing/roadmap)。

## 当前 4 条主力线（截至 2026-10-08）

| 模型 | Claude API ID | Bedrock ID | Context | Max output | Input / Output（$/MTok） | 缓存读 | 思考 | 默认 effort | 退役承诺 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Fable 5.1** | `claude-fable-5-1` | `anthropic.claude-fable-5-1` | 1M | 128k | $10 / $50 | $0.25 | Adaptive（总是开） | `high` | 不早于 2027-09-01 |
| **Opus 5.5** | `claude-opus-5-5` | `anthropic.claude-opus-5-5` | 1M | 128k | $4 / $20 | $0.20 | Adaptive（总是开） | `medium` | 不早于 2027-09-22 |
| **Sonnet 5.5** | `claude-sonnet-5-5` | `anthropic.claude-sonnet-5-5` | 1M | 128k | $2 / $10 | $0.10 | Adaptive | `high` | 不早于 2027-09-28 |
| **Haiku 5.5** | `claude-haiku-5-5` | `anthropic.claude-haiku-5-5` | 1M | 128k | $0.10 / $0.50 † | $0.01 | Adaptive | `medium` | 不早于 2027-10-07 |

† Haiku 5.5 按 prompt 长度分档：上表是 **prompt ≤ 100k token** 的档位。超过 10 万 token 时输入 $0.50、输出 $2.50、缓存读 $0.05。**它是全系唯一按 prompt 长度分档计费的型号**。

> Google Cloud / Microsoft Foundry / Claude Platform on AWS 三个平台用的就是 Claude API ID（无 `anthropic.` 前缀），不需要额外记一套。

## 仍可调用的上一代

引 [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)（访问于 2026-10-08）：

| Model ID | 状态 | 退役承诺 |
| --- | --- | --- |
| `claude-haiku-4-5-20251001` | Active | 不早于 2026-10-15 |
| `claude-fable-5` | Active | 不早于 2027-06-09 |
| `claude-opus-5` | Active | 不早于 2027-07-24 |
| `claude-sonnet-5` | Active | 不早于 2027-06-30 |
| `claude-opus-4-8` / `claude-opus-4-7` / `claude-opus-4-6` | Active | 2027-05-28 / 04-16 / 02-05 |
| `claude-opus-4-5-20251101` | Active | 不早于 2026-11-24 |
| `claude-sonnet-4-6` | Active | 不早于 2027-02-17 |
| `claude-sonnet-4-5-20250929` | **Deprecated**（2026-09-30 公告） | **2026-11-30 退役** → 迁移到 `claude-sonnet-5-5` |
| `claude-mythos-preview` | Deprecated（2026-06-09） | 待定 |

**已 Retired**（请求会失败）：`claude-opus-4-1-20250805`、`claude-opus-4-20250514`、`claude-sonnet-4-20250514`、`claude-3-7-sonnet-20250219`、`claude-3-5-haiku-20241022`、`claude-3-haiku-20240307`。

> ⚠️ **两页口径不一致**：[Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) 把上一代归入「Legacy models (still available)」，[Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) 的状态列至今仍标 **Active**。判断"能不能调"看后者，判断"该不该用"看前者。

## alias 怎么解析

Anthropic API 上 `opus` / `sonnet` / `haiku` / `fable` 自动解析到当前最新版本，老代码无需改 Model ID。跨 provider 部署必须显式 pin——完整对照表见 [Claude Code · 模型选择 · Alias 在不同 provider 上](/claude-code/basics/model-selection#alias-在不同-provider-上解析不同-重要)。

**新代码直接写完整 ID**（如 `claude-sonnet-5-5`）。4.6 世代起 alias 本身就是快照，显式写 ID 才能表达"我要这个版本"。

## 参考

- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-10-08）
- [Anthropic Docs · Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)（访问于 2026-10-08）
- [Anthropic Docs · Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（访问于 2026-10-08）
- [Anthropic Docs · Claude Haiku 5.5](https://platform.claude.com/docs/en/models/haiku-5-5/overview)（访问于 2026-10-08）
- [模型家族总览](/claude-capabilities/models/overview)

## 下一步

- 选型决策 → [模型概览](/claude-capabilities/models/overview)
- CLI 视角 alias / effort → [Claude Code · 模型选择](/claude-code/basics/model-selection)

## 如果你想

- 成本计算细节 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)
- 各模型详解 → [Opus 5.5](./opus) / [Sonnet 5.5](./sonnet) / [Haiku 5.5](./haiku) / [Fable 5.1](./fable)
