---
title: Fable 5
description: '长链 agent 专家；Model ID `claude-fable-5`；1M context；定位 "the specialist"；adaptive thinking 强制开启'
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-06
verifiedWith:
  claudeCode: 2.1.220
  model: claude-fable-5
  modelOverview: 'https://platform.claude.com/docs/en/about-claude/models/overview'
  modelConfig: 'https://code.claude.com/docs/en/model-config'
  choosingBlog: 'https://claude.com/blog/claude-model-and-effort-level-in-claude-code'
  accessedAt: 2026-08-06
---

# Fable 5

> **TL;DR**：Fable 5 = 「the specialist」——`claude-fable-5`，1M context，**$10 / $50 per 1M token**（最贵）。**长链多步 agent** 场景的顶级专家；adaptive thinking **强制开启且不能关**；新 tokenizer 同样文本比 Opus 4.6 前多 ~30% token；Cybersecurity / Biology 触发 automatic fallback。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 最小调用示例与"显式启用"（不是默认 model）
- Adaptive thinking 强制行为 + 新 tokenizer 计费影响
- Cybersecurity / Biology fallback 路由与 trusted access 流程
- 长链多步 agent 实战模式（描述结果不描述步骤）
- 何时不该用 Fable 5（成本反直觉 + Zero data retention 不可用）
- 跟 [Opus 5](./opus) 的实战差异（不是"更聪明"而是"少 N 步"）

## 一、最小调用示例

Fable 5 **不是默认 model**——必须显式指定：

```python
import anthropic

client = anthropic.Anthropic()

msg = client.messages.create(
    model="claude-fable-5",          # ← 显式启用
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "为什么这个分布式系统在凌晨 3 点定期出现延迟尖峰？"}
    ],
)
```

**Tokenizer 注意**：Fable 5 用**新 tokenizer**，相同文本比 Opus 4.6 前**多约 30% token**——同样的输入在 Fable 5 上计费更高，且 cache_control 的命中率计算也会受影响（见 [Prompt Caching API](/claude-capabilities/api/prompt-caching)）。

## 二、Adaptive Thinking 强制开启

Fable 5 的 adaptive thinking **总是开启**且**用户无法关闭**——这是 specialist 模型的设计决策：

```python
# ❌ 传 budget_tokens 会被忽略（甚至报错）
thinking={"type": "enabled", "budget_tokens": 4096}    # 错

# ✅ Fable 5 上 thinking 字段是只读
# 想控制"想多深"——走 effort level（CLI 视角）/ environment
```

**与其他模型的对比**：

| 模型 | thinking 行为 |
| --- | --- |
| **Fable 5** | **Adaptive，强制开，不能关，不能显式调** |
| Opus 5 | Adaptive，总开（不能显式关） |
| Sonnet 5 | Adaptive，总开 |
| Haiku 4.5 | Legacy `budget_tokens` 显式控制 |

详见 [Extended Thinking 详解](/claude-capabilities/core/extended-thinking)。

## 三、Cybersecurity / Biology Fallback（关键使用限制）

Fable 5 走 safety classifier——遇到以下场景会**自动 fallback**到 Opus 系列：

| 触发场景 | Fallback 目标 |
| --- | --- |
| **Cybersecurity**（渗透测试、漏洞利用代码） | Opus 4.8 |
| **Biology**（基因工程、病原体相关） | Opus 5 |
| CTF（Capture The Flag 比赛） | Opus 4.8 |

**这是预期路由，不是账号问题**——Anthropic 出厂设计就是如此。

**企业级 trusted access**：

需要 Fable 5 在上述场景稳定使用的企业，得通过 Anthropic 客户团队单独申请 trusted access：

```text
联系 Anthropic 客户经理 → 提交使用场景说明
→ 签 trusted access 协议 → 账号解 classifier 路由
→ 验证：/model fable 在 CTF 任务上不再 fallback
```

个人开发者 / 一般企业**别尝试**绕——会被认为 safety 滥用，影响账号信誉。

## 四、长链多步 agent 实战模式

Fable 5 强在**单次会话内能完成的任务深度**——按 Anthropic 官方描述，「能完成 Opus 和 Sonnet 任何 effort 都到不了的任务」（[Anthropic Blog · Choosing a Claude model](https://claude.com/blog/claude-model-and-effort-level-in-claude-code)，访问于 2026-08-06）。

**3 个实战模式**：

### 模式 1：描述结果不描述步骤

Fable 5 自带规划能力——把"想要的最终态"交给它，让它自己规划路径：

```text
# ❌ Sonnet 5 / Opus 5 范式——要步骤
请按以下步骤调试：
1. 看 orders 服务的 3 个 trace
2. 找延迟最高的 2 个
3. 比对 db connection pool 配置
4. ...

# ✅ Fable 5 范式——描述结果
请找出订单服务为什么会卡顿，给我一个可以直接 commit 的根因修复。
```

### 模式 2：模糊问题直接扔

```text
请基于过去 30 天的指标数据，找出"看起来不太对"的异常模式，附严重性排序。
```

Fable 5 会自己定义"不太对"、自己选检测方法、自己排序。Sonnet 5 / Opus 5 上这种 prompt 容易跑偏。

### 模式 3：长链任务不拆

本来会拆给 sub-agent 的工作（Fable 5 完成总成本更低）：

```text
把整个 monorepo 的 4 个老旧服务从 Flask + Celery 重构到 FastAPI + asyncpg。
```

**Sonnet 5 上**：拆 4 个 sub-agent 任务，每 agent 拿一份。
**Fable 5 上**：直接一次做完——它自己跑 4 个子任务、自己验证、给完整 PR。

## 五、成本反直觉

**Fable 5 不是"贵"而是"少步数"**——单次贵但任务完成步数少，总成本可能反而低：

| 任务 | Sonnet 5（多步） | Fable 5（少步） | 谁更省 |
| --- | --- | --- | --- |
| 30 步长链 agent 任务 | $2.10 | $1.50 | **Fable** |
| 50 步长链 agent 任务 | $3.50 | $2.20 | **Fable** |
| 日常 5 步对话 | $0.05 | $0.20 | **Sonnet** |
| 单次 Q&A | $0.01 | $0.05 | **Sonnet** |

**决策**：

```
任务总步数估算
  │
  ├─ < 10 步 ────────────── Sonnet 5（或更低）
  │
  ├─ 10-30 步 ────────────── Opus 5（默认）/ Sonnet 5（成本敏感）
  │
  └─ 30+ 步 / 复杂长链 ──── Fable 5（不一定更贵）
```

## 六、何时不该用 Fable 5

1. **日常 5 步以内任务**——Sonnet 5 便宜 5-10 倍
2. **批量处理**——Haiku 4.5 + Batch API 便宜 10-20 倍
3. **Zero data retention 环境**——Fable 5 **不可用**（[Anthropic Docs · ZDR](https://platform.claude.com/docs/en/build-with-claude/data-residency)）
4. **Cybersecurity / Biology 任务**（未申请 trusted access）—— 会 fallback，结果是 Opus 4.8 而非 Fable 5
5. **短 prompt + 短输出**（< 500 token 全程）—— 完全浪费 Fable 5 的多步能力

## 七、常见坑

**默认调用走 Fable 5**

Anthropic API 上 `claude-fable-5` 不是任何 alias 的解析结果——必须显式 model id。忘了显式用就走 Sonnet 5 / Opus 5 默认。

**没提早发现 fallback，账单里全是 Opus 4.8**

**注意**：fallback 时**账单仍按 Fable 5 报价**——Anthropic 收的是"启动 Fable 5 的钱"，交付的是 Opus 4.8 的输出。看账单里的 `model_used` 字段才发现不对劲。

**用 `budget_tokens` 想控制 thinking**

Fable 5 不支持 legacy extended thinking——传 `budget_tokens` 会被忽略或报错。

**Zero data retention 启用后 Fable 5 报 403**

Fable 5 当前**不支持** ZDR。ZDR 环境下只可用 Opus 5 / Sonnet 5 / Haiku 4.5。

**没申请 trusted access 就让 Fable 5 跑 CTF 题目**

走 safety fallback，账号可能被风控——不是 bug，是**预期**。

## 参考

- [Anthropic Docs · Models overview](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-08-06）
- [Anthropic Docs · Model configuration · Work with Fable 5](https://code.claude.com/docs/en/model-config#work-with-fable-5)（访问于 2026-08-06）
- [Anthropic Blog · Choosing a Claude model and effort level in Claude Code](https://claude.com/blog/claude-model-and-effort-level-in-claude-code)（访问于 2026-08-06）
- [模型家族总览](/claude-capabilities/models/overview)
- [Opus 5 对照](./opus)

## 下一步

- API 视角选型决策 → [模型选型](./choosing-model)
- 长链 agent 编排 → [Subagent 与工作流编排](/claude-code/subagents-and-workflows/workflow-orchestration)
- Adaptive thinking 深入 → [Extended Thinking 详解](/claude-capabilities/core/extended-thinking)

## 如果你想

- Cybersecurity / Biology 场景企业接入 → 联系 Anthropic 客户团队申请 trusted access
- Zero data retention 兼容模型 → [Opus 5](./opus) / [Sonnet 5](./sonnet) / [Haiku 4.5](./haiku)
- 成本计算 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)
