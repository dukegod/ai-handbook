---
title: Token Counting
description: 预计算 token 用量的 count_tokens 端点；3 个实战场景（成本预估 / 超限拦截 / 拆分策略）
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5-...
  tokenCounting: 'https://platform.claude.com/docs/en/api/messages-count-tokens'
  accessedAt: 2026-08-07
---

# Token Counting

> **TL;DR**：`count_tokens` 端点**预计算请求会消耗多少 token**——不调模型、零成本。3 个实战场景：成本预估（用户输入前报价）/ 超限拦截（防 400 错）/ 拆分策略（超 1M 怎么办）。

⏱ 预计阅读时间：3 分钟

## 一、最小调用

```python
import anthropic

client = anthropic.Anthropic()

count = client.messages.count_tokens(
    model="claude-sonnet-5-...",
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
    pricing = {"claude-sonnet-5-...": 3, "claude-opus-5-...": 5, "claude-haiku-4-5-...": 1}
    return count.input_tokens / 1_000_000 * pricing[model]

print(estimate_cost("一段 1000 字的文本", "claude-sonnet-5-..."))
# 0.006
```

### 2. 超限拦截

```python
def safe_create(model, messages, max_tokens=1024, max_input=200_000):
    count = client.messages.count_tokens(model=model, messages=messages)
    if count.input_tokens > max_input:
        # 切片 / 摘要 / 改模型
        raise InputTooLongError(f"input {count.input_tokens} > {max_input}")
    return client.messages.create(model=model, messages=messages, max_tokens=max_tokens)
```

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
    model="claude-sonnet-5-...",
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

详见 [Vision · Token 计算公式](/claude-capabilities/core/vision#三token-计算)。

## 四、4 个常见坑

**1. 期望 `count_tokens` 包含输出 token**

不能——`count_tokens` 只算**输入**，输出 token 取决于模型实际生成。

**2. 不算 `tools`**

```python
# count_tokens 不算 tools 定义占的 token
# 生产里把 tools 也算进去
total = count.input_tokens + sum(len(json.dumps(t)) for t in tools) // 4
```

**3. 不算 cache**

`count_tokens` 报的是"未缓存"输入——缓存命中后实际计费更低。详见 [Prompt Caching](/claude-capabilities/api/prompt-caching)。

**4. 跟实际有 ± 5% 偏差**

tokenizer 边界条件（特殊字符、多语言混合）会有微小差异。**预算留 5-10% buffer**。

## 参考

- [Anthropic Docs · Count Tokens](https://platform.claude.com/docs/en/api/messages-count-tokens)（访问于 2026-08-07）
- [Messages API](/claude-capabilities/api/messages)
- [Vision · Token 计算](/claude-capabilities/core/vision#三token-计算)
- [Prompt Caching](/claude-capabilities/api/prompt-caching)
- [成本与 Token 管理](/claude-code/basics/cost-and-tokens)

## 下一步

- Admin & Usage 报告 → [Admin & Usage](/claude-capabilities/api/admin-usage)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)
- 完整 token 优化 → [成本与 Token 管理](/claude-code/basics/cost-and-tokens)

## 如果你想

- 长 context token 策略 → [长上下文](/claude-capabilities/core/long-context)
- 工具 token 不算坑 → [Tool Use API](/claude-capabilities/api/tool-use)
