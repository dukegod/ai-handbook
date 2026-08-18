---
title: Claude.ai
description: Anthropic 官方 Web 产品——chat / project / artifacts / 5 个实战模式
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-07
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-5
  claudeAi: 'https://claude.ai'
  accessedAt: 2026-08-07
---

# Claude.ai

> **TL;DR**：claude.ai 是 Anthropic 官方 Web 端——开箱即用的 chat 界面，无需编程。**适合非开发者 / 临时任务 / 团队协作**。支持 model 切换、project（持久化 system + 知识库）、artifacts（独立可分享输出）。

⏱ 预计阅读时间：4 分钟

## 一、核心能力

| 能力 | 说明 |
| --- | --- |
| **Chat** | 单次对话（多轮 context） |
| **Projects** | 持久化 system + 知识库 + 多次对话 |
| **Artifacts** | 独立窗口渲染代码 / 文档 / SVG / 图表 |
| **Custom Styles** | 自定义 system prompt 风格 |
| **Team Workspace** | 团队共享 project / 知识库 |
| **File Upload** | PDF / 图片 / 代码文件（> 文本输入） |
| **Web Search** | 内置联网搜索（与 WebFetch 不同） |

## 二、5 个实战模式

### 模式 1：日常对话

直接在 chat 框问问题——开箱即用。

### 模式 2：Project 持久化

```
Project: "我的代码审查助手"
  - System: "你是 Rust 资深审查员..."
  - 知识库: 公司编码规范、过去 10 次审查结果
  - 多轮对话: 都在这个 project 内
```

**优势**：跨对话保留 system + 知识库——比每次重新输入方便。

### 模式 3：Artifacts 输出

```text
用户：请画一张 transformer 架构图
Claude：<artifact>SVG 图表</artifact>
       ↑ 独立窗口渲染，可下载 / 分享
```

**支持 artifact 类型**：
- React 组件
- HTML / CSS / JS
- SVG 图表
- Markdown 文档
- Mermaid 流程图

### 模式 4：团队协作

```
Workspace: "Marketing Team"
  - Members: 全员
  - Projects: 文案风格 / 品牌指南 / 客户 FAQ
  - 共享 system + 知识库
```

**优势**：团队风格统一、新人 onboarding 快。

### 模式 5：代码任务（无 CLI）

不想用 Claude Code 终端？claude.ai 能：

```
上传代码 → 问 "找 bug" → 看到带行号的修改建议
```

**vs Claude Code**：

| 维度 | claude.ai | Claude Code |
| --- | --- | --- |
| 入口 | Web 浏览器 | 终端 |
| 改文件 | 手动复制 | 自动 |
| 跑命令 | ❌ | ✅ |
| 适合 | 临时 / 探索 | 项目级 |

## 三、3 个常见坑

**1. Knowledge base ≠ 长期记忆**

Knowledge base 静态文件——Claude **不会从对话中自动学习**。要持续优化就更新文件。

**2. Project 间不共享 context**

每个 project 独立——chat history 不互通。需要的话**主动复制**或**导出**。

**3. 团队 plan 才有 Workspace**

个人 plan 只能个人用——团队用需要 Team plan。

## 四、与 API 关系

```
claude.ai  →  Anthropic 提供的 Web 产品（付费 plan）
Claude API  →  Anthropic 提供的 HTTP 服务（API key 付费）
Claude Code  →  Anthropic 提供的 CLI 工具（同 API）
```

**三者用同一组 model**（Opus 5 / Sonnet 5 / Haiku 4.5 / Fable 5），但**计费 / 功能 / 限额不同**。

详见 [模型家族总览](/claude-capabilities/models/overview)。

## 五、何时用 claude.ai vs Claude Code vs API

| 场景 | 用 |
| --- | --- |
| 临时 / 探索 / 学习 | **claude.ai** |
| 团队协作 / 知识管理 | **claude.ai** |
| 项目级编码 / 文件操作 | **Claude Code** |
| 自动化 / CI | **API** |
| 自建应用 | **API** |

## 参考

- [Claude.ai 官方](https://claude.ai)
- [模型家族总览](/claude-capabilities/models/overview)
- [Artifacts](/claude-capabilities/surfaces/artifacts)
- [Claude Code 入门](/claude-code/getting-started/what-is-claude-code)

## 下一步

- 渲染输出 → [Artifacts](/claude-capabilities/surfaces/artifacts)
- 桌面应用 → [Desktop](/claude-capabilities/surfaces/desktop-app)
- 切到 API → [Messages API](/claude-capabilities/api/messages)

## 如果你想

- 团队 Workspace → [Claude.ai · 团队协作](#模式-4团队协作)
- 深度提示工程 → [深度提示工程](/claude-capabilities/prompting/best-practices)
