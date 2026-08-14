---
title: Task 派生子代理
description: Claude Code 的 Agent 工具——派生 Subagent 到独立 context 并行干活，主会话不阻塞
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-13
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5
---

# Task 派生子代理

> **TL;DR**：`Agent` 工具派生一个 Subagent 到独立 context 执行任务，结果返回主会话。适合并行、隔离、重型任务。

⏱ 预计阅读时间：6 分钟

## 你能在这里学到

- Agent 工具的核心概念与参数
- Subagent 的工具子集与限制
- 同步 vs 后台运行的选择
- 工作隔离（worktree）的用法

## 核心概念

`Agent` 创建一个**独立的 Claude 会话**（Subagent），在自己的 context window 中执行任务，完成后把结果返回主会话。

```
Agent prompt="搜索 src/ 目录中所有 TODO 注释，按文件分组汇总"
      description="搜索 TODO 注释"
```

## 核心参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `prompt` | 任务描述（必须） | — |
| `description` | 简短描述（3-5 词） | — |
| `model` | 模型覆盖 | 继承主会话 |
| `run_in_background` | 后台运行 | `true` |
| `isolation` | 隔离模式 | 无 |

## 同步 vs 后台

**后台运行（默认）**

```
Agent prompt="分析 src/auth.ts 的代码质量"
      run_in_background="true"
```

Subagent 在后台执行，主会话继续工作。完成后收到通知。

**同步运行**

```
Agent prompt="读取 package.json 并提取依赖版本"
      run_in_background="false"
```

主会话等待 Subagent 完成再继续。需要结果才能继续下一步时使用。

::: tip 选择建议
- 不需要立即结果 → 后台（默认）
- 后续步骤依赖结果 → 同步
- 并行多个任务 → 全部后台
:::

## 工具子集

Subagent **不继承**主会话的全部工具。默认可用的工具子集：

- `Read`、`Edit`、`Write`、`Bash`、`Grep`、`Glob`、`LSP`
- `WebFetch`、`WebSearch`
- `TaskCreate/Get/List/Update`
- `Agent`（可递归派生）

**不可用的工具**：

- `ExitPlanMode`、`Skill`、`EnterWorktree`、`ExitWorktree`
- MCP 工具（需显式配置）

可通过 Subagent 定义的 `tools` / `disallowedTools` 进一步收窄。

## 工作隔离

`isolation: "worktree"` 让 Subagent 在独立的 git worktree 中工作：

```
Agent prompt="重构 src/utils.ts，提取公共函数"
      isolation="worktree"
```

**适用场景**：

- 多个 Subagent 并行修改文件（避免冲突）
- 需要隔离的实验性修改
- 代码审查（不影响工作目录）

::: warning worktree 开销
每次 worktree 隔离约 200-500ms 设置时间 + 额外磁盘空间。只在确实需要并行修改时使用。
:::

## 模型选择

Subagent 默认继承主会话模型。可用 `model` 参数覆盖：

```
Agent prompt="简单文件读取任务"
      model="haiku"
```

```
Agent prompt="复杂架构分析"
      model="opus"
```

::: tip 何时覆盖模型
- 简单机械任务 → `haiku`（省成本）
- 需要深度推理 → `opus`
- 大多数场景 → 不设，继承主会话
:::

## 常见模式

### 并行探索

```
# 同时探索三个模块
Agent prompt="分析 src/auth/ 的代码结构" description="探索 auth"
Agent prompt="分析 src/api/ 的代码结构" description="探索 api"
Agent prompt="分析 src/db/ 的代码结构" description="探索 db"
```

### 代码审查

```
Agent prompt="审查 src/auth.ts 的安全性，列出潜在问题"
      description="安全审查"
      model="opus"
```

### 文件批处理

```
Agent prompt="把 src/ 下所有 .js 文件转换为 .ts"
      description="JS 转 TS"
      isolation="worktree"
```

## 常见坑

**Subagent 没有输出**

原因：`run_in_background` 默认为 `true`，结果在通知中。

修复：用 `run_in_background="false"` 同步获取结果。

**工具不可用**

原因：Subagent 的工具子集不包含该工具。

修复：检查 Subagent 定义的 `tools` / `disallowedTools`。

**worktree 冲突**

原因：多个 Subagent 修改同一文件。

修复：确保每个 worktree 修改不同文件，或用 `isolation="worktree"` 隔离。

## 参考

- Anthropic Docs · [Sub-agents](https://code.claude.com/docs/en/sub-agents)（访问于 2026-08-13）
- Anthropic Docs · [Sub-agents · Available tools](https://code.claude.com/docs/en/sub-agents#available-tools)（访问于 2026-08-13）

## 下一步

- 学会编排多个 Subagent → [Workflow 编排](../subagents-and-workflows/workflow-orchestration)
- 了解不同 Agent 类型 → [Agent 类型清单](../subagents-and-workflows/agent-types)

## 如果你想

- 了解 Agent 在工具总览中的位置 → [工具总览](./overview)
- 用 Workflow 做确定性编排 → [Workflow 编排](../subagents-and-workflows/workflow-orchestration)
- 深入多 Agent 模式 → [多 Agent 常见模式](../subagents-and-workflows/multi-agent-patterns)
