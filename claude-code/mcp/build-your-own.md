---
title: 写你自己的 MCP Server
description: '从零写一个 MCP server 并接入 Claude Code——Python / TypeScript 双路径最小骨架、本地调试、Inspector 验证'
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-03
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  buildServerDocs: 'https://modelcontextprotocol.io/docs/develop/build-server'
  mcpDocs: 'https://code.claude.com/docs/en/mcp'
  accessedAt: 2026-08-03
---

# 写你自己的 MCP Server

> **目标**：本篇结束后，你有一个能跑的 MCP server（Python 或 TypeScript）——暴露至少一个自定义 tool，Claude Code 里能调用。全程约 15 分钟。

## 你将做到

- ✅ 用 MCP SDK 写一个最小 server（暴露一个 tool）
- ✅ 用 stdio transport 接入 Claude Code
- ✅ 用 MCP Inspector 独立测试 server
- ✅ 知道 stdio vs HTTP server 的开发差异
- ✅ 理解发布到 plugin / marketplace / directory 的路径

## 前置

- 读过 [什么是 MCP](./what-is-mcp) 和 [传输：stdio / HTTP / SSE](./transports)
- Python 3.10+ 或 Node.js 20+
- Claude Code v2.1.220

## 一、两种起步方式

| 方式 | 适合 | 命令 |
| --- | --- | --- |
| **手动 SDK** | 精细控制、理解原理 | 本文主路径 |
| **脚手架 plugin** | 快速原型、交互式引导 | `/plugin install mcp-server-dev@claude-plugins-official` → `/mcp-server-dev:build-mcp-server` |

脚手架会问你几个问题后自动生成代码——适合「先跑通再看」。**本文走手动路径**，理解骨架后再用脚手架不迟。

## 二、Python 路径（推荐）

### 初始化项目

```bash
uv init my-server && cd my-server
uv venv && source .venv/bin/activate
uv add "mcp[cli]"
```

### 写最小 server

新建 `server.py`：

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone. Use when the user asks to greet."""
    return f"Hello, {name}! 👋"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**关键点**：

- `@mcp.tool()` 装饰器把函数注册为 MCP tool
- 函数 **docstring 第一行** = tool 的 description（Claude 看这个决定用不用）
- 类型注解 → 自动生成 `input_schema`（JSON Schema）
- `transport="stdio"` → 走 stdin/stdout 通信

### 接入 Claude Code

```bash
claude mcp add --transport stdio my-server -- uv run server.py
```

重启 Claude Code（或 `/mcp` 看状态），然后试：

```text
跟 Alice 打个招呼
```

Claude 应调用 `my-server__hello(name="Alice")` 并返回结果。

## 三、TypeScript 路径

### 初始化项目

```bash
mkdir my-server && cd my-server
npm init -y
npm install @modelcontextprotocol/sdk
```

### 写最小 server

新建 `index.ts`：

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

server.tool("hello", "Say hello to someone", {
  name: { type: "string", description: "Person to greet" },
}, async ({ name }) => ({
  content: [{ type: "text", text: `Hello, ${name}! 👋` }],
}));

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 接入 Claude Code

```bash
claude mcp add --transport stdio my-server -- npx tsx index.ts
```

## 四、调试与测试

### MCP Inspector（独立测试，不依赖 Claude Code）

```bash
npx @modelcontextprotocol/inspector uv run server.py
```

Inspector 打开浏览器 UI——能看到暴露的 tools / resources / prompts，手动发请求测返回。

### Claude Code 内调试

```bash
claude --debug
```

`--debug` 模式下看到 MCP tool call 的完整 JSON 请求/响应、连接错误细节。

### 常见调试手段

- `/mcp` 面板看连接状态、tool 数量
- `claude mcp get <name>` 看单个 server 详情
- **Python stdio server**：**不能用 `print()`**——stdout 是 JSON-RPC 通道，print 会破坏协议。用 `logging` 模块写 stderr

## 五、stdio vs HTTP server 差异

| | stdio | HTTP（远程） |
| --- | --- | --- |
| 部署 | 跑在用户本地 | 部署到云端 |
| 鉴权 | 环境变量 | OAuth / Bearer / API Key |
| logging | **只能写 stderr** | stdout 可用 |
| 适合 | 本地工具、个人自动化 | SaaS 产品对外暴露 |
| SDK 差异 | `StdioServerTransport` | `StreamableHTTPServerTransport` |

HTTP server 开发详情见 [MCP 官方文档 · Build server](https://modelcontextprotocol.io/docs/develop/build-server) —— 本文聚焦使用层，不深入远程部署。

## 六、从本地到分发

| 阶段 | 做什么 |
| --- | --- |
| **本地验证** | `claude mcp add --transport stdio` 接入测通 |
| **项目共享** | 写 `.mcp.json` 提交到仓库 → 同事 clone 后自动接入 |
| **Plugin 打包** | 把 server 作为 plugin 的 `.mcp.json` 分发 → 见 [Plugins 与 Marketplace](../skills/plugins-marketplace) |
| **Directory 提交** | 远程 HTTP server → 提交到 [Anthropic Directory](https://claude.ai/directory) |
| **Community** | 投稿到 `claude-community` marketplace |

## 常见坑

**Python server 里用了 `print()`**——stdout 是 JSON-RPC 通道，任何 `print()` 都会破坏协议、导致 Claude Code 报连接错误。改用 `logging.getLogger(__name__).info()`。

**Tool description 写得太泛**——Claude 看 description 决定用不用这个 tool。写清楚「何时用」+ 「输入是什么」。和 [写好触发描述](../skills/writing-triggers) 同理。

**忘了类型注解**——MCP SDK 用类型注解生成 `input_schema`；没写的话 tool 参数在 Claude 眼里是 `any`，容易传错类型。

**`uv run` 环境问题**——`claude mcp add` 的 command 在 Claude Code 的 shell 里跑，不是你当前 terminal。确保 `uv` / `npx` 在 PATH 里、或用绝对路径。

## 参考

- [MCP · Build a server](https://modelcontextprotocol.io/docs/develop/build-server)（访问于 2026-08-03）—— Python & TypeScript 完整教程
- [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector)（访问于 2026-08-03）—— 独立测试工具
- [Anthropic · Claude Code MCP 参考](https://code.claude.com/docs/en/mcp)（访问于 2026-08-03）

## 下一步

- 鉴权（OAuth / token）与远程调试 → [鉴权与调试](./auth-and-debug) 🚧
- 把 server 配置共享给团队 → [.mcp.json 项目配置](./mcp-json-config) 🚧
- 打包成 plugin 分发 → [Plugins 与 Marketplace](../skills/plugins-marketplace)

## 如果你想

- 看协议层细节（JSON-RPC / capability negotiation） → [Claude 能力 · MCP 协议层](/claude-capabilities/mcp-protocol/protocol-spec) 🚧
- 回顾已有 server 不用自己写 → [官方常用 Server](./official-servers)
- 理解 tool search 对自定义 tool 的影响 → [什么是 MCP · Tool Search](./what-is-mcp#四、在-claude-code-里的使用流程)
