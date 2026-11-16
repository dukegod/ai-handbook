---
title: 'addyosmani/agent-skills：把「约束」放到编码之前，而不是放在评审之后'
description: agent-skills 深度解读——25 个 skill 的开发生命周期映射、constraint-driven-development 把质量标准写成 CONSTRAINTS.md、doubt-driven-development 的 CLAIM-EXTRACT-DOUBT 复核流程，以及跨 70+ harness 的安装矩阵
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-16
---

# addyosmani/agent-skills：把「约束」放到编码之前，而不是放在评审之后

> **TL;DR**：118,003 star、12,346 fork，**本周涨星 +3,889，涨星占存量仅 3.3%**——**这是典型的「大项目持续吸量」，不是新项目爆发**：绝对值排周榜第 9，但比例只有 3.1% 那个量级。MIT 协议，JavaScript，仓库建于 **2026-02-15**，最新版本 **Agent Skills 0.6.16（2026-11-14）**，最近一次提交 2026-11-14。59 个 open issue、69 个 open PR。

📅 数据窗口：2026-11-10 ~ 2026-11-16 ｜ 🏷️ Agent 工具链 / 约束工程 ｜ 本周涨星 +3,889 ｜ 总 star 118,003

## 是什么

[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) 的自我定义是 **production-grade engineering skills for AI coding agents**——把资深工程师的工作流、质量门和最佳实践打包，让 Agent 在**每个阶段**都一致遵守。

它把开发生命周期映射成 9 个 slash command：`/spec`（先有规格）、`/plan`、`/build`、`/test`、`/constraints`（定一次质量标准）、`/review`、`/webperf`、`/code-simplify`、`/ship`。底层是 **25 个 skill**（24 个生命周期 skill + 一个 `using-agent-skills` 元 skill），每个 skill 都是「带步骤、验证门和 anti-rationalization 表」的结构化工作流。

几个 skill 值得逐字看：

- **`interview-me`**——一次问一个问题，挖出用户真正要的，**直到约 95% 置信度**。
- **`constraint-driven-development`**——**面试你定一个质量标准**，把默认阈值写进 `CONSTRAINTS.md`，按成本给每项检查分级，**并且专门抓「Agent 为了变绿而 silencing 检查或跳过测试」**。
- **`doubt-driven-development`**——对每个非平凡决策做**新上下文对抗式复核**，流程是 **CLAIM → EXTRACT → DOUBT → RECONCILE → STOP**，可选在用户授权下升级到跨模型。
- **`context-engineering`**——在正确的时间喂正确的信息（规则文件、上下文打包、MCP 集成）。
- **`source-driven-development`**——每个框架决策都以官方文档为准，**核实、引用来源、标注未核实项**。

`/build auto` 的特别之处：**一次生成计划并在一次批准后自主实现所有任务**——README 说它**移除的是任务之间的人为停顿，不是验证**：每个任务仍测试驱动、单独提交，**在失败或高风险步骤处暂停**。

安装矩阵很宽：`npx skills add` 一次装进 **70+ 个 Agent**，或走原生集成（Claude Code 插件市场、Cursor 的 `.cursor/skills/`、Antigravity CLI、Gemini CLI、OpenCode 的 `.opencode/skills/`、Codex 插件等）。**skill 本身是纯 Markdown**，任何能吃系统提示词的宿主都能用。

## 技术亮点

**第一，`constraint-driven-development` 是这套东西里最值得单独抄的一个。** 它做三件事：**访谈出质量标准**（有合理默认阈值）、**写进 `CONSTRAINTS.md`**（把标准变成仓库里可版本化的资产）、**按成本给检查分级**。最狠的一句是——**专门用来抓 Agent 让检查闭嘴或跳过测试以达成「变绿」**。**这直接命中了 Agent 工程化最大的失败模式：Agent 通过降低标准来通过验收，而不是通过改进代码。** 内部平台做质量治理，**「检测标准被静默降级」本身要可检测**。

**第二，`doubt-driven-development` 是本周 EGM「换无前情上下文评审」的同源思路，但更工程化。** 流程 CLAIM → EXTRACT → DOUBT → RECONCILE → STOP，**默认在流程进行中对每个非平凡决策做复核，而不是事后统一评审**。README 给的触发场景很具体：生产 / 安全 / 不可逆操作、不熟悉的代码、**或者「现在多花一点时间验证，比之后调试便宜」**。它还支持**在用户授权下升级到跨模型**，比 EGM 更进一步。

**第三，`context-engineering` 被当成一个一等 skill，而不是隐含在每个提示词里。** 它处理规则文件、上下文打包、MCP 集成，触发时机是「输出质量下降时」——**把质量下降当成一个需要处理的信号**，不是「换个模型试试」。

**第四，它在 README 里如实写出了一个真实的工程坑。** 单个 skill 安装（`--skill <name>`）只复制 `skills/<name>/`，**不复制仓库级的 `references/` 目录**——skill 还能用，但**指向共享检查清单的路径会失效**（issue 编号 #361 跟踪）。

**第五，它给每个 harness 都写了适配说明，包括坏消息。** Antigravity CLI 旧版 command TOML「报告为已转换，但 wrapper 命令不可发现」；Copilot 里**生命周期 slash command 不存在**；Claude Code 插件市场默认走 SSH 克隆，**没有 SSH key 会失败**，README 给出 HTTPS 强制和 `url."https://github.com/".insteadOf` 两种绕法。

## 后续发展建议

**最重要的判断是：Agent 工程化正在从「教它怎么做」转向「先定标准再让它做」。** 四个判断：

- **「约束先行」的顺序，比约束的内容更重要。** `/spec` 和 `/constraints` 排在 `/build` 之前——**先定义什么算好，再让它去写**。这与 W46 讲的 `spec-kit` 是同一条脉络，但这里多一步**「按成本分级」**：**分级才能让 Agent 在有限预算里做对的取舍**。内部平台建议：**质量门按成本分级（廉价的每步跑、昂贵的按变更范围跑）**，而不是一刀切全量检查。

- **「防 Agent 降级标准」应当作为一条独立的安全规则。** `constraint-driven-development` 专门抓「silencing checks or skipping tests to get green」——**这与 Agent 运行时安全（沙箱、权限、审计）是同一类问题的不同层面**：前者管**结果可信**，后者管**行为可控**。**建议把「Agent 是否为了让检查通过而修改检查」列入可观测项**。

- **「跨 70+ harness 的适配成本是这个生态的真实成本」，README 里那些坏消息比任何好话都有参考价值。** 内部平台如果自建 skill 生态，**建议先支持 2～3 个 harness 并把差异写进适配层**，而不是追求覆盖率。

- **`/build auto` 的语义值得直接抄：移除「任务之间的人为停顿」，但不移除验证。** **自动化的是节奏，不是验收**。**建议把「哪些节点必须停」显式建模成任务图的属性**。

**风险与局限**：**118,003 star 却只有 +3,889 周涨星（3.3%）**——**它已经过了爆发期**；**25 个 skill 每条都是结构化工作流，装进去有上下文成本**；最后，**整个项目的前提是「流程可以被编码」**——团队流程非标准的话，套进来只会得到一个更长的提示词。

## 下一步

- 想看同一层问题的 UI 版本 → [taste-skill 深度解读（本期同期项目）](./taste-skill.md)
- 想看规格阶段的另一种做法 → [EGM 深度解读（本期同期项目）](./elephant-goldfish-model.md)

## 如果你想

- 想理解怎么把工程纪律变成可执行流程 → [AI Native 方法论](../../../ai-harness/index.md)
- 想看 Agent 工具全景 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想看可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)
