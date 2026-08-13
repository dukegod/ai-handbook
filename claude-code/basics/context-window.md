---
title: 上下文窗口
description: 200k 是怎么用完的、/context 看什么、auto-compact 后哪些还活着——Claude Code 的 context 结构与收支
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-29
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/context-window'
  accessedAt: 2026-07-29
---

# 上下文窗口

> **TL;DR**：Claude Code 默认 **200,000 tokens** 上下文；Fable 5、Sonnet 5、Opus 4.6+、Sonnet 4.6 可开 **1M**。context 里装的**远不止你能看见的对话**——system prompt、CLAUDE.md、auto memory、MCP 工具名、skill 描述、每次 file read 都在里面。用尽时**auto-compact 会摘要老对话**并**从磁盘重注入** CLAUDE.md 与 auto memory，但 **`paths:` scoped rules 与嵌套 CLAUDE.md 会丢**——这是最常被踩的坑。用 `/context` 看当前收支、`/compact focus on ...` 主动摘要以保留关键信息。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- Claude Code 一场会话里，context 到底装了什么
- 200k 与 1M 窗口的区别、哪些模型/plan 支持
- `/context` 命令看什么、`/memory` 编辑什么
- Auto-compact 之后**哪些内容活着、哪些死了**（含官方表格）
- 什么时候你该主动干预、什么时候放手

## 前置知识

- 已读 [Sessions](./sessions)——理解 `/clear` `/compact` 命令的边界
- 已读 [CLAUDE.md](./claude-md)——理解四层 memory 是怎么加载进 context 的
- 已读 [成本与 Token 管理](./cost-and-tokens)——理解每 turn 重发完整历史与 Prompt Caching

## 一、200k 装了什么

Claude Code 默认 window = **200,000 tokens**，这个数**不等于「你在终端看到的字数」**。**你输入第一个字之前**，context 里已经有：

| 层 | 大约 tokens | 来源 |
| --- | --- | --- |
| System prompt | ~4,200 | Claude Code 内置，你看不到 |
| Auto memory（`MEMORY.md`） | 视文件 | 前 200 行或 25 KB，取较小 |
| Environment info | ~280 | 工作目录 / 平台 / OS / git 状态 |
| MCP 工具名（**不含 schema**） | ~120+ | 具体 schema 通过 `ToolSearch` 按需拉，见下 |
| Skill 描述 + `when_to_use` | 每 skill ≤ 1,536 字符 | 全部 skill 常驻 |
| Project-root CLAUDE.md + unscoped rules | 视文件 | [四层 memory](./claude-md) 的静态部分 |

**MCP schema 的默认策略**：只挂工具名（省 token），schema 按调用时机拉。想强制预加载：

- `ENABLE_TOOL_SEARCH=auto`——只有能塞进 window 的 10% 才预加载
- `ENABLE_TOOL_SEARCH=false`——全预加载（贵但完全无搜索延迟）

会话开始后每一次 **file read / tool call / Claude 的回复**都往 context 里加。所以「开了一天后随手一句话其实带着整天的历史」——[Cost & Tokens · 长会话成本 5 大原因](./cost-and-tokens#五、长会话成本爬升的-5-大原因)展开讲过。

## 二、1M 是谁的

需要更大窗口时，**换模型**而不是换配置：

| 模型 | 默认窗口 | 1M 开法 |
| --- | --- | --- |
| Fable 5 | 1M | 直接就是 1M |
| Sonnet 5 | 1M | 无 `[1m]` variant（唯一）；LLM gateway 例外见官方文档 |
| Opus 4.6+ / Sonnet 4.6 | 200k | 选 `<model>[1m]` variant |
| 其他 Opus / Haiku | 200k | 无 1M |

1M 场景下 auto-compact 机制**一模一样**——只是触发阈值等比放大。**留意 1M 输入的价格**：Prompt Caching TTL 与常规窗口一致，但 cache miss 时的 token 数是常规的 5 倍。

## 三、`/context` 看什么

在会话里敲 `/context` 会看到分类明细：

```
Category           Tokens    %  Note
System prompt       4,200   2.1
Memory files        3,120   1.6  ~/.claude/CLAUDE.md, ./CLAUDE.md
MCP tools             120   0.1  (schemas deferred)
Skills              8,540   4.3  6 skills loaded
Conversation      112,300  56.2
Free              71,720  35.9
```

同时给出**优化建议**（比如「MCP 工具 X 未被调用，可关闭」）。搭配 `/memory` 打开当前加载的 memory 文件直接编辑——**不用重启会话**，下一次 turn 就能看到修改。

## 四、Auto-compact 之后哪些活着

用尽时 Claude Code **不结束会话**，而是自动 compact：把老对话摘要化。以下表格来自 [Anthropic 官方](https://code.claude.com/docs/en/context-window#what-survives-compaction)（访问于 2026-07-29）：

| 机制 | Compact 之后 |
| --- | --- |
| System prompt / output style | **不动**（不在 message history 里） |
| Project-root CLAUDE.md + unscoped rules | **从磁盘重注入** |
| Auto memory | **从磁盘重注入** |
| `paths:` scoped rules | **丢失**，直到再读一个匹配文件 |
| 嵌套 CLAUDE.md（子目录里的） | **丢失**，直到再读该子目录的文件 |
| 已调 skill body | **重注入**，每 skill 上限 5,000 tokens、总上限 25,000 tokens；旧的先丢 |
| Hooks | 不适用（hooks 是代码，不占 context） |

**v2.1.198+ 起**：auto-compact 请求继承 session 的 [extended thinking](/claude-capabilities/core/extended-thinking) 配置——开了 thinking 的会话，摘要过程也会用 thinking 生成，通常更保信息、更贵。

## 五、什么时候手动介入

**你能主动做的三件事**（`/compact` 完全自动，你甚至可以不管）：

- **`/compact focus on <topic>`** —— 摘要**前**告诉 Claude 保留什么，胜过它自己猜
- **`/clear`** —— 切换不相关任务时直接开新对话；不做 compact，0 成本
- **委托给 subagent** —— 大文件读、日志分析、抓文档，[派 subagent](/claude-code/subagents-and-workflows/what-is-a-subagent) 到独立窗口跑，主会话只收摘要

**不要**手动干预的情况：

- 会话还早、context 使用率 < 60%——观察一下 `/context` 再决定
- 处于一段复杂推理中——auto-compact 会等你结束当前 turn 再触发

## 常见坑

**改了 `paths:` scoped 的 rule，compact 后没生效**

Path-scoped rules **只有匹配文件被读时才进 context**。auto-compact 把老对话摘要掉，包括那条 rule；下次 Claude 读到匹配文件才会重加载。想让规则**永远存活**，去掉 `paths:` frontmatter 或搬到 project-root CLAUDE.md。

**Skill body 被截断，关键指令丢了**

单个 skill 在 compact 后**上限 5,000 tokens**，超过就**保留开头**丢结尾。写 `SKILL.md` 时**最重要的指令放最前**——这跟往常写代码「重要函数放最上」的直觉一致。

**Auto memory 从来没预期加载**

`MEMORY.md` 只加载**前 200 行或前 25 KB**——超过的部分**根本不会**进 context。想让 Claude 长期记住某事，检查 `/context` 里 Auto memory 一栏的实际大小，别以为写在末尾就有效。

**`/context` 显示还剩很多但下一 turn 突然 auto-compact**

一次 file read 或长 tool output 可能瞬间填掉几十 k token——`/context` 是**上一次 turn 结束后**的快照，不代表下一次 tool call 的余量。想在关键操作前留出余量，先 `/clear` 再干。

**误以为 1M 就没 auto-compact**

1M window 的 auto-compact **一样在跑**，只是阈值放大到 1M。1M 场景下的 tool output 也可能特别大（比如读一份 500k 的日志），`/compact focus` 依然是主动兜底手段。

## 参考

- [Anthropic Docs · Context window](https://code.claude.com/docs/en/context-window)（访问于 2026-07-29）
- [Anthropic Docs · Extended context](https://code.claude.com/docs/en/model-config#extended-context)（访问于 2026-07-29）
- [Anthropic Docs · How Claude Code works § When context fills up](https://code.claude.com/docs/en/how-claude-code-works#when-context-fills-up)（访问于 2026-07-29）

## 下一步

- 学写 Skill 时预留 compact 幸存空间 → [什么是 Skill](/claude-code/skills/what-is-a-skill)
- 深入 API 层缓存机制 → [Prompt Caching](/claude-capabilities/api/prompt-caching) 🚧

## 如果你想

- 看会话生命周期与 `/clear` 全场景 → [Sessions](./sessions)
- 精细分析长会话成本 → [成本与 Token 管理 § 长会话成本爬升](./cost-and-tokens#五、长会话成本爬升的-5-大原因)
- 用 subagent 把大读写隔离到子窗口 → [什么是 Subagent](/claude-code/subagents-and-workflows/what-is-a-subagent) 🚧
