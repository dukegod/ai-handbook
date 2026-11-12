---
title: 'mattpocock/skills：反对「流程占有」，Skill 应该小、可改、可组合'
description: mattpocock/skills 深度解读——user-invoked 与 model-invoked 的双轴分类、grill-me / to-spec / to-tickets / implement 的方法论链条，以及「Skill 不该接管流程」这个立场对内部平台的意义
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-09
---

# mattpocock/skills：反对「流程占有」，Skill 应该小、可改、可组合

> **TL;DR**：318,693 star、26,670 fork、226 open issue，MIT。**本周涨星 +9,635，涨星占存量只有 3.0%——但绝对值排全榜第二**，在 31 万 star 的巨量盘子上保持这个增速，是典型的「大项目持续吸量」。README 开头就站了队：**「Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control and make bugs in the code harder to fix.」**

📅 数据窗口：2026-11-03 ~ 2026-11-09 ｜ 🏷️ Skill 生态 / 方法论 ｜ 本周涨星 +9,635 ｜ 总 star 318,693

## 是什么

[mattpocock/skills](https://github.com/mattpocock/skills) 是作者 Matt Pocock 自己的 **「Skills For Real Engineers」**——README 第一句：**「My agent skills that I use every day to do real engineering - not vibe coding.」**

它的立论有两个支点：

**第一，它明确反对流程框架「占有流程」。** README 直接点名 GSD、BMAD、Spec-Kit 三家，说它们靠**接管流程**来帮忙，代价是**夺走控制权、让代码里的 bug 更难修**。**它的立场是：skill 要小、易改、可组合，与任何模型搭配，用户拿去改。**

**第二，它按「修复真实失败模式」来组织，而不是按「功能」组织。** README 的 "Why These Skills Exist" 章节列了四个失败模式，每个对应一组 skill：

| 失败模式 | 诊断 | 对应 skill |
| --- | --- | --- |
| #1 Agent 没做我想要的 | 对齐缺口 | `grill-me` / `grill-with-docs` |
| #2 Agent 太啰嗦 | 词汇不统一 | `domain-modeling` + 项目词汇表 |
| #3 代码跑不起来 | 反馈回路缺失 | `diagnosing-bugs` / `tdd` |
| #4 代码变成一坨泥球 | 模块边界缺失 | `codebase-design` / `code-review` |

## 技术亮点

**第一，「谁能调用」被做成了一条明确的分类轴。** README 的 Reference 章节第一句：**「These split on one axis: who can invoke them.」**——**user-invoked**（只有你手动敲才触发，职责是「编排」）和 **model-invoked**（Agent 判断相关性时自己加载，职责是「执行」）。这个切分很实用：**编排类 skill 应该由用户显式调用，否则 Agent 会把自己编排进死循环**。

**第二，「grill-me」揭示了它的核心方法论。** README 引用《程序员修炼之道》那句——**「No-one knows exactly what they want」**——给出的解法是 **grilling session**：**让 Agent 反过来反复拷问你，直到设计树的每一支都被解掉**。README 说：**「These are my most popular skills.」**

**第三，它有完整的「从对话到落地」链条。** `to-spec`（把当前对话变成 spec 并发到 issue tracker，**不做访谈，直接综合**）→ `to-tickets`（拆成 tracer-bullet 式的票，每张声明自己的阻塞关系）→ `implement`（按 spec 或票干活，在约定接缝上驱动 `/tdd`）→ `implement-spec`（整份 spec 走一条集成分支，**把票当成任务图跑**）。**这条链把「聊出来的想法」和「落地的代码」之间每一段都做成可交接的产物。**

**第四，大块工作有专门的规划 skill。** `wayfinder` 的描述是：**「Plan a huge chunk of work, more than one agent session can hold, as a shared map of decision tickets」**——**一次会话装不下的工作，规划成一张「决策票」的共享地图**。这对应 Agent 的真实约束：**上下文窗口有限，长任务必须能跨会话接力**。

**第五，它有「回头改环境」的机制。** `retro` 的描述是：**「Suggest improvements to the coding agent's environment (navigation, automated checks, coding standards, steering）」**——**定期回头优化给 Agent 的环境本身**，而不是只优化这次任务的做法。**这是把 harness 当成可迭代对象来运营。**

**第六，安装路径覆盖主流 harness，并区分「自动更新」与「手动更新」。** Claude Code 走 `claude plugin install mattpocock-skills@claude-plugins-official`（**默认自更新**）；Codex 走 marketplace + plugin（**启动时自更新**）；Copilot 走 marketplace + `autoUpdate`；Gemini CLI **手动更新**；其他 harness 走 `npx skills@latest add mattpocock/skills -a <agent>`。

**第七，安装器会问对问题，而不是猜。** `/setup-matt-pocock-skills` 每个仓库跑一次，问的是：**用哪个 issue tracker**、**triage 时打什么 label**、**文档存哪**。**「问不出来才问」是它整个设计的基调。**

## 后续发展建议

**这是本周唯一一个明确把「Skill 该不该接管流程」摆上台面正面回答的样本，答案对内部平台有直接含义。** 四个判断：

- **「Skill 提供能力，流程框架拥有流程」是一条值得站住的分工线。** 本周 `github/spec-kit`（+4,045）与 `mattpocock/skills`（+9,635）**同时在榜、方向相反**：spec-kit 是「给你一整套流程，用它或者改它」，mattpocock 是「给你一堆能力，流程你自己拼」。**两者不互斥，用户画像不同**——spec-kit 适合团队统一交付口径，skill 合集适合工程师保留控制权。**内部平台建议明确选边：提供可组合、可替换的流程原语，而不是一条不可绕过的流程。** 这与 spec-kit 自己的路线一致（见 [spec-kit 深读](./spec-kit.md)）。

- **「user-invoked / model-invoked」这条轴应该成为内部平台 Skill 规范的强制字段。** 当前多数 skill 目录靠名字约定隐式区分，**Agent 可能把编排类的也自动加载**。建议把「触发方式」写成显式元数据，**编排类默认只允许用户显式调用**。成本极低，却能避免一整类「Agent 自己编排自己」的失控。

- **「先拷问再动手」应当是任务入口的标准动作。** `grill-me` 的逻辑是：**需求不清是失败模式的源头，澄清成本远低于返工成本**。这与 A2A 调研的结论一致——**跨信任边界时最贵的不是协议实现，是把需求猜错**。建议 Agent 接到模糊任务时**默认先走一轮结构化澄清**，结论沉淀成可交接产物（`to-spec` 那一环）。

- **「环境也是可迭代对象」值得纳入 harness 运营。** `retro` 提示了一个常被忽略的问题：**Agent 表现不好时，第一个该改的不是提示词，是它所处的环境**——导航方式、自动检查、编码规范、上下文供给。**只提供「更强的模型 + 更好的提示词」，收益很快见顶；提供「让 Agent 更容易找到正确上下文」的环境改造，收益更持续。**

**风险与局限**：**318,693 star 配 226 open issue（0.07%）**，issue 密度极低，是本期维护健康度最好的样本；最新 release **v1.3.2（2026-10-29）**。它**自带商业属性**：README 直接推自己的付费 newsletter（~60,000 订阅者），**skill 仓库同时是内容漏斗**——**设计会持续向「教学向」倾斜**，但不该假设每个 skill 都从真实痛点反推而来。内容上它是**个人经验结集**，**没有 eval、成功率数字或案例复盘**——**这既是简洁之处，也是证据强度上限**。它**明确点名 GSD / BMAD / Spec-Kit 并与之对立**，但也**把自己放在有对立面的位置上**——这些框架一改进，它的一部分论证就会过时。另外 **skill 数量在增长，Reference 已是长列表**，**「可组合」的收益会随数量上升而递减**。

## 下一步

- 想看流程原语那条路线的具体做法 → [spec-kit 深读](./spec-kit.md)
- 想看反 AI 味设计那条线 → [interface-skills 深读（界面 skill 合集）](./interface-skills.md)

## 如果你想

- 想看可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)
- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
- 想看团队落地的方法论 → [AI Native 方法论](../../../ai-harness/index.md)
