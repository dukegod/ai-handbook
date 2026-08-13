---
title: Skill vs Command vs Agent
description: Claude Code 里 Slash Command / Skill / Subagent / Hook 四种扩展机制的边界、三问决策树、六个真实场景与常见误选
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

# Skill vs Command vs Agent

> **TL;DR**：Claude Code 有**四种**把工作流固化下来的机制——Slash Command / Skill / Subagent / Hook。选型三问：**触发者是谁？需要独立 context 吗？是不是 LLM 决策？** 记住 Slash Command 已经并入 Skills（是简化形态），真实选型多数是 **Skill / Subagent / Hook 三选一**。

⏱ 预计阅读时间：9 分钟

## 你能在这里学到

- 四种机制各自的**一句话本质**（含触发者 / LLM 参与 / context 归属四栏对比表）
- **三问决策树**：触发者 / context 独立性 / LLM 决策
- 六个真实场景走一遍——同一个需求换个变量该选什么
- 三种「组合使用」模式（Skill × Command、Hook × Skill、Subagent × Skill）
- 五种最常见的选错场景

## 前置

- 读过 [什么是 Skill](./what-is-a-skill) 与 [Slash Commands](../customization/slash-commands)
- 知道 Claude Code 有 [Hooks](../customization/hooks) 与 Subagent（见 [什么是 Subagent](../subagents-and-workflows/what-is-a-subagent)）

## 一、一句话本质

| 机制 | 一句话 | 触发者 | LLM 参与 | Context 归属 |
| --- | --- | --- | --- | --- |
| **Slash Command** | 敲 `/xxx` 展开一段 prompt 模板 | **只用户** | 是 | 主会话 |
| **Skill** | Claude 看情况自动加载的能力包 | **用户或 Claude** | 是 | 主会话（可 fork 到子上下文） |
| **Subagent** | 派生一次独立 context 的完整任务 | Claude 显式派生 | 是 | **独立**，返回一段结果 |
| **Hook** | 生命周期事件触发的 shell 脚本 | **系统事件** | **否** | 不接触 LLM |

Slash Command 现在是 **Skill 的简化形态**——同一套引擎（`$ARGUMENTS` / `` !`cmd` `` / `allowed-tools` 完全一致），差别只在**能否让 Claude 自动触发**、**能否带支持文件**、**能否 fork 子上下文**。所以真实的选型题多数是 **Skill / Subagent / Hook 三选一**。

## 二、三问决策树

**问题 1：谁应该按启动键？**

- **只有用户** → Slash Command，或 `disable-model-invocation: true` 的 Skill
- **用户或 Claude 都行** → 默认 Skill
- **只有 Claude 自动**（不进 `/` 菜单）→ `user-invocable: false` 的 Skill（背景知识型）
- **完全不用"决定"，事件到了就跑** → Hook

**问题 2：需要独立 context 吗？**

- **不需要**（往主会话里塞领域知识 / 修改行为）→ Skill（inline body）或 Command
- **需要**（任务重、只要一份结果、不污染主会话）→ Subagent（Agent 工具）或 Skill + `context: fork`

**问题 3：是不是 LLM 决策？**

- **是**（需要 Claude 判断、生成、总结）→ Skill / Command / Subagent
- **否**（"改动前跑 lint"、"session 开始加载 .env"）→ Hook

三问排完基本就锁定一个。

## 三、六个具体场景

**1. "每次 pnpm build 之前先跑 lint"** → **Hook**（PreToolUse），确定性事件、无 LLM 决策

**2. "review 我今天的 diff 并写 commit message"** → **Skill**（想让 Claude 看到 diff 自己想起来这件事）或 **Slash Command**（想每次主动敲 `/review-diff`）——取决于你要不要它自动触发

**3. "并行开三个 agent 分析 auth / billing / api 三个子系统，最后合并成一份报告"** → **Subagent**（Agent 工具或 [Workflow 编排](../subagents-and-workflows/workflow-orchestration)），三个独立 context 并行、结果汇总

**4. "让我敲 `/deploy prod` 触发部署脚本，只能我自己敲，Claude 不能误触"** → **`disable-model-invocation: true` 的 Skill**，副作用大的操作必须走用户显式确认

**5. "我们老 CRM 系统的领域知识 —— Claude 看到相关 ticket 应该自己想起来"** → **`user-invocable: false` 的 Skill**（背景知识型，不占 `/` 菜单也不需要用户主动敲）

**6. "session 一启动就把当前 sprint 的 JIRA 上下文注入进来"** → **Hook**（SessionStart），确定性、每次都要跑、无判断

## 四、组合使用

三种常见组合：

**Command + Skill · fork subagent 做重活**

`.claude/commands/deploy.md` 里 body 触发一个 fork subagent 跑 pre-deploy 检查——命令负责入口和参数，重活扔到独立 context 里。

**Hook + Skill · 拦截 + 提示**

PreToolUse hook 拦截敏感操作（如 `rm -rf`）→ 强制让 Claude 加载一个"这个操作需要人工 review"的 skill 走额外确认流程。

**Subagent + Skill · 每个 agent 加载不同姿势**

[Workflow 编排](../subagents-and-workflows/workflow-orchestration) 里每个 subagent 加载不同 skill（一个走安全审计姿势、一个走 perf 分析姿势）——一个模型多种"人格"。

## 五、五种常见误选

**把「想让 Claude 自动想起来」的能力写成 Slash Command** → 用户没敲 `/` 就永远不触发。改成默认 Skill（双向可触发）。

**把「想拦截 PreToolUse」写成 Skill** → Skill 是 Claude 自己判断触发，**无法阻止**别的工具调用发生。改 Hook。

**把「一次性 prompt」写成 Skill** → Skill body 加载后**驻留整段会话**，一次性任务白白污染 context。直接在 prompt 里说清楚就行。

**把「需要独立 context 的完整任务」写成 inline Skill** → 会占主会话 token 且干扰后续对话。改 Subagent 或 Skill + `context: fork`。

**把「有副作用的操作」（部署、发消息、写数据库）设成 Claude 可自动触发的 Skill** → Claude 觉得代码差不多就自己按按钮，事故多。**副作用大的操作永远设 `disable-model-invocation: true`**。

## 参考

- [Anthropic · Skills 概念页](https://code.claude.com/docs/en/skills)（访问于 2026-07-29）
- [Anthropic · Slash commands（已并入 Skills）](https://code.claude.com/docs/en/slash-commands)（访问于 2026-07-29）
- [Anthropic · Hooks 参考](https://code.claude.com/docs/en/hooks)（访问于 2026-07-29）
- [Anthropic · Subagents 与 Task 工具](https://code.claude.com/docs/en/subagents)（访问于 2026-07-29）

## 下一步

- 拿这些选型原则做出你自己的 skill → [写你的第一个 Skill](./custom-skill) 🚧
- 深入 Skill 的完整机制 → [什么是 Skill](./what-is-a-skill)
- 深入 Slash Command 的完整机制 → [Slash Commands](../customization/slash-commands)

## 如果你想

- 看 Hook 的完整触发事件表 → [Hooks](../customization/hooks) 🚧
- 深入 Subagent → [什么是 Subagent](../subagents-and-workflows/what-is-a-subagent) 🚧
- 看内置和 bundled 的 Skill 有哪些 → [内置 Skills 一览](./built-in-skills) 🚧
