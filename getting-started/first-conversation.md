---
title: 第一次对话
description: '从 `claude` 命令到第一次可用回答；含权限模式、必备 slash 命令与 Shift+Tab 切换'
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-07-28
verifiedWith:
  claudeCode: 2.1.215
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/quickstart'
  accessedAt: 2026-07-28
---

# 第一次对话

> **目标**：从 `claude` 命令到 5 分钟内产出第一次可用的对话；理解三种启动方式、必备命令与权限模式的切换。

⏱ 预计阅读时间：5 分钟

## 你将做到

- ✅ 启动 Claude Code 并进入交互模式
- ✅ 让 Claude 读懂你的项目
- ✅ 完成一次真实改动（比如加个函数）
- ✅ 掌握 `/help` / `/clear` / `/exit` 与 Shift+Tab 四条基本操作

## 前置

- 已装好 Claude Code、通过认证 → [安装与认证](./installation)
- 有一个可以练手的代码项目

## 第 1 步：进入项目并启动

```bash
$ cd /path/to/your/project
$ claude
```

启动后 Claude Code 会在提示符上方显示 **版本 / 当前模型 / 工作目录**，然后等你输入。

> 💡 Claude Code 会按需自动读你的文件——**不用**手动把整个仓库塞给它。

## 第 2 步：让 Claude 读懂项目

先了解、再动手。用自然语言：

```text
这个项目是做什么的？
```

Claude 会挑关键文件读、给一段概述。也可以更具体：

```text
用了什么技术栈？主入口在哪？
解释一下目录结构
```

## 第 3 步：让它做一件事

从最小改动开始：

```text
在主文件里加个 hello world 函数
```

Claude 会：

1. 定位合适的文件
2. **给你看要改的地方**（diff）
3. 询问你是否同意——**默认权限模式下每一次改动都会问**
4. 你确认后执行 Edit

### Permission Mode 与 Shift+Tab

Claude Code 有 6 种权限模式；`Shift+Tab` 在**默认循环**里的三种间切换：`default` → `acceptEdits` → `plan`。

| 模式 | 行为 | 什么时候用 |
| --- | --- | --- |
| **default**（v2.1.200+ 起 UI 显示为 **Manual**） | 只读；写/命令都要问你 | 陌生代码 / 刚上手不放心 |
| **acceptEdits** | 自动接受文件编辑与常见文件系统命令（`mkdir` / `touch` / `mv` 等） | 熟悉的操作、快速迭代 |
| **plan** | 只探索 + 提议，不改文件 | 复杂改动前的方案审阅（详见 [Plan Mode](/claude-code/basics/plan-mode)） |

另有三种模式默认**不在**循环里，需要显式启用后才能切到：**auto**（后台安全检查、账号需满足条件）、**dontAsk**（只允许预授权工具，适合 CI）、**bypassPermissions**（跳过全部检查，仅隔离容器/VM 使用）。系统提示行会显示当前模式。深度权限规则见 [权限系统](/claude-code/basics/permissions)。

## 会话内的三种输入

Claude Code 在同一个提示符里接受三种输入：

- **自然语言**：直接说，中英文都行
- **`/slash` 命令**：以 `/` 开头触发内置或自定义命令；输入 `/` 就有补全
- **`@path` 文件引用**：`@src/index.ts` 明确让 Claude 关注某个文件

## 常用 slash 命令

按官方 [Quickstart · Essential commands](https://code.claude.com/docs/en/quickstart) 与 [Commands reference](https://code.claude.com/docs/en/commands)：

| 命令 | 作用 |
| --- | --- |
| `/help` | 列全部可用命令与 Skill |
| `/clear` | 清对话历史（保留会话文件，见 [会话](/claude-code/basics/sessions)） |
| `/status` | 查看当前 provider、模型、代理配置 |
| `/model` | 切换模型（Opus / Sonnet / Haiku） |
| `/config` | 打开配置面板 |
| `/login` | 切账号或重新认证 |
| `/resume` | 恢复某次历史会话 |
| `/exit` | 退出 |

完整清单见 [定制与扩展 · Slash Commands](/claude-code/customization/slash-commands)。

## 三种启动方式

大多数时候用交互模式，另外两种适合脚本化：

```bash
$ claude
# 交互模式（本页主要讲的）

$ claude "帮我 review 一下最近的 3 个 commit"
# 带初始提示进入交互模式：先按 prompt 干活，之后你可以继续追问

$ claude -p "解释这段代码" --output-format json
# Headless / 一次性：给完输出就退出，适合 CI 与 shell pipe

$ claude -c
# 继续当前目录最近一次会话

$ claude -r
# 恢复某次历史会话（进入交互后会给你选）
```

## 键盘小抄

- `Tab` 补全命令 / 文件路径
- `↑` / `↓` 翻输入历史
- **`Shift+Tab` 循环权限模式**（很常用）
- `/` 打开命令 & Skill 补全菜单
- `Ctrl+C` 中断当前生成
- `Ctrl+D` 或 `/exit` 退出会话

## 常见坑

**权限第一次询问时误选 deny**

Claude Code 会记住你的选择，之后在该工具上反复失败。改法：用 `/permissions` 交互调整，或改 `~/.claude/settings.json`。详见 [权限系统](/claude-code/basics/permissions)。

**忘了配 API Key 就 `claude`**

首次进入时若既没登录、也没设 `ANTHROPIC_API_KEY`，会卡在认证。按 [安装与认证 · 方式 A/B](./installation#第-3-步完成认证) 完成后再回来。

**`-c` 加载了错的会话**

`--continue` 加载的是**当前目录**最近的会话——切到别的目录会加载错的。想接前一个项目请用 `-r` 或 `/resume` 从列表选。

**Claude 一直"读文件"、不出结果**

首次跑大项目时 Claude 常先 Read/Grep 探索——耐心等 30–60 秒。想省成本可切到 [Plan Mode](/claude-code/basics/plan-mode) 先出方案再放行。

## 参考

- [Anthropic Docs · Quickstart](https://code.claude.com/docs/en/quickstart)（访问于 2026-07-28）
- [Anthropic Docs · Permission modes](https://code.claude.com/docs/en/permission-modes)（访问于 2026-07-28）
- [Anthropic Docs · Commands reference](https://code.claude.com/docs/en/commands)（访问于 2026-07-28）

## 下一步

- 建立对 Claude Code 内部行为的直觉 → [心智模型](./mental-model)

## 如果你想

- 查所有 CLI Flag → [参考 · CLI Flags](/reference/cli-flags)
- 查所有 Slash Commands → [定制与扩展 · Slash Commands](/claude-code/customization/slash-commands)
- 用 Plan Mode 探索复杂改动 → [Plan Mode](/claude-code/basics/plan-mode)
- 看一个真实的端到端案例 → [Cookbook · 第一个真实任务](/cookbook/first-real-task)
