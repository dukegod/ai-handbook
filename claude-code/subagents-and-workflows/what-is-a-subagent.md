---
title: 什么是 Subagent
description: 'Claude Code Subagent 心智模型——独立上下文窗口、自定义系统提示、受限工具集、主线程委派机制，五大价值与内置 Explore/Plan/general-purpose'
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

# 什么是 Subagent

> **TL;DR**：Subagent 是在**独立上下文窗口**里跑的 Claude 实例——有自己的系统提示、受限工具集、独立权限。主线程遇到匹配的任务时**委派**给 subagent，它干完活只返回摘要，把搜索结果、日志、文件内容这些「脏数据」留在自己窗口里。类比：Subagent 之于主线程 ≈ 函数之于主程序——独立栈帧，用完即收。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- Subagent 解决什么问题（上下文污染）
- 独立上下文窗口：什么是共享、什么是隔离
- 内置 subagent 三件套：Explore / Plan / general-purpose
- 五大使用价值
- Subagent vs Background Agent vs Agent Team 的边界

## 前置

- 读过 [上下文窗口](../basics/context-window) —— 知道 context 是有限资源
- 读过 [工具总览](../tools/overview) —— 知道 Claude Code 有哪些工具

## 一、Subagent 解决什么问题

主线程对话的 context 是**有限且昂贵**的。想象这个场景：

```text
你：「帮我看看这个 bug 跟哪些文件相关」
Claude（主线程）：grep 一遍 → 读 8 个文件 → 跑测试 → 贴回 3000 行日志
                 ↑ 这些全塞进主 context，后续每轮都要带着
你：「现在修一下」
Claude：还要带着那 3000 行没用的日志
```

**Subagent 改变了这个模型**：

```text
你：「帮我看看这个 bug 跟哪些文件相关」
Claude（主线程）：委派给 Explore subagent
  └─ Explore（独立窗口）：grep → 读 8 个文件 → 跑测试
     └─ 返回：「跟 auth.ts、session.ts 相关，根因在 session.ts:42」
Claude（主线程）：只收到这一句摘要，主 context 干净
你：「现在修一下」
```

**核心**：脏数据留在 subagent 的窗口里，主线程只拿到结论。

## 二、独立上下文窗口

| | 主线程 | Subagent |
| --- | --- | --- |
| **Context 窗口** | 独立 | **独立**（互不污染） |
| **System prompt** | Claude Code 默认 | 自定义 |
| **工具集** | 全部 | 可限制 |
| **权限** | 继承会话 | 可独立配置 |
| **CLAUDE.md** | 加载 | 加载（Explore/Plan 除外） |
| **git status** | 可见 | 可见（Explore/Plan 除外） |
| **返回值** | — | **只返回摘要**给主线程 |

**关键隔离**：subagent 读的文件、跑的命令、搜索结果——**主线程看不到**。主线程只看到 subagent 最后的返回文本。这就是 context 节省的本质。

## 三、内置 Subagent

Claude Code 自带几个 subagent，Claude 在合适时机**自动委派**：

| Subagent | 模型 | 工具 | 用途 |
| --- | --- | --- | --- |
| **Explore** | 继承主线程（API 上限 Opus） | 只读 | 代码搜索、文件发现、理解代码库 |
| **Plan** | 继承主线程 | 只读 | plan mode 下做代码调研 |
| **general-purpose** | 继承主线程 | 全部 | 复杂多步任务（探索 + 修改） |
| **claude** | 继承 | 全部 | 兜底默认 agent；background session 默认 |
| **claude-code-guide** | Haiku | — | 回答 Claude Code 功能问题 |
| **statusline-setup** | Sonnet | — | `/statusline` 配置时 |

**Explore 和 Plan 跳过 CLAUDE.md 和 git status**——保持调研快且省。其它 subagent（含自定义）都加载这两者。

**v2.1.198+ 注意**：Explore 不再固定跑 Haiku，而是**继承主线程模型**（API 上限 Opus）。想强制低成本，自定义一个 `model: haiku` 的同名 subagent 覆盖它。

## 四、五大使用价值

| 价值 | 场景 |
| --- | --- |
| **保留 context** | 调研类任务（grep / 读文件 / 跑测试）的中间结果不污染主线程 |
| **强制约束** | 限制 subagent 只能用只读工具，防误改 |
| **配置复用** | 用户级 subagent 跨项目可用 |
| **行为特化** | 专属系统提示（如「你是安全审计专家」） |
| **控制成本** | 路由到更便宜模型（Haiku）跑低难度任务 |

## 五、委派机制

Claude **看 subagent 的 `description`** 决定是否委派：

```text
用户提问
   ↓
Claude 判断：这任务匹配某个 subagent 的 description 吗？
   ↓ 是                              ↓ 否
委派给该 subagent              主线程自己干
   ↓
subagent 在独立窗口工作
   ↓
返回摘要给主线程
```

所以 **description 写得好坏决定命中率**——和 [Skill 的触发描述](../skills/writing-triggers) 同理：写清楚「做什么」+「何时用」。

## 六、与 Background Agent / Agent Team 的边界

Subagent **在单个 session 内**运作。Claude Code 还有两个相关概念别混淆：

| | Subagent | Background Agent | Agent Team |
| --- | --- | --- | --- |
| 上下文 | session 内独立窗口 | 独立 session | 多个独立 session |
| 并行 | session 内 | 多个并行跑 | 多个并行 + 互相通信 |
| 监控 | 主线程等返回 | `/agents` 面板看 | 团队协作视图 |
| 适合 | 单任务委派 | 批量后台任务 | 多角色协作 |

**本页只讲 Subagent**。Background Agent 和 Agent Team 是更重的机制，本站后续高级篇覆盖。

## 参考

- [Anthropic · Create custom subagents](https://code.claude.com/docs/en/sub-agents)（访问于 2026-08-04）
- [Anthropic · Context window 可视化](https://code.claude.com/docs/en/context-window)（访问于 2026-08-04）—— subagent 如何节省 context 的演示

## 下一步

- 看所有 subagent 类型和配置字段 → [Agent 类型清单](./agent-types) 🚧
- 多 subagent 怎么编排 → [Workflow 编排](./workflow-orchestration) 🚧
- 常见多 agent 模式 → [多 Agent 常见模式](./multi-agent-patterns) 🚧

## 如果你想

- 自己写一个 subagent → [Agent 类型清单 · 自定义](./agent-types) 🚧
- 理解 context 为何是瓶颈 → [上下文窗口](../basics/context-window)
- 看 Skill 与 Subagent 的边界 → [Skill vs Command vs Agent](../skills/skills-vs-commands-vs-agents)
