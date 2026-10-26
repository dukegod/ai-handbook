---
title: 'pbakaus/impeccable：把「AI 味」变成 62 条不需要 LLM 的确定性规则'
description: pbakaus impeccable 深度解读——它如何用 1 个 Skill、24 个命令和 62 条确定性检测规则治理 AI 生成的前端设计，以及这套「规则化 harness」对内部研发流水线的借鉴价值
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-10-26
---

# pbakaus/impeccable：把「AI 味」变成 62 条不需要 LLM 的确定性规则

> **TL;DR**：所有模型都在同一批 SaaS 模板上训练，于是产出长得很像——**处处用 Inter、紫蓝渐变、卡片套卡片、彩色底上的灰字、每个标题上方一个圆角方形图标块**。impeccable 的做法不是再写一段提示词，而是把这些「破绽」拆成 **62 条确定性检测规则 + 24 个命令**，**CLI 和浏览器扩展都能跑，不需要 LLM、也不需要 API key**。本月涨星 +16,493，总 star 87,912。

📅 数据窗口：2026-10-20 ~ 2026-10-26 ｜ 🏷️ Harness 规则化 ｜ 本月涨星 +16,493 ｜ 总 star 87,912

## 是什么

[pbakaus/impeccable](https://github.com/pbakaus/impeccable)（Apache-2.0，Rust 实现，官网 impeccable.style）是给 AI 编码 Agent 用的**设计指导层**，README 开门见山：*1 skill, 24 commands, live browser iteration, and 62 deterministic detector rules for AI-generated frontend design*。

它是从 Anthropic 的 `frontend-design` skill 演化来的——README 明说这是起点。安装是 `npx impeccable install`，然后在工具里跑 `/impeccable init`。

三块内容：

- **一个 setup 流程** —— `/impeccable init` 会检查项目、**只追问「材质性的缺口」**（material gaps），然后把产品的持久事实写进 `PRODUCT.md`：受众、目的、运行场景、约束、语气、证据。视觉方向单独记在 `DESIGN.md`（在用或新建的视觉系统）。
- **24 个命令** —— 一套和 AI 对话的设计词汇表：`craft`（先塑形再实现）、`init`、`document`（从现有代码生成 DESIGN.md）、`extract`（把可复用组件和 token 抽成设计系统）、`shape`（写码前先规划 UX/UI）、`critique`（层次、清晰度、情绪共鸣）、`audit`（a11y、性能、响应式的技术检查）、`polish`，还有 `distill`、`animate`、`bolder`、`quieter` 等。
- **62 条确定性检测规则** —— 加上只靠 LLM 的 critique 检查。**关键在于：CLI 和浏览器扩展运行的是确定性规则那一部分，全程无 LLM、无 API key。**

## 技术亮点

**第一，它把「品味」翻译成了可执行检查。** 设计审美长期被认为是不可自动化的主观判断，impeccable 反过来做：**先把 AI 生成的常见破绽穷举成 62 条规则，再让机器跑**。这个转换的价值不在于规则有多全，而在于它把「这个界面是不是 AI 味」从一次主观评审变成了一次可重复的检查。

**第二，规则能被放进流水线，这是落地的关键。** 因为 CLI 不需要模型就能跑，这些规则**可以直接进 CI，在提交时拦截，而不是生成完再靠人眼看**。41 个 open issue 对应 87,912 star，这个极低的 issue 密度（对比 orca 的 8,424）说明它工程上收敛得很干净——**规则集形态的工具天生比「全能编排台」更容易维护**。

**第三，PRODUCT.md 与 DESIGN.md 的分离值得单独学。** 它把「产品事实」和「视觉方向」拆成两个文件：前者是受众、目标、约束、语气这些跨页面稳定的部分，后者是具体界面的表现。**这和 Claude Code 里「项目规则文件 vs 各工具配置」的层级是同一个思路**——稳定的上层约束、可替换的下层表现。而 `init` 只问材质性缺口、不做问卷式盘问，也避免了另一个常见失败：setup 阶段把人问烦了。

**第四，它的起点是官方 skill。** 从 Anthropic `frontend-design` 出发做「工程化补强」（加确定性规则、加 CLI、加浏览器扩展、加 CI 可用性），是生态里非常典型的一条路径：**官方 skill 逐渐成为基线，第三方在基线上补工具链**。

## 后续发展建议

**这套东西对内部团队最容易复制的不是 62 条规则，是「规则要能脱离 LLM 单独跑」这个要求。**

- **规则检查应该进研发流水线，而不是留在提示词里。** 内部做前端或文档类质量门禁时，**建议把检查项拆成两类**：能用确定性规则判的（格式、禁用项、结构约束、命名、a11y 基线）交给脚本，进 CI 阻断；必须靠理解语义的（文案是否切题、视觉是否协调）才交给模型。**impeccable 41 个 issue 换 8.8 万 star 的工程健康度，本身就是「规则集形态」优于「对话形态」的证据。**
- **「产品事实」与「表现方向」分层，要映射到内部平台。** 内部 Agent 平台里对应的是「能力契约与约束」（这个 Agent 能访问什么、产出什么格式、必须遵守什么）与「运行时默认值」（当前任务的临时参数）。**这两层混在一起是内部平台最常见的技术债来源**——改一个默认参数会意外改掉契约。建议照 PRODUCT.md / DESIGN.md 的思路把两层物理分开。
- **规则集要能被审计和版本化。** 62 条规则意味着「为什么这条算 AI 味」需要能被解释、被讨论、被单独关闭。**内部落地时应要求每条规则有出处、有可关闭开关、有生效范围**，否则会变成一份没人敢动的强制清单。

**风险与局限**：24 个命令 × 62 条规则的组合空间学习成本不低，团队容易只学一个命令就放弃；62 条规则本质是**反面检测**——它能告诉你「这里有 AI 味」，但改完之后是否真的更好，仍要靠人判断，这部分没有自动化兜底；版本号还是 `engine-v0.1.17`，规则引擎处于早期，格式可能变；Rust 实现 + 浏览器扩展的分发链比纯 Markdown skill 重，**团队落地时最常见的失败是只抄规则清单不抄工具，最后退化成一份没人运行的文档**——抄的时候务必连 CLI 一起抄。

## 下一步

- 看另一个方向的 harness 优化（让模型自己改 harness）→ [harness2 深读](./harness2.md)
- 看官方 skill 目录长什么样 → [knowledge-work-plugins 深读](./knowledge-work-plugins.md)
- 想知道这些 Agent Skill 该怎么组织 → [AI Native 方法论](../../../ai-harness/index.md)

## 如果你想

- 想比较各家 Agent 工具形态 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想看生态里有哪些可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)
- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
