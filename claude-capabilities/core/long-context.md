---
title: 长上下文
description: 'API 视角的 1M context；定价分档、Prompt Caching 配合、衰减实测与长文档处理实战'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 复核了四型号 context 上限与 1M 窗口计价口径、Haiku 5.5 分档规则、缓存读写倍率、Batch 300k 输出支持范围与 tokenizer 换代；本页示例未在本机重跑'
  claudeCode: 2.1.220
  model: claude-opus-5-5
  longContext: 'https://platform.claude.com/docs/en/build-with-claude/context-windows'
  promptCaching: 'https://platform.claude.com/docs/en/build-with-claude/prompt-caching'
  pricing: 'https://platform.claude.com/docs/en/about-claude/pricing'
  accessedAt: 2026-11-13
---

# 长上下文

> **TL;DR**：当前四型号（Fable 5.2 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5）**全部 1M context / 128k 输出**，而且 **1M 窗口含在标准价内**——90 万 token 和 9 千 token 单价相同。唯一例外是 **Haiku 5.5 按 prompt 长度分档**（> 100k 时输入输出各跳 5 倍）。**长 context 真实可用**——但有「中段衰减」实测：100k+ 之后召回率从 95% 掉到 ~75%。**Prompt Caching + 关键信息前置**是 1M 实战标配。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 4 型号的 context 上限（1M）与 1M 窗口的计价口径
- 1M context 的定价（Prompt Caching 配合）
- Long context 衰减实测（中段 vs 头尾）
- 长文档处理 4 种实战模式（PDF / 代码库 / 多文档 / RAG）
- 6 个常见坑（衰减、token 爆炸、分档跳价、cache 失配、跨云差异）

## 一、4 模型 context 上限

| 型号 | Model ID | Context | Max output | 1M 窗口计价 |
| --- | --- | :---: | :---: | --- |
| **Fable 5.2** | `claude-fable-5-2` | 1M | 128k | 标准价内含 |
| **Opus 5.5** | `claude-opus-5-5` | 1M | 128k | 标准价内含 |
| **Sonnet 5.5** | `claude-sonnet-5-5` | 1M | 128k | 标准价内含 |
| **Haiku 5.5** | `claude-haiku-5-5` | 1M | 128k | ⚠️ 按 prompt 分档 |

**反直觉**：在 **Anthropic API** 上这四型号**默认就是 1M context**——**不要**写 `claude-opus-5-5[1m]` 这种后缀（Sonnet 4.5 时代残留，那之后 1M 窗口不再需要显式开启）。

**对比上一代**（都还能调用，状态 Active）：`claude-opus-5` / `claude-sonnet-5` / `claude-fable-5` 同样是 1M；只有 `claude-haiku-4-5-20251001` 上限停在 **200k**，退役不早于 2026-10-15。

**Model ID 语义**：4.6 世代之前 `claude-sonnet-4-5` 这类 dateless ID 是便利 alias（解析到最近的 dated 快照）；**4.6 世代及之后 dateless ID 本身就是 pinned 快照**，不是 alias——写 `claude-sonnet-5-5` 就是精确锁到那个快照，不会自动升级。

**注意 Bedrock / Vertex 等 provider**：Model ID 与 1M 的启用方式都跟 Anthropic API 不同（Bedrock 上要用 `anthropic.` 前缀的 ID，跨区推理还要 inference profile ID）——看 provider 文档。

## 二、1M Context 的 Pricing

**长 context 走 Prompt Caching 经济性最好**——cache 读价只有基础输入价的 2.5%~10%：

| 型号 | 输入 $/MTok | 输出 $/MTok | 缓存读 | 缓存写 5m | 缓存写 1h |
| --- | :---: | :---: | :---: | :---: | :---: |
| **Fable 5.2** | $8 | $40 | $0.20（2.5%） | $10 | $16 |
| **Opus 5.5** | $4 | $20 | $0.20（5%） | $5 | $8 |
| **Sonnet 5.5** | $2 | $10 | $0.10（5%） | $2.50 | $4 |
| **Haiku 5.5** † | $0.10 | $0.50 | $0.01（10%） | $0.125 | $0.20 |

† Haiku 5.5 是**全系唯一按 prompt 长度分档计费的型号**：上表是 prompt ≤ 100k 的档位；**> 100k 时输入 $0.50 / 输出 $2.50**（各跳 5 倍），缓存写 $0.625 / $1、缓存读 $0.05。分档按**单次请求**判定——即使部分内容命中缓存，该次请求仍按高档计价。

**关键认知**：
- **1M 窗口不加价**：4.6 世代及以后的模型（Haiku 5.5 除外）在标准价内含完整 1M 窗口——90 万 token 与 9 千 token 单价相同，缓存与批量折扣同样覆盖全窗口。**没有「> 200k 按 2× 计价」这回事**（那是 Sonnet 4 时代 1M beta 的规则）
- **Haiku 5.5 跑 1M 反而最贵**：长 prompt 直接跳贵档，先量长度再定型号

**实战示例**（Sonnet 5.5，1M token 输入，50% 命中 cache）：

```
无 cache:
  1M × $2/M = $2.00

有 cache（命中部分早已写入，其余本次写入）:
  cache 读: 500k × $0.10/M = $0.05   (基础价 5%)
  cache 写: 500k × $2.50/M = $1.25   (基础价 125%)
  总: $1.30  → 节省 35%
```

**再省一层**：离线任务走 Batch API 再打 5 折。注意 **300k 输出是 beta**（需 `anthropic-beta: output-300k-2026-03-24`），官方点名的支持型号是 Opus 5.5 / Sonnet 5.5 / Haiku 5.5 等，**不含 Fable**；同步 Messages API 的 max output 上限是 **128k**。

**Tokenizer 别套旧数**：当前 tokenizer（4.7 世代引入）下 1M token ≈ 555k 词 ≈ 250 万字符（旧 tokenizer 下 1M token ≈ 750k 词）。同样文本在 4.7+ 型号上约多 30~35% token，预算要重算。

详见 [Prompt Caching API 详解](/claude-capabilities/api/prompt-caching)。

## 三、Long Context 衰减实测

**1M context 不是「全 context 都能用」**——社区 + 官方 benchmark 都观察到**中段衰减**：

```
召回率（"大海捞针"实测）
  ↓
  0%   20%   40%   60%   80%   100%
  ┌─────┬─────┬─────┬─────┬─────┐
  │ 头  │     │     │     │ 尾  │
  │ 95% │ 90% │ 80% │ 75% │ 90% │
  │     │     │  ↓  │     │     │
  │     │     │ 中段衰减 │     │
  └─────┴─────┴─────┴─────┴─────┘
```

**衰减规律**（基于 Anthropic 公开 needle-in-haystack 测试）：

| Context 位置 | 召回率 | 解读 |
| --- | :---: | --- |
| 头 20% | 95%+ | 最佳 |
| 20-50% | 90% | 良好 |
| **50-80%** | **75-80%** | **衰减区** |
| 尾 20% | 90% | 良好（recency bias） |

**实战应对**：
- **关键信息放头或尾**——别放中段
- **中段内容用 explicit 引用**——「请参考第 700k token 处的那个函数……」
- **长文档问答中提具体位置**——「文档中部提到了 X，请确认」

## 四、长文档处理 4 种实战模式

### 模式 1：单文档问答（1M context 够）

```python
with open("long_doc.pdf", "rb") as f:
    pdf = base64.b64encode(f.read()).decode()

msg = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": [
            {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": pdf}},
            {"type": "text", "text": "这份 500 页报告里，2024 年 Q3 的营收数据是？"},
        ],
    }],
)
```

**适用**：单文档 < 100 页、单次问答。

### 模式 2：多文档对比（slice + cache）

```python
# 多个文档切片 + 独立 cache
system = []
for i, doc in enumerate(documents):
    system.append({
        "type": "text",
        "text": f"文档 {i+1}：\n{doc.content}",
        "cache_control": {"type": "ephemeral"},
    })

msg = client.messages.create(
    model="claude-sonnet-5-5",
    system=system,
    max_tokens=4096,
    messages=[{"role": "user", "content": "对比文档 1 和 2 的结论"}],
)
```

**适用**：5-10 个文档跨文档问答。

### 模式 3：代码库理解（1M + agent）

```python
# 1M context + 工具调用做代码库探索
tools = [...]    # Read / Grep / Bash 工具

msg = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=8192,
    tools=tools,
    messages=[{"role": "user", "content": "在 src/auth/ 找所有 hardcoded 的 API key"}],
)
```

**适用**：代码库 ≤ 1M token（中等规模项目）。

### 模式 4：RAG（超 1M 走 RAG）

```
1M 都不够时（10 万页文档库 / 整个 monorepo）：
  ├─ 预先 embedding + 向量检索
  ├─ 取 top-K 切片进 context
  └─ Claude 总结 / 回答
```

**实战工具**：voyageai / cohere embeddings + Claude 作为 generator。详见 [深度提示工程 · 检索增强](/claude-capabilities/prompting/templates)。

> **API 提醒**：API version `2026-10-21` 起 `temperature` / `top_p` / `top_k` 已被移除——传了返回 400，别再往示例里加这三个参数。

## 五、何时不该用 long context

| 场景 | 该用 | 替代 |
| --- | :---: | --- |
| 单文档 < 100k token | 1M context | Sonnet 5.5 / Opus 5.5 |
| 单文档 100k-1M token | 1M context | Opus 5.5（强一些） |
| 单文档 > 1M token | **RAG** | 切片 + 检索 |
| 实时流式（视频 / 直播） | 不该用 long context | 帧提取 + vision |
| **大量重复 prompt** | **Prompt Caching** | cache 命中率优先 |
| 延迟敏感 | **不要** long context | 长 input 拖慢 first token |

**反直觉**：**长 context 不一定比短 context 慢太多**——长输入主要拖慢的是 first token，Opus 5.5 / Sonnet 5.5 上这个开销可接受。但**输出延迟不变**——模型还是按输出 token 数计算。

## 六、常见坑

**1. 关键信息放中段**

```text
# ❌ 长 context 里把关键问题放中段
[100k filler text]
请回答：这个 API 设计 anti-pattern 吗？    # ← 50% 位置，召回率 75%
[100k more text]

# ✅ 关键问题放末尾（recency bias 强）
[200k context 内容]
请回答：这个 API 设计 anti-pattern 吗？    # ← 末尾 95%+ 召回
```

**2. 1M context 全用 Sonnet 5.5 不上 cache**

**Sonnet 5.5 + 1M context 不开 Prompt Caching = 浪费 30%+ 成本**（上面示例里 50% 命中就省 35%）。长 context 必开 cache。

**3. 用 Haiku 5.5 跑超长 prompt**

Haiku 5.5 是唯一按 prompt 长度分档的型号：单次请求 prompt > 100k 时输入输出**各跳 5 倍**。分档看的是**单次请求的 prompt 长度**，不是会话累计——一半内容命中 cache 也救不了，长文档摘要别用 Haiku 5.5。

**4. 跨 Bedrock / Vertex 期望 1M 默认**

跨 provider 的 Model ID、1M 启用方式、缓存行为都可能不同（Bedrock 上 Fable 5.2 / Mythos 5.2 要走跨区推理端点，带 `global.` / `us.` 前缀的 inference profile ID）。**跨云部署前查 provider 文档**。

**5. PDF > 1M context 切片直接传**

```python
# ❌ 100 页 PDF 全传 → 90k token → 还行
# ❌ 1000 页 PDF 全传 → 900k token → 还能
# ❌ 10000 页 PDF 全传 → 9M token → 爆 context

# ✅ 超 1M 走 RAG
```

**6. 「全 context 都能用」幻觉**

「我 context 装得下 → Claude 全看得到」是错的。**中段衰减是事实**——长 context 任务必须主动「点名」关键信息位置。

## 参考

- [Anthropic Docs · Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)（访问于 2026-11-13）
- [Anthropic Docs · Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)（访问于 2026-11-13）
- [Anthropic Docs · Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（访问于 2026-11-13）
- [Sonnet 5.5 · Prompt Caching 命中率优化](/claude-capabilities/models/sonnet#四、prompt-caching-命中率优化)
- [Opus 5.5 详解](/claude-capabilities/models/opus)
- [CLI 视角 · context-window](/claude-code/basics/context-window)
- [Vision · PDF 处理](/claude-capabilities/core/vision)

## 下一步

- Prompt Caching 实战 → [Prompt Caching API](/claude-capabilities/api/prompt-caching)
- 工具使用协议 → [工具使用 API 协议](/claude-capabilities/core/tool-use)
- 视觉处理 PDF → [Vision 能力](/claude-capabilities/core/vision)

## 如果你想

- RAG 实战 → [深度提示工程 · 检索模板](/claude-capabilities/prompting/templates)
- 成本控制 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)
- 跨 provider 差异 → [模型概览 · 按规模](/claude-capabilities/models/overview#按规模)
