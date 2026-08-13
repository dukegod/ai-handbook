---
title: Messages API
description: HTTP 主入口——请求结构、响应 blocks、5 个核心参数、3 段完整可运行代码（curl / Python / TypeScript）
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  messagesApi: 'https://platform.claude.com/docs/en/api/messages'
  accessedAt: 2026-08-07
---

# Messages API

> **TL;DR**：Messages API 是 Claude API 的**HTTP 主入口**——发请求 `POST /v1/messages`、收响应 `content` blocks。本页是**协议层**视角（HTTP / 请求结构 / 响应结构 / 参数），[Python SDK](/claude-capabilities/sdk/python-sdk) 与 [TypeScript SDK](/claude-capabilities/sdk/typescript-sdk) 是它的客户端封装。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- Messages API 是什么 / 协议层定位 / 与 SDK 的关系
- 完整可运行代码 3 段（curl / Python / TypeScript）
- 请求结构（model / messages / system / max_tokens / 关键参数）
- 响应结构（content blocks / stop_reason / usage）
- 5 个核心参数详解
- 错误处理（status codes / retry）
- 4 类常见消息结构
- 5 个常见坑

## 一、Messages API 是什么

```
┌─────────────────────────────────────────┐
│ 你的应用                                 │
│   ↓ POST /v1/messages                  │
├─────────────────────────────────────────┤
│ Anthropic API（Messages API）           │
│   ↓ response: content blocks           │
├─────────────────────────────────────────┤
│ Claude 模型（Opus 5 / Sonnet 5 / ...）  │
└─────────────────────────────────────────┘
```

**核心路径**：

```
POST https://api.anthropic.com/v1/messages
Headers:
  x-api-key: $ANTHROPIC_API_KEY
  anthropic-version: 2023-06-01
  content-type: application/json

Body:
  {
    "model": "claude-sonnet-5-...",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "..."}]
  }
```

**与 SDK 的关系**：
- **HTTP API 是协议层**——所有 SDK 内部都调这个
- **SDK 是客户端封装**——Python / TypeScript / Agent SDK 都是
- 学了 HTTP API，再看 SDK 就像看"魔术揭秘"

## 二、3 段完整可运行代码

### 1. curl（最简）

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-5-...",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello, Claude"}]
  }'
```

### 2. Python（推荐生产用）

```python
import anthropic

client = anthropic.Anthropic()  # 读 ANTHROPIC_API_KEY env var

msg = client.messages.create(
    model="claude-sonnet-5-...",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)

print(msg.content[0].text)
```

### 3. TypeScript

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const msg = await client.messages.create({
  model: "claude-sonnet-5-...",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
});

console.log(msg.content[0].text);
```

**验证运行**：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python3 hello.py    # 期望输出：'Hello! How can I help you today?'
```

## 三、请求结构

```json
{
  "model": "claude-sonnet-5-...",     // 必填：Model ID
  "max_tokens": 1024,                  // 必填：最大输出 token
  "messages": [                        // 必填：消息数组
    {"role": "user", "content": "..."}
  ],
  "system": "你是 helpful 助手",       // 可选：System prompt
  "temperature": 1.0,                  // 可选：0-1
  "top_p": 0.9,                        // 可选：nucleus sampling
  "top_k": 40,                         // 可选
  "stop_sequences": ["\n\nHuman:"],    // 可选：自定义 stop
  "stream": false,                     // 可选：流式响应
  "metadata": {"user_id": "u_123"},   // 可选：追踪字段
  "tools": [...]                       // 可选：tool definitions
}
```

## 四、响应结构

```json
{
  "id": "msg_01ABC...",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello! How can I help you today?"
    }
  ],
  "model": "claude-sonnet-5-...",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "output_tokens": 11
  }
}
```

**关键字段**：
- `content`：**block 数组**——可能含 text / image / tool_use / thinking block
- `stop_reason`：`end_turn`（完成）/ `max_tokens`（超长截断）/ `tool_use`（要调工具）/ `stop_sequence`（触发 stop）
- `usage`：token 用量——计费依据

## 五、5 个核心参数

### 1. `model`（必填）

```
claude-opus-5-...
claude-sonnet-5-...
claude-haiku-4-5-...
claude-fable-5-...
```

完整列表见 [模型家族总览](/claude-capabilities/models/overview)。

### 2. `max_tokens`（必填）

最大输出 token 数。**必须设**——不设会 400 错。

各模型上限：
- Opus 5 / Sonnet 5 / Fable 5: **128k**
- Haiku 4.5: **64k**

### 3. `messages`（必填）

消息数组，每条形如 `{"role": "user|assistant", "content": "..."}`。

**关键约束**：
- 第一条必须是 `user` 角色
- `user` 和 `assistant` 交替
- 多轮对话：append 之前的 assistant 响应

### 4. `system`（可选）

System prompt——放角色、规则、风格。详见 [System Prompt 设计](/claude-capabilities/prompting/system-prompts)。

### 5. `stream`（可选）

是否流式响应。`true` 时返回 SSE 流；`false` 一次性返回。

详见 [流式响应](/claude-capabilities/api/streaming)。

## 六、4 类常见消息结构

### 1. 单轮对话

```json
{"messages": [{"role": "user", "content": "Hello"}]}
```

### 2. 多轮对话

```json
{
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "What's the weather?"}
  ]
}
```

### 3. 多模态（图）

```json
{
  "messages": [{
    "role": "user",
    "content": [
      {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "..."}},
      {"type": "text", "text": "描述这张图"}
    ]
  }]
}
```

详见 [视觉能力](/claude-capabilities/core/vision)。

### 4. Tool Use

```json
{
  "messages": [{"role": "user", "content": "查 JIRA 上的 ISSUE-1234"}],
  "tools": [{"name": "search_jira", ...}]
}
# → response.content[0].type == "tool_use"
```

详见 [Tool Use 协议](/claude-capabilities/core/tool-use)。

## 七、错误处理

| Status | 含义 | 处理 |
| --- | --- | --- |
| 200 | 成功 | — |
| 400 | 请求参数错（model 不存在、max_tokens 超限） | 修参数 |
| 401 | API key 无效 | 检查 env var |
| 403 | 权限不足（账号欠费 / ZDR 限制） | 检查账号 |
| 404 | endpoint 不存在 | 检查 URL |
| 429 | 速率限制 | 退避重试 |
| 500 | 服务端错 | 重试 |
| 529 | 过载 | 退避重试 |

**Python SDK 错误处理**：

```python
import anthropic

client = anthropic.Anthropic()

try:
    msg = client.messages.create(...)
except anthropic.APIStatusError as e:
    if e.status_code == 429:
        # 退避重试
        time.sleep(1)
        msg = client.messages.create(...)
    elif e.status_code >= 500:
        # 服务端错，重试
        ...
    else:
        raise    # 客户端错，不重试
```

**重试策略**：

| Status | 重试？ | 退避 |
| --- | :---: | --- |
| 429 | ✅ | 指数退避（1s → 2s → 4s ...） |
| 500 / 529 | ✅ | 同上 |
| 4xx（除 429） | ❌ | 改参数 |

## 八、5 个常见坑

**1. 忘记设 `max_tokens`**

```python
# ❌
client.messages.create(model="claude-sonnet-5-...", messages=[...])  # 400

# ✅
client.messages.create(model="claude-sonnet-5-...", max_tokens=1024, messages=[...])
```

**2. `messages` 第一条不是 user**

```json
// ❌
{"messages": [{"role": "assistant", "content": "Hi"}]}

// ✅
{"messages": [{"role": "user", "content": "Hi"}]}
```

**3. 多轮对话忘 append assistant 响应**

```python
# ❌ 缺中间轮
messages = [
    {"role": "user", "content": "A"},
    {"role": "user", "content": "B"},   # Claude 不知 A 之后发生了什么
]

# ✅
messages = [
    {"role": "user", "content": "A"},
    {"role": "assistant", "content": "response to A"},
    {"role": "user", "content": "B"},
]
```

**4. `stop_reason: "max_tokens"` 没处理**

模型输出被截断（max_tokens 设太小）——**生产里要检测**并补救（提示用户"继续"或换更大 max_tokens）。

**5. Token 用量 (`usage`) 不记账**

```python
# ❌ 不知道花了多少
msg = client.messages.create(...)

# ✅ 记账
total_input += msg.usage.input_tokens
total_output += msg.usage.output_tokens
```

详见 [成本与 Token 管理](/claude-code/basics/cost-and-tokens)。

## 参考

- [Anthropic Docs · Messages API](https://platform.claude.com/docs/en/api/messages)（访问于 2026-08-07）
- [Anthropic Docs · API Overview](https://docs.claude.com/en/api/overview)（访问于 2026-08-07）
- [Python SDK](/claude-capabilities/sdk/python-sdk)
- [TypeScript SDK](/claude-capabilities/sdk/typescript-sdk)
- [Tool Use 协议](/claude-capabilities/core/tool-use)
- [流式响应](/claude-capabilities/api/streaming)
- [成本与 Token 管理](/claude-code/basics/cost-and-tokens)

## 下一步

- 流式响应 → [流式响应](/claude-capabilities/api/streaming)
- Tool Use 协议 → [Tool Use 协议](/claude-capabilities/core/tool-use)
- SDK 客户端封装 → [Python SDK](/claude-capabilities/sdk/python-sdk)

## 如果你想

- 结构化输出 → [结构化输出](/claude-capabilities/api/structured-outputs)
- Prompt Caching → [Prompt Caching API](/claude-capabilities/api/prompt-caching)
- Token 计算 → [Token Counting](/claude-capabilities/api/token-counting)
