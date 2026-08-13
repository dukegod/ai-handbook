---
title: 流式响应
description: SSE 协议的 stream=true 模式；5 类事件、Python / TypeScript 实战、何时该用流式
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  streaming: 'https://platform.claude.com/docs/en/api/messages#stream'
  accessedAt: 2026-08-07
---

# 流式响应

> **TL;DR**：设 `stream=true` 让响应**逐块返回**（SSE 协议）——首 token < 1s，体感"打字机效果"。**何时该用**：长输出（> 500 token）/ 用户等待场景 / 长链 agent 单步响应。**何时不该用**：短输出 / 批处理 / 需要完整 result 才能继续。

⏱ 预计阅读时间：4 分钟

## 一、SSE 协议概览

```
请求：
  stream: true
  ↓
响应（HTTP chunked）：
  event: message_start
  data: {"type":"message_start","message":{...}}

  event: content_block_start
  data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}

  event: content_block_delta
  data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Hello"}}

  event: content_block_delta
  data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":" there"}}

  event: content_block_stop
  event: message_delta
  event: message_stop
```

## 二、5 类事件

| 事件 | 含义 |
| --- | --- |
| `message_start` | 消息开始（含 id / model / usage.input_tokens） |
| `content_block_start` | block 开始（text / tool_use / thinking） |
| `content_block_delta` | block 内容增量（text_delta / input_json_delta / thinking_delta） |
| `content_block_stop` | block 结束 |
| `message_delta` | 消息级更新（stop_reason / usage.output_tokens） |
| `message_stop` | 消息结束 |

## 三、Python 实战

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-5-...",
    max_tokens=1024,
    messages=[{"role": "user", "content": "讲个故事"}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    print()

# 流结束后可读最终 message
final = stream.get_final_message()
print(f"input tokens: {final.usage.input_tokens}")
print(f"output tokens: {final.usage.output_tokens}")
```

## 四、TypeScript 实战

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const stream = client.messages.stream({
  model: "claude-sonnet-5-...",
  max_tokens: 1024,
  messages: [{ role: "user", content: "讲个故事" }],
});

for await (const event of stream) {
  if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
    process.stdout.write(event.delta.text);
  }
}
```

## 五、何时该用流式

| 场景 | 用流式？ | 原因 |
| --- | :---: | --- |
| 长输出（> 500 token） | ✅ | 首 token 快 + 体感流畅 |
| 用户等待场景 | ✅ | 减少 perceived latency |
| 聊天 UI | ✅ | 打字机效果 |
| 长链 agent 单步 | ✅ | 实时显示 agent 在做什么 |
| 短输出（< 100 token） | ❌ | 流式开销不必要 |
| 批处理 | ❌ | 一次拿全才好处理 |
| 必须拿到完整 result 才能继续 | ❌ | 流式逐字到达无意义 |

## 六、5 个常见坑

**1. 流式 + JSON 输出**

Claude 流式输出时**JSON 不完整**——`{` 之后下一 chunk 还没到。**生产用 `tool_use` 实现 JSON**（见 [结构化输出](/claude-capabilities/api/structured-outputs)）。

**2. 流式 + 同步 UI**

```python
# ❌ 阻塞 UI
for text in stream.text_stream:
    print(text, end="")

# ✅ 异步 / 回调
def on_text(text):
    ui_update(text)    # 推到前端

for text in stream.text_stream:
    on_text(text)
```

**3. 流式 + tool_use 循环**

每次 `tool_use` 是单独 block——**流到 `tool_use` block 结束时再执行工具**，不要在 delta 阶段就执行。

**4. 不读 `final_message`**

```python
# ❌ 没用 usage
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text)

# ✅ 读 final_message
    final = stream.get_final_message()
    log_usage(final.usage)
```

**5. 流式 + 异常处理**

流式中途断网 → **SDK 抛异常**。生产里要 try/except 重试。

## 参考

- [Anthropic Docs · Messages API · Stream](https://platform.claude.com/docs/en/api/messages#stream)（访问于 2026-08-07）
- [Messages API](/claude-capabilities/api/messages)
- [结构化输出](/claude-capabilities/api/structured-outputs)
- [Python SDK · 流式实战](/claude-capabilities/sdk/python-sdk)

## 下一步

- 强制 JSON 输出 → [结构化输出](/claude-capabilities/api/structured-outputs)
- Prompt 缓存优化 → [Prompt Caching](/claude-capabilities/api/prompt-caching)
- 切到 SDK → [Python SDK](/claude-capabilities/sdk/python-sdk)

## 如果你想

- 流式 + tool_use 组合 → [Tool Use API](/claude-capabilities/api/tool-use)
- 流式 + 长输出策略 → [长上下文](/claude-capabilities/core/long-context)
- 多 agent 流式 → [Subagent 编排](/claude-code/subagents-and-workflows/workflow-orchestration)
