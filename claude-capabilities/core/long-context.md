---
title: 长上下文
description: API 视角的 200k / 1M context；batching / streaming / pricing、Prompt Caching 配合、衰减实测与长文档处理实战
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-06
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  longContext: 'https://platform.claude.com/docs/en/build-with-claude/context-windows'
  promptCaching: 'https://platform.claude.com/docs/en/build-with-claude/prompt-caching'
  accessedAt: 2026-08-06
---

# 长上下文

> **TL;DR**：Opus 5 / Sonnet 5 / Fable 5 全部支持 **1M context**（200k 基础 + Prompt Caching 扩到 1M），Haiku 4.5 上限 **200k**。**长 context 真实可用**——但有"中段衰减"实测：100k+ 之后召回率从 95% 掉到 ~75%。**Prompt Caching + 关键信息前置**是 1M 实战标配。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 4 模型 context 上限（200k vs 1M）+ 如何切换
- 1M context 的 pricing（Prompt Caching 配合）
- Long context 衰减实测（中段 vs 头尾）
- 长文档处理 4 种实战模式（PDF / 代码库 / 多文档 / RAG）
- 5 个常见坑（衰减、token 爆炸、Prompt Caching 失配、cross-region 差异）

## 一、4 模型 context 上限

| 模型 | 基础 context | 1M context | 切换方式 |
| --- | :---: | :---: | --- |
| **Opus 5** | 200k | ✅ | **默认就是 1M**（Anthropic API） |
| **Sonnet 5** | 200k | ✅ | **默认就是 1M** |
| **Fable 5** | 200k | ✅ | **默认就是 1M** |
| **Haiku 4.5** | 200k | ❌ | 硬上限 200k |

**反直觉**：在 **Anthropic API** 上，Opus 5 / Sonnet 5 / Fable 5 **永远 1M context**——**不要写** `claude-opus-5[1m]` 这种后缀（Sonnet 4.5 时代残留）。

**注意 Bedrock / Vertex 等 provider**：1M context 可能需要**显式开启**——看 provider 文档。

## 二、1M Context 的 Pricing

**长 context 走 Prompt Caching 经济性最好**——cache 读价是基础价 10%：

| 阶段 | Opus 5 输入 $/1M | Sonnet 5 输入 $/1M | Fable 5 输入 $/1M |
| --- | :---: | :---: | :---: |
| **基础（≤ 200k）** | $5 | $3 | $10 |
| **> 200k 部分** | $10（2x） | $6（2x） | $20（2x） |
| **Prompt Caching 写入** | +25% 基础价 | +25% | +25% |
| **Prompt Caching 读取** | 基础价 10% | 基础价 10% | 基础价 10% |

**关键认知**：
- 1M context 的 **> 200k 部分** 走 **2x 定价**——成本不只是 token 数翻倍
- **Prompt Caching 命中后** cache 读价只有 10%——长 context 场景必上

**实战示例**（100 万 token 输入，命中率 50%）：

```
无 cache:
  500k × $5/M + 500k × $10/M = $7.5

有 cache (50% 命中):
  cache 读: 500k × $0.5/M = $0.25    (cache 10% 价)
  cache 写: 250k × $6.25/M = $1.56   (首次 +25%)
  剩余: 250k × $5/M = $1.25
  总: $3.06  → 节省 59%
```

详见 [Prompt Caching API 详解](/claude-capabilities/api/prompt-caching)。

## 三、Long Context 衰减实测

**1M context 不是"全 context 都能用"**——社区 + 官方 benchmark 都观察到**中段衰减**：

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
- **中段内容用 explicit 引用**——"请参考第 700k token 处的那个函数..."
- **长文档问答中提具体位置**——"文档中部提到了 X，请确认"

## 四、长文档处理 4 种实战模式

### 模式 1：单文档问答（1M context 够）

```python
with open("long_doc.pdf", "rb") as f:
    pdf = base64.b64encode(f.read()).decode()

msg = client.messages.create(
    model="claude-opus-5",
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
    model="claude-sonnet-5",
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
    model="claude-opus-5",
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

## 五、何时不该用 long context

| 场景 | 该用 | 替代 |
| --- | :---: | --- |
| 单文档 < 100k token | 1M context | Sonnet 5 / Opus 5 |
| 单文档 100k-1M token | 1M context | Opus 5（强一些） |
| 单文档 > 1M token | **RAG** | 切片 + 检索 |
| 实时流式（视频 / 直播） | 不该用 long context | 帧提取 + vision |
| **大量重复 prompt** | **Prompt Caching** | cache 命中率优先 |
| 延迟敏感 | **不要** long context | 长 input 拖慢 first token |

**反直觉**：**长 context 不一定比短 context 慢太多**——Opus 5 / Sonnet 5 优化后 long context 的 first token 延迟**可接受**（< 1.5s）。但**输出延迟不变**——模型还是按输出 token 数计算。

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

**2. 1M context 全用 Sonnet 5 不上 cache**

**Sonnet 5 + 1M context 不开 Prompt Caching = 浪费 50%+ 成本**。长 context 必开 cache。

**3. 跨 Bedrock / Vertex 期望 1M 默认**

跨 provider 1M context 不一定默认——AWS Bedrock 上 Sonnet 5 1M 仍需 `sonnet[1m]` 显式开启。**跨云部署前查 provider 文档**。

**4. PDF > 1M context 切片直接传**

```python
# ❌ 100 页 PDF 全传 → 70k token → 还行
# ❌ 1000 页 PDF 全传 → 700k token → 还能
# ❌ 10000 页 PDF 全传 → 7M token → 爆 context

# ✅ 超 1M 走 RAG
```

**5. "全 context 都能用"幻觉**

"我 context 装得下 → Claude 全看得到"是错的。**中段衰减是事实**——长 context 任务必须主动"点名"关键信息位置。

## 参考

- [Anthropic Docs · Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows)（访问于 2026-08-06）
- [Anthropic Docs · Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)（访问于 2026-08-06）
- [Sonnet 5 · Prompt Caching 优化 5 错误](/claude-capabilities/models/sonnet#四prompt-caching-命中率优化)
- [Opus 5 详解](/claude-capabilities/models/opus)
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
