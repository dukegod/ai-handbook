---
title: WebFetch / WebSearch
description: Claude Code 的 WebFetch 与 WebSearch 工具——抓取网页内容 vs 联网搜索，让 Claude 获取外部信息
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-13
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5
---

# WebFetch / WebSearch

> **TL;DR**：`WebFetch` 抓一个 URL 转 markdown，`WebSearch` 联网搜索返回结果列表。两者默认需确认，可按域名放行。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- WebFetch 与 WebSearch 的核心区别
- WebFetch 的 URL 限制与缓存机制
- WebSearch 的搜索范围与结果格式
- 权限配置与常见坑

## WebFetch：抓取网页

`WebFetch` 抓取一个 URL，转换为 markdown，然后基于内容回答 prompt：

```
WebFetch url="https://docs.claude.com/en/api/messages"
        prompt="提取 Messages API 的请求格式"
```

### 工作流程

1. 抓取 URL 内容
2. 转换为 markdown
3. 用 `prompt` 对内容提问
4. 返回答案（不是原始 HTML）

### 限制

| 限制 | 说明 |
|------|------|
| **需 HTTPS** | HTTP 自动升级为 HTTPS |
| **不支持认证页面** | 需要登录的页面抓不到 |
| **缓存 15 分钟** | 同一 URL 15 分钟内返回缓存 |
| **跨域重定向** | 返回重定向 URL 而非自动跟随 |

::: tip 适用场景
抓取公开文档、API 参考、博客文章等**不需要登录**的页面。需要认证的内容用 MCP 工具或 `gh` CLI。
:::

## WebSearch：联网搜索

`WebSearch` 执行联网搜索，返回带标题和 URL 的结果块：

```
WebSearch query="Claude Code MCP server tutorial"
```

### 结果格式

返回结构化的搜索结果，包含：
- 标题
- URL
- 摘要片段

### 限制

| 限制 | 说明 |
|------|------|
| **美国区搜索** | 结果偏向英文和美国地区 |
| **无分页** | 只返回首页结果 |
| **需确认** | 默认需要用户确认 |

## 使用场景对比

| 场景 | 用哪个 |
|------|--------|
| 已知 URL，需要内容 | `WebFetch` |
| 不知道 URL，需要搜索 | `WebSearch` |
| 查官方文档 | `WebFetch`（直接抓文档页） |
| 查最新资讯 | `WebSearch` |
| 获取 API 参考 | `WebFetch`（已知文档 URL） |

## 权限配置

两个工具默认**需要确认**。可按域名放行 `WebFetch`：

```json
{
  "permissions": {
    "allow": [
      "WebFetch(docs.claude.com)",
      "WebFetch(github.com)",
      "WebSearch"
    ]
  }
}
```

::: warning WebSearch 无法按域名限制
`WebSearch` 不支持按域名过滤结果。放行后所有搜索请求都会自动通过。
:::

## 常见坑

**WebFetch 返回空内容**

原因：页面需要 JavaScript 渲染（SPA），或需要认证。

修复：用 `Bash` + `curl` 获取原始内容，或用 MCP 工具。

**WebSearch 结果不相关**

原因：搜索词太泛，或结果偏向英文。

修复：用更具体的关键词，包含英文技术术语。

**缓存导致内容过时**

原因：同一 URL 15 分钟内返回缓存。

修复：等 15 分钟，或在 URL 后加 `?v=2` 等参数绕过缓存。

## 参考

- Anthropic Docs · [Tools reference](https://code.claude.com/docs/en/tools-reference)（访问于 2026-08-13）

## 下一步

- 学会管理任务列表 → [TodoWrite 任务列表](./todo)
- 学会派生子代理 → [Task 派生子代理](./dispatch-subagent)

## 如果你想

- 了解 Web 工具在工具总览中的位置 → [工具总览](./overview)
- 用 MCP 扩展更多 Web 能力 → [什么是 MCP](../mcp/what-is-mcp)
