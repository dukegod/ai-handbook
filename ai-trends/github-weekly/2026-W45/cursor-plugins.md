---
title: 'cursor/plugins：130+ 个插件里绝大多数是连接器，不是技能包'
description: Cursor 官方插件仓库深度解读——.cursor-plugin/plugin.json 清单规范、130+ 第三方 SaaS 连接器的结构，以及「插件」概念正在分裂成接口层与知识层两种语义
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-02
---

# cursor/plugins：130+ 个插件里绝大多数是连接器，不是技能包

> **TL;DR**：15,039 star（月 +5,809，涨星/存量 **38.6%**），617 个 open issue。Cursor 的插件仓库分两层：`plugins/` 是 Cursor 自家的 16 个插件（`thermos` 代码审查、`orchestrate` 编排、`cursor-sdk`、`create-plugin` 脚手架等），`plugins/third_party/` 则是 **100 多个第三方 SaaS 连接器**——Salesforce、S&P Global Capital IQ、Playwright、Tailscale、QuickBooks、Snowflake 式的「让 Agent 接上系统」。**本周最值得注意的信号是：同一个「插件」这个词，正在分裂成接口层和知识层两种互不兼容的语义。**

📅 数据窗口：2026-10-26 ~ 2026-11-02 ｜ 🏷️ 插件生态 ｜ 本周涨星 未进周榜 ｜ 总 star 15,039

## 是什么

[cursor/plugins](https://github.com/cursor/plugins) 的定位是「**Cursor 插件规范 + 官方插件**」。结构上是一个多插件市场仓库：根目录的 `.cursor-plugin/marketplace.json` 列出全部插件，每个插件自己带一个 `.cursor-plugin/plugin.json` 清单。

清单里的 `name` / `author` / `category` / `description` 是最小元信息。README 里有个细节值得注意：**author 字段的值必须和该插件 `plugin.json` 里的 `author.name` 一致**（市场列表里统一显示 `plugins@cursor.com`）——**这是清单一致性校验，不是装饰**。

## 技术亮点

**第一，插件生态的绝大部分是「连接器」而不是「技能包」。** 粗略统计 `plugins/third_party/` 下的条目，绝大多数是单一 SaaS 的接入：Gmail、Google Drive、Calendar、Docs、Sheets、Slides、Salesforce、HubSpot、Intercom、Zoom、Gong、Asana 系的 Todoist、Calendly、Workday、ServiceNow、NetSuite 系的 QuickBooks、Tailscale、GitHub、Playwright、Snowflake 类的 Databricks Genie、Capital IQ、PitchBook、Meltwater、Excalidraw、BigQuery、Statsig……

**这个结构意味着 Cursor 的插件生态重心是「让 Agent 接得上企业系统」，而不是「教 Agent 怎么做事」。**

**第二，自家插件里有三个方向值得注意。**

- `orchestrate`：**把大任务扇出给并行的云端 Agent**，有 planner、worker、verifier 和结构化交接——**Cursor 自己做多 Agent 编排了**。
- `thermos`：「热核级」分支审查——深度安全 / 正确性审计、严苛代码质量 rubric、并行 subagent，可选直接产出可合并的 PR 流程。
- `agent-compatibility`：**用 CLI 扫仓库兼容性**，并让 Agent 对照现状审计启动流程、校验和文档——**它审计的是「文档说的」和「实际做的」是否一致**。

**第三，第三方作者也在建自己的方法论层。** `pstack`（"想快就先扎深"）、`dyl-stack`（根因优先、The Algorithm before design、Figma-to-UI 带视觉评审）、`advisor`（**重大决策前、卡住时、宣布完成前先去咨询一个更强的模型**）、`continual-learning`（用 transcript 增量更新 `AGENTS.md`）。**Cursor 自己的插件商店里已经出现了「skill 套 skill」的生态。**

**第四，规范走的是自有清单格式。** `.cursor-plugin/plugin.json` 是 Cursor 自己的 schema，**和 Anthropic 的 `SKILL.md` 不通用**。

## 后续发展建议

**「插件」这个词现在指向两件不同的事，而内部平台必须在建之前先选定自己要做哪一件。** 四个判断：

- **先分清接口层和知识层，两者的组织方式完全不同。** Cursor 的插件仓库里，第三方部分几乎全是**接口层**——把一个 SaaS 的能力包成 Agent 可调用的工具，核心是鉴权、OAuth、权限范围、错误处理。Anthropic 的 `knowledge-work-plugins` 是**知识层**——把「市场分析师」这个角色的方法、模板、协作流程打包，核心是提示词与产出物。**内部平台如果两类都想要，必须分开建包、分开授权、分开度量**——接口层看调用成功率与鉴权失败率，知识层看产出采纳率，混在一起就两头都测不准。
- **接口层最大的成本从来不是代码，是鉴权和信任边界。** 看这份清单就知道：每个 SaaS 都有自己的 OAuth 流程、权限范围、webhook 语义、错误模型。**建议内部平台把「连接器」抽象成统一的凭据托管 + 权限范围 + 审计三件套**，而不是让每个连接器各写一套——Cursor 这份清单里有一半插件是同一个作者的（Eric Zakariasson），**说明单个开发者靠人工维护是撑不住这个量级的**。
- **`agent-compatibility` 那个插件值得单独抄。** 「**对照现实审计文档和启动流程**」这件事，正好是内部平台最容易出事的地方：Agent 按文档做事，文档与实现不符时，错误会被系统性地放大。**建议内部平台的 skill / 文档体系里加一条自动化校验：文档里写的命令、参数、路径必须真实可执行。**
- **`advisor` 插件体现了对「完成信号」的怀疑。** 「重大决策前、卡住时、宣布完成前先去咨询一个更强的模型」——**这条规则对内部平台同样成立**：Agent 说「做完了」是最不可靠的信号。内部平台应该把「声明完成」和「验证通过」做成两个不同的状态，而不是同一个。

**风险与局限**：**仓库没有 license**（GitHub API 返回空）。617 个 open issue 相对 15,039 star 比例极高（**4.1%**），反映生态扩张速度远超维护能力。**没有 release**，版本靠 git 跟踪。**Cursor 的 `.cursor-plugin/plugin.json` 是自有格式，不能直接被 Claude Code、Codex、OpenCode 消费**——**如果内部平台想「一个插件多处用」，现在只能选 agentskills.io 这条路（见 [vercel-labs/skills 深读](./vercel-skills.md)），选 Cursor 这条路就只能吃 Cursor 生态。**

## 下一步

- 想看跨 harness 通用的分发方案 → [vercel-labs/skills 深读](./vercel-skills.md)
- 想看另一个方向的插件（岗位角色包） → [2026-W44 knowledge-work-plugins 深读](../2026-W44/knowledge-work-plugins.md)

## 如果你想

- 想看生态里有哪些可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)
- 想理解跨系统集成时的信任边界划分 → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)
- 想比较各家 Agent 工具形态 → [AI 工具全景](../../../ai-coding/tools/overview.md)
