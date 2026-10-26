---
title: 'android/skills：Google 用「评测」决定写哪些 Skill，不写哪些'
description: Android 官方 skills 深度解读——它如何用 agentskills.io 开放标准做 Android 开发 Skill、只做评测显示 LLM 不擅长的用例，以及「用评测划定 Skill 边界」这条方法论
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-10-26
---

# android/skills：Google 用「评测」决定写哪些 Skill，不写哪些

> **TL;DR**：Android 官方开了一个 skills 仓库，里面是 **AI 优化的模块化指令**（`SKILL.md`），帮 Agent 更好地理解并执行 Android 开发的最佳实践。它最有价值的一句话在 README 里：**「我们的 Skill 开发聚焦于评测显示 LLM 表现不佳的用例和工作流；对于 LLM 已经擅长的领域（比如基础的 Jetpack Compose 最佳实践），我们不优先做。」** 本周涨星 +1,070，涨星占存量 11%。

📅 数据窗口：2026-10-20 ~ 2026-10-26 ｜ 🏷️ Skill 生态标准 ｜ 本周涨星 +1,070 ｜ 总 star 9,737

## 是什么

[android/skills](https://github.com/android/skills)（Apache-2.0，Kotlin）是 **Android 官方的 Agent Skills 仓库**。README 的定义很精确：**AI-optimized, modular instructions**——为 AI 优化过的模块化指令与资源，帮助 Agent 更好地理解和执行符合 [developer.android.com](https://developer.android.com) 最佳实践的 Android 开发模式。

技术形态上，它遵循 **open-standard agent skills**（[agentskills.io](https://agentskills.io/home)）规范：用 markdown 文件（`SKILL.md`）给出某个任务的**技术规格**，把 LLM 锚定在专业领域与具体工作流上。

安装给了三条路径：

- **Android CLI** —— `android skills add r8-analyzer --project=.`；`android skills add --all` 装全部；`--agent` 指定逗号分隔的 Agent 列表；`--project` 指定项目根。检测不到已有 Agent 目录时默认装给 Gemini 和 Antigravity（`~/.gemini/antigravity/skills`）。更新用 `android skills update --all`。
- **作为 Agent 插件（Claude Code）** —— `/plugin marketplace add android/skills` 再 `/plugin install android-skills@android-skills`。
- **作为 Agent 插件（Codex）** —— `codex plugin marketplace add android/skills` 再 `codex plugin add android-skills@android-skills`。

Skill 会被 Agent **按任务相关性自动激活**——比如你说「把界面做成全面屏」，它应该自动找到并使用对应 skill。

## 技术亮点

**第一，用评测划定边界，而不是靠覆盖面取胜。** 这句话值得单独拎出来：**聚焦评测显示 LLM 表现不佳的用例，对 LLM 已经擅长的领域不优先做。** 大多数 skill 仓库在拼命堆覆盖面——覆盖越多越显得全，越全越受欢迎。但 skill 有 token 成本、有检索干扰成本，**教会模型已经会的东西是净亏损**。Android 选择先划边界再填内容，这是从 harness 经济学出发的取舍。

**第二，跟随开放标准而不是自造格式。** 它明确采用 agentskills.io 的 `SKILL.md` 规范。一个平台厂商愿意让自己的资产被别的 harness 装走，说明它赌的是**标准胜过封闭**——对使用者来说，能被多个 Agent 装走的 skill 才不会因为换工具而作废。

**第三，「标准源 + 各宿主适配层」的双层结构已经成形。** 注意它给的三条路径其实是两层：底层是遵循开放标准的 `SKILL.md` 内容源，上层是 Android CLI（平台自己的安装入口）、Claude Code 插件市场、Codex 插件市场三个适配入口。**内容一份，安装面多个**——这正是上期周报提到的「分发层先于协议统一」的实物样本。

**第四，选题标准本身可以跨领域迁移。** 「用评测决定写哪些 skill、不写哪些」这条规则，与 skill 内容无关，任何领域都能套用。内部做 skill 库时，这是最该先建立的一条纪律。

**第五，激活靠语义匹配而非显式调用。** README 描述的是「Agent 根据任务相关性自动激活 skill」。这比让用户记住命令名更自然，但也意味着**内容质量直接决定触发准确率**——描述写得含糊，skill 就可能该用时不用、不该用时乱用。

## 后续发展建议

**这个仓的内容是 Android 专属的，但它的方法论是通用的，且通用部分比内容更值钱。**

- **「用评测决定 Skill 边界」这条要抄成内部纪律。** 内部做 skill / 插件库时，**建议先建一组内部用例评测集，再决定写哪些、不写哪些**。具体做法：每个候选 skill 对应一组已知会失败的用例，用它跑一遍，只在确实能提分的方向上投入。**没有评测就不要写 skill**——否则内部 skill 库会迅速膨胀成一份没人敢删、也没人验证的清单。
- **双层结构（开放标准内容源 + 各宿主适配层）值得作为内部 skill 分发的架构参考。** 内部平台建议把 skill 内容放在自己这一侧、用开放格式存储，再为各宿主写薄适配。**这样换 harness 时只换适配层，不动内容。** 这与 knowledge-work-plugins 的「平台给结构、业务方填内容」是同一类分层思路。
- **自动激活的机制对内部平台是个提醒：skill 的描述就是路由规则。** 内部 skill 的元数据（标题、描述、适用条件、排除条件）实际上决定了它什么时候被选中。**建议把 skill 描述当成接口契约来写和评审**——明确「什么情况下用它」和「什么情况下不要用」，而不是写一句宽泛的用途说明。
- **平台厂商下场做 skill，本身是信号。** Google 用 Android 官方身份发布 skill 仓，意味着**领域知识分发开始由领域权威承担，而不是社区自发整理**。内部平台可以借鉴这一点：**领域型知识（内部框架规范、发布流程、值班手册）由权威方维护 skill，比让业务方各自总结更可靠**。

**风险与局限**：仅限 Android 领域，跨领域只能借方法论；**README 明确写着「暂不接受公开贡献」**（Public contributions are not accepted at this time），意味着它是单向输出而非社区共建，**内容更新完全依赖 Google 内部节奏**；36 个 open issue 配 9,737 star，issue 密度极低，说明多数用户还没真正接入；版本 v1.0.17 说明仍在早期迭代。另外 `android skills add` 这类命令依赖 Android CLI 分发，**内部平台若要抄这个模式，得先确认自己有类似的「CLI + 插件市场」双通道**，否则会出现只有内容没有安装面的悬空状态。

## 下一步

- 看另一个厂商的插件包结构 → [knowledge-work-plugins 深读](./knowledge-work-plugins.md)
- 看 skill 如何被装进多个宿主 → [harness2 深读](./harness2.md)
- 想知道这些 Agent Skill 该怎么组织 → [AI Native 方法论](../../../ai-harness/index.md)

## 如果你想

- 想看生态里有哪些可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)
- 想比较各家 Agent 工具形态 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
