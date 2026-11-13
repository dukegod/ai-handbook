---
title: Sonnet 5.5
description: '当前主力日常模型；Model ID `claude-sonnet-5-5`；1M context / 128k 输出；$2 / $10 per MTok，缓存读 $0.10（基准价 5%）'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 复核了模型 ID、定价与缓存倍率、生命周期、Prompt Caching 官方口径，以及 thinking / tool_choice 行为；归档节的 Sonnet 5 + Haiku 4.5 成本表沿用 2026-10-08 的旧记录，本页示例未在本机重跑'
  claudeCode: 2.1.319
  model: claude-sonnet-5-5
  modelOverview: 'https://platform.claude.com/docs/en/about-claude/models/overview'
  modelPage: 'https://platform.claude.com/docs/en/models/sonnet-5-5/overview'
  pricing: 'https://platform.claude.com/docs/en/about-claude/pricing'
  deprecations: 'https://platform.claude.com/docs/en/about-claude/model-deprecations'
  promptCaching: 'https://platform.claude.com/docs/en/build-with-claude/prompt-caching'
  accessedAt: 2026-11-13
---

# Sonnet 5.5

> ⚠️ **本页讲的是当前的 Sonnet 5.5**。上一代 **Sonnet 5**（`claude-sonnet-5`）仍可调用但已不是主力——独有内容压缩在文末「[八、Sonnet 5（上一代）档案](#八、sonnet-5-上一代-档案)」。

> **TL;DR**：Sonnet 5.5 = 「the generalist」——`claude-sonnet-5-5`，**1M context / 128k 输出**，**$2 / $10 per 1M token**，**缓存读 $0.10（基准输入价的 5%）**。日常 80% 编程与对话的首选；`cache_control` 用对、混搭 Haiku 5.5 是省钱关键。

**Sonnet 5.5 官方规格**（[模型页](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)，访问于 2026-11-13）：

| 项 | 值 |
| --- | --- |
| Model ID | `claude-sonnet-5-5` |
| Context / Max output | 1M / 128k |
| 思考 | Adaptive（默认开），默认 effort `high` |
| 相对延迟 | Fast |
| 知识截止 | 2026-06 |
| 发布 / 退役承诺 | 2026-09-28 / 不早于 2027-09-28 |

其它平台 ID：Bedrock `anthropic.claude-sonnet-5-5`；Google Cloud / Microsoft Foundry / Claude Platform on AWS 均用 `claude-sonnet-5-5`。Claude Code 侧需 **v2.1.284+**。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 最小调用示例（与同代 API 协议，仅 model 字段换 ID）
- 1M context 是默认行为——不需要 `[1m]` 后缀
- 当前定价与缓存倍率（「限时折扣」为什么已不存在）
- Prompt Caching 命中率优化（官方口径 + 5 个常见错误）
- Sub-agent 编排：Sonnet 5.5 主 + Haiku 5.5 sub 混搭
- 何时该升 Opus 5.5 / 何时该降 Haiku 5.5

## 一、最小调用示例

API 调用结构与 [Opus 5.5](./opus)、[Haiku 5.5](./haiku)、[Fable 5.2](./fable) **完全相同**——只是 `model` 字段换 ID：

```python
import anthropic

client = anthropic.Anthropic()

msg = client.messages.create(
    model="claude-sonnet-5-5",     # ← 唯一区别
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
)
```

**三条 API 纪律**：`temperature` / `top_p` / `top_k` 自 API version `2026-10-21` 起被移除（传了 400）；`thinking: {"type": "enabled", "budget_tokens": N}` 一律 400，改用 adaptive thinking + `output_config={"effort": ...}`；`tool_choice` 只支持 `auto` / `none`。逐条展开见 [第七节](#七、常见坑)。

**Model ID 就是快照**：4.6 世代及之后，`claude-sonnet-5-5` 这类 dateless ID **本身就是 pinned 快照**而非 alias——Anthropic 不更新已有 ID 的权重。4.6 世代之前 `claude-sonnet-4-5` 才只是解析到最近 dated 快照的便利 alias。

**Claude Code 侧**：`sonnet` alias 在 Anthropic API 上已解析到 Sonnet 5.5，在 Bedrock / Foundry 上仍指向上一代。跨云部署要显式 pin：

```bash
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5
```

## 二、1M Context 是默认

Sonnet 5.5 在 Anthropic API 上**永远是 1M context**。**不要写** `claude-sonnet-5-5[1m]`：

```python
# ✅ 正确
client.messages.create(model="claude-sonnet-5-5", ...)

# ❌ 错——[1m] 后缀是 Sonnet 4.5 时代的写法，在 5.5 上是冗余
client.messages.create(model="claude-sonnet-5-5[1m]", ...)
```

`[1m]` 后缀在 Bedrock / Vertex 等 provider 上可能仍需保留，**Anthropic API 直接调可以省**。1M 窗口**按标准价计费**——90 万 token 与 9 千 token 的请求单价相同，缓存与批量折扣同样覆盖全窗口。

**Tokenizer 换算**（当前 tokenizer 由 4.7 世代引入）：1M token ≈ **555k 词** ≈ 250 万字符；旧 tokenizer 下 1M token ≈ 750k 词；200k token ≈ 150k 词。同样一段文本在 4.7 及之后型号上**约多 30% token**。Sonnet 5.5 与 Sonnet 5 **用同一个 tokenizer**，迁移不改变 token 计数。

**Auto-compact 触发点**：约 **967k token** 处，可用环境变量提前：

```bash
export CLAUDE_CODE_AUTO_COMPACT_WINDOW=800000   # 提前到 800k 触发
```

## 三、定价

> ⚠️ **「Introductory Pricing（限时折扣）」对 Sonnet 5.5 已不适用。** 上一代 Sonnet 5 的限时促销（截至 2026-08-31）早已结束——官方定价页脚注写明该价格**已转为标准价**，原定 2026-09-01 上调到 $3 / $15 **不会发生**。Sonnet 5.5 直接按下面价目表算账。

| 项 | Sonnet 5.5 |
| --- | :---: |
| 输入 | **$2 / MTok** |
| 输出 | **$10 / MTok** |
| 缓存写（5 分钟 / 1 小时） | $2.50 / $4（基准输入价 × 1.25 / × 2） |
| **缓存读（命中）** | **$0.10 / MTok（基准输入价 × 0.05）** |
| Batch API 输入 / 输出 | $1 / $5（5 折） |

**同代横向对照**：

| 模型 | 输入 / 输出 | 缓存读 | 默认 effort | 相对延迟 |
| --- | --- | --- | --- | --- |
| Fable 5.2 | $8 / $40 | $0.20（2.5%） | `high` | Slower |
| Opus 5.5 | $4 / $20 | $0.20（5%） | `medium` | Moderate |
| **Sonnet 5.5** | **$2 / $10** | **$0.10（5%）** | `high` | Fast |
| Haiku 5.5 | $0.10 / $0.50 † | $0.01（10%） | `medium` | Fastest |

† Haiku 5.5 是全系**唯一按 prompt 长度分档计费的型号**：prompt 超过 10 万 token 时输入 $0.50、输出 $2.50。

**长输出要走 Batch**：**300k 输出是 beta**，只在 Message Batches API + `anthropic-beta: output-300k-2026-03-24` 下可用；同步 Messages API 上限就是 **128k**。官方点名支持 300k 输出的型号**不含 Fable**。

> ⚠️ 定价在 Bedrock / Vertex 等第三方 provider 上**不一定同步**——跨云部署前看各 provider 自己的 pricing 页。

## 四、Prompt Caching 命中率优化

Sonnet 5.5 缓存读是基准输入价的 **5%**（$2 → $0.10 / MTok）——同代里 Opus 5.5 同为 5%，Fable 5.2 是 2.5%，Haiku 5.5 与上一代是 10%。命中率从 30% 升到 80%，单次成本可能腰斩。

**官方协议**（[Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)，访问于 2026-11-13）：

- 一次请求最多 **4 个 cache breakpoint**；顶层 `cache_control` 会自动缓存到**最后一个可缓存 block**，但**同样占 1 个槽位**（4 个显式 breakpoint 用满后再加自动缓存会 400）
- 缓存前缀顺序固定：`tools` → `system` → `messages`——改动上层会让下层一起失效
- 写入倍率：5 分钟 = × 1.25，1 小时 = × 2
- **最小可缓存长度 512 token**（Sonnet 5.5 / Opus 5.5 / Haiku 5.5 / Fable 5.2 统一）——低于这个长度**静默不缓存、也不报错**；上一代 Sonnet 5 是 1024 token
- 官方支持两种用法：**顶层单个 `cache_control`（自动，推荐作为起点）** 或**逐 block 精确控制**

**回本点**：按 1.25x 写 / 0.05x 读摊平，**第 2 次调用就回本**。10 万 token 前缀连续调 10 次：不缓存 $2.00，走缓存 $0.34（写 1 次 $0.25 + 读 9 次 $0.09）。

```python
import anthropic
client = anthropic.Anthropic()

msg = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=2048,
    system=[{"type": "text", "text": "你是资深 Python 代码审查员…"}],
    cache_control={"type": "ephemeral"},     # ← 顶层，自动缓存到最后一个可缓存 block
    messages=[{"role": "user", "content": "审查 PR #1234"}],
)
```

**5 个常见错误**（按影响排序）：

1. **System prompt 放 messages 末尾**——只有 `system` 字段在缓存前缀里
2. **长 system 块不分区**——「角色设定」和「few-shot 示例」拆成两块，各有独立 TTL
3. **消息体里塞时间戳**——`datetime.now()` 每次都变，必 miss
4. **Tool 定义顺序不稳定**——`tools` 在缓存前缀最前面，顺序一变全废
5. **可变内容放在不可变内容前面**——Image / PDF 一律放 messages 末尾

详见 [Prompt Caching API 详解](/claude-capabilities/api/prompt-caching)。

## 五、Sub-agent 编排

Sonnet 5.5 做主 agent 最划算——Opus 5.5 太贵、Haiku 5.5 智能不够。典型模式：

```
主 agent（Sonnet 5.5）
  ├─ sub: 评论情感分类（Haiku 5.5）
  ├─ sub: 文章摘要（Haiku 5.5）
  └─ sub: 实体提取（Haiku 5.5）
→ 主 agent 综合
```

**省钱的杠杆很直接**：同样一段 token，Sonnet 5.5 的单价是 Haiku 5.5 的 **20 倍**（输入 $2 vs $0.10，输出 $10 vs $0.50）。按 token 分配折算的相对成本：

| 模式 | 假设 | 相对成本 |
| --- | --- | ---: |
| 全 Sonnet 5.5 | 全部 token 走 Sonnet 5.5 | 100% |
| **Sonnet 5.5 主 + Haiku 5.5 sub** | 80% token 走 Haiku 5.5 | **≈ 24%** |
| 全 Haiku 5.5 | 全部 token 走 Haiku 5.5 | 5% |

> 上表是**按价格倍率折算的量级示意**，不是实测账单——真实比例取决于 sub-agent 承担了多少 token。全用 Haiku 5.5 做主 agent 则质量塌方。

详见 [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)。

## 六、何时该升 / 降

**该升 Opus 5.5**（[Opus 5.5 详解](./opus)）：

- 大型陌生代码 debug
- 多文件架构重构
- 长链多步 agent（10+ tool call）

**该降 Haiku 5.5**（[Haiku 5.5 详解](./haiku)）：

- 简单批处理（分类、提取、格式化）
- 延迟敏感场景
- 大量并发 sub-agent

**保持 Sonnet 5.5**：

- 日常编程、对话、文档总结（80% 场景）
- 中等复杂度的多步任务（5-10 tool call）

## 七、常见坑

**还在写 `sonnet[1m]`**

见 [第二节](#二、1m-context-是默认)。Anthropic API 上 1M 是默认，`[1m]` 后缀是 Sonnet 4.5 时代产物。

**照抄旧代码带 `temperature` / `top_p` / `top_k`**

API version `2026-10-21` 起这三个参数被移除，传了返回 400——**即使传默认值也报错**。新代码一律靠 prompt 引导行为。

**用 `thinking: {"type": "disabled"}` 关思考**

Sonnet 5.5 上返回 400（错误消息会指向正确写法）。要关掉前置思考用 `thinking: {"type": "between_tools"}`——但**只在 `high` 及以下 effort 生效**，`xhigh` / `max` 下会 400。legacy `budget_tokens` 一律不被接受。

**`tool_choice: any` / `tool` 强制工具调用**

Sonnet 5.5 **不支持强制工具调用**，返回 400。改用 `auto` + [strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use)，或在 prompt 里说明何时该用工具。

**alias 在 Bedrock 上仍解析成上一代**

`sonnet` alias 的解析结果随 provider 变。跨云部署要显式 pin：`ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5`。

**Sub-agent 全用 Sonnet 5.5 拼成本**

sub-agent 的批量小任务全用 Sonnet 5.5，账单是 Haiku 5.5 混搭的数倍。混搭是默认模式，不是优化项。

## 八、Sonnet 5（上一代）档案

Sonnet 5（`claude-sonnet-5`）状态仍是 **Active**——退役承诺不早于 **2027-06-30**。它与 Sonnet 5.5 同代、同 tokenizer，但有这些差别：

| 项 | Sonnet 5.5（当前） | Sonnet 5（上一代） |
| --- | --- | --- |
| 输入 / 输出 | $2 / $10 | $2 / $10（已是标准价） |
| 缓存读 | $0.10（5%） | $0.20（10%） |
| 最小可缓存长度 | 512 token | 1024 token |
| 关掉前置思考 | `between_tools`（`high` 及以下 effort） | `thinking: {"type": "disabled"}` |
| `tool_choice: any / tool` | ❌ 400 | ✅ 支持 |
| per-message effort / mid-conversation system messages | ✅ | ❌ 不支持 |
| 退役承诺 | 不早于 2027-09-28 | 不早于 2027-06-30 |

**更老两代的状态**：

| Model ID | 输入 / 输出 | 缓存读 | 状态 |
| --- | --- | --- | --- |
| `claude-sonnet-4-6` | $3 / $15 | $0.30 | Active，退役不早于 2027-02-17 |
| `claude-sonnet-4-5-20250929` | $3 / $15 | $0.30 | **Deprecated（2026-09-30 公告），2026-11-30 退役** → 迁到 `claude-sonnet-5-5` |

**上一代独有的 sub-agent 成本表**（Sonnet 5 + Haiku 4.5，Haiku 4.5 单价 $1 / $5）：

| 模式 | 总成本估算 |
| --- | --- |
| 全 Sonnet 5 | $0.45 |
| 全 Opus 5 | $0.75 |
| **Sonnet 5 主 + Haiku 4.5 sub** | **$0.15** |
| 全 Haiku 4.5 | $0.08（但质量塌方） |

> ⚠️ 这张表是**上一代配比**。Haiku 5.5 的单价只有 Haiku 4.5 的 1/10——新项目请按 [Haiku 5.5](./haiku) 重算。

**迁移到 Sonnet 5.5 要做的六件事**（[官方迁移指南](https://platform.claude.com/docs/en/models/sonnet-5-5/migration-guide)）：换 model ID；`disabled` 改 `between_tools`；`tool_choice` 的 `any` / `tool` 改 `auto` + strict tool use；会话保持 append-only（改写早期历史会让 thinking block 校验失败）；computer use 迁到 `computer_toolset_20260801`；需要展示工具调用间文本时设置 `thinking.display`。

## 参考

- [Anthropic Docs · Claude Sonnet 5.5 模型页](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)（访问于 2026-11-13）
- [Anthropic Docs · What's new in Claude Sonnet 5.5](https://platform.claude.com/docs/en/models/sonnet-5-5/whats-new-sonnet-5-5)（访问于 2026-11-13）
- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-11-13）
- [Anthropic Docs · Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)（访问于 2026-11-13）
- [Anthropic Docs · Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（访问于 2026-11-13）
- [Anthropic Docs · Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)（访问于 2026-11-13）
- [Anthropic Docs · Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)（访问于 2026-11-13）
- [Claude Code · Model configuration](https://code.claude.com/docs/en/model-config)（访问于 2026-11-13）
- [模型 ID 与定价速查](./model-ids)
- [Opus 5.5 对照](./opus)
- [Haiku 5.5 对照](./haiku)
- [Prompt Caching API 详解](/claude-capabilities/api/prompt-caching)

## 下一步

- 批量 / 延迟敏感 → [Haiku 5.5](./haiku)
- 长链 agent 专家 → [Fable 5.2](./fable)
- Prompt caching 详解 → [Prompt Caching API](/claude-capabilities/api/prompt-caching)

## 如果你想

- sub-agent 编排省钱模式 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)
- 详细成本与 token 优化 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)
- 选型决策树 → [模型概览 · 选型决策指南](./overview#五、选型决策指南)
