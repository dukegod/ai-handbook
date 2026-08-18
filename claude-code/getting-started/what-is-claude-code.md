---
title: 什么是 Claude Code
description: Anthropic 官方 agentic 编程工具的一句话定义、能力全景、平台矩阵、术语边界与选型建议
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-07-28
verifiedWith:
  claudeCode: 2.1.215
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/overview'
  accessedAt: 2026-07-28
---

# 什么是 Claude Code

> **TL;DR**：Claude Code 是 Anthropic 官方的 **agentic 编程工具**——它能读你的整个代码库、编辑文件、执行命令、调用你的开发工具，运行在终端、IDE 插件、桌面应用、浏览器和手机上。

⏱ 预计阅读时间：3 分钟

## 你能在这里学到

- Claude Code 的一句话定义
- 它能做什么（三层能力 + 典型场景）
- 它在哪些「表面」上运行（Terminal / IDE / Desktop / Web / Mobile）
- 「Claude」「Anthropic」「Claude Code」三者的边界
- 什么样的人最适合用它

## 前置知识

无。这是入门第一篇。

## 一句话定义

Anthropic 官方的原话是：

> Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools.
>
> —— 引自 [Anthropic Docs · Claude Code Overview](https://code.claude.com/docs/en/overview)（访问于 2026-07-28）

抓住两个关键词：

- **agentic**：不是行内补全，也不是聊天问答——Claude Code 是一个能自己**决定用什么工具、怎么用**的 Agent
- **coding tool**：目标场景是编程，重心是代码库、命令、开发工具

如果你熟悉 GitHub Copilot 的行内补全或 Cursor 的编辑器内聊天，可以这样区分：

- Copilot / Cursor 是 **Chat + Edit**——你打字它接你
- Claude Code 是 **Agent Loop**——你给目标它自己去干

这条循环的详细图见 [心智模型](./mental-model)。

## 三层能力

Claude Code 的能力可以分成三层：

### 1. 对话

用中文或英文自然语言告诉 Claude 你想做什么。不用写 prompt 模板，日常语言即可。

```bash
$ claude "帮我给 auth 模块补一版单元测试，跑一遍并修掉失败"
```

### 2. 工具调用

Claude 自动决定何时调用工具。内置工具覆盖：

- 文件：Read / Write / Edit
- Shell：Bash
- 搜索：Grep / Glob
- Web：WebFetch / WebSearch
- 任务：TodoWrite（Claude 自己给自己列 todo）
- 子代理：Task（派生独立上下文的 Subagent）

工具全表见 [工具总览](/claude-code/tools/overview)。

### 3. 会话记忆

- **Session**：一次连续交互的完整历史
- **[CLAUDE.md](/claude-code/basics/claude-md)**：项目 / 用户 / 企业级的持久化上下文文件
- **[Skills](/claude-code/skills/what-is-a-skill)**：Claude 自动调用的能力包
- **Auto Memory**：Claude 自己跨会话记住 build 命令、调试洞察等，无需你手写

## Claude Code 跑在哪里

不只是命令行。Anthropic 目前把 Claude Code 支持在 5 个「表面」（Surface）上：

| 表面 | 适合场景 |
| --- | --- |
| **Terminal CLI** | 本站主要教这个；最完整、最灵活 |
| **VS Code / Cursor 插件** | 需要图形化 diff 与选区共享 |
| **JetBrains 插件** | IntelliJ / WebStorm / PyCharm |
| **Desktop App** | macOS / Windows 独立应用，支持多会话并行 |
| **Web / Mobile** | 无本地环境时用；`claude.ai/code` + 手机 App |

关键：**同一份 CLAUDE.md、settings、MCP servers 在所有表面共享**。你在终端配置好的东西，桌面 App 打开同一项目立刻能用。

## 三者禁止混用：Claude / Anthropic / Claude Code

一份写作规范级别的约束（详见 [术语表](/contributing/glossary#claude-与-anthropic-家族)）：

| 说到 | 指的是 |
| --- | --- |
| **Anthropic** | 出品公司 |
| **Claude** | 模型本身（Opus 4.8 / Sonnet 5 / Haiku 4.5 / Fable 5） |
| **Claude Code** | Anthropic 出品的编程工具，底层调用 Claude 模型 |

新手最常见的错误：

- ❌「Claude 公司出了个新工具」 → ✅「Anthropic 出了 Claude Code」
- ❌「Claude Code 模型」 → ✅「Claude Code 工具」或「Claude 模型」
- ❌「Anthropic CLI」 → ✅「Claude Code」

## 什么样的人最适合用

- **日常在终端工作**的开发者——Claude Code CLI 就在你已经开着的 iTerm / WezTerm / Warp 里
- **想让 AI 深入代码库**的人——它不像 Copilot 只看到当前光标附近，它能读全库、跨文件推理
- **有多步 Agent 任务需求**的人——比如「审 30 个 PR、按 issue 打标签、写 release notes」这种 chain-of-tasks
- **想让 CI 也用上 AI** 的团队——可以通过 [GitHub Actions](https://code.claude.com/docs/en/github-actions) 集成

如果你更喜欢 IDE 内的图形交互，Cursor / Copilot Chat 仍然是好选择——它们和 Claude Code 不冲突，可以并存。详细对比见 [对比 Cursor / Copilot / Codex CLI](./comparisons)。

## 参考

- [Anthropic Docs · Claude Code Overview](https://code.claude.com/docs/en/overview)（访问于 2026-07-28）
- [Anthropic Docs · Quickstart](https://code.claude.com/docs/en/quickstart)（访问于 2026-07-28）
- [Anthropic 产品页 · code.claude.com](https://code.claude.com/)（访问于 2026-07-28）

## 下一步

- 装到你的机器上 → [安装与认证](./installation)

## 如果你想

- 直接看它长啥样 → [第一次对话](./first-conversation)
- 跳过铺垫，看内部机制 → [心智模型](./mental-model)
- 先决定要不要迁移 → [对比 Cursor / Copilot / Codex CLI](./comparisons)
