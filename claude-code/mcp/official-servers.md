---
title: 官方常用 Server
description: 按类型分类的 MCP Server 速查表——官方 plugin 版（一键装）与 modelcontextprotocol 开源版，含接入命令和典型 tool 列表
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-03
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  discoverDocs: 'https://code.claude.com/docs/en/discover-plugins'
  mcpServersGithub: 'https://github.com/modelcontextprotocol/servers'
  directoryUrl: 'https://claude.ai/directory'
  accessedAt: 2026-08-03
---

# 官方常用 Server

> **TL;DR**：MCP server 有两种获取方式：**官方 plugin**（`/plugin install xxx@claude-plugins-official`，一键装）和 **modelcontextprotocol 开源包**（`claude mcp add` 手动接，更灵活）。本页按类别列出最常用的 server——查到要的那个，照命令接就行。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- 两种获取方式的差异（plugin 版 vs 开源手动版）
- 按类别速查：源码管理 / 项目管理 / 数据库 / 设计 / 监控 / 通用
- 每个 server 的典型 tool 与接入命令

## 前置

- 读过 [什么是 MCP](./what-is-mcp) 和 [传输：stdio / HTTP / SSE](./transports)
- Claude Code v2.1.220

## 一、两种获取方式

| | 官方 Plugin 版 | modelcontextprotocol 开源版 |
| --- | --- | --- |
| 安装 | `/plugin install xxx@claude-plugins-official` | `claude mcp add` |
| 配置管理 | plugin 系统自动管 | 手动写 `.mcp.json` |
| 鉴权 | 多数自带 OAuth 流 | 需自己配 token / env |
| 更新 | auto-update 跟随 marketplace | 手动更新 |
| 命名空间 | MCP tool 无前缀 | 无前缀 |
| 最佳场景 | 快速接入、团队统一 | 精细控制、自定义配置 |

**推荐**：有 plugin 版的优先用 plugin（省配置）；plugin 不覆盖的场景再手动接。

## 二、源码管理

| Server | 能力 | 获取 |
| --- | --- | --- |
| **GitHub** | Issue / PR / repo / branch / review | `/plugin install github@claude-plugins-official` |
| **GitLab** | MR / issue / pipeline / repo | `/plugin install gitlab@claude-plugins-official` |

**典型用法**：「帮我创建一个 PR，标题从 commit 推断」→ Claude 调 `github_create_pull_request`。

## 三、项目管理

| Server | 能力 | 获取 |
| --- | --- | --- |
| **Atlassian**（JIRA + Confluence） | ticket CRUD / 搜索 / 文档读写 | `/plugin install atlassian@claude-plugins-official` |
| **Linear** | issue / project / cycle | `/plugin install linear@claude-plugins-official` |
| **Asana** | task / project / section | `/plugin install asana@claude-plugins-official` |
| **Notion** | page / database / block | `/plugin install notion@claude-plugins-official` |

**典型用法**：「实现 JIRA ENG-4521 里描述的功能并创建 PR」→ Claude 读 JIRA → 写代码 → 推 GitHub。

## 四、数据库

| Server | 能力 | 获取 |
| --- | --- | --- |
| **PostgreSQL** | SQL 查询 / schema 读 | `claude mcp add --transport stdio postgres -- npx -y @modelcontextprotocol/server-postgres <conn-string>` |
| **SQLite** | 轻量 SQL | `claude mcp add --transport stdio sqlite -- npx -y @modelcontextprotocol/server-sqlite <db-path>` |

**⚠️ 安全**：生产数据库请用只读连接字符串或限权 role，防止 Claude 执行破坏性 SQL。

## 五、设计 & 前端

| Server | 能力 | 获取 |
| --- | --- | --- |
| **Figma** | 设计稿读取 / 组件 / token | `/plugin install figma@claude-plugins-official` |
| **Vercel** | 部署 / project / domain | `/plugin install vercel@claude-plugins-official` |
| **Firebase** | Firestore / Auth / Hosting | `/plugin install firebase@claude-plugins-official` |
| **Supabase** | DB / Auth / Storage | `/plugin install supabase@claude-plugins-official` |

## 六、监控 & 通信

| Server | 能力 | 获取 |
| --- | --- | --- |
| **Sentry** | 错误事件 / issue / stacktrace | `/plugin install sentry@claude-plugins-official` |
| **Slack** | 消息收发 / channel / thread | `/plugin install slack@claude-plugins-official` |

**典型用法**：「查 Sentry 里最新 5 条错误，定位源码并修」→ Claude 拿 stacktrace → 定位 → 修复。

## 七、通用工具（modelcontextprotocol 开源）

| Server | 能力 | 安装命令 |
| --- | --- | --- |
| **Filesystem** | 沙盒化文件读写 | `claude mcp add --transport stdio fs -- npx -y @modelcontextprotocol/server-filesystem <allowed-dir>` |
| **Memory** | 持久化知识图谱 | `claude mcp add --transport stdio memory -- npx -y @modelcontextprotocol/server-memory` |
| **Brave Search** | 网页搜索 | `claude mcp add --env BRAVE_API_KEY=xxx --transport stdio brave -- npx -y @anthropic-ai/mcp-server-brave-search` |
| **Puppeteer** | 浏览器自动化 | `claude mcp add --transport stdio puppeteer -- npx -y @modelcontextprotocol/server-puppeteer` |
| **Google Maps** | 地理信息 / 路线 | `claude mcp add --env GOOGLE_MAPS_API_KEY=xxx --transport stdio maps -- npx -y @modelcontextprotocol/server-google-maps` |

## 八、在哪找更多

- **[Anthropic Directory](https://claude.ai/directory)**——已审核的远程 MCP server，可直接 `claude mcp add`
- **[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)** GitHub org——开源 server 合集
- **[claude-plugins-official](https://claude.com/plugins)**——官方 plugin 形态的 server
- **[claude-community marketplace](https://github.com/anthropics/claude-plugins-community)**——社区投稿 plugin

## 常见坑

**Plugin 版与手动版同时接同一个服务**——两份 server 会暴露重复 tool，Claude 可能调错那份。选一种方式接入。

**PostgreSQL server 用了写权限连接**——Claude 可能执行 `DROP TABLE`。**永远用只读 role 或加 hook 拦截**。

**忘了装 plugin 的依赖**——某些 plugin（如 LSP 类）需要本机装 binary。`/plugin` → Errors tab 看报错。

**Server 需要网络但你在离线环境**——远程 HTTP server 连不上时 Claude Code 标为 `✘ Failed`，本地 stdio server 不受影响。

## 参考

- [Anthropic · Discover and install plugins](https://code.claude.com/docs/en/discover-plugins)（访问于 2026-08-03）
- [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)（访问于 2026-08-03）
- [Anthropic Directory](https://claude.ai/directory)（访问于 2026-08-03）

## 下一步

- 想自己写 server → [写你自己的 MCP Server](./build-your-own) 🚧
- 鉴权流程与调试 → [鉴权与调试](./auth-and-debug) 🚧
- 完整 `.mcp.json` 配置 → [.mcp.json 项目配置](./mcp-json-config) 🚧

## 如果你想

- 回顾 MCP 概念 → [什么是 MCP](./what-is-mcp)
- 理解四种 Transport → [传输：stdio / HTTP / SSE](./transports)
- 把 MCP server 打包到 plugin 分发 → [Plugins 与 Marketplace](../skills/plugins-marketplace)
