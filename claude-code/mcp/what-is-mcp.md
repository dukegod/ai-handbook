---
title: 什么是 MCP
description: Model Context Protocol 的心智模型——Claude Code 如何通过 MCP 连接外部工具、数据库与 API，架构三层（host/client/server）与本章使用层定位
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-03
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  mcpDocs: 'https://code.claude.com/docs/en/mcp'
  protocolSite: 'https://modelcontextprotocol.io/introduction'
  accessedAt: 2026-08-03
---

# 什么是 MCP

> **TL;DR**：MCP（Model Context Protocol）是 Anthropic 主导的**开源协议标准**——定义 AI host（如 Claude Code）如何连接外部工具和数据源。你接一个 MCP server，Claude 就多了一组工具可调用（读 JIRA、查 Postgres、操作 Figma……）。类比：MCP 之于 Claude Code ≈ USB 之于电脑——标准化接口，按需插拔。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- MCP 解决什么问题（为什么内置工具不够）
- 架构三层：Host / Client / Server
- 一个 MCP server 能提供什么：tools / resources / prompts / channels
- Claude Code 里 MCP 的使用流程（发现 → 连接 → 授权 → 调用）
- 本章「使用层」vs 能力全景章「协议层」的定位区分
- 安全模型：每个 MCP 工具都走权限系统

## 前置

- 读过 [权限系统](../basics/permissions) —— MCP 工具同样走权限审批
- 读过 [工具总览](../tools/overview) —— 知道 Claude Code 有哪些内置工具

## 一、MCP 解决什么问题

Claude Code 的内置工具（Read / Edit / Bash / Grep / WebFetch …）覆盖了**本地文件系统 + shell + 网页**。但你的工作流远不止这些：

| 你经常在做的 | 内置工具能做？ | MCP 接上后 |
| --- | --- | --- |
| 去 JIRA 拿 ticket 详情 | ❌ 得手动贴 | Claude 直接读 JIRA |
| 查线上 Postgres 表 | ❌ 要你写 SQL 贴回来 | Claude 自己跑 SQL |
| 看 Sentry 错误堆栈 | ❌ | Claude 拿堆栈直接定位 |
| 操作 Figma 设计稿 | ❌ | Claude 读设计 token |
| 发 Slack 消息 | ❌ | Claude 代你发 |

**MCP 的定位**：把这些「外部系统」用统一协议接入，让 Claude 像用内置工具一样调用它们——无需每个系统写一套 prompt hack。

## 二、架构三层

```
┌─────────────────────────────────────────────┐
│  Host（Claude Code）                         │
│  ┌───────────────────────────────────────┐  │
│  │  Client（MCP 客户端，内嵌于 Host）      │  │
│  └───────────┬───────────────────────────┘  │
└──────────────│──────────────────────────────┘
               │ Transport（stdio / HTTP / SSE / WebSocket）
┌──────────────▼──────────────────────────────┐
│  Server（MCP 服务端，如 @modelcontextprotocol │
│         /server-github）                     │
│  暴露：tools / resources / prompts          │
└─────────────────────────────────────────────┘
```

| 角色 | 谁 | 职责 |
| --- | --- | --- |
| **Host** | Claude Code（或 Claude.ai / Agent SDK） | 管理会话、决定调哪个 tool |
| **Client** | Host 内置 | 维持与 server 的连接、转发请求 |
| **Server** | 你装的或自己写的进程 | 对外暴露 tools / resources / prompts |

**一句话**：Claude Code 是 Host，MCP server 是「外接设备」，Transport 是「连接线」。

## 三、一个 MCP Server 能提供什么

| 能力 | 说明 | 举例 |
| --- | --- | --- |
| **Tools** | Claude 可调用的函数 | `jira_get_issue`、`postgres_query`、`slack_send` |
| **Resources** | 静态或动态数据供 Claude 读 | 项目 README、数据库 schema、配置文件 |
| **Prompts** | 预定义 prompt 模板 | 「分析这条 Sentry 错误」模板 |
| **Channels** | Server 主动推消息到 session | Telegram 新消息、webhook 事件 |

绝大多数 server 只暴露 **Tools**——其它能力按需。

## 四、在 Claude Code 里的使用流程

```text
1. 配置 → .mcp.json 或 claude mcp add
2. 连接 → Claude Code 启动时自动连
3. 发现 → Claude 通过 Tool Search 看到可用工具
4. 授权 → 首次调用时权限系统弹窗
5. 调用 → Claude 像用内置工具一样使用
```

**Tool Search**（默认开启）：Claude Code **不把所有 MCP 工具一次性塞到 context**——只在相关时动态加载，避免 token 浪费。你装 20 个 server、暴露 200 个 tool，Claude 也只在当前任务需要时才看到相关那几个。

## 五、本章「使用层」vs 能力全景「协议层」

| | 使用层（本章） | 协议层（`claude-capabilities/mcp-protocol/`） |
| --- | --- | --- |
| 读者 | Claude Code 用户 | 想自己实现 server / client 的开发者 |
| 关注点 | 怎么装、怎么配、怎么用 | Transport 规范、JSON-RPC 报文、capability negotiation |
| 前提 | 装好 Claude Code | 读过 MCP spec |

**大多数用户只需要使用层**——装几个 server、配好 `.mcp.json` 就够了。只有要写自己的 MCP server 时才需要看协议层。

## 六、安全模型

MCP 工具**和内置工具走同一套权限系统**：

- 首次调用弹权限确认（可 allow / deny / always allow）
- `.claude/settings.json` 的 `permissions.allow` 支持 MCP 工具（如 `"mcp__github__create_pr"`）
- 项目级 `.mcp.json` 的 server 需要**你手动批准**才会连接（防恶意仓库注入 server）

**⚠️ 提示注入风险**：MCP server 拉回的外部内容（JIRA 描述、Slack 消息、网页内容）可能包含恶意 prompt——Claude Code 有内建防护，但你仍应只连接**信任来源**的 server。

## 七、快速一览：常见 MCP Server

| Server | 能力 | 来源 |
| --- | --- | --- |
| `github` | Issue / PR / repo 操作 | 官方 plugin |
| `atlassian` | JIRA / Confluence | 官方 plugin |
| `postgres` | SQL 查询 | 社区 |
| `figma` | 设计稿读取 | 官方 plugin |
| `sentry` | 错误监控 | 官方 plugin |
| `slack` | 消息收发 | 官方 plugin |
| `filesystem` | 沙盒化文件访问 | 官方 |

完整列表见 [Anthropic Directory](https://claude.ai/directory) 和 [官方常用 Server](./official-servers) 🚧。

## 参考

- [Anthropic · Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp)（访问于 2026-08-03）
- [MCP 官网](https://modelcontextprotocol.io/introduction)（访问于 2026-08-03）—— 协议定义与 spec
- [Anthropic Directory](https://claude.ai/directory) —— 已审核的 MCP server 列表

## 下一步

- 实际接一个 server 试试 → [传输：stdio / HTTP / SSE](./transports) 🚧
- 看看有哪些现成 server → [官方常用 Server](./official-servers) 🚧
- 想自己写 server → [写你自己的 MCP Server](./build-your-own) 🚧

## 如果你想

- 看完整 `.mcp.json` 配置格式 → [.mcp.json 项目配置](./mcp-json-config) 🚧
- 深入传输协议细节 → [Claude 能力 · MCP 协议层](/claude-capabilities/mcp-protocol/protocol-spec) 🚧
- 理解 tool search 与 token 节省 → [上下文窗口](../basics/context-window)
