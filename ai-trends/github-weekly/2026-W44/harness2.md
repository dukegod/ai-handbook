---
title: 'google-research/harness2：把 harness 拆成组件，让模型自己改 harness'
description: Google Research harness2 深度解读——它如何把 harness 拆成 8 个可编辑组件，并用 Propose–Probe–Compose 递归优化出更好的 harness，以及这套方法论对自建 Agent 平台的可借鉴部分
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-10-26
---

# google-research/harness2：把 harness 拆成组件，让模型自己改 harness

> **TL;DR**：README 开头就给了定义——**harness 是模型周围那套让它能当 Agent 用的系统（提示词、工具、记忆、技能、编排），harnessing 是优化这套系统的过程**。harness2 把 harness 拆成 8 个可编辑组件，用 **Propose–Probe–Compose** 在同一个任务上反复试探、比对执行差异、合成新 harness，3 个专业 benchmark 上最高提升 11.5 分。**这是 harness 从「提示词手艺」变成「有评测、有优化回路的工程对象」的第一个公开实现。**

📅 数据窗口：2026-10-20 ~ 2026-10-26 ｜ 🏷️ Harness 工程 ｜ 本周涨星 未进周榜 ｜ 总 star 19,725（存活 19 天）

## 是什么

[google-research/harness2](https://github.com/google-research/harness2) 是 Google Research 在 2026-10-06 开源的**递归式 harness 优化框架**，配套 arXiv 论文 2610.14224 与站点 harness2.github.io。它要解决的问题很具体：**Agent 遇到设计时没见过的新任务时，harness 本身该怎么调整。**

它连接了两层递归：

- **任务级递归（task-level）**：用对比式的 **Propose–Probe–Compose** 三步，在当前任务上细化执行用的 harness —— 先提出编辑方案，再在同一任务上探测这些编辑的效果，最后从多次执行的行为差异里合成一个更好的 harness。**全程不需要 ground truth 标注。**
- **harnessing 级递归**：维护一个持久的 *improvement harness*，把每个任务里被采纳的 harness 和有证据支撑的经验沉淀进去，指导后续任务的细化。

配套的 `harness2` 命令行提供 `setup / check / judge / report` 一整套 benchmark 流程，支持 `--mode parallel` 与 `--mode sequential` 两种递归模式、`--k` 控制递归预算，覆盖 JobBench（职业工作）、LAB（法律工作）、WorkBuddy-Bench（办公 / 网页 / 代码）三个 benchmark，执行器支持 OpenCode 与 Codex。

## 技术亮点

**第一，8 个组件的拆法本身就是一份可复用的 harness 架构清单。** harness2 暴露的八个可编辑组件是：system prompt、guardrails、memory、tool guidance、subagents、skills、scripts、plugins。它们分成三组——前四个（提示词、护栏、记忆、技能）负责**上下文构建**，tool guidance 与 scripts 负责**工具接口**，subagents 负责**委派编排**，plugins 负责**中间件**。任何自建 Agent 平台都可以拿这八个格子去对照自己的配置模型：缺哪一块，通常就是线上问题出在哪一块。

**第二，Propose–Probe–Compose 用「行为差异」当反馈信号，这是它能免掉标注的关键。** 大多数自我改进方案要靠打分器或人工标注给信号，这里改成：同一个任务跑两次（改进前 vs 改进后），用两次执行的差异当证据。好处是零标注成本；代价是**信号质量完全取决于任务的可判定性**——如果两次执行的差异无法归因到 harness 改动上，优化回路就会朝噪声方向走。

**第三，评测与优化是同一套契约。** README 特别强调 judge 与 report 必须使用相同的 benchmark、执行器、子集、`--k`、`--mode` 和随机种子。这条约束看着琐碎，但它保证了「优化时用 A 指标、验收时用 B 指标」这类自欺欺人的做法在工具层被堵死。

**第四，demo 路径不需要任何模型凭据。** `harness2-demo` 用确定性的编辑器和真实 Python 执行跑通两种递归模式，不消耗 API。这让团队能在不申请预算的前提下先把优化回路接进 CI。

## 后续发展建议

**harness2 的真正价值不是代码，是它把「优化 harness」变成了一件有明确输入输出契约的事。** 三个判断：

- **组件清单可以直接搬到内部平台当配置模型的检查表。** 自建 Agent 平台最常见的失败模式，是只做了 system prompt 和 tool guidance 两格，guardrails、memory、plugins 都缺。**建议把这 8 项做成平台配置项的固定分区，每一项都必须有明确的默认实现**——缺哪项就在平台侧显式标注「未实现」，而不是让它悄悄退化。这比「我们支持自定义 prompt」这种说法可验证得多。
- **Propose–Probe–Compose 的机制可以先在内部用例上试，不必等框架成熟。** 最小可行版本是：固定一组内部任务，让 Agent 提出配置改动 → 在同一任务上跑对照 → 用执行差异（是否通过测试、是否触发人工介入、耗时与 token 成本）合成新配置。**关键不在框架，在于把「谁在什么任务上改了什么配置、结果如何」这条链路记录下来**——这是 harness 优化的资产，跟数据库里的向量索引不同，它是可审计的决策轨迹。
- **对内部平台的真实价值在「评测先于优化」。** harness2 的所有数字都挂在三个 benchmark 上。**内部平台推进 harness 调优之前，先把内部评测集建起来**——否则优化就是盲改，而盲改在多 Agent 场景下很容易越改越差（护栏被稀释、技能互相冲突）。这一条比用哪个框架更关键。

**风险与局限**：工程门槛高——只支持 Linux、Python 3.12、需 `uv`，跑模型侧 benchmark 还要 Node.js 20+ 与 Google Cloud CLI，且默认走 Vertex AI；执行器目前只有 OpenCode 与 Codex 两家，泛化性待观察。项目 2026-10-06 才创建、至今没有 release，最后一次 push 停在 10-14，132 个 open issue 悬在 19,725 star 之上——**热度远跑在工程成熟度前面**，建议按研究原型对待而不是按可用框架对待。

## 下一步

- 看 harness 里「安全」那一格怎么单独做 → [security-audit-skill 深读](./security-audit-skill.md)
- 看另一个方向的 harness 优化（人工规则化）→ [impeccable 深读](./impeccable.md)
- 想理解 harness 组件在内部平台怎么分层 → [AI Native 方法论](../../../ai-harness/index.md)

## 如果你想

- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
- 想看跨系统集成时的信任边界划分 → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)
- 想比较各家 Agent 工具形态 → [AI 工具全景](../../../ai-coding/tools/overview.md)
