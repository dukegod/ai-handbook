---
title: Python SDK
description: '`anthropic` 官方 Python 包；同步 + async + streaming + 5 个实战模式（最小调用 / 工具循环 / 流式 / 结构化输出 / 缓存）'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  pythonSdk: 'https://github.com/anthropics/anthropic-sdk-python'
  pypi: 'https://pypi.org/project/anthropic/'
  accessedAt: 2026-08-07
---

# Python SDK

> **TL;DR**：`anthropic` 官方 Python 包——同步 + async 双接口，Streaming / Tool Use / Prompt Caching / Structured Outputs 全支持。**生产首选**——比 HTTP 调 Messages API 省心 100 倍。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 安装与初始化
- 5 个核心模式实战（最小调用 / Tool Use 循环 / Streaming / Structured Outputs / Prompt Caching）
- 同步 vs async 选型
- 错误处理与重试
- 5 个常见坑

## 一、安装与初始化

```bash
pip install anthropic
```

```python
import anthropic

# 默认读 ANTHROPIC_API_KEY 环境变量
client = anthropic.Anthropic()

# 或显式传
client = anthropic.Anthropic(api_key="sk-ant-...")

# 自定义 base_url（Azure / Bedrock / Vertex 代理）
client = anthropic.Anthropic(base_url="https://my-proxy.com")
```

## 二、5 个核心模式

### 模式 1：最小调用

```python
msg = client.messages.create(
    model="claude-sonnet-5-...",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)
print(msg.content[0].text)
```

### 模式 2：Tool Use 循环

```python
TOOLS = [{
    "name": "get_weather",
    "description": "查天气",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    },
}]

def run_agent(query):
    messages = [{"role": "user", "content": query}]
    for _ in range(20):
        msg = client.messages.create(
            model="claude-sonnet-5-...",
            max_tokens=4096,
            tools=TOOLS,
            messages=messages,
        )
        if msg.stop_reason == "end_turn":
            return next(b.text for b in msg.content if b.type == "text")
        if msg.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": msg.content})
            results = []
            for block in msg.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": results})
```

详见 [Tool Use API](/claude-capabilities/api/tool-use)。

### 模式 3：Streaming

```python
with client.messages.stream(
    model="claude-sonnet-5-...",
    max_tokens=1024,
    messages=[{"role": "user", "content": "讲个故事"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

详见 [流式响应](/claude-capabilities/api/streaming)。

### 模式 4：Structured Outputs

```python
TOOL = {
    "name": "extract_user",
    "description": "提取用户信息",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "email": {"type": "string"},
        },
        "required": ["name", "email"],
    },
}

msg = client.messages.create(
    model="claude-sonnet-5-...",
    max_tokens=512,
    tools=[TOOL],
    tool_choice={"type": "tool", "name": "extract_user"},
    messages=[{"role": "user", "content": "用户：Bob，30 岁，bob@x.com"}],
)

# 解析
for block in msg.content:
    if block.type == "tool_use":
        user = block.input
        # user = {"name": "Bob", "age": 30, "email": "bob@x.com"}
```

详见 [结构化输出](/claude-capabilities/api/structured-outputs)。

### 模式 5：Prompt Caching

```python
SYSTEM = [
    {
        "type": "text",
        "text": "你是 Python 审查员。代码风格：PEP 8 + async/await。",
        "cache_control": {"type": "ephemeral"},
    },
]

msg = client.messages.create(
    model="claude-sonnet-5-...",
    max_tokens=2048,
    system=SYSTEM,
    messages=[{"role": "user", "content": "审查：def foo(): pass"}],
)

# 看 cache 命中
print(f"cache_read: {msg.usage.cache_read_input_tokens}")
```

详见 [Prompt Caching](/claude-capabilities/api/prompt-caching)。

## 三、Async 接口

```python
import asyncio
import anthropic

async def main():
    client = anthropic.AsyncAnthropic()

    msg = await client.messages.create(
        model="claude-sonnet-5-...",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}],
    )
    print(msg.content[0].text)

asyncio.run(main())
```

**何时用 async**：
- Web 框架（FastAPI / Starlette / aiohttp）
- 高并发（同时 100+ 请求）
- Streaming 长输出 + WebSocket 推送

**何时用 sync**：
- 脚本 / CLI / 一次性任务
- 简单 demo

## 四、错误处理

```python
import anthropic
import time

try:
    msg = client.messages.create(...)
except anthropic.APIStatusError as e:
    if e.status_code == 429:
        # 速率限制 → 退避重试
        time.sleep(1)
        msg = client.messages.create(...)
    elif e.status_code >= 500:
        # 服务端错 → 重试
        msg = client.messages.create(...)
    else:
        raise    # 4xx 客户端错，不重试
except anthropic.APIConnectionError:
    # 网络错
    ...
```

**错误类型**：
- `APIStatusError`：HTTP 4xx / 5xx
- `APIConnectionError`：网络问题
- `APITimeoutError`：超时
- `RateLimitError`：429 限流

详见 [Messages API · 错误处理](/claude-capabilities/api/messages#七错误处理)。

## 五、5 个常见坑

**1. 忘记设 `max_tokens`**

```python
# ❌
client.messages.create(model="claude-sonnet-5-...", messages=[...])  # 400

# ✅
client.messages.create(model="claude-sonnet-5-...", max_tokens=1024, messages=[...])
```

**2. 同步 / async 混用**

```python
# ❌ sync client 配 await
client = anthropic.Anthropic()
await client.messages.create(...)   # TypeError

# ✅ async 用 AsyncAnthropic
client = anthropic.AsyncAnthropic()
```

**3. 同步阻塞 event loop**

```python
# ❌ async 函数里用 sync client（阻塞 event loop）
async def handler():
    msg = client.messages.create(...)   # 阻塞！
    return msg

# ✅ async 上下文用 AsyncAnthropic
async def handler():
    msg = await async_client.messages.create(...)
    return msg
```

**4. 流式不读 final_message**

```python
# ❌ 没用 usage
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text)

# ✅ 读 final_message
    final = stream.get_final_message()
    log_usage(final.usage)
```

**5. Tool Use 循环无上限**

必设 `MAX_TURNS`（如 20 步）——避免死循环 + 账单爆炸。

## 参考

- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)（访问于 2026-08-07）
- [PyPI · anthropic](https://pypi.org/project/anthropic/)（访问于 2026-08-07）
- [Messages API](/claude-capabilities/api/messages)
- [Tool Use API](/claude-capabilities/api/tool-use)
- [流式响应](/claude-capabilities/api/streaming)
- [结构化输出](/claude-capabilities/api/structured-outputs)
- [Prompt Caching](/claude-capabilities/api/prompt-caching)
- [TypeScript SDK](/claude-capabilities/sdk/typescript-sdk)
- [SDK 概览](/claude-capabilities/sdk/overview)

## 下一步

- TypeScript 对照 → [TypeScript SDK](/claude-capabilities/sdk/typescript-sdk)
- 多步 agent → [Agent SDK](/claude-capabilities/sdk/agent-sdk)
- Claude Code 嵌入应用 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)

## 如果你想

- examples/ 仓库骨架 → [SDK 概览 · 仓库骨架规划](/claude-capabilities/sdk/overview#七examples-仓库骨架)
- 错误处理细节 → [Messages API · 错误处理](/claude-capabilities/api/messages#七错误处理)
- 切到 TypeScript → [TypeScript SDK](/claude-capabilities/sdk/typescript-sdk)
