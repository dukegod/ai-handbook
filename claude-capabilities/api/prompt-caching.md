---
title: Prompt Caching
description: cache_control 协议 + 2 种 TTL + 实战命中率优化（多 block / 独立 TTL / system 字段用法）
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 复核了缓存读写倍率、两种 TTL、breakpoint 上限与最小可缓存长度；本页示例未在本机重跑'
  claudeCode: 2.1.319
  model: claude-sonnet-5-5
  promptCaching: 'https://platform.claude.com/docs/en/build-with-claude/prompt-caching'
  pricing: 'https://platform.claude.com/docs/en/about-claude/pricing'
  accessedAt: 2026-11-13
---

# Prompt Caching

> **TL;DR**：在请求中加 `cache_control: {"type": "ephemeral"}` 让该 block **缓存 5 分钟**——命中时输入价按基础价打折（Sonnet 5.5 / Opus 5.5 为 **5%**，Fable 5.2 为 **2.5%**）。长 context 场景必开，能砍 30-60% 成本。

⏱ 预计阅读时间：5 分钟

## 一、cache_control 协议

```json
{
  "model": "claude-sonnet-5-5",
  "system": [
    {
      "type": "text",
      "text": "你是 Python 代码审查员...",
      "cache_control": {"type": "ephemeral"}
    },
    {
      "type": "text",
      "text": "以下是项目代码风格约定...",
      "cache_control": {"type": "ephemeral"}
    }
  ],
  "messages": [...]
}
```

**关键认知**：
- `cache_control` 加在 **block 级别**（不是整个 system 字段）
- 一次请求最多 **4 个 cache breakpoint**（每个 `cache_control` 占 1 个）
- 也可以在请求**顶层**放 `cache_control` → 自动缓存到最后一个可缓存 block（同样占 1 个槽位）
- 缓存前缀按 `tools` → `system` → `messages` 顺序生成
- 命中 cache → 输入价按基础价打折（倍率见下）

## 二、2 种 TTL

| TTL | 用途 | 写入倍率 |
| --- | --- | --- |
| `ephemeral`（5 分钟，默认） | 短时高频 | × 1.25 |
| `1h` | 中等场景 | × 2 |

**缓存读命中倍率**（相对基础输入价）：

- Fable 5.2 / Fable 5.1：**× 0.025**
- Opus 5.5 / Sonnet 5.5：**× 0.05**（Sonnet 5.5 即 $2 → $0.10 / MTok）
- 其余型号（含 Haiku 5.5）：**× 0.1**

> 5 分钟 TTL 命中后自动续期，续期不额外计费；`1h` 适合「间隔 > 5 分钟但 < 1 小时」的场景，也**不计入命中缓存的速率限制**。

## 三、实战命中率优化

### 1. 多 block 独立 TTL

```python
system = [
    {"type": "text", "text": "角色设定", "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": "Few-shot 示例 1", "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": "Few-shot 示例 2", "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": "Few-shot 示例 3", "cache_control": {"type": "ephemeral"}},
]
# 4 个 block 独立 cache——某 block 变了其他 3 个仍命中
```

### 2. System 字段用 list 而非 string

```python
# ❌ 整个 system 一个 cache（任一字符变了全失效）
system = "你是 Python 审查员 + Few-shot 1 + Few-shot 2 + ..."

# ✅ 多个 block 独立 cache
system = [
    {"type": "text", "text": "你是 Python 审查员", "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": "Few-shot 1", "cache_control": {"type": "ephemeral"}},
    ...
]
```

### 3. 不加时间戳

```python
# ❌ 每次请求 datetime 不同 → cache miss
{"role": "user", "content": f"现在时间 {datetime.now()}，请回答：..."}

# ✅ 时间放 system（不变）或不放
{"role": "user", "content": "请回答：..."}
```

### 4. tool 顺序固定

```python
# ❌ tool list 每次顺序不同
tools = random.sample(TOOLS, len(TOOLS))

# ✅ 固定顺序
tools = [tool_a, tool_b, tool_c]
```

**改 `tool_choice` 会让已缓存的 message block 失效**（tool 定义与 system 仍缓存）——所以 tool 顺序和 `tool_choice` 都要稳定。

### 5. Image / PDF 放末尾

```python
# ✅ 不可变放 system（cache），可变放 messages 末尾
messages = [
    {"role": "user", "content": [
        {"type": "text", "text": "可变问题"},
        {"type": "image", "source": {...}},  # 末尾
    ]}
]
```

## 四、完整可运行示例

```python
import anthropic

client = anthropic.Anthropic()

# System 跨请求不变
SYSTEM = [
    {
        "type": "text",
        "text": "你是资深 Python 代码审查员，10 年经验。",
        "cache_control": {"type": "ephemeral"},
    },
    {
        "type": "text",
        "text": "代码风格：PEP 8、async/await、Result<T, E> 错误处理。",
        "cache_control": {"type": "ephemeral"},
    },
]

def review(code: str) -> str:
    msg = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=2048,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"审查：\n{code}"}],
    )
    # 读 usage 看 cache 命中
    usage = msg.usage
    print(f"input: {usage.input_tokens}, cache_read: {usage.cache_read_input_tokens}")
    return msg.content[0].text

# 第 1 次：写 cache（贵）
review("def foo(): pass")
# 第 2 次：命中 cache（Sonnet 5.5 读价 = 基础价的 5%）
review("def bar(): pass")
```

**关键字段**：
- `usage.input_tokens` — 最后一个 cache breakpoint **之后**的 token
- `usage.cache_creation_input_tokens` — 本次写入 cache 的 token
- `usage.cache_read_input_tokens` — 本次命中 cache 的 token

总输入 = 三者之和。

## 五、何时该用 cache

| 场景 | 用 cache？ | 预期收益 |
| --- | :---: | --- |
| 长 system prompt（> 512 token） | ✅ | 显著（命中率高） |
| Few-shot 示例（3+ examples） | ✅ | 显著 |
| 长文档 RAG（重复引用） | ✅ | 显著 |
| 多轮对话（前几轮不变） | ✅ | 中等 |
| 一次性短 prompt | ❌ | 命中率低 |
| 每次内容完全不同 | ❌ | 完全 miss |

**最小可缓存长度**：当前四型号（Fable 5.2 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5）统一是 **512 token**——低于这个长度**不报错，但根本不缓存**。老型号（Sonnet 4.5 / Opus 4.5 / Haiku 4.5）要 1024~4096 token。

**经验阈值**：**system 字段 > 1024 token + 请求频次高** → 必上 cache。

## 六、4 个常见坑

**1. breakpoint 上限 4 个**

```python
# ❌ 5 个 block 各带 cache_control → 第 5 个报错
system = [
    {"type": "text", "text": "角色", "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": "风格", "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": "示例", "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": "约定", "cache_control": {"type": "ephemeral"}},
    {"type": "text", "text": "补充", "cache_control": {"type": "ephemeral"}},  # ← 超了
]
```

整个请求（`tools` + `system` + `messages` 合计）最多 **4 个 cache breakpoint**；顶层自动缓存也占其中 1 个。

**解决**：前 4 块放**最稳定的内容**（角色 + 风格）；少变的放后面（也可显式 cache_control）。

**2. 没到最小长度 = 静默不缓存**

```python
# ❌ system 只有 300 token → 低于 512 token 门槛，不缓存也不报错
system = [{"type": "text", "text": "很短的设定", "cache_control": {"type": "ephemeral"}}]
```

看 `usage`：`cache_creation_input_tokens` 和 `cache_read_input_tokens` 都是 0，就说明没缓存。

**3. cache 写比读贵**

```python
# 5 分钟 TTL：写 1.25x，读 0.05x（Sonnet 5.5）
# 第 2 次调用就回本，不必等 5 次
```

**4. 跨 region cache 不共享**

`us-east-1` 写的 cache 在 `eu-west-1` 不命中。

## 参考

- [Anthropic Docs · Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)（访问于 2026-11-13）
- [Anthropic Docs · Pricing](https://platform.claude.com/docs/en/about-claude/pricing)（访问于 2026-11-13）
- [Sonnet 5.5 · Prompt Caching 命中率优化](/claude-capabilities/models/sonnet#四、prompt-caching-命中率优化)
- [System Prompt 设计](/claude-capabilities/prompting/system-prompts)
- [Messages API](/claude-capabilities/api/messages)
- [成本与 Token 管理](/claude-code/basics/cost-and-tokens)

## 下一步

- 批处理（50% 折扣）→ [Message Batches](/claude-capabilities/api/message-batches)
- 文件引用 → [Files API](/claude-capabilities/api/files)
- Token 用量 → [Token Counting](/claude-capabilities/api/token-counting)

## 如果你想

- 命中率优化 → [Sonnet 5.5 · Prompt Caching 命中率优化](/claude-capabilities/models/sonnet#四、prompt-caching-命中率优化)
- 长 context 实战 → [长上下文](/claude-capabilities/core/long-context)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)
