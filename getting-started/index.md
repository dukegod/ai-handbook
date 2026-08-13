---
title: 入门
description: 从零开始了解 Claude Code；15 分钟看完核心概念，30 分钟跑起来第一个真实任务
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-07-23
---

# 入门

> 你从没用过 Claude Code？从这里开始。整章按顺序读约 30 分钟。

## 谁应该读这一章

- **完全没接触过 Claude Code** — 想搞清楚它是什么、能做什么、和 Copilot / Cursor 有什么不同
- **听说过但没上手** — 想在半小时内跑起来第一个真实任务
- **有 CLI 经验的开发者** — 快速建立心智模型，之后跳到 [Claude Code](/claude-code/) 深入

## 推荐阅读顺序

```mermaid
flowchart LR
  A[什么是 Claude Code] --> B[安装与认证]
  B --> C[第一次对话]
  C --> D[心智模型]
  D --> E[对比 Cursor / Copilot / Codex CLI]

  style A fill:#f4d5c5,stroke:#c96442
  style D fill:#f4d5c5,stroke:#c96442
```

心智模型（图中橙色）是本章最重要的两页：一开一合，前者建立初印象，后者让你能预测 Claude Code 的行为。

## 本章目录

| # | 页面 | 一句话 | 时长 |
| --- | --- | --- | --- |
| 1 | [什么是 Claude Code](./what-is-claude-code) | Anthropic 官方 CLI，让 Claude 直接进入你的终端 | 3 分钟 |
| 2 | [安装与认证](./installation) | macOS / Linux / Windows / WSL 全平台，含常见报错 | 5 分钟 |
| 3 | [第一次对话](./first-conversation) | 从 `claude` 命令到第一个可用回答，含 `/help` `/model` `/cost` | 5 分钟 |
| 4 | [心智模型](./mental-model) | 一张图讲透 Claude Code 如何工作——全站的认知锚点 | 10 分钟 |
| 5 | [对比 Cursor / Copilot / Codex CLI](./comparisons) | 一张选型表，帮你决定要不要迁移过来 | 7 分钟 |

## 下一步

读完本章后：

- **想深入使用** → [Claude Code 精通](/claude-code/)
- **想直接看代码** → [Cookbook · 第一个真实任务](/cookbook/first-real-task)
- **想理解模型底层能力** → [Claude 能力全景](/claude-capabilities/)

## 如果你想

- 只查一个具体命令 → [参考 · CLI Flags](/reference/cli-flags)
- 了解术语中英对照 → [术语表](/contributing/glossary)
