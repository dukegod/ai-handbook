---
title: 'backnotprop/plannotator：把「人在环路」从提示词里拆成一层产品'
description: plannotator 深度解读——本地浏览器评审面、11 个 harness 的接入方式、Plannotator Inbox 与多 Agent 评审回路、双协议开源与隐私边界，以及「从 Agent 提问到人的判断被收到」这段延迟
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-16
---

# backnotprop/plannotator：把「人在环路」从提示词里拆成一层产品

> **TL;DR**：11,973 star、1,090 fork，**本周涨星 +1,719，涨星占存量 14.4%**。**Apache-2.0 或 MIT 双协议**（任选），TypeScript，仓库建于 **2025-12-28**，最新版本 **v0.28.65（2026-11-15）**，最近一次提交 2026-11-16——**补丁号已经到 28 位，说明它几乎每天都在发版**。105 个 open issue、65 个 open PR。

📅 数据窗口：2026-11-10 ~ 2026-11-16 ｜ 🏷️ Agent 协作 / 人在环路 ｜ 本周涨星 +1,719 ｜ 总 star 11,973

## 是什么

[backnotprop/plannotator](https://github.com/backnotprop/plannotator) 是一个**本地运行、浏览器打开的评审面**，专门给 AI 编码 Agent 用。它通过 plugin、hook 和 command 直接挂进 Agent：**当 Agent 提出一个决定、一份计划、一个 HTML，或者干完活时，浏览器会自动打开评审面**，你标注、评论，**反馈直接回到 Agent 让它执行**。

三块能力：

- **评审文档、计划与 Agent 消息**——标注计划、规格、消息、HTML，把反馈送回 Agent。
- **代码评审**——支持本地改动、GitHub PR、GitLab MR、GitButler 工作区、`jj`（Jujutsu）、`p4`（Perforce），也能直接喂一个静态 unified diff 文件。
- **Plannotator Inbox**——一个本地窗口，Agent 在你回复期间继续干活，把消息、问题、文件和引导式评审留给你；**回复回到提问的那个会话**。

另有 **Herdr Annotate** 把这套评审搬进终端（`brew` / 插件安装），以及独立的 **Plannotator TUI**。

接入面很宽：README 明确列出 **Claude Code、Codex、Copilot CLI、Gemini CLI、OpenCode、Kiro、Droid、Amp、DeepSeek Harness、Pi**，外加个人助理（Grok Bot、Muse、Hermes、OpenClaw）。Claude Code、Pi、OpenCode 走插件直接接，**其余 Agent 走 MCP（`plannotator inbox mcp`）**，并且 `plannotator inbox --help` 就是给 Agent 读的说明书。

## 技术亮点

**第一，它的接入点选在「Agent 结束这一轮的时刻」，而不是「Agent 请求权限的时刻」。** README 写得很具体：**在 Claude Code 2.1.287 及以上，plan review、code review 和 annotate 都不让 Claude 等待——Claude 结束它的回合，你的决定稍后作为一条消息到达**（`PLANNOTATOR_CLAUDE_MOD=0` 可退回经典阻塞式流程）。**这是本周所有 Agent 工具里唯一明确把「异步评审」当成产品语义来做的**——它改变的是交互模型，不是功能。

**第二，「Nothing holds an agent session open while you do」是一个被写进文档的产品原则。** 人不在的时候 Agent 继续跑，人回来时按需处理；Inbox 把多个 Agent 的线程按「各自需要什么」分组，手机上也能答。**这解决的是多 Agent 场景的真实瓶颈：不是 Agent 不会干，是人成了串行瓶颈。**

**第三，隐私边界写得非常具体，是这周读过最细的一份。** 不收集使用埋点和分析；计划、diff、标注、草稿、历史、配置默认全在本地。**唯一的例外是「每个评审面加载时会向 GitHub 查一次最新 release」**——README 明说不发任何计划或评审内容，且**当前没有开关**。本地 Git 评审会用 `git ls-remote` 探测默认分支与过期基线，**不发本地 diff**，且明确说「从不设定时器，闲置的评审页不会发起任何网络请求」，可以用 `--no-git-remote-check` / `PLANNOTATOR_GIT_REMOTE_CHECK=0` / 配置项关掉。分享方面：小 markdown 压进 URL fragment（**不加密**），大段 markdown 与原始 HTML 走短链服务，**AES-256-GCM 加密后只上传密文、密钥留在 URL fragment**，托管的粘贴 **7 天过期**，服务可自托管。

**第四，它的开源模型正在从「链接分享」转向「托管工作区」。** README 写明开源的异步链接分享「为兼容性保留，但正在转向弃用支持」，**Workspaces 是团队分享的主方向**（独立托管产品，开源 App 的本地存储模型不适用于放进那里的内容）。**这是一家开源产品向 SaaS 演进的完整路径，值得作为「开源 Agent 工具怎么赚钱」的样本。**

**第五，安装器把 11 个 harness 的差异全部吸收掉。** 一条 `curl … | bash`（Windows 有 `.ps1`）装好二进制、自动探测已装的 Agent 并配置各自的 hook、skill 和 slash command；`--minimal` 只装二进制。**README 里那张表逐个写清了每个 harness 要补哪一步**——比如 Codex 用的是实验性 `Stop` hook，Windows 原生上 hook 仍是实验性的、安装器会打印手动配置步骤。

## 后续发展建议

**最重要的判断是：多 Agent 平台的下一层竞争，不是「Agent 怎么协作」，而是「人怎么在最短路径上把判断塞回 Agent 的上下文」。** 四个判断：

- **「人在环路」已经从提示词里的一句话变成了有版本、有协议、有隐私边界、有付费路径的独立产品层。** 这不是某个作者的偏好，而是**多个项目同时收敛到同一个位置**：EGM 让 Goldfish 当独立评审者（本期深读）、OpenMausBot 用 permission broker 挡审批（W46 深读）、Game Studios 写死「没有你的签字什么都不落盘」（W46 深读）、plannotator 把评审做成产品。**内部平台如果还在用「请人工确认一下」这种提示词约定，就落后了一层。**

- **衡量指标应该是延迟，不是自动化率。** 真正的成本是「从 Agent 提出问题」到「人的判断被 Agent 收到」这一段的时间。plannotator 的答案很具体：**评审不阻塞 Agent 回合**（Claude Code 2.1.287+）、Inbox 汇总多 Agent 线程、手机可答。**建议内部平台把「Agent 等待人的时间」当成一等指标去度量**，而不是看「有多少步骤不需要人」。

- **评审面的价值在于它统一了「产物」的形态。** plannotator 能标注计划、规格、消息、**渲染后的 HTML**，也能做代码评审——**同一个反馈通道覆盖从设计到 diff 的全链路**。内部平台的启示是：**如果要做一个「人给 Agent 反馈」的入口，入口必须能接住各种形态的产物**，否则人就得在不同工具之间切换，反馈延迟反而上升。

- **它的本地优先 + 精确披露网络边界，是内部平台可以直接抄的隐私基线。** 它把「什么时候会发请求」「发了什么」「怎么关」全部写在 README 里。**内部平台一旦引入外部 Agent 工具，这条基线应该变成准入门槛**——否则「Agent 读了我们的代码」这个问题永远无法回答。

**风险与局限**：**补丁版本号 v0.28.65 意味着 API 仍在高频变动**，接入方需要自己锁版本；**105 个 open issue、65 个 open PR 对 11,973 star 来说比例不低**（issue/star ≈ 0.88%），说明需求杂、兼容矩阵宽（11 个 harness × 各自的 hook / command / skill 机制）；**开源链接分享正在弃用、团队分享转向托管的 Workspaces**，这意味着**团队协作路径上它已经不是一个纯本地方案**；Windows 原生上 Codex hook 仍是实验性的；最后，它依赖各 harness 的 hook / Stop 事件做拦截，**harness 改机制，它就得跟着改**。

## 下一步

- 想看同一问题的「评审者隔离」方案 → [EGM 深度解读（本期同期项目）](./elephant-goldfish-model.md)
- 想看跨会话记忆怎么做 → [claude-mem 深度解读（往期）](../2026-W45/claude-mem.md)

## 如果你想

- 想理解多 Agent 为什么需要职责分离 → [AI Native 方法论](../../../ai-harness/index.md)
- 想看协议层的可信传递问题 → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)
- 想看 Agent 工具全景 → [AI 工具全景](../../../ai-coding/tools/overview.md)
