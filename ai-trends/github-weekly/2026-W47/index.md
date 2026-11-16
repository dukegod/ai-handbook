---
title: '2026-W47 GitHub 周报：Meta 开源 Agent 设计系统，Google 补上无前情评审层，跨行业权威开始用 Skill 承载方法论'
description: '2026-11-10 ~ 2026-11-16 的 GitHub 热榜与涨星盘点——11 个周榜条目里 9 个面向 Agent 工具链，合计吸走 46,396 star，占周榜总涨星 61,364 的 75.6%；Meta 开源 agent-ready 设计系统 Astryx 单周 +13,501 夺冠，Google 发布用无前情 subagent 做独立评审的 EGM 插件，Cloudflare 安全审计 skill 拿下月榜第一却已 63 天没有提交'
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-16
---

# 2026-W47 GitHub 周报

📅 数据窗口：2026-11-10 ~ 2026-11-16 ｜ 来源：GitHub Trending 官方口径

> **TL;DR**：本周周榜抓到 **11 条**，其中 **9 条面向 Agent 工具链**，合计吸走 **46,396 star，占周榜总涨星 61,364 的 75.6%**。四条值得记：**Meta 亲自开源 `Astryx`（单周 +13,501，涨星占存量 46.5%），把设计系统做成 Agent 的第一层约束**；**Google 发布 `elephant-goldfish-model`（单周 +5,060），用「没有前情的新 subagent」做独立评审**；**本周最刺眼的反例是 `cloudflare/security-audit-skill`——月榜第一 +43,540，但最后一次提交停在 2026-09-14，距今 63 天且没有任何 release**；**新锐榜里出现两个非 AI 行业权威——Jane Street 和 Uncle Bob 都在用 skill 承载自己的方法论**。

## 一、本周热榜全表（11 个）

> 榜位按 **Trending 页面顺序**（趋势分排名）列出，**与涨星排序不一致**——涨星排序见第三节。

| 榜位 | 仓库 | 本周涨星 | 总 star | 语言 | 一句话 |
| --- | --- | ---: | ---: | --- | --- |
| 1 | [meta/astryx](https://github.com/meta/astryx) | **+13,501** | 29,020 | TypeScript | Meta 开源的 agent-ready 设计系统 |
| 2 | [anthropics/skills](https://github.com/anthropics/skills) | +6,077 | 195,456 | Python | 官方 Agent Skills 规范源 |
| 3 | [sherlock-project/sherlock](https://github.com/sherlock-project/sherlock) | +10,412 | 112,607 | Python | 跨社交平台查用户名（非 AI） |
| 4 | [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | +1,719 | 11,973 | TypeScript | 本地 Agent 评审 / 标注回路 |
| 5 | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | +4,217 | 51,702 | Rust | Agent 浏览器自动化 CLI |
| 6 | [ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) | +4,548 | 72,573 | Python | LLM 驱动的多市场股票分析 |
| 7 | [we-promise/sure](https://github.com/we-promise/sure) | +4,556 | 15,755 | Ruby | 个人财务应用（非 AI） |
| 8 | [milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot) | +5,463 | 23,544 | TypeScript | 聊天式多 Agent 团队 |
| 9 | [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model) | +5,060 | 19,875 | Python | Google 的无前情评审插件 |
| 10 | [google-deepmind/mujoco](https://github.com/google-deepmind/mujoco) | +1,922 | 18,095 | C++ | DeepMind 通用物理引擎 |
| 11 | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | +3,889 | 118,003 | JavaScript | 生产级工程 skill 合集 |

> 本周周榜条目数从上周的 17 条降到 **11 条**，是 Trending 页面自身给出的条目数波动，**不等于生态降温**；抓取脚本与上周用同一套解析逻辑，已逐条复核原始 HTML。

## 二、本月热榜 TOP（GitHub Trending `since=monthly`，按本月涨星降序）

| # | 仓库 | 本月涨星 | 总 star | 涨星/存量比 | 方向 |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | **+43,540** | 73,319 | **59.4%** | **Agent 安全审计 Skill（已 63 天未提交）** |
| 2 | [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | +33,583 | 61,725 | 54.4% | Harness 控制面 |
| 3 | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | +29,631 | 110,841 | 26.7% | **编码 Agent 的设计词汇表** |
| 4 | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | +25,448 | 55,581 | 45.8% | 反 AI 味设计 |
| 5 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | +20,878 | 84,812 | 24.6% | **写 HTML 渲染视频** |
| 6 | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | +19,546 | 116,318 | 16.8% | 给编码 Agent 装品味 |
| 7 | [sherlock-project/sherlock](https://github.com/sherlock-project/sherlock) | +18,371 | 112,607 | 16.3% | 跨社交平台查用户名（非 AI） |
| 8 | [HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor) | +18,278 | 59,530 | 30.7% | 终身个性化辅导 |
| 9 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | +17,038 | 117,419 | 14.5% | 跨会话记忆 |
| 10 | [anthropics/skills](https://github.com/anthropics/skills) | +14,332 | 195,456 | 7.3% | 官方 Skills 规范源 |
| 11 | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | +10,672 | 29,765 | 35.9% | SEO skill |
| 12 | [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | +7,937 | 20,160 | 39.4% | **AI 产品短片 skill** |
| 13 | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | +7,545 | 51,702 | 14.6% | Agent 浏览器自动化 CLI |
| 14 | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | +6,417 | 36,208 | 17.7% | 知识工作者插件包 |

> 本月榜抓到 14 条，其中 13 条与 Agent / 大模型相关，合计吸走 **254,845 star，占月榜总涨星 273,216 的 93.3%**。

## 三、本周涨星 TOP 10

| 排名 | 仓库 | 本周涨星 | 涨星/存量比 | 判读 |
| ---: | --- | ---: | ---: | --- |
| 1 | [meta/astryx](https://github.com/meta/astryx) | **+13,501** | **46.5%** | 大厂开源爆发，单周吃掉周榜 22.0% 的涨星 |
| 2 | [sherlock-project/sherlock](https://github.com/sherlock-project/sherlock) | +10,412 | 9.2% | 非 AI 老项目持续吸量 |
| 3 | [anthropics/skills](https://github.com/anthropics/skills) | +6,077 | 3.1% | 巨量存量持续吸量 |
| 4 | [milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot) | +5,463 | 23.2% | 持续爆发 |
| 5 | [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model) | +5,060 | 25.5% | 大厂官方插件，新项目爆发 |
| 6 | [we-promise/sure](https://github.com/we-promise/sure) | +4,556 | 28.9% | 非 AI 新项目爆发 |
| 7 | [ZhuLinsen/daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) | +4,548 | 6.3% | 存量走量 |
| 8 | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | +4,217 | 8.2% | 存量走量 |
| 9 | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | +3,889 | 3.3% | 巨量存量持续吸量 |
| 10 | [google-deepmind/mujoco](https://github.com/google-deepmind/mujoco) | +1,922 | 10.6% | 经典项目回榜 |

## 四、新锐仓库（近 30 天新建）

> 数据源：GitHub Search API 按 `created:>2026-10-17 stars:>300` 过滤，命中 **846** 个仓库，取前 10。

| 仓库 | star | 建仓日期 | 方向 |
| --- | ---: | --- | --- |
| [storytold/craft-anything](https://github.com/storytold/craft-anything) | 33,975 | 2026-10-31 | 「理解任何软件」工具（上期已出现） |
| [ccch1mneyyy/dsh-Go](https://github.com/ccch1mneyyy/dsh-Go) | 23,943 | 2026-10-25 | DeepSeek Harness 进手机（上期已出现） |
| [deepseek-ai/dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype) | 23,338 | 2026-10-31 | DeepSeek Agent 原型（上期已出现） |
| [Zagitta/gpu-unlock](https://github.com/Zagitta/gpu-unlock) | 19,740 | 2026-10-18 | GeForce 驱动解锁 |
| [heydamir/unslop](https://github.com/heydamir/unslop) | 16,831 | 2026-10-29 | 反 AI 味 UI |
| [pengchujin/aerial-tv](https://github.com/pengchujin/aerial-tv) | 12,072 | 2026-10-20 | 国产电视干净桌面 |
| [anefzaoui/misterdownloadmanager](https://github.com/anefzaoui/misterdownloadmanager) | 10,566 | 2026-10-29 | 下载管理器 |
| [zortos293/Lichii](https://github.com/zortos293/Lichii) | 9,400 | 2026-10-31 | 自托管应用 |
| [JuneYaooo/rea-video](https://github.com/JuneYaooo/rea-video) | 9,282 | 2026-10-29 | 视频逆向 |
| [janestreet/agent_skills](https://github.com/janestreet/agent_skills) | 9,095 | 2026-11-03 | **Jane Street 官方 skill** |

**新信号：非 AI 行业权威开始用 skill 交付方法论。** 新锐榜里有两个重量级名字——**Jane Street**（量化交易巨头，11 天内建仓 9,095 star）只发了**一个** skill：`socratic-tutor`，把苏格拉底式教学拆成「诊断 → 0-5 级技能图 → 一次一问 → 间隔复习 → 最终测评」；**Uncle Bob**（Robert C. Martin，22 天建仓 8,009 star）的 `ub-mode` 把「先让它工作，再让它正确」的工程纪律配成三个**确定性质量门工具**——`crapper` 算 CRAP（复杂度 × 覆盖率，要求每个函数 < 10）、`dryer` 抓 ≥ 0.8 相似度的结构重复、`mutator` 跑变异测试找出测试杀不死的 mutant。**一个做教学法，一个做质量门，都不是模型厂商**——skill 正在变成行业方法论的通用载体。

## 五、本周判断

1. **Meta 亲自下场，把「设计系统」做成了 Agent 的第一层约束。** `astryx` 单周 **+13,501**、涨星占存量 **46.5%**，拿下周榜涨星冠军，也是本周唯一一家一周吃掉周榜 **22.0%** 涨星的仓库。README 的定位句是「**built for how we build now: by people and the agents working alongside them**」，四条原则里有一条直接叫 **One system for humans and AI**。三个设计值得直接抄：**CLI 支持全局安装**，装完 `astryx` 命令在每个目录都能用，README 明说这是为了「让每个 coding agent 都认识 Astryx」；**`swizzle` 能把组件完整源码 eject 到你的项目里自己拥有**，而不是只能包一层；**theme 只是 CSS 自定义属性覆盖**，改品牌不用 fork 也不用包组件。**判断：Agent 时代的设计约束不可能靠「规范文档」落地，只能靠「Agent 能直接调用的原语 + 可 eject 的源码」落地。** 内部平台如果要给 Agent 提供组件库，**建议从第一天就把「可 eject」和「CLI 可查」当硬要求**，否则 Agent 只会绕过你的组件库。

2. **Google 补的是「评审层」，而且评审的定义是「没有前情的新上下文」。** `elephant-goldfish-model` 单周 +5,060、涨星占存量 25.5%。它把角色切成三个：**Elephant** 持有项目上下文、起草规格；**Goldfish** 只拿到「文档 + 被引用的源码，**但没有之前的对话**」，专门找未言明的假设和盲点；**You** 做权衡和批准。README 里那句是关键——**Goldfish 评审必须能创建全新的 subagent 上下文，如果 harness 不支持，EGM 直接停止评审**。**判断：当前 Agent 的「自我评审」几乎无效，因为评审者继承了作者的推理路径，也就继承了作者的盲点。** 「换一个无前情的 subagent 当评审者」是本周最值得落地的机制，成本只是一条 subagent 规则。W46 讲的「Agent 协作要靠架构规则」在这里有了具体落点：**隔离上下文比约束措辞有效**。

3. **「设计味」这条赛道正式分裂成四层，而且已经从形容词变成可执行门禁。** 本周同框的四个项目各占一层：`astryx`（组件级设计系统）、[impeccable](https://github.com/pbakaus/impeccable)（编码 Agent 的设计词汇表，月榜 +29,631）、[hallmark](https://github.com/Nutlope/hallmark)（反 AI 味设计，月榜 +25,448）、`taste-skill`（成品站点审美，月榜 +19,546）。关键变化在 `taste-skill` 的实现方式：**它的 checker 在真实浏览器里按 1440 / 1024 / 820 / 768 / 390 五个视口渲染，逐条输出 PASS / WARN / FAIL**，抓空画面、坏掉的 shader、对比度下降、列错位、占位文案、编造的街道门牌号；`gate.mjs` **最多修三轮**才放行交付。这和 `addyosmani/agent-skills` 的 `constraint-driven-development` 是同一个模式——**把「品味」和「质量」写成会被执行的检查项，而不是写成形容词**。**判断：任何「反 AI 味」「设计规范」类项目，值不值得用的唯一判据是它有没有可执行的 checker；没有 checker 的，只是又一套 prompt。**

4. **本周最值得写进选型清单的反例：`cloudflare/security-audit-skill` 拿下月榜第一，但代码已经 63 天没动。** 月榜 **+43,540**、涨星占存量 **59.4%**，排第一；但最近一次提交是 **2026-09-14**，**至今没有任何 release**（releases feed 为空）。W46 已经标注过这个异常，本周数据把它坐实了。**讽刺的是它自述的价值正是「多阶段安全审计 + 每条发现由机器独立验证」——一个卖可信度的 skill，自己已经三个月没被维护。** **判断：Agent 安全这个方向上，「流量先于工程」已经是常态。** 选型时必须把两件事分开评估：**skill 内容是否可信**（读 README 和规则文本就能判断）与 **skill 是否会被持续维护**（只能看提交和 release 记录）。前者可以静态审查，后者只能动态观察——**后者没有替代信号**。

5. **「人在环路」正在从提示词里的一句话，独立成一类基础设施。** `plannotator`（11,973 star，单周 +1,719，涨星占存量 14.4%）把这件事做成了产品：**Agent 一产出计划就自动在浏览器里打开评审面**，你逐条标注、评论，反馈直接回到 Agent 的下一轮；它同时列出 **11 个 harness 的接入方式**（Claude Code、Codex、Copilot CLI、Gemini CLI、OpenCode、Kiro、Droid、Amp、DeepSeek Harness、Pi、T3 Code），并用 MCP 作为通用兜底入口。新锐榜里的 `unclebob/ub-mode` 则从另一头补同一件事——**用确定性工具而不是提示词来卡质量门**。**判断：多 Agent 平台的下一层竞争，不是「Agent 怎么协作」，而是「人怎么在最短路径上把判断塞回 Agent 的上下文」。** 这件事的关键指标不是自动化率，而是**从「Agent 提出」到「人的判断被 Agent 收到」这一段的延迟**。

## 六、数据口径与局限

- 涨星数一律采用 GitHub Trending 页面自带的官方口径（`stars this week` / `this month`），不做二次推算；已用独立解析复核 Trending 原始 HTML，**周榜 11 条、月榜 14 条逐条一致**。
- GitHub REST `/stargazers` 接口已全量下线，无法自算任意窗口的精确涨星；本期未采用 OSS Insight（自 2026-05 起官方标注严重降级，仅能作趋势下界）。
- Trending 每页仅 15 个条目（GitHub 已从 25 下调），本周抓到 **11 条**——**不等于「Top 15 之外没有更多」**，也不代表生态降温（上周同源抓到 17 条）。
- 「涨星/存量比」= 涨星 ÷ 总 star，区分「新项目爆发」与「大项目持续吸量」，对新项目天然偏高。第一节「榜位」是 **Trending 页面顺序**，**不是涨星排名**。
- **采集工具链的一处降级（本期已知局限）**：本机没有 `gh` CLI，GitHub 匿名 API 配额在采集时段已耗尽，因此 `metadata`（topics / license / open issues / pushed_at）与 `rising_new_repos` 由采集脚本产出失败。补救路径是**改走免鉴权通道**：`raw.githubusercontent.com` 取 README 原文、`commits.atom` / `releases.atom` 取最近提交与最新 release、仓库页 HTML 取 topics 与 issue / PR 计数、Search API 取新锐榜（该接口配额独立）。**因此本期的 release 日期取自 Atom feed 的 `<updated>` 字段而非 API 的 `published_at`，两者对草稿 / 预发布可能有偏差，已在表中以 release 标题与日期并列呈现。**
- **需标注的异常**：`cloudflare/security-audit-skill` 月涨 +43,540 但 63 天未提交、无 release（见判断 4）；`meta/astryx` 建仓于 2026-01-09，本周涨星占存量 46.5%，属于**「开源发布」而非「新建仓」的爆发**，README 自述在 Meta 内部已 grown for eight years。

## 下一步

- 按下面的深读逐个展开，或挑感兴趣的仓库看
- 想看这轮升温背后的协议动向 → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)

## 如果你想

- 想知道这些 Agent Skill 该怎么组织 → [AI Native 方法论](../../../ai-harness/index.md)
- 想比较各家 Agent 工具形态 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想看可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)

## 本期深读

| 仓库 | 一句话 · 方向 |
| --- | --- |
| [meta/astryx](./astryx.md) | Meta 的 agent-ready 设计系统 |
| [google/elephant-goldfish-model](./elephant-goldfish-model.md) | 无前情 subagent 评审 |
| [backnotprop/plannotator](./plannotator.md) | 人在环路独立成层 |
| [Leonxlnx/taste-skill](./taste-skill.md) | 品味写成可执行 checker |
| [addyosmani/agent-skills](./agent-skills.md) | 约束驱动开发 |
| [heygen-com/hyperframes](./hyperframes.md) | 写 HTML 渲染视频 |
| [Vincentwei1021/video-shotcraft](./video-shotcraft.md) | 产品短片 shot 库 |
| [HKUDS/DeepTutor](./deeptutor.md) | 终身个性化辅导 |
| [ZhuLinsen/daily_stock_analysis](./daily-stock-analysis.md) | LLM 决策仪表盘 |
| [google-deepmind/mujoco](./mujoco.md) | 仿真底座与可微物理 |
