---
title: 什么是 Skill
description: 声明式扩展——Claude 自己决定何时用的能力包
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-08-08
verifiedWith:
  claudeCode: 2.1.220
  model: claude-opus-4-8
  officialDocs: 'https://code.claude.com/docs/en/skills'
  accessedAt: 2026-08-08
---

# 什么是 Skill

> **TL;DR**：Skill = 一个 `SKILL.md`（含 `description`）+ 可选的支持文件目录。**Claude 读到你的问题、根据 description 判定「这是它该处理的事」时自动加载**。类比：Slash Command 是你按按钮，Skill 是 Claude 看情况自己伸手。它是 Claude Code 定制化里**最声明式**的一档——你只描述能力，不写触发时机。

⏱ 预计阅读时间：9 分钟

## 你能在这里学到

- Skill 与 Slash Command / Subagent / Hook 的边界
- Skill 的两阶段加载（description 常驻 vs body 按需）
- 支持文件目录如何降低 token 成本
- 触发方式的三种控制：默认双向 / 只让 Claude / 只让人
- Skill 生命周期与 auto-compaction 的关系
- 什么时候该写、什么时候别写

## 前置

- 装好 Claude Code v2.1.202+（Skill 重复调用去重从这版起可用）
- 读过 [Slash Commands](../customization/slash-commands)（Skill 是它的超集）

## 一句话定义

**Skill 是一个目录**，最少包含一个 `SKILL.md`：

```text
my-skill/
├── SKILL.md           # 必需：description + 指令主体
├── reference.md       # 可选：详细参考，Claude 按需读
├── examples/          # 可选：示例
└── scripts/
    └── helper.py      # 可选：Claude 会 Bash 执行的脚本
```

`SKILL.md` frontmatter 的 `description` 字段是**触发机制的核心**：Claude 每一轮会看到你项目里所有 skill 的 description（**不是全文**），据此判断这一轮该不该调进来。

```yaml
---
description: 分析 git diff，用 2-3 条 bullet 概括并列出风险。用户说"这次改了啥"或需要 commit message 时用。
---

## 任务
...（Claude 触发这个 skill 才看到的部分）...
```

## 触发方式的三档

Skill 默认**双向可触发**：用户敲 `/name` 或 Claude 觉得适用时都能拉起。两个 frontmatter 字段可以收窄：

| 配置 | 用户能敲 `/name` | Claude 能自动调 | description 是否常驻 |
| --- | --- | --- | --- |
| 默认 | ✅ | ✅ | ✅ |
| `disable-model-invocation: true` | ✅ | ❌ | ❌（省 token） |
| `user-invocable: false` | ❌ | ✅ | ✅ |

- `disable-model-invocation` 用于有**副作用**的操作（`/commit`、`/deploy`、`/send-slack`）——你不希望 Claude 觉得代码差不多就自己按按钮
- `user-invocable: false` 用于**背景知识**（如 `legacy-system-context`），是 Claude 该知道的、但用户没必要主动敲的东西

## 边界：Skill vs Slash Command vs Subagent vs Hook

| | 触发者 | 运行上下文 | 生命周期 |
| --- | --- | --- | --- |
| Slash Command（`.claude/commands/`） | **用户主动**敲 `/name` | 当前会话 | 一次性 prompt 展开 |
| Skill | **用户或 Claude** | 当前会话（inline）或子上下文（`context: fork`） | 加载后**驻留整段会话** |
| Subagent | 显式 `Agent` 派生 | **独立** context，任务结束返回一段结果 | 完整独立任务 |
| Hook | Claude Code 生命周期事件（`PreToolUse` / `Stop` …） | 无 LLM，Shell 脚本 | 事件触发一次 |

注意 Slash Command 现在是 Skill 的**简化形态**——`.claude/commands/deploy.md` 和 `.claude/skills/deploy/SKILL.md` 都创建 `/deploy` 命令，走同一套机制。区别只在能否带支持文件、能否让 Claude 自动触发。

## 两阶段加载：为什么 Skill 便宜

Claude Code 用**渐进披露**避免把所有 skill 都塞进 context：

1. **常驻**：所有 skill 的 `description` + `when_to_use`（合计上限 1536 字符/skill）拼进 system 侧，是**便宜的固定成本**
2. **按需**：触发某个 skill 时，`SKILL.md` **body** 才作为一条消息进入对话——之后**整段会话都留着**

支持文件（`reference.md` / `examples/*.md` / 脚本）**不自动加载**：Claude 判断需要时才 `Read` 或 `Bash` 拉进来。这是 Skill 相较 CLAUDE.md 的核心优势——CLAUDE.md 每轮都在，Skill 只在真被用到时才付出 body 的 token 成本。

**副作用**：一旦 body 进入 context，它整场会话都在。所以官方建议 **`SKILL.md` 保持在 500 行内**；大段参考文档单独拆到 `reference.md`，从 `SKILL.md` 里用 markdown 链接引到（Claude 会在需要时再读）。

## 生命周期与 auto-compaction

Skill body 进入 context 后 Claude Code **不会再读磁盘**——所以你想让指令贯穿任务始终，写成**standing instructions**（"始终 X"），而不是一次性步骤（"接下来做 Y"）。

同一个 skill 在同一场会话里被再次调起，如果**渲染后内容和已存副本相同**，Claude Code 只加一句"这个 skill 已加载"；如果 `$ARGUMENTS` 或 `!` bash 注入的输出变了，才会追加整份新副本。

会话进入 auto-compaction 时，Claude Code 会把**最近一次调起的每个 skill** 各留 5000 token 拼回来（总预算 25k）。所以在长会话里，如果你调过很多 skill，靠前的可能被摘要吞掉——**关键 skill 在压缩后重新调一次**能把它拉回来。

## 什么时候写 Skill / 什么时候别写

**该写 Skill 的信号**：

- 一段流程**在多个会话里反复用**（"每次做 XX 就要先 YY"）
- 你希望 Claude **看到某类问题就自动切换姿势**（一种领域知识、一种代码风格约束）
- 需要**支持文件**（模板、脚本、参考）——把 `SKILL.md` 当入口、其他文件按需拉

**别写 Skill 的信号**：

- 只在**一个会话**里用一次 → 直接写在 prompt 里
- 想让用户**主动触发**、不需要 Claude 自动判断 → 用 [Slash Command](../customization/slash-commands)
- 任务**独立、完整、要独立 context** → 用 Subagent（`Agent` 工具）
- 想**拦截生命周期事件**（工具调用前后、会话结束）→ 用 Hook

## 生态与工具：skill-creator + 开源仓库

知道什么时候该写 Skill 后，下一步就是**写**。两个最常用的入手点：

### 元技能：skill-creator

Claude Code 自带 `skill-creator`（也称 Skill Creator v2）——专门用来**辅助你创建 Skill 的 Skill**。在会话里说"用 skill-creator 帮我做一个 add-supabase-table 的 Skill，要求包含 migration、schema、API route 和测试"，它会一步步引导：明确 use case 和触发词 → 生成正确的 YAML frontmatter → 编写结构化指令（steps）→ 建议与 rules/hooks/agents 的联动 → 生成测试用例。

**优势**：15–30 分钟出生产级 Skill、自动遵循最新最佳实践（frontmatter/trigger/tools/联动 rules）、用完反馈"上次失败案例"还能迭代优化。

### 优秀开源仓库导航

| 仓库 | 特点 | 适合场景 |
| --- | --- | --- |
| [anthropics/skills](https://github.com/anthropics/skills) | Anthropic 官方，结构最规范 | 学习官方 frontmatter/token 优化 |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 205+ 生产级 Skills，覆盖工程/营销/产品/合规 | 快速扩充技能库的"百宝箱" |
| [obra/superpowers](https://github.com/obra/superpowers) | 20+ 实战核心 Skills（TDD/调试/计划执行） | vibecoding 风格强烈 |
| [jeffallan/claude-skills](https://github.com/jeffallan/claude-skills) | 66 个全栈专项（React/NestJS/DevOps/测试） | Next.js/TypeScript 项目 |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 实用 Skills 精选列表 | 找可重复任务的 prompt 范本 |
| [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) | 宝玉的 Skills 集，专注内容生成/微信公众号发布/工作流，支持 `.claude-plugin` 市场 | 内容创作/SaaS 端到端工作流 |

**学习路径**：先看 anthropics/skills（官方规范）→ baoyu-skills（端到端案例）→ alirezarezvani/obra（大型实战库）。多数支持 `npx skills add <repo>` 一键安装。

## 常见坑

- **`description` 太模糊 Claude 用不上**——写清楚"触发场景"和"具体做什么"，专门有一章讲 [写好触发描述](./writing-triggers) 🚧
- **description 太具体 Claude 只在极窄场景用**——留一定泛化空间，例如"分析 git diff"比"分析今日提交"泛化
- **一个 Skill 想覆盖所有场景** → 拆成多个 skill，触发命中率更高
- **`SKILL.md` 里放几百行代码但没写"如何调用"**——Claude 看到就当参考读，不知道你想让它跑
- **忘记 skill body 会驻留整段会话**——里面写"接下来做 X" Claude 只会做一次；改成"始终 X"
- **项目级 skill 可能被别人写并 commit**——审 `.claude/skills/*` 再 accept workspace trust；skill 里的 `allowed-tools` 能免询问放行工具

## 参考

- Anthropic Docs · [Extend Claude with skills](https://code.claude.com/docs/en/skills)（访问于 2026-07-28）
- Anthropic Docs · [Skill content lifecycle](https://code.claude.com/docs/en/skills#skill-content-lifecycle)（访问于 2026-07-28）
- [Agent Skills 开放标准](https://agentskills.io)——Anthropic 主推、多 AI 工具兼容

## 下一步

- 学 SKILL.md 完整字段规范 → [SKILL.md 规范](./skill-md-spec) 🚧
- 学怎样把 description 写得让 Claude 恰好触发 → [写好触发描述](./writing-triggers) 🚧

## 如果你想

- 立刻上手写一个 → [Cookbook · 写你的第一个 Skill](/cookbook/build-first-skill) 🚧
- 看官方与生态里现成的 Skill → [内置 Skills 一览](./built-in-skills) 🚧
- 弄清 Skill / Command / Subagent 的选型 → [Skill vs Command vs Agent](./skills-vs-commands-vs-agents) 🚧
