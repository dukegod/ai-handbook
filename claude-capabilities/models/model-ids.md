---
title: 模型 ID 与定价
description: '全部 Claude 模型的 ID、context 长度、$/1M token、缓存价与生命周期状态（截至 2026-11-13）'
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-11-13
verifiedWith:
  sources:
    - name: Anthropic 模型总览
      url: https://platform.claude.com/docs/en/about-claude/models/overview
      accessedAt: 2026-11-13
    - name: Claude 模型退役与生命周期
      url: https://platform.claude.com/docs/en/about-claude/model-deprecations
      accessedAt: 2026-11-13
    - name: Anthropic 定价
      url: https://platform.claude.com/docs/en/about-claude/pricing
      accessedAt: 2026-11-13
    - name: Claude Code 模型配置
      url: https://code.claude.com/docs/en/model-config
      accessedAt: 2026-11-13
---

# 模型 ID 与定价

> **TL;DR**：当前 4 条主力线是 **Fable 5.2**（长链 agent 专家）/ **Opus 5.5**（长跑 agentic 编码）/ **Sonnet 5.5**（速度与智能平衡）/ **Haiku 5.5**（高并发延迟敏感）。新代码直接写完整 ID；alias 会随 provider 和时间漂移。

本页是查表用的速查页——**先在这里确认要用的模型 ID 和价格，再去 [模型概览](./overview) 看选型逻辑**。

⏱ 预计阅读时间：3 分钟

## 当前 4 条主力线（截至 2026-11-13）

| 模型 | Claude API ID | Context | Max output | 输入 / 输出（$/MTok） | 缓存写 5m / 1h | 缓存读 | 思考 | 默认 effort | 退役承诺 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Fable 5.2** | `claude-fable-5-2` | 1M | 128k | $8 / $40 | $10 / $16 | $0.20 | Adaptive（总是开） | `high` | 不早于 2027-11-09 |
| **Opus 5.5** | `claude-opus-5-5` | 1M | 128k | $4 / $20 | $5 / $8 | $0.20 | Adaptive（总是开） | `medium` | 不早于 2027-09-22 |
| **Sonnet 5.5** | `claude-sonnet-5-5` | 1M | 128k | $2 / $10 | $2.50 / $4 | $0.10 | Adaptive | `high` | 不早于 2027-09-28 |
| **Haiku 5.5** | `claude-haiku-5-5` | 1M | 128k | $0.10 / $0.50 † | $0.125 / $0.20 | $0.01 | Adaptive | `medium` | 不早于 2027-10-07 |

† Haiku 5.5 按 prompt 长度分档：上表是 **prompt ≤ 100k token** 的档位。超过 10 万 token 时输入 $0.50、输出 $2.50、缓存写 $0.625 / $1、缓存读 $0.05。**它是全系唯一按 prompt 长度分档计费的型号**，且分档按**单次请求**判定——即使部分内容命中缓存，该次请求仍按高档计价。

> **1M context 不加价**：4.6 世代及以后的模型（Haiku 5.5 除外）在标准价内含完整 1M 窗口——90 万 token 的请求和 9 千 token 的请求单价相同，缓存与批量折扣同样按标准价覆盖全窗口。

> **批量 API 一律 5 折**：输入输出同时打对折（Fable 5.2 → $4 / $20，Opus 5.5 → $2 / $10）。

**跨平台 ID**（除 Bedrock 外其余平台都用 Claude API ID，无 `anthropic.` 前缀）：

| 模型 | Amazon Bedrock ID | Google Cloud / Foundry / Claude Platform on AWS |
| --- | --- | --- |
| Fable 5.2 | `global.anthropic.claude-fable-5-2` | `claude-fable-5-2` |
| Opus 5.5 | `anthropic.claude-opus-5-5` | `claude-opus-5-5` |
| Sonnet 5.5 | `anthropic.claude-sonnet-5-5` | `claude-sonnet-5-5` |
| Haiku 5.5 | `anthropic.claude-haiku-5-5` | `claude-haiku-5-5` |

> Bedrock 上 Fable 5.2 / Mythos 5.2 走 `bedrock-runtime` 跨区推理端点，要带 `global.` 或 `us.` 前缀的 inference profile ID。

**Mythos 系列**（`claude-mythos-5-2` / `claude-mythos-5-1` / `claude-mythos-5`）状态同样是 Active、定价与对应 Fable 一致，但属**受限可用**——需通过 Anthropic 验证计划（如 Cyber Verification Program）认证后才能调用。`claude-mythos-preview` 已于 2026-06-09 进入 Deprecated。

## 近期退役提醒

| 退役日期 | 模型 | 迁移到 | 剩余 |
| --- | --- | --- | --- |
| **2026-11-30** | `claude-sonnet-4-5-20250929`（Deprecated 于 2026-09-30） | `claude-sonnet-5-5` | 17 天 |
| **2026-11-24** | `claude-opus-4-5-20251101` | `claude-opus-4-8` | 11 天 |

过了退役日再请求会直接失败（400）。Anthropic 对公开模型至少提前 60 天公告，所以**看到公告就是最后的迁移窗口**。

## 完整生命周期表

引 [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)（访问于 2026-11-13）：

**Active**（仍可调用，部分已是上一代）：

| Model ID | 退役承诺 |
| --- | --- |
| `claude-fable-5-2` / `claude-mythos-5-2` | 不早于 2027-11-09 |
| `claude-fable-5-1` / `claude-mythos-5-1` | 不早于 2027-09-01 |
| `claude-opus-5-5` | 不早于 2027-09-22 |
| `claude-sonnet-5-5` | 不早于 2027-09-28 |
| `claude-haiku-5-5` | 不早于 2027-10-07 |
| `claude-fable-5` / `claude-mythos-5` | 不早于 2027-06-09 |
| `claude-opus-5` | 不早于 2027-07-24 |
| `claude-sonnet-5` | 不早于 2027-06-30 |
| `claude-opus-4-8` / `claude-opus-4-7` / `claude-opus-4-6` | 2027-05-28 / 04-16 / 02-05 |
| `claude-sonnet-4-6` | 不早于 2027-02-17 |
| `claude-haiku-4-5-20251001` | 不早于 2026-10-15 |
| `claude-opus-4-5-20251101` | 不早于 2026-11-24 |

**Deprecated**（仍能用但不再推荐）：`claude-sonnet-4-5-20250929`（2026-11-30 退役）、`claude-mythos-preview`（2026-06-09 起，退役日待定）。

**Retired**（请求会失败）：`claude-opus-4-1-20250805`、`claude-opus-4-20250514`、`claude-sonnet-4-20250514`、`claude-3-7-sonnet-20250219`、`claude-3-5-haiku-20241022`、`claude-3-haiku-20240307`。

> ⚠️ **两页口径不一致**：[Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) 把上一代归入「Legacy models」，[Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) 的状态列至今仍标 **Active**。判断"能不能调"看后者，判断"该不该用"看前者。

## alias 怎么解析

**先分清 alias 和快照**——这是最容易搞错的一点：

- **4.6 世代之前**：`claude-sonnet-4-5` 是便利 alias，解析到该 minor 版本最近的 dated 快照。
- **4.6 世代及之后**：`claude-sonnet-5-5` 这类 dateless ID **本身就是 pinned 快照**，不是 alias。Anthropic 不会更新已有 ID 的权重或配置，新版本会另发新 ID。

**Claude Code 侧**的 `opus` / `sonnet` / `haiku` / `fable` 是真 alias，解析结果**随 provider 变**：

| Provider | `opus` | `sonnet` | `haiku` |
| --- | --- | --- | --- |
| Anthropic API | Opus 5.5 | Sonnet 5.5 | Haiku 5.5 |
| Claude Platform on AWS | Opus 5.5 | Sonnet 4.6 | Haiku 4.5 |
| Amazon Bedrock / Google Agent Platform | Opus 5.5 | Sonnet 4.5 | Haiku 4.5 |
| Microsoft Foundry | Opus 4.6 | Sonnet 4.5 | Haiku 4.5 |

`fable` 解析到 Fable 5.2，仅 Claude apps gateway 会话例外（默认落到 Fable 5，需显式 `/model claude-fable-5-2`）。

**所以**：要跨 provider 或要长期稳定，就 pin 完整 ID：

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-5-5
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5
export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-5-5
export ANTHROPIC_DEFAULT_FABLE_MODEL=claude-fable-5-2
```

Claude Code 侧最低版本要求：`claude-fable-5-2` 需 **v2.1.321**、`claude-haiku-5-5` 需 v2.1.293、`claude-sonnet-5-5` 需 v2.1.284、`claude-opus-5-5` 需 v2.1.280。

## API 版本变更提醒

**API version `2026-10-21` 起，`temperature` / `top_p` / `top_k` 被移除**——传了会返回 400 错误。新代码靠 prompt 本身引导行为，不要再调采样参数。

## 参考

- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-11-13）
- [Anthropic Docs · Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)（访问于 2026-11-13）
- [Anthropic Docs · Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（访问于 2026-11-13）
- [Anthropic Docs · Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)（访问于 2026-11-13）
- [Claude Code · Model configuration](https://code.claude.com/docs/en/model-config)（访问于 2026-11-13）
- [模型家族总览](/claude-capabilities/models/overview)

## 下一步

- 选型决策 → [模型概览](/claude-capabilities/models/overview)
- CLI 视角 alias / effort / 最低版本 → [Claude Code · 模型选择](/claude-code/basics/model-selection)

## 如果你想

- 各模型详解 → [Fable 5.2](./fable) / [Opus 5.5](./opus) / [Sonnet 5.5](./sonnet) / [Haiku 5.5](./haiku)
- 多约束下怎么选 → [模型选型（API 视角）](./choosing-model)
- 成本计算细节 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)
- 第三方 provider 对照 → [第三方模型](/claude-code/ecosystem/third-party-models)
