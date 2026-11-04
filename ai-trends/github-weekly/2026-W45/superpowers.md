---
title: 'obra/superpowers：把「skill 是强制工作流」做成 16+ harness 通吃的方法论'
description: obra/superpowers 深度解读——用 brainstorming 到 finishing-a-development-branch 的七步强制工作流把开发方法论装进编码 Agent，以及跨 16+ harness 分发与 bootstrap 注入的工程细节
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-02
---

# obra/superpowers：把「skill 是强制工作流」做成 16+ harness 通吃的方法论

> **TL;DR**：310,723 star、**27,652 fork**——fork 数几乎追平 star 数，说明绝大多数是「clone 一份改自己的」，这是方法论型项目的典型传播形态。superpowers 的关键设计只有一句：**skill 不是建议，是强制工作流**。README 原文——「The agent checks for relevant skills before any task. Mandatory workflows, not suggestions.」七步从 brainstorming 一路到 finishing-a-development-branch，**且适配 16+ 个 harness**。

📅 数据窗口：2026-10-26 ~ 2026-11-02 ｜ 🏷️ Skill 生态 ｜ 本周涨星 +5,896 ｜ 总 star 310,723

## 是什么

[obra/superpowers](https://github.com/obra/superpowers) 是「**给你的编码 Agent 的完整软件开发方法论**」，由 Jesse Vincent（blog.fsck.com）和 Prime Radiant 团队构建。它不是插件合集，是**一套有先后顺序的工作流**：先问清要做什么，出设计文档，拆计划，逐任务派 subagent 实现，红绿重构，交叉评审，收尾合并。

MIT 协议，最新 release **v7.0.1（2026-10-21）**，277 条 fork 之外还有 377 个 open issue。

## 技术亮点

**第一，七步工作流的每一步都有明确的触发条件和产出物。**

| 步骤 | 触发时机 | 产出 |
| --- | --- | --- |
| `brainstorming` | 动手建任何东西之前 | 小改动在聊天里达成共识；项目级产出**书面设计文档** |
| `using-git-worktrees` | 设计通过后 | 隔离工作区 + 新分支 + 项目初始化 + **验证干净测试基线** |
| `writing-plans` | 有批准的设计后 | 拆成 2–5 分钟粒度的任务，每个含**确切文件路径、完整代码、验证步骤** |
| `subagent-driven-development` / `executing-plans` | 有计划后 | 前者每个任务派新 subagent 并逐个评审（最彻底），后者当前 session 内联实现、末尾整体评审一次（最省） |
| `test-driven-development` | 实现中 | 强制 RED-GREEN-REFACTOR，**先写的测试后写的代码要删掉** |
| `requesting-code-review` | 任务之间 | 按计划评审，**严重问题阻断进度** |
| `finishing-a-development-branch` | 任务完成 | 验证测试、给出合并 / PR / 保留 / 丢弃选项、清理 worktree |

值得注意的是 README 对计划质量的描述：目标读者是「**一个热情但品味不佳、没有判断力、不了解项目背景、而且讨厌写测试的初级工程师**」。**这是把「计划必须自足」写进了验收标准**，而不是靠 Agent 猜。

**第二，bootstrap 注入是它能跨 16+ harness 工作的真正原因。** README 里 Antigravity 那段讲得很清楚：Antigravity 会列出每个已安装 skill 的描述，而 `using-superpowers` 这个 skill 的**描述本身就是一句提示，让模型在会话开始时加载这个 skill**。Pi 的做法类似——包会加载 skills 并加一个 extension，在 session 启动时和**压缩之后**再次注入 bootstrap。Muse 用原生 `SessionStart` hook 做同样的事。**这是个很聪明的 hack：用一个 skill 的 description 当作入口信号。**

**第三，它自带诊断自己失灵的能力。** `diagnosing-superpowers` skill 专门处理「skill 该触发没触发、不该触发却触发了、Agent 无视计划、重复劳动、token 烧超预期」这些情况，会读 session transcript、给出带行号的证据，并可以打包成脱敏 bundle 提交 bug report。**把「我的方法论自己坏了」当成一个可被排障的工单，这是成熟框架才有的设计。**

**第四，Harness 差异被显式建模。** README 里直接写了 Hermes **没有 post-compaction hook**，所以超长会话压缩掉首轮后会丢失 bootstrap，需要开新会话——这种「哪个 harness 缺哪个钩子」的坑都写进了文档。**兼容层不是抹平差异，而是把差异列成清单。**

## 后续发展建议

**superpowers 的真正贡献是证明了「方法论可以被打包成可分发的 Agent 资产」。** 四个判断：

- **「强制」而非「建议」这个决定，比它具体有哪七步更值得抄。** README 反复强调 skill 会**自动触发**，用户不用做任何特殊操作。这意味着**触发条件写在 skill 的描述里，由 harness 的加载机制保证它被读进上下文**。内部平台如果只是提供「用户可以 @ 某个流程」的机制，得到的是一个可选工具；**只有让流程自动出现在 Agent 的候选列表里，它才真的会被用。**
- **「计划必须自足到能让一个没品味的初级工程师执行」是极好的验收标准。** 这条可以直接搬到内部平台的需求文档规范里：**一份 Agent 能执行的计划，必须包含确切文件路径、完整代码和验证步骤，不能只写方向。** 这一条比「用 TDD」「要健壮」之类的口号有用得多。
- **它和上期的 `impeccable`、`hallmark` 形成了一个有意思的分工：superpowers 管「做事的顺序」，后两者管「做出来的东西长什么样」。** 三者合起来正好覆盖 harness 的两个正交维度——**流程轴和品质轴**。内部平台的 skill 体系如果只有流程轴，会产出正确但难看的代码；只有品质轴，会产出好看但做错事的代码。**建议两个轴分开建，不要混成一套。**
- **诊断 skill 的设计值得单独学。** 内部平台在推广 skill 体系时，一定会被问「为什么这次没触发」。**与其让用户自己去翻日志，不如内置一个「解释这次为什么这样跑」的诊断能力**——这比事后统计触发率有用得多。

**风险与局限**：**310,723 star 只有 2.1% 的周涨星比（+5,896），是典型的「大盘存量型项目」**，热度不是本周新起。377 个 open issue 对一个方法论项目来说偏多。**它锁定的是「软件工程流程」这一套特定假设（严格 TDD、worktree 隔离、subagent 驱动），对于探索性任务、数据分析、运维排障这类工作并不天然适配**——内部推广时不应要求全量照搬，按任务类型挑子集更现实。另外 README 里有商业服务入口（Prime Radiant 的企业支持），**开源部分与商业部分的边界需要自己确认**。

## 下一步

- 想看同一生态里「skill 是官方规范源」的那一端 → [anthropics/skills 深读](./anthropic-skills.md)
- 想看 skill 怎么被分发到各家 harness → [vercel-labs/skills 深读](./vercel-skills.md)

## 如果你想

- 想知道这些 Agent Skill 该怎么组织 → [AI Native 方法论](../../../ai-harness/index.md)
- 想看工具链横评 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
