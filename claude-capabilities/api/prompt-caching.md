---
title: Prompt Caching
description: cache_control 协议 + 4 种 TTL + 实战命中率优化（多 block / 独立 TTL / system 字段用法）
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5
  promptCaching: 'https://platform.claude.com/docs/en/build-with-claude/prompt-caching'
  accessedAt: 2026-08-07
---

# Prompt Caching

> **TL;DR**：在请求中加 `cache_control: {"type": "ephemeral"}` 让该 block **缓存 5 分钟**——缓存命中时输入价格是基础价 **10%**。长 context 场景必开，能砍 30-60% 成本。

⏱ 预计阅读时间：5 分钟

## 一、cache_control 协议

```json
{
  "model": "claude-sonnet-5-...",
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
- 默认对 system 字段前 **4 个 block** 自动生效（API 自动加 ephemeral）
- 命中 cache → 价格是基础价 10%

## 二、4 种 TTL

| TTL | 用途 | 价格倍率 |
| --- | --- | --- |
| `ephemeral`（5 分钟） | 短时高频 | 读 1x，写 1.25x |
| `1h` | 中等场景 | 读 1x，写 2x |

> 注：Anthropic 当前主推 `ephemeral`，长期 TTL 在不同 plan 上可能有差异。

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
        model="claude-sonnet-5-...",
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
# 第 2 次：命中 cache（10% 价格）
review("def bar(): pass")
```

**关键字段**：
- `usage.input_tokens` — 本次新输入
- `usage.cache_creation_input_tokens` — 本次写入 cache 的 token
- `usage.cache_read_input_tokens` — 本次命中 cache 的 token

## 五、何时该用 cache

| 场景 | 用 cache？ | 预期收益 |
| --- | :---: | --- |
| 长 system prompt（> 500 token） | ✅ | 显著（命中率高） |
| Few-shot 示例（3+ examples） | ✅ | 显著 |
| 长文档 RAG（重复引用） | ✅ | 显著 |
| 多轮对话（前几轮不变） | ✅ | 中等 |
| 一次性短 prompt | ❌ | 命中率低 |
| 每次内容完全不同 | ❌ | 完全 miss |

**经验阈值**：**system 字段 > 1024 token + 请求频次高** → 必上 cache。

## 六、4 个常见坑

**1. 默认只看前 4 块**

```python
system = [block1, block2, block3, block4, block5, block6]
# 只有前 4 块自动 cache
# 5、6 不 cache
```

**解决**：前 4 块放**最稳定的内容**（角色 + 风格）；少变的放后 4 块（也可显式 cache_control）。

**2. 块大小限制**

每个 cache block 限制 **4 blocks / 5 breakpoints**——超过会报 400。

**3. cache 写比读贵 25%**

```python
# 写 cache: 1.25x 价格
# 读 cache: 0.1x 价格
# 5+ 次读取才能摊平写成本
```

**4. 跨 region cache 不共享**

`us-east-1` 写的 cache 在 `eu-west-1` 不命中。

## 参考

- [Anthropic Docs · Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)（访问于 2026-08-07）
- [Sonnet 5 · Prompt Caching 5 错误](/claude-capabilities/models/sonnet#四prompt-caching-命中率优化)
- [System Prompt 设计](/claude-capabilities/prompting/system-prompts)
- [Messages API](/claude-capabilities/api/messages)
- [成本与 Token 管理](/claude-code/basics/cost-and-tokens)

## 下一步

- 批处理（50% 折扣）→ [Message Batches](/claude-capabilities/api/message-batches)
- 文件引用 → [Files API](/claude-capabilities/api/files)
- Token 用量 → [Token Counting](/claude-capabilities/api/token-counting)

## 如果你想

- 命中率优化 → [Sonnet 5 · 5 错误](/claude-capabilities/models/sonnet#四prompt-caching-命中率优化)
- 长 context 实战 → [长上下文](/claude-capabilities/core/long-context)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)
