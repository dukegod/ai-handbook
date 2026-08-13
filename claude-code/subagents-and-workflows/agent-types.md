---
title: Agent 类型清单
description: 'Claude Code subagent 完整配置——frontmatter 15 个字段、5 种 scope 优先级、工具白名单/黑名单、model 选择、内置 Explore/Plan/general-purpose 详解'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-04
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  subagentsDocs: 'https://code.claude.com/docs/en/sub-agents'
  accessedAt: 2026-08-04
---

# Agent 类型清单

> **TL;DR**：Subagent 是 `.claude/agents/*.md` 文件——YAML frontmatter 配置 + Markdown 正文当系统提示。必填 `name` + `description`，可选 `tools` / `model` / `permissionMode` / `mcpServers` / `hooks` / `memory` 等 15 个字段。5 种 scope 按优先级覆盖。

⏱ 预计阅读时间：9 分钟

## 你能在这里学到

- 内置 subagent 全清单与各自特性
- 自定义 subagent 文件写法与 15 个 frontmatter 字段
- 5 种 scope 优先级（managed > CLI > project > user > plugin）
- 工具控制：`tools` 白名单 vs `disallowedTools` 黑名单
- model / effort / permissionMode 的覆盖规则

## 前置

- 读过 [什么是 Subagent](./what-is-a-subagent)

## 一、内置 Subagent 全清单

| Agent | 模型 | 工具 | 何时用 |
| --- | --- | --- | --- |
| **Explore** | 继承（API 上限 Opus） | 只读 | 代码搜索、理解代码库；跳过 CLAUDE.md / git status |
| **Plan** | 继承 | 只读 | plan mode 下代码调研；同样跳过 CLAUDE.md / git status |
| **general-purpose** | 继承 | 全部 | 复杂多步任务（探索 + 修改） |
| **claude** | 继承 | 全部 | 兜底默认；background session 默认 agent |
| **claude-code-guide** | Haiku | — | 回答 Claude Code 功能问题 |
| **statusline-setup** | Sonnet | — | `/statusline` 配置时 |

**禁用内置**：

- 禁某个：`permissions.deny` 加 `Agent(Explore)`
- 全禁：`permissions.deny` 加 `Agent`
- 只禁 Explore/Plan：环境变量 `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1`（v2.1.198+）
- headless / SDK 全禁：`CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1`

## 二、5 种 Scope 优先级

同名 subagent 按优先级覆盖（高 → 低）：

| 优先级 | 位置 | scope |
| --- | --- | --- |
| 1（最高） | managed settings | 组织全员 |
| 2 | `--agents` CLI flag | 当前 session |
| 3 | `.claude/agents/` | 当前项目 |
| 4 | `~/.claude/agents/` | 你所有项目 |
| 5（最低） | plugin `agents/` | plugin 启用时 |

**项目级**适合跟代码库强相关的 subagent，提交到 git 团队共享。**用户级**适合个人偏好跨项目复用。

**Plugin subagent 限制**：不支持 `hooks` / `mcpServers` / `permissionMode` 字段（安全考虑），需要这些能力就复制到 `.claude/agents/`。

## 三、自定义 Subagent 文件

`.claude/agents/code-reviewer.md`：

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices. Use proactively after code changes.
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. Analyze the code and provide specific,
actionable feedback on quality, security, and best practices.
```

**正文 = 系统提示**。subagent 只收到这段提示 + 基本环境信息（工作目录等），**不收**完整 Claude Code system prompt。

**热更新**：Claude Code 监听 `agents/` 目录，改文件后几秒内生效、下次委派用新定义——无需重启。例外：新建 scope 的**第一个** agent 文件后需重启（watcher 只覆盖 session 启动时已存在的目录）。

## 四、Frontmatter 字段全表

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `name` | ✅ | 唯一标识（小写 + 连字符，不能含 `:`） |
| `description` | ✅ | 何时委派（Claude 看这个决定用不用） |
| `tools` | — | 可用工具白名单；省略 = 继承全部 |
| `disallowedTools` | — | 工具黑名单（先于 `tools` 应用） |
| `model` | — | `sonnet` / `opus` / `haiku` / `fable` / 完整 ID / `inherit`（默认） |
| `effort` | — | `low` / `medium` / `high` / `xhigh` / `max`，覆盖 session effort |
| `permissionMode` | — | `default` / `acceptEdits` / `auto` / `dontAsk` / `bypassPermissions` / `plan` |
| `maxTurns` | — | 最大 agentic 轮数 |
| `skills` | — | 启动时预载入的 skill（注入完整内容） |
| `mcpServers` | — | 该 subagent 专属 MCP server |
| `hooks` | — | 该 subagent 生命周期 hook |
| `memory` | — | `user` / `project` / `local` 持久记忆 |
| `background` | — | `true` = 总在后台跑 |
| `isolation` | — | `worktree` = 在临时 git worktree 里跑 |
| `color` | — | 任务列表显示颜色 |
| `initialPrompt` | — | 作为主 session agent 时自动提交的首轮 |

## 五、工具控制

**白名单**（只给这些工具）：

```yaml
tools: Read, Grep, Glob, Bash
```

**黑名单**（继承全部除了这些）：

```yaml
disallowedTools: Write, Edit
```

**MCP server 级**：

```yaml
disallowedTools: mcp__github      # 移除 github server 全部 tool
disallowedTools: mcp__*           # 移除所有 MCP tool
```

**限制可生成的 subagent 类型**（主线程 agent 用）：

```yaml
tools: Agent(worker, researcher), Read, Bash   # 只能生成 worker 和 researcher
```

**硬限制**：以下工具**所有 subagent 都没有**（即使列了也移除）：`AskUserQuestion` / `EnterPlanMode` / `ExitPlanMode`（plan 模式除外）/ `ScheduleWakeup` / `TaskOutput` / `Workflow` 等。

## 六、Model 选择

```yaml
model: haiku       # 低成本跑简单任务
model: sonnet      # 平衡
model: opus        # 高难度
model: fable       # 顶级专家
model: inherit     # 跟主线程（默认）
```

**解析顺序**（高 → 低）：

1. `CLAUDE_CODE_SUBAGENT_MODEL` 环境变量
2. 本次调用的 `model` 参数
3. frontmatter `model` 字段
4. 主线程模型

**v2.1.198+**：subagent 继承主线程的 extended thinking 配置——主线程开了思考，subagent 也开。

## 七、常用模式

### 只读研究 agent

```yaml
---
name: researcher
description: Research codebase patterns without modifying files
tools: Read, Grep, Glob
model: sonnet
---
```

### 带持久记忆的 reviewer

```yaml
---
name: code-reviewer
description: Reviews code, remembers patterns across sessions
memory: project
tools: Read, Grep, Glob, Bash
---
Review code and update your memory with recurring issues.
```

### Worktree 隔离的实验 agent

```yaml
---
name: experimenter
description: Try risky changes in an isolated worktree
isolation: worktree
tools: Read, Edit, Write, Bash
---
```

## 常见坑

**description 写太泛**——Claude 不知道何时委派。写「做什么 + 何时用 + use proactively」鼓励主动委派。

**`tools` 列了不存在的工具**——v2.1.208+ 直接拒绝启动 subagent，报错指出未解析项。检查拼写和工具名。

**plugin subagent 用了 `hooks` / `mcpServers` / `permissionMode`**——这三个字段在 plugin subagent 里被忽略。需要就复制到 `.claude/agents/`。

**新建 `~/.claude/agents/` 第一个文件后没生效**——watcher 只覆盖 session 启动时已存在的目录。重启 Claude Code。

**同名 subagent 被意外覆盖**——5 种 scope 按优先级覆盖。用 `/doctor` 查重名冲突。

## 参考

- [Anthropic · Create custom subagents](https://code.claude.com/docs/en/sub-agents)（访问于 2026-08-04）—— 完整字段与配置参考

## 下一步

- 多个 subagent 怎么编排 → [Workflow 编排](./workflow-orchestration) 🚧
- 常见多 agent 协作模式 → [多 Agent 常见模式](./multi-agent-patterns) 🚧

## 如果你想

- 回顾 subagent 概念 → [什么是 Subagent](./what-is-a-subagent)
- 看 Skill 与 Subagent 边界 → [Skill vs Command vs Agent](../skills/skills-vs-commands-vs-agents)
- 深入 hooks 配置 → [Hooks](../customization/hooks)

## 实战补充

**4 类生产级 agent 模板**（生产项目最常见的 agent 分工——取自团队实战经验）：

| Agent | 工具 | 职责 |
| --- | --- | --- |
| `frontend-reviewer` | Read, Grep, Glob, Search | Next.js + shadcn/ui 代码审查（read-only） |
| `architect` | Read, Grep, Glob, Write | 系统架构设计，输出 ADR 格式 |
| `tester` | Read, Grep, Glob, Bash | 写单测 + 跑测试 + 报覆盖率 |
| `security-guard` | Read, Grep, Glob | 安全审计（SQL 注入 / XSS / 密钥泄露） |

**完整 frontmatter + body 模板**见 [awesome-claude/agents.md](https://coding.jd.com/sz-fe/sz-2024/docs/awesome-claude/agents.md)（含 `autoSpawn: true` 配置 / 工具最小化 / 层级协作等 9 条 2026 优化技巧）。
