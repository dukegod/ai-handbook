---
title: MCP 协议规范
description: API/SDK 视角的 MCP 协议层——JSON-RPC 2.0 + stdio/HTTP transport + 4 类 primitive（tools / resources / prompts / notifications）
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  protocolSpec: 'https://modelcontextprotocol.io/specification/2025-06-18'
  protocolSite: 'https://modelcontextprotocol.io/introduction'
  accessedAt: 2026-08-07
---

# MCP 协议规范

> **TL;DR**：MCP（Model Context Protocol）是 Anthropic 主导的**开源协议**——基于 JSON-RPC 2.0 + stdio / HTTP transport。本页是**协议层规范**（消息结构 / 握手 / primitive），与 [v0.2 mcp/*](/claude-code/mcp/what-is-mcp) **使用层**分工：那里讲 Claude Code 怎么接 MCP server，这里讲协议本身怎么实现。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- MCP 协议层 vs 使用层分工
- 协议核心（JSON-RPC 2.0 / 4 类 primitive / 2 种 transport）
- 握手协议（initialize / initialized / capabilities）
- 消息结构（request / response / notification / error）
- 协议版本（2025-06-18）
- 与 [MCP 使用层](/claude-code/mcp/what-is-mcp) / [MCP Cookbook](/cookbook/build-first-mcp-server) 的关系

## 一、协议层 vs 使用层

```
┌─────────────────────────────────────────┐
│ 使用层：Claude Code 怎么接 MCP server    │  ← v0.2 mcp/*
├─────────────────────────────────────────┤
│ 协议层：消息结构 / 握手 / primitive       │  ← 本章
├─────────────────────────────────────────┤
│ 原语层：tool_use / tool_result           │  ← v0.3.1 core/tool-use
└─────────────────────────────────────────┘
```

**协议层** = 标准化消息格式（实现 MCP server / client 必读）
**使用层** = 在 Claude Code 里 `claude mcp add` 的工作流
**原语层** = 协议层下面用的 tool_use block

详见 [Claude Code · 什么是 MCP](/claude-code/mcp/what-is-mcp) + [v0.3.1 Tool Use 协议](/claude-capabilities/core/tool-use)。

## 二、协议核心

MCP 协议 = **JSON-RPC 2.0** 消息 + **2 种 transport** + **4 类 primitive**。

### 1. JSON-RPC 2.0

所有 MCP 消息都是 JSON-RPC 2.0 格式：

```json
// Request
{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}

// Response
{"jsonrpc": "2.0", "id": 1, "result": {"tools": [...]}}

// Notification（无 id）
{"jsonrpc": "2.0", "method": "notifications/initialized"}

// Error
{"jsonrpc": "2.0", "id": 1, "error": {"code": -32601, "message": "Method not found"}}
```

### 2. 2 种 transport

| Transport | 适用 | 特点 |
| --- | --- | --- |
| **stdio** | 本地进程（Claude Code 主流） | 通过 stdin/stdout 通信，零网络 |
| **HTTP** + SSE | 远程服务 | Server-Sent Events 流式推送 |

详见 [MCP 传输方式选型](/claude-code/mcp/transports)。

### 3. 4 类 primitive

MCP server 可暴露 4 种能力：

| Primitive | 含义 | Claude 端调用 |
| --- | --- | --- |
| **tools** | 可调用的函数 | `client.messages.create(tools=[...])` |
| **resources** | 可读取的数据（文件、URL） | `client.read_resource(uri)` |
| **prompts** | 预定义 prompt 模板 | `client.get_prompt(name, args)` |
| **notifications** | server 主动推送 | server 调 `notifications/...` |

## 三、握手协议

```
1. Client → Server: initialize
   {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
     "protocolVersion": "2025-06-18",
     "capabilities": {},
     "clientInfo": {"name": "claude-code", "version": "2.1.220"}
   }}

2. Server → Client: initialize result
   {"jsonrpc": "2.0", "id": 1, "result": {
     "protocolVersion": "2025-06-18",
     "capabilities": {"tools": {}, "resources": {}},
     "serverInfo": {"name": "glossary", "version": "0.1.0"}
   }}

3. Client → Server: notifications/initialized
   {"jsonrpc": "2.0", "method": "notifications/initialized"}

4. 正常通信（tools/list, tools/call, ...）
```

详见 [MCP 协议握手详解](/claude-capabilities/mcp-protocol/protocol-spec#三握手协议)。

## 四、4 类消息

### 1. Request（请求）

```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}
```

- 有 `id`（数字 / 字符串）
- 有 `method`（如 `tools/list`）
- 有 `params`（对象，可选）

### 2. Response（响应）

```json
{"jsonrpc": "2.0", "id": 1, "result": {...}}
```

- `id` 与对应 request 相同
- `result` 是返回值，**或** `error`

### 3. Notification（通知）

```json
{"jsonrpc": "2.0", "method": "notifications/initialized"}
```

- **无 `id`**——server 不会回包
- 常用：initialized 通知、心跳、resource 变化推送

### 4. Error

```json
{"jsonrpc": "2.0", "id": 1, "error": {"code": -32601, "message": "Method not found"}}
```

**标准错误码**：

| Code | 含义 |
| --- | --- |
| -32700 | Parse error（JSON 错） |
| -32600 | Invalid Request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |
| -32000 ~ -32099 | Server-defined（应用自定义） |

## 五、4 个工具方法（tools/*）

```
tools/list
  ↓ server 返回工具列表
  {"tools": [{"name": "...", "description": "...", "inputSchema": {...}}]}

tools/call
  ↓ client 调工具
  {"name": "read_file", "arguments": {"path": "/..."}}
  ↓ server 返回结果
  {"content": [{"type": "text", "text": "..."}], "isError": false}
```

## 六、协议版本

**当前**：`2025-06-18`（MCP 协议 spec 2025-06-18 版本）

**版本协商**：
- client 发送支持的 `protocolVersion`
- server 回 `protocolVersion`（可能是其支持的最旧或最新）
- 不匹配 → client 决定降级 / 报错

详见 [MCP Spec · 版本协商](https://modelcontextprotocol.io/specification/2025-06-18)。

## 七、4 个常见坑

**1. 忘发 `notifications/initialized`**

```python
# ❌ initialize 后直接调 tools/list
client.send("initialize", ...)
client.send("tools/list", ...)    # server 不响应

# ✅ initialize + notifications/initialized + 等响应
client.send("initialize", ...)
client.send_notification("notifications/initialized")
client.send("tools/list", ...)
```

**2. 错误码不标准**

```python
# ❌ 用 500 / 404 等 HTTP 风格错误码
{"code": 500, "message": "..."}

# ✅ JSON-RPC 2.0 标准错误码
{"code": -32603, "message": "Internal error"}
```

**3. tool input 不用 JSON Schema**

```python
# ❌ 自然语言描述
{"name": "search", "parameters": "a query string"}

# ✅ JSON Schema
{"name": "search", "inputSchema": {"type": "object", "properties": {"q": {"type": "string"}}}}
```

**4. 协议版本不一致**

```python
# client 发 "2025-06-18"，server 只支持 "2025-03-26"
# → 失败
# ✅ 协商：client 支持多版本，从最新到最旧重试
```

## 参考

- [MCP Spec · 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18)（访问于 2026-08-07）
- [MCP Introduction](https://modelcontextprotocol.io/introduction)
- [Claude Code · 什么是 MCP](/claude-code/mcp/what-is-mcp)
- [Claude Code · MCP 传输方式](/claude-code/mcp/transports)
- [Cookbook · 写你的第一个 MCP Server](/cookbook/build-first-mcp-server)
- [v0.3.1 Tool Use 协议](/claude-capabilities/core/tool-use)
- [v0.2 examples/glossary-mcp-server](/examples/glossary-mcp-server/README)

## 下一步

- 实现 Server → [Server 作者指南](/claude-capabilities/mcp-protocol/server-authoring)
- 实现 Client → [Client 实现要点](/claude-capabilities/mcp-protocol/client-implementation)
- 实战 → [Cookbook · 写你的第一个 MCP Server](/cookbook/build-first-mcp-server)

## 如果你想

- 切到 MCP 使用层 → [Claude Code · MCP 使用层](/claude-code/mcp/what-is-mcp)
- 切到 tool_use 原语 → [Tool Use 协议](/claude-capabilities/core/tool-use)
- 实战示例仓库 → [examples/glossary-mcp-server](/examples/glossary-mcp-server/README)
