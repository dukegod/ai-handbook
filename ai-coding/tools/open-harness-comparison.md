---
title: 四个开源 Harness 对比：Pi / DeepSeek Harness / Codex CLI / OpenCode
description: 同为「模型之外的运行时」，四家给出四种不同的内核设计——减法、拆分、加法、折中，以及各自的适用边界
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-10-10
verifiedWith:
  sources:
    - name: DeepSeek Harness 官网
      url: https://deepseek.com/harness/
      accessedAt: 2026-10-10
    - name: DeepSeek Harness GitHub
      url: https://github.com/deepseek-ai/deepseek-harness
      accessedAt: 2026-10-10
    - name: OpenCode GitHub
      url: https://github.com/anomalyco/opencode
      accessedAt: 2026-10-10
    - name: Codex 官方产品页
      url: https://openai.com/codex/
      accessedAt: 2026-10-10
    - name: Pi 文档（第三方整理）
      url: https://agentic-ai.readthedocs.io/en/latest/AgentHarness/pi-dev/
      accessedAt: 2026-10-10
---

# 四个开源 Harness 对比

> **TL;DR**：这四家不是同一层的东西。真正的差别不在功能多少，在**「内核里放什么」这个决定**——Pi 做减法、DeepSeek Harness 做拆分、Codex CLI 做加法、OpenCode 走折中。**目前没有共识。**

⏱ 预计阅读时间：8 分钟

## 你能在这里学到

- 四家在内核设计上做了哪些不同选择
- 「harness」这个词为什么会在 2026 年成为独立的产品层
- 每家的适用边界——什么时候该选哪种，不要一刀切
- 为什么「开源 CLI + 闭源产品」是当前主流做法

## 一、先看结论

| | 内核里有什么 | 立场 | Star（2026-10-10） |
|---|---|------|--------|
| **Pi** | 4 个工具 + <1000 token 提示词，其他全推到扩展 | **减法**：功能多是缺陷 | 未实测 ⚠️ |
| **DeepSeek Harness** | Cordis 内核（只管插件装载/卸载/依赖）+ 一切皆插件 | **拆分**：内核不预设什么是能力 | **246.6k** |
| **Codex CLI** | 完整 agent loop + OS 原生沙箱 + hooks / skills / MCP | **加法**：能力做扎实 | **127.6k**（10-01） |
| **OpenCode** | build / plan 两个内置 agent + general subagent | **折中**：够用就开箱 | **212.5k** |

> ⚠️ Pi 的 star 数本轮未实测（GitHub 页面未抓取）。第三方只笼统说「stars 很高」，未给具体数字。

## 二、一个共同信号：harness 已经成为独立的产品层

**这四家都在同一个词上撞车：harness。**

- DeepSeek 官网直接写：**Agent = Model + Harness**
- Pi 把自己定位成「terminal coding agent **harness**」
- Codex 开源出来的那个部分叫「**agent harness**」
- OpenCode 被中文技术博客归为「一个 Harness 范式的实战样本」

为什么这个词今年突然到处都是？因为模型能力差距在收敛，但**模型之外的运行时差异极大**——上下文怎么组装、工具怎么调、权限怎么管、沙箱怎么隔离、状态怎么恢复、多 agent 怎么编排。这些东西决定了同样的模型在不同 harness 里表现差多少。

**换句话说：模型的差距在缩小，harness 的差距在放大。**

## 三、逐个拆解

### Pi：唯一做减法的

作者是 **Mario Zechner（libGDX 作者）**，MIT，仓库 `earendil-works/pi`。

设计论点很硬：

> a coding agent needs exactly **four tools** — read, write, edit, bash — and a system prompt **under 1,000 tokens**. Everything else is opt-in via a typed TypeScript extension system.

**刻意不做**（官方口径是「每个都是设计决定，不是功能缺失」）：

| 功能 | Pi 的立场 |
|------|----------|
| MCP | 不内置，CLI 工具靠 README 实现 |
| 子代理 | 不内置 |
| 权限弹窗 | 不内置，主张用容器隔离 |
| Plan Mode | 不内置 |
| 待办清单 | 不内置 |
| 后台 bash | 不内置，建议用 tmux 保证可观测 |

他反对 MCP 的理由值得记：**有些 MCP server 在干正事之前就占掉相当一部分上下文窗口**。他的对策是「小工具 + 可读文档 + 专用 skill」。

作者的动机更直白：他受够了那些「像飞船、80% 功能没人用」的 agent。

**四个运行模式**：交互 TUI / Print-JSON / RPC / SDK。

**树状会话历史**——这是四家里最有想法的设计。会话存成树形 JSONL，可以从任意历史节点分叉、试另一条路，所有分支共存于同一文件。避免了线性对话的沉没成本。

> **Pi 还是 OpenClaw 的底层 coding agent。** 仓库里的 OpenClaw 那 145k star 平台，底座就是 Pi。

### DeepSeek Harness：内核最小，但插件最大

已发布桌面端（macOS Apple 芯片 13+ / Windows 64 位 10+）+ Web UI（`npx dsh`）+ 源码安装三种用法，MIT。

**Cordis 内核的职责边界是这家的关键设计**：

> Cordis 内核**只负责插件的加载、卸载和依赖关系，不承载 Agent 的具体能力**。

这条边界正是「UI 本身也是插件」能成立的原因——内核对「什么是能力」毫无预设。

**与 Pi 的关键区别**：Pi 是「功能少所以核心小」，DeepSeek 是「核心小但能力全在插件里，插件可以无限加」。所以 DeepSeek 能在配置层拼出 4 种模式，Pi 的默认形态就是它自己。

| 模式 | 能力 |
|------|------|
| 标准模式 | 文件编辑、Shell、文件与网页检索、Skills、计划、目标、子代理、工作流 |
| **PTC 模式** | 标准模式全部 + Code Mode SDK，让模型用一个 TypeScript 程序组合多步操作 |
| 极简模式 | 仅持久 `bash` 与 `str_replace_editor` 双工具 |
| 创造模式 | 标准模式全部 + 检查运行时、在内存中试验 Cordis 插件、据此创作新 preset |

**两样 Pi 和 OpenCode 都没有的**：

1. **Trajectory 视图**——仅追加设计的会话日志，记录系统提示词、思维链、工具调用与结果、子 Agent 调度、每一次上下文注入。三条泳道（输入/模型/工具）× 五类记录，每步可展开概述/参数/结果/Schema/计时。恢复、分叉、检索、回放共享同一份事件流。
2. **Agent 可现场写插件**——创造模式下用对话创建，官网演示「帮我写个番茄时钟插件」全程工具调用可见，用时 5 分 24 秒完成并验证通过。

### Codex CLI：唯一开源 agent loop 的商业产品

Rust 重写、**Apache 2.0**、127,608 star（2026-10-01）。

**开源与闭源的分层是刻意的**：

| 开源（Apache 2.0） | 闭源 |
|---|---|
| CLI、SDK、App Server | 桌面 App、IDE 扩展 |

把 agent loop 交出去让人审，把交互界面留作商业资产。

**OS 原生沙箱默认开启**——这是它区别于其他三家的硬安全设计：

| 平台 | 沙箱 |
|------|------|
| macOS | Seatbelt |
| Linux | bubblewrap |
| Windows | Windows Sandbox |

官方描述是「提供比单纯权限提示更强的隔离，减少意外破坏」。**安全靠隔离，不靠弹窗**——和 Pi 的主张意外地一致，但实现方式不同（Pi 是建议你上容器，它是内置 OS 级隔离）。

其他：原生 subagents、MCP 双向（既做 client 也能当 MCP server 被 Claude Code 调用）、Automations（定时任务）、hooks、skills。

> ⚠️ 第三方评测称它「每任务 token 消耗约为 Claude Code 的 1/4」「并行云端任务是真优势，但紧密耦合的重构是弱项」。**这是第三方口径，非官方数据**，未找到官方对照实验。

### OpenCode：折中派

仓库已从 `sst/opencode` 迁到 **`anomalyco/opencode`**（Anomaly 公司），MIT，212.5k star。

内置 agent 只有三个，Tab 键切换：

| Agent | 行为 |
|-------|------|
| **build** | 默认，全权限，开发用 |
| **plan** | 只读。默认拒绝文件编辑，bash 命令需许可 |
| **general** | subagent，用于复杂搜索和多步任务，用 `@general` 调用 |

比 Pi 完整、比 Codex 简单。第三方对比的原话：「Pi 是 4 工具极简 harness，OpenCode 是多工具全功能 harness」。

LSP 集成、75+ 模型提供商、client-server 架构（可远程驱动）。

> ⚠️ **OpenCode 的沙箱模型本轮未查到**，README 未提及。它有 `plan` agent 的权限控制，但那是 agent 层的行为约束，不等于 Codex 那样的 OS 级隔离。

## 四、按需求选

| 你的处境 | 选 | 理由 |
|---------|-----|------|
| 想搞懂 harness 到底怎么运作 | **Pi** | 4 个工具读得完，1000 行以内能吃透整个 agent loop |
| 要给团队做可审计、可自定制的运行时 | **DeepSeek Harness** | 能力全在插件、Trajectory 可追溯、Agent 能自己写插件 |
| 企业要控制供应链但想要成熟能力 | **Codex CLI** | Apache 2.0 + OS 原生沙箱 + 多端统一 |
| 想要个够用就开箱的开源替代品 | **OpenCode** | MIT、212k star、build/plan 切换 |
| 已经在用 OpenClaw | **Pi** | OpenClaw 的底座就是它 |
| 需要深度可观测性 | **DeepSeek Harness** | 四家里只有它有完整的运行轨迹视图 |

**不适合选的场景**：

- **生产环境 + 要求 API 稳定** → DeepSeek Harness 仍是预览版，官方明示「部分功能和体验仍在持续完善」
- **需要开箱即用** → Pi 和 DeepSeek Harness 都要自己组装能力栈
- **想要 MCP 但不想装适配器** → Pi 不内置 MCP

## 五、共同点与分歧

**四家共同点**（这部分已经收敛了）：

- 都用 `AGENTS.md` 作为项目指令入口
- 都支持 Anthropic + OpenAI 系模型（Pi 和 OpenCode 支持 75+ / 15+ 提供商）
- 都开源、都有终端入口
- 都把会话持久化当作一等公民

**四家分歧**（这部分没共识）：

| 维度 | 分歧 |
|------|------|
| 内核大小 | 4 个工具 vs 完整 agent loop |
| MCP | 不内置（Pi）/ 插件提供（DSH）/ 原生双向（Codex） |
| 权限模型 | 靠容器（Pi）/ 靠 agent 行为（OpenCode）/ 靠 OS 沙箱（Codex） |
| 可观测性 | 只有 DSH 有完整 Trajectory |
| 插件谁写 | 人写扩展（Pi）/ **Agent 自己写**（DSH）/ 官方内置（Codex、OpenCode） |

## 六、值得注意的一个现象

**这四家的 star 数排序和它们的「极简程度」完全不相关。**

DeepSeek Harness（246.6k）内核最小、OpenCode（212.5k）只内置三个 agent、Codex（127.6k）是完整实现——三者都排在前面。而设计哲学最激进、代码量最小的 Pi，第三方只说「stars 很高」却给不出具体对比。

这说明：**star 数反映的是「有多少人想换个不被厂商锁定的运行时」，不是「内核有多优雅」。** 开源 harness 的需求主要来自供应商锁定焦虑，而不是架构偏好。

这也是 DeepSeek Harness 能到 246k 的原因——它是**模型厂商自己开源的 harness**，等于官方背书「你可以不用我的模型，但可以用我的运行时」。

## 未核实项

- **Pi 的 star 数**：本轮未实测
- **OpenCode 的沙箱模型**：README 未提及，未找到官方说明
- **Codex 的 token 效率与并行优势**：第三方评测口径，无官方对照数据
- **OpenCode 从 sst 迁到 anomalyco 是否有 API / 行为变更**：未查
- **Pi 的设计细节**：本轮依据的是第三方整理文档（readthedocs、promptgenius 等），未直接读 pi.dev 官网与源码仓库

## 参考

- [DeepSeek Harness 深度评测](./deepseek-harness) — 含 Trajectory 与插件生态细节
- [PI-agent 深度评测](./pi-agent) — 含 pi-ai / pi-agent-core 分层与扩展机制
- [AI 工具全景](./overview)
- [Agent 工作台的产品形态与设计取舍](./agent-workspace) — 闭源产品侧的形态收敛

## 下一步

- 看闭源产品怎么收敛形态 → [Agent 工作台的产品形态与设计取舍](./agent-workspace)
- 选工具 → [AI 工具全景](./overview)

## 如果你想

- 深入 DeepSeek Harness → [DeepSeek Harness 深度评测](./deepseek-harness)
- 深入 Pi 的扩展机制 → [Pi 配置文件详解](./pi-coding-agent/configuration) / [Pi 进阶资源加载](./pi-coding-agent/resources)
- 团队怎么落地 → [团队 AI 工作流](/ai-harness/workflows/team)