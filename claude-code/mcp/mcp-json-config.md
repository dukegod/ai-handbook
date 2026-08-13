---
title: .mcp.json 项目配置
description: '项目根目录 .mcp.json 的完整格式——mcpServers 各字段、scope 区分、批准机制、与 plugin 和 settings.json 的关系'
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

# .mcp.json 项目配置

> **TL;DR**：`.mcp.json` 放在项目根目录，**提交到仓库**——团队成员 clone 后 Claude Code 自动发现里面的 MCP server 并提示批准。格式是 `{ "mcpServers": { "<name>": { ... } } }`，支持 stdio / HTTP / SSE / WebSocket 四种 transport。用户级配置在 `~/.claude.json` 的同结构字段里。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- `.mcp.json` 完整 schema（`mcpServers` 各字段）
- 项目级 vs 用户级 vs plugin 级三种来源
- 批准机制：为什么 clone 后 server 不自动连接
- 常用配置模式：多 server / 动态 header / 条件启用

## 前置

- 读过 [传输：stdio / HTTP / SSE](./transports) 和 [鉴权与调试](./auth-and-debug)
- 有至少一个 MCP server 已手动接入成功

## 一、文件位置与 scope

| 位置 | 作用域 | 提交到仓库 |
| --- | --- | --- |
| **`.mcp.json`**（项目根） | 本项目所有人 | ✅ |
| **`~/.claude.json`** | 你所有项目 | ❌ |
| **plugin `.mcp.json`** | plugin 启用时 | 跟 plugin 走 |

**合并规则**：三处定义的 server **全部加载**（不覆盖）。同名 server 按优先级：用户级 > 项目级 > plugin 级。

## 二、完整 schema

```json
{
  "mcpServers": {
    "server-name": {
      // ---- 通用字段 ----
      "type": "http",           // "http" | "sse" | "ws"（省略默认 stdio）
      "alwaysLoad": false,      // true = 跳过 tool search 直接加载所有 tool

      // ---- stdio 专用 ----
      "command": "node",        // 启动命令
      "args": ["server.js"],    // 命令参数
      "env": { "KEY": "val" },  // 注入环境变量
      "cwd": "./servers/",      // 工作目录（相对项目根）

      // ---- HTTP / SSE / WebSocket 专用 ----
      "url": "https://...",     // 端点 URL
      "headers": { "Auth": "Bearer xxx" },  // 静态 header
      "headersHelper": "cmd",   // 动态 header 命令
      "allowedEnvVars": ["TOKEN"],  // headersHelper 可用的环境变量
      "timeout": 30             // 连接超时秒数
    }
  }
}
```

### 字段速查

| 字段 | 类型 | Transport | 说明 |
| --- | --- | --- | --- |
| `type` | string | all | 省略 = stdio；有 `url` 必须显式写 |
| `command` | string | stdio | 启动命令 |
| `args` | string[] | stdio | 命令参数 |
| `env` | object | stdio | 环境变量 |
| `cwd` | string | stdio | 工作目录 |
| `url` | string | http/sse/ws | 端点地址 |
| `headers` | object | http/sse/ws | 静态请求头 |
| `headersHelper` | string | http/sse/ws | 动态 header 生成命令 |
| `timeout` | number | all | 连接超时（秒） |
| `alwaysLoad` | boolean | all | 跳过 tool search 直接加载 |

## 三、批准机制

项目级 `.mcp.json` 里的 server **不会自动连接**——防止恶意仓库注入 server。用户必须显式批准：

1. 首次 `claude` 启动时看到 `⏸ Pending approval` 提示
2. 选择 approve / reject
3. 批准记录存在 `~/.claude.json` 或 `.claude/settings.local.json`

**快捷批准所有项目 server**——在 `.claude/settings.json`（或用户 settings）加：

```json
{
  "enableAllProjectMcpServers": true
}
```

**⚠️ 安全**：只在信任的仓库开启。`enableAllProjectMcpServers` 在未信任的工作目录下被忽略。

## 四、常用配置模式

### 多 server 并列

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://mcp.github.com/sse"
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    },
    "internal-api": {
      "type": "http",
      "url": "https://internal.example.com/mcp",
      "headersHelper": "node scripts/get-token.js"
    }
  }
}
```

### 密钥不入库——引用环境变量

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_KEY": "$MY_API_KEY"
      }
    }
  }
}
```

`$MY_API_KEY` 在 Claude Code 启动时从 shell 环境读取。团队成员各自在 `.env` 或 shell profile 里设置。

### 空 URL 占位（plugin 预留）

```json
{
  "mcpServers": {
    "custom-api": {
      "type": "http",
      "url": ""
    }
  }
}
```

`url` 为空 → Claude Code 不连接、不报错，标为 `not configured`。用户后续设 URL 即可激活。

## 五、与 `claude mcp add` 的关系

`claude mcp add` 做的事 = 往 `~/.claude.json`（用户级）或 `.mcp.json`（`--scope project`）里写一条 server 配置。手动编辑 `.mcp.json` 等效。

```bash
# 等价于手动在 .mcp.json 里加一条
claude mcp add --transport http --scope project notion https://mcp.notion.com/mcp
```

加 `--scope project` 写到 `.mcp.json`；不加默认写到 `~/.claude.json`（用户级）。

## 六、与 settings.json 的关系

| 文件 | 管什么 |
| --- | --- |
| `.mcp.json` | MCP server 定义（command / url / env） |
| `.claude/settings.json` | MCP server 的批准（`enabledMcpjsonServers` / `disabledMcpjsonServers`）、plugin 启用 |

**不要在 `settings.json` 里定义 server**——那是 `.mcp.json` 的职责。`settings.json` 只管批准/禁用。

## 常见坑

**有 `url` 没写 `type`**——Claude Code 当 stdio 解析，报 `command: expected string`。**只要有 `url` 就必须写 `type`**。

**把密钥硬编码到 `.mcp.json` 并提交**——所有有 clone 权限的人看得到。用 `$VAR` 引用或 `headersHelper`。

**`enableAllProjectMcpServers` 放在项目 `.claude/settings.json` 里想自动批准**——在未信任的 workspace 下被忽略（防恶意仓库）。要生效需要用户先信任目录。

**server name 用了保留名**——`workspace` / `claude-in-chrome` / `computer-use` / `Claude Preview` / `Claude Browser` 是内置 server 名，用了会被跳过。

## 参考

- [Anthropic · Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)（访问于 2026-08-03）
- [Anthropic · Settings reference](https://code.claude.com/docs/en/settings)（访问于 2026-08-03）—— `enabledMcpjsonServers` 等字段

## 下一步

- 把 MCP 配置打包到 plugin → [Plugins 与 Marketplace](../skills/plugins-marketplace)
- 看有哪些现成 server → [官方常用 Server](./official-servers)
- 自己写 server → [写你自己的 MCP Server](./build-your-own)

## 如果你想

- 深入鉴权方式 → [鉴权与调试](./auth-and-debug)
- 看 settings.json 完整结构 → [Settings 配置文件](../customization/settings) 🚧
- 回顾 MCP 概念 → [什么是 MCP](./what-is-mcp)
