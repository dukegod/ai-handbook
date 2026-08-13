---
title: TypeScript SDK
description: '`@anthropic-ai/sdk` 官方 TS 包；Node / Deno / 浏览器 + 5 模式实战'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  typescriptSdk: 'https://github.com/anthropics/anthropic-sdk-typescript'
  npm: 'https://www.npmjs.com/package/@anthropic-ai/sdk'
  accessedAt: 2026-08-07
---

# TypeScript SDK

> **TL;DR**：`@anthropic-ai/sdk` 官方 TypeScript 包——Node / Deno / 现代浏览器全支持，**类型安全**（TypeScript 5+）。与 [Python SDK](/claude-capabilities/sdk/python-sdk) 是 Anthropic 唯二官方 SDK，**前端 / Node 生态首选**。

⏱ 预计阅读时间：5 分钟

## 一、安装与初始化

```bash
npm install @anthropic-ai/sdk
```

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
// 默认读 ANTHROPIC_API_KEY 环境变量
```

## 二、5 个核心模式

### 模式 1：最小调用

```typescript
const msg = await client.messages.create({
  model: "claude-sonnet-5-...",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude" }],
});
console.log(msg.content[0].text);
```

### 模式 2：Tool Use 循环

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const TOOLS: Anthropic.Tool[] = [{
  name: "get_weather",
  description: "查天气",
  input_schema: {
    type: "object",
    properties: { city: { type: "string" } },
    required: ["city"],
  },
}];

async function runAgent(query: string): Promise<string> {
  const messages: Anthropic.MessageParam[] = [{ role: "user", content: query }];
  for (let i = 0; i < 20; i++) {
    const msg = await client.messages.create({
      model: "claude-sonnet-5-...",
      max_tokens: 4096,
      tools: TOOLS,
      messages,
    });
    if (msg.stop_reason === "end_turn") {
      const text = msg.content.find((b): b is Anthropic.TextBlock => b.type === "text");
      return text?.text ?? "";
    }
    if (msg.stop_reason === "tool_use") {
      messages.push({ role: "assistant", content: msg.content });
      const results: Anthropic.ToolResultBlockParam[] = [];
      for (const block of msg.content) {
        if (block.type === "tool_use") {
          const result = await executeTool(block.name, block.input);
          results.push({
            type: "tool_result",
            tool_use_id: block.id,
            content: result,
          });
        }
      }
      messages.push({ role: "user", content: results });
    }
  }
  throw new Error("Max turns exceeded");
}
```

### 模式 3：Streaming

```typescript
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

详见 [流式响应](/claude-capabilities/api/streaming)。

### 模式 4：Structured Outputs

```typescript
const TOOL: Anthropic.Tool = {
  name: "extract_user",
  description: "提取用户信息",
  input_schema: {
    type: "object",
    properties: {
      name: { type: "string" },
      age: { type: "integer" },
      email: { type: "string" },
    },
    required: ["name", "email"],
  },
};

const msg = await client.messages.create({
  model: "claude-sonnet-5-...",
  max_tokens: 512,
  tools: [TOOL],
  tool_choice: { type: "tool", name: "extract_user" },
  messages: [{ role: "user", content: "用户：Bob，30 岁，bob@x.com" }],
});

const toolUse = msg.content.find((b): b is Anthropic.ToolUseBlock => b.type === "tool_use");
if (toolUse) {
  const user = toolUse.input as { name: string; age: number; email: string };
}
```

### 模式 5：Prompt Caching

```typescript
const SYSTEM: Anthropic.TextBlockParam[] = [
  {
    type: "text",
    text: "你是 TypeScript 审查员。",
    cache_control: { type: "ephemeral" },
  },
];

const msg = await client.messages.create({
  model: "claude-sonnet-5-...",
  max_tokens: 2048,
  system: SYSTEM,
  messages: [{ role: "user", content: "审查：const x = 1;" }],
});

console.log(`cache_read: ${msg.usage.cache_read_input_tokens}`);
```

## 三、3 个运行时

### Node.js

```bash
npm install @anthropic-ai/sdk
node --experimental-strip-types app.ts   # Node 22+ TS 直跑
# 或编译：tsc → node dist/
```

### Deno

```typescript
import Anthropic from "npm:@anthropic-ai/sdk";
const client = new Anthropic();
```

### 浏览器

```typescript
// ❌ 不推荐直连（API key 暴露）
// ✅ 走后端代理
const response = await fetch("/api/claude", {
  method: "POST",
  body: JSON.stringify({ model: "claude-sonnet-5-...", messages: [...] }),
});
```

**注意**：浏览器直连**会暴露 API key**——必须走后端代理或 Vite 代理。

## 四、错误处理

```typescript
import Anthropic from "@anthropic-ai/sdk";

try {
  await client.messages.create({...});
} catch (e) {
  if (e instanceof Anthropic.APIError) {
    if (e.status === 429) {
      // 退避重试
      await new Promise(r => setTimeout(r, 1000));
      await client.messages.create({...});
    } else if (e.status && e.status >= 500) {
      // 服务端错，重试
    } else {
      throw e;  // 4xx 不重试
    }
  }
}
```

## 五、5 个常见坑

**1. 浏览器直连暴露 API key**

```typescript
// ❌
const client = new Anthropic({ apiKey: "sk-ant-..." });  // 暴露给用户
// ✅ 走后端代理
```

**2. `max_tokens` 漏设**

```typescript
// ❌
client.messages.create({ model: "claude-sonnet-5-...", messages: [...] });  // 400
// ✅
client.messages.create({ model: "claude-sonnet-5-...", max_tokens: 1024, messages: [...] });
```

**3. TypeScript 类型推导失效**

```typescript
// 用 type guard
const text = msg.content.find((b): b is Anthropic.TextBlock => b.type === "text");
```

**4. Tool Use 循环无 MAX_TURNS**

必设循环上限——避免死循环。

**5. Streaming + structured outputs**

流式 JSON 不完整——用 `tool_use` 强制结构化，不用流式拼 JSON。

## 参考

- [Anthropic TypeScript SDK](https://github.com/anthropics/anthropic-sdk-typescript)（访问于 2026-08-07）
- [npm · @anthropic-ai/sdk](https://www.npmjs.com/package/@anthropic-ai/sdk)（访问于 2026-08-07）
- [Python SDK](/claude-capabilities/sdk/python-sdk)
- [Messages API](/claude-capabilities/api/messages)
- [Tool Use API](/claude-capabilities/api/tool-use)
- [SDK 概览](/claude-capabilities/sdk/overview)

## 下一步

- 多步 agent → [Agent SDK](/claude-capabilities/sdk/agent-sdk)
- 隔离 tool → [Tool Runner](/claude-capabilities/sdk/tool-runner)
- Claude Code 嵌入应用 → [Claude Code SDK](/claude-capabilities/sdk/claude-code-sdk)

## 如果你想

- examples/ 仓库骨架 → [SDK 概览](/claude-capabilities/sdk/overview#七examples-仓库骨架)
- 切到 Python 对照 → [Python SDK](/claude-capabilities/sdk/python-sdk)
