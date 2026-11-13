---
title: Token Counting
description: 预计算 token 用量的 count_tokens 端点；3 个实战场景（成本预估 / 超限拦截 / 拆分策略）
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-13
verifiedWith:
  scope: '2026-11-13 复核模型 ID、count_tokens 计数范围与 tokenizer 换代口径；示例未在本机实跑，token 数与成本为量级示意'
  claudeCode: 2.1.319
  model: claude-sonnet-5-5
  tokenCounting: 'https://platform.claude.com/docs/en/api/messages-count-tokens'
  tokenCountingGuide: 'https://platform.claude.com/docs/en/build-with-claude/token-counting'
  accessedAt: 2026-11-13
---

# Token Counting

> **TL;DR**：`count_tokens` 端点**预计算请求会消耗多少 token**——不调模型、零成本。3 个实战场景：成本预估（用户输入前报价）/ 超限拦截（防 400 错）/ 拆分策略（超 1M 怎么办）。

⏱ 预计阅读时间：3 分钟

## 一、最小调用

```python
import anthropic

client = anthropic.Anthropic()

count = client.messages.count_tokens(
    model="claude-sonnet-5-5",
    messages=[{"role": "user", "content": "Hello, Claude"}],
    system="你是 helpful 助手",
)

print(f"input tokens: {count.input_tokens}")
# input tokens: 18
```

**关键**：**不计费、不调模型、纯计算**——可以高频用。

## 二、3 个实战场景

### 1. 成本预估

```python
def estimate_cost(text: str, model: str) -> float:
    count = client.messages.count_tokens(model=model, messages=[{"role": "user", "content": text}])
    pricing = {"claude-sonnet-5-5": 2, "claude-opus-5-5": 4, "claude-haiku-5-5": 0.1}  # $/MTok 输入价
    return count.input_tokens / 1_000_000 * pricing[model]

print(estimate_cost("一段 1000 字的文本", "claude-sonnet-5-5"))
# 1000 汉字约 1000-2000 token → 约 $0.002-0.004
```

⚠ **Haiku 5.5 是唯一分档计费的型号**——prompt 超过 100k token 时，输入输出各跳 5 倍。报价别忘了乘。

### 2. 超限拦截

```python
def safe_create(model, messages, max_tokens=1024, max_input=200_000):
    count = client.messages.count_tokens(model=model, messages=messages)
    if count.input_tokens > max_input:
        # 切片 / 摘要 / 改模型
        raise InputTooLongError(f"input {count.input_tokens} > {max_input}")
    return client.messages.create(model=model, messages=messages, max_tokens=max_tokens)
```

当前四型号（Fable 5.2 / Opus 5.5 / Sonnet 5.5 / Haiku 5.5）都是 **1M context**——`max_input` 按目标型号的实际窗口设，别照抄 200k。

### 3. 拆分策略

```python
# 检查是否需要切分
count = client.messages.count_tokens(model=model, messages=messages)
if count.input_tokens > 200_000:
    # 走 RAG / 切片
    chunks = split_by_tokens(text, max_tokens=200_000)
    # 多次请求
```

## 三、与 vision / files 的计算

`count_tokens` **精确计算**多模态输入：

```python
import base64

with open("chart.png", "rb") as f:
    img = base64.b64encode(f.read()).decode()

count = client.messages.count_tokens(
    model="claude-sonnet-5-5",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img}},
            {"type": "text", "text": "描述"},
        ],
    }],
)
print(f"input tokens: {count.input_tokens}")   # 包含图片按尺寸算的 token
```

⚠ 图片和 PDF **必须用 base64 传**——`url` / `file` 来源的图像或文档块会让 `count_tokens` 直接报 `invalid_request_error`。

详见 [Vision · Token 计算公式](/claude-capabilities/core/vision#三、token-计算)。

## 四、4 个常见坑

**1. 期望 `count_tokens` 包含输出 token**

不能——`count_tokens` 只算**输入**，输出 token 取决于模型实际生成。

**2. 以为 `tools` 不计入**

官方口径：`input_tokens` 是 **messages + system prompt + tools** 的总和，图片和 PDF 也算。所以 `tools` 定义不用自己折算。

```python
count = client.messages.count_tokens(
    model="claude-sonnet-5-5",
    system="你是 helpful 助手",
    tools=[{"name": "get_weather", "description": "查天气", "input_schema": {...}}],
    messages=[{"role": "user", "content": "北京今天天气？"}],
)
```

⚠ 另一头：server tools（web search / web fetch / code execution / tool search）和 MCP connector 会让 `count_tokens` 报 `invalid_request_error`——这类请求的用量得回 Messages 响应的 `usage` 里读。

**3. 不算 cache**

`count_tokens` 报的是"未缓存"输入——缓存命中后实际计费更低。详见 [Prompt Caching](/claude-capabilities/api/prompt-caching)。

**4. 跟实际有 ± 5% 偏差**

tokenizer 边界条件（特殊字符、多语言混合）会有微小差异。**预算留 5-10% buffer**。

⚠ **更大的偏差来自换 tokenizer**：Claude 4.7 世代及之后的型号（Fable 5.x / Opus 4.7+ / Sonnet 5.5 / Haiku 5.5 等）用新 tokenizer，同样输入文本**约多 30% token**（官方口径，具体幅度取决于内容与负载形态）。`count_tokens` 按你传入的 `model` 的 tokenizer 计——**换型号必须重算**，不能复用旧型号量出来的数。

换算口径（官方 models overview）：

- **1M token ≈ 555k 词 ≈ 250 万 Unicode 字符**（当前 tokenizer，Claude Opus 4.7 引入）
- 更早的型号：1M token ≈ 750k 词
- 200k token ≈ 150k 词

（按词数算是 750k → 555k，约 35%；官方给的 token 增幅是"约 30%"——两个口径描述同一件事。）

## 参考

- [Anthropic Docs · Count Tokens](https://platform.claude.com/docs/en/api/messages-count-tokens)（访问于 2026-11-13）
- [Anthropic Docs · Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting)（访问于 2026-11-13）
- [Anthropic Docs · Models overview（context window 换算）](https://platform.claude.com/docs/en/about-claude/models/overview)（访问于 2026-11-13）
- [Messages API](/claude-capabilities/api/messages)
- [Vision · Token 计算](/claude-capabilities/core/vision#三、token-计算)
- [Prompt Caching](/claude-capabilities/api/prompt-caching)
- [成本与 Token 管理](/claude-code/basics/cost-and-tokens)

## 下一步

- Admin & Usage 报告 → [Admin & Usage](/claude-capabilities/api/admin-usage)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)
- 完整 token 优化 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)

## 如果你想

- 长 context token 策略 → [长上下文](/claude-capabilities/core/long-context)
- 工具 token 不算坑 → [Tool Use API](/claude-capabilities/api/tool-use)
