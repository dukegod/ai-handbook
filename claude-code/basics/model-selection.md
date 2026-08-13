---
title: 模型选择
description: Opus 5 / Sonnet 5 / Haiku 4.5 / Fable 5 的官方定位、pricing、context window、effort levels 与选型决策树
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-28
verifiedWith:
  claudeCode: 2.1.215
  model: claude-opus-4-8
  modelConfig: 'https://code.claude.com/docs/en/model-config'
  modelOverview: 'https://platform.claude.com/docs/en/about-claude/models/overview'
  choosingBlog: 'https://claude.com/blog/claude-model-and-effort-level-in-claude-code'
  accessedAt: 2026-07-28
---

# 模型选择

> **TL;DR**：Claude Code 支持 4 条产品线——**Fable 5**（长链条 agent 专家）/ **Opus 5**（复杂 agentic 编程）/ **Sonnet 5**（速度与智能的平衡）/ **Haiku 4.5**（最快接近前沿）。用 `/model` 切换。选型核心判断：**「缺知识」就升 tier，「没努力」就升 effort**。

⏱ 预计阅读时间：10 分钟

## 你能在这里学到

- 4 条产品线的官方定位、pricing、context window
- Fable / Opus / Sonnet / Haiku 的**比喻式定位**（Anthropic 官方口径）
- Model aliases 与它们在不同 provider 上的解析
- Effort levels 的 5 档 + `ultracode`
- 决策规则：**缺知识 vs 没努力**
- 常见坑与 provider 差异

## 前置

- 装好 Claude Code
- 理解 [成本与 Token 管理](./cost-and-tokens)——模型选择是省钱头号杠杆

## 一、4 条产品线速览

**当前活跃模型**（引 [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) 访问于 2026-07-28）：

| 模型 | 官方定位 | Model ID | Pricing（$/1M token 输入/输出） | Context | Max Output |
| --- | --- | --- | --- | --- | --- |
| **Fable 5** | Next-generation intelligence for long-running agents | `claude-fable-5` | **$10 / $50** | 1M | 128k |
| **Opus 5** | For complex agentic coding and enterprise work | `claude-opus-5` | $5 / $25 | 1M | 128k |
| **Sonnet 5** | The best combination of speed and intelligence | `claude-sonnet-5` | $3 / $15 * | 1M | 128k |
| **Haiku 4.5** | The fastest model with near-frontier intelligence | `claude-haiku-4-5` | $1 / $5 | 200k | 64k |

`*` Sonnet 5 至 **2026-08-31** 有 introductory pricing **$2 / $10**。

**能力差异**：

- **Fable 5**：Adaptive thinking **总是开启**（不能关）；context 用新 tokenizer，相同文本比 Opus 4.6 前多约 **30%** token
- **Opus 5 / Sonnet 5**：Adaptive thinking 开启；不支持 legacy extended thinking
- **Haiku 4.5**：Extended thinking 开启；**不**支持 adaptive thinking

## 二、Anthropic 的比喻式定位

来自官方 blog [Choosing a Claude model and effort level in Claude Code](https://claude.com/blog/claude-model-and-effort-level-in-claude-code)（访问于 2026-07-28）：

- **Fable = the specialist**——见过几乎没人见过的问题的顶级专家。长链条、多步骤工作中优势最大，能「完成 Opus 和 Sonnet 任何 effort 都到不了的任务」
- **Opus = the expert**——领域专家，在陌生代码里靠模式识别就能帮你
- **Sonnet = a really good generalist**——优秀通才，给足上下文能透彻理解**你的具体代码**
- **Haiku**：主打「最快接近前沿」——简单批量、快速回答、subagent 快跑

## 三、`/model` 与 aliases

**会话内切换**：

```text
/model sonnet     # 换 Sonnet
/model opus       # 换 Opus
/model fable      # 换 Fable 5（需 v2.1.170+）
/model haiku      # 换 Haiku
/model default    # 恢复账号默认
/model best       # 有 Fable 就用 Fable，否则最新 Opus
```

**特殊 alias**：

- **`opusplan`** —— Plan Mode 用 Opus，退出后自动切 Sonnet 执行（**混合策略最省钱**）
- **`sonnet[1m]` / `opus[1m]`** —— 强制 1M context（部分 provider 需 usage credits）
- **`ultracode`** —— 严格说是 effort 而非 model：xhigh + Claude Code 动态编排 workflows

**命令行 & settings.json**：

```bash
$ claude --model sonnet
```

```json
{ "model": "opusplan" }
```

### Alias 在不同 provider 上解析不同（重要）

| Provider | `opus` 解析为 | `sonnet` 解析为 |
| --- | --- | --- |
| Anthropic API | Opus 5 | Sonnet 5 |
| Claude Platform on AWS | Opus 5 | Sonnet 4.6 |
| Amazon Bedrock, Google Cloud | Opus 5 | Sonnet 4.5 |
| Microsoft Foundry | Opus 4.6 | Sonnet 4.5 |

想 pin 具体版本用 4 个环境变量：

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-5
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5
export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5
export ANTHROPIC_DEFAULT_FABLE_MODEL=claude-fable-5
```

## 四、Effort levels 与 `/effort`

Effort level 控制模型在一次请求上做**多少总工作**（读多少文件、用多少工具、检查前推进多少步骤）——不只是「思考多少」。Effort 随请求传给模型，模型被训练理解每档行为。

**5 档 + Ultracode**（`/effort` 或 `/model` 里切换）：

| Level | 何时用 |
| --- | --- |
| `low` | 短、有限定、延迟敏感、对智能不敏感的任务 |
| `medium` | 成本敏感、可以牺牲一些智能 |
| **`high`**（默认） | 平衡 token 与智能——多数编程任务的最优选 |
| `xhigh` | 更深推理，token 花销更高 |
| `max` | 极难任务；有 overthinking 风险 |
| `ultracode` | xhigh + [Claude Code 动态编排 workflow](/claude-code/subagents-and-workflows/workflow-orchestration)（仅本次会话） |

**注意**：

- Effort 是**领域偏好**而非逐任务决策——大多数任务用默认 `high` 即可（官方 blog 原话）
- Effort 尺度**每个模型独立校准**——`high` 在不同模型上不代表同一水平
- 你的 prompt 里加 `ultrathink` 关键词可以**单次**触发深度推理（不改会话 effort）

## 五、决策规则：缺知识 vs 没努力

Anthropic 官方给出的核心判断问题（原话）：

> "Did it not *try* hard enough, or did it not *know* enough?"

**决策树**：

```
问题 → Claude 犯错？
        │
        ├─ 答案离谱、方向都错 → 升 tier（Sonnet → Opus → Fable）
        │
        ├─ 大方向对但漏了细节 → 升 effort（high → xhigh → max）
        │
        └─ 长链条多步任务，Opus 也慢 → Fable 5
```

- **知识不够** → 升 tier：问题微妙、陌生领域、架构决策；小模型即使给足上下文仍自信地错
- **努力不够** → 升 effort：Claude 跳过了文件、没跑测试、没反复检查

**成本反直觉**：**用 Sonnet 反复迭代**可能比 **Opus 少步数直接搞定** 更贵——大模型少步数反而总成本可能更低。

## 六、Fable 5 特别使用建议

引 [Claude Code 官方 model config · Work with Fable 5](https://code.claude.com/docs/en/model-config#work-with-fable-5)：

- **描述结果不描述步骤**——把想要的最终态交给它，让它自己规划路径
- **交给它模糊问题**——根因分析、outage 调试、架构决策
- **不用重复提醒「记得验证」**——它自己验证得多
- **给大任务**——本来会拆分的工作直接扔给它一次做完

**注意事项**：

- **不是默认模型**——任何账号类型都要 `/model fable` 显式启用
- **Cybersecurity / biology 触发 automatic fallback**（生物 → Opus 5，网络安全 → Opus 4.8）——这是预期路由，不是账号问题
- **Zero data retention 环境下不可用**
- 需要 Claude Code **v2.1.170+**

## 七、Prompt Caching 与模型

Claude Code 自动对每个模型都用 Prompt Caching（见 [成本与 Token 管理 · Prompt Caching](./cost-and-tokens#三prompt-caching-自动生效)）。可按模型关闭：

```bash
export DISABLE_PROMPT_CACHING=1              # 全关
export DISABLE_PROMPT_CACHING_FABLE=1        # 只关 Fable
export DISABLE_PROMPT_CACHING_OPUS=1
export DISABLE_PROMPT_CACHING_SONNET=1
export DISABLE_PROMPT_CACHING_HAIKU=1
```

## 常见坑

**忘了切模型，Opus 跑全天**

`/model sonnet` 切回 Sonnet，或 `/config` 设默认。日常 Sonnet 应付 80%+ 场景。

**Alias 在不同 provider 上解析不同**

在 Bedrock / Vertex 上 `sonnet` 可能不是 Sonnet 5 而是 4.5。想 pin 具体版本用 `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5`（见第三节）。

**Fable 5 遇 CTF / 生物代码就 fallback**

安全研究、CTF、生物学工作会触发 classifier，Fable 5 换到 Opus 5。这是**预期路由**，企业级 Fable 使用需和 Anthropic 客户团队沟通 trusted access。

**Ultracode 与 xhigh 混淆**

`ultracode` 不是新 effort level——它 = `xhigh` + Claude Code 编排 workflows。**仅本次会话**，`effortLevel` setting 与 `CLAUDE_CODE_EFFORT_LEVEL` 环境变量**不接受** `ultracode`。

**Sonnet 5 在 Anthropic API 永远是 1M context**

不用 `sonnet[1m]` 后缀。auto-compact 在约 967k token 处触发，可用 `CLAUDE_CODE_AUTO_COMPACT_WINDOW` 调。

## 参考

- [Anthropic Docs · Model configuration](https://code.claude.com/docs/en/model-config)（访问于 2026-07-28）
- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-07-28）
- [Anthropic Docs · Effort](https://platform.claude.com/docs/en/build-with-claude/effort)（访问于 2026-07-28）
- [Anthropic Blog · Choosing a Claude model and effort level in Claude Code](https://claude.com/blog/claude-model-and-effort-level-in-claude-code)（访问于 2026-07-28）

## 下一步

- 学 Plan Mode 让 Claude 先出方案 → [Plan Mode](./plan-mode)

## 如果你想

- 深入 Claude 模型全景 → [Claude 能力 · 模型概览](/claude-capabilities/models/overview)
- 深入 Fable 5 → [Fable 5](/claude-capabilities/models/fable)
- 学 Extended Thinking → [Extended Thinking](/claude-capabilities/core/extended-thinking)
- 学 Prompt Caching → [Prompt Caching](/claude-capabilities/api/prompt-caching)
