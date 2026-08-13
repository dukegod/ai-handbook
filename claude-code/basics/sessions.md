---
title: 会话 Session
description: Session 生命周期、5 种启动/恢复方式、picker 快捷键、Fork/Branch、context 管理与存储路径
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-07-28
verifiedWith:
  claudeCode: 2.1.215
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/sessions'
  accessedAt: 2026-07-28
---

# 会话 Session

> **TL;DR**：Session 是 Claude Code 的**基本工作单位**——一次绑定项目目录的对话，自动写盘。命名后可恢复、可分叉、可跨 worktree 切换。理解 Session，你就理解了「Claude 记得什么、忘了什么、能不能接上之前的事」。

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- Session 的完整生命周期
- **5 种启动 / 恢复方式**的具体行为
- Session picker 的 8 个键盘快捷键
- Fork（`/branch`）与继续（`--continue`）的区别
- 会话与 CLAUDE.md / Auto-compact 的边界
- 会话文件的存储路径与保留策略

## 前置

- 装好 Claude Code、跑过 [第一次对话](/getting-started/first-conversation)

## 一、Session 是什么

**Session = 一次绑定项目目录的对话记录**。Claude Code 在会话进行时**自动保存**到本地，你退出、`/clear`、崩溃后都能回来。

关键属性：

- 存**目录**级，不是分支级——切 git 分支后 Claude 看新分支的文件，但对话记忆保留
- 每一条消息、每次工具调用与结果都被写入 JSONL 文件
- 默认无名，Claude 会用 Haiku-class 模型给一个 AI title；你可自己命名替换

## 二、5 种启动与恢复方式

| 命令 | 行为 |
| --- | --- |
| `claude` | 启动新会话（当前目录） |
| `claude --continue` / `-c` | 恢复**当前目录**最近一次会话 |
| `claude --resume` / `-r` | 打开交互 [Session picker](#三session-picker) |
| `claude --resume <name>` | 直接恢复指定名字的会话 |
| `claude --from-pr <number>` | Picker 过滤到关联某 PR 的会话 |
| `/resume`（会话内） | 会话内切到另一个会话 |

### 恢复时保留什么

- 完整对话历史（含工具调用与结果）
- 模型（除非 retired / 有 `--model` flag / 特定 provider）
- Agent（如启动时指定了 `--agent`）
- 权限模式（**`plan` 与 `bypassPermissions` 不恢复**）
- Active goal 与未到期的 scheduled tasks

### 恢复时**不**保留什么

需要在恢复时重传：`--mcp-config` / `--settings` / `--plugin-dir` / `--fallback-model` / `--add-dir` 加的目录。

`settings.json`、`settings.local.json` 这类静态文件会重读，不用手动传。

## 三、Session picker

`claude --resume` 或会话内 `/resume` 打开交互 picker。**10 个键盘快捷键必须掌握**：

| 快捷键 | 行为 |
| --- | --- |
| `↑` / `↓` | 上下导航 |
| `→` / `←` | 展开 / 折叠分组会话（fork / branch 后同源会话会合并成一行，按 `→` 展开） |
| `Enter` | 恢复高亮会话 |
| `Space` | 预览会话内容（部分终端把 `Space` 当粘贴，用 `Ctrl+V` 备选） |
| **`Ctrl+R`** | 重命名当前高亮 |
| `/` 或字符 | 进搜索模式（可粘 GitHub / GitLab PR/MR URL 找到创建它的会话） |
| **`Ctrl+A`** | 显示**所有项目**的会话（再按回到当前 repo） |
| **`Ctrl+W`** | 显示当前 repo 的**所有 worktree**（多 worktree 才有） |
| `Ctrl+B` | 只看当前 git 分支的会话 |
| `Esc` | 退出 picker |

Picker 每行显示：**会话名** → AI title → conversation summary → 首个 prompt，加上最后活动时间、git 分支、文件大小。

## 四、给会话起名

命名后可以 `--resume <name>` 直接跳、也在 picker 里一眼找到：

| 时机 | 方法 |
| --- | --- |
| 启动时 | `claude -n auth-refactor` |
| 会话中 | `/rename auth-refactor` |
| Picker 里 | 高亮 → `Ctrl+R` |
| Plan Mode 接受时 | 自动从 plan 内容生成（除非你已命名） |

> ⚠️ AI 生成的 title 与默认显示名（如 `my-app-3f`）**都不能当 resume handle**——只有你显式命名（`-n` / `/rename` / `Ctrl+R`）的名字才能用 `--resume <name>` 直接恢复。

## 五、Fork：分叉一个会话

**Fork 复制历史到一个新 session ID，你切进新分支，原会话不变**。用于"想试另一个方向但保留当前路径"。

会话内：

```text
/branch try-streaming-approach
```

命令行：

```bash
$ claude --continue --fork-session
```

**Fork 保留**：对话历史（复制到 fork 点）、当前会话内的"允许一次"权限授权（同进程）、后台跑着的 subagent 与 Bash 命令。

> ⚠️ 如果你在**两个 terminal 里 resume 同一个会话**（未 fork），双边消息**会交织写入同一 transcript**，通常会乱掉——想并行任务请 `/branch` 或用 [Worktree 隔离](/claude-code/advanced/worktree)。

## 六、Context 管理：/clear vs /compact

会话内三个命令控制上下文（不离开会话）：

- **`/clear`** — 清空 context 开新对话；老对话保留在文件，可 `/resume` 找回。会话名（若你命名过）保留，AI 生成的 title 不保留
- **`/compact [instructions]`** — 用摘要替换历史，可指定 focus（如 `/compact focus on API changes`）
- **`/context`** — 显示当前哪些内容在占 context

深入 auto-compact 见 [心智模型 · 上下文用完了怎么办](/getting-started/mental-model#上下文用完了怎么办auto-compact)。

## 七、导出会话

```text
/export                     # 打开菜单：复制到剪贴板 / 保存为文件
/export my-refactor.md      # 直接写到文件
```

对**脚本化**处理会话数据，见 [Headless / CI 模式](/claude-code/advanced/headless)。

## 八、存储路径与保留策略

默认路径：

```
~/.claude/projects/<project>/<session-id>.jsonl
```

`<project>` = 工作目录路径，非字母数字字符替换为 `-`。每行是一个 JSON 对象（消息 / 工具调用 / 元数据）。

**配置项**：

| 想做什么 | 配 |
| --- | --- |
| 迁移会话存储位置 | 环境变量 `CLAUDE_CONFIG_DIR` |
| 修改保留天数（默认 30） | `settings.json` 里 `cleanupPeriodDays` |
| 全局关闭 transcript 写入 | 环境变量 `CLAUDE_CODE_SKIP_PROMPT_HISTORY` |
| Headless 单次关闭 | `claude -p --no-session-persistence` |

> ⚠️ JSONL 格式是 **Claude Code 内部结构，会随版本变**——想 parse 请用 `/export` 或 [脚本接口](/claude-code/advanced/headless)，别直接读文件。

## 常见坑

**`--continue` 加载了错的会话**

`-c` 恢复的是**当前目录**最近一次会话。切换项目后要么先 `cd`，要么用 `--resume <name>` 或 `-r` 打 picker 精准选。

**`/clear` 不删除会话文件**

`/clear` 只清 context，会话仍在 `~/.claude/projects/` 里。想彻底删要么手动 `rm`，要么等 `cleanupPeriodDays` 到期。

**AI title 不是 resume handle**

只有显式命名（`-n` / `/rename` / `Ctrl+R`）的名字才能 `--resume <name>` 直接恢复。AI title 只在 picker 里显示。

**两个 terminal 同时 resume 同一 session**

消息会交织写入 transcript，通常会乱。想并行请用 `/branch` 或 [worktree](/claude-code/advanced/worktree)。

**Auto-compact 后早期指令丢失**

Auto-compact 会砍掉最老的工具输出和摘要化老对话——**长期规则要写进 [CLAUDE.md](./claude-md)，别指望对话历史长期记住**。

## 参考

- [Anthropic Docs · Manage sessions](https://code.claude.com/docs/en/sessions)（访问于 2026-07-28）
- [Anthropic Docs · Context window](https://code.claude.com/docs/en/context-window)（访问于 2026-07-28）
- [Anthropic Docs · Checkpointing](https://code.claude.com/docs/en/checkpointing)（访问于 2026-07-28）
- [Anthropic Docs · Worktrees](https://code.claude.com/docs/en/worktrees)（访问于 2026-07-28）

## 下一步

- 让稳定上下文在会话间自动加载 → [CLAUDE.md 项目记忆](./claude-md)

## 如果你想

- 深入 Auto-compact 机制 → [心智模型 · 上下文用完了怎么办](/getting-started/mental-model#上下文用完了怎么办auto-compact)
- 并行多会话 → [Worktree 隔离](/claude-code/advanced/worktree)
- Headless 脚本化调用 → [Headless / CI 模式](/claude-code/advanced/headless)
- 查所有会话内 slash 命令 → [定制与扩展 · Slash Commands](/claude-code/customization/slash-commands)
