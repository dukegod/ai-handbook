---
title: 鉴权与调试
description: 'MCP server 的三种鉴权方式（OAuth / Bearer / env）与 Claude Code 里的调试手段——/mcp 面板、--debug、Inspector、常见连接失败排查'
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

# 鉴权与调试

> **TL;DR**：MCP server 鉴权三条路：**OAuth**（远程 HTTP server 推荐，Claude Code 自动弹浏览器授权）/ **静态 Header**（Bearer token / API key）/ **环境变量**（stdio server 密钥注入）。调试靠四件套：`/mcp` 面板看连接状态、`claude --debug` 看 JSON-RPC 细节、MCP Inspector 独立测、`claude mcp get <name>` 查单个 server。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- 三种鉴权方式各自的适用场景与配置方法
- `headersHelper`：动态生成 token 的命令
- 调试四件套：`/mcp` / `--debug` / Inspector / `mcp get`
- 常见连接失败 6 种原因与修复

## 前置

- 读过 [传输：stdio / HTTP / SSE](./transports) —— 知道自己的 server 用哪种 transport
- 有一个已接入但可能有问题的 MCP server

## 一、鉴权方式一览

| 方式 | Transport | 配置 | 适合 |
| --- | --- | --- | --- |
| **OAuth** | HTTP | Claude Code 自动弹浏览器 | SaaS 服务（Notion / Figma / GitHub） |
| **静态 Header** | HTTP / SSE / WebSocket | `--header` 或 `.mcp.json` `headers` | 有固定 API key 的服务 |
| **环境变量** | stdio | `--env` 或 `.mcp.json` `env` | 本地进程需要密钥 |
| **headersHelper** | HTTP / SSE / WebSocket | 动态命令生成 header | token 有过期时间 |

## 二、OAuth（远程 HTTP server）

大多数官方 plugin（GitHub、Notion、Figma、Slack……）用 OAuth。**你什么都不用配**——首次调用时 Claude Code 自动：

1. 弹出浏览器授权页
2. 你点击授权
3. token 自动存储、后续静默使用

**`/mcp` 面板状态**：未授权时显示 `! Needs authentication`，点击后走 OAuth 流程。

**⚠️ 注意**：OAuth 只支持 **HTTP** transport（不支持 SSE / WebSocket / stdio）。

## 三、静态 Header

**CLI 方式**：

```bash
claude mcp add --transport http my-api https://api.example.com/mcp \
  --header "Authorization: Bearer sk-xxx" \
  --header "X-Custom: value"
```

**`.mcp.json` 方式**：

```json
{
  "mcpServers": {
    "my-api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer sk-xxx",
        "X-Custom": "value"
      }
    }
  }
}
```

**⚠️ 安全**：`.mcp.json` 会提交到仓库——**不要把真实 token 写进去**。用 `headersHelper` 或环境变量引用。

## 四、环境变量（stdio server）

**CLI 方式**：

```bash
claude mcp add --env API_KEY=xxx --env DB_URL=postgres://... \
  --transport stdio my-server -- node server.js
```

**`.mcp.json` 方式**：

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_KEY": "xxx",
        "DB_URL": "postgres://..."
      }
    }
  }
}
```

server 进程启动时自动拿到这些环境变量。同样注意不要把密钥提交到仓库——用 `.env` 文件 + `.gitignore`，在 `env` 里引用 `$API_KEY`。

## 五、headersHelper——动态 token

当 token 有过期时间（如 15 分钟一换），用 `headersHelper` 字段指定一个**命令**——每次连接前 Claude Code 跑这个命令，stdout 作为 header 值：

```json
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://internal.example.com/mcp",
      "headersHelper": "node scripts/get-token.js"
    }
  }
}
```

`get-token.js` stdout 输出 JSON：

```json
{
  "Authorization": "Bearer eyJhbG..."
}
```

**环境变量插值**：`headers` 字段支持 `$VAR` 语法，`headersHelper` 的 `allowedEnvVars` 控制哪些变量可用。

## 六、调试四件套

### 1. `/mcp` 面板

Claude Code 内敲 `/mcp` 看所有 server：

- ✔ Connected（正常）
- ! Needs authentication（未授权）
- ✘ Failed to connect（连接失败）
- ⏸ Pending approval（等你批准）
- 每个 server 旁显示 **tool 数量**

### 2. `claude --debug`

启动时加 `--debug`，看完整 MCP 通信日志：

- JSON-RPC 请求/响应
- 连接错误详情
- tool call 参数与结果
- 超时信息

### 3. MCP Inspector（独立于 Claude Code）

```bash
npx @modelcontextprotocol/inspector <启动命令>
```

在浏览器 UI 里：
- 看暴露的 tools / resources / prompts 清单
- 手动发请求、检查返回值
- 不依赖 Claude Code，纯粹测 server 本身

### 4. `claude mcp get <name>`

单个 server 详情——连接状态、配置来源、tool 列表、错误信息。

## 七、常见连接失败

| 现象 | 原因 | 修复 |
| --- | --- | --- |
| `command: expected string, received undefined` | `.mcp.json` 里有 `url` 但没写 `type` | 加 `"type": "http"` |
| `! Needs authentication` | OAuth 未完成 | 点击走 OAuth 流程或用 `--header` |
| `✘ Failed to connect` + timeout | server 没启动或端口错 | 确认 server 进程在跑、URL 可达 |
| `Executable not found in $PATH` | stdio server 的 command 不在 PATH | 用绝对路径或确认环境 |
| `⏸ Pending approval` | 项目级 `.mcp.json` 的 server 未批准 | 跑 `claude` 交互式批准 |
| Tool 数量显示 0 | server 启动了但 tool 注册失败 | 用 Inspector 看 server 有无报错 |

**通用排查步骤**：

1. `claude mcp get <name>` 看状态
2. `claude --debug` 看连接日志
3. 用 Inspector 确认 server 本身没问题
4. 检查 `.mcp.json` 格式（特别是 `type` 字段）

## 参考

- [Anthropic · Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)（访问于 2026-08-03）
- [MCP · Inspector](https://modelcontextprotocol.io/docs/tools/inspector)（访问于 2026-08-03）

## 下一步

- 把 MCP 配置共享给团队 → [.mcp.json 项目配置](./mcp-json-config) 🚧
- 回顾有哪些现成 server → [官方常用 Server](./official-servers)
- 打包到 plugin 分发 → [Plugins 与 Marketplace](../skills/plugins-marketplace)

## 如果你想

- 自己写 server → [写你自己的 MCP Server](./build-your-own)
- 看权限系统全貌 → [权限系统](../basics/permissions)
- 深入 Transport 选型 → [传输：stdio / HTTP / SSE](./transports)
