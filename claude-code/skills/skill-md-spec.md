---
title: SKILL.md 规范
description: SKILL.md 的完整 frontmatter 字段、命令名解析、字符串替换与动态注入——Claude Code Skills 的机器可读参考
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-07-29
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/skills'
  accessedAt: 2026-07-29
---

# SKILL.md 规范

> **TL;DR**：`SKILL.md` = **YAML frontmatter** + **markdown body**。frontmatter 决定 Claude Code **怎么加载**这个 skill（触发、权限、运行位置），body 决定 Claude **看到之后做什么**。本页是**参考文档**：完整字段表、命令名解析规则、`$ARGUMENTS` 与 `${CLAUDE_SKILL_DIR}` 等替换语法、`` !`cmd` `` 动态注入。想先建立心智，回 [什么是 Skill](./what-is-a-skill)。

⏱ 预计阅读时间：作为速查用

## 前置

- 读过 [什么是 Skill](./what-is-a-skill) — 熟悉 skill 的加载模型与生命周期
- Claude Code v2.1.218+（多个字段的最新语义依赖此版本）

## 一、最小完整例子

```yaml
---
description: 分析当前 git diff，用 2-3 条 bullet 概括并列出风险。用户说"这次改了啥"或需要 commit message 时用。
---

## Current changes

!`git diff HEAD`

## Instructions

用 2-3 条 bullet 概括上面的改动，然后单列一段"风险"标注可能缺失的错误处理、硬编码值、需要跟改的测试。若 diff 为空，明确说"没有未提交改动"。
```

三处关键：`description` 决定 Claude 自动触发时机；`` !`git diff HEAD` `` 在 skill 内容送到 Claude 之前**先执行**并把输出替换进来；body 用**祈使句 + standing instruction**（一旦加载会驻留整段会话）。

## 二、Frontmatter 全字段

所有字段都是可选；**只 `description` 强推荐**（决定 Claude 何时自动触发）。v2.1.218+ 起 boolean 字段接受 `yes/no/on/off/1/0` 与大小写任意的 `true/false`，早期版本仅识别 `true/false`。

### 身份与文案

| 字段 | 类型 | 作用 |
| --- | --- | --- |
| `name` | string | 列表里的显示名。**personal / project skill 里不改命令名**（命令名仍等于目录名）；plugin skill 里替换命令的最后一段 |
| `description` | string | Claude 用它判断何时自动触发。合计 `description + when_to_use` 上限 **1,536 字符**，超出被截断——**把最重要的触发场景放最前** |
| `when_to_use` | string | 附加触发提示（触发短语、示例请求）。计入 1,536 字符预算 |
| `argument-hint` | string | 自动补全时显示的参数提示，如 `[issue-number]` |
| `arguments` | string \| list | 命名位置参数，用于 `$name` 替换。空格分隔或 YAML 列表 |

### 触发控制

| 字段 | 类型 | 作用 |
| --- | --- | --- |
| `disable-model-invocation` | bool | `true` = 只允许你敲 `/name`，Claude 不能自动触发；同时**从 subagent 预加载中移除**，且 v2.1.196+ 起也阻止 scheduled task 以此 skill 为 prompt。默认 `false` |
| `user-invocable` | bool | `false` = 只允许 Claude 自动调，`/` 菜单里不出现。适合"背景知识"型 skill（如 `legacy-system-context`）。默认 `true` |
| `paths` | string \| list | Glob 模式，限定**仅在编辑匹配文件时**才自动加载。同 `paths:` scoped rule 语法 |

### 工具与权限

| 字段 | 类型 | 作用 |
| --- | --- | --- |
| `allowed-tools` | string \| list | 触发本 skill 的**那一 turn** 内自动放行的工具，无需询问权限。**下一次用户发消息时清除**——再次触发要再放行。空格 / 逗号分隔或 YAML 列表 |
| `disallowed-tools` | string \| list | 触发本 skill 期间从可用工具池**移除**的工具。用于"背景循环 skill 不该问用户"这种场景。同样 next-message 后清除 |

### 运行环境

| 字段 | 类型 | 作用 |
| --- | --- | --- |
| `model` | string | 触发时切模型；本 turn 结束后恢复 session 模型。接受 `/model` 的值或 `inherit` |
| `effort` | `low` / `medium` / `high` / `xhigh` / `max` | 触发时切 effort；本 turn 后恢复 |
| `context` | `fork` | 在 forked subagent 里跑，skill body 成为 subagent 的 prompt。详见 [什么是 Subagent](/claude-code/subagents-and-workflows/what-is-a-subagent) 🚧 |
| `agent` | string | `context: fork` 时指定 subagent 类型（`Explore` / `Plan` / `general-purpose` / 自定义）。默认 `general-purpose` |
| `background` | bool | 仅 `context: fork` 有效。`false` = 阻塞当前 turn 等 subagent 结果；`true`（默认）= 后台跑。v2.1.218+ 起可用 |
| `hooks` | object | 绑定到本 skill 生命周期的 hooks 配置 |
| `shell` | `bash` / `powershell` | `` !`cmd` `` 内联命令用哪种 shell。默认 `bash`；PowerShell 需 Windows 或 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` |

## 三、目录布局与命令名

Skill 目录支持四级作用域：

| 位置 | 路径 | 覆盖对象 |
| --- | --- | --- |
| Enterprise | 见 [managed settings](https://code.claude.com/docs/en/settings#settings-files) | 组织全员，最高优先级 |
| Personal | `~/.claude/skills/<name>/SKILL.md` | 你所有项目 |
| Project | `<repo>/.claude/skills/<name>/SKILL.md` | 当前项目 |
| Plugin | `<plugin>/skills/<name>/SKILL.md` | 启用该 plugin 的场景 |

**同名优先级**：enterprise > personal > project > bundled。Plugin skill 走 `plugin:skill` 命名空间不与前三者冲突。

**嵌套 skill**（v2.1.203+）：`apps/web/.claude/skills/deploy/SKILL.md` 在编辑 `apps/web/` 文件时自动加载；若与 project-root 同名 `deploy`，nested 那份挂在 `/apps/web:deploy`，`/deploy` 仍是 project-root 版本，但 Claude 会看到"目录限定变体"列表并按当前工作路径自动选择。

**命令名从哪来**：

| 位置 | 命令名来源 | 示例 |
| --- | --- | --- |
| `~/.claude/skills/` / `.claude/skills/` | 目录名 | `.claude/skills/deploy-staging/SKILL.md` → `/deploy-staging` |
| `.claude/commands/*.md` | 文件名去后缀 | `.claude/commands/deploy.md` → `/deploy` |
| Plugin `skills/` 子目录 | frontmatter `name` 或目录名，带 plugin 前缀 | `my-plug/skills/review/SKILL.md` → `/my-plug:review` |
| Plugin 根 `SKILL.md` | frontmatter `name`（无则 plugin 目录名） | `my-plug/SKILL.md` + `name: review` → `/my-plug:review` |

## 四、字符串替换

| 变量 | 展开为 |
| --- | --- |
| `$ARGUMENTS` | 调用时传的**全部参数字符串**。skill body 若不写 `$ARGUMENTS`，Claude Code 追加一行 `ARGUMENTS: <值>` |
| `$ARGUMENTS[N]` / `$N` | 第 N 个位置参数（0-based）。多词值用引号包起来当一个参数 |
| `$name` | `arguments: [issue, branch]` 声明后 `$issue` / `$branch` 按声明顺序对应位置 |
| `${CLAUDE_SESSION_ID}` | 当前 session ID，用于日志或 session 相关文件命名 |
| `${CLAUDE_EFFORT}` | 当前 effort 档位（`low` / `medium` / `high` / `xhigh` / `max`；ultracode 报 `xhigh`） |
| `${CLAUDE_SKILL_DIR}` | 当前 skill 目录绝对路径。用于 `` !`${CLAUDE_SKILL_DIR}/scripts/x.sh` `` 引用同目录脚本 |
| `${CLAUDE_PROJECT_DIR}` | 项目根目录，与 hooks / MCP server 收到的一致（v2.1.196+） |

`${CLAUDE_SKILL_DIR}` 与 `${CLAUDE_PROJECT_DIR}` 在 **body 与 `allowed-tools` 两处都会展开**（v2.1.129+）——这让 skill 能通过 `Bash(${CLAUDE_SKILL_DIR}/scripts/x.sh *)` 精确放行自己捆绑的脚本而不放行任意 `Bash`。

要在文本里写字面 `$0` / `$ARGUMENTS`，用 `\$` 转义。

## 五、动态注入：`` !`cmd` ``

`` !`<command>` `` 语法在 skill body **送到 Claude 之前**先执行，用命令输出替换占位符。是**预处理**，不是 Claude 执行的动作。

- 只在**行首或空白后**出现的 `!` 才被识别；`KEY=!\`x\`` 里的 `!` 保持字面量
- 输出**作为纯文本插入**，不会再被扫一遍替换——命令输出不能夹带另一个 `` !`cmd` ``
- 多行命令用围栏代码块 ```` ```! ```` 开头
- 全局关闭：`settings.json` 里 `"disableSkillShellExecution": true`，命令被替换为 `[shell command execution disabled by policy]`

**触发限制**：`` !`cmd` `` 只有在 skill **被触发**时才跑一次；单纯 description 常驻到 context 时不会跑。

## 六、YAML 解析细节与常见坑

**description 里含反引号 / 冒号 / `{}[]#&*!|>%@` 用单引号包**——否则 YAML 解析失败，Claude Code **加载空 metadata 的 skill body**，`/name` 还能跑但 Claude 没 description 无法自动触发。`--debug` 能看到 parse error。

**description 过长被截断**——总预算按 model context window 的 **1%** 缩放（v2.1.196+ 起 `/context` 的 Skills 行反映**截断后**大小）。想给关键 skill 保留完整描述：

- 把**最重要的触发场景放在 `description` 最前**
- 用 `skillOverrides` 把不常用的 skill 设 `"name-only"`（`.claude/settings.local.json`）
- 或调大预算：`skillListingBudgetFraction: 0.02`（2%）或 `SLASH_COMMAND_TOOL_CHAR_BUDGET`

**`name` 不改 personal / project skill 的命令名**——命令名总是目录名。要改命令名就改目录名（或用 plugin 承载）。

**`allowed-tools` 只护当前 turn**——下次用户发消息后自动清除。想全 session 放行，加到 `permissions.allow`。

**boolean 值 `true` / `false` 是唯一保底写法**——v2.1.218+ 才接受 `yes` / `on` / `1`；跨版本共享的 skill 库仍用 `true` / `false`。

## 七、字段速查（按用途分）

- **想让 Claude 自动触发** → `description` + 可选 `paths`
- **想让副作用 skill 只有你能敲** → `disable-model-invocation: true`
- **想让 Claude 后台看的领域知识不占 `/` 菜单** → `user-invocable: false`
- **想跑长任务不阻塞** → `context: fork` + `background: true`
- **想放行自己捆绑的脚本** → `allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/x.sh *)`
- **想深思考** → body 里写 `ultrathink` 关键词 或 `effort: max`

## 参考

- [Anthropic Docs · Extend Claude with skills](https://code.claude.com/docs/en/skills)（访问于 2026-07-29）
- [Anthropic Docs · Frontmatter reference](https://code.claude.com/docs/en/skills#frontmatter-reference)（访问于 2026-07-29）
- [Anthropic Docs · Available string substitutions](https://code.claude.com/docs/en/skills#available-string-substitutions)（访问于 2026-07-29）
- [Agent Skills 开放标准](https://agentskills.io)（访问于 2026-07-29）—— 多 AI 工具兼容的 skill 规范

## 下一步

- 学怎样写让 Claude 恰好触发的 description → [写好触发描述](./writing-triggers) 🚧
- 立刻上手写一个 → [写你的第一个 Skill](./custom-skill) 🚧

## 如果你想

- 回到概念全景 → [什么是 Skill](./what-is-a-skill)
- 弄清 Skill / Command / Subagent 的边界 → [Skill vs Command vs Agent](./skills-vs-commands-vs-agents) 🚧
- 看官方与生态里现成的 Skill → [内置 Skills 一览](./built-in-skills) 🚧
