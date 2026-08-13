---
title: 模型选型（API 视角）
description: 多约束下的 Claude 模型选型决策——任务 / 成本 / 延迟 / 数据驻留 / 规模五个维度
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-06
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5
  modelOverview: 'https://platform.claude.com/docs/en/about-claude/models/overview'
  pricing: 'https://platform.claude.com/docs/en/about-claude/pricing'
  effortDocs: 'https://platform.claude.com/docs/en/build-with-claude/effort'
  accessedAt: 2026-08-06
---

# 模型选型（API 视角）

> **TL;DR**：选型不是"哪个模型最聪明"，而是**多约束下的最优解**——任务类型、成本预算、延迟要求、数据驻留、规模。v0.1 的 [CLI 视角选型](/claude-code/basics/model-selection) 讲「缺知识 vs 没努力」；本页讲 **API/SDK 视角**的多约束决策。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 5 维选型决策框架（任务 / 成本 / 延迟 / 数据驻留 / 规模）
- 按场景直接抄的决策表
- 成本 + 延迟 + 质量三角的实战调优路径
- 何时该用 [Batch API](/claude-capabilities/api/message-batches) 而不是 online
- 何时该申请 [Fable 5 trusted access](/claude-capabilities/models/fable#三cybersecurity--biology-fallback关键使用限制)

## 一、5 维选型决策框架

```
                ┌─ 任务类型 ──────── 短对话 / 编程 / 长链 agent / 批量 / 视觉
                │
                ├─ 成本预算 ──────── 个人 $50/月 / 团队 $500/月 / 企业自定
                │
选型决策 ───────┼─ 延迟要求 ──────── < 200ms / < 2s / < 30s / 24h batch
                │
                ├─ 数据驻留 ──────── 普通 / ZDR（Zero data retention）
                │
                └─ 规模 ────────── PoC / 生产小流量 / 生产大流量 / 企业内网
```

每个维度都有**硬约束**——硬约束把可选范围直接砍掉。剩下的再在软约束里权衡。

## 二、按任务类型——直接抄的决策表

| 任务类型 | 首选 | 次选 | 不推荐 |
| --- | --- | --- | --- |
| 短对话（< 5 步） | [Sonnet 5](./sonnet) | [Haiku 4.5](./haiku) | Opus 5、Fable 5（杀鸡用牛刀） |
| 日常编程（80% 场景） | [Sonnet 5](./sonnet) | Opus 5 | Fable 5 |
| 复杂编程（陌生代码 / 重构） | [Opus 5](./opus) | Sonnet 5 + 多轮迭代 | Haiku 4.5 |
| 长链 agent（10+ 步） | [Opus 5](./opus) | [Sonnet 5](./sonnet) | Haiku 4.5 |
| 超长链 agent（30+ 步） | **[Fable 5](./fable)** | Opus 5 | Sonnet 5、Haiku 4.5 |
| 批量任务（> 1 万条） | [Haiku 4.5 + Batch](./haiku#四批量任务实战) | Haiku 4.5 online | Opus 5 / Fable 5（贵） |
| 分类 / 提取 / 格式化 | [Haiku 4.5](./haiku) | Sonnet 5 | Opus 5、Fable 5 |
| Vision（图 / PDF） | Sonnet 5 | Opus 5 | Haiku 4.5（如需深度理解） |
| Cybersecurity / Biology | Opus 5 / 4.8 | Fable 5（需 trusted access） | — |
| 实时语音 / 视频流 | [Haiku 4.5](./haiku) | Sonnet 5 | Opus 5、Fable 5（延迟） |

## 三、按成本预算——月度 token 估算

**个人开发者**（预算 $50/月）：

```
日常 80% 任务用 Sonnet 5
  → 100 万输入 + 30 万输出 = $3 + $4.5 = $7.5/月
+ 偶尔 Opus 5 处理大任务
  → 50 万输入 + 10 万输出 = $2.5 + $2.5 = $5/月
+ 总：~$13/月，离 $50 预算很远
```

**小团队**（5-10 人，预算 $500/月）：

```
每人每天 20 万输入 + 5 万输出 × 5 人 × 30 天
= 3000 万输入 + 750 万输出（按 Sonnet 5）
= $90 + $112.5 = $202.5/月
+ 偶尔 Opus 5 / Fable 5 处理重任务 = ~$100
+ 总：~$300/月，预算内
```

**生产大流量**（日均 100 万请求）：

```
按请求类型分流：
  60% Haiku 4.5（分类、提取）     → 60 万 × $0.001 = $600/天
  30% Sonnet 5（对话、文档）      → 30 万 × $0.003 = $900/天
  10% Opus 5（复杂任务）          → 10 万 × $0.005 = $500/天
+ 总：$2000/天 = $60k/月
+ 启用 prompt caching（命中率 50%）→ 砍半 ≈ $30k/月
+ 启用 Batch API（50% 折扣）      → 砍 25% ≈ $22.5k/月
```

## 四、按延迟要求——p50 / p95 选模型

| 延迟档 | 含义 | 推荐 |
| --- | --- | --- |
| **< 200ms** | 实时语音、typing effect、streaming first token | [Haiku 4.5 streaming](./haiku) |
| **200ms - 2s** | 聊天 UI、agent 单步响应 | Sonnet 5 streaming |
| **2s - 30s** | 用户提交后等结果、研究任务 | Opus 5 online |
| **30s - 数分钟** | 多步 agent 综合、长文档生成 | Opus 5 / Fable 5 |
| **< 24h** | 离线批处理 | **Batch API**（50% off） |

**first-token latency 经验值**（仅供参考）：

```
Haiku 4.5:  ~150ms
Sonnet 5:   ~400ms
Opus 5:     ~800ms
Fable 5:    ~1.2s
```

数据基于公开 benchmark + 社区实测，实际受 prompt 长度 / region / cache 命中率影响。

## 五、按数据驻留——ZDR 环境选型

**ZDR（Zero Data Retention）**——Anthropic 不保留请求/响应数据用于训练，企业级合规必备。

| 模型 | ZDR 支持 |
| --- | --- |
| Opus 5 | ✅ |
| Sonnet 5 | ✅ |
| Haiku 4.5 | ✅ |
| **Fable 5** | ❌ **不支持** |

**ZDR 环境决策**：

```python
# 企业 ZDR 启用后
import anthropic
client = anthropic.Anthropic()    # 默认走 ZDR

# ✅ 可用
client.messages.create(model="claude-opus-5", ...)
client.messages.create(model="claude-sonnet-5", ...)
client.messages.create(model="claude-haiku-4-5", ...)

# ❌ 403
client.messages.create(model="claude-fable-5", ...)
```

详见 [Anthropic Docs · Data residency](https://platform.claude.com/docs/en/build-with-claude/data-residency)。

## 六、按规模——PoC / 小流量 / 大流量

**PoC 阶段**（个人 / 内部 demo）：

- 单一 model，Sonnet 5 默认；混搭不必要
- 成本估算用 $50/$500/月线性推
- **别**过早优化（Prompt Caching / Batch / Sub-agent 拆分）

**小流量生产**（日均 < 1 万请求）：

- 主流量 Sonnet 5，重型任务 Opus 5
- Prompt Caching 启用（命中率目标 30%+）
- 单 region 部署即可

**大流量生产**（日均 > 10 万请求）：

- 三层分流（Haiku 4.5 / Sonnet 5 / Opus 5 比例按业务）
- Prompt Caching 命中率目标 60%+
- Batch API 处理离线部分
- 跨 region 部署，注意 [alias 在不同 provider 上解析不同](/claude-code/basics/model-selection#alias-在不同-provider-上解析不同-重要)

**企业内网**（私有部署）：

- 看 provider 文档（[Amazon Bedrock](https://aws.amazon.com/bedrock/) / [Google Vertex](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude) / [Microsoft Foundry](https://ai.azure.com/)）
- 显式 pin Model ID（`ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5`）
- ZDR 必开

## 七、完整决策树（API 视角）

```
任务是什么？
  │
  ├─ 批量 / 分类 / 提取 ────────── Haiku 4.5 + Batch API
  │
  ├─ 短对话 / 文档 / 80% 编程 ── Sonnet 5
  │
  ├─ 复杂编程 / 陌生代码 ──────── Opus 5
  │
  └─ 长链多步 agent ────────────── Fable 5（如果预算允许）
                                    │
                                    ├─ ZDR？─────── 改 Opus 5（Fable 不支持）
                                    │
                                    └─ Cybersecurity/Biology？─ 改 Opus 4.8/5（fallback）

成本预算紧？
  │
  ├─ 是 ── 启用 Prompt Caching（目标 30%+ 命中率）
  │
  └─ 否 ── 直接走性能最优

延迟要求 < 200ms？
  │
  ├─ 是 ── Haiku 4.5 + streaming
  │
  └─ 否 ── 任何模型都可，Batch API 24h 内也可
```

## 八、常见坑

**「最贵 = 最好」**

Fable 5 适合长链 agent，但日常对话用 Fable 5 完全是浪费。选型核心是**任务复杂度匹配**，不是价格高低。

**只盯单价忽略步数**

Opus 5 单价是 Sonnet 5 的 1.7-2x，但任务完成步数可能少 50%——**总成本可能反而低**。看总账单别看单价。

**Batch API 拿来跑实时任务**

Batch 是 24h SLA，**不能**用于实时场景。误用会让用户等 24h。

**没测 cache 命中率就上 Prompt Caching**

Prompt Caching 不命中时反而增加 metadata 开销（首请求 + 5% token 写费）。先跑 1000 个真实请求估算命中率，< 30% 别上。

**Fable 5 在 ZDR 环境调用**

直接 403，浪费重试 budget。ZDR 启用前先确认业务能接受 Fable 5 不可用。

**Alias 在不同 provider 上解析不同**

跨云部署时 `opus` 在 Bedrock 可能不是 Opus 5 而是 4.6。**显式 pin Model ID** 是企业级部署的最低要求。

## 参考

- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-08-06）
- [Anthropic Docs · Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（访问于 2026-08-06）
- [Anthropic Docs · Effort](https://platform.claude.com/docs/en/build-with-claude/effort)（访问于 2026-08-06）
- [Anthropic Docs · Message Batches API](https://platform.claude.com/docs/en/api/messages/batches)（访问于 2026-08-06）
- [Anthropic Docs · Data residency / ZDR](https://platform.claude.com/docs/en/build-with-claude/data-residency)（访问于 2026-08-06）
- [CLI 视角选型（缺知识 vs 没努力）](/claude-code/basics/model-selection)

## 下一步

- 模型家族全貌 → [模型概览](/claude-capabilities/models/overview)
- 切到具体模型详解 → [Opus 5](./opus) / [Sonnet 5](./sonnet) / [Haiku 4.5](./haiku) / [Fable 5](./fable)
- 提示技巧 → [深度提示工程](/claude-capabilities/prompting/best-practices)

## 如果你想

- 成本计算细节 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)
- Prompt Caching 实战 → [Prompt Caching API](/claude-capabilities/api/prompt-caching)
- Batch API 实战 → [Message Batches API](/claude-capabilities/api/message-batches)
