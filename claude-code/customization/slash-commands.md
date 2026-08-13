---
title: Slash Commands
description: 一个 markdown 文件就是一个 /xxx 快捷指令——Claude Code 里最低门槛的定制化
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-07-28
verifiedWith:
  claudeCode: 2.1.215
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/slash-commands'
  accessedAt: 2026-07-28
---

# Slash Commands

> **TL;DR**：Slash Command 就是你敲 `/name` 展开的一段 markdown 提示模板。**最简形态是一个文件**：`.claude/commands/name.md`。Anthropic 已把 custom commands 合入 Skills（同一套机制），`.claude/commands/` 目录继续兼容工作；一旦要带支持文件、让 Claude 自动触发、fork 到子上下文，就升级到 `.claude/skills/name/SKILL.md`。

⏱ 预计阅读时间：9 分钟

## 你能在这里学到

- 3 分钟做出你的第一个 `/xxx` 命令
- Slash Command / Skill / 内置命令三者的边界
- 文件放哪里、frontmatter 哪几个字段最重要
- 参数替换（`$ARGUMENTS` / `$0` / `$1`）与 `!` bash 动态注入
- 什么时候该升级到 Skill

## 前置

- 装好 Claude Code v2.1.199 或更高（`/a /b 参数` 多命令 stacking 从这版起可用）
- 读过 [权限系统](../basics/permissions)（`allowed-tools` 字段会用到）

## 3 分钟做出第一个命令

在项目根目录：

```bash
mkdir -p .claude/commands
```

写入 `.claude/commands/summarize.md`：

````md
---
description: 用两三条 bullet 概括当前 git diff
---

## 当前改动

!`git diff HEAD`

## 任务

用 2-3 条 bullet 概括上述改动，然后列出你注意到的风险（如缺少错误处理、硬编码、需要更新的测试）。
````

保存后在会话里输：

```text
/summarize
```

Claude Code 会**先跑一遍** `git diff HEAD`、把输出替换进模板、再把整段送给 Claude。你就有了一个「一键概括改动」的私人命令。

## 和内置命令 / Skill 的边界

- **内置命令**（`/help` / `/model` / `/config` / `/permissions`）—— 由 Claude Code 二进制直接实现，不是 markdown 模板，不能自定义。详见本文下方的「内置命令 vs 用户命令」段。
- **Bundled skill**（`/doctor` / `/code-review` / `/verify` / `/loop`）—— 随二进制打包、走 skill 机制，可被 `disableBundledSkills` 关掉。
- **Custom command**（`.claude/commands/xxx.md`）—— 你自己或团队写的 markdown 模板，只有敲 `/xxx` 才触发。**本文主要讲这个。**
- **Skill**（`.claude/skills/xxx/SKILL.md`）—— custom command 的超集：可以带支持文件目录、可以让 Claude 根据 `description` **自动**触发、可以 `context: fork` 进独立子上下文。

同名时的优先级：**enterprise > personal > project**；同层级下 **skill > command**。也就是说，如果你项目里同时有 `.claude/commands/deploy.md` 和 `.claude/skills/deploy/SKILL.md`，敲 `/deploy` 走的是 skill。

## 文件放哪里

| 层级 | 路径 | 谁能用 |
| --- | --- | --- |
| 项目 | `.claude/commands/xxx.md` 或 `.claude/skills/xxx/SKILL.md` | 只这个项目（要 commit 进 git） |
| 个人 | `~/.claude/commands/xxx.md` 或 `~/.claude/skills/xxx/SKILL.md` | 你所有项目 |
| 企业 | managed settings 指定的目录 | 组织全员 |
| 插件 | 安装的插件 `skills/` 目录 | 装了该插件的地方 |

**敏感 prompt**（含密钥、内部 URL、爬虫策略等）放个人级，或在项目 `.gitignore` 里排除；否则 commit 的一瞬间就外泄了。

## Frontmatter 关键字段

只有 `description` **推荐**填，其余全部可选。

| 字段 | 作用 |
| --- | --- |
| `description` | 敲 `/` 时的自动补全说明；Skill 自动触发的**决策依据** |
| `argument-hint` | 补全时的参数提示，如 `[issue-number]` |
| `allowed-tools` | 该命令期间**免询问**的工具白名单，例：`Bash(gh *) Read` |
| `model` | 该命令期间切换到指定模型（`fable` / `opus` / `sonnet` / `haiku`），下一轮消息后恢复 |
| `disable-model-invocation` | Skill 才用；`true` 时禁止 Claude 自动触发（回归纯手动） |

`allowed-tools` 的授权**只覆盖触发命令的那一轮**——你发下一条消息后立即失效，不会持久。想彻底放行某工具走 `/permissions`。

## 参数替换

`$ARGUMENTS` 拿到全部参数：

````md
---
description: 修复一个 GitHub issue
argument-hint: [issue-number]
---

修复 GitHub issue $ARGUMENTS，遵循我们的编码规范。
````

`/fix-issue 42` → `$ARGUMENTS` 变成 `42`。

位置参数用 `$0` / `$1` / `$2`（0-based）或等价的 `$ARGUMENTS[0]`：

````md
将 $0 组件从 $1 迁移到 $2。
````

`/migrate SearchBar React Vue` → 三个位置各就各位。多词参数用双引号包起来：`/migrate "primary button" React Vue` → `$0 = primary button`。

**没有匹配到的位置**（例如只传 2 个参数却用了 `$3`）—— **保留字面**不替换。命名参数（`arguments:` 声明）没匹配到则展开为空字符串。想在正文里写字面量 `$1.00`，前面加 `\` 转义：`\$1.00`。

## 动态注入：`!` bash

行首或空白后紧跟的 `` !`<cmd>` ``，在 prompt 送给 Claude **之前**运行 shell，把 stdout 替换进模板：

````md
## 当前分支

!`git branch --show-current`

## 未提交改动

```!
git status --short
git diff --stat
```
````

多行命令用 `` ```! `` 起头的 fenced code block。关键行为：

- 是 **preprocessing**——Claude 看到的是命令输出，不是命令本身；不算 Claude 用了 `Bash` 工具
- 只匹配**行首或空白后**的 `!`；`KEY=!`cmd`` 里的 `!` 是普通字符
- 每处命令**只跑一次**，输出不再递归展开占位符
- managed settings 里 `disableSkillShellExecution: true` 能全局关掉（用输出替换为 `[shell command execution disabled by policy]`）

## 何时该升级到 Skill

维持在 `.claude/commands/xxx.md` **够用的时候**：一段模板、几个参数、一个文件装得下。

**升级到 `.claude/skills/xxx/SKILL.md`** 的信号：

- 需要**支持文件**（脚本 / 模板 / 长参考文档）—— skill 是目录，能装多个文件，用 `${CLAUDE_SKILL_DIR}` 引用
- 想让 Claude 根据 `description` **自动触发**（不再要求用户显式敲 `/xxx`）
- 想 `context: fork` 到独立子上下文（skill 内容作为子代理的 system prompt，不占主对话 token）
- 想精细指定 `model` / `effort` / `agent`（skill frontmatter 支持更多字段）

Skill 完整机制见 [什么是 Skill](/claude-code/skills/what-is-a-skill) 🚧。

## 常见坑

- **`description` 太模糊** → 升级到 Skill 后 Claude 判断不了何时触发，只能靠用户显式敲
- **`allowed-tools` 是白名单，忘写 `Read` Claude 就得每次请求**——不写这字段 = 走 `/permissions` 默认规则；一旦写就只有列内的免询问
- **敏感 prompt 被 commit**：`.claude/commands/` 项目级默认会被 git 追踪，含密钥或内部链接前先看 `.gitignore`
- **占位符没匹配**：`$3` 只传了 2 个参数时**保留原字面**（会以 `$3` 出现在 prompt 里），不是空字符串
- **body 里 `[text](/abs/path)` 会被当链接而不是路径**——想让 Claude 读某个绝对路径的文件，直接用行内代码 `` `/abs/path` `` 或写一句 "Read the file at `/abs/path`"

## 参考

- Anthropic Docs · [Extend Claude with skills](https://code.claude.com/docs/en/slash-commands)（访问于 2026-07-28，页面本身现在讲 Skills；custom commands 已并入）
- Anthropic Docs · [Commands reference](https://code.claude.com/docs/en/commands)（访问于 2026-07-28，内置命令与 bundled skill 全表）

## 下一步

- 学 Skill 完整机制 → [什么是 Skill](/claude-code/skills/what-is-a-skill) 🚧
- 学生命周期钩子 → [Hooks](./hooks) 🚧

## 如果你想

- 看内置命令与 bundled skill 全表 → 本文「内置命令 vs 用户命令」段
- 精细控制某命令能碰哪些工具 → [权限系统](../basics/permissions)
- 把命令打包分发给团队 → [Plugins Marketplace](/claude-code/skills/plugins-marketplace) 🚧
