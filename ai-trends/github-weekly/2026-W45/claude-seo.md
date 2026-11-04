---
title: 'AgriciDaniel/claude-seo：agent readiness——让站点对 Agent 可读、可调用'
description: claude-seo 深度解读——26 个子 skill 与 19 个子 agent 的组织方式，以及 agent readiness 这条新战线：Lighthouse Agentic Browsing、llms.txt、WebMCP 与 AI 搜索可发现性
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-02
---

# AgriciDaniel/claude-seo：agent readiness——让站点对 Agent 可读、可调用

> **TL;DR**：25,622 star、**周涨星 +5,034（19.6%）**，MIT，最新 release **v2.5.0（2026-10-22）**。它表面是 SEO 工具，**真正的看点是它把「站点对 Agent 的可读性」单独立成了一条战线**：一条 `/seo agentic` 命令同时检查 **Lighthouse Agentic Browsing 得分、AI agent 访问权限、`llms.txt`、Markdown 可读性、WebMCP**——**这是 A2A 协议在 Web 侧的镜像问题：不是 Agent 之间怎么说话，而是站点怎么让 Agent 读得懂、调用得动。**

📅 数据窗口：2026-10-26 ~ 2026-11-02 ｜ 🏷️ Agent 可发现性 ｜ 本周涨星 +5,034 ｜ 总 star 25,622

## 是什么

[AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) 是「**Claude Code 的通用 SEO skill**」：**26 个子 skill + 19 个子 agent**，覆盖技术 SEO、E-E-A-T、schema、GEO/AEO、**agent readiness**、外链、本地 SEO、电商、国际化、Google API、PDF / Excel 报告，另有 9 个可选扩展接实时数据。

命令组织成六组共 30 条：

- **审计与规划**（5 条）：`/seo setup`、`/seo doctor`、`/seo audit <url>`（**并行 agent 做全站审计**）、`/seo page <url>`、`/seo plan <type>`
- **技术 SEO、内容、schema 与 AI 搜索**（含 `/seo geo`、`/seo agentic`）
- **本地、外链、电商**（4 条）
- **扩展**（5 条）：`/seo image-gen`、`/seo seranking`（ChatGPT / Gemini / Perplexity / AI Overviews / AI Mode 的 AI 份额声量）、`/seo profound`（LLM 引用追踪）、`/seo bing`、`/seo unlighthouse`

## 技术亮点

**第一，`/seo agentic` 这条命令定义了「agent readiness」这个指标。** 它的检查项是：**Lighthouse Agentic Browsing 得分（X/N）、AI agent 的访问权限、`llms.txt`、Markdown 可读性、WebMCP**。

这五项各自对应一个具体的接入问题：

- **AI agent 访问权限**——很多站点在 `robots.txt` 里屏蔽 AI 爬虫，等于把自己排除在 Agent 的知识来源之外。
- **`llms.txt`**——给 LLM 读的站点说明书，是给大模型时代的 `robots.txt`。
- **WebMCP**——**站点直接暴露可被 Agent 调用的工具**，这是从「被爬取」到「被调用」的跃迁。
- **Markdown 可读性**——同一个页面，给人和给模型看的版本往往不同。

**第二，它把 GEO / AEO（生成式引擎优化）和传统 SEO 并列，而且做得比传统 SEO 更细。** `/seo geo` 专门做 AI Overviews 和生成式引擎优化；`/seo seranking` 追踪的是 **ChatGPT、Gemini、Perplexity、AI Overviews、AI Mode** 五个引擎里的 AI 份额声量；`/seo profound` 做 LLM 引用追踪与时间序列。**换句话说，它已经在做「在被模型回答里被引用」这套指标了**，而不是等传统排名自然迁移过去。

**第三，skill 与 sub-agent 的分工很清楚。** 19 个 sub-agent 大多绑定特定模型：`/seo agentic`、`/seo local`、`/seo maps`、`/seo google`、`/seo backlinks` 用 Sonnet；`/seo cluster`（主题策略）、`/seo sxo`（搜索体验设计）、`/seo drift`（变更监控）、`/seo ecommerce`、`/seo flow` 用 Opus。**把「需要强推理的策略类任务」和「需要大量抓取的执行类任务」分给不同模型**——这是多模型 Agent 编排的一个具体范式。

**第四，审计是真并行 Agent，不是单线程跑脚本。** `/seo audit <url>` 标注为「parallel agents」，`/seo page <url>` 是单页深度分析。**这是「一个 skill 下挂多个专门 agent」的完整样板**，比单 Agent 跑到底要稳得多。

**第五，运行在自己机器上。** README 的对比表把「你的数据是否留在本地」列成一列并标为 Yes——`/seo setup` 创建**隔离的 Python 运行时和 Chromium**，`/seo doctor` 只检查环境不改系统，报告产出为 Markdown / PDF / JSON 文件。**「本地优先 + 产物是文件而不是界面」**是这类工具的典型形态。

## 后续发展建议

**agent readiness 这条线，比这份 SEO skill 本身更值得内部平台关注——它和 A2A 协议是同一个问题的两面。** 四个判断：

- **A2A 关心的是 Agent 之间怎么对话；agent readiness 关心的是系统怎么让 Agent 读得懂、调得动。** 这两件事在内部平台上会汇合：**内部系统的接口既要给 Agent 调，也要给 Agent 读**——前者是 MCP / A2A 的活，后者是文档结构、`llms.txt` 式说明、结构化输出的活。**建议内部平台在评估一个系统「能否被 Agent 集成」时，把这两条分开打分**：能不能调（接口完备性）、能不能读（上下文完备性）。
- **`llms.txt` 和 WebMCP 值得在内部系统上试一遍。** 成本很低：**给每个内部系统加一个 `llms.txt` 风格的说明文件**（系统能做什么、参数、约束、典型场景），再加一个「本系统能被 Agent 调用什么」的工具声明。**这两件事能直接降低 Agent 的探索成本**，比写更多文档的收益高得多。
- **skill 与 sub-agent 分层 + 按模型分工，是可以直接搬的内部模式。** 内部平台的 skill 体系如果只有单层，执行类和策略类任务会互相拖累。**建议至少分两层：skill 负责「做什么、怎么算完成」，sub-agent 负责「强推理的判断」**，并允许按任务类型路由不同模型。
- **别把它当成 SEO 工具用。** 它的实际形态是「**一个垂类领域的完整 Agent 工作流范例**」——26 个子 skill、19 个子 agent、30 条命令、六组划分、并行审计、本地隔离运行时、文件化产物。**对内部平台来说，这份 README 的组织方式本身就是模板**，比它的 SEO 能力更有参考价值。

**风险与局限**：**25,622 star 对应 78 个 open issue（0.3%）**，最新 release v2.5.0 在 11 天前。**但它的复杂度明显偏高**：26 个子 skill + 19 个子 agent + 9 个扩展 + 独立 Python 运行时 + 自带 Chromium——**安装门槛比一般 skill 高不少**，README 里对浏览器类检查的依赖也意味着**环境不全时部分检查会降级**。**它没有任何官方背书**（个人仓库，非 Anthropic 官方），与 `anthropics/skills` 的关系是「遵循规范」而非「官方认证」。另外，**它把 SEO 公司的商业诉求（代理周报、竞品对比、AI 声量追踪）做进了产品**，内部引入时需要判断哪些子能力与我们的目标无关——**整套照搬会引入大量无用命令**。

## 下一步

- 想看 A2A 协议本身的调研结论 → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)
- 想看多 Agent 编排的另一个形态 → [dsh-superagent 深读](./dsh-superagent.md)

## 如果你想

- 想理解 Agent 与 Workflow 的分工 → [Agent 与 Workflow](../../../getting-started/agents-and-workflows.md)
- 想知道这些 Agent Skill 该怎么组织 → [AI Native 方法论](../../../ai-harness/index.md)
- 想看工具链横评 → [AI 工具全景](../../../ai-coding/tools/overview.md)
