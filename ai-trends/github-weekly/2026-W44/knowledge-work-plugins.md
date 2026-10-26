---
title: 'anthropics/knowledge-work-plugins：按岗位而不是按工具打包 Agent 能力'
description: Anthropic knowledge-work-plugins 深度解读——11 个岗位角色插件如何把 skills、connectors、slash commands 与 sub-agents 打包成可分发单元，以及这套「角色插件」模型对内部平台的借鉴价值
audience: beginner
difficulty: 🟢
status: published
lastUpdated: 2026-10-26
---

# anthropics/knowledge-work-plugins：按岗位而不是按工具打包 Agent 能力

> **TL;DR**：Anthropic 开源了 **11 个插件**，每个对应一个岗位角色——产品、销售、客服、产品管理、市场、法务、财务、数据、企业搜索等。一个插件打包 **skills + connectors + slash commands + sub-agents** 四件套，为 [Claude Cowork](https://claude.com/product/cowork) 构建，同时兼容 Claude Code。本周涨星 +2,790，涨星占存量 8%。

📅 数据窗口：2026-10-20 ~ 2026-10-26 ｜ 🏷️ 插件生态 ｜ 本周涨星 +2,790 ｜ 总 star 33,029

## 是什么

[anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)（Apache-2.0，Python）是一套**面向知识工作者的 Claude 插件**。README 的定位是：*Plugins that turn Claude into a specialist for your role, team, and company*。

它区分了两层：Cowork 让你设定目标、Claude 交付成品；**插件再进一步——告诉 Claude 你喜欢怎么工作、要拉哪些工具和数据、关键流程怎么处理、要暴露哪些斜杠命令**。四件套分工是：**skills 给方法、connectors 给数据源、slash commands 给显式入口、sub-agents 给隔离执行**。

开源了 11 个插件，README 列出的几个及其 connectors 范围：

| 插件 | 作用 | Connectors |
| --- | --- | --- |
| productivity | 任务、日程、日常流程、个人上下文 | Slack、Notion、Asana、Linear、Jira、Microsoft 365 |
| sales | 调研潜客、会前准备、复盘管道、外联草稿 | Slack、HubSpot、Close、Notion、Jira、Fireflies |
| customer-support | 工单分诊、回复草稿、升级打包、转成知识库文章 | Slack、Intercom、HubSpot、Guru、Jira |
| product-management | 写规格、规划路线图、综合用户研究、同步干系人 | Slack、Linear、Asana、Figma、Amplitude、Pendo |
| finance | 凭证准备、对账、生成报表、差异分析、支持审计 | Snowflake、Databricks、BigQuery |
| data | 写 SQL、统计分析、搭看板、分享前先自检 | Snowflake、Databricks、BigQuery、Hex |

README 说明这些插件是为 Anthropic 自己团队的工作方式**构建或受其启发**的，并鼓励按自己公司的工具与流程定制。

## 技术亮点

**第一，它按「岗位」而不是按「工具」组织分发单元，这是最本质的变化。** 以往的插件市场按工具分——Notion 插件、Jira 插件、Figma 插件；这里是销售插件、产品管理插件、财务插件。**岗位是组织里天然存在的预算单位与责任单位**，比按工具分更贴近企业真实的采购与治理结构——财务负责人能对一个财务插件做决定，却没法对「Jira 插件」做决定。

**第二，四件套的组合方式比单点能力强得多。** 单拎出任何一个都是别人的功能：skills 是提示词与流程，connectors 是 API 授权，slash commands 是触发入口，sub-agents 是隔离上下文。**四个绑在一起才是「能真正干活的工作单元」**——有方法、有数据、有入口、有隔离。这个组合模型比「发布一个 skill」高出一档抽象。

**第三，connectors 列表本身就是一份企业 SaaS 采购清单。** Slack、Notion、Asana、Linear、Jira、Microsoft 365、HubSpot、Intercom、Figma、Amplitude、Snowflake、Databricks、BigQuery、Box。**这份清单等于「一家中型 SaaS 公司默认在用哪些系统」的事实快照**，对内部平台做接入排期、对齐数据源清单，是现成的参照系。

**第四，双宿主兼容说明插件包正在脱离单一产品。** 同一套插件为 Cowork 构建、同时兼容 Claude Code，意味着插件格式的抽象层次在**产品之上**，这是生态资产可迁移的前提。这与上期 `wshobson/agents` 的「一份源 + 各家适配器」同向——**分发层正在先于 A2A 协议成型**。

**第五，定制被明确鼓励，且定制点被限定在正确的地方。** 真正的价值来自**按自己公司的工具、术语、流程做定制**。官方提供**结构与默认值**，企业填**自己的系统与规矩**——这正是企业内部推广 Agent 时该坚持的分层：**平台给结构，业务方填内容。**

## 后续发展建议

**它最值得内部平台参考的是映射结构，不是插件内容。**

- **「角色 → 插件包 → connectors 清单」这套映射，值得作为内部 Agent 平台的配置模型模板。** 对应到内部场景就是：**哪个角色（研发 / 测试 / 运维 / 数据）、挂哪些技能、接哪些系统、留哪些审计**。**建议把「角色」作为 Agent 能力包的一级概念**——内部团队也是按角色切分的（前端、后端、QA、SRE），角色包天然对应现有组织结构与责任划分。
- **「平台给结构、业务方填内容」这条分工要落成机制。** Anthropic 这套的关键是默认值开箱可用、定制点明确。**内部平台建议照此设计**：给出一套通用角色包 + 明确的扩展点（哪些 connectors、哪些 skills 可替换），而不是要求各团队从零搭 Agent。**门槛差一档，采用率就差一个量级。**
- **connectors 清单可以直接当作内部接入排期的输入。** 内部平台的系统接入顺序，不该凭感觉定，**应该对着「这套插件选择了哪些系统」反推优先级**——被主流角色插件选中的系统（Slack、Jira、Figma、Snowflake 这类），几乎一定是内部同样高频的系统。
- **但要注意护城河很浅。** 插件内容的本质是指令加连接器配置，结构可被竞品照抄。真正难复制的是**连接器的授权稳定性**和**宿主产品的分发控制力**。**内部平台要把资产留在自己这一侧**（核心技能与流程定义在平台内，而不是某个第三方插件包里），否则跨生态复用率会明显下降。

**风险与局限**：这是 Claude 生态内的插件形态，迁到其他 harness 需要适配，README 只承诺 Cowork 与 Claude Code 两个宿主；11 个插件覆盖「知识工作者」，**不含工程研发角色**——对内部研发场景参考价值有限，需要自己补齐；项目自 2026-01-23 创建至今**没有 release**，接口稳定性未知；141 个 open issue 对 33,029 star 属健康区间。

## 下一步

- 看 skill 生态的另一个样本（平台厂商如何选品）→ [android-skills 深读](./android-skills.md)
- 看官方插件目录长什么样 → [claude-plugins-official 深读](../2026-W43/claude-plugins-official.md)
- 想理解跨 harness 的资产分发层 → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)

## 如果你想

- 想知道这些 Agent Skill 该怎么组织 → [AI Native 方法论](../../../ai-harness/index.md)
- 想比较各家 Agent 工具形态 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想看生态里有哪些可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)
