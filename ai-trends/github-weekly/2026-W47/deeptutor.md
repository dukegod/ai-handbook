---
title: 'HKUDS/DeepTutor：Agent 原生的学习工作台，以及一个自己做的 skill 注册表'
description: DeepTutor 深度解读——五区域工作台模型、EduHub 与 ClawHub 双注册表、MCP Services 与 CLI Apps 的授权模型、bounded tutoring memory，以及「谁来定义学习空间、谁来分配权限」的架构判断
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-11-16
---

# HKUDS/DeepTutor：Agent 原生的学习工作台，以及一个自己做的 skill 注册表

> **TL;DR**：59,530 star，**本月涨星 +18,278，涨星占存量 30.7%**（本周未进周榜，月榜第 8）。Apache-2.0，Python，仓库建于 **2025-12-28**，**最新版本 v1.7.3 于 2026-11-16 发布**——也就是今天。最近一次提交 2026-11-15。124 个 open issue、167 个 open PR。**发版节奏极密**：2026-10-04 到 11-16 之间至少 15 个版本，近三周基本每 2～3 天一版。arXiv 编号 2604.26962。

📅 数据窗口：2026-11-10 ~ 2026-11-16 ｜ 🏷️ Agent 平台 / 学习工作台 ｜ 本月涨星 +18,278 ｜ 总 star 59,530

## 是什么

[HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) 由香港大学 HKUDS 团队（Data Intelligence Lab @ HKU，负责人 Bingxi Zhao）主导，README 写得很清楚：**fully open-source form，built together with the community，目前没有任何付费在线产品**。README 顶部同时挂着一条 **「We're actively recruiting maintainers!」**。

它对自己的定义是 **an agent-native learning workspace that connects tutoring, research, creation, and practice in one extensible system**。

工作台按五个区域组织，边界划得很细：

| 区域 | 作用域 | 内容 |
| --- | --- | --- |
| **Home / Learning / Resources** | 工作区 | 每个学科或项目一个 workspace，首页 / 学习 / 资源随当前 workspace 切换；含聊天记录、收藏、学习日志、题库、知识中心 |
| **Partners** | 账号 | 持久陪伴者、Partner Groups、资源访问、IM 渠道（支持微信扫码登录） |
| **Personalization** | 账号 | My Agents、Personas、Skills、MCP Services、CLI Apps、Memory、Settings |

技术底座包括：LightRAG（一等公民，自研集成）、WeKnora、PageIndex OSS、GraphRAG 索引、**可微的引用**、Mastery Path（掌握路径）会按模式开关工具、**bounded tutoring memory**（有边界的辅导记忆）、13 种语言的界面。

## 技术亮点

**第一，它把 skill 生态做成了「多注册表 + 统一导入门」，这是本周最完整的实践样本。** DeepTutor 的 skill 用的是**开放的 Agent-Skills 格式**——一个文件夹 + `SKILL.md`（YAML frontmatter + Markdown）+ 可选参考文件，**README 明确说「Nothing about it is DeepTutor-specific, so any registry that speaks the format becomes a source for your library」**。它内置两个 hub：

- **EduHub**——自建的、专注教学的 skill 注册表，收录苏格拉底导师、闪卡生成、作文反馈等。
- **ClawHub**——作为一等来源内置兼容。

安装走 CLI：`deeptutor skill search "socratic tutor"` / `deeptutor skill install socratic-tutor`（**fetch → verify → register**）/ `deeptutor skill install eduhub:socratic-tutor@1.2.0`（**可钉版本**）/ `deeptutor skill publish ./my-skill`（**交互式发布：选赛道 + 标签**）/ `deeptutor skill update`（回滚或发新版）。**EduHub 本身也是独立的 ClawHub 兼容注册表**，Claude Code、Codex 等非 DeepTutor 的 Agent 可直接用 `npx eduhub install socratic-tutor`。新增注册表只需在 `data/user/settings/skill_hubs.json` 里加一条：`type: "clawhub"` 指向兼容 HTTP API、`type: "command"` 包装任意 fetch CLI、`"default"` 指定裸 slug 走哪个 hub——**全部走同一个导入门**。

**第二，导入社区 skill 要过一道安全门。** README 写的是「download a skill straight into your library… **through a security gate**」。**这是本周读到的唯一把「社区 skill 导入」当成安全问题处理的实现**——社区 skill 的本质是「别人写的提示词在你机器上跑」。

**第三，权限模型是按「资源 × 授权」两维组织的，不靠模型自觉。** README 的原话：**MCP Services authorize external tools，CLI Apps expose installed programs from the CLI-Anything catalog through the execution sandbox，而 workspace assignments and user grants determine which resources each turn may use.** 也就是说：**每个 Agent 回合能用哪些资源，由工作区分配和用户授权共同决定**。**「凭据被移出沙箱可及范围」（v1.5.7）也是同一个思路的延续。**

**第四，CLI 同时服务人和 Agent，但用两种形态。** 一个 `deeptutor` 二进制两种入口：面向人的**交互式 REPL**，以及面向 Agent 的**结构化 JSON**——「Same capabilities, tools, and knowledge bases either way」。**这正是内部平台该抄的分层：人用交互界面，Agent 用结构化接口。**

**第五，它把「记忆」当作需要设上限的资源。** v1.6.15 的 release note 写的是 **bounded tutoring memory**，v1.5.8 还有 **bounded LLM client and index caches**。**在人人谈「Agent 记忆」的时候，它先把记忆和缓存都做了上限——这是一个务实的反向信号。**

## 后续发展建议

**最重要的判断是：本周两个项目（DeepTutor 的 EduHub、Jane Street 的 agent_skills）用不同方式确认了同一件事——skill 正在变成跨行业的通用载体，而「谁来审 skill」会变成平台职责。** 四个判断：

- **「skill 是别人写的提示词在你机器上跑」这句话决定了 skill 注册表的治理模型。** EduHub 的做法是**统一导入门 + 签名式验证（fetch → verify → register）+ 版本钉选 + 可回滚**，并且**允许自建 hub 但都走同一道门**。**这是本周最值得抄的内部平台设计**：如果内部要建 skill 库，**「所有来源走同一个导入门」比「每个来源各自信任」重要得多**；至少要有**版本钉选 + 可回滚 + 来源标记**三件事。

- **「授权」和「可执行」分层，是 Agent 平台该抄的权限模型。** DeepTutor 把 MCP Services（授权外部工具）和 CLI Apps（暴露已安装程序 + 执行沙箱）分开，再叠加工作区分配和用户授权决定每回合可用资源。**与 W46 讲的 OpenMausBot permission broker 同向**——**它不是给 Agent 一个大权限再靠提示词约束，而是把「哪些资源」显式建模成可分配的对象**。

- **「有边界的记忆」比「无限记忆」更接近可用。** v1.6.15 的 bounded tutoring memory 和 v1.5.8 的 bounded caches 是同一个信号：**Agent 记忆系统的第一个工程问题不是「怎么记得更多」，而是「什么时候该忘」。** **持久化那一侧在卷容量，边界那一侧在补上限。**

- **「开放格式 + 多注册表」是这个生态能长大的前提。** DeepTutor 明说不做任何 DeepTutor 专属的东西，因此任何说这个格式的注册表都能成为它的来源。**内部平台自建 skill 生态，最重要的决定不是做多少个 skill，而是选一个开放格式并让外部也能往里写**——**封闭生态做 skill 库，永远做不出生态。**

**风险与局限**：**发版密度极高（近三周每 2～3 天一版）**，**这既是活跃的证据，也是稳定性风险**——README 里反复出现「reliable / sturdier / recovery」这类修复型措辞；**124 个 issue、167 个 PR** 事务量相当高；**README 顶部挂「正在招募 maintainer」，说明维护人力不足**；**它是教育场景的产品**——Mastery Path、题库、Anki 导出、学习日志这套模型，**照搬到研发场景要重新设计，不是换皮**；最后，**它同时提供桌面应用、Web、CLI 三种形态 + 自建注册表 + 沙箱执行**，**运维面很宽**——参考架构可以，参考功能清单会超载。

## 下一步

- 想看 skill 生态的另一个跨行业样本 → [本期周报的新锐信号](./index.md#四新锐仓库近-30-天新建)
- 想看记忆系统这条线的另一端 → [claude-mem 深度解读（往期）](../2026-W45/claude-mem.md)

## 如果你想

- 想理解 Agent 平台怎么组织权限与资源 → [AI Native 方法论](../../../ai-harness/index.md)
- 想看 Agent 平台方向的方法论 → [AI 研发 Agent 平台](../../../ai-harness/agent-platform/index.md)
- 想看可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)
