---
title: '传输：stdio / HTTP / SSE / WebSocket'
description: MCP 四种 Transport 的选型决策——本地进程走 stdio、远程服务走 HTTP、需要推送走 WebSocket，附 claude mcp add 完整用法
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-03
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  mcpDocs: 'https://code.claude.com/docs/en/mcp'
  accessedAt: 2026-08-03
---

# 传输：stdio / HTTP / SSE / WebSocket

> **TL;DR**：MCP 有四种 Transport（连接方式）。**本地工具用 stdio**（进程级通信）、**远程服务用 HTTP**（Anthropic 推荐默认）、需要服务端主动推事件用 **WebSocket**。SSE 已 deprecated，只在老 server 兼容时用。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- 四种 Transport 一表对比（通信方向 / 部署位置 / 鉴权 / 推荐度）
- 每种怎么用 `claude mcp add` 接入
- `.mcp.json` 里对应的 JSON 配置写法
- 选型三问决策树

## 前置

- 读过 [什么是 MCP](./what-is-mcp) —— 知道 Host / Client / Server 三层
- Claude Code v2.1.220

## 一、四种 Transport 对比

| Transport | 通信 | 部署 | 鉴权 | 推送 | 推荐度 |
| --- | --- | --- | --- | --- | --- |
| **stdio** | stdin/stdout | 本地进程 | 环境变量 | ❌ | ✅ 本地首选 |
| **HTTP** | HTTP 请求/响应（Streamable HTTP） | 远程 | OAuth / Bearer / Header | ❌ | ✅ 远程首选 |
| **SSE** | HTTP + Server-Sent Events | 远程 | Header | ❌ | ⚠️ deprecated |
| **WebSocket** | 双向持久连接 | 远程 | Header | ✅ | 需要推送时 |

## 二、stdio——本地进程

**适用**：server 是你机器上的一个进程（Node.js / Python / Go 编译二进制）。

**怎么加**：

```bash
claude mcp add --transport stdio <name> -- <command> [args...]
```

`--` 分隔 Claude Code 选项和 server 命令。`--` 之后的一切原样传给 server。

**示例**——接 Airtable server：

```bash
claude mcp add --env AIRTABLE_API_KEY=xxx --transport stdio airtable \
  -- npx -y airtable-mcp-server
```

**`.mcp.json` 写法**：

```json
{
  "mcpServers": {
    "airtable": {
      "command": "npx",
      "args": ["-y", "airtable-mcp-server"],
      "env": { "AIRTABLE_API_KEY": "xxx" }
    }
  }
}
```

没有 `type` 字段时默认 stdio。

**特点**：

- 进程随 Claude Code 启动 / 关闭
- 通过 `env` 注入密钥，不走网络
- server 进程能访问本地文件系统
- `CLAUDE_PROJECT_DIR` 自动设置在 server 环境中

## 三、HTTP——远程服务（推荐）

**适用**：server 部署在云端、SaaS 服务暴露 MCP 端点。

**怎么加**：

```bash
claude mcp add --transport http <name> <url>
```

**示例**——接 Notion：

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

带 Bearer token：

```bash
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

**`.mcp.json` 写法**：

```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    },
    "secure-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": { "Authorization": "Bearer your-token" }
    }
  }
}
```

**⚠️ 常见坑**：有 `url` 但没写 `type` → Claude Code 当 stdio 解析 → 报错 `command: expected string, received undefined`。**只要有 `url` 就必须带 `type`**。

**MCP spec 别名**：`"type": "streamable-http"` 等价于 `"http"`——从 server 文档里复制配置时无需改。

**特点**：

- 支持 OAuth 流（Claude Code 自动弹浏览器授权）
- 支持 `--header` 传静态 token
- 支持 `headersHelper`（动态生成 header 的命令）
- 无推送能力

## 四、SSE（deprecated）

**适用**：老 server 只有 SSE 端点时兼容使用。**新项目应选 HTTP**。

```bash
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

**`.mcp.json` 写法**：

```json
{
  "mcpServers": {
    "asana": {
      "type": "sse",
      "url": "https://mcp.asana.com/sse"
    }
  }
}
```

与 HTTP 的唯一技术差异：SSE 维持**单向**长连接，server 通过 event stream 返回数据。HTTP（Streamable HTTP）在每次请求维度独立，更符合 REST 心智。

## 五、WebSocket——推送场景

**适用**：server 需要主动向 Claude 推消息（如 Telegram bot、Discord 监听、webhook 实时转发）。

**⚠️ 不支持 `claude mcp add --transport ws`**——只能通过 JSON 配置：

```bash
claude mcp add-json events-server \
  '{"type":"ws","url":"wss://mcp.example.com/socket","headers":{"Authorization":"Bearer TOKEN"}}'
```

或在 `.mcp.json` 里：

```json
{
  "mcpServers": {
    "events-server": {
      "type": "ws",
      "url": "wss://mcp.example.com/socket",
      "headers": { "Authorization": "Bearer TOKEN" }
    }
  }
}
```

**特点**：

- 双向持久连接，server 可 push 到 Claude session
- 只能 header 鉴权，不支持 OAuth
- 不出现在 `claude mcp list` 输出中——用 `/mcp` 面板或 `claude mcp get <name>` 查看

## 六、选型三问

**问 1：server 跑在哪？**

- **本地进程** → stdio
- **远程/云端** → 问 2

**问 2：需要 server 主动推消息吗？**

- **不需要**（大多数） → HTTP
- **需要**（实时监听事件） → WebSocket

**问 3：远程 server 只有 SSE 端点？**

- **是** → SSE（兼容）
- **否** → HTTP

```text
本地？ ──yes──→ stdio
  │no
  ▼
需推送？ ──yes──→ WebSocket
  │no
  ▼
只有 SSE？ ──yes──→ SSE
  │no
  ▼
HTTP ✅
```

## 七、管理已接入的 Server

```bash
claude mcp list              # 列出所有 server + 连接状态
claude mcp get <name>        # 单个 server 详情
claude mcp remove <name>     # 移除
```

在 Claude Code 内敲 `/mcp` 打开交互面板——看连接状态、tool 数量、启用/禁用。

## 常见坑

**有 `url` 没写 `type`**——Claude Code 默认 stdio，报 `command: expected string`。只要配了 `url` 就必须显式写 `"type": "http"` / `"sse"` / `"ws"`。

**stdio server 的 `--` 忘了加**——Claude Code 把 server 参数当自己的 flag 解析。`--` 之后才是 server 命令。

**`--env` 紧跟 server name**——CLI 把 name 当作 env pair 报错。在 `--env` 和 name 之间加其它选项（如 `--transport stdio`）。

**WebSocket server 在 `claude mcp list` 里看不到**——用 `/mcp` 面板或 `claude mcp get <name>` 看。

## 参考

- [Anthropic · MCP — Installing MCP servers](https://code.claude.com/docs/en/mcp)（访问于 2026-08-03）
- [MCP spec · Transports](https://modelcontextprotocol.io/docs/concepts/transports)（访问于 2026-08-03）

## 下一步

- 看有哪些现成 server 可以直接装 → [官方常用 Server](./official-servers) 🚧
- 想自己写 server → [写你自己的 MCP Server](./build-your-own) 🚧
- 配置细节 → [.mcp.json 项目配置](./mcp-json-config) 🚧

## 如果你想

- 深入 OAuth 与动态 header → [鉴权与调试](./auth-and-debug) 🚧
- 理解 Transport 协议层细节 → [Claude 能力 · MCP 协议层](/claude-capabilities/mcp-protocol/protocol-spec) 🚧
- 回顾 MCP 整体概念 → [什么是 MCP](./what-is-mcp)
