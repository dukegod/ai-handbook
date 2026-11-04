---
title: '2026-W45 GitHub 周报：Skill 生态吞掉周榜，JetBrains 亲自下场做 harness'
description: 2026-10-26 ~ 2026-11-02 的 GitHub 热榜与涨星盘点——16 个周榜条目里 13 个是 skill / plugin / harness 类，JetBrains 官方 agentic IDE 入场，DeepSeek 开源主动型 Agent 系统原型
audience: intermediate
difficulty: 🟡
status: published
lastUpdated: 2026-11-02
---

# 2026-W45 GitHub 周报

> **TL;DR**：本周 16 个周榜条目里 **13 个是 skill / plugin / harness 类**，「反 AI 味设计」四件套单周吸走 **30,526 star，占周榜总涨星的 31.8%**。三条值得记：**JetBrains 官方下场做 agentic IDE**（`thinkrail` 涨星比 82.2%，全榜最高）；**DeepSeek 开源的不是模型，是一套 Agent 授权模型**；**Cursor 插件仓库 130+ 个插件绝大多数是 SaaS 连接器，不是技能包**。

📅 数据窗口：2026-10-26 ~ 2026-11-02 ｜ 来源：GitHub Trending 官方口径

⏱ 预计阅读时间：9 分钟

## 一、本周热榜全表（16 个）

> 榜位按 **Trending 页面顺序**（趋势分排名）列出，**与涨星排序不一致**——涨星排序见第三节。

| 榜位 | 仓库 | 本周涨星 | 总 star | 语言 | 一句话 |
| --- | --- | ---: | ---: | --- | --- |
| 1 | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | **+11,566** | 45,069 | CSS | 反 AI 味设计 skill |
| 2 | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | **+12,017** | 99,544 | Rust | 编码 Agent 的设计词汇表 |
| 3 | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | +5,034 | 25,622 | Python | SEO skill 套件 |
| 4 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | +5,852 | 109,575 | TypeScript | 跨会话持久记忆 |
| 5 | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | +10,069 | 56,522 | JavaScript | 多阶段安全审计 skill |
| 6 | [obra/superpowers](https://github.com/obra/superpowers) | +5,896 | 310,723 | Shell | 编码 Agent 方法论 |
| 7 | [JetBrains/thinkrail](https://github.com/JetBrains/thinkrail) | +5,760 | 7,010 | TypeScript | JetBrains 官方 agentic IDE |
| 8 | [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | +6,926 | 38,442 | TypeScript | 三端控制面 |
| 9 | [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | +4,459 | 228,087 | — | 单个 CLAUDE.md |
| 10 | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) | +1,607 | 10,137 | Markdown | 界面 skill 合集 |
| 11 | [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | +5,432 | 119,601 | Python | 多 Agent 金融交易框架 |
| 12 | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | +5,336 | 107,949 | JavaScript | 给编码 Agent 装审美 |
| 13 | [anthropics/skills](https://github.com/anthropics/skills) | +2,600 | 186,426 | Python | 官方 skills 仓库兼规范源 |
| 14 | [affaan-m/ECC](https://github.com/affaan-m/ECC) | +6,299 | 294,896 | JavaScript | harness 性能优化系统 |
| 15 | [YuJunZhiXue/dsh-purge](https://github.com/YuJunZhiXue/dsh-purge) | +6,644 | 15,521 | JavaScript | DSH 红队工具 |
| 16 | [ghostty-org/ghostty](https://github.com/ghostty-org/ghostty) | +589 | 63,208 | Zig | 终端模拟器（唯一非 AI） |

## 二、本月热榜 TOP（GitHub Trending `since=monthly`，按本月涨星降序）

| # | 仓库 | 本月涨星 | 总 star | 涨星/存量比 | 方向 |
| --- | --- | ---: | ---: | ---: | --- |
| 1 | [debpalash/VoiceStudio](https://github.com/debpalash/VoiceStudio) | +47,055 | 98,109 | 48.0% | 本地语音 |
| 2 | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | +32,599 | 56,522 | **57.7%** | **Agent 安全审计 Skill** |
| 3 | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | +26,119 | 99,544 | 26.2% | **Harness 设计语言** |
| 4 | [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | +22,225 | 77,198 | 28.8% | Agent 视频 |
| 5 | [NationalSecurityAgency/ghidra](https://github.com/NationalSecurityAgency/ghidra) | +16,858 | 96,844 | 17.4% | 逆向 |
| 6 | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | +16,333 | 107,949 | 15.1% | 审美 skill |
| 7 | [tashfeenahmed/freellmapi](https://github.com/tashfeenahmed/freellmapi) | +15,908 | 45,845 | 34.7% | 免费 LLM API |
| 8 | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | +15,201 | 45,070 | 33.7% | **反 AI 味设计** |
| 9 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | +14,011 | 109,575 | 12.8% | **跨会话记忆** |
| 10 | [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | +12,629 | 38,442 | 32.9% | 多端控制面 |
| 11 | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | +8,625 | 45,742 | 18.9% | 官方插件目录 |
| 12 | [mksglu/context-mode](https://github.com/mksglu/context-mode) | +8,666 | 33,180 | 26.1% | 上下文优化 |
| 13 | [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | +8,486 | 34,390 | 24.7% | **岗位角色包** |
| 14 | [earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad) | +8,238 | 24,804 | 33.2% | **AI 实体设计 + MCP** |
| 15 | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | +7,274 | 25,622 | 28.4% | **Agent readiness** |
| 16 | [cursor/plugins](https://github.com/cursor/plugins) | +5,809 | 15,039 | **38.6%** | **插件规范 + 连接器** |
| 17 | [vercel-labs/skills](https://github.com/vercel-labs/skills) | +4,758 | 37,660 | 12.6% | 75+ harness 分发 CLI |
| 18 | [flutter/flutter](https://github.com/flutter/flutter) | +2,343 | 180,988 | 1.3% | 跨平台 |
| 19 | [android/skills](https://github.com/android/skills) | +2,618 | 10,244 | 25.6% | Android 官方 skills |

> 本月榜抓到 19 条，完整清单见原始数据快照。

## 三、本周涨星 TOP 10

| 排名 | 仓库 | 本周涨星 | 涨星/存量比 | 判读 |
| ---: | --- | ---: | ---: | --- |
| 1 | [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | +12,017 | 12.1% | 首次进周榜 |
| 2 | [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | +11,566 | **25.7%** | 新项目爆发 |
| 3 | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | +10,069 | 17.8% | 降温 33% |
| 4 | [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | +6,926 | 18.0% | 环比 +291% |
| 5 | [YuJunZhiXue/dsh-purge](https://github.com/YuJunZhiXue/dsh-purge) | +6,644 | **42.8%** | 新项目爆发 |
| 6 | [affaan-m/ECC](https://github.com/affaan-m/ECC) | +6,299 | 2.1% | 持续吸量 |
| 7 | [obra/superpowers](https://github.com/obra/superpowers) | +5,896 | 1.9% | 持续吸量 |
| 8 | [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | +5,852 | 5.3% | 持续吸量 |
| 9 | [JetBrains/thinkrail](https://github.com/JetBrains/thinkrail) | +5,760 | **82.2%** | 比例最高 |
| 10 | [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | +5,432 | 4.5% | 存量走量 |

## 四、新锐仓库（近 30 天新建）

| 仓库 | star | 存活天数 | 方向 |
| --- | ---: | ---: | --- |
| [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) | 49,347 | 15 | 电视盒子卸载 |
| [deepseek-ai/DeepInfer](https://github.com/deepseek-ai/DeepInfer) | 24,861 | 16 | **DeepSeek 推理框架开源** |
| [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | 23,834 | 24 | 等距图 skill |
| [google-research/harness2](https://github.com/google-research/harness2) | 21,925 | 26 | 上期已深读 |
| [openai/math](https://github.com/openai/math) | 17,253 | 26 | Lean 数学证明 |
| [storytold/wordcraft](https://github.com/storytold/wordcraft) | 16,972 | 25 | Word 复刻 |
| [tangency-labs/solidcraft](https://github.com/tangency-labs/solidcraft) | 12,943 | 25 | 参数化 3D CAD + MCP |
| [deepseek-ai/dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype) | 8,965 | **1** | **DeepSeek Agent 原型** |
| [T-Auto/dsh-ops](https://github.com/T-Auto/dsh-ops) | 5,014 | 24 | **DSH 插件：省 token** |
| [heydamir/unslop](https://github.com/heydamir/unslop) | 5,019 | 3 | 反 AI 味 UI |

**DeepSeek 一周开源了两件不同类型的东西**：推理框架 `DeepInfer`（Apache-2.0，主打 batch-invariant inference、deterministic sampling、structured outputs，支持 NVIDIA SM100 与昇腾 950）和 Agent 原型 `dsh-superagent-prototype`（MIT）。前者是模型服务层，后者是 Agent 运行时层——同时开源两侧，说明内部是连着做的。

`storytold` 批量复刻现象本期降温：新锐榜只剩三个，合计 31,375 star，上期是 9 个、合计 169,762 star。**连续两周出现容易误判，本周数据说明它更像一次性造星脉冲，不是稳定产线。**

## 五、本周判断

1. **Skill / plugin / harness 类吞掉周榜 13/16，AI 味设计四件套单周吸走三万 star。** `hallmark`（+11,566）、`impeccable`（+12,017）、`taste-skill`（+5,336）、`jakubkrehel/skills`（+1,607）合计 30,526，占周榜总涨星 96,086 的 **31.8%**。关键变化在**形态**：`hallmark` 把 gate 分成 **Floor / Reflex / Finish** 三档——Floor 永不发布、Reflex 需留推翻理由、Finish 不阻塞。**设计审美从「偏好」变成了 harness 里可执行、可记录、可推翻的检查项。** 另一面是留榜项目在升温（`t3code` +291%）——**上期「留榜全部降温」的结论本周不成立，撤掉。**
2. **IDE 厂商不再只做插件宿主，JetBrains 自己下场做 agentic IDE。** `thinkrail` 涨星比 **82.2%**（+5,760 / 7,010），全榜最高——7,010 star 就拿到这个比例，流量几乎全来自本周。它把 `pi` coding agent 装进真 IDE：worktree 隔离、`SPEC.md` 图谱当唯一事实源、MCP server 调用逐次征求同意、可直连公司 LLM 网关。**当 IDE 厂商自己提供 Agent 运行时，「插件宿主」这个位置就不安全了。**
3. **DeepSeek 开源的不是模型，是一套完整的 Agent 授权模型。** `dsh-superagent-prototype` 1 天 8,965 star。抽象层是 **Policy / Eval / Mandate / Ticket / Assignment / Subscription** 七个概念，加上 **explicit / inferred / not admitted** 三档触发强度——**权限是一等公民，且权限变更不追溯撤销已发出的授权**。这是公开材料里**最接近「Agent 平台该长什么样」的设计**，与 W43 的 A2A 调研同题：前者管跨系统，后者管跨信任边界。
4. **「插件」有两套互不兼容的语义，两家正往相反方向长。** `cursor/plugins` 15,039 star（月 +5,809，38.6%），130+ 个插件里**绝大多数是第三方 SaaS 连接器**——Salesforce、Capital IQ、Playwright，核心是「让模型接上系统」；同期 `anthropics/knowledge-work-plugins`（月 +8,486）走「11 个岗位角色包」，核心是「教模型做事」。**前者是接口层，后者是知识层**——自建平台要先选定建哪一层。
5. **一个 harness 生态的健康度，不看它自己有多少 star，看有多少第三方愿意在上面建插件——以及有多少人在拆它的护栏。** `dsh-purge`（+6,644，42.8%，v1.1.88，Apache-2.0）是一个**有版本号、有 release、进了 3 个目录站**的红队越狱工具；`T-Auto/dsh-ops`（5,014 star）做「减少 token 消耗」的 DSH 插件。**生态在长，但长出来的一半是攻击面**——**harness 的护栏必须当成对外攻击面来设计**。

## 六、数据口径与局限

- 涨星数一律采用 GitHub Trending 页面自带的官方口径（`stars this week` / `this month`），不做二次推算。
- GitHub REST `/stargazers` 接口已全量下线，无法自算任意窗口的精确涨星；OSS Insight 等第三方数据自 2026-05 起严重降级，仅作趋势下界，本期未采用。
- Trending 榜单每页仅 15 个条目（GitHub 已从 25 下调），本周抓到 **16 条**——**不等于「Top 15 之外没有更多」**。
- 「涨星/存量比」= 涨星 ÷ 总 star，区分「新项目爆发」与「大项目持续吸量」，对新项目天然偏高；「新锐仓库」由 GitHub Search API 按 `created:` 过滤近 30 天按 star 排序，与周榜口径不同，两表不可相加。
- 第一节「榜位」是 **Trending 页面顺序**（趋势分排名），**不是涨星排名**；涨星排名见第三节，第二节按涨星降序重排。仓库状态数据是 REST API 抓取时刻的快照，会随时间变化。

## 下一步

- 按下面的深读逐个展开，或挑感兴趣的仓库看
- 想看这轮升温背后的协议动向 → [A2A 协议行业深度调研](../../industry/a2a-protocol.md)

## 如果你想

- 想知道这些 Agent Skill 该怎么组织 → [AI Native 方法论](../../../ai-harness/index.md)
- 想比较各家 Agent 工具形态 → [AI 工具全景](../../../ai-coding/tools/overview.md)
- 想看可复用组件 → [开源项目推荐](../../research-highlights/open-source.md)

## 本期深读

| 仓库 | 一句话 · 方向 |
| --- | --- | --- |
| [deepseek-ai/dsh-superagent-prototype](./dsh-superagent.md) | 权限一等公民 · 授权模型 |
| [JetBrains/thinkrail](./thinkrail.md) | 厂商亲自下场 · Harness |
| [obra/superpowers](./superpowers.md) | 强制工作流 · 方法论 |
| [anthropics/skills](./anthropic-skills.md) | 官方源 + 规范 · 标准 |
| [cursor/plugins](./cursor-plugins.md) | 主体是连接器 · 插件 |
| [thedotmack/claude-mem](./claude-mem.md) | 递进检索 · 记忆系统 |
| [vercel-labs/skills](./vercel-skills.md) | 75+ harness 分发 · 分发 |
| [Nutlope/hallmark](./hallmark.md) | 三档 gate · 规则化 |
| [AgriciDaniel/claude-seo](./claude-seo.md) | 站点可被 Agent 读 · 发现性 |
| [deepseek-ai/DeepInfer](./deepinfer.md) | 批量不变推理 · 推理 |
