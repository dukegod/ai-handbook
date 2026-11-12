---
title: 'milind-soni/OpenMausBot：把多 Agent 团队做成聊天应用，权限是一等公民'
description: OpenMausBot 深度解读——每个 bot 一个本地 CLI 与一台云电脑、permission broker 独立审批层、driver SPI 的可扩展性，以及它要替代的四个闭源个人 Agent 产品
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-09
---

# milind-soni/OpenMausBot：把多 Agent 团队做成聊天应用，权限是一等公民

> **TL;DR**：18,553 star、2,568 fork、841 open issue，Apache-2.0。**本周涨星 +7,621，涨星占存量 41.1%**——三个多月的新项目，八成 star 是这一周来的。README 有一张对照表，列出它要替代的四个闭源产品：**xAI 的 Grok Bot、Meta 的 Muse、OpenAI 的 dots、Manus 的 Cue**。**四个闭源个人 Agent 产品七周内集中发布，是这波热度真正的源头。**

📅 数据窗口：2026-11-03 ~ 2026-11-09 ｜ 🏷️ 多 Agent 协作 / 运行时安全 ｜ 本周涨星 +7,621 ｜ 总 star 18,553

## 是什么

[milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot) 的形态一句话说清：**「一个聊天应用里的 AI bot 团队」**。

核心主张有三条，README 里都有对应机制：

1. **每个 bot 都是一个真 agent，跑在你机器上的 CLI。** README 写得很具体：**bots run on the `claude`, `codex`, and `grok` CLIs installed on your own machine**——**用你自己的登录和订阅，不新开账号、中间不架代理**；harness server 跑在 `127.0.0.1`，transcript、key、事件全在 `~/.openmausbot`，**不上云**。
2. **每个 bot 都有自己的模型、自己的电脑、自己的应用。** 模型可按 bot 选（Claude / Codex 并排展示，不可用 provider 变灰并说明原因，**中途还能换模型**）；电脑可以是**云端 Linux 桌面**（带实时画面预览）、**隔离的本地 VM**，或在**平台安全边界已认证时**直接用你自己的电脑；应用通过 Composio 接入 500+ 个服务。
3. **引擎不锁死。** **可在 Settings → Engines 里把引擎指向任意自定义 CLI 二进制**。

README 专门声明：**「No affiliation with any cryptocurrency. OpenMausBot has no token.」**

## 技术亮点

**第一，permission broker 是独立的一层，这是整个架构最值得抄的地方。**

README 的架构图：

```
App (React + Tailwind) --HTTP 命令--> Harness server (127.0.0.1:8799)
                                      ├── Driver registry → Event bus → SSE
                                      └── Permission broker  ← 权限请求在这里汇聚
Agents (claude CLI / codex CLI / grok CLI) --权限请求--> Broker
```

**agent 不直接弹权限框，权限请求上行到 broker，由它决定和呈现。** 叠加「Bots ask before they act」，**审批变成了架构组件而不是提示词里的祈使句**。

**第二，driver SPI 的边界被刻意做小。** Status 章节写明：**「the driver SPI in `server/contracts.ts` is deliberately small; adding a provider is one file in `server/drivers/` plus a one-line registration」**——**加一个 provider = 一个文件 + 一行注册**。更进一步：**任何说 ACP 协议的 CLI、或任何 OpenAI 兼容端点，都能通过配置接进来，不用写代码**。

**第三，对外暴露的 MCP 控制面是「刻意收窄」的。** 它提供 stdio MCP server 给 Claude Desktop、Cursor 这类客户端，能查 bot 和 channel、读 transcript、建 bot 和任务、派活、等完成、切模型、打断 turn——**但明确不暴露**：审批授权、删除、任意设置、凭据、电脑生命周期。**「哪些能力不开放」被写进文档，是 Agent 工具里少见的克制。**

**第四，它同时提供无头 CLI 路径，能进 CI。** `openmausbot team apply team.yaml` 从文件建团队；`openmausbot run "Room Lead" "..." --export ./out` 给一个 bot 一件活、**等它和求助过的队友都干完**，再导出产物。输出支持 `--json`，退出码可被脚本分支。**「一支 Agent 团队」不只能人在聊天里用，也能被 CI 调用。**

**第五，它诚实标注了能力边界。** README 写明：**宿主机控制在 macOS 和 Ubuntu Xorg 上可用（需显式 opt-in），Ubuntu Wayland 下仍然禁用，等 issue #345 解决**。Status 章节也说 Ubuntu 仍是 beta，**托管 / 移动连通性还在建，webhook 触发用本地接收器而非常开中继**。**第六，隐私默认值保守**——使用分析可选且匿名，**从不记录 keys、姓名、地址或对话内容**。

## 后续发展建议

**这个项目最有价值的不是它实现了什么，而是它把「个人 Agent 团队」这个品类的验收标准写清楚了。** 四个判断：

- **「多 Agent 平台的竞争点正从协作能力移到审批能力」。** 它的协作是薄的——bot 各跑各的 CLI，靠聊天界面聚合，靠 broker 挡审批。**它没做任务图、调度、跨 bot 共享记忆，但用户依然觉得它有用，因为「每个 bot 有自己的模型和电脑、越权操作都要我点一下」就够撑起产品形态。** 内部平台若先做编排、后补审批，**顺序可能是反的**：审批不做对，编排越复杂只是更快地产生烂摊子。**建议把「权限请求的上行路径」当成一期需求。**

- **「复用你自己的登录和订阅」是对个人 Agent 市场最正确的解法。** 四个闭源产品（Grok Bot / Muse / dots / Cue）的做法是**模型、电脑、数据全在厂商那侧**；OpenMausBot 是**全在你机器上**。**这不是「开源版功能少」，是「信任边界画在了完全不同的位置」**。**边界画在「谁持有凭据、谁的数据不出内网」，这决定了内部场景能不能用**——建议明确回答：**Agent 的凭据和执行环境在谁的机器上？**

- **MCP 暴露面「刻意收窄」值得直接抄。** README 明确列出不暴露的四类能力（审批授权、删除、任意设置、凭据、电脑生命周期）。**给 Agent 开的 MCP 端口，每多暴露一个「能改状态」的能力，就多一条被诱导利用的路径。** 内部平台做 MCP / A2A 接口时**建议默认只读，写操作分级开启**——这与 [A2A 协议调研](../../industry/a2a-protocol.md) 是同一议题。

- **「从 Markdown 文件装一整支团队」把编排降级成了声明式配置。** `openmausbot team apply team.yaml` 加上 `--json` 输出和可分支的退出码，说明**团队定义可以被版本管理、被 CI 复现**。这补上 [t3code 深读](./t3code.md) 的缺口——**控制面管「运行时」，文件管「编排」**。内部平台若要同时支持「聊天里指挥」和「CI 里跑团队」，**两个入口应共享同一份团队定义**。

**风险与局限**：**18,553 star 里 41.1% 是这一周来的**，处在**爆发早期**，还没经历外部检验。每天发版（最新 **0.1.150，2026-11-09**）节奏快但**版本语义不稳**；**841 open issue 配 18,553 star（4.5%）**，对桌面 + 服务端双端应用偏高。**对标闭源产品是全部卖点，也是全部风险**——它唯一的护城河是「本地优先 + 用你自己的订阅 + 开源」，**这三个都不是技术壁垒**。技术上它**强绑三个 CLI 的本地协议**（stream-JSON / JSON-RPC / ACP），**上游改协议就要跟着改**。功能上窟窿也明确：**Ubuntu Wayland 宿主机控制被禁用、托管连通性在建、webhook 靠本地接收器、Ubuntu 整体还是 beta**；**云端 Linux 桌面依赖第三方服务（boat.dev）**，即使数据本地，**「每 bot 一台电脑」的关键一环仍在别人手里**。

## 下一步

- 想看控制面那条线 → [t3code 深读](./t3code.md)
- 想看多 Agent 的协作规则怎么定 → [Claude Code Game Studios 深读](./game-studios.md)

## 如果你想

- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
- 想看团队落地的方法论 → [AI Native 方法论](../../../ai-harness/index.md)
- 想看工具链横评 → [AI 工具全景](../../../ai-coding/tools/overview.md)
