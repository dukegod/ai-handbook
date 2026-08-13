---
title: 后台与定时任务
description: 'Claude Code 后台任务与定时任务——background Bash/subagent、/agents 视图、CronCreate 定时调度、ScheduleWakeup 自节拍，headless 与自动化编排'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-04
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  agentViewDocs: 'https://code.claude.com/docs/en/agent-view'
  cronDocs: 'https://code.claude.com/docs/en/scheduled-tasks'
  accessedAt: 2026-08-04
---

# 后台与定时任务

> **TL;DR**：Claude Code 有三层「异步」能力：**后台任务**（`Ctrl+B` 转后台的 Bash/subagent，`/tasks` 看）、**Background Agent**（独立 session，`/agents` 视图监控）、**定时任务**（`/scheduled-tasks` cron 调度，app 关了也能跑）。三者各自适合不同场景，别混。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- 后台 Bash 命令（session 内）
- Background Agent（独立 session）
- 定时任务（cron 调度）
- 三者边界与选型
- headless + cron 的自动化组合

## 前置

- 读过 [Headless / CI 模式](./headless) 和 [Subagent](../subagents-and-workflows/what-is-a-subagent)

## 一、三层异步能力对比

| 能力 | 作用域 | 监控 | 适合 | 生命周期 |
| --- | --- | --- | --- | --- |
| **后台 Bash/subagent** | session 内 | `/tasks` | 长命令不阻塞主对话 | 随 session |
| **Background Agent** | 独立 session | `/agents` 视图 | 并行独立任务 | 独立进程 |
| **定时任务** | 跨 session | `/scheduled-tasks` | 周期/延时触发 | app 开着才跑 |

## 二、后台 Bash 命令（session 内）

把运行中的 Bash 命令转后台——不阻塞主对话：

- **`Ctrl+B`**：把当前 Bash 调用转后台（tmux 按两次）
- **`run_in_background: true`**：Bash 工具参数，直接后台跑

```bash
# Claude 主动后台跑
claude -p "在后台跑 dev server" --allowedTools "Bash"
```

**特点**：

- 输出写文件，Claude 用 Read 工具取
- 有唯一 task ID
- session 退出自动清理（转后台 session 则交接给它）
- 输出超 5GB 自动杀
- macOS/Linux：session 空闲超 30 分钟 + OS 内存压力时杀（`CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` 关）

**查看**：`/tasks` 看运行中的 shell 和 subagent。

**subagent 后台**：v2.1.198+ subagent 默认后台跑。`background: true` 强制后台。

## 三、Background Agent（独立 session）

独立 session 跑——主 session 关了它还在。`/agents` 视图监控多个并行 session。

**从 session 里派发**：

```text
用 /agents 派一个后台 session 去跑测试
```

**从 CLI**：

```bash
claude agents
```

**特点**：

- 每个 background agent 是独立 session（独立 context）
- 用你的 settings permission mode（不是父 session 的）
- `/agents` 视图看状态、结果、交互
- 完成后通知
- agent team 多 session 互相通信

**与 subagent 区别**：subagent 在**当前 session 内**独立窗口；background agent 是**另一个 session**。

## 四、定时任务（cron 调度）

`/scheduled-tasks` 管理——cron 表达式（本地时区）调度任务自动跑。

**创建**：

```text
/scheduled-tasks
```

或用工具：

- **CronCreate**：recurring（`*/5 * * * *`）或 one-shot（`fireAt`）
- **CronDelete** / **CronList**：删 / 列

**关键约束**：

- **app 开着才跑**——关了不跑，下次开 app 跑（one-shot 错过的在下次开 app 补跑）
- **非无人值守**——与 OS cron 不同，Claude Code 的定时任务需要 app 运行
- 每个 task 是独立 session，**无对话记忆**——prompt 必须自包含
- recurring 任务 **7 天自动过期**（fire 一次后删）

**durable vs session-only**：

- `durable: false`（默认）：仅当前 session，Claude 退出即没
- `durable: true`：写 `.claude/scheduled_tasks.json`，跨 session 持久

**适合**：

- 「每天早上检查 PR 状态」
- 「每小时同步某个 dashboard」
- 「15 分钟后提醒我 review」

## 五、ScheduleWakeup（自节拍）

`/loop` 动态模式——Claude 自己决定何时再被唤醒继续迭代：

- 不用 cron 固定间隔
- Claude 完成一轮后调 `ScheduleWakeup` 安排下次
- 适合「持续监控某状态直到变化」的循环任务

**delaySeconds 选型**：

- < 5 分钟：cache 保持热
- 5 分钟–1 小时：付 cache miss，换更长等待
- **别选 300s**：最差——付 cache miss 又没摊薄

## 六、headless + cron 自动化

OS 层 cron 调 `claude -p`：

```bash
# crontab -e
0 9 * * * cd /path/to/repo && claude --bare -p "检查依赖更新并报告" \
  --allowedTools "Bash,Read" --output-format json >> /tmp/claude-deps.log
```

**vs Claude Code 内定时任务**：

| | Claude Code 定时任务 | OS cron + `claude -p` |
| --- | --- | --- |
| app 依赖 | 需 app 开着 | 不依赖 |
| 持久 | durable 跨 session | OS 级，最稳 |
| 交互 | 可在 app 里看 | 纯日志 |
| 适合 | 开发时辅助 | 真正无人值守 |

**真正无人值守用 OS cron + `claude --bare -p`**；开发时辅助用 Claude Code 内定时任务。

## 七、关闭后台能力

```bash
CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1   # 关所有后台任务
```

或 settings.json：

```json
{ "disableWorkflows": true }
```

## 常见坑

**定时任务 app 关了不跑**——Claude Code 定时任务需 app 运行。要真无人值守用 OS cron + `claude -p`。

**定时任务 prompt 不自包含**——每个 task 是新 session，无对话记忆。写清要做什么、读哪些文件、输出到哪。

**recurring 任务 7 天后没了**——自动过期机制。长期任务用 OS cron。

**后台 Bash 输出超 5GB 被杀**——大输出重定向到文件、用 Read 工具取片段。

**background agent 用错 permission mode**——它用你 settings 的 permission mode，不是父 session 的。CI 场景注意配 `acceptEdits` 或 allow 规则。

## 参考

- [Anthropic · Agent view（background agents）](https://code.claude.com/docs/en/agent-view)（访问于 2026-08-04）
- [Anthropic · Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks)（访问于 2026-08-04）
- [Anthropic · Background tasks](https://code.claude.com/docs/en/interactive-mode#background-bash-commands)（访问于 2026-08-04）

## 下一步

- Headless 模式 → [Headless / CI 模式](./headless)
- Git 与 PR 工作流 → [Git 与 PR 工作流](./git-workflow)
- 多 agent 编排 → [Workflow 编排](../subagents-and-workflows/workflow-orchestration)

## 如果你想

- 真正无人值守 → OS crontab + `claude --bare -p`（见第六节）
- 并行多 session → `/agents` 派 background agent
- 持续监控循环 → `/loop` + ScheduleWakeup
