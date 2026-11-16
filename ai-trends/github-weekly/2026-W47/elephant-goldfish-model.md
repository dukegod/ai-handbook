---
title: 'google/elephant-goldfish-model：评审的关键是「没有前情的新上下文」'
description: EGM 深度解读——Elephant / Goldfish / You 三角色分工、用全新 subagent 做独立评审、五阶段评审流程与文档漂移报告，以及「隔离上下文比约束措辞有效」这个可直接抄的机制
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-16
---

# google/elephant-goldfish-model：评审的关键是「没有前情的新上下文」

> **TL;DR**：19,875 star、1,477 fork，**本周涨星 +5,060，涨星占存量 25.5%**——新项目爆发。Apache-2.0，Python，仓库建于 **2026-09-13**，最新版本 **EGM v0.1.1（2026-11-06）**，最近一次提交 2026-11-15。Google 官方的开源插件，但 README 末尾写明：**This is not an officially supported Google product**。

📅 数据窗口：2026-11-10 ~ 2026-11-16 ｜ 🏷️ Agent 协作 / 独立评审 ｜ 本周涨星 +5,060 ｜ 总 star 19,875

## 是什么

[google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model)（EGM）是一套给 AI 助手用的**规格起草 + 独立评审**工作流。口号是「**Design with an elephant. Review with a goldfish.**」——大象记性好，金鱼记性差。

角色分工在 README 里是一张三行表：

| 角色 | 上下文 | 职责 |
| --- | --- | --- |
| **Elephant** | 你的项目、需求和之前的决策 | 探索问题、起草规格 |
| **Goldfish** | **文档 + 被引用的源码，但没有之前的对话** | 找出缺失的假设、不清楚的需求和实现风险 |
| **You** | 真正重要的目标和约束 | 解决权衡、批准设计、决定做什么 |

七个 skill 可单独使用，不要求走完整流程：`egm-brainstorm`（理清想法、写概念简报）、`egm-draft`（转设计文档）、`egm-resolve`（逐条处理评审意见）、`egm-bootstrap`（补建文档）、`egm-review`（新 Agent 分五阶段评审）、`egm-review-loop`（挑一组评审者）、`egm-drift-report`（文档与源码逐条对比，报告偏离）。

安装方式覆盖了主流 harness：Claude Code 与 Codex CLI 都走 `plugin marketplace add` + `plugin install`；**Antigravity CLI 一条 `agy plugin install` 搞定**；ChatGPT / Codex 桌面端有已上架的插件。

## 技术亮点

**第一，Goldfish 的上下文定义是整个项目最值钱的一行。** README 的表格写的是：**「文档 + 被引用的源码，但没有之前的对话」**。这不是修辞，是实现约束——Goldfish 必须在**全新 subagent 上下文**里跑。README 还有一句更硬的：**「Goldfish reviews require fresh subagent contexts. If your agent cannot create them, EGM stops the review.」**——harness 不支持创建全新 subagent，**EGM 直接停止评审，不降级成同会话自评**。**「评审必须有独立的评审者」被做成了会失败的功能，而不是一句建议。**

**第二，评审分五个阶段，且是「新鲜评审者」而不是「新鲜提示词」。** README 描述的流程是：先探索想法（fresh reviewers challenge the proposal），把结论写进 `concepts_brief.md`；再起草规格（`design_draft.md`，每写完一节就停下来等你反馈）；然后用新评审者检查设计本身、清晰度、与代码的契合度、实施计划；**最后你批准，才让编码 Agent 去实现**。批准过的规格存在 `docs/designs/` 下。

**第三，`egm-drift-report` 解决的是「文档腐化」这个长期问题。** 它把每个文件夹里的文档与当前源码对比，报告偏离，**然后由你决定是改文档还是改代码**——多数工具只管生成文档，不管文档什么时候开始骗人。

**第四，它把「评审」做成了可以单独跑的能力。** `/egm:egm-review docs/designs/webhooks.md` 就能直接评审一份既有设计文档、README 或 PR 计划，**不需要先走一遍起草流程**。

**第五，README 把「不能做什么」写得很克制。** 它明说：内置的起草与设计评审流程**针对软件规格**；别的文档要用 `/egm-review-loop` 自己挑评审者和标准；bootstrap 和 drift report **只适用于代码库**。另外写了 **「A review does not replace tests or human judgment」**。

## 后续发展建议

**最重要的判断是：「换人评审」比「换提示词评审」有效，而这件事的门槛只是 harness 能不能创建 subagent。** 四个判断：

- **当前 Agent 的自我评审几乎无效，根因不是提示词写得不好，而是评审者继承了作者的推理路径，也就继承了作者的盲点。** EGM 的机制直接把这条根因消掉：**新上下文 + 只给文档和源码 + 不给对话历史**。**这条机制的成本极低——它不是新组件，就是一条「评审必须由独立 subagent 执行」的执行规则。建议内部平台把「评审任务的执行者必须是新建子会话、且不继承作者对话历史」写成硬约束**，这比任何评审模板都更可能改变结果。

- **「评审者必须能看到相关源码、但看不到作者的思考过程」是一个可以直接复用的上下文裁剪策略。** 内部场景里复核方案失败，通常是两个极端：要么把整个会话转过去（盲点一起转过去），要么只给结论不给代码。**EGM 的裁剪点值得原样抄：给产物 + 给被引用的源码，不给过程。**

- **独立性的另一个维度是「角色不能自我批准」。** EGM 的三行表里，**Goldfish 只找问题、不做决定；You 做权衡和批准；Agent 不自我批准**。这和 OpenMausBot 的 permission broker、W46 的 Game Studios「没有你的签字什么都不落盘」是同一条线索：**多 Agent 系统的可信度来自职责分离，而不是来自更强的模型。**

- **`egm-drift-report` 是最容易被低估的能力。** 大多数团队的文档问题是「写完就过期」，而**过期的规格比没有规格更危险**——Agent 会照着过期文档实现。建议把「文档与代码的偏离检测」当成一类**常规 CI 检查**。

**风险与局限**：**版本号还是 v0.1.1（2026-11-06 发布）**，距建仓才两个月多，说明**协议与流程仍在调整**；**74 个 open issue、40 个 open PR** 对 19,875 star 来说是活跃的早期信号；README 写明**「This is not an officially supported Google product」**——**投入前要按第三方项目评估**；对 harness 的依赖很硬：**不支持 subagent 的环境直接不可用**（Claude Code、Codex、Antigravity 都支持）；README 里连具体 issue 编号都给了（`#220`、`#196`：agy CLI 1.4.10 会把无前缀命令补成带前缀，1.4.8 不会），**说明它正在处理 harness 之间的命令解析差异——这类差异是「一套流程跑多个 harness」的常态成本**。

## 下一步

- 想看同一层问题的另一面（组件级设计约束）→ [astryx 深度解读（本期同期项目）](./astryx.md)
- 想看「人在环路」如何独立成产品层 → [plannotator 深度解读（本期同期项目）](./plannotator.md)

## 如果你想

- 想理解多 Agent 为什么需要职责分离 → [AI Native 方法论](../../../ai-harness/index.md)
- 想看协议层的可信传递问题 → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)
- 想看 Agent 工具全景 → [AI 工具全景](../../../ai-coding/tools/overview.md)
