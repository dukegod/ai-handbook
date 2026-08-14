---
title: TodoWrite 任务列表
description: Claude Code 的任务管理工具——TaskCreate/Get/List/Update 四件套，追踪复杂任务进度
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-08-13
verifiedWith:
  claudeCode: 2.1.220
  model: claude-sonnet-5
---

# TodoWrite 任务列表

> **TL;DR**：Claude Code 用 `TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` 管理任务进度。复杂多步任务时 Claude 会自动创建任务清单，你也可以主动要求。

⏱ 预计阅读时间：5 分钟

## 你能在这里学到

- 任务管理四件套的用法
- 任务状态流转：pending → in_progress → completed
- 任务依赖（blocks / blockedBy）的设置
- 何时该用任务管理 vs 直接执行

## 四件套速查

| 工具 | 作用 | 权限 |
|------|------|------|
| `TaskCreate` | 创建新任务 | 无需 |
| `TaskGet` | 获取任务详情 | 无需 |
| `TaskList` | 列出所有任务 | 无需 |
| `TaskUpdate` | 更新任务状态/详情 | 无需 |

## 任务状态流转

```
pending → in_progress → completed
                      → deleted
```

- **pending**：待处理，创建后的默认状态
- **in_progress**：正在处理
- **completed**：已完成
- **deleted**：永久删除

## 基本用法

### 创建任务

```
TaskCreate subject="实现用户登录功能"
          description="添加 JWT 认证、登录页面、错误处理"
          activeForm="实现用户登录"
```

### 更新状态

```
TaskUpdate taskId="1" status="in_progress"
```

```
TaskUpdate taskId="1" status="completed"
```

### 查看任务列表

```
TaskList
```

返回所有任务的摘要：ID、标题、状态、所有者、依赖。

### 获取任务详情

```
TaskGet taskId="1"
```

返回完整描述、依赖关系、评论等。

## 任务依赖

用 `addBlocks` 和 `addBlockedBy` 设置任务间的依赖关系：

```
TaskUpdate taskId="2" addBlockedBy=["1"]
```

含义：任务 2 必须等任务 1 完成后才能开始。

```
TaskUpdate taskId="1" addBlocks=["2", "3"]
```

含义：任务 1 阻塞任务 2 和 3。

::: tip 依赖检查
`TaskGet` 会显示 `blockedBy` 列表。开始工作前确认列表为空，否则说明前置任务未完成。
:::

## 何时自动触发

Claude 会在以下场景自动创建任务：

- 用户请求包含 3 个以上步骤
- 任务需要多文件修改
- 需要先探索再实施的复杂任务
- 使用 Plan Mode 时

## 何时手动触发

主动要求 Claude 创建任务清单：

```
帮我把这 5 个 API 端点都加上错误处理，用任务清单追踪进度
```

## 旧版 TodoWrite

`TodoWrite` 是 v2.1.142 之前的旧 API，新版本默认关闭。如果你的 Claude Code 版本较旧，可能还在用 `TodoWrite`——建议升级后使用 `TaskCreate` 四件套。

## 常见坑

**任务卡在 in_progress**

原因：Claude 开始了任务但未完成（可能被中断）。

修复：用 `TaskUpdate` 手动改回 `pending` 或 `completed`。

**依赖循环**

原因：A blockedBy B，B blockedBy A。

修复：检查依赖关系，打破循环。

**任务太多难以管理**

原因：创建了过多细粒度任务。

修复：合并相关任务，保持 5-10 个为宜。

## 参考

- Anthropic Docs · [Tools reference](https://code.claude.com/docs/en/tools-reference)（访问于 2026-08-13）

## 下一步

- 学会派生子代理处理任务 → [Task 派生子代理](./dispatch-subagent)
- 学会编排多任务工作流 → [Workflow 编排](../subagents-and-workflows/workflow-orchestration)

## 如果你想

- 了解任务工具在工具总览中的位置 → [工具总览](./overview)
- 用后台任务自动化 → [后台与定时任务](../advanced/automation)
