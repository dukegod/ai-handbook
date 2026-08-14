---
title: 工具总览
description: Claude Code 内置的 40+ 个工具一表看完，附场景、权限与深入链接
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-28
verifiedWith:
  claudeCode: 2.1.215
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/tools-reference'
  accessedAt: 2026-07-28
---

# 工具总览

> **TL;DR**：Claude Code 出厂带 40+ 个工具，覆盖文件、Shell、搜索、Web、任务、子代理、Plan Mode、Worktree、调度、Workflow 十大类。**不是每个都要记**——先记 9 类里最常用的十来个，剩下的用到再查。这一页就是那张速查表。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- Claude Code 内置工具的十大类分组与每一类的典型触发场景
- 每个工具的权限档位（默认放行 vs 需要询问）
- 内置工具 vs MCP Server 工具 vs Skill 三者的边界
- Subagent 能用哪些子集，被谁限制

## 前置

- 装好 Claude Code v2.1.215+（早期版本部分工具名或行为不同）
- 读过 [权限系统](../basics/permissions)——权限档位在下表右列会用到

## 十大类速查表

「一句话作用」写给你，「权限」写给 `/permissions` 配置者。链接指向本站更细的一页——🚧 表示尚未撰写。

### ① 文件（4）

| 工具 | 一句话作用 | 权限 | 深入 |
| --- | --- | --- | --- |
| `Read` | 按行读取文件/图片/PDF/notebook 单元格 | 无需（工作目录外要放行） | [Read](./read) |
| `Edit` | 精准替换文件片段（含 `replace_all`） | 需询问 | [Edit & Write](./edit-and-write) |
| `Write` | 新建或整覆写文件 | 需询问 | [Edit & Write](./edit-and-write) |
| `NotebookEdit` | 改 Jupyter notebook 单元格 | 需询问 | [Notebook](./notebook) |

> **note**：`MultiEdit` 已合入 `Edit` 的 `replace_all` 语义，不再是独立工具。

### ② Shell（3）

| 工具 | 一句话作用 | 权限 | 深入 |
| --- | --- | --- | --- |
| `Bash` | 执行 shell 命令，支持后台与 timeout | 需询问（内置只读命令直接放行） | [Bash](./shell) |
| `PowerShell` | 原生 PowerShell（Windows / 支持环境） | 需询问 | [Bash](./shell) |
| `Monitor` | 后台跑一条命令并把每行输出回喂给 Claude | 需询问 | — |

### ③ 搜索（3）

| 工具 | 一句话作用 | 权限 | 深入 |
| --- | --- | --- | --- |
| `Grep` | 按 ripgrep 语法搜文件内容 | 无需 | [Grep / Glob](./search) |
| `Glob` | 按 glob 模式匹配文件路径 | 无需 | [Grep / Glob](./search) |
| `LSP` | 跳转定义、找引用、类型报错（需装 LSP） | 无需 | — |

### ④ Web（2）

| 工具 | 一句话作用 | 权限 | 深入 |
| --- | --- | --- | --- |
| `WebFetch` | 抓一个 URL 转 markdown 再答一段 prompt | 需询问（可按域名放行） | [Web](./web) |
| `WebSearch` | 联网搜索（美国区）返回带 URL 的结果列表 | 需询问 | [Web](./web) |

### ⑤ 任务管理（7）

| 工具 | 一句话作用 | 权限 | 深入 |
| --- | --- | --- | --- |
| `TaskCreate` / `Get` / `List` / `Update` | v2.1.142+ 的任务清单四件套 | 无需 | [Todo](./todo) |
| `TaskOutput` / `TaskStop` | 读/停后台任务 | 无需 | [Todo](./todo) |
| `TodoWrite` | 老 API，2.1.142 起默认关闭 | 无需 | [Todo](./todo) |

### ⑥ 子代理与通信（3）

| 工具 | 一句话作用 | 权限 | 深入 |
| --- | --- | --- | --- |
| `Agent` | 派生一个 subagent 到独立 context 干活 | 无需（子调用逐条判） | [Dispatch Subagent](./dispatch-subagent) |
| `SendMessage` | 给 agent-team 队友/已完成 subagent 传消息 | 无需 | [Multi-agent 模式](/claude-code/subagents-and-workflows/multi-agent-patterns) 🚧 |
| `Workflow` | 跑一段编排多 subagent 的确定性脚本 | 需询问 | [Workflow 编排](/claude-code/subagents-and-workflows/workflow-orchestration) 🚧 |

### ⑦ Plan Mode（2）

| 工具 | 一句话作用 | 权限 | 深入 |
| --- | --- | --- | --- |
| `EnterPlanMode` | 切进 plan 模式，只读探索 | 无需 | [Plan Mode](../basics/plan-mode) |
| `ExitPlanMode` | 呈上 plan 等你审批 | 需询问 | [Plan Mode](../basics/plan-mode) |

### ⑧ Worktree（2）

| 工具 | 一句话作用 | 权限 | 深入 |
| --- | --- | --- | --- |
| `EnterWorktree` | 新建或切入一个 git worktree | 需询问 | [Worktree](../advanced/worktree) |
| `ExitWorktree` | 退回原目录（保留或删除 worktree） | 无需 | [Worktree](../advanced/worktree) |

### ⑨ 调度与后台（4）

| 工具 | 一句话作用 | 权限 | 深入 |
| --- | --- | --- | --- |
| `CronCreate` / `List` / `Delete` | 会话内一次性或周期任务 | 无需 | [自动化](../advanced/automation) |
| `ScheduleWakeup` | 自适应 `/loop` 的下次触发（Claude 自调） | 无需 | [自动化](../advanced/automation) |

### ⑩ 其他常见（4）

| 工具 | 一句话作用 | 权限 | 何时会遇到 |
| --- | --- | --- | --- |
| `Skill` | 主对话里显式调一个 skill | 需询问 | 输 `/skill-name` 时 |
| `AskUserQuestion` | 弹一个多选题问你 | 无需 | Claude 遇到分歧 |
| `ReportFindings` | 结构化上报 code-review 结果 | 无需 | 走 code-review skill 时 |
| `EndConversation` | 直接结束会话（v2.1.213+） | 无需 | 极少见 |

## 剩下几个专用工具

MCP 相关：`ListMcpResourcesTool` / `ReadMcpResourceTool` / `ToolSearch` / `WaitForMcpServers`——只有连了 MCP Server 才用得上，见 [什么是 MCP](../mcp/what-is-mcp) 🚧。

对外发送：`SendUserFile` / `PushNotification` / `Artifact` / `ShareOnboardingGuide` / `RemoteTrigger`——把内容外送到你的设备、claude.ai 或 Slack 时才被拉起，多数走 Anthropic 直连基础设施（Bedrock/Vertex/Foundry 上不可用）。

## 内置工具 vs MCP Server vs Skill

三者常被混为一谈。核心区别：

- **内置工具**：Claude Code 二进制自带，40+ 个，工具名不会变（`Read`、`Bash`、`Agent`…）。上表的所有工具都属于这类。
- **MCP Server 工具**：由 `.mcp.json` 或用户配置**动态注册**。工具名形如 `mcp__<server>__<tool>`（例：`mcp__github__create_issue`）。装了才有，不同机器/项目可用集不同。
- **Skill**：**不是工具**，是一个 markdown 文件 + 可选脚本，被 Claude 判定为「该做这件事」时通过 `Skill` 工具拉起。Skill 内部可以调若干内置工具，但 Skill 本身不出现在工具列表里。

一次调用**能用哪些工具**受层层过滤：`settings.json` 的 `permissions.allow/deny` → CLI `--allowedTools/--disallowedTools` → subagent 定义的 `tools/disallowedTools` → skill frontmatter 的 `allowed-tools`。任一层拒掉就用不到。

## Subagent 的工具子集

`Agent` 派生的 subagent 不是继承你的全部工具。它拿到的是 [subagent 可用工具集](https://code.claude.com/docs/en/sub-agents#available-tools)（比主会话少几个，例如 `ExitPlanMode`、`Skill` 默认不给），再被自身 frontmatter 的 `tools` / `disallowedTools` 收窄。

规则速记：

- 两个字段都没设 → 拿 subagent 可用集全集
- 只设 `tools` → 只给列表里的
- 只设 `disallowedTools` → 全集减去列表
- 都设 → `disallowedTools` 胜出

一个 `tools` 列表里所有条目都匹配不到可用工具时，`Agent` 会直接报错而不是启动一个「零工具 subagent」。

## 三个坑

- **别把 MCP 工具当内置**——同事的 `.mcp.json` 你没装就用不了；写文档/复现命令时要注明。
- **Read 大文件先 Grep 定位**——`Read` 单次默认最多 2000 行，塞满 context 更贵；先 `Grep` 出行号再 `Read --offset --limit`。
- **`allowed-tools` 是白名单，忘写就没有**——Skill / Subagent / Slash Command 的 frontmatter 里一旦写了 `allowed-tools`，未列入的一个都不给用，包括 `Read`。

## 参考

- Anthropic Docs · [Tools reference](https://code.claude.com/docs/en/tools-reference)（访问于 2026-07-28）
- Anthropic Docs · [Subagents · Available tools](https://code.claude.com/docs/en/sub-agents#available-tools)（访问于 2026-07-28）
- Anthropic Docs · [Permissions § Read-only commands](https://code.claude.com/docs/en/permissions#read-only-commands)（访问于 2026-07-28）

## 下一步

- 学 Shell 场景与安全边界 → [Bash 执行命令](./shell)
- 学如何让 Claude 派生 subagent 干重活 → [Dispatch Subagent](./dispatch-subagent)

## 如果你想

- 精细控制某个工具在项目里的可用范围 → [权限系统](../basics/permissions)
- 用 MCP 扩出更多工具 → [什么是 MCP](../mcp/what-is-mcp)
- 把工具能力打包给别人复用 → [什么是 Skill](/claude-code/skills/what-is-a-skill)
